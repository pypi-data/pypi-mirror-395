#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
The module provides some general decorator utilities that are used in several parts of the code, and that can be
reused by the user community.
"""

import functools
import typing
import warnings
from importlib.util import find_spec
from typing import Any, Callable, Type

from mafw.enumerators import LoopType
from mafw.mafw_errors import MissingDatabase, MissingOptionalDependency
from mafw.processor import Processor

F = typing.TypeVar('F', bound=typing.Callable[..., object])
"""TypeVar for generic function."""

# Define a TypeVar to capture Processor subclasses
P = typing.TypeVar('P', bound=Processor)
"""TypeVar for generic processor."""


def suppress_warnings(func: F) -> F:
    """
    Decorator to suppress warnings during the execution of a test function.

    This decorator uses the `warnings.catch_warnings()` context manager to
    temporarily change the warning filter to ignore all warnings. It is useful
    when you want to run a test without having warnings clutter the output.

    Usage::

        @suppress_warnings
        def test_function():
            # Your test code that might emit warnings


    :param func: The test function to be decorated.
    :type func: Callable
    :return: The wrapped function with suppressed warnings.
    :rtype: Callable
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> F:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            return func(*args, **kwargs)  # type: ignore[return-value]

    return wrapper  # type: ignore[return-value]


@typing.no_type_check  # no idea how to fix it
def singleton(cls):
    """Make a class a Singleton class (only one instance)"""

    @functools.wraps(cls)
    def wrapper_singleton(*args: Any, **kwargs: Any):
        if wrapper_singleton.instance is None:
            wrapper_singleton.instance = cls(*args, **kwargs)
        return wrapper_singleton.instance

    wrapper_singleton.instance = None
    return wrapper_singleton


@typing.no_type_check
def database_required(cls):
    """Modify the processor start method to check if a database object exists.

    This decorator must be applied to processors requiring a database connection.

    :param cls: A Processor class.
    """
    orig_start = cls.start

    @functools.wraps(cls.start)
    def _start(self) -> None:
        if self._database is None:
            raise MissingDatabase(f'{self.name} requires an active database.')
        orig_start(self)

    cls.start = _start

    return cls


@typing.no_type_check
def orphan_protector(cls):
    """
    A class decorator to modify the init method of a Processor so that the remove_orphan_files is set to False and
    no orphan files will be removed.
    """
    old_init = cls.__init__

    @functools.wraps(cls.__init__)
    def new_init(self, *args, **kwargs):
        old_init(self, *args, remove_orphan_files=False, **kwargs)

    cls.__init__ = new_init
    return cls


@typing.no_type_check
def execution_workflow(loop_type: LoopType | str = LoopType.ForLoop):
    """
    A decorator factory for the definition of the looping strategy.

    This decorator factory must be applied to Processor subclasses to modify their value of loop_type in order to
    change the execution workflow.

    See :func:`single_loop`, :func:`for_loop` and :func:`while_loop` decorator shortcuts.

    :param loop_type: The type of execution workflow requested for the decorated class. Defaults to LoopType.ForLoop.
    :type loop_type: LoopType | str, Optional
    """

    def dec(cls):
        """The class decorator."""
        old_init = cls.__init__

        @functools.wraps(cls.__init__)
        def new_init(self, *args, **kwargs):
            """The modified Processor init"""
            old_init(self, *args, looper=loop_type, **kwargs)

        cls.__init__ = new_init

        return cls

    return dec


single_loop = execution_workflow(LoopType.SingleLoop)
"""A decorator shortcut to define a single execution processor."""

for_loop = execution_workflow(LoopType.ForLoop)
"""A decorator shortcut to define a for loop execution processor."""

while_loop = execution_workflow(LoopType.WhileLoop)
"""A decorator shortcut to define a while loop execution processor."""


def depends_on_optional(
    module_name: str, raise_ex: bool = False, warn: bool = True
) -> Callable[[F], Callable[..., Any]]:
    """
    Function decorator to check if module_name is available.

    If module_name is found, then returns the wrapped function. If not, its behavior depends on the raise_ex and
    warn_only values. If raise_ex is True, then an ImportError exception is raised. If it is False and warn is
    True, then a warning message is displayed but no exception is raised. If they are both False, then function is
    silently skipped.

    If raise_ex is True, the value of `warn` is not taken into account.

    **Typical usage**

    The user should decorate functions or class methods when they cannot be executed without the optional library.
    In the specific case of Processor subclass, where the class itself can be created also without the missing
    library, but it is required somewhere in the processor execution, then the user is suggested to decorate the
    execute method with this decorator.

    :param module_name: The optional module(s) from which the function depends on. A ";" separated list of modules can
        also be provided.
    :type module_name: str
    :param raise_ex: Flag to raise an exception if module_name is not found, defaults to False.
    :type raise_ex: bool, Optional
    :param warn: Flag to display a warning message if module_name is not found, default to True.
    :type warn: bool, Optional
    :return: The wrapped function
    :rtype: Callable
    :raise ImportError: if module_name is not found and raise_ex is True.
    """

    def decorator(func: F) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            all_mods_found = all(find_spec(mod.strip()) is not None for mod in module_name.split(';'))
            if not all_mods_found:
                msg = f'Optional dependency {module_name} not found ({func.__qualname__})'
                if raise_ex:
                    raise ImportError(msg)
                else:
                    if warn:
                        warnings.warn(MissingOptionalDependency(msg), stacklevel=2)
                    return None  # Explicitly return None when skipping the function
            else:
                return func(*args, **kwargs)

        return wrapper

    return decorator


def processor_depends_on_optional(
    module_name: str, raise_ex: bool = False, warn: bool = True
) -> Callable[[Type[P]], Type[Processor]]:
    """
    Class decorator factory to check if module module_name is available.

    It checks if all the optional modules listed in `module_name` separated by a ';' can be found.

    If all modules are found, then the class is returned as it is.

    If at least one module is not found:
     - and raise_ex is True, an ImportError exception is raised and the user is responsible to deal with it.
     - if raise_ex is False, instead of returning the class, the :class:`~.Processor` is returned.
     - depending on the value of warn, the user will be informed with a warning message or not.

    **Typical usage**

    The user should decorate Processor subclasses everytime the optional module is required in their __init__ method.
    Should the check on the optional module have a positive outcome, then the Processor subclass is returned.
    Otherwise, if raise_ex is False, an instance of the base :py:class:`~.Processor` is returned. In
    this way, the returned class can still be executed without breaking the execution scheme but of course, without
    producing any output.

    Should be possible to run the __init__ method of the class without the missing library, then the user can also
    follow the approach described in this other :func:`example <depends_on_optional>`.

    :param module_name: The optional module(s) from which the class depends on. A ";" separated list of modules can
        also be provided.
    :type module_name: str
    :param raise_ex: Flag to raise an exception if module_name not found, defaults to False.
    :type raise_ex: bool, Optional
    :param warn: Flag to display a warning message if module_name is not found, defaults to True.
    :type warn: bool, Optional
    :return: The wrapped processor.
    :rtype: type(Processor)
    :raise ImportError: if module_name is not found and raise_ex is True.
    """

    def decorator(cls: Type[P]) -> Type[Processor]:
        """
        The class decorator.

        It checks if all the modules provided by the decorator factory are available on the systems.
        If yes, then it simply returns `cls`. If no, it returns a subclass of the :class:`~.Processor`
        after all the introspection properties have been taken from `cls`.

        :param cls: The class being decorated.
        :type cls: type(Processor)
        :return: The decorated class, either cls or a subclass of  :class:`~autorad.processor.Processor`.
        :rtype: type(Processor)
        """

        def class_wrapper(klass: Type[Processor]) -> Type[Processor]:
            """
            Copy introspection properties from cls to klass.

            :param klass: The class to be modified.
            :type klass: class.
            :return: The modified class.
            :rtype: class.
            """
            klass.__module__ = cls.__module__
            klass.__name__ = f'{cls.__name__} (Missing {module_name})'
            klass.__qualname__ = cls.__qualname__
            klass.__annotations__ = cls.__annotations__
            klass.__doc__ = cls.__doc__
            return klass

        all_mods_found = all([find_spec(mod.strip()) is not None for mod in module_name.split(';')])
        if not all_mods_found:
            msg = f'Optional dependency {module_name} not found ({cls.__qualname__})'
            if raise_ex:
                raise ImportError(msg)
            else:
                if warn:
                    warnings.warn(MissingOptionalDependency(msg), stacklevel=2)

                # We subclass the basic processor.
                class NewClass(Processor):
                    pass

                # The class wrapper is copying introspection properties from the cls to the NewClass
                new_class = class_wrapper(NewClass)

        else:
            new_class = cls
        return new_class

    return decorator


def class_depends_on_optional(
    module_name: str, raise_ex: bool = False, warn: bool = True
) -> Callable[[Type[Any]], Type[Any]]:
    """
    Class decorator factory to check if module module_name is available.

    It checks if all the optional modules listed in `module_name` separated by a ';' can be found.

    If all modules are found, then the class is returned as it is.

    If at least one module is not found:
     - and raise_ex is True, an ImportError exception is raised and the user is responsible to deal with it.
     - if raise_ex is False, instead of returning the class, a new empty class is returned.
     - depending on the value of warn, the user will be informed with a warning message or not.

    :param module_name: The optional module(s) from which the class depends on. A ";" separated list of modules can
        also be provided.
    :type module_name: str
    :param raise_ex: Flag to raise an exception if module_name not found, defaults to False.
    :type raise_ex: bool, Optional
    :param warn: Flag to display a warning message if module_name is not found, defaults to True.
    :type warn: bool, Optional
    :return: The wrapped class.
    :rtype: type(object)
    :raise ImportError: if module_name is not found and raise_ex is True.
    """

    def decorator(cls: Type[Any]) -> Type[Any]:
        """
        The class decorator.

        It checks if all the modules provided by the decorator factory are available on the systems.
        If yes, then it simply returns `cls`. If no, it returns a subclass of the cls bases.
        after all the introspection properties have been taken from `cls`.

        :param cls: The class being decorated.
        :type cls: type(cls)
        :return: The decorated class, either cls or a subclass of cls.
        :rtype: type(cls)
        """

        def class_wrapper(klass: Type[Any]) -> Type[Any]:
            """
            Copy introspection properties from cls to klass.

            :param klass: The class to be modified.
            :type klass: class.
            :return: The modified class.
            :rtype: class.
            """
            klass.__module__ = cls.__module__
            klass.__name__ = f'{cls.__name__} (Missing {module_name})'
            klass.__qualname__ = cls.__qualname__
            klass.__annotations__ = cls.__annotations__
            klass.__doc__ = cls.__doc__
            return klass

        all_mods_found = all([find_spec(mod.strip()) is not None for mod in module_name.split(';')])
        if not all_mods_found:
            msg = f'Optional dependency {module_name} not found ({cls.__qualname__})'
            if raise_ex:
                raise ImportError(msg)
            else:
                if warn:
                    warnings.warn(MissingOptionalDependency(msg), stacklevel=2)

                # we subclass the original class.
                class NewClass(*cls.__bases__):  # type: ignore
                    pass

                # the class wrapper is copying introspection properties from the cls to the NewClass
                new_class = class_wrapper(NewClass)

        else:
            new_class = cls
        return new_class

    return decorator
