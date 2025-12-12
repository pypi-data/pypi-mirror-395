#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2023-2024, Featrix, Inc. All rights reserved.
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

import logging
import traceback

from enum import Enum

from featrix.neural.scalar_codec import ScalarCodec
from featrix.neural.set_codec import SetCodec
from featrix.neural.featrix_token import TokenStatus

logger = logging.getLogger(__name__)


class Result(Enum):
    OK = "OK"
    ERROR = "Error"
    WARNING = "Warning"
    INFO = "Info"


def RunGuardrails(query, fsp, issues_only=True):
    es = fsp.embedding_space

    if isinstance(query, dict):
        query = [query]

    cols = list(es.col_codecs.keys())
    results = {}

    def add_result(col, is_error: Result, index, line):
        if issues_only and is_error == Result.OK:
            return
        line = f"{is_error.value}: {line}"

        existing = results.get(col, {})
        count = existing.get(line, {"count": 0, "indexList": []})
        count["count"] += 1
        if is_error != Result.OK:
            count["indexList"].append(index)
        existing[line] = count
        results[col] = existing
        return

    for idx, entry in enumerate(query):
        query_columns = list(entry.keys())
        for query_column in query_columns:
            # print(idx, query_column)
            if query_column not in cols:
                # print("-----error-----")
                add_result(
                    query_column,
                    Result.WARNING,
                    idx,
                    f"Column '{query_column}' not in embedding_space space.",
                )
                continue

            add_result(
                query_column, Result.OK, idx, "Column found in embedding_space space"
            )
            codec = es.col_codecs.get(query_column)

            if codec is None:
                add_result(query_column, Result.ERROR, idx, f"Internal error with column '{query_column}' (codec).",)
                continue
                
            # ok, it is available... if it's a set, is it in the set?
            if isinstance(codec, SetCodec):
                add_result(query_column, Result.OK, idx, "Categorical variable")
                t = None
                try:
                    t = codec.tokenize(entry[query_column])
                except Exception as e:  # noqa
                    traceback.print_exc()
                    add_result(
                        query_column,
                        Result.ERROR,
                        idx,
                        f"categorical value raised error during tokenization: {e}",
                    )

                if t is not None:
                    if t.status == TokenStatus.OK:
                        add_result(
                            query_column, Result.OK, idx, "categorical value is known"
                        )
                    else:
                        if entry[query_column] is None: # [] notation ok -- query_col came from entry.keys
                            add_result(
                                query_column,
                                Result.WARNING,
                                idx,
                                "categorical value is (null)",
                            )
                        elif entry[query_column] != entry[query_column]:
                            add_result(
                                query_column,
                                Result.WARNING,
                                idx,
                                "categorical value is (NaN)",
                            )
                        else:
                            add_result(
                                query_column,
                                Result.WARNING,
                                idx,
                                f"categorical value '{entry[query_column]}' is UNKNOWN: expected one of {str(list(codec.members_to_tokens.keys()))}",
                            )
            elif isinstance(codec, ScalarCodec):
                add_result(query_column, Result.OK, idx, "Scalar variable")
                t = None
                try:
                    t = codec.tokenize(entry[query_column])
                except Exception as e:
                    traceback.print_exc()
                    add_result(
                        query_column,
                        Result.ERROR,
                        idx,
                        f"scalar value raised error during tokenization: {e}",
                    )

                if t is not None:
                    if t.status == TokenStatus.OK:
                        add_result(query_column, Result.OK, idx, "value tokenized OK")
                        # FIXME: check range.
                        
                        try:
                            v = entry[query_column]
                            v = float(v)
                        except Exception as err:
                            traceback.print_exc()
                            raw_v = entry[query_column]
                            if raw_v is None:
                                raw_v = "(null)"
                            if raw_v == "":
                                raw_v = "(empty string)"
                            add_result(
                                query_column,
                                Result.ERROR,
                                idx,
                                f"scalar value \"{raw_v}\" unable to convert to scalar: {err}",
                            )
                        # Calculate normalized value (z-score)
                        # This is what the encoder will see
                        if codec.stdev == 0:
                            normalized_value = v - codec.mean
                        else:
                            normalized_value = (v - codec.mean) / codec.stdev
                        
                        # Training distribution bounds
                        codec_min = codec.mean - (4 * codec.stdev)
                        codec_max = codec.mean + (4 * codec.stdev)

                        try:
                            # CRITICAL: Check for encoder clamping at ±100 standard deviations
                            # Values beyond ±100σ get clamped, causing saturation
                            ENCODER_CLAMP_LIMIT = 100.0
                            
                            if abs(normalized_value) > ENCODER_CLAMP_LIMIT:
                                # SEVERE: Value will be clamped - predictions will be saturated
                                clamped_to = ENCODER_CLAMP_LIMIT if normalized_value > 0 else -ENCODER_CLAMP_LIMIT
                                add_result(
                                    query_column,
                                    Result.ERROR,
                                    idx,
                                    f"🚨 CLAMPING: scalar value {v:.2e} is {abs(normalized_value):.1f}σ from training mean "
                                    f"(>{ENCODER_CLAMP_LIMIT}σ limit). Value will be CLAMPED to {clamped_to}σ. "
                                    f"Predictions will be SATURATED and unreliable. "
                                    f"Training range: [{codec_min:.2e}, {codec_max:.2e}] (±4σ)",
                                )
                                logger.warning(
                                    f"🚨 GUARDRAIL CLAMPING DETECTED: Column '{query_column}' at index {idx}: "
                                    f"value={v:.2e}, normalized={normalized_value:.1f}σ, "
                                    f"will clamp to ±{ENCODER_CLAMP_LIMIT}σ. "
                                    f"Training: mean={codec.mean:.2e}, std={codec.stdev:.2e}"
                                )
                            
                            elif abs(normalized_value) > 20.0:
                                # SEVERE EXTRAPOLATION: Far outside training, but not yet clamped
                                add_result(
                                    query_column,
                                    Result.WARNING,
                                    idx,
                                    f"⚠️  SEVERE EXTRAPOLATION: scalar value {v:.2e} is {abs(normalized_value):.1f}σ from training mean. "
                                    f"Prediction quality highly uncertain. "
                                    f"Training range: [{codec_min:.2e}, {codec_max:.2e}] (±4σ)",
                                )
                                logger.warning(
                                    f"⚠️  GUARDRAIL SEVERE EXTRAPOLATION: Column '{query_column}' at index {idx}: "
                                    f"value={v:.2e}, normalized={abs(normalized_value):.1f}σ outside training distribution"
                                )
                            
                            elif v > codec_max:
                                # MODERATE EXTRAPOLATION: Beyond ±4σ but < 20σ
                                add_result(
                                    query_column,
                                    Result.WARNING,
                                    idx,
                                    f"Extrapolation: scalar value {v:.2e} is {normalized_value:.1f}σ above training mean "
                                    f"(> {codec_max:.2e}, 4σ upper limit). Prediction may be less accurate.",
                                )
                                logger.info(
                                    f"ℹ️  GUARDRAIL EXTRAPOLATION: Column '{query_column}' at index {idx}: "
                                    f"value={v:.2e} is {normalized_value:.1f}σ (>{codec_max:.2e})"
                                )
                            
                            elif v < codec_min:
                                # MODERATE EXTRAPOLATION: Beyond ±4σ but < 20σ
                                add_result(
                                    query_column,
                                    Result.WARNING,
                                    idx,
                                    f"Extrapolation: scalar value {v:.2e} is {abs(normalized_value):.1f}σ below training mean "
                                    f"(< {codec_min:.2e}, 4σ lower limit). Prediction may be less accurate.",
                                )
                                logger.info(
                                    f"ℹ️  GUARDRAIL EXTRAPOLATION: Column '{query_column}' at index {idx}: "
                                    f"value={v:.2e} is {abs(normalized_value):.1f}σ (<{codec_min:.2e})"
                                )
                        
                        except Exception as err:
                            traceback.print_exc()
                            add_result(
                                query_column,
                                Result.ERROR,
                                idx,
                                f"scalar value {v} raised error during range checking: {err}",
                            )
                            logger.error(
                                f"❌ GUARDRAIL ERROR: Column '{query_column}' at index {idx}: "
                                f"exception during range checking: {err}"
                            )
                    else:
                        if entry.get(query_column) is None:
                            add_result(
                                query_column,
                                Result.WARNING,
                                idx,
                                "scalar value is (null)",
                            )
                        elif entry[query_column] != entry[query_column]:
                            add_result(
                                query_column,
                                Result.WARNING,
                                idx,
                                "scalar value is (NaN)",
                            )
                        else:
                            add_result(
                                query_column,
                                Result.ERROR,
                                idx,
                                f"scalar value '{entry[query_column]}' did not tokenize",
                            )

            else:
                add_result(
                    query_column, Result.INFO, idx, "value not checked for guardrails."
                )

    return results
