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

from vector_db import CSVtoLanceDB

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


from featrix.neural.io_utils import load_embedded_space

# #sys.path.append(".")

# class LightTrainingArgs:
#     epochs: int = 500
#     row_limit: int = 25000
#     is_production: bool = True
#     input_file: str = "test.csv"
#     ignore_cols: List[str] = []
#     learning_rate: float = 0.001
#     batch_size: int = 1024

def train_knn(es_path: Path, sqlite_db_path: Path, job_id: str = None):
    print("Hello!")

    logging.getLogger().handlers.clear()  # Remove all handlers
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, format="%(asctime)s [%(levelname)-8s] %(name)-45s: %(message)s")
    logger = logging.getLogger(__name__)

    # Force CPU for KNN training (doesn't need GPU)
    from featrix.neural.device import set_device_cpu
    set_device_cpu()
    logger.info("🖥️  KNN training running on CPU (GPU not needed for vector DB operations)")

    # load the ES...
    job_uuid = "bob"
    # es = load_embedded_space("embedded_space.pickle")
    es = load_embedded_space(str(es_path))
    vector_db = CSVtoLanceDB(featrix_es=es, sqlite_db_path=sqlite_db_path, job_id=job_id)
    vector_db.create_table()

    print("--finished--")
    # 

    return vector_db.get_output_files()


if __name__ == "__main__":
    print("Starting up!")
    train_knn(
        model_path=Path("embedded_space.pickle"),
        input_file=Path("test.csv")    
    )


