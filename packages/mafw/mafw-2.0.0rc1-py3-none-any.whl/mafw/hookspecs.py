#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Defines the hook specification decorator bound the MAFw library.
"""

from typing import TYPE_CHECKING, List

import pluggy

if TYPE_CHECKING:
    from mafw.lazy_import import ProcessorClassProtocol, UserInterfaceClassProtocol

mafw_hookspec = pluggy.HookspecMarker('mafw')


@mafw_hookspec
def register_processors() -> List['ProcessorClassProtocol']:
    """Register multiple processor classes"""
    return []  # pragma: no cover


@mafw_hookspec
def register_user_interfaces() -> List['UserInterfaceClassProtocol']:
    """Register multiple user interfaces"""
    return []  # pragma: no cover


@mafw_hookspec
def register_db_model_modules() -> list[str]:
    """Register database model modules"""
    return []  # pragma: no cover
