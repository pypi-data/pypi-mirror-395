import random

import numpy as np
import torch

# Based on https://pytorch.org/docs/stable/notes/randomness.html

# NOTE in particular: Completely reproducible results are not guaranteed across PyTorch releases,
# individual commits, or different platforms. Furthermore, results may not be reproducible between
# CPU and GPU executions, even when using identical seeds.


def set_seed(seed):
    # Python
    random.seed(seed)

    # PyTorch
    torch.manual_seed(seed)
    # set seed for cuda operations (only if CUDA is available)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        # to ensure that you're using the same CUDNN algorithm each time.
        torch.backends.cudnn.deterministic = True

    # NumPy
    np.random.seed(seed)
