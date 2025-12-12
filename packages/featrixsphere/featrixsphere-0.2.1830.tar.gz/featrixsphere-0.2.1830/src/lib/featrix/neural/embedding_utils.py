#
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#
#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2024 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#
import torch.nn as nn


class NormalizedEmbedding(nn.Module):
    # NOTE: an alternative to defining our own custom NormalizedEmbedding class
    # would be to use the max_norm parameter available in nn.Embeddings.
    # As explained in the documentation, the weights of such an embedding are
    # updated in-place, and special handling is required to correctly pass
    # gradient info through the module.
    # this is explained in more detail at https://pytorch.org/docs/stable/generated/torch.nn.Embedding.html

    def __init__(self, *args, **kwargs):
        super(NormalizedEmbedding, self).__init__()
        self.embed = nn.Embedding(*args, **kwargs)

    @property
    def weight(self):
        # Return normalized weights
        return nn.functional.normalize(self.embed.weight, dim=-1)

    def forward(self, input):
        # Get embeddings and normalize them
        # print("NormalizedEmbedding:", input)
        embeddings = self.embed(input)
        # embeddings.to(self._device)
        return nn.functional.normalize(embeddings, dim=-1)
