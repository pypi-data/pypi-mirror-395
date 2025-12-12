#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2024 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#
import torch
import hashlib


def hash_model_by_parameters(model: torch.nn.Module, hash_type: str = "sha256") -> str:
    """
    Compute a hash representation of a PyTorch model based solely on its parameters.

    This function generates a hash in a memory-efficient manner, loading parameters
    incrementally to avoid loading the entire model into memory if it is too large.

    Args:
        model (torch.nn.Module): The PyTorch model to hash. Only the model's parameters
            (weights and biases) are used for hashing.
        hash_type (str, optional): The type of hashing algorithm to use. Defaults to "sha256".
            Other common options include "md5", "sha1", "sha512", etc.

    Returns:
        str: The computed hash as a hexadecimal string. This hash uniquely represents the model's
        parameters and will change if any of the parameter values change.

    Example:
        >>> model = torch.nn.Linear(10, 5)  # Define your model
        >>> model_hash = hash_model_by_parameters(model)
        >>> print("Model Hash:", model_hash)

    Notes:
        - The model's structure is not included in the hash. Only the parameter values 
          from `state_dict()` are considered. This is because the model's structure is difficult
          to hash in a way that is both unique and invariant to minor changes in how the layers
          are defined and implemented. We get some of the benefits of hashing the model structure
          by hashing the parameters, as the parameters are dependent on the model's structure.
        - The hashing algorithm can be changed by passing a different value to `hash_type`, 
          such as "md5" or "sha512".
    """
    hash_obj = hashlib.new(hash_type)

    # Incrementally hash the parameters from the state_dict
    for param_name, param_tensor in model.state_dict().items():
        # Hash the parameter name
        hash_obj.update(param_name.encode('utf-8'))

        # Hash the parameter tensor values, ensuring a consistent byte order
        hash_obj.update(param_tensor.numpy().tobytes(order='C'))

    return hash_obj.hexdigest()


if __name__ == "__main__":
    from torch import nn

    my_model1 = nn.Linear(10, 10)
    my_model2 = nn.Linear(10, 10)

    my_model_3 = nn.Linear(10, 10)
    my_model_3.load_state_dict(my_model1.state_dict())

    hash1 = hash_model_by_parameters(my_model1)
    hash2 = hash_model_by_parameters(my_model2)
    hash3 = hash_model_by_parameters(my_model_3)

    assert hash1 != hash2
    assert hash3 != hash2
    assert hash1 == hash3