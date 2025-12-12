#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2024 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#
import logging
import csv
import os
import traceback


import pandas as pd

from csv import Dialect
from io import StringIO
from pathlib import Path

def _find_bad_line_number(file_path: Path | str = None, buffer: bytes | str = None):
    try:
        if file_path:
            buffer = file_path.read_text()

        reader = csv.reader(buffer)
        linenumber = 1
        try:
            for row in reader:
                linenumber += 1
        except Exception as e:
            return linenumber
    except:
        pass
    return -1


def log_trace(s):
    print("\tTRACE CSV:", s)

def evaluate_csv_quality(df, expected_rows=None):
    """
    Evaluate the quality of a CSV parsing result.
    Returns a score (higher is better) based on:
    - Column uniformity (fewer NaN/empty values)
    - Data type consistency
    - Reasonable column count
    - Row count (if expected_rows provided)
    """
    if df is None or len(df) == 0:
        return -1.0
    
    score = 0.0
    
    # CRITICAL: If we have expected row count, heavily penalize options that lose rows
    # This catches cases where wrong quotechar causes rows to be skipped
    if expected_rows is not None and expected_rows > 0:
        row_ratio = len(df) / expected_rows
        if row_ratio < 0.5:
            # Lost more than half the rows - very bad
            score -= 200.0 * (0.5 - row_ratio)
        elif row_ratio < 0.8:
            # Lost 20-50% of rows - bad
            score -= 100.0 * (0.8 - row_ratio)
        elif row_ratio > 1.1:
            # Got more rows than expected (might be splitting incorrectly) - slightly bad
            score -= 20.0 * (row_ratio - 1.1)
        else:
            # Row count is close to expected - reward this
            score += 50.0 * (1.0 - abs(1.0 - row_ratio))
    
    # Penalize extremely high column counts (>200 is suspicious)
    if len(df.columns) > 200:
        score -= 100.0 * (len(df.columns) - 200) / 200
    
    # Reward reasonable column counts (10-100 is typical)
    if 10 <= len(df.columns) <= 100:
        score += 50.0
    elif 100 < len(df.columns) <= 200:
        score += 25.0
    
    # Evaluate column uniformity: check a sample of columns for NaN rates
    # Good CSVs should have most columns with reasonable fill rates
    sample_cols = min(20, len(df.columns))
    sampled_cols = df.columns[:sample_cols] if len(df.columns) > sample_cols else df.columns
    
    total_nan_rate = 0.0
    uniform_cols = 0
    for col in sampled_cols:
        nan_rate = df[col].isna().sum() / len(df)
        total_nan_rate += nan_rate
        
        # Columns with <90% NaN are considered "uniform" (have actual data)
        if nan_rate < 0.9:
            uniform_cols += 1
    
    avg_nan_rate = total_nan_rate / len(sampled_cols) if len(sampled_cols) > 0 else 1.0
    
    # Reward lower NaN rates (more uniform data)
    score += (1.0 - avg_nan_rate) * 30.0
    
    # Reward having many columns with actual data
    uniform_ratio = uniform_cols / len(sampled_cols) if len(sampled_cols) > 0 else 0.0
    score += uniform_ratio * 20.0
    
    # Penalize if we have too many completely empty columns
    empty_cols = sum(1 for col in df.columns if df[col].isna().all())
    empty_ratio = empty_cols / len(df.columns) if len(df.columns) > 0 else 1.0
    score -= empty_ratio * 30.0
    
    return score

def count_newlines(s):
    parts = s.split("\n")
    return len(parts)

def check_excel_utf16_nonsense(file_path: str):
    with open(file_path, "rb") as fp:
        try:
            bytes = fp.read(16)
            if bytes[0] == 0xEF and bytes[1] == 0xBB and bytes[2] == 0xBF:
                # print("CRAZY STUFF MAN")
                return True
        except:
            return False
        
    return False

from pathlib import Path
# A wrapper for dealing with CSV files.
def featrix_wrap_pd_read_csv(
    file_path: str | Path = None, 
    on_bad_lines="skip",
    trace=True
):
    """
    If you want to split CSVs in your notebook and so on when working
    with Featrix, this function should be used to capture the extra work
    around pandas' `pd.read_csv` that you'll want for best performance
    with Featrix. We will add split and a way to get back the test df
    to the client in a future release.

    Any column with an 'int' type -- meaning there doesn't seem to be a
    header line in the CSV -- will be renamed to `column_N`.

    Parameters
    ----------
    file_path : str
        Path to the CSV on your local system.
    on_bad_lines: str
        What to do with bad lines. By default, we 'skip', but you may want to 'error'.
        This is passed directly to `pd.read_csv`.
    trace: bool
        Trace path through this code for debugging on problematic files.

    This can raise exceptions if the file is not found or seems to be empty.

    """
    if trace:
        if file_path:
            print(f"featrix_wrap_pd_read_csv called with file_path={file_path}")
        print(f"featrix_wrap_pd_read_csv: on_bad_lines = {on_bad_lines}")

    df = None
    if not file_path:
        raise ValueError(
            "No data provided via buffer or path to featrix_wrap_pd_read_csv"
        )
    if file_path:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No such file {file_path}")
        # get the size of the file
        sz = os.path.getsize(file_path)
        if sz == 0:
            raise Exception(f"The file {file_path} appears to be 0 bytes long.")

        hasSillyStuff = check_excel_utf16_nonsense(file_path)
        if hasSillyStuff:
            new_file = str(file_path) + ".cleaned"
            with open(new_file, "wb") as fp_new:
                with open(file_path, "rb") as fp_old:
                    fp_old.seek(3)
                    try:
                        data = fp_old.read()
                        fp_new.write(data)
                    except:
                        print("error copying file...")
                        traceback.print_exc()
            if trace:
                log_trace(f"new file created without Excel bytes: {file_path} -> {new_file}")
            file_path = new_file

    dialect = None
    has_header = True
    input_size = os.path.getsize(file_path)
    if trace:
        log_trace(f"input_size of {file_path} --> {input_size}")

    # get the file size and adjust the sampling based on that.
    assert input_size is not None

    sample = None
    sample_size = int(input_size * 0.20)
    if sample_size < (32 * 1024):
        sample_size = 32 * 1024
    if input_size < sample_size:
        sample_size = input_size - 1

    if trace:
        log_trace(f"sample_size = {sample_size}")

    # sniff
    sniffer = csv.Sniffer()
    # check for a gzip header first.
    def has_gzip_header(buffer):
        # GZIP files start with these two bytes
        GZIP_MAGIC_NUMBER = b'\x1f\x8b'
        return buffer.startswith(GZIP_MAGIC_NUMBER)
    
    # XXX: need to see if it's an XLSX file...

    if trace:
        log_trace("checking if it's a gzip file...")
    with open(file_path, "rb") as gzip_file:
        possible_header = gzip_file.read(10)
        if has_gzip_header(possible_header):
            if trace:
                log_trace("we got a gzip header, trying to gunzip it...")
            
            # uncompress it first.
            # print(f"file_path = __{file_path}__")
            # print(os.system(f"ls {str(file_path)}*"))
            os.rename(file_path, f"{file_path}.gz")
            rc = os.system(f"gunzip -k -t \"{file_path}.gz\"")
            log_trace(f"gunzip returned {rc}")
            file_path = Path(str(file_path) + ".gz")

    log_trace(f"working with file_path = {file_path}")

    with open(file_path, newline="", errors='ignore') as csvfile:
        attempts = 0
        all_good = False
        while attempts < 10:
            if all_good: 
                if trace:
                    log_trace("all_good is True")
                break
            if trace:
                log_trace(f"file read: attempt {attempts} to read {file_path}")

            if sample_size > input_size:
                if trace:
                    log_trace(f"hitting the end of the buffer...")
                sample_size = input_size - 1

            attempts += 1
            try:
                csvfile.seek(0)
                sample = csvfile.read(sample_size)
                num_newlines = count_newlines(sample)
                if trace:
                    log_trace(f"got num_newlines = {num_newlines}")

                if num_newlines < 10:
                    if trace: 
                        log_trace(f"attempt={attempts}: Only {num_newlines} found in first {sample_size} bytes--increasing buffer size")
                    sample_size *= 2
                    continue
                else:
                    # OK, we have at least 4 lines. we're good
                    if attempts > 1:
                        if trace:
                            log_trace(f"attempt={attempts}: Found {num_newlines} in first {sample_size} bytes--proceeding")
            except Exception as e:
                bad_line = _find_bad_line_number(file_path=file_path, buffer=sample)
                if bad_line > 0:
                    if trace: 
                        log_trace(f"first BAD LINE WAS ...{bad_line}")

            try:
                dialect = sniffer.sniff(sample)
                has_header = sniffer.has_header(sample)
                all_good = True
            except Exception as err:
                sample_size *= 2
                if trace:
                    log_trace(f"attempt={attempts}: got an error: {err}... will try again... new sample size is {sample_size}")    
    if trace: 
        log_trace(f"file sniffer: sample length = {'None' if sample is None else len(sample)}, header = {has_header}, dialect delimiter = \"{dialect.delimiter if dialect is not None else 'None'}\"")

    csv_parameters = {}
    if dialect is not None:
        csv_parameters = {
            'delimiter': dialect.delimiter,
            'quotechar': dialect.quotechar,
            'escapechar': dialect.escapechar,
            'doublequote': dialect.doublequote,
            'skipinitialspace': dialect.skipinitialspace,
            'quoting': dialect.quoting,
            # Pandas does not support line terminators > 1 but Sniffer returns things like '\r\n'
            # 'lineterminator': dialect.lineterminator
        }

    # print("has_header = ", has_header)
    log_trace(f"csv_parameters = {csv_parameters}")
    log_trace(f"has_header = {has_header}")

    # SIMPLE APPROACH: Just try pd.read_csv() directly first - it usually works
    if trace:
        log_trace(f"Trying pd.read_csv() directly first (pandas default)...")
    try:
        df = pd.read_csv(
            file_path,
            on_bad_lines=on_bad_lines,
            encoding_errors='ignore',
        )
        if trace:
            log_trace(f"✅ pd.read_csv() succeeded: {len(df)} rows x {len(df.columns)} columns")
        
        # Clean up column names (strip whitespace)
        if df is not None:
            df.columns = df.columns.str.strip()
        
        # Rename int-type columns (no header detected)
        cols = list(df.columns)
        renames = {}
        for idx, c in enumerate(cols):
            if not isinstance(c, str):
                renames[c] = "column_" + str(c)
        if len(renames) > 0:
            if trace:
                log_trace(f"Renaming {len(renames)} int-type columns: {renames}")
            df.rename(columns=renames, inplace=True)
        
        return df
    except Exception as e:
        if trace:
            log_trace(f"⚠️  pd.read_csv() failed: {e}")
            log_trace(f"Falling back to CSV sniffer approach...")
    
    # FALLBACK: Use CSV sniffer if direct read fails
    if has_header:
        if trace:
            log_trace(f"has_header = {has_header}")
        try:
            df = pd.read_csv(
                file_path,
                on_bad_lines=on_bad_lines,
                encoding_errors='ignore',
                **csv_parameters
            )
            if trace:
                log_trace(f"file_path={file_path}: loaded {len(df)} x {len(df.columns)}")

            cols = list(df.columns)
            if len(cols) <= 1:
                if trace:
                    log_trace(f"only got {len(cols)} ... trying without our sniffed parameters")
                df = pd.read_csv(
                    file_path,
                    on_bad_lines=on_bad_lines,
                    skipinitialspace=True,
                    encoding_errors='ignore',
                )
                if trace:
                    log_trace(f"{file_path}: loaded {len(df)} x {len(df.columns)}")
                
                return df
        except pd.errors.EmptyDataError as err:
            if trace:
                log_trace(f"{file_path} - got a pandas EmptyDataError: {err}")
            return None
        
        except pd.errors.ParserError as err:
            if trace:
                log_trace(f"{file_path} - got a pandas ParserError: {err}")
            
            try:
                df = pd.read_csv(
                        file_path,
                        # Pandas doesn't take the same dialect as csv.Sniffer produces so we create csv_parameters
                        # dialect=dialect,
                        on_bad_lines=on_bad_lines,
                        skipinitialspace=True,
                        encoding_errors='ignore',
                    )
                if trace:
                    log_trace(f"{file_path}: loaded {len(df)} x {len(df.columns)}")
            except:
                traceback.print_exc()
                if trace:
                    log_trace(f"tried again with no parameters and still had an error")

        except csv.Error as err:
            bad_line = _find_bad_line_number(file_path=file_path)
            if bad_line > 0:
                if trace: 
                    log_trace(f"read_csv() - first BAD LINE WAS ...{bad_line}")

            s_err = str(err)
            if trace:
                log_trace(f"read_csv() -> error -> {s_err}")

            # FIXME: Not sure if there is something we can do if the buffer is hosed?
            if (
                s_err is not None
                and s_err.find("malformed") >= 0
                and file_path is not None
            ):
                df = pd.read_csv(
                        file_path,
                        # Pandas doesn't take the same dialect as csv.Sniffer produces so we create csv_parameters
                        # dialect=dialect,
                        on_bad_lines=on_bad_lines,
                        skipinitialspace=True,
                        lineterminator="\n",
                        **csv_parameters
                    )
                if trace:
                    log_trace(f"{file_path}: loaded {len(df)} x {len(df.columns)}")
            else:
                if trace: 
                    log_trace("c'est la vie")
                raise err
            # endif

        # if any of the columns have an 'int' type, rename it.
        if df is not None:
            if trace:
                log_trace(f"df is not None... checking for crazy columns... {len(df.columns)} columns found.")
            
            cols = list(df.columns)
            renames = {}
            for idx, c in enumerate(cols):
                if not isinstance(c, str):
                    renames[c] = "column_" + str(c)
            log_trace(f"renames = {renames}")
            if len(renames) > 0:
                if trace:
                    log_trace(f"renaming some columns: {renames}")
                df.rename(columns=renames, inplace=True)

        if trace:
            log_trace(f"returning {df} with columns {list(df.columns)}")

        if df is not None:
            df.columns = df.columns.str.strip()

        return df

    if not has_header:
        if trace:
            log_trace(f"has_header = {has_header}")
            log_trace(f"trying again -- csv_parameters = {csv_parameters}")

        try:
            df = pd.read_csv(file_path,
                             on_bad_lines=on_bad_lines,
                             skipinitialspace=True,
                             **csv_parameters)
            if trace:
                log_trace(f"{file_path}: loaded {len(df)} x {len(df.columns)}")

            cols = list(df.columns)
            if len(cols) >= 0:
                count_unnamed_columns = 0
                for col_name in cols:
                    if col_name.startswith("Unnamed"):
                        count_unnamed_columns += 1

                if count_unnamed_columns == len(cols):
                    # still no good.
                    raise Exception(
                        f"CSV file {file_path} doesn't seem to have a header line, which means it does not "
                        "have labels for the columns. This will make creating predictions on "
                        "specific targets difficult!"
                    )
            if len(cols) == 1:
                # need to try again with a bigger sample_size.
                log_trace("only 1 col... going to force a retry")
                raise Exception("going to force a retry")
            
            if df is not None:
                df.columns = df.columns.str.strip()
            return df
        except Exception as err:  # noqa - catch anything
            if trace:
                log_trace(f"trying again with no parameters specified")

            # OK, maybe the csv parameters are crap.
            df = pd.read_csv(file_path, skipinitialspace=True)
            if trace:
                log_trace(f"{file_path}: loaded {len(df)} x {len(df.columns)}")
            cols = list(df.columns)

            if trace:
                log_trace(f"df = {len(df)} rows x = {cols} cols")
            if len(cols) >= 0:
                count_unnamed_columns = 0
                for col_name in cols:
                    if col_name.startswith("Unnamed"):
                        count_unnamed_columns += 1

                if count_unnamed_columns == len(cols):
                    raise Exception(
                        f"CSV file {file_path} doesn't seem to have a header line, which means it does not "
                        "have labels for the columns. This will make creating predictions on specific targets difficult! [2]"
                    )
                if df is not None:
                    df.columns = df.columns.str.strip()
                return df
            else:
                raise Exception(
                        f"CSV file {file_path} doesn't seem to have a multiple columns that we could detect"
                    )

    if trace:
        log_trace(f"returning {df} at the bitter end")
    if df is not None:
        df.columns = df.columns.str.strip()
    return df
