#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2024 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#
from collections import defaultdict
from typing import Dict
from typing import List

from pydantic import Field

from torch.utils.data import Dataset  # DataLoader,

# from featrix.models import ProjectRowMetaData
from featrix.neural.featrix_token import create_token_batch
# from featrix.neural.stopwatch import StopWatch


class ProjectRowMetaData:
    """
    When we combine datasets, we end up with a single dataset (df) with rows from each dataset.  This structure
    defines a segment in that combined dataset that corresponds to the original input.
    """

    row_idx_start: int
    num_rows: int
    columns_list: List[str] = Field(default_factory=list)
    label: str
    # This will be the % this segment represents of the entire dataset
    overall_percent: float = Field(default=0.0)
    # If we sample from this segment, we will save the original row count here in case it's needed
    original_rows: int = -1
    debug_index: int

    def contains_row(self, idx):
        # This could just be
        # return self.row_idx_start <= idx < self.row_idx_start + self.num_rows
        # but spelling it out step-by-step makes it easier to debug.

        range_start = self.row_idx_start
        range_end = self.row_idx_start + self.num_rows
        outcome = range_start <= idx < range_end
        return outcome


def collate_tokens(cinput: List) -> Dict:
    col_tokens = defaultdict(list)

    for entry in cinput:
        for col_name, token in entry.items():
            col_tokens[col_name].append(token)

    out = {}
    for col_name, tokens in col_tokens.items():
        out[col_name] = create_token_batch(tokens)

    return out


class SuperSimpleSelfSupervisedDataset(Dataset):
    def __init__(
        self,
        df,
        codecs,
        row_meta_data: List[ProjectRowMetaData] = None,
        casted_df=None
    ):
        if casted_df is not None:
            assert len(casted_df) == len(df)

        self.df = df
        self.df_column_names = list(df.columns)
        self.codecs = codecs
        self.row_meta_data = row_meta_data
        # If there's no metadata about the segments, it means that
        # the DF is just a single segment.
        self.is_single_segment = row_meta_data is None

        self.casted_df = casted_df
        # self.stopwatch = StopWatch()


    def __len__(self):
        return len(self.df)

    def column_exists_for_idx(self, col_name, idx):
        # If the DF has a single segment, just check for DF index bounds.
        if self.is_single_segment:
            return 0 <= idx < len(self.df)

        # DF is multi-segment.
        # This is a simple linear scan through segments because the
        # number of segments is expected to be small.
        for entry in self.row_meta_data:
            if entry.contains_row(idx):
                return col_name in entry.columns_list

        # Still here? That's not good.
        # Getting here means we have a hole in the row entries!
        assert False, "Incomplete row mapping. idx = %s, col_name = %s --> %s" % (
            idx,
            col_name,
            self.dumpRowMapping(col_name),
        )

    def __getitem__(self, idx):
        tokens = {}

        # The model expects to get a dictionary of tokens that it can encode, and so
        # we should return a token for every codec that is available.

        # There are 4 possible cases:

        # 1. The set of codecs and the set of DF columns are identical.
        #    This is the most straight-forward case.

        # 2. Some columns don't have a corresponding codec.
        #    These columns are completely ignored, and do not
        #    appear in the returned dictionary of tokens.

        # 3. Some codecs have no corresponding DF columns.
        #    For these codecs we use the NOT_PRESENT token.

        # 4. A column for a given codec IS present, but not part of the
        #    segment for the specified idx.
        #    This case is handled the same as if the column did not exist,
        #    i.e. the codec returns a NOT_PRESENT token.

        # Iterate over all codecs, pull out the value from the corresponding
        # DF columns at the desired idx, and tokenize the value using the codec.
        for codec_name, codec in self.codecs.items():
            # If the codec does not have a corresponding column in the DF,
            # return a NOT_PRESENT token.
            if codec_name not in self.df_column_names:
                token = codec.get_not_present_token()

            # If the codec corresponds to a field that is not available for this idx,
            # (e.g. as a result of merging datasets), return a NOT_PRESENT token.
            elif not self.column_exists_for_idx(codec_name, idx):
                token = codec.get_not_present_token()

            # Otherwise, tokenize the value in the field.
            else:
                # We must know that the column exists in the dataframe before
                # we try to retrieve it.
                use_casted_df = False
                if self.casted_df is not None and codec_name in self.casted_df.columns:
                    col = self.casted_df[codec_name]
                    use_casted_df = True
                else:
                    col = self.df[codec_name]
                try:
                    value = col.iloc[idx]
                    token = codec.tokenize(value)
                except Exception as err:
                    import traceback
                    import sys
                    print("----------------------------------------------------------------- >>>")
                    print("use_casted_df = ", use_casted_df)
                    print("codec_name = ", codec_name)
                    print("idx = ", idx)
                    print("len = ", len(col))
                    print("index = ", self.df.index, "; len = ", len(self.df.index))
                    # print("index = ", list(self.df.index))
                    traceback.print_exc(file=sys.stdout)
                    assert False, "Indexing is toast; cannot continue."
                    token = codec.get_not_present_token()

                # At this point, the only way we can have a token of type unknown is
                # if the input itself is a Nan, None, or ' ', or otherwise contained a value
                # that is interpreted as "unknown" by the codec's .tokenize method.

                # The possible statuses of the token at this point are:
                # - OK
                # - NOT_PRESENT (if the codec does not have a corresponding column in df,
                #                or corresponds to a column that came from another segment of the DF)
                # - UNKNOWN (if the value is interpreted as unknown in the codec)

                # NOTE: MARGINAL tokens are created as part of the masking process within the model
                # itself. They're assigned dynamically during training, and are not part of the dataset.

            tokens[codec_name] = token
        return tokens

    def dump_row_mapping(self, col_name):
        lines = []
        if self.row_meta_data is None:
            lines.append("row mapping is None")
        else:
            lines.append("row mapping len = %s" % len(self.dataspaceRowMetadata))
            lines.append("looking for column __%s__" % col_name)
            for idx, entry in enumerate(self.dataspaceRowMetadata):
                lines.append(
                    '\t[%s] --> row %s to row %s from label "%s" column found = %s (%s cols)'
                    % (
                        idx,
                        entry.row_idx_start,
                        entry.row_idx_start + entry.num_rows,
                        entry.label,
                        col_name in entry.columns_list,
                        len(entry.columns_list),
                    )
                )
        return "\n".join(lines)
