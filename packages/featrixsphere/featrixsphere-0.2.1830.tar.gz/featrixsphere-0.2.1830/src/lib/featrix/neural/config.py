#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2024 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

"""
Neural network configuration that can be set from outside.
"""

import os


class NeuralConfig:
    """Configuration for neural network training."""
    
    def __init__(self):
        # Read from environment variable FEATRIX_D_MODEL, default to 128
        d_model_env = os.getenv("FEATRIX_D_MODEL")
        if d_model_env:
            try:
                self.d_model = int(d_model_env)
            except ValueError:
                self.d_model = 128  # Fallback to default if invalid
        else:
            self.d_model = 128  # Default embedding dimension
    
    def set_d_model(self, value: int):
        """Set the embedding dimension."""
        self.d_model = value
    
    def get_d_model(self) -> int:
        """Get the embedding dimension."""
        return self.d_model


# Global instance
_config = NeuralConfig()


def get_config() -> NeuralConfig:
    """Get the global neural config instance."""
    return _config

