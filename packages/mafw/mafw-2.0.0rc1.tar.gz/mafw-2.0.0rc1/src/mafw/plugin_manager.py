#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Plugin management system for MAFw framework.

This module provides the core functionality for loading and managing plugins within the MAFw framework.
It supports loading various types of plugins including processors, standard tables, database models, and
user interfaces.

The plugin manager uses the pluggy library to handle plugin discovery and registration
through entry points and hooks.

When plugins are loaded using the :meth:`.MAFwPluginManager.load_plugins` function, the job is divided into multiple
threads to improve performance.

Key features:
    - Asynchronous plugin loading with progress indication
    - Support for both internal and external plugins
    - Type-safe plugin handling with proper data structures
    - Logging integration for monitoring plugin loading processes
    - Global plugin manager singleton for consistent access

The module defines several key components:
    - :class:`.LoadedPlugins`: Data container for loaded plugins
    - :class:`.MAFwPluginManager`: Main plugin manager class
    - :func:`.get_plugin_manager`: Factory function for accessing the plugin manager

Plugin types supported:
    - Processors (`processors`): Classes that implement data processing logic
    - Database Modules (`db_modules`): Model modules for database interaction
    - User Interfaces (`ui`): UI implementations for different interfaces

.. versionchanged:: v2.0.0
    Complete refactoring of the plugin manager system.

"""

import importlib
import itertools
import logging
import time
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Literal, Tuple, cast

import pluggy

from mafw import hookspecs, plugins
from mafw.lazy_import import ProcessorClassProtocol, UserInterfaceClassProtocol

if TYPE_CHECKING:
    pass

log = logging.getLogger(__name__)


@dataclass
class LoadedPlugins:
    """
    Container class for storing loaded plugins of various types.

    This dataclass holds collections of different plugin types that have been loaded
    by the :class:`MAFwPluginManager`. It provides organized storage for processors,
    database modules, and user interfaces.

    .. versionadded:: v2.0.0
    """

    processor_list: List[ProcessorClassProtocol] = field(default_factory=list)
    # List[Type['Processor'] | 'LazyPlugin'] = field(default_factory=list)
    """List of loaded processor classes."""

    processor_dict: Dict[str, ProcessorClassProtocol] = field(default_factory=dict)
    # Dict[str, Type['Processor'] | 'LazyPlugin'] = field(default_factory=dict)
    """Dictionary mapping processor names to their classes."""

    db_model_modules: List[str] = field(default_factory=list)
    """List of database model module names."""

    ui_list: List[UserInterfaceClassProtocol] = field(default_factory=list)
    # List[Type['UserInterfaceBase'] | 'LazyPlugin'] = field(default_factory=list)
    """List of loaded user interface classes."""

    ui_dict: Dict[str, UserInterfaceClassProtocol] = field(default_factory=dict)
    # Dict[str, Type['UserInterfaceBase'] | 'LazyPlugin'] = field(default_factory=dict)
    """Dictionary mapping user interface names to their classes."""


PluginTypes = Literal['processors', 'db_modules', 'ui']
"""Type alias for accepted types of plugins."""


def _as_processor_result(obj: object) -> tuple[list[ProcessorClassProtocol], dict[str, ProcessorClassProtocol]]:
    """
    Cast an object to the expected processor result type.

    This helper function is used to convert the raw result from plugin loading
    operations into the expected tuple format for processors.

    .. versionadded:: v2.0.0

    :param obj: The object to cast
    :type obj: object
    :return: A tuple containing a list of processor classes and a dictionary mapping
             processor names to their classes
    :rtype: tuple[list[ProcessorClassProtocol], dict[str, ProcessorClassProtocol]]
    """
    return cast(tuple[list[ProcessorClassProtocol], dict[str, ProcessorClassProtocol]], obj)


def _as_ui_result(obj: object) -> tuple[list[UserInterfaceClassProtocol], dict[str, UserInterfaceClassProtocol]]:
    """
    Cast an object to the expected UI result type.

    This helper function is used to convert the raw result from plugin loading
    operations into the expected tuple format for user interfaces.

    .. versionadded:: v2.0.0

    :param obj: The object to cast
    :type obj: object
    :return: A tuple containing a list of UI classes and a dictionary mapping
             UI names to their classes
    :rtype: tuple[list[UserInterfaceClassProtocol], dict[str, UserInterfaceClassProtocol]]
    """
    return cast(tuple[list[UserInterfaceClassProtocol], dict[str, UserInterfaceClassProtocol]], obj)


def _as_db_module_result(obj: object) -> list[str]:
    """
    Cast an object to the expected database module result type.

    This helper function is used to convert the raw result from plugin loading
    operations into the expected list format for database modules.

    .. versionadded:: v2.0.0

    :param obj: The object to cast
    :type obj: object
    :return: A list of database module names
    :rtype: list[str]
    """
    return cast(list[str], obj)


class MAFwPluginManager(pluggy.PluginManager):
    """
    The MAFw plugin manager.

    The MAFwPluginManager class manages the loading and registration of plugins within the MAFw framework.
    It supports asynchronous loading of various plugin types, including processors, database modules,
    and user interfaces, using a thread pool executor for improved performance.

    The class provides methods to load each type of plugin and handles delayed status messages if loading takes
    longer than expected.

    .. versionadded:: v2.0.0
    """

    max_loading_delay = 1  # sec
    """
    Loading delay before displaying a message.

    If the loading of the external plugins is taking more than this value, a message is displayed to inform the user.
    """

    def __init__(self, project_name: str = 'mafw'):
        super().__init__(project_name)
        self._executor = ThreadPoolExecutor(max_workers=4)

    def load_db_models_plugins(self) -> list[str]:
        """
        Load database model modules from the plugin manager.

        This method retrieves all database model modules registered through the plugin manager's
        :meth:`~mafw.plugins.register_db_model_modules` hook and imports them.

        :returns: List of database model module names
        :rtype: list[str]
        """
        log.debug('Starting database model plugins...')
        db_model_module_list = list(itertools.chain(*self.hook.register_db_model_modules()))
        for module in db_model_module_list:
            importlib.import_module(module)
        log.debug('Finished database model plugins')
        return db_model_module_list

    def load_processor_plugins(self) -> Tuple[List[ProcessorClassProtocol], Dict[str, ProcessorClassProtocol]]:
        """
        Load available processor plugins from the plugin manager.

        This method retrieves all processor plugins registered through the plugin manager's
        :meth:`~mafw.plugins.register_processors` hook.
        :meth:`~mafw.plugins.register_processors` hook.

        :returns: A tuple containing:
            - List of available processor classes
            - Dictionary mapping processor names to their classes
        :rtype: tuple[list[type[Processor]], dict[str, type[Processor]]]
        """
        log.debug('Starting processor plugins...')
        lst = list(itertools.chain(*self.hook.register_processors()))
        dct = {}
        for p in lst:
            if hasattr(p, 'plugin_name'):  # LazyPlugin case
                key = p.plugin_name
            else:
                key = p.__name__
            dct[key] = p
        log.debug('Finished processor plugins')
        return lst, dct

    def load_user_interface_plugins(
        self,
    ) -> Tuple[List[UserInterfaceClassProtocol], Dict[str, UserInterfaceClassProtocol]]:
        """
        Load available user interface plugins from the plugin manager.

        This method retrieves all user interface plugins registered through the plugin manager's
        :meth:`~mafw.plugins.register_user_interfaces` hook.

        :returns: A tuple containing:
            - List of available user interface classes
            - Dictionary mapping user interface names to their classes
        :rtype: tuple[list[type[UserInterfaceBase]], dict[str, type[UserInterfaceBase]]]
        """
        log.debug('Start loading user interface plugins...')
        lst = list(itertools.chain(*self.hook.register_user_interfaces()))
        dct = {ui.name: ui for ui in lst}
        log.debug('Finished loading user interface plugins')
        return lst, dct

    def _delayed_status_message(self, futures: List[Future[Any]]) -> None:
        """
        Display a warning message if plugin loading takes longer than expected.

        This method is called after a delay to check if all plugin loading operations
        have completed. If not, it logs a warning message to inform the user that
        plugin loading is taking longer than expected.

        :param futures: List of futures representing ongoing plugin loading operations
        :type futures: list[concurrent.futures.Future]
        """
        time.sleep(self.max_loading_delay)
        if not all(f.done() for f in futures):
            log.warning('Plugin loading is taking longer than expected, please be patient.')

    def load_plugins(self, plugins_to_load: Iterable[PluginTypes]) -> LoadedPlugins:
        """
        Load plugins of specified types in multiple threads.

        This method loads plugins of the specified types using a thread pool executor
        for improved performance. It handles different plugin types including processors,
        standard tables, database modules, and user interfaces.

        :param plugins_to_load: Iterable of plugin types to load
        :type plugins_to_load: Iterable[:obj:`PluginTypes`]
        :return: Container with loaded plugins of all requested types
        :rtype: :obj:`LoadedPlugins`
        """
        plugins_to_load = list(dict.fromkeys(plugins_to_load))
        if not plugins_to_load:
            return LoadedPlugins()

        lut = {
            'processors': self.load_processor_plugins,
            'db_modules': self.load_db_models_plugins,
            'ui': self.load_user_interface_plugins,
        }

        # drop invalid plugin types
        plugins_to_load = [p for p in plugins_to_load if p in lut]
        if not plugins_to_load:
            return LoadedPlugins()

        log.debug(f'Status message will appear if loading takes > {self.max_loading_delay}s')

        # Submit tasks to the executor
        futures: list[Future[Any]] = []
        for plugin_type in plugins_to_load:
            fut = self._executor.submit(lut[plugin_type])
            futures.append(fut)

        # Start delayed status thread
        status_thread = self._executor.submit(self._delayed_status_message, futures)

        # Wait for completion
        results = []
        try:
            for fut in futures:
                results.append(fut.result())  # will re-raise exceptions
        finally:
            # When all tasks finished, no need for the warning message
            if not status_thread.done():
                status_thread.cancel()

        # Assemble output
        plugins_ = LoadedPlugins()
        idx = 0

        for plugin_type in plugins_to_load:
            result = results[idx]

            if plugin_type == 'processors':
                plugins_.processor_list, plugins_.processor_dict = _as_processor_result(result)

            elif plugin_type == 'ui':
                plugins_.ui_list, plugins_.ui_dict = _as_ui_result(result)

            else:  # if plugin_type == 'db_modules':
                plugins_.db_model_modules = _as_db_module_result(result)

            idx += 1

        return plugins_


global_mafw_plugin_manager: dict[str, 'MAFwPluginManager'] = {}
"""The global mafw plugin manager dictionary."""


def get_plugin_manager(force_recreate: bool = False) -> 'MAFwPluginManager':
    """
    Create a new or return an existing plugin manager for a given project

    :param force_recreate: Flag to force the creation of a new plugin manager. Defaults to False
    :type force_recreate: bool, Optional
    :return: The plugin manager
    :rtype: pluggy.PluginManager
    """
    if 'mafw' in global_mafw_plugin_manager and force_recreate:
        del global_mafw_plugin_manager['mafw']

    if 'mafw' not in global_mafw_plugin_manager:
        pm = MAFwPluginManager('mafw')
        pm.add_hookspecs(hookspecs)
        pm.load_setuptools_entrypoints('mafw')
        pm.register(plugins)
        global_mafw_plugin_manager['mafw'] = pm

    return global_mafw_plugin_manager['mafw']
