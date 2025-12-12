#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2024 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#
#
#  Copyright (c) 2023, Featrix, Inc. All rights reserved.
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#
import base64
import hashlib
import io
import os
import pickle
import traceback

import torch
import torch.nn as nn

from featrix.neural.device import device
from featrix.neural.embedding_utils import NormalizedEmbedding
from featrix.neural.featrix_token import create_token_batch
from featrix.neural.featrix_token import Token
from featrix.neural.featrix_token import TokenStatus
from featrix.neural.model_config import ColumnType
from featrix.neural.model_config import ListOfASetEncoderConfig
from featrix.neural.model_config import SimpleMLPConfig
from featrix.neural.simple_mlp import SimpleMLP


def split_and_strip(s, delimiter):
    s = str(s)
    v = [ss.strip() for ss in s.split(delimiter)]
    return v


class ListOfASetEncoder(nn.Module):
    def __init__(self, config=ListOfASetEncoderConfig):
        super().__init__()
        self.config = config

        # CRITICAL FIX: Better parameter initialization to prevent NaN corruption
        self._replacement_embedding = nn.Parameter(torch.zeros(config.d_model))
        nn.init.xavier_uniform_(self._replacement_embedding.unsqueeze(0))
        self._replacement_embedding.data = self._replacement_embedding.data.squeeze(0)
        self.embedding = nn.Embedding(config.n_members, config.d_model)
        # Also use better initialization for the main embedding layer
        nn.init.xavier_uniform_(self.embedding.weight)

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
        # CRITICAL: Ensure value is on the same device as module parameters
        # Respect FEATRIX_FORCE_CPU_SINGLE_PREDICTOR env var - force CPU if set
        force_cpu = os.environ.get('FEATRIX_FORCE_CPU_SINGLE_PREDICTOR') == '1'
        
        # Get device from embedding layer
        module_device = None
        if not force_cpu:
            try:
                module_device = next(self.embedding.parameters()).device
            except (StopIteration, AttributeError):
                pass
        
        # Force CPU mode if env var is set
        if force_cpu:
            module_device = torch.device('cpu')
            if list(self.parameters()):
                first_param_device = next(self.parameters()).device
                if first_param_device.type != 'cpu':
                    self.cpu()
        
        # Move value to module device if there's a mismatch
        value = token.value
        if module_device is not None and value.device != module_device:
            value = value.to(device=module_device)
        
        # NOTE: should we normalize before or after averaging?
        out = self.embedding(value).mean(dim=1)

        # override embeddings for unknown and not present tokens
        # Ensure dtype compatibility with mixed precision
        replacement_embedding = self._replacement_embedding.to(dtype=out.dtype)
        out[token.status == TokenStatus.NOT_PRESENT] = replacement_embedding
        out[token.status == TokenStatus.UNKNOWN] = replacement_embedding
        out[token.status == TokenStatus.MARGINAL] = replacement_embedding

        short_vec = nn.functional.normalize(out[:, 0:3], dim=1)
        full_vec = nn.functional.normalize(out, dim=1)

        return short_vec, full_vec

    @staticmethod
    def get_default_config(d_in: int, n_members: int):
        return ListOfASetEncoderConfig(
            d_in=d_in,
            n_members=n_members,
        )


class ListsOfASetCodec(nn.Module):
    def __init__(self, members: set, delimiter: str, enc_dim: int):
        super().__init__()
        self._is_decodable = False

        self.delimiter = delimiter
        # self.members = members

        row_uniques = set(members)

        parts = []
        maxLen = 0
        for u in row_uniques:
            p = u.split(delimiter)
            maxLen = max(maxLen, len(p))
            for pp in p:
                if pp not in parts:
                    pp = pp.strip()  # FIXME: this will bite us somehow.
                    parts.append(pp)

        if maxLen == 1:
            print(f"... warning: maxLen = {maxLen}")
        self.maxLen = maxLen

        # endfor
        # parts is now the unique symbols in the lists across all the rows.
        parts = list(set(parts))  # just to be sure.

        # FIXME: So... customer cannot have <UNKNOWN> in their data? :-)
        assert "<UNKNOWN>" not in parts, "Call Pawel."
        parts.sort()
        uniques = ["<UNKNOWN>"] + parts

        self.enc_dim = enc_dim
        self.members_to_tokens = {member: token for token, member in enumerate(uniques)}
        self.tokens_to_members = {
            token: member for member, token in self.members_to_tokens.items()
        }
        self.n_members = len(uniques)

        self.loss_fn = nn.CrossEntropyLoss()
        self._debug = {}

    def get_codec_name(self):
        return ColumnType.LIST_OF_A_SET

    def get_not_present_token(self):
        return Token(
            value=torch.zeros(1, dtype=self.token_dtype),
            status=torch.tensor([TokenStatus.NOT_PRESENT] * 1),
        )

    def get_encodings_for_2d_plot(self, _min=None, _max=None):
        print("LISTS OF A SET CODEC: get_encodings_for_2d_plot called")
        _members = list(self.members_to_tokens.keys())
        the_members = [
            self.detokenize(Token(value=i, status=TokenStatus.OK))
            for i in range(len(_members))
        ]
        print("....the_members = ", the_members)
        return the_members, self.embedding.weight

    @property
    def token_dtype(self):
        return int

    def tokenize(self, string_list):
        # TODO: must be able to tokenize an entire batch in a single go, and return
        # a batch token.
        parts = split_and_strip(string_list, self.delimiter)
        translated_list = []

        hadKnown = False
        # print("parts...", parts)
        for member in parts:
            if len(translated_list) >= self.maxLen:
                print(f"... truncating... {len(translated_list)} vs {self.maxLen}")
                break

            try:
                member = str(member)
            except Exception:
                translated_list.append(0)  # Unknown index in the list

            if member in self.members_to_tokens:
                translated_list.append(self.members_to_tokens[member])
                hadKnown = True
            else:
                translated_list.append(0)  # Unknown index in the list

        while len(translated_list) < self.maxLen:
            translated_list.append(0)  # Unknown index in the list

        # print("translated_list[%s] = %s" % (len(translated_list), translated_list))
        # FIXME: if translated_list is all unknown?
        # FIXME: if translated_list is empty?
        if not hadKnown:
            # print("GOT UNKNOWN: delimter = __%s__, parts = __%s__" % (self.delimiter, parts))
            # print("MEMBERS:", self.members_to_tokens)
            return Token(
                # Keep on CPU for DataLoader workers - will move to GPU in training loop
                value=torch.tensor([0] * self.maxLen, dtype=torch.long),
                status=TokenStatus.UNKNOWN,
            )
        # tr_unique = list(set(translated_list)) # [0,4]
        # print("tr_unique = ", tr_unique)
        # if tr_unique == {0}:
        #    print("tr_unique = 0")
        #    return Token(
        #        value=torch.tensor([0] * self.maxLen),
        #        status=TokenStatus.UNKNOWN,
        #    )

        assert len(translated_list) == self.maxLen, "mismatched lengths"

        return Token(
            value=torch.tensor(translated_list),
            status=TokenStatus.OK,
        )

    def detokenize(self, token):
        existing = self._debug.get(token, 0)
        existing += 1
        self._debug[token] = existing

        # FIXME: need to parse the token.
        # print("detokenize called: __%s__" % token.value)
        if (
            token.status == TokenStatus.NOT_PRESENT
            or token.status == TokenStatus.UNKNOWN
        ):
            raise ValueError(f"Cannot detokenize a token with status {token.status}.")
        else:
            if token.value in self.tokens_to_members:
                return self.tokens_to_members[token.value]
            else:
                raise ValueError(f"Cannot decode token with value {token.value}.")

    def loss(self, logits, targets):
        return self.loss_fn(logits, targets)

    def loss_single(self, logits, target):
        # Loss function specific to batches of size one, and single targets.

        # We assume that target can be the wrong type, because it's type depends on the
        # types of other target variables it's batched with, and that it's provided as a
        # single value. Therefore, it must be cast to the correct type, and a dimension
        # must be added via `unsqueeze`.
        target = target.long().unsqueeze(dim=0)

        return self.loss(logits, target)

    def save(self):
        # we create a json dict.
        buffer = io.BytesIO()
        torch.save(self.state_dict(), buffer)

        buffer_b64 = "base64:" + str(
            base64.standard_b64encode(buffer.getvalue()).decode("utf8")
        )
        checksum = hashlib.md5(buffer.getvalue()).hexdigest()
        enc_bytes = pickle.dumps(self.members)
        members_b64 = "base64:" + str(
            base64.standard_b64encode(enc_bytes).decode("utf8")
        )

        d = {
            "type": "ListsOfASetCodec",
            "embedding": buffer_b64,
            "embedding_checksum": checksum,
            "enc_dim": self.enc_dim,
            "members": members_b64,
        }

        return d

    def load(self, j):
        d_type = j.get("type")
        assert d_type == "ListsOfASetCodec", (
            "wrong load method called for __%s__" % d_type
        )
        self.enc_dim = j.get("enc_dim")

        ########################
        # Set up members/uniques
        ########################
        members = j.get("members")
        assert members.startswith("base64:")
        members = members[6:]

        try:
            # theEncoder is a string 'b'<>'' ... sigh
            # print("members = __%s__" % members)
            e64 = base64.standard_b64decode(members)  # uniques[2:-1])
            unpickledEncoder = pickle.loads(e64)  # pickleBytes.read())
            # print("unpickledEncoder = ", unpickledEncoder)
            self.members = unpickledEncoder  # encoders[key] = unpickledEncoder
        except Exception:
            print(f"PICKLE ERROR for = __{j}__")
            traceback.print_exc()

        # copied from constructor
        uniques = sorted(list(self.members))
        self.members_to_tokens = {member: token for token, member in enumerate(uniques)}
        self.tokens_to_members = {
            token: member for member, token in self.members_to_tokens.items()
        }

        ########################
        # Set up embedding stuff
        ########################
        embed = j.get("embedding")
        embed_checksum = j.get("embedding_checksum")

        if embed.startswith("base64:"):
            embed = embed[6:]

        r64 = base64.standard_b64decode(embed)
        r_checksum64 = hashlib.md5(r64).hexdigest()

        if r_checksum64 != embed_checksum:
            print(f"CHECKSUMS {r_checksum64} and {embed_checksum} DO NOT MATCH - !")
            return

        buffer = io.BytesIO(r64)
        theDict = torch.load(buffer)
        # print("theDict = ", theDict)

        # Without the below 'initializations', the load_state_dict() fails due to Size mismatches.
        self._unknown_embedding = nn.Parameter(torch.randn(self.enc_dim))
        self._not_present_embedding = nn.Parameter(torch.randn((self.enc_dim)))
        self.embedding = NormalizedEmbedding(len(uniques), self.enc_dim)
        self.load_state_dict(theDict)
        return

    # def set_device(self, device):
    #     self.embedding.set_device(device)
    #     return


def runTest():
    colors = [
        ["blue", "red", "green"],
        ["cyan"],
        ["cyan", "magenta", "black", "pink", "orange"],
        ["yellow", "blue"],
    ]

    colorStrList = []
    for c in colors:
        colorStrList.append(",".join(c))

    # Save what we make.
    codec = ListsOfASetCodec(colorStrList, delimiter=",", enc_dim=50)
    # jj = codec.save()
    tt = codec.tokenize("yellow,red")
    print(tt)
    tt_batch = create_token_batch([tt])
    embedding = codec.encode(tt_batch)
    print(embedding)

    #    print(codec.)

    # Load what we saved.
    #    newCodec = ListsOfASetCodec([], enc_dim=50)
    #    newCodec.load(jj)

    #    assert newCodec.members == codec.members
    #    assert newCodec.enc_dim == codec.enc_dim
    #    assert torch.equal(newCodec.unknown, codec.unknown)
    #    assert torch.equal(newCodec.embedding.embed.weight, codec.embedding.embed.weight)
    #    print("PASS!")
    #    print(newCodec.members)
    return


def test_strip():
    s = "9223;  9441"
    p = split_and_strip(s, ";")
    print(p)
    return


if __name__ == "__main__":
    #    runTest()
    test_strip()
