#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
The Modular Analysis Framework

A software tool for scientists written by scientists!

"""

import pluggy

from mafw.__about__ import __version__ as __version__

mafw_hookimpl = pluggy.HookimplMarker('mafw')
"""Marker to be imported and used in plugins loading"""
