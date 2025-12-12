#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2024 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#
import sys
import torch

if torch.cuda.is_available():
    device = torch.device("cuda")   
#elif torch.backends.mps.is_available():        # Still stuff to debug on the Mac.
#    device = torch.device("mps")
else:
    device = torch.device("cpu")


def get_current_device():
    return device.type if device is not None else "<NONE>"

def set_device_cpu():
    global device
    device = torch.device("cpu")

def set_device_gpu():
    global device
    if torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        raise RuntimeError("CUDA is not available. Cannot set device to GPU.")

def reset_device():
    if torch.cuda.is_available():
        device = torch.device("cuda")   
    #elif torch.backends.mps.is_available():        # Still stuff to debug on the Mac.
    #    device = torch.device("mps")
    else:
        device = torch.device("cpu")

