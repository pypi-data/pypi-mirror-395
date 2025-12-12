#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2024 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#
from enum import Enum
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from pydantic import BaseModel, ConfigDict
from pydantic import validator


class ColumnType(Enum):
    SET = "set"
    SCALAR = "scalar"
    FREE_STRING = "free_string"
    LIST_OF_A_SET = "list_of_a_set"
    VECTOR = "vector"
    URL = "url"
    JSON = "json"
    TIMESTAMP = "timestamp"
    EMAIL = "email"
    DOMAIN = "domain_name"


class SimpleMLPConfig(BaseModel):
    model_config = ConfigDict(protected_namespaces=())  # Allow fields starting with "model_" to avoid Pydantic warnings
    
    d_in: int
    d_out: int
    d_hidden: Optional[int] = 256
    n_hidden_layers: Optional[int] = 0
    dropout: Optional[float] = 0.3  # Increased from 0.1 for better regularization on imbalanced data
    normalize: Optional[bool] = True
    residual: Optional[bool] = True
    use_batch_norm: Optional[bool] = True


class SetEncoderConfig(BaseModel):
    model_config = ConfigDict(protected_namespaces=())  # Allow fields starting with "model_" to avoid Pydantic warnings
    
    d_model: int
    n_members: int
    normalize_output: Optional[bool] = True  # Config-controlled normalization
    sparsity_ratio: Optional[float] = 0.0  # Ratio of null/missing values (0.0 = dense, 1.0 = all null)
    initial_mixture_logit: Optional[float] = None  # Initial value for mixture logit (None = random small value ~0.1)
                                                    # Positive → prefer learned embeddings, Negative → prefer semantic (BERT)
                                                    # 0.0 = 50/50 mixture, +1.0 ≈ 73% learned, -1.0 ≈ 27% learned


class ScalarEncoderConfig(SimpleMLPConfig):
    d_in: int = 1


class TimestampEncoderConfig(SimpleMLPConfig):
    d_in: int = 12  # 12 temporal features from TimestampCodec


class StringEncoderConfig(SimpleMLPConfig):
    n_hidden_layers: int = 0
    d_model: Optional[int] = None  # Target dimension for stacking (if different from d_out)


class VectorEncoderConfig(SimpleMLPConfig):
    n_hidden_layers: int = 0


class ListOfASetEncoderConfig(BaseModel):
    model_config = ConfigDict(protected_namespaces=())  # Allow fields starting with "model_" to avoid Pydantic warnings
    
    d_model: int
    n_members: int


ColumnEncoderConfigType = Union[
    SetEncoderConfig,
    ScalarEncoderConfig,
    TimestampEncoderConfig,
    StringEncoderConfig,
    ListOfASetEncoderConfig,
    VectorEncoderConfig,
    SimpleMLPConfig,  # Fallback for other types
]


ColumnPredictorConfigType = Union[SimpleMLPConfig]


JointEncoderInConverterConfigType = Union[SimpleMLPConfig]


class SpreadLossConfig(BaseModel):
    model_config = ConfigDict(protected_namespaces=())  # Allow fields starting with "model_" to avoid Pydantic warnings
    
    joint_weight: float = 1
    marginal_weight: float = 1


class LossFunctionConfig(BaseModel):
    model_config = ConfigDict(protected_namespaces=())  # Allow fields starting with "model_" to avoid Pydantic warnings
    
    joint_loss_weight: float = 1
    marginal_loss_weight: float = 1
    spread_loss_weight: float = 1
    spread_loss_config: SpreadLossConfig
    spread_lr_multiplier: Optional[float] = None  # If set, scale spread loss gradients by this factor (e.g., 0.3 = 30% of base LR)
    marginal_loss_scaling_coefficient: Optional[float] = None  # Scaling coefficient applied to marginal loss value (not weight) to match spread/joint magnitudes


class JointEncoderConfig(BaseModel):
    model_config = ConfigDict(protected_namespaces=())  # Allow fields starting with "model_" to avoid Pydantic warnings
    
    # dimensionality of the transformer's internal representation
    d_model: int = 256
    # number of attention heads in the transformer
    n_heads: int = 8
    # Whether to use column encodings.
    # Analogous to positional encodings in language models.
    # FIXME: this parameter should be called "use_additive_positional_encoding_for_columns"
    use_col_encoding: bool = True
    # Number of columns to generate positional encodings for.
    # This is only relevant when use_col_encoding=True
    n_cols: int = None
    # number of transofmer layers to use
    n_layers: int = 1
    # how large the internal feedforward layer should be
    # this factor multiplies d_model
    dim_feedforward_factor: int = 4
    # dropout factor to use in each transformer layer
    dropout: float = 0
    normalize_output: bool = True
    # FIXME: allow a fixed, known value for the positional column embeddings
    # so that we can use embeddings from LLMs (although we'd likely only see)
    # a benefit from this if we were using a pre-trained model that used a
    # similar
    in_converter_configs: Dict[str, JointEncoderInConverterConfigType]
    out_converter_config: SimpleMLPConfig


class FeatrixTableEncoderConfig(BaseModel):
    # NOTE: something I don't like is that the values in different field are not
    # independent, e.g. the number of items in 'cols_in_order' must be equal to 'n_cols',
    # and the values in 'cols_in_order' must be the same as the keys in 'col_types'.
    # What's the best way to enforce this? Does pydantic have a way to handle this?

    # More generally, we'll need a way to enforce that e.g. d_out in the encoder is the
    # same as the input to the joint encoder. Otherwise we'll run into difficult-to-diagnose
    # issues. Also, it will be very difficult to hand-edit json configuration files.

    # One solution, would be to have a system where part of the configuration can be serialized,
    # and another part is overwriten dynamically, so that a model that composes other models could
    # override some of the serialized settings, and enforce that all the parameters match. But then
    # it would result in possibly confusing behavior where the instantiated model is different from
    # what the serialized data might imply.

    # The best of both worlds would be to have a validator tells the user EXACTLY what the problem is
    # with the serialized configuration, and what to do to make it work.

    model_config = ConfigDict(protected_namespaces=())  # Allow fields starting with "model_" to avoid Pydantic warnings
    
    d_model: int
    n_cols: int
    cols_in_order: List[str]
    col_types: Dict[str, ColumnType]
    column_encoders_config: Dict[str, ColumnEncoderConfigType]
    column_predictors_config: Dict[str, ColumnPredictorConfigType]
    # All column predictors for short embeddings share the same config because
    # they're just for UI and visualization so they don't need much fidelity.
    column_predictors_short_config: SimpleMLPConfig
    joint_encoder_config: JointEncoderConfig
    joint_predictor_config: SimpleMLPConfig
    joint_predictor_short_config: SimpleMLPConfig
    loss_config: LossFunctionConfig
