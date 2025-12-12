import lancedb
import pandas as pd
import numpy as np
import os
from typing import List, Dict, Any, Tuple
import sqlite3
import time
import logging

from lib.job_manager import check_abort_file, update_job_status, JobStatus

logger = logging.getLogger(__name__)

class CSVtoLanceDB:
    def __init__(self, featrix_es, sqlite_db_path: str, lancedb_path: str = "lance_db", job_id: str = None):
        """
        Initializes the LanceDB-based storage for CSV data and vectors.
        """
        self.featrix_es = featrix_es
        self.sqlite_db_path = sqlite_db_path
        self.sql_conn = sqlite3.connect(sqlite_db_path)
        self.job_id = job_id  # Store job_id for ABORT file checks

        self.lancedb_path = lancedb_path
        self.db = lancedb.connect(self.lancedb_path)  # Connect to LanceDB storage
        self.table_name = "csv_data"
    
    def _analyze_embeddings(self, df):
        """
        Comprehensive analysis of embeddings to identify problematic vectors.
        Returns statistics about the embeddings.
        """
        print("\n🔍 EMBEDDING ANALYSIS:")
        print("=" * 50)
        
        total_rows = len(df)
        none_count = 0
        nan_count = 0
        inf_count = 0
        zero_count = 0
        problematic_rows = []
        vector_dimensions = []
        
        for i, vec in enumerate(df["vector"]):
            row_issues = []
            
            # Check for None
            if vec is None:
                none_count += 1
                row_issues.append("None")
            else:
                # Convert to numpy array if not already
                if not isinstance(vec, np.ndarray):
                    try:
                        vec = np.array(vec, dtype=np.float32)
                    except Exception as e:
                        row_issues.append(f"conversion_error: {str(e)}")
                        continue
                
                # Check vector dimensions
                vector_dimensions.append(len(vec))
                
                # Check for NaN values
                if np.isnan(vec).any():
                    nan_count += 1
                    nan_positions = np.where(np.isnan(vec))[0]
                    row_issues.append(f"NaN_at_positions: {list(nan_positions[:5])}")  # Show first 5 positions
                
                # Check for infinite values
                if np.isinf(vec).any():
                    inf_count += 1
                    inf_positions = np.where(np.isinf(vec))[0]
                    row_issues.append(f"Inf_at_positions: {list(inf_positions[:5])}")
                
                # Check for all-zero vectors
                if np.allclose(vec, 0.0):
                    zero_count += 1
                    row_issues.append("all_zeros")
            
            if row_issues:
                problematic_rows.append({
                    'row_id': df.iloc[i]['__featrix_row_id'],
                    'index': i,
                    'issues': row_issues,
                    'sample_data': dict(list(df.iloc[i].drop(['vector', '__featrix_row_id']).items())[:3])  # First 3 columns as sample
                })
        
        # Analyze vector dimensions
        unique_dimensions = set(vector_dimensions) if vector_dimensions else set()
        
        # Print summary
        print(f"📊 Total rows: {total_rows}")
        print(f"🚫 None vectors: {none_count}")
        print(f"🔢 NaN vectors: {nan_count}")
        print(f"♾️  Infinite vectors: {inf_count}")
        print(f"0️⃣  All-zero vectors: {zero_count}")
        
        if vector_dimensions:
            print(f"📏 Vector dimensions found: {sorted(unique_dimensions)}")
            if len(unique_dimensions) > 1:
                print(f"⚠️  DIMENSION MISMATCH: Found {len(unique_dimensions)} different vector sizes!")
                for dim in sorted(unique_dimensions):
                    count = vector_dimensions.count(dim)
                    print(f"   - Dimension {dim}: {count} vectors")
            else:
                print(f"✅ All vectors have consistent dimension: {list(unique_dimensions)[0]}")
        else:
            print("🚨 NO VALID VECTORS FOUND!")
        
        bad_vectors_count = none_count + nan_count + inf_count
        good_vectors_count = total_rows - bad_vectors_count
        print(f"✅ Clean vectors: {good_vectors_count}")
        print(f"❌ Bad vectors (will be dropped): {bad_vectors_count}")
        
        if bad_vectors_count > 0:
            print(f"📉 Data loss: {(bad_vectors_count/total_rows)*100:.1f}%")
        
        # Show sample problematic rows
        if problematic_rows:
            print(f"\n🔍 Sample problematic rows (showing first 5):")
            for i, prob_row in enumerate(problematic_rows[:5]):
                print(f"  Row {prob_row['index']} (ID: {prob_row['row_id']}):")
                print(f"    Issues: {', '.join(prob_row['issues'])}")
                print(f"    Sample data: {prob_row['sample_data']}")
        
        print("=" * 50)
        
        return {
            'total_rows': total_rows,
            'bad_vectors_count': bad_vectors_count,
            'good_vectors_count': good_vectors_count,
            'none_count': none_count,
            'nan_count': nan_count,
            'inf_count': inf_count,
            'zero_count': zero_count,
            'problematic_rows': problematic_rows,
            'vector_dimensions': unique_dimensions,
            'has_dimension_mismatch': len(unique_dimensions) > 1
        }
    
    def create_table(self):
        """
        Reads the CSV, computes embeddings, and stores data in LanceDB.
        
        Note: This preserves ALL columns including __featrix_meta* metadata columns.
        Metadata columns are not used during embedding generation (they're not in the
        embedding space codecs), but they're stored in LanceDB and returned with search results.
        """        
        assert self.sql_conn is not None
        df = pd.read_sql_query("SELECT rowid AS __featrix_row_id, * from data ORDER BY rowid", self.sql_conn)
        
        print(f"\n🚀 Starting KNN table creation with {len(df)} rows...")
        
        # Check for ABORT file before starting
        if self.job_id:
            try:
                if check_abort_file(self.job_id, output_dir=str(os.getcwd())):
                    logger.error(f"🚫 ABORT file detected for job {self.job_id} - exiting KNN training")
                    # Update job status before exiting
                    try:
                        update_job_status(self.job_id, JobStatus.FAILED, {
                            "error_message": "Training aborted due to ABORT file before KNN training"
                        })
                    except Exception as e:
                        logger.error(f"Failed to update job status: {e}")
                    raise SystemExit("Training aborted due to ABORT file")
            except SystemExit:
                raise
            except Exception as e:
                logger.warning(f"⚠️  Could not check ABORT file: {e}")
        
        # Compute embeddings for each row
        # Note: encode_record() will skip any columns not in the embedding space codecs,
        # including __featrix_meta* columns, but they remain in the DataFrame
        print("⚙️  Computing embeddings...")
        
        # Convert apply to loop so we can check ABORT periodically
        vectors = []
        total_rows = len(df)
        last_abort_check = time.time()
        abort_check_interval = 10  # Check every 10 seconds
        
        for idx, (_, row) in enumerate(df.iterrows()):
            # Periodic ABORT check during embedding computation
            if self.job_id and (time.time() - last_abort_check) >= abort_check_interval:
                try:
                    if check_abort_file(self.job_id, output_dir=str(os.getcwd())):
                        logger.error(f"🚫 ABORT file detected for job {self.job_id} during embedding computation (row {idx}/{total_rows}) - exiting")
                        # Update job status before exiting
                        try:
                            update_job_status(self.job_id, JobStatus.FAILED, {
                                "error_message": f"Training aborted due to ABORT file during embedding computation (row {idx}/{total_rows})"
                            })
                        except Exception as e:
                            logger.error(f"Failed to update job status: {e}")
                        raise SystemExit("Training aborted due to ABORT file")
                except SystemExit:
                    raise
                except Exception as e:
                    logger.debug(f"Could not check ABORT file: {e}")
                last_abort_check = time.time()
            
            # Compute embedding for this row
            vectors.append(self.featrix_es.encode_record(row.to_dict()))
            
            # Progress logging every 1000 rows
            if (idx + 1) % 1000 == 0:
                print(f"   Processed {idx + 1}/{total_rows} rows ({(idx + 1)/total_rows*100:.1f}%)")
        
        df["vector"] = vectors
        
        # Ensure embeddings are numpy arrays
        df["vector"] = df["vector"].apply(lambda x: np.array(x, dtype=np.float32) if x is not None else None)

        # Comprehensive embedding analysis
        embedding_stats = self._analyze_embeddings(df)

        # Early exit if no good vectors
        if embedding_stats['good_vectors_count'] == 0:
            print("🚨 CRITICAL: No valid vectors found! Cannot create LanceDB table.")
            print("   This usually means all embeddings failed to generate properly.")
            print("   Check your embedding space and input data.")
            return None

        # Filter out None vectors before passing to LanceDB to prevent schema inference errors
        print(f"\n🧹 Filtering out {embedding_stats['none_count']} None vectors before LanceDB creation...")
        df_filtered = df[df["vector"].notna()].copy()
        print(f"   Rows after None filtering: {len(df_filtered)}")

        # Additional safety check: ensure remaining vectors are not empty
        if len(df_filtered) == 0:
            print("🚨 CRITICAL: No rows remain after filtering None vectors!")
            return None

        # 🛠️ LANCEDB COLUMN NAME SANITIZATION
        # LanceDB doesn't allow dots in top-level field names, so we need to clean them
        print(f"\n🧼 Sanitizing column names for LanceDB compatibility...")
        original_columns = df_filtered.columns.tolist()
        sanitized_columns = []
        renamed_count = 0
        
        for col in original_columns:
            if '.' in col:
                # Replace dots with underscores for LanceDB compatibility
                sanitized_col = col.replace('.', '_')
                sanitized_columns.append(sanitized_col)
                renamed_count += 1
                print(f"   • '{col}' → '{sanitized_col}'")
            else:
                sanitized_columns.append(col)
        
        if renamed_count > 0:
            print(f"   ✅ Renamed {renamed_count} columns with dots to use underscores")
            df_filtered.columns = sanitized_columns
        else:
            print(f"   ✅ All column names are already LanceDB-compatible")

        # Check for ABORT file before creating LanceDB table
        if self.job_id:
            try:
                if check_abort_file(self.job_id, output_dir=str(os.getcwd())):
                    logger.error(f"🚫 ABORT file detected for job {self.job_id} before LanceDB table creation - exiting")
                    # Update job status before exiting
                    try:
                        update_job_status(self.job_id, JobStatus.FAILED, {
                            "error_message": "Training aborted due to ABORT file before LanceDB table creation"
                        })
                    except Exception as e:
                        logger.error(f"Failed to update job status: {e}")
                    raise SystemExit("Training aborted due to ABORT file")
            except SystemExit:
                raise
            except Exception as e:
                logger.warning(f"⚠️  Could not check ABORT file: {e}")
        
        # Convert to dictionary format for LanceDB storage
        records = df_filtered.to_dict(orient="records")
        
        print(f"\n🗄️  Creating LanceDB table with {len(records)} records...")
        
        try:
            # Create or overwrite LanceDB table with bad vector handling
            # Using 'drop' strategy to remove rows with NaN vectors
            self.table = self.db.create_table(
                self.table_name, 
                data=records, 
                mode="overwrite",
                on_bad_vectors="drop"
            )
        except Exception as e:
            print(f"🚨 LANCEDB ERROR: {str(e)}")
            print(f"   This might be due to dimension mismatches or other vector issues.")
            if embedding_stats.get('has_dimension_mismatch'):
                print(f"   DETECTED: Vector dimension mismatch - this is likely the cause!")
                print(f"   Dimensions found: {embedding_stats['vector_dimensions']}")
            raise e
        
        # Post-creation verification
        print(f"\n📋 POST-CREATION VERIFICATION:")
        print("=" * 30)
        
        final_count = len(self.table)
        expected_good = embedding_stats['good_vectors_count']
        actually_dropped = len(df) - final_count
        expected_dropped = embedding_stats['bad_vectors_count']
        
        print(f"📏 Final table size: {final_count} rows")
        print(f"📉 Actually dropped: {actually_dropped} rows")
        print(f"🎯 Expected to drop: {expected_dropped} rows")
        
        if actually_dropped == expected_dropped:
            print("✅ Drop count matches expectation!")
        else:
            print(f"⚠️  Drop count mismatch! Expected {expected_dropped}, got {actually_dropped}")
            if actually_dropped > expected_dropped:
                print("   LanceDB may have found additional issues we didn't detect")
            else:
                print("   LanceDB kept some vectors we thought were bad")
        
        # Data retention rate
        retention_rate = (final_count / len(df)) * 100
        print(f"📊 Data retention rate: {retention_rate:.1f}%")
        
        if final_count == 0:
            print("🚨 WARNING: No vectors were retained! All data was dropped.")
            return None
        elif retention_rate < 50:
            print("⚠️  WARNING: Less than 50% of data retained. Check embedding generation.")
        elif retention_rate < 90:
            print("⚠️  NOTICE: Some data loss occurred. Consider investigating embedding issues.")
        else:
            print("✅ Good data retention rate.")
        
        print("=" * 30)
        
        return
    
    def append_records(self, new_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Append new records to an existing LanceDB table.
        
        Args:
            new_records: List of dictionaries containing the record data
            
        Returns:
            Dictionary with statistics about the append operation
        """
        if not hasattr(self, 'table') or self.table is None:
            raise ValueError("No table loaded. Call load_existing() first or create_table().")
        
        if not new_records:
            return {
                "records_added": 0,
                "records_failed": 0,
                "success": True,
                "message": "No records to add"
            }
        
        print(f"\n🔄 Appending {len(new_records)} new records to vector database...")
        
        # Get the next row ID based on the current max row ID
        try:
            # Query to get the max __featrix_row_id
            existing_df = self.table.to_pandas()
            if len(existing_df) > 0 and '__featrix_row_id' in existing_df.columns:
                next_row_id = int(existing_df['__featrix_row_id'].max()) + 1
            else:
                next_row_id = 1
        except Exception as e:
            logger.warning(f"Could not determine next row ID, starting from 1: {e}")
            next_row_id = 1
        
        # Compute embeddings for each new record
        print("⚙️  Computing embeddings for new records...")
        records_to_add = []
        failed_count = 0
        
        for i, record in enumerate(new_records):
            try:
                # Encode the record
                embedding = self.featrix_es.encode_record(record)
                
                if embedding is None or np.isnan(embedding).any() or np.isinf(embedding).any():
                    logger.warning(f"Skipping record {i}: Invalid embedding")
                    failed_count += 1
                    continue
                
                # Create record with vector and row ID
                record_with_vector = record.copy()
                record_with_vector['vector'] = np.array(embedding, dtype=np.float32)
                record_with_vector['__featrix_row_id'] = next_row_id + i
                
                # Sanitize column names (replace dots with underscores)
                sanitized_record = {}
                for key, value in record_with_vector.items():
                    sanitized_key = key.replace('.', '_')
                    sanitized_record[sanitized_key] = value
                
                records_to_add.append(sanitized_record)
                
            except Exception as e:
                logger.error(f"Failed to encode record {i}: {e}")
                failed_count += 1
        
        if not records_to_add:
            return {
                "records_added": 0,
                "records_failed": failed_count,
                "success": False,
                "message": "All records failed to encode"
            }
        
        # Add records to LanceDB table
        print(f"🗄️  Adding {len(records_to_add)} records to LanceDB...")
        try:
            self.table.add(records_to_add)
            
            success_count = len(records_to_add)
            print(f"✅ Successfully added {success_count} records")
            if failed_count > 0:
                print(f"⚠️  {failed_count} records failed to encode")
            
            return {
                "records_added": success_count,
                "records_failed": failed_count,
                "success": True,
                "message": f"Added {success_count} records ({failed_count} failed)",
                "new_total": len(self.table)
            }
            
        except Exception as e:
            logger.error(f"Failed to add records to LanceDB: {e}")
            return {
                "records_added": 0,
                "records_failed": len(new_records),
                "success": False,
                "message": f"Error adding records: {str(e)}"
            }
    
    def search(self, query_data: Dict[str, Any], k: int = 5, include_field_similarity: bool = True) -> Dict[str, Any]:
        """
        Performs a nearest neighbor search on the LanceDB vector store.
        Returns a dictionary containing:
        - results: List of matching records with coords, original_data, distance, and field_similarity
        - stats: Query statistics including timing, record count, and distance metrics
        
        Args:
            query_data: Query record as dictionary
            k: Number of nearest neighbors to return
            include_field_similarity: If True, compute field-level similarity for each result
        """
        # Start timing the query
        start_time = time.perf_counter()
        
        query_vec = self.featrix_es.encode_record(query_data)  # Compute embedding for query

        results_df = (
            self.table.search(query_vec.numpy())
            .limit(k)
            .to_pandas()[["_distance", *self.table.schema.names]]
        )

        formatted_results = []
        distances = []
        
        for _, row in results_df.iterrows():
            original_data = row.drop("_distance").to_dict()
            del original_data["vector"]
            row_id = original_data.pop("__featrix_row_id")
            distance = row["_distance"]
            distances.append(distance)
            
            result_entry = {
                "__featrix_row_id": row_id,
                "coords": self.featrix_es.encode_record(original_data, short=True).tolist(),
                "original_data": original_data,
                "distance": distance
            }
            
            # Compute field-level similarity if requested
            if include_field_similarity:
                try:
                    field_distances = self.featrix_es.compute_field_similarity(query_data, original_data)
                    result_entry["field_similarity"] = field_distances
                except Exception as e:
                    print(f"Warning: Failed to compute field similarity: {e}")
                    result_entry["field_similarity"] = {}
            
            formatted_results.append(result_entry)

        # End timing
        elapsed_time = time.perf_counter() - start_time
        
        # Calculate statistics
        total_records = len(self.table)
        vector_dimensions = len(query_vec)
        brute_force_comparisons = total_records * vector_dimensions
        
        # Distance statistics
        distances_array = np.array(distances)
        avg_distance = float(np.mean(distances_array)) if len(distances_array) > 0 else 0.0
        std_distance = float(np.std(distances_array)) if len(distances_array) > 0 else 0.0
        
        return {
            "results": formatted_results,
            "stats": {
                "query_time_seconds": round(elapsed_time, 6),
                "records_searched": total_records,
                "brute_force_comparisons": brute_force_comparisons,
                "vector_dimensions": vector_dimensions,
                "results_returned": len(formatted_results),
                "avg_distance": round(avg_distance, 6),
                "std_distance": round(std_distance, 6),
                "min_distance": round(float(np.min(distances_array)), 6) if len(distances_array) > 0 else 0.0,
                "max_distance": round(float(np.max(distances_array)), 6) if len(distances_array) > 0 else 0.0
            }
        }

    def load_existing(self):
        """
        Loads an existing LanceDB table from disk.
        """
        self.table = self.db.open_table(self.table_name)
        print(f"✅ Loaded existing LanceDB table: {self.table_name}")

    def vectordb_size(self) -> int:
        """
        Returns the number of records in the vector database.
        """
        if not hasattr(self, 'table') or self.table is None:
            raise ValueError("No table loaded. Call load_existing() first or create_table().")
        return len(self.table)

    def get_output_files(self) -> Tuple[str, str]:
        """
        Returns the path to the LanceDB storage and the table name.
        """
        return dict(
            vector_db_path=self.lancedb_path,
        )

# # Usage
# csv_path = "data.csv"
# ldb = CSVtoLanceDB(csv_path)
# ldb.create_table()  # Store CSV in LanceDB
# query = {"column1": "example", "column2": 42}  # Example query
# results = ldb.search(query, k=3)  # Search for nearest neighbors
# print(results)
