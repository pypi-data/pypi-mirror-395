#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2024 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

import json
import logging
import csv
import os
import traceback
from csv import Dialect
from io import StringIO
from pathlib import Path

import pandas as pd

def try_jsonl_file(file_path):

    json_dicts = []
    
    with open(file_path, 'r') as f:
        for line_number, line in enumerate(f, start=1):
            try:
                json_obj = json.loads(line.strip())
                if isinstance(json_obj, dict):
                    json_dicts.append(json_obj)
                else:
                    return None
                    #raise ValueError(f"Line {line_number} is not a valid JSON dictionary.")
            except json.JSONDecodeError as e:
                print(f"Line {line_number} is not valid JSON: {e}")
                return None
            
    if len(json_dicts) > 0:
        return pd.DataFrame(json_dicts)
    
    return None

# Example usage:
# json_data = read_jsonl_file('data.jsonl')



def featrix_wrap_read_json_file(file_path):
    """
    Read JSON or JSONL file into a pandas DataFrame.
    
    For JSONL files (one JSON object per line), tries JSONL parsing first.
    For regular JSON files, tries standard JSON parsing.
    """
    file_path_obj = Path(file_path)
    
    # Check if it's a JSONL file (by extension or by trying to parse as JSONL first)
    is_jsonl = file_path_obj.suffix.lower() == '.jsonl'
    
    if is_jsonl:
        # For JSONL files, try JSONL parsing first
        try:
            df = try_jsonl_file(file_path=file_path)
            if df is not None:
                return df
        except Exception as e:
            logging.warning(f"JSONL parsing failed for {file_path}: {e}")
            traceback.print_exc()
    
    # Try regular JSON parsing (for .json files or as fallback)
    try:
        df = pd.read_json(file_path)
        return df
    except Exception as e:
        logging.debug(f"Regular JSON parsing failed for {file_path}: {e}")
        # If it's a .jsonl file and both failed, try JSONL one more time
        if is_jsonl:
            try:
                df = try_jsonl_file(file_path=file_path)
                if df is not None:
                    return df
            except Exception as e2:
                logging.warning(f"JSONL parsing failed again for {file_path}: {e2}")
    
    # If all parsing attempts failed, return None
    logging.error(f"Failed to parse {file_path} as JSON or JSONL")
    return None
