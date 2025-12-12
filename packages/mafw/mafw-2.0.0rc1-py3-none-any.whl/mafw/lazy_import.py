#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
This module provides classes for lazy importing of plugins, ensuring thread-safe access and transparent usage.

Classes:
    - LazyImportPlugin: A generic class for lazy importing of plugin classes.
    - LazyImportProcessor: A specialised class for lazy importing of Processor plugins.
    - LazyImportUserInterface: A specialised class for lazy importing of UserInterface plugins.

Protocols:
    - ProcessorClassProtocol: Defines the expected interface for Processor classes.
    - UserInterfaceClassProtocol: Defines the expected interface for UserInterface classes.

.. versionadded:: v2.0.0
"""

import importlib
import threading
from abc import ABC, abstractmethod
from typing import Any, Generic, Protocol, Type, TypeVar, cast, runtime_checkable

from mafw.processor import Processor
from mafw.ui.abstract_user_interface import UserInterfaceBase


@runtime_checkable
class ProcessorClassProtocol(Protocol):
    """
    Protocol for Processor classes.

    .. versionadded:: v2.0.0

    :cvar plugin_name: The name of the plugin.
    :cvar plugin_qualname: The qualified name of the plugin.
    :cvar __name__: The name of the class.
    """

    plugin_name: str
    plugin_qualname: str
    __name__: str

    def __call__(self, *args: Any, **kwargs: Any) -> Processor:
        """
        Instantiate the Processor class.

        :param args: Positional arguments for the Processor constructor.
        :param kwargs: Keyword arguments for the Processor constructor.
        :return: An instance of Processor.
        :rtype: Processor
        """
        ...  # pragma: no cov


@runtime_checkable
class UserInterfaceClassProtocol(Protocol):
    """
    Protocol for UserInterface classes.

    .. versionadded:: v2.0.0

    :cvar plugin_name: The name of the plugin.
    :cvar plugin_qualname: The qualified name of the plugin.
    :cvar name: The name of the user interface.
    """

    plugin_name: str
    plugin_qualname: str
    name: str

    def __call__(self, *args: Any, **kwargs: Any) -> UserInterfaceBase:
        """
        Instantiate the UserInterfaceBase class.

        :param args: Positional arguments for the UserInterfaceBase constructor.
        :param kwargs: Keyword arguments for the UserInterfaceBase constructor.
        :return: An instance of UserInterfaceBase.
        :rtype: UserInterfaceBase
        """
        ...  # pragma: no cov


T = TypeVar('T')  # Class type (e.g., Processor class)
"""The class type to be used for the generic lazy import plugin."""
R = TypeVar('R')  # Instance type (e.g., Processor instance)
"""The instance type to be used for the generic lazy import plugin."""


class LazyImportPlugin(Generic[T, R], ABC):
    """
    Proxy object that lazily imports a plugin class only when accessed.
    Thread-safe and transparent to the user.

    .. versionadded:: v2.0.0
    """

    def __init__(self, module: str, class_name: str) -> None:
        """
        Constructor parameter:

        :param module: The module name where the class is located.
        :type module: str
        :param class_name: The name of the class to be lazily imported.
        :type class_name: str
        """
        self._module = module
        self._class_name = class_name
        self._cached: Type[T] | None = None
        self._lock = threading.Lock()

        self.plugin_name = class_name
        self.plugin_qualname = f'{module}.{class_name}'

    @abstractmethod
    def _post_load(self, cls: Type[T]) -> Type[T]:
        """
        Perform operations after loading the class.

        :param cls: The class type that has been loaded.
        :type cls: Type[T]
        :return: The class type after post-load operations.
        :rtype: Type[T]
        """
        return cls  # pragma: no cov

    def _load(self) -> Type[T]:
        """
        Load the class from the specified module.

        :return: The loaded class type.
        :rtype: Type[T]
        """
        if self._cached is None:
            with self._lock:
                module = importlib.import_module(self._module)
                cls = getattr(module, self._class_name)
                self._cached = self._post_load(cls)
        return self._cached

    # Allow calling class attributes transparently
    def __getattr__(self, item: str) -> Any:
        """
        Access attributes of the lazily loaded class.

        :param item: The attribute name to access.
        :type item: str
        :return: The attribute value.
        :rtype: Any
        """
        return getattr(self._load(), item)

    # Allow instantiation: LazyPlugin() behaves like ActualClass()
    def __call__(self, *args: Any, **kwargs: Any) -> R:
        """
        Instantiate the lazily loaded class.

        :param args: Positional arguments for the class constructor.
        :param kwargs: Keyword arguments for the class constructor.
        :return: An instance of the class.
        :rtype: R
        """
        cls = self._load()
        return cast(R, cls(*args, **kwargs))

    def __repr__(self) -> str:
        """
        Return a string representation of the LazyImportPlugin.

        :return: The string representation.
        :rtype: str
        """
        return f'LazyImportPlugin("{self._module}", "{self._class_name}")'  # pragma: no cov


class LazyImportProcessor(LazyImportPlugin[Processor, Processor]):
    """
    Lazy import proxy for Processor classes.

    .. versionadded:: v2.0.0
    """

    def _post_load(self, cls: Type[Processor]) -> Type[Processor]:
        """
        Perform operations after loading the Processor class.

        :param cls: The Processor class type that has been loaded.
        :type cls: Type[Processor]
        :return: The Processor class type after post-load operations.
        :rtype: Type[Processor]
        """
        return cls

    def __repr__(self) -> str:
        """
        Return a string representation of the LazyImportProcessor.

        :return: The string representation.
        :rtype: str
        """
        return f'LazyImportProcessor("{self._module}", "{self._class_name}")'


class LazyImportUserInterface(LazyImportPlugin[UserInterfaceBase, UserInterfaceBase]):
    """
    Lazy import proxy for UserInterface classes.

    .. versionadded:: v2.0.0
    """

    def __init__(self, module: str, class_name: str, ui_name: str) -> None:
        """
        Constructor parameter:

        :param module: The module name where the class is located.
        :type module: str
        :param class_name: The name of the class to be lazily imported.
        :type class_name: str
        :param ui_name: The expected name of the user interface.
        :type ui_name: str
        """
        super().__init__(module, class_name)
        self.name = ui_name

    def _post_load(self, cls: Type[UserInterfaceBase]) -> Type[UserInterfaceBase]:
        """
        Perform operations after loading the UserInterface class.

        :param cls: The UserInterface class type that has been loaded.
        :type cls: Type[UserInterfaceBase]
        :return: The UserInterface class type after post-load operations.
        :rtype: Type[UserInterfaceBase]
        :raises ValueError: If the class name is inconsistent with the expected name.
        """
        if getattr(cls, 'name', None) != self.name:
            raise ValueError(f'UserInterface class {cls} has inconsistent .name: expected {self.name}')
        return cls

    def __repr__(self) -> str:
        """
        Return a string representation of the LazyImportUserInterface.

        :return: The string representation.
        :rtype: str
        """
        return f'LazyImportUserInterface("{self._module}", "{self._class_name}", "{self.name}")'
