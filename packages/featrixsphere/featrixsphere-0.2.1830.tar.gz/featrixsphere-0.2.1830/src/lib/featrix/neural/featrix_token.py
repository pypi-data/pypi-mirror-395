#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2024 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#
from enum import IntEnum
from enum import unique

import torch
import numpy as np

from .device import device


@unique
class TokenStatus(IntEnum):
    NOT_PRESENT = 0
    UNKNOWN = 1
    OK = 2
    MARGINAL = 3
    # NOTE: Potentially, we could add another type, which is "VALUE_OMMITTED", for fields that are
    #       optional, and were not provided


# The most important thing about the token is that
# it's easily expressed in batch form.
# Tokens must be expressed in batch form because they are
# fed into neural networks, which expect batch input.
# @dataclass
# class Token:
#     value: Any
#     status: TokenStatus
#     attention_mask: Any = field(default=None)


class Token(dict):
    def __init__(self, value, status, attention_mask=None):
        super().__init__()
        
        # Detach tensors for multiprocessing compatibility (DataLoader workers)
        # Without this, tensors with requires_grad=True can't be pickled
        if isinstance(value, torch.Tensor) and value.requires_grad:
            value = value.detach()
        
        self["value"] = value
        self["status"] = status

        if attention_mask is not None:
            # Also detach attention mask if it's a tensor
            if isinstance(attention_mask, torch.Tensor) and attention_mask.requires_grad:
                attention_mask = attention_mask.detach()
            self["attention_mask"] = attention_mask

    @property
    def value(self):
        return self["value"]

    @property
    def status(self):
        return self["status"]

    @status.setter
    def status(self, value):
        self["status"] = value

    @property
    def attention_mask(self):
        if "attention_mask" in self:
            return self["attention_mask"]
        else:
            return None


def parse_floats_properly(s):
    # Handle numeric types that shouldn't go through string parsing
    if isinstance(s, (int, float, np.integer, np.floating)):
        # Convert numeric values directly to float32
        return float(s)
    
    # Handle None/NaN cases
    if s != s:  # NaN check
        return 0.0
        
    if s is None or s == "" or (hasattr(s, '__len__') and len(s) == 0):
        return 0.0

    # Handle string parsing (original logic)
    s_str = str(s)
    if s_str[0] == "[":
        s_str = s_str[1:]
    if s_str[-1] == "]":
        s_str = s_str[:-1]
    parts = s_str.split(",")
    fl = []
    for p in parts:
        fl.append(float(p))
    return fl


class TokenBatch(dict):
    def __init__(self, token_list):
        values = []
        statuses = []
        attention_masks = []

        for i, token in enumerate(token_list):
            # Check for None tokens and replace with NOT_PRESENT token
            if token is None:
                # Create a default NOT_PRESENT token with value 0
                token = Token(value=0, status=TokenStatus.NOT_PRESENT)
            
            values.append(token.value)
            statuses.append(token.status)
            attention_masks.append(token.attention_mask)

        if len(values) == 0:
            # FIXME: Might be bad.
            print("We're in the danger zone.")
            return torch.tensor(values, dtype=torch.float32)
        elif isinstance(values[0], torch.Tensor):
            try:
                values = torch.stack(values, dim=0)
                # Ensure float32 dtype for tensor values too
                if values.dtype != torch.float32:
                    values = values.to(dtype=torch.float32)
            except RuntimeError as e:
                # Multi-device issue - move all tensors to the same device
                devices_found = set()
                for idx, vv in enumerate(values):
                    devices_found.add(str(vv.device))
                    original_dtype = vv.dtype
                    values[idx] = vv.to(device=device, dtype=torch.float32)  # Force float32 here too
                values = torch.stack(values, dim=0)
        else:
            try:
                # Convert all values to float32 consistently
                if all(isinstance(v, (int, float, np.integer, np.floating)) for v in values):
                    # All numeric values - convert to float32 directly
                    values = torch.tensor(values, dtype=torch.float32)
                else:
                    # Mixed or non-numeric values - use original tensor creation but force float32
                    values = torch.tensor(values, dtype=torch.float32)
            except:
                # FIXME: We are processing a list of strings or complex data...
                new_values = []
                for v in values:
                    parsed = parse_floats_properly(v)
                    new_values.append(parsed)

                try:
                    values = torch.tensor(new_values, dtype=torch.float32)
                except:
                    raise Exception("Failed to convert values to tensor")

            # mps can't handle float64, so convert to float32
            if values.dtype == torch.float64:
                values = values.float()

        if all([mask is None for mask in attention_masks]):
            attention_mask = None
        else:
            try:
                attention_mask = torch.stack(attention_masks, dim=0)
            except RuntimeError as e:
                # Multi-device issue for attention masks - move to same device
                for idx, mask in enumerate(attention_masks):
                    if mask is not None and hasattr(mask, 'device'):
                        original_dtype = mask.dtype
                        attention_masks[idx] = mask.to(device=device, dtype=original_dtype)
                attention_mask = torch.stack(attention_masks, dim=0)

        statuses = torch.tensor(statuses, dtype=int)

        self["values"] = values
        self["status"] = statuses
        self["attention_mask"] = attention_mask
        
        self.to(device)

    @property
    def value(self):
        return self["values"]

    @property
    def status(self):
        return self["status"]

    @status.setter
    def status(self, value):
        self["status"] = value

    @value.setter
    def value(self, value):
        self["values"] = value

    @property
    def attention_mask(self):
        if "attention_mask" in self:
            return self["attention_mask"]
        else:
            return None

    def __len__(self):
        return self.value.shape[0]

    def to(self, device):
        if hasattr(self.value, 'to'):
            # FORCE float32 dtype for values to prevent int64 issues
            self.value = self.value.to(device=device, dtype=torch.float32)
        if hasattr(self.status, 'to'):
            original_dtype = self.status.dtype
            self.status = self.status.to(device=device, dtype=original_dtype)
        if self.attention_mask is not None and hasattr(self.attention_mask, 'to'):
            original_dtype = self.attention_mask.dtype
            self.attention_mask = self.attention_mask.to(device=device, dtype=original_dtype)
        return self

    @staticmethod
    def from_tensors(value: torch.Tensor, status: torch.Tensor, attention_mask: torch.Tensor=None):
        # just use dummy value and status
        out = TokenBatch([Token(value=0, status=TokenStatus.UNKNOWN)])
        out.status = status
        
        # FORCE float32 dtype for input value tensor to prevent int64 issues
        if hasattr(value, 'to') and value.dtype != torch.float32:
            value = value.to(dtype=torch.float32)
        out.value = value
        
        # TODO: should out.attention_mask be set here? It's None by default.
        return out



def set_not_present(token: Token):
    # Return a Token with the same value, but changes status to NOT_PRESENT.
    return Token(
        value=token.value,
        status=TokenStatus.NOT_PRESENT,
        attention_mask=token.attention_mask,
    )


def set_unknown(token: Token):
    # Return a Token with the same value, but changes status to UNKNOWN.
    return Token(
        value=token.value,
        status=TokenStatus.UNKNOWN,
        attention_mask=token.attention_mask,
    )


def set_marginal(token: Token):
    # Return a Token with the same value, but changes status to UNKNOWN.
    return Token(
        value=token.value,
        status=TokenStatus.MARGINAL,
        attention_mask=token.attention_mask,
    )

def create_token_batch(token_list):
    return TokenBatch(token_list)

