#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Exports Processor classes to the execution script.
"""

from typing import List

from mafw import mafw_hookimpl
from mafw.lazy_import import (
    LazyImportProcessor,
    LazyImportUserInterface,
    ProcessorClassProtocol,
    UserInterfaceClassProtocol,
)


@mafw_hookimpl
def register_processors() -> List[ProcessorClassProtocol]:
    """Returns a list of processors to be registered"""
    return [
        LazyImportProcessor('mafw.examples.sum_processor', 'AccumulatorProcessor'),
        LazyImportProcessor('mafw.examples.sum_processor', 'GaussAdder'),
        LazyImportProcessor('mafw.examples.loop_modifier', 'ModifyLoopProcessor'),
        LazyImportProcessor('mafw.examples.db_processors', 'CountStandardTables'),
        LazyImportProcessor('mafw.examples.db_processors', 'FillFileTableProcessor'),
        LazyImportProcessor('mafw.examples.loop_modifier', 'FindNPrimeNumber'),
        LazyImportProcessor('mafw.examples.loop_modifier', 'FindPrimeNumberInRange'),
        LazyImportProcessor('mafw.examples.importer_example', 'ImporterExample'),
        LazyImportProcessor('mafw.processor_library.db_init', 'TableCreator'),
        LazyImportProcessor('mafw.processor_library.db_init', 'TriggerRefresher'),
        LazyImportProcessor('mafw.processor_library.db_init', 'SQLScriptRunner'),
    ]


@mafw_hookimpl
def register_user_interfaces() -> List[UserInterfaceClassProtocol]:
    """Returns a list of user interfaces that can be used"""
    return [
        LazyImportUserInterface('mafw.ui.rich_user_interface', 'RichInterface', 'rich'),
        LazyImportUserInterface('mafw.ui.console_user_interface', 'ConsoleInterface', 'console'),
    ]


@mafw_hookimpl
def register_db_model_modules() -> List[str]:
    """Returns the list of modules with the database model definitions"""
    return []
