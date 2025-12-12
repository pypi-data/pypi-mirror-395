#!/usr/bin/env python3
"""
Wrapper script to run ES training in a non-daemon process.

This script is executed by Celery workers via fork/exec to create a new
session leader process that can spawn DataLoader workers for maximum GPU utilization.
"""
import json
import logging
import os
import socket
import sys
import traceback
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set up logging with same format as Celery job logging
# This ensures consistent log format in the job log file
logging.basicConfig(
    level=logging.INFO,
    format=f'%(asctime)s [{socket.gethostname()}] [%(levelname)-8s] %(name)-45s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    stream=sys.stdout  # Write to stdout (inherited from parent, redirected to log file)
)

from lib.es_training import train_es, LightTrainingArgs

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='ES training wrapper')
    parser.add_argument('args_json_file', help='JSON file containing training arguments')
    parser.add_argument('--job-id', help='Job ID (visible in /proc for process identification)', default=None)
    parsed_args = parser.parse_args()
    
    args_file = parsed_args.args_json_file
    job_id = parsed_args.job_id
    
    # Store job_id in environment so child processes can inherit it
    # This makes it visible in /proc/<pid>/environ as well
    if job_id:
        os.environ['FEATRIX_JOB_ID'] = job_id
    
    # Load args from JSON file
    with open(args_file, 'r') as f:
        args_dict = json.load(f)
    
    # Create LightTrainingArgs object
    args = LightTrainingArgs(**args_dict)
    
    # Run training
    try:
        train_es(args)
        sys.exit(0)
    except Exception as e:
        print(f"Training failed: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)
