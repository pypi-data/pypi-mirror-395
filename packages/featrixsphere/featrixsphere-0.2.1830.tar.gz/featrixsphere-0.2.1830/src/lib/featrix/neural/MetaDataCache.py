#
#  Copyright (c) 2023, Featrix, Inc. All rights reserved.
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#
#
import argparse
import hashlib
import os
import signal
import socket
import sqlite3
import sys
import time
import traceback
import pandas as pd

class MetaDataCache(object):
    def __init__(self, filename, readOnly=False):
        self._filename = filename + ".metadata"
        self.conn = sqlite3.connect(self._filename)
        self.cursor = self.conn.cursor()

        self.memCache = {}
        self._readOnly = readOnly

        if not self._readOnly:
            # self.cursor.execute("CREATE TABLE IF NOT EXISTS token_cache(string_value TEXT,max_length, bert_blob BLOB);")
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS
                    file_list(
                        file_id integer primary key,
                        file_hash blob,
                        file_path text);
                        """)


#            YOU ARE HERE -- fix this cache so we can get back useful values on the client.

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS 
                    metadata(
                        vector_idx integer UNIQUE,
                        row_idx integer,
                        file_id integer);""")
        # self.hits = 0
        # self.misses = 0

        self.files_dict = {}
        self.file_id_to_path = {}

    def count_rows(self):
        self.cursor.execute(
            """
                SELECT 
                    COUNT(*)
                FROM
                    metadata
            """)
        try:
            result = self.cursor.fetchone()
            return result[0]
        except:
            traceback.print_exc()
        return 0

    def begin(self):
        self.cursor.execute("BEGIN TRANSACTION")
        return

    def add_file(self, file_name, file_hash):
        self.cursor.execute(
            """
                SELECT file_id FROM file_list WHERE file_hash=?
            """,
            (file_hash,)
        )
        try:
            result = self.cursor.fetchall()
            if result is None or len(result) == 0:
                # got nothing; insert it.
                self.cursor.execute("""
                    INSERT INTO file_list (file_hash, file_path) VALUES (?,?)
                """, (file_hash, file_name))
                self.files_dict[file_hash] = self.cursor.lastrowid
            else:
                self.files_dict[file_hash] = result[0]
        except:
            traceback.print_exc()
        return self.files_dict.get(file_hash)

    def get_file_by_id(self, file_id):
        if self.file_id_to_path.get(file_id) is not None:
            return self.file_id_to_path.get(file_id)

        self.cursor.execute(
            """
                SELECT file_path FROM file_list WHERE file_id=?
            """,
            (file_id,)
        )
        result = self.cursor.fetchone()
        if result is not None:
            # print("result...", result)
            self.file_id_to_path[file_id] = result[0]
        return self.file_id_to_path.get(file_id)

    def add(self, vector_idx, file_id, row_idx):
        if self._readOnly:
            return
        # print(f"add: {vector_idx} {file_id} {row_idx}")
        self.cursor.execute(
            """
                INSERT INTO
                    metadata
                    (
                        vector_idx,
                        row_idx,
                        file_id
                    )
                    VALUES
                    (
                        ?, ?, ?
                    )
            """,
            (vector_idx, row_idx, file_id)
        )

        #self.conn.commit()
        return

    def commit(self):
        if self._readOnly:
            return

        self.conn.commit()
        return

    def query_all(self, focus_columns=None):
        self.cursor.execute(
            """
                SELECT 
                    vector_idx,
                    row_idx,
                    file_id
                FROM
                    metadata
                ORDER BY
                    row_idx ASC
            """)
        try:
            result = self.cursor.fetchall()
            d = {}

            df_dict = {}

            for r in result:
                # print(r)
                (vector_idx, row_idx, file_id) = r
                file_id = file_id
                df = df_dict.get(file_id)
                if df is None:
                    filePath = self.get_file_by_id(file_id)
                    # print("filePath = ", filePath)
                    assert filePath is not None

                    # FIXME: need original parameters to ensure consistency (e.g., skip bad lines...)... or write out a normalized dataframe
                    df = pd.read_csv(filePath)

                    if focus_columns is not None:
                        # FIXME: need to check for an error where focus_columns contains a column name that doesn't exist
                        new_df = pd.DataFrame()
                        for c in list(df.columns):
                            if c in focus_columns:
                                new_df[c] = df[c]
                        df_dict[file_id] = new_df
                        print("new_df = ")
                        print(new_df)
                    else:
                        df_dict[file_id] = df
                df = df_dict.get(file_id)       # do this again in case we moved things above
                assert df is not None
                print("r[0] = ", r[0])
                d[r[0]] = df.iloc[row_idx].to_dict()
            return d
        except:
            traceback.print_exc()
        return None




def main():
    c = MetaDataCache("test")

    #c.

    return


if __name__ == "__main__":
    main()