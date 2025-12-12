#!/usr/bin/env python3
"""
Recreate Featrix Session File from Trained ES and SP Outputs

Given paths to trained EmbeddingSpace and SinglePredictor output directories,
this tool reconstructs the session file that would normally be created during training.

Usage:
    python recreate_session.py --es-path /sphere/app/featrix_output/session-name/train_es/job-id \\
                               --sp-path /sphere/app/featrix_output/session-name/train_single_predictor/job-id \\
                               [--session-id SESSION_ID] [--output-dir /sphere/app/featrix_sessions]
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from zoneinfo import ZoneInfo

# Add src to path
src_path = Path(__file__).parent
if str(src_path.resolve()) not in sys.path:
    sys.path.insert(0, str(src_path.resolve()))

try:
    from config import config
    from featrix_queue import SessionStatus, serialize_session, save_session
except ImportError as e:
    print(f"❌ Failed to import required modules: {e}")
    sys.exit(1)


def extract_es_info(es_path: Path) -> Dict[str, Any]:
    """Extract information from EmbeddingSpace output directory."""
    info = {}
    
    # Look for metadata files
    metadata_path = es_path / "best_model_package" / "metadata.json"
    if not metadata_path.exists():
        # Try alternative locations
        for alt_path in [
            es_path / "metadata.json",
            es_path.parent / "metadata.json",
        ]:
            if alt_path.exists():
                metadata_path = alt_path
                break
    
    if metadata_path.exists():
        try:
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
                info['name'] = metadata.get('model_info', {}).get('name')
                info['created_at'] = metadata.get('model_info', {}).get('created_at')
        except Exception as e:
            print(f"⚠️  Warning: Could not read metadata.json: {e}")
    
    # Look for training logs to extract job info
    log_path = es_path / "logs" / "stdout.log"
    if log_path.exists():
        try:
            # Try to extract session name from log
            with open(log_path, 'r') as f:
                for line in f:
                    if 'session_id' in line.lower() or 'session:' in line.lower():
                        # Try to extract session ID
                        parts = line.split()
                        for i, part in enumerate(parts):
                            if 'session' in part.lower() and i + 1 < len(parts):
                                potential_id = parts[i + 1].strip(':,')
                                if len(potential_id) > 10:  # Likely a session ID
                                    info['session_id'] = potential_id
                                    break
        except Exception as e:
            print(f"⚠️  Warning: Could not parse log file: {e}")
    
    # Look for embedding space files
    for file_pattern in ['embedding_space.pickle', 'best_model.pickle', 'embedded_space.pickle']:
        pickle_path = es_path / file_pattern
        if not pickle_path.exists():
            pickle_path = es_path / "best_model_package" / file_pattern
        if pickle_path.exists():
            info['embedding_space'] = str(pickle_path)
            break
    
    # Look for other ES files
    for file_name, key in [
        ('projection.json', 'projected_points'),
        ('projections.json', 'projections'),
        ('embedding_space.db', 'sqlite_db'),
        ('vector_db.lance', 'vector_db'),
        ('strings_cache.pkl', 'strings_cache'),
    ]:
        file_path = es_path / file_name
        if file_path.exists():
            info[key] = str(file_path)
    
    return info


def extract_sp_info(sp_path: Path) -> Dict[str, Any]:
    """Extract information from SinglePredictor output directory."""
    info = {}
    
    # Look for predictor files
    for file_pattern in ['single_predictor.pickle', 'predictor.pickle', 'model.pickle']:
        pickle_path = sp_path / file_pattern
        if pickle_path.exists():
            info['single_predictor'] = str(pickle_path)
            break
    
    # Look for training metrics
    metrics_path = sp_path / "training_metrics.json"
    if metrics_path.exists():
        try:
            with open(metrics_path, 'r') as f:
                metrics = json.load(f)
                info['target_column'] = metrics.get('target_column')
                info['training_metrics'] = metrics
        except Exception as e:
            print(f"⚠️  Warning: Could not read training_metrics.json: {e}")
    
    return info


def find_job_ids(output_dir: Path) -> Dict[str, Optional[str]]:
    """Find job IDs from output directory structure."""
    job_ids = {
        'create_structured_data': None,
        'train_es': None,
        'train_knn': None,
        'run_clustering': None,
        'train_single_predictor': None,
    }
    
    # Look for job directories
    for job_type in job_ids.keys():
        job_dir = output_dir / job_type
        if job_dir.exists():
            # Find the most recent job directory
            job_dirs = sorted([d for d in job_dir.iterdir() if d.is_dir()], 
                            key=lambda x: x.stat().st_mtime, reverse=True)
            if job_dirs:
                # Job ID is typically the directory name
                job_ids[job_type] = job_dirs[0].name
    
    return job_ids


def find_predictor_by_target_column(output_dir: Path, target_column: str) -> Optional[Path]:
    """
    Find a single predictor directory by target_column.
    
    Args:
        output_dir: Base output directory (e.g., /sphere/app/featrix_output/session-name)
        target_column: Target column name to search for
        
    Returns:
        Path to the predictor directory, or None if not found
    """
    train_sp_dir = output_dir / "train_single_predictor"
    if not train_sp_dir.exists():
        return None
    
    # Search through all predictor job directories
    for job_dir in train_sp_dir.iterdir():
        if not job_dir.is_dir():
            continue
        
        # Check training_metrics.json for target_column
        metrics_path = job_dir / "training_metrics.json"
        if metrics_path.exists():
            try:
                with open(metrics_path, 'r') as f:
                    metrics = json.load(f)
                    if metrics.get('target_column') == target_column:
                        return job_dir
            except Exception:
                continue
    
    return None


def recreate_session(es_path: Optional[Path] = None, sp_path: Optional[Path] = None, 
                    session_id: Optional[str] = None,
                    output_dir: Optional[Path] = None,
                    target_column: Optional[str] = None) -> str:
    """
    Recreate a session file from ES and SP output directories.
    
    Args:
        es_path: Optional path to trained EmbeddingSpace output directory
        sp_path: Optional path to trained SinglePredictor output directory (required if es_path not provided)
        session_id: Optional session ID (will be inferred if not provided)
        output_dir: Optional output directory for session file
        target_column: Optional target column name to search for predictor
        
    Returns:
        session_id: The session ID of the recreated session
    """
    if not es_path and not sp_path:
        raise ValueError("Either --es-path or --sp-path must be provided")
    
    if es_path and not es_path.exists():
        raise ValueError(f"ES path does not exist: {es_path}")
    
    if sp_path and not sp_path.exists():
        raise ValueError(f"SP path does not exist: {sp_path}")
    
    # Determine output directory
    if output_dir is None:
        output_dir = Path(config.session_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Extract information from SP directory first (required if no ES)
    sp_info = {}
    if sp_path:
        sp_info = extract_sp_info(sp_path)
    elif target_column:
        # Find predictor by target_column if not explicitly provided
        if es_path:
            output_base = es_path.parent.parent if es_path.parent.name == 'train_es' else es_path.parent
        else:
            # Try to infer from common output directory
            output_base = Path("/sphere/app/featrix_output")
        found_sp_path = find_predictor_by_target_column(output_base, target_column)
        if found_sp_path:
            sp_path = found_sp_path
            sp_info = extract_sp_info(sp_path)
            print(f"✅ Found predictor for target_column '{target_column}' at: {sp_path}")
        else:
            raise ValueError(f"Could not find predictor for target_column '{target_column}'")
    
    # Extract information from ES directory (if provided)
    es_info = {}
    if es_path:
        es_info = extract_es_info(es_path)
    elif sp_path:
        # Try to find ES from predictor directory structure
        # Look for train_es directory in parent directories
        current = sp_path
        for _ in range(5):  # Check up to 5 levels up
            current = current.parent
            train_es_dir = current / "train_es"
            if train_es_dir.exists():
                # Find most recent ES job
                es_jobs = sorted([d for d in train_es_dir.iterdir() if d.is_dir()], 
                                key=lambda x: x.stat().st_mtime, reverse=True)
                if es_jobs:
                    es_path = es_jobs[0]
                    es_info = extract_es_info(es_path)
                    print(f"✅ Found embedding space at: {es_path}")
                    break
    
    # Determine session ID
    if not session_id:
        # Try to extract from ES info
        session_id = es_info.get('session_id')
        
        # If not found, try to infer from directory structure
        if not session_id:
            # Look for session-like patterns in parent directories
            search_path = es_path if es_path else sp_path
            if search_path:
                current = search_path
                for _ in range(5):  # Check up to 5 levels up
                    current = current.parent
                    dir_name = current.name
                    # Check if it looks like a session ID (has timestamp pattern)
                    if len(dir_name) > 20 and ('-' in dir_name or '_' in dir_name):
                        session_id = dir_name
                        break
        
        # If still not found, generate one
        if not session_id:
            from uuid import uuid4
            unique_string = str(uuid4())[:6]
            timestamp = datetime.now(tz=ZoneInfo("America/New_York")).strftime('%Y%m%d-%H%M%S')
            session_id = f"{unique_string}-{timestamp}"
            print(f"⚠️  Could not determine session ID, generated: {session_id}")
    
    # Determine session name
    session_name = es_info.get('name')
    if not session_name:
        # Try to infer from directory structure
        search_path = es_path if es_path else sp_path
        if search_path:
            session_name = search_path.parent.name if search_path.parent.name not in ['train_es', 'train_single_predictor'] else search_path.parent.parent.name
        if not session_name or session_name in ['featrix_output', 'train_es', 'train_single_predictor']:
            session_name = session_id
    
    # Find job IDs from directory structure
    if es_path:
        output_base = es_path.parent.parent if es_path.parent.name == 'train_es' else es_path.parent
    elif sp_path:
        output_base = sp_path.parent.parent if sp_path.parent.name == 'train_single_predictor' else sp_path.parent
    else:
        output_base = Path("/sphere/app/featrix_output")
    job_ids = find_job_ids(output_base)
    
    # If we have a specific predictor, find its job ID
    if sp_path:
        # Extract job ID from predictor path
        # Path format: .../train_single_predictor/job-id/...
        if 'train_single_predictor' in str(sp_path):
            parts = Path(sp_path).parts
            try:
                sp_index = parts.index('train_single_predictor')
                if sp_index + 1 < len(parts):
                    predictor_job_id = parts[sp_index + 1]
                    job_ids['train_single_predictor'] = predictor_job_id
            except ValueError:
                pass
    
    # Determine created_at timestamp
    created_at = es_info.get('created_at')
    if created_at:
        try:
            if isinstance(created_at, str):
                created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            elif isinstance(created_at, datetime):
                pass  # Already a datetime
            else:
                created_at = None
        except Exception:
            created_at = None
    
    if not created_at:
        # Use directory creation time as fallback
        search_path = es_path if es_path else sp_path
        if search_path:
            created_at = datetime.fromtimestamp(search_path.stat().st_ctime, tz=ZoneInfo("America/New_York"))
        else:
            created_at = datetime.now(tz=ZoneInfo("America/New_York"))
    
    # Build job plan
    job_plan = [
        {
            "job_type": "create_structured_data",
            "spec": {},
            "job_id": job_ids.get('create_structured_data'),
        },
        {
            "job_type": "train_es",
            "spec": {},
            "job_id": job_ids.get('train_es'),
        },
        {
            "job_type": "train_knn",
            "spec": {},
            "job_id": job_ids.get('train_knn'),
        },
        {
            "job_type": "run_clustering",
            "spec": {},
            "job_id": job_ids.get('run_clustering'),
        }
    ]
    
    # Add single predictor job if SP path provided
    if sp_path:
        job_plan.append({
            "job_type": "train_single_predictor",
            "spec": {
                "target_column": sp_info.get('target_column'),
            },
            "job_id": job_ids.get('train_single_predictor'),
        })
    
    # Determine input data path
    input_data_path = None
    for possible_path in [
        output_base / f"{session_name}_training.jsonl",
        output_base / f"{session_name}_training_data.csv",
        output_base / "training_data.jsonl",
        output_base / "training_data.csv",
    ]:
        if possible_path.exists():
            input_data_path = str(possible_path)
            break
    
    # Build session document
    session_doc = {
        "session_id": session_id,
        "session_type": "embedding_space",
        "name": session_name,
        "status": SessionStatus.DONE,
        "created_at": created_at,
        "input_data": input_data_path or str(output_base / "training_data.jsonl"),
        "s3_training_dataset": None,  # Unknown from output directory
        "s3_validation_dataset": None,  # Unknown from output directory
        "job_plan": job_plan,
    }
    
    # Add ES-related fields if ES exists
    if es_info:
        session_doc.update({
            "projected_points": es_info.get('projected_points', str(output_base / "projection.json")),
            "preview_png": str(output_base / "preview.png"),
            "embedding_space": es_info.get('embedding_space', str(es_path / "embedding_space.pickle") if es_path else None),
            "sqlite_db": es_info.get('sqlite_db', str(output_base / "embedding_space.db")),
            "vector_db": es_info.get('vector_db', str(output_base / "vector_db.lance")),
            "projections": es_info.get('projections', str(output_base / "projections.json")),
            "strings_cache": es_info.get('strings_cache', str(output_base / "strings_cache.pkl")),
        })
    
    # Add single predictor info if available
    if sp_info.get('single_predictor'):
        session_doc['single_predictor'] = sp_info['single_predictor']
        # Add training metrics path if available
        if sp_path:
            metrics_path = sp_path / "training_metrics.json"
            if metrics_path.exists():
                session_doc['training_metrics'] = str(metrics_path)
    
    # Save session file
    save_session(session_id, session_doc, exist_ok=True)
    
    print(f"✅ Recreated session file: {output_dir / f'{session_id}.session'}")
    print(f"   Session ID: {session_id}")
    print(f"   Session Name: {session_name}")
    if es_path:
        print(f"   ES Path: {es_path}")
    if sp_path:
        print(f"   SP Path: {sp_path}")
    
    return session_id


def main():
    parser = argparse.ArgumentParser(
        description='Recreate Featrix session file from trained ES and SP outputs'
    )
    parser.add_argument(
        '--es-path',
        type=str,
        default=None,
        help='Path to trained EmbeddingSpace output directory (optional if --sp-path provided)'
    )
    parser.add_argument(
        '--sp-path',
        type=str,
        default=None,
        help='Path to trained SinglePredictor output directory (optional)'
    )
    parser.add_argument(
        '--target-column',
        type=str,
        default=None,
        help='Target column name - will search for matching predictor if --sp-path not provided'
    )
    parser.add_argument(
        '--session-id',
        type=str,
        default=None,
        help='Session ID to use (will be inferred if not provided)'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default=None,
        help='Output directory for session file (default: /sphere/app/featrix_sessions)'
    )
    
    args = parser.parse_args()
    
    try:
        es_path = Path(args.es_path).resolve() if args.es_path else None
        sp_path = Path(args.sp_path).resolve() if args.sp_path else None
        output_dir = Path(args.output_dir).resolve() if args.output_dir else None
        
        if not es_path and not sp_path:
            parser.error("Either --es-path or --sp-path must be provided")
        
        session_id = recreate_session(
            es_path=es_path,
            sp_path=sp_path,
            session_id=args.session_id,
            output_dir=output_dir,
            target_column=args.target_column
        )
        
        print(f"\n✅ Successfully recreated session: {session_id}")
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

