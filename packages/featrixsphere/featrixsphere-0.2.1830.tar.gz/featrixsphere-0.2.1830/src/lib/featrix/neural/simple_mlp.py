#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2024 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#
from dataclasses import dataclass
import logging

import torch
import torch.nn as nn
import torch.nn.functional as F

from featrix.neural.model_config import SimpleMLPConfig

logger = logging.getLogger(__name__)

# class SimpleMLP(nn.Module):
#     def __init__(
#         self, d_in, d_out, d_hidden, hidden_layers=0, dropout=0.1, normalize=True
#     ):
#         super().__init__()

#         if hidden_layers == 0:
#             self.model = nn.Linear(d_in, d_out)
#         else:
#             layers_prefix = [
#                 nn.Linear(d_in, d_hidden),
#             ]

#             layers_middle = []
#             for _ in range(hidden_layers - 1):
#                 layers_middle.append(nn.LeakyReLU())
#                 layers_middle.append(nn.Linear(d_hidden, d_hidden))

#             layers_suffix = [
#                 nn.BatchNorm1d(d_hidden, affine=False),
#                 nn.LeakyReLU(),
#                 nn.Dropout(p=dropout),
#                 nn.Linear(d_hidden, d_out),
#             ]

#             layers = layers_prefix + layers_middle + layers_suffix

#             self.model = nn.Sequential(*layers)

#         self.normalize = normalize

#     def forward(self, input):
#         out = self.model(input)
#         if self.normalize:
#             out = nn.functional.normalize(out, dim=1)
#         return out


class SimpleMLP(nn.Module):
    def __init__(
        # self, d_in, d_out, d_hidden, hidden_layers=0, dropout=0.1, normalize=True, residual=True, use_batch_norm=True,
        self,
        config: SimpleMLPConfig,
    ):
        super().__init__()

        self.config = config

        # If there's 0 requested hidden layers, we just use a single linear layer.
        if config.n_hidden_layers == 0:
            self.single_layer = nn.Linear(config.d_in, config.d_out)

        self.linear_in = nn.Linear(config.d_in, config.d_hidden, bias=True)
        self.linear_out = nn.Linear(config.d_hidden, config.d_out, bias=True)

        module_list = []
        for _ in range(config.n_hidden_layers):
            if config.use_batch_norm:
                modules = [
                    nn.Linear(config.d_hidden, config.d_hidden),
                    nn.BatchNorm1d(config.d_hidden),
                    # nn.LayerNorm(d_hidden),
                    nn.GELU(),
                    nn.Dropout(config.dropout),
                ]
            else:
                modules = [
                    nn.Linear(config.d_hidden, config.d_hidden),
                    nn.GELU(),
                    nn.Dropout(config.dropout),
                ]

            module_list.append(nn.Sequential(*modules))

        self.layers = nn.ModuleList(module_list)
        
        # Debug flag for logging batch norm statistics
        # Only enable for debugging - logs every forward pass (very verbose!)
        self.debug_batchnorm = True

    def log_batchnorm_stats(self):
        """Log statistics about all BatchNorm layers in the model."""
        if not self.config.use_batch_norm:
            logger.info("🔍 BatchNorm: Not using batch normalization")
            return
            
        logger.info(f"🔍 BatchNorm Debug - Model training mode: {self.training}")
        
        for layer_idx, layer in enumerate(self.layers):
            for module_idx, module in enumerate(layer):
                if isinstance(module, nn.BatchNorm1d):
                    bn = module
                    logger.info(f"🔍 BatchNorm Layer {layer_idx}.{module_idx}:")
                    logger.info(f"   Training mode: {bn.training}")
                    logger.info(f"   Num batches tracked: {bn.num_batches_tracked.item() if bn.num_batches_tracked is not None else 'N/A'}")
                    if bn.running_mean is not None:
                        logger.info(f"   Running mean: min={bn.running_mean.min().item():.4f}, max={bn.running_mean.max().item():.4f}, std={bn.running_mean.std().item():.4f}")
                    if bn.running_var is not None:
                        logger.info(f"   Running var: min={bn.running_var.min().item():.4f}, max={bn.running_var.max().item():.4f}, mean={bn.running_var.mean().item():.4f}")
                    if bn.weight is not None:
                        logger.info(f"   Gamma (weight): min={bn.weight.min().item():.4f}, max={bn.weight.max().item():.4f}")
                    if bn.bias is not None:
                        logger.info(f"   Beta (bias): min={bn.bias.min().item():.4f}, max={bn.bias.max().item():.4f}")

    def forward(self, x):
        if self.config.n_hidden_layers == 0:
            return self.single_layer(x)

        # x = self.batch_norm_in(x)
        x_input = x
        x = self.linear_in(x)

        for layer_idx, layer in enumerate(self.layers):
            x_before = x
            
            if self.config.residual:
                x = x + layer(x)
            else:
                x = layer(x)
            
            # Debug: Check if output changed (backwards compatible - check if attribute exists)
            # Only log during training mode to reduce eval noise
            # COMMENTED OUT: Too verbose, clutters logs
            # if getattr(self, 'debug_batchnorm', False) and self.config.use_batch_norm and self.training:
            #     x_diff = (x - x_before).abs().mean().item() if not self.config.residual else (x - x_before - layer(x_before)).abs().mean().item()
            #     logger.debug(f"🔍 Layer {layer_idx} output change: {x_diff:.6f}")


        x = self.linear_out(x)

        if self.config.normalize:
            x_before_norm = x
            x = F.normalize(x, p=2, dim=-1)
            # Backwards compatible - check if attribute exists
            # Only log during training mode to reduce eval noise
            if getattr(self, 'debug_batchnorm', False) and self.training:
                norm_change = (x - x_before_norm).abs().mean().item()
                logger.debug(f"🔍 Output normalization change: {norm_change:.6f}")

        return x

    # def __init__(
    #     self, d_in, d_out, d_hidden, hidden_layers=0, dropout=0.1, normalize=True
    # ):
    #     super().__init__()

    #     if hidden_layers == 0:
    #         self.model = nn.Linear(d_in, d_out)
    #     else:
    #         layers_prefix = [
    #             nn.Linear(d_in, d_hidden),
    #         ]

    #         layers_middle = []
    #         # for _ in range(hidden_layers - 1):
    #         #     layers_middle.append(nn.LeakyReLU())
    #         #     layers_middle.append(nn.Linear(d_hidden, d_hidden))

    #         layers_suffix = [
    #             # nn.BatchNorm1d(d_hidden, affine=False),
    #             # nn.LeakyReLU(),
    #             # nn.Dropout(p=dropout),
    #             nn.Linear(d_hidden, d_out),
    #         ]

    #         layers = layers_prefix + layers_middle + layers_suffix

    #         self.model = nn.Sequential(*layers)

    #     self.linear = nn.Linear(d_in, d_out)
    #     # self.linear_in = nn.Linear(d_in, d_hidden, bias=True)
    #     # self.linear_out = nn.Linear(d_hidden, d_hidden, bias=True)

    #     self.linear_in = nn.Linear(d_in, d_hidden)
    #     self.linear_out = nn.Linear(d_hidden, d_out)

    #     self.normalize = normalize

    # def forward(self, input):
    #     # out = self.model(input)
    #     # if self.normalize:
    #     #     out = nn.functional.normalize(out, dim=1)

    #     # x = self.batch_norm_in(x)
    #     x = self.linear_in(input)

    #     # layers = self.layers

    #     # for layer in layers:
    #     #     if self.residual:
    #     #         x = x + layer(x)
    #     #     else:
    #     #         x = layer(x)

    #     x = self.linear_out(x)

    #     # x = self.linear(input)

    #     if self.normalize:
    #         x = F.normalize(x, p=2, dim=1)

    #     return x
    #     # return out
