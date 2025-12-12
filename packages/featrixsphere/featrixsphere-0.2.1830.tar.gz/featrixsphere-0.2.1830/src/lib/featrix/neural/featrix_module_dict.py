#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2024 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

import torch.nn as nn


class FeatrixModuleDict(nn.ModuleDict):
    """
    A subclass of torch.nn.ModuleDict that provides a solution for using reserved words
    as keys in the dictionary by prefixing them with a specified string.

    This class addresses the issue where certain common words, like 'type', might be
    used as keys in the dictionary but are also reserved by PyTorch or pose conflicts
    within the framework. By automatically prefixing all keys, it allows for the safe
    inclusion of such terms without manual key management or risk of collisions.

    Certain other strings also cannot be used as keys in the ModuleDict, such as those that
    contain the full stop character, i.e. `.` To fix that, we replace any period in the key
    with the string "$FEATRIX$".

    Parameters:
        modules (iterable, optional): An iterable of key/module pairs to initialize the dictionary.
        prefix (str, optional): The prefix string to be prepended to each key to avoid collisions.
            Defaults to 'prefix_'.

    Example usage:
        >>> prefixed_dict = PrefixedModuleDict()
        >>> module = nn.Linear(10, 5)
        >>> prefixed_dict["linear"] = module  # Adds with key "custom_linear"
        >>> print(prefixed_dict["linear"])    # Retrieves using key "custom_linear"

    This implementation ensures that the dictionary can seamlessly include keys that might
    otherwise be problematic due to naming conflicts or reserved words in the PyTorch ecosystem.
    """

    def __init__(self, modules: dict = None):
        super().__init__()

        self.prefix = "featrix_"

        if modules is not None:
            for key, value in modules.items():
                self[key] = value

    def _add_prefix(self, key):
        # Add prefix to the key
        return f"{self.prefix}{key}"

    def _replace_periods(self, key):
        return key.replace(".", "$FEATRIX$")

    def _sanitize_key(self, key):
        key = self._replace_periods(key)
        # CRITICAL FIX: Don't double-prefix if key already starts with prefix
        if not key.startswith(self.prefix):
            key = self._add_prefix(key)
        return key

    def __setitem__(self, key, module):
        # Set item with prefixed key
        super().__setitem__(self._sanitize_key(key), module)

    def __getitem__(self, key):
        # Get item by prefixed key
        return super().__getitem__(self._sanitize_key(key))

    def __delitem__(self, key):
        # Delete item by prefixed key
        super().__delitem__(self._sanitize_key(key))

    def __contains__(self, key):
        # Check containment by prefixed key
        return super().__contains__(self._sanitize_key(key))
