#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
from copy import deepcopy
from typing import Any

"""
Generic utility functions for data manipulation.

This module provides helper functions for common data structure operations,
particularly focused on dictionary manipulation with support for deep updates
and recursive merging of nested structures.
"""


def deep_update(base_dict: dict[Any, Any], update_dict: dict[Any, Any], copy_first: bool = True) -> dict[Any, Any]:
    """
    Recursively updates a dictionary.

    If copy_first is set to False, then the base_dict is actually updated.

    :param base_dict: The dictionary to update.
    :type base_dict: dict[Any, Any]
    :param update_dict: The dictionary containing the updated fields
    :type update_dict: dict[Any, Any]
    :param copy_first: Whether the base dictionary should be copied or updated. Defaults to True
    :type copy_first: bool, Optional
    :return: The recursively updated dictionary
    :rtype: dict[Any, Any]
    """
    # 1. Handle Copying
    if copy_first:
        # Use deepcopy to ensure nested dictionaries are also new objects
        target_dict = deepcopy(base_dict)
    else:
        # Modify the original dictionary in place
        target_dict = base_dict

    # 2. Perform Recursive Update
    for key, value in update_dict.items():
        if isinstance(value, dict) and key in target_dict and isinstance(target_dict[key], dict):
            # If both values are dictionaries, recurse on the target_dict's value
            # Note: We pass copy_first=False here because we are modifying
            # the already-copied/selected target_dict, we don't need another copy.
            deep_update(target_dict[key], value, copy_first=False)
        else:
            # Otherwise, update or insert the new value
            target_dict[key] = value

    return target_dict
