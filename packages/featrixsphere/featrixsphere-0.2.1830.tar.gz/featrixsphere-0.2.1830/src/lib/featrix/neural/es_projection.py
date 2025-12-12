#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2024 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

import asyncio
import json
import logging
import os
import pickle
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path

import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.cluster import AgglomerativeClustering
from sklearn.manifold import TSNE
from sklearn.metrics import davies_bouldin_score
from torch.utils.data import DataLoader, TensorDataset

from featrix.neural.embedded_space import EmbeddingSpace
# from featrix.neural.input_data_set import FeatrixInputDataSet

logger = logging.getLogger(__name__)

import numpy as np

def stereographic_projection(point_3d, projection_point=(0,0,1)):
    """
    Perform stereographic projection of a 3D point on the unit sphere to a 2D plane.

    Parameters:
    point_3d (tuple or list or np.array): A point on the sphere as (x, y, z).
    projection_point (tuple or list or np.array): The point from which to project (e.g., (0, 0, 1)).

    Returns:
    tuple: The 2D coordinates (X, Y) of the projected point on the plane.
    """
    # Convert input to numpy arrays for easier manipulation
    point_3d = np.array(point_3d)
    projection_point = np.array(projection_point)
    
    # Ensure the projection point is not the same as the input point
    if np.allclose(point_3d, projection_point):
        raise ValueError("The projection point cannot be the same as the point being projected.")

    # Direction vector from projection point to the input point
    direction_vector = point_3d - projection_point
    
    # Intersection with the plane z = 0
    t = -projection_point[2] / direction_vector[2]  # Solve for intersection with z = 0
    
    # Projected 2D coordinates
    X = projection_point[0] + t * direction_vector[0]
    Y = projection_point[1] + t * direction_vector[1]

    return (X, Y)


def sqlite_save_sample_rowids():
    return

def sqlite_save_embeddings():
    return

def sqlite_save_cluster_ids():
    return

def sqlite_build_faiss_for_nn_search():
    return

class ESProjection:
    def __init__(
            self,
            es: EmbeddingSpace,
            df: pd.DataFrame,
            max_training_samples=2_000,
            # embeddings_file=None,
            weight_cutoff=69.0,
            include_missing_messages=False,
            is2d=False,
            sqlite_conn=None
    ):
        self._es = es
        self._df = df
        self._maxTrainingSamples = max_training_samples
        self._include_missing = include_missing_messages
        self._weight_cutoff = weight_cutoff
        # self._embeddings_file = embeddings_file
        self._is2d = is2d
        self._sqlite_conn = sqlite_conn

    @staticmethod
    def cluster_embeddings(embeddings):

        data = np.array(embeddings)

        # Remove rows with NaN values, if there are any.
        try:
            cleaned_embeddings = data[~np.isnan(data).any(axis=1)]
        except Exception as err:
            traceback.print_exc()
            print("...data = ", data)
            raise(err)
        
        print(f"len(embeddings) = {len(embeddings)}; len(cleaned_embeddings) = {len(cleaned_embeddings)}")
        
        # Handle edge cases where clustering is not possible
        if len(cleaned_embeddings) == 0:
            print("⚠️  No clean embeddings available - all embeddings contain NaNs")
            # Return default cluster labels (all zeros)
            default_labels = np.zeros(len(embeddings), dtype=int)
            return default_labels, {}
        
        if len(cleaned_embeddings) < 2:
            print("⚠️  Too few clean embeddings for clustering (need at least 2)")
            # Return default cluster labels (all zeros)
            default_labels = np.zeros(len(embeddings), dtype=int)
            return default_labels, {}
        
        n_clusters_list = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

        cluster_results = {}

        best_score = None
        # best_n_clusters = 0
        best_cluster_labels = []

        for n_clusters in n_clusters_list:
            # Fix: Check against cleaned_embeddings length, not original embeddings
            if n_clusters > len(cleaned_embeddings):
                continue

            try:
                print(f"{time.ctime()}: starting k = {n_clusters}...")

                agglom = AgglomerativeClustering(n_clusters=n_clusters,
                                                linkage='average')
                cluster_labels = agglom.fit_predict(cleaned_embeddings)
                
                # Fix: Use cleaned_embeddings for scoring, not original embeddings
                score = davies_bouldin_score(cleaned_embeddings, cluster_labels)
                print("score = ", score)
                cluster_results[n_clusters] = { "score": score, "cluster_labels": cluster_labels.tolist() }
                if best_score is None or score < best_score:
                    best_score = score
                    # best_n_clusters = n_clusters
                    best_cluster_labels = cluster_labels
            except Exception as e:
                print(f"❌ Clustering failed for k={n_clusters}: {e}")
                traceback.print_exc()

        # Handle case where no clustering succeeded
        if len(best_cluster_labels) == 0:
            print("⚠️  All clustering attempts failed - using default single cluster")
            default_labels = np.zeros(len(embeddings), dtype=int)
            return default_labels, cluster_results
        
        # If we have NaN embeddings, we need to map the clean cluster labels back to the original indices
        if len(cleaned_embeddings) < len(embeddings):
            print(f"📍 Mapping cluster labels from {len(cleaned_embeddings)} clean embeddings back to {len(embeddings)} original embeddings")
            # Create mapping from clean indices back to original indices
            clean_indices = ~np.isnan(data).any(axis=1)
            full_cluster_labels = np.full(len(embeddings), -1, dtype=int)  # -1 for NaN embeddings
            full_cluster_labels[clean_indices] = best_cluster_labels
            best_cluster_labels = full_cluster_labels
                
        print("best clustering was k = ", len(set(best_cluster_labels)))
        # print("best_cluster_labels = ", best_cluster_labels)
        # print(f"cluster_results[{len(set(best_cluster_labels))}] = ", cluster_results[len(set(best_cluster_labels))])
        print("cluster_results = ", cluster_results)

        return best_cluster_labels, cluster_results

    def run(self):
        assert self._df is not None
        assert self._es is not None

        df = self._df
        assert df is not None
        assert len(df) > 0
        assert len(df.columns) > 0
        logger.info(f"... df = {len(df.columns)} x {len(df)} with cols {df.columns}")
        es = self._es

        embeddings = []
        full_embeddings = []
        set_columns_matrix = []        # 

        # Subsample the data to save compute.
        # 10k samples should be more than enough to get a good idea of the data distribution.
        if len(df) > self._maxTrainingSamples:
            logger.info(f"Subsampling the data for projections... from {len(df)} to {self._maxTrainingSamples} samples.")
            # NOTE: We're taking a "naive" sample here, which means we're not considering the possibly many
            # segments in the dataframe. Taking a naive sample may result in a sample that does not adequately
            # represent the segments. However, this is a trade-off we're willing to make here because the 
            # t-SNE projection is only used for visualization purposes, and not as a basis for further analysis.
            # The fact that not all segments in the data may be represented adequately in the t-SNE projection
            # is unlikely to distort the visual representation of the data in a significant way.
            df = df.sample(self._maxTrainingSamples).reset_index(drop=True)
    
        # if self._embeddings_file and Path(self._embeddings_file).exists():
        #     with open(self._embeddings_file, "rb") as _f:
        #         embeddings = pickle.load(_f)
        # else:
        embeddings = []
        full_embeddings = []
        set_columns_matrix = []        # 
        scalar_columns_matrix = []
        string_columns_matrix = []
        rowids = []
        row_offsets = []

        set_columns_names_and_values = es.get_set_columns()
        scalar_columns_names_and_codecs = es.get_scalar_columns()
        string_columns_names = es.get_string_column_names()

        # encode the training set
        #print(f"Encoding {len(df)} records...")
        start = datetime.utcnow()
        exc_count = 0
        successful_embeddings = 0
        failed_embeddings = 0
        
        for idx, row in df.iterrows():
            assert len(embeddings) == len(full_embeddings)
            assert len(embeddings) == len(set_columns_matrix)
            assert len(embeddings) == len(scalar_columns_matrix)
            assert len(embeddings) == len(rowids)

            try:
                # print(row)
                rShort = es.encode_record(row, short=True, output_device=torch.device("cpu"))
                # print(rShort)
                rLong = es.encode_record(row, short=False, output_device=torch.device("cpu"))
                # print(rShort)

                # Check if embeddings contain NaN values
                if torch.isnan(rShort).any() or torch.isnan(rLong).any():
                    failed_embeddings += 1
                    if failed_embeddings <= 5:  # Show first 5 failures
                        print(f"🚨 EMBEDDING {idx} HAS NaN VALUES:")
                        print(f"   rShort: {rShort}")
                        print(f"   rLong: {rLong}")
                        print(f"   Row data sample: {dict(list(row.items())[:3])}")
                        # Check which columns might be causing issues
                        for col, val in row.items():
                            if col in es.col_codecs:
                                try:
                                    test_token = es.col_codecs[col].tokenize(val)
                                    if hasattr(test_token.value, 'isnan') and torch.isnan(test_token.value).any():
                                        print(f"   🔥 Column '{col}' tokenization produced NaN: {val} -> {test_token}")
                                except Exception as e:
                                    print(f"   💥 Column '{col}' tokenization failed: {e}")
                    # Skip this row - don't append anything to keep arrays in sync
                    continue
                else:
                    successful_embeddings += 1

                orig_set_data = {}
                orig_scalar_data = {}
                orig_string_data = {}
                for k, v in row.items():
                    theCodec = set_columns_names_and_values.get(k)
                    if theCodec is not None:
                        orig_set_data[k] = v
                    else:
                        theCodec = scalar_columns_names_and_codecs.get(k)
                        if theCodec is not None:
                            orig_scalar_data[k] = v
                        else:
                            if k in string_columns_names:
                                orig_string_data[k] = v

                # Only append to all arrays after successful encoding
                # This ensures all arrays stay in sync
                rowids.append(row['__featrix_row_id'])
                row_offsets.append(idx)
                embeddings.append(rShort.detach())
                full_embeddings.append(rLong.detach())
                set_columns_matrix.append(orig_set_data)
                scalar_columns_matrix.append(orig_scalar_data)
                string_columns_matrix.append(orig_string_data)

                if idx % 100 == 0:
                    logger.debug(f"... record {idx}... (time so far {(datetime.utcnow() - start).total_seconds()})")
            except Exception:  # noqa
                traceback.print_exc()
                print("crash")
                if exc_count == 0:
                    try:
                        print(f"ENCODE RECORD CRASHED ROW = __{row.tolist()}__")
                    except:
                        print("tolist failed...")
                    traceback.print_exc()
                else:
                    if (exc_count % 100) == 0:
                        try:
                            theList = row.tolist()
                            for idx, item in enumerate(theList):
                                if type(item) == str:
                                    if len(item) > 32:
                                        item = item[:32] + "..."
                                        theList[idx] = item
                            print(f"ROW {exc_count} = __{theList}__")
                        except:
                            print("@@@@ grrr")
                            traceback.print_exc()
                        sys.stderr.write(f"(another traceback {exc_count})\n")
                exc_count += 1
        
        print(f"🔍 EMBEDDING GENERATION SUMMARY:")
        print(f"   ✅ Successful embeddings: {successful_embeddings}")
        print(f"   ❌ Failed embeddings (NaN): {failed_embeddings}")
        print(f"   💥 Exception count: {exc_count}")
        print(f"   📊 Total processed: {len(embeddings)}")
        
        logger.debug(f"Encoded {len(df)} records in {(datetime.utcnow() - start).total_seconds()} seconds.... {exc_count} exceptions")

        # If the caller provides an embeddings file that didnt' exist, save out the embedding file.
        # if self._embeddings_file:
        #     with open(self._embeddings_file, "wb") as fp:
        #         pickle.dump(embeddings, fp)

        cluster_labels, entire_cluster_results = self.cluster_embeddings(full_embeddings)

        if self._is2d:
            coords_2d = []

            for embed in embeddings:
                pt = stereographic_projection(embed)
                coords_2d.append(pt)

            new_df = pd.DataFrame(coords_2d)
            new_df['cluster_pre'] = cluster_labels

            new_df = new_df.rename(columns={"0": "x", "1": "y"})
            new_df.to_csv("debug_2d.csv", index=None)
        else:
            coords_3d = []
            for embed in embeddings:
                pt = [embed[0].item(), embed[1].item(), embed[2].item()]
                coords_3d.append(pt)
            new_df = pd.DataFrame(coords_3d)
            # new_df['cluster_results'] = entire_cluster_results
            new_df['cluster_pre'] = cluster_labels
            new_df['__featrix_row_id'] = rowids
            new_df['__featrix_row_offset'] = row_offsets
            new_df['set_columns'] = set_columns_matrix
            new_df['scalar_columns'] = scalar_columns_matrix
            new_df['string_columns'] = string_columns_matrix

            new_df.to_csv("debug_3d.csv", index=None)
            new_df = new_df.rename(columns={"0": "x", "1": "y", "2": "z"})

        msgs = []
        try:
            msgs = self.characterize_clusters(
                labels=cluster_labels,
                tsne_df=new_df,
                data_df=df,
                cluster_field='cluster_pre',
                include_missing=self._include_missing,
                weight_cutoff=self._weight_cutoff
            )
        except:
            msgs.append("Crash when trying to describe clusters; please contact support.")
        js = {
            'coords': json.loads(new_df.to_json(orient='records')),
            'cluster_messages': msgs,
            'entire_cluster_results': entire_cluster_results
        }
        return js
        # return msgs, new_df
        # new_df, tsne_normalized_vectors, cluster_labels


    @staticmethod
    def characterize_clusters(
            labels,
            tsne_df,
            data_df,
            cluster_field,
            include_missing=True,
            weight_cutoff: float = 69.0
    ):
        print("Characterize...")
        return []
    
        assert len(labels) == len(tsne_df), f"len(labels) = {len(labels)} != len(tsne_df) = {len(tsne_df)}"
        assert len(labels) == len(data_df), f"len(labels) = {len(labels)} != len(data_df) = {len(data_df)}"

        cols = data_df.columns
        unique_labels = list(set(labels))
        msgs = {}
        for u in unique_labels:
            cluster_rows = tsne_df[tsne_df[cluster_field] == u]
            # per column let's look for columns that never change or are > 80% one variable.
            c_msgs = []
            for c in cols:
                col_vals = data_df.loc[cluster_rows.index, c]
                h = col_vals.value_counts(dropna=True).to_dict()
                if len(h) == 0:
                    if include_missing:
                        c_msgs.append({
                            "weight": .01,
                            "col": c,
                            "perc": 100,
                            "value": "NaN",
                            "msg": f"Column '{c}' is always NaN in this cluster."
                        })
                    else:
                        logger.debug( f"Cluster {u}: Column '{c}' is always NaN in this cluster.")
                elif len(h) == 1:
                    the_key = list(h.keys())[0]
                    if the_key is not None:
                        the_key = str(the_key)
                        if len(the_key) > 100:
                            the_key = the_key[:100] + "..."
                            
                    msg = {"weight": 1,
                           "col": c,
                           "perc": 100,
                           "value": str(the_key),
                           "msg": f"Column '{c}' is always '{the_key}' in this cluster."}
                    c_msgs.append(msg)
                else:
                    try:
                        max_key = max(h, key=h.get)
                        num_rows = sum(h.values())  # remember, h is a histogram - the item is always a count [int]
                        this_key_perc = (float(h[max_key]) / float(num_rows)) * 100
                        if this_key_perc > weight_cutoff:
                            msg = {"weight": this_key_perc / 100,
                                   "col": c,
                                   "perc": this_key_perc, 
                                   "value": str(max_key),
                                   "non_null_count": num_rows,
                                   "msg": f"Column '{c}' = '{max_key}' {this_key_perc:.2f}% of the "
                                          f"time (non-null n={num_rows})"}
                            c_msgs.append(msg)
                    except Exception as e:
                        logger.warning(f"Problem with cluster label {u} column {c}): {e}: {traceback.format_exc()}")

                # endif
            # endfor
            msgs[int(u)] = c_msgs
        # endfor
        return msgs
