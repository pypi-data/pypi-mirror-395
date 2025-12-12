#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2024 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

from typing import Any


import hashlib
import os
import traceback
import logging
from featrix.neural.featrix_csv import featrix_wrap_pd_read_csv
from featrix.neural.featrix_json import featrix_wrap_read_json_file
from featrix.neural.sqlite_utils import check_sqlite_header, load_sqlite_file_to_df
from featrix.neural.integrity import FeatrixDataIntegrity

logger = logging.getLogger(__name__)


def is_gzip(filename):
    with open(filename, 'rb') as file:
        file_header = file.read(2)
        return file_header == b'\x1f\x8b'

import pandas as pd


# def is_sqlite(filename):
#     with open(filename, 'rb') as file:
#         file_header = file.read(16)
#         return file_header == b'SQLite format 3\0'

class FeatrixInputDataFile:
    def __init__(
        self,
        filename: str
    ):
        assert filename is not None
        assert type(filename) == str, f"filename must be a str, not a {type(filename)}"

        try:
            self.debugFilePath = (
                os.path.realpath(filename) if filename is not None else None
            )
        except:
            traceback.print_exc()

        if is_gzip(filename): #filename.endswith(".gz"):
            logger.info(f".... unzipping {filename}")
            rc = os.system(f"gunzip -f \"{filename}\"")
            logger.info(f"gunzip returned {rc}")
            if rc != 0:
                if os.path.exists(filename[:-3]):
                    # already unzipped... a re-run of a job. should do this in a better way.
                    pass
                else:
                    # NOTE: why not just throw an exception?
                    assert rc == 0, "Failed to gunzip data"
            filename = filename[:-3]  # chop .gz
        else:
            # we have to set up the file name correctly or pd.read() will get angry.
            if filename.endswith(".gz"):
                # If this clause triggers, we have a file that's NOT a gzip file, but
                # it does have a gzip extension. 
                # In this case we just cut off the extension.
                # BUT: why would this ever happen?
                os.rename(filename, filename[:-3])
                filename = filename[:-3]  # chop .gz

        # If the filename ends with ".sqlite3" but the file contents is not
        # really an sqlite database, we cut off the sqlite3 suffix.
        # NOTE: this seems to indicate that something's gone wrong - why not bail?
        if filename.endswith(".sqlite3"):
            if not check_sqlite_header(filename):
                # assume CSV
                logger.info("looking like a good day / to be a csv~~~")
                new_name = filename[:-(len(".sqlite3"))]
                os.rename(filename, new_name)
                filename = new_name

        self.debugFileName = filename
        self.debugFileSize = 0
        self.debugFileHash = 0
        self.integrity_file_name = f"integrity-dump-df-{os.path.basename(filename)}.json"
        
        # Why would filename ever be None here? There's an explicit assert to that end
        # at the top of of this method.
        if filename is not None:
            st = os.stat(filename)
            self.debugFileSize = st.st_size
            # Get the hash of the file contents
            with open(filename, "rb") as fp:
                try:
                    self.debugFileHash = hashlib.md5(fp.read()).hexdigest()
                except:
                    # print()....
                    logger.info.print_exc()
                    print("[continuing anyway]")

            # see if it's a SQL file
            if check_sqlite_header(filename):
                logger.info(f"{filename} is a SQLite db")
                self._df = load_sqlite_file_to_df(filename)
            else:
                # Check file extension to determine file type
                file_ext = os.path.splitext(filename)[1].lower()
                if file_ext == '.parquet':
                    # Parquet file
                    logger.info(f"{filename} is a Parquet file - reading with pandas...")
                    try:
                        self._df = pd.read_parquet(filename)
                        logger.info(f"✅ Parquet file loaded successfully: {len(self._df)} rows x {len(self._df.columns)} columns")
                    except Exception as e:
                        logger.error(f"❌ Failed to read Parquet file: {e}")
                        raise ValueError(f"Failed to parse Parquet file {filename}: {e}")
                elif file_ext in ('.json', '.jsonl'):
                    # JSON/JSONL file
                    logger.info(f"{filename} is a JSON/JSONL file - reading...")
                    self._df = featrix_wrap_read_json_file(file_path=filename)
                    if self._df is None:
                        logger.warning(f"JSON parsing failed for {filename}, trying CSV fallback...")
                        self._df = featrix_wrap_pd_read_csv(filename, trace=True)
                else:
                    # Assume CSV (or try JSON first, then CSV)
                    logger.info(f"{filename} - trying JSON first, then CSV...")
                    self._df = featrix_wrap_read_json_file(file_path=filename)
                    if self._df is None:
                        self._df = featrix_wrap_pd_read_csv(filename, trace=True)
            
            # always dump integrity stats of what we took in.
            try:
                integrity = FeatrixDataIntegrity(self._df)
                integrity.dump_file(self.integrity_file_name)
            except:
                traceback.print_exc()

            df_str = ""
            if self.df is None:
                df_str = "[is None]"
            else:
                try:
                    df_str = f"[{len(self.df.columns)} x {len(self.df)}]"
                except:
                    df_str = "[error trying to get dimensions]"
            logger.info(f"FeatrixInputDataFile: df = {df_str}")
            logger.info(f"df type    = {type(self.df)}")
            if self._df is not None:
                # Log columns in same format as CSV/SQLite loading for consistency
                logger.info(f"📋 Columns found after loading ({len(self.df.columns)} total): {list(self.df.columns)[:50]}{'...' if len(self.df.columns) > 50 else ''}")
                if len(self.df.columns) > 50:
                    logger.info(f"   ... and {len(self.df.columns) - 50} more columns")
        else:
            self.debugFileName = "pandas dataframe was passed by called; file unknown"
        # endif


    def get_filtered_df(self, target_column):
        """
        Returns a df with none of the rows that have Nones/nulls/nans in the specified column -- i.e., filter them out.
        """
        assert target_column in self._df.columns, f"Expected column {target_column} to be in {self._df.columns}"

        df = self._df[self._df[target_column].notna()]

        return df

    @property
    def df(self):
        return self._df

    def sample_df(self, max_rows):
        if max_rows > len(self._df):
            self._df = self._df.sample(max_rows)
            self._df.reset_index()
        return

