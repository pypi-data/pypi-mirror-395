#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
This is the module that will be exposed via the entry point declaration.

Make sure to have all processors that you need to export in the list.
"""

import mafw
from mafw.lazy_import import LazyImportProcessor, ProcessorClassProtocol


@mafw.mafw_hookimpl
def register_processors() -> list[ProcessorClassProtocol]:
    return [
        LazyImportProcessor('plug.plug_processor', 'GenerateDataFiles'),
        LazyImportProcessor('plug.plug_processor', 'PlugImporter'),
        LazyImportProcessor('plug.plug_processor', 'Analyser'),
        LazyImportProcessor('plug.plug_processor', 'PlugPlotter'),
    ]


@mafw.mafw_hookimpl
def register_db_model_modules() -> list[str]:
    return ['plug.db_model']
