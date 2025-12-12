#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2025 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#
import copy

import logging
import sys
import os
from pathlib import Path
from typing import List
import time
import traceback

try:
    from featrix.neural import device
except ModuleNotFoundError:
    p = Path(__file__).parent
    sys.path.insert(0, str(p))
    from featrix.neural import device

from featrix.neural.embedded_space import EmbeddingSpace

from featrix.neural.input_data_file import FeatrixInputDataFile
from featrix.neural.input_data_set import FeatrixInputDataSet

# from vector_db import CSVToFAISS

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)-8s] %(name)-45s: %(message)s")

logger = logging.getLogger(__name__)


# Removed test debug messages


for noisy in [
    "aiobotocore",
    "asyncio",
    "botocore",
    "com",
    "fastapi",
    "dotenv",
    "concurrent",
    "aiohttp",
    "filelock",
    "fsspec",
    "httpcore",
    "httpx",
    "requests",
    "s3fs",
    "tornado",
    "twilio",
    "urllib3",
    "com.supertokens",
    "kombu.pidbox"
]:
    logging.getLogger(noisy).setLevel(logging.WARNING)

from render_sphere import write_preview_image

from featrix.neural.io_utils import load_embedded_space
import sqlite3
import json

import pandas as pd
from featrix.neural.es_projection import ESProjection

import numpy as np

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()  # Convert NumPy array to list
        return super().default(obj)

def run_clustering(model_path, sqlite_db_path):
    print("Hello!")

    logging.getLogger().handlers.clear()  # Remove all handlers
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(asctime)s [%(levelname)-8s] %(name)-45s: %(message)s")
    logger = logging.getLogger(__name__)

    es = load_embedded_space(model_path)

    sql_conn = sqlite3.connect(sqlite_db_path)
    assert sql_conn is not None
    
    df = pd.read_sql_query("SELECT rowid AS __featrix_row_id, * from data ORDER BY rowid", sql_conn)

    projection = ESProjection(es=es, df=df, sqlite_conn=sql_conn)
    projection_js = projection.run()

    with open("embedded_space_projections.json", "w") as fp:
        json.dump(projection_js, fp, cls=NumpyEncoder)

    assert os.path.exists("embedded_space_projections.json")

    sphere_file = "sphere_preview.png"
    try:
        write_preview_image("embedded_space_projections.json", sphere_file)
    except:
        traceback.print_exc()
        sphere_file = None

    return { "projections": "embedded_space_projections.json", "preview_png": sphere_file }


if __name__ == "__main__":
    print("Starting up!")
    run_clustering()


