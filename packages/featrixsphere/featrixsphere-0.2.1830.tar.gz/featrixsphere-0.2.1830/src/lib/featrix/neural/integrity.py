#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2024 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

import hashlib
import logging
import json
import os
import pandas as pd
import pickle
import sys
import traceback

logger = logging.getLogger(__name__)

FEATRIX_FOUND_NULL = "FEATRIX_FOUND_NULL"

class FeatrixDataIntegrity:
    """
    This class computes integrity for a given data frame.
    """
    def __init__(self, df):
        self.full_df = df
        self.full_null_counts = self._compute_full_null_counts()

        self.sample_indices = []
        self.sample_df = None
        self.sample_row_checksums = None
        self.sample_col_checksums = None
        
        self.embedding_info = None
        self.full_nulls = None

        self._sample_rows()
        self._compute_sample_col_checksums()
        self._compute_sample_row_checksums()
    
        self._check_embedding_columns()
        self._check_full_nulls()

    def _check_embedding_columns(self):
        # FIXME: need to figure out what to do here.
        
        def build_embedding_column_details(c):
            thisCol = []
            for idx, row in self.full_df.iterrows():
                prefix = ""
                v = row[c]
                d = {}
                d['col_name'] = c
                d['idx'] = idx
                v_is_nan = None
                try:
                    if v != v:
                        v_is_nan = True
                except Exception as e:
                    from torch import is_tensor
                    if is_tensor(v):
                        v_is_nan = False
                    else:
                        raise e
                if v_is_nan or v is None:
                    d['was_null'] = FEATRIX_FOUND_NULL
                    thisCol.append(d)
                    continue
                d['was_null'] = False
                if isinstance(v, memoryview):
                    #pickle.dumps(v)
                    blob = pickle.loads(v)
                    # print(type(blob))
                    if blob is None:
                        v = None
                    else:
                        try:
                            if type(blob) == dict:
                                assert False, "we should not have a dict, should we???"
                                ks = list(blob.keys())
                                print(ks)
                                v = blob.get(ks[0])
                            elif type(blob) == list:
                                v = blob
                            else:
                                print("dunno what this is...", type(v))
                                v = blob 
                        except:
                                traceback.print_exc()
                    prefix += "pickled_array,"
                if v_is_nan or v is None:
                    d["was_pickled_null"] = True
                    thisCol.append(d)
                    continue

                if type(v) == str:
                    if v[0] == '[' and v[-1] == ']':
                        v = v[1:-1]
                        parts = v.split(",")
                        vv = []
                        had_error = []
                        for idx, p in parts:
                            try:
                                v.append(float(p))
                            except:
                                had_error.append(idx)
                        assert len(had_error) == 0, f"Had errors in row {idx} parsing string embedding vector at positions {had_error}"
                        v = vv
                        prefix += "string array,"
                # not elif -- we fall through if we have converted from a string
                if type(v) == list:
                    d['vector_len'] = len(v)
                    num_bad_values = 0
                    num_cast_errors = 0
                    num_good_floats = 0
                    num_zeros = 0
                    for x in v:
                        if x != x or x is None:
                            num_bad_values += 1
                        else:
                            try:
                                num_x = float(x)
                                num_good_floats += 1
                                if num_x == 0:
                                    num_zeros += 1
                            except:
                                num_cast_errors += 1
                    prefix += "list of floats"
                    d['num_bad_values']  = num_bad_values
                    d['num_cast_errors'] = num_cast_errors
                    d['num_good_floats'] = num_good_floats
                    d['num_zeros_in_embedding'] = num_zeros
                    d['prefix'] = prefix
                    thisCol.append(d)
                else:
                    str_v = "[failed]"
                    try:
                        str_v = str(v)
                        str_v = str_v[:100]
                        str_v += "..."
                    except:
                        pass
                    d['prefix'] = prefix
                    d["error"] = f"unexpected type of value in embedding column {c}: {type(v)}...{str_v}"
                    thisCol.append(d)
                # endif

            return thisCol

        dd = {}
        for c in self.full_df.columns:
            if c.endswith("_embedding"):
                d = build_embedding_column_details(c)
                dd[c] = d
        
        self.embedding_info = dd
        return
    
    def _check_full_nulls(self):
        dd = {}
        for c in self.full_df.columns:
            count_nulls = self.full_df[c].isna().sum()
            dd[c] = count_nulls
        
        self.full_nulls = dd
        return

    def to_dict(self):
        d = { 
            "full_df_rows": self.nrows,
            "full_df_cols": self.ncols,
            "col_names": list(self.full_df.columns),
            "sample_df_rows": len(self.sample_df),
            "sample_df_indices": self.sample_indices,
            "sample_row_checksums": self.sample_row_checksums,
            "sample_col_checksums": self.sample_col_checksums,
            "embedding_columns": self.embedding_info,
            "full_null_counts": self.full_nulls
        }
        
        return d
    
    def dump_file(self, filename):
        with open(filename, "w") as fp:
            json.dump(self.to_dict(), fp, indent=4, default=str)
        return

    @property
    def nrows(self):
        return len(self.full_df)
    
    @property
    def ncols(self):
        return len(self.full_df.columns)
         
    def _sample_rows(self):
        if self.nrows > 2500:
            self.sample_df = self.full_df.sample(n=2500, random_state=42)
        else:
            self.sample_df = self.full_df
        self.sample_indices = list(self.sample_df.index)
        self.sample_df.reset_index()
        return
    
    def _compute_full_null_counts(self):
        d = {}
        for c in list(self.full_df.columns):
            # In Pandas, null and NaN are the same.
            # This might be ok.
            #nan_count = self.df[c].isna().sum()
            null_count = self.full_df[c].isnull().sum()
            d[c] = null_count
        return d
    
    def _compute_sample_row_checksums(self):
        assert self.sample_df is not None

        def compute_checksum(row):
            filled_row = row.fillna(FEATRIX_FOUND_NULL)
            row_str = ''.join(map(str, filled_row))
            return hashlib.sha256(row_str.encode('utf-8')).hexdigest()
        
        checksum_list = list(self.sample_df.apply(compute_checksum, axis=1))
        d = {}
        for idx, ck in enumerate(checksum_list):
            d[idx] = ck
        self.sample_row_checksums = d
        return
        
    def _compute_sample_col_checksums(self):
        
        def compute_column_checksum(col_values):
            filled_col = col_values.fillna(FEATRIX_FOUND_NULL)
            col_str = ''.join(map(str, filled_col))
            return hashlib.sha256(col_str.encode('utf-8')).hexdigest()
        
        d = {}
        
        for c in list(self.sample_df.columns):
            d[c] = compute_column_checksum(self.sample_df[c])

        self.sample_col_checksums = d
        return


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Usage: $0 <file>")
    file_name = sys.argv[1]
    
    if not os.path.exists(file_name):
        print(f"File __{file_name}__ does not exist")
        exit(1)
        
    df = pd.read_csv(file_name) 

    fdi = FeatrixDataIntegrity(df)
    print(json.dumps(fdi.to_dict(), indent=4, default=str))
    
