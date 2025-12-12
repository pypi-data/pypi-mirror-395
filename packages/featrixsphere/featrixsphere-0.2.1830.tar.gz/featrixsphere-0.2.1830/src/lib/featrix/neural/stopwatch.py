# #  -*- coding: utf-8 -*-
# #
# #  Copyright (c) 2024 Featrix, Inc, All Rights Reserved
# #
# #  Proprietary and Confidential.  Unauthorized use, copying or dissemination
# #  of these materials is strictly prohibited.
# #
# import time

# ============================================================================
# STUB CLASSES FOR BACKWARD COMPATIBILITY
# ============================================================================
# These stub classes exist solely to allow old training checkpoints to be
# loaded successfully. When PyTorch saves a checkpoint using torch.save(),
# it pickles the entire model state, including any StopWatch, Interval, or
# TimedIterator objects that were embedded in the model or training state.
#
# When loading old checkpoints, pickle needs these classes to exist in the
# module namespace to successfully unpickle the saved objects. Without these
# stubs, loading old checkpoints fails with:
#   "Can't get attribute 'StopWatch' on <module 'featrix.neural.stopwatch'>"
#
# These classes are intentionally minimal stubs - they don't implement the
# original functionality since StopWatch is no longer actively used in the
# codebase. They only need to be unpicklable, not functional.
# ============================================================================

class StopWatch:
    """Stub class for backward compatibility with old checkpoints."""
    def __init__(self, *args, **kwargs):
        # Accept any arguments to allow unpickling of old objects
        # Initialize default attributes if not already set (e.g., during unpickling)
        if not hasattr(self, 'event_timestamps'):
            self.event_timestamps = {}
        if not hasattr(self, 'intervals'):
            self.intervals = set()
        if not hasattr(self, 'state'):
            self.state = 'ready'
    
    def __getstate__(self):
        # Allow pickling
        return self.__dict__
    
    def __setstate__(self, state):
        # Allow unpickling - restore all attributes from the pickled state
        self.__dict__.update(state)
        # Ensure required attributes exist even if not in state
        if 'event_timestamps' not in self.__dict__:
            self.event_timestamps = {}
        if 'intervals' not in self.__dict__:
            self.intervals = set()
        if 'state' not in self.__dict__:
            self.state = 'ready'


class Interval:
    """Stub class for backward compatibility with old checkpoints."""
    def __init__(self, *args, **kwargs):
        # Accept any arguments to allow unpickling of old objects
        pass
    
    def __getstate__(self):
        return self.__dict__
    
    def __setstate__(self, state):
        self.__dict__.update(state)


class TimedIterator:
    """Stub class for backward compatibility with old checkpoints."""
    def __init__(self, *args, **kwargs):
        # Accept any arguments to allow unpickling of old objects
        pass
    
    def __getstate__(self):
        return self.__dict__
    
    def __setstate__(self, state):
        self.__dict__.update(state)

