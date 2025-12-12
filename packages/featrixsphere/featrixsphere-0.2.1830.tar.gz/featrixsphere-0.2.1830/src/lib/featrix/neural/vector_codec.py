#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2024 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#
import base64
import hashlib
import io
import math
import os
import traceback

import numpy as np
import torch
import torch.nn as nn

from featrix.neural.device import device
from featrix.neural.featrix_token import set_not_present
from featrix.neural.featrix_token import Token
from featrix.neural.featrix_token import TokenStatus
from featrix.neural.model_config import ColumnType
from featrix.neural.model_config import VectorEncoderConfig
from featrix.neural.simple_mlp import SimpleMLP
from featrix.neural.simple_mlp import SimpleMLPConfig

torch.set_printoptions(threshold=10_000)
torch.set_printoptions(profile="full")
torch.set_printoptions(linewidth=240)


class VectorEncoder(nn.Module):
    def __init__(self, config: VectorEncoderConfig):
        super().__init__()

        self.config = config

        # CRITICAL FIX: Better parameter initialization to prevent NaN corruption
        self._replacement_embedding = nn.Parameter(torch.zeros(config.d_out))
        nn.init.xavier_uniform_(self._replacement_embedding.unsqueeze(0))
        self._replacement_embedding.data = self._replacement_embedding.data.squeeze(0)

        self.mlp_encoder = SimpleMLP(config)

    @property
    def unknown_embedding(self):
        # FIXME: what was the rationale for unknown embeddings again?
        return nn.functional.normalize(self._replacement_embedding, dim=-1)

    @property
    def marginal_embedding(self):
        # We return the same vector as NOT_PRESENT token because they are treated the
        # same from a probabilistic point of view by the network, and should be treated
        # the same when the model is queried.
        # However, they must remain distinct tokens because the masking strategy for the loss
        # function is affected by whether a field is NOT_PRESENT, or MARGINAL.
        return nn.functional.normalize(self._replacement_embedding, dim=-1)

    @property
    def not_present_embedding(self):
        return nn.functional.normalize(self._replacement_embedding, dim=-1)

    def forward(self, token):
        try:
            # CRITICAL: Ensure value is on the same device as module parameters
            # Respect FEATRIX_FORCE_CPU_SINGLE_PREDICTOR env var - force CPU if set
            force_cpu = os.environ.get('FEATRIX_FORCE_CPU_SINGLE_PREDICTOR') == '1'
            
            # Get device from MLP encoder (prefer module's device over global device)
            module_device = None
            if not force_cpu:
                try:
                    module_device = next(self.mlp_encoder.parameters()).device
                except (StopIteration, AttributeError):
                    # Fallback to global device if module has no parameters
                    module_device = device
            
            # Force CPU mode if env var is set
            if force_cpu:
                module_device = torch.device('cpu')
                if list(self.parameters()):
                    first_param_device = next(self.parameters()).device
                    if first_param_device.type != 'cpu':
                        self.cpu()
            
            # Move value to module device
            value = token.value
            if module_device is not None and value.device != module_device:
                value = value.to(device=module_device)
            else:
                value = token.value
            
            out = self.mlp_encoder(value)

            # override embeddings for unknown and not present tokens
            # Ensure dtype compatibility with mixed precision
            replacement_embedding = self._replacement_embedding.to(dtype=out.dtype)
            out[token.status == TokenStatus.NOT_PRESENT] = replacement_embedding
            out[token.status == TokenStatus.UNKNOWN] = replacement_embedding
            out[token.status == TokenStatus.MARGINAL] = replacement_embedding

            short_vec = nn.functional.normalize(out[:, 0:3], dim=1)
            full_vec = nn.functional.normalize(out, dim=1)

            return short_vec, full_vec
        except Exception as err:
            #print(token.value)
            traceback.print_exc()
            raise err
            print(token.value.dtype)

    @staticmethod
    def get_default_config(d_in: int, d_out: int):
        return VectorEncoderConfig(
            d_in=d_in,
            d_out=d_out,
            normalize=False,  # don't normalize to allow for short and full embeddings
        )


count = 0

class VectorCodec(nn.Module):
    # def __init__(self, in_dim: int, enc_dim: int, debugName=None, use_mlp=True):
    def __init__(self, in_dim: int, enc_dim: int, debugName=None):
        super().__init__()
        assert in_dim > 0
        assert enc_dim > 0
        # self._use_mlp = use_mlp

        self._numEncodeCalls = 0
        self.colName = debugName  # HACK
        self._is_decodable = False
        self.debug_name = "%50s" % str(debugName)
        self.in_dim = in_dim
        self.enc_dim = enc_dim
        
        # self.to(device)

    def get_codec_name(self):
        return ColumnType.VECTOR

    def get_not_present_token(self):
        tok = self.tokenize("")
        return set_not_present(tok)

    @property
    def token_dtype(self):
        return int

    def tokenize(self, value):
        """Here we actually do both the tokenize & encode."""
        isNan = False
        if value is None:
            isNan = True
        
        if (
            type(value) == float
            or type(value) == int
            or type(value) == np.float64
            or type(value) == np.float32
        ):
            if math.isnan(value):
                isNan = True

        if type(value) == list:
            # Keep on CPU for DataLoader workers - will move to GPU in collate_fn or training
            value = torch.tensor(value, dtype=torch.float32)

        if isNan or len(value) != self.in_dim:
            # Keep on CPU for DataLoader workers - will move to GPU in collate_fn or training
            result = Token(
                value=torch.zeros(self.in_dim, dtype=torch.float32),
                status=TokenStatus.UNKNOWN,
            )
        else:
            result = Token(value=value, status=TokenStatus.OK)
        global count
        count += 1
        # assert count < 100, "Died."
        if count < 10:
            print(f"VECTOR {self.debug_name}:{count}: value=__{str(value)[:100]}__ {type(value)} --> {str(result)[:100]} ")
        return result

    def encode(self, token: Token):
        # print("token...", token)
        try:
            return self.encoder(token)
        except:
            print("token = ", token)
            print("token.value = ", token.value)
            traceback.print_exc()
            os._exit(2)


if __name__ == "__main__":
    # from Token import create_token_batch, set_not_present, set_unknown
    from featrix.neural.featrix_token import (
        create_token_batch,
        set_not_present,
        set_unknown,
    )

    d_embed = 384  # FIXME: somewhere this is defined.
    enc_dim = 128
    sc = VectorCodec(in_dim=d_embed, enc_dim=enc_dim)
    print(sc.mlp_encoder)

    v = [1] * d_embed

    token = sc.tokenize(v)
    # print("the real token:", token)
    token_not_present = set_not_present(token)
    token_unknown = set_unknown(token)

    tokens = create_token_batch([token, token_not_present, token_unknown])
    # print("tokens = ", tokens)
    # print("---")
    out = sc.encode(tokens)
    print("out = ", out)
    print("out.shape = ", out.shape)
    assert out.shape[0] == 3  # we created a batch of 3.
    assert out.shape[1] == enc_dim
    print(out.shape)

    # runStringSaveLoadTest()
