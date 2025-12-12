"""
An abstract generic user interface.

The module provides a generic user interface that can be implemented to allow MAFw to communicate with different
user interfaces.

MAFw is designed to operate seamlessly without a user interface; however, users often appreciate the added benefit of communication between the process execution and themselves.

There are several different interfaces and different interface types (Command Line, Textual, Graphical...) and
everyone has its own preferences. In order to be as generic as possible, MAFw is allowing for an abstract
interface layer so that the user can either decide to use one of the few coming with MAFw or to implement the
interface to their favorite interface.
"""

#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
from __future__ import annotations

from contextlib import contextmanager
from types import TracebackType
from typing import Any, Generator, Self

from mafw.enumerators import ProcessorStatus


class UserInterfaceMeta(type):
    """
    A metaclass used for the creation of user interface
    """

    __required_members__ = (
        'create_task',
        'update_task',
        'display_progress_message',
        'change_of_processor_status',
        'prompt_question',
        'enter_interactive_mode',
    )
    __required_callable__ = (
        'create_task',
        'update_task',
        'display_progress_message',
        'change_of_processor_status',
        'prompt_question',
        'enter_interactive_mode',
    )

    def __instancecheck__(cls, instance: Any) -> bool:
        return cls.__subclasscheck__(type(instance))

    def __subclasscheck__(cls, subclass: Any) -> bool:
        members = all([hasattr(subclass, m) for m in cls.__required_members__])
        if not members:
            return False
        callables = all([callable(getattr(subclass, c)) for c in cls.__required_callable__])
        return callables


class UserInterfaceBase(metaclass=UserInterfaceMeta):
    """
    An abstract base user interface class that defines the interface for communicating with different user interfaces.

    This class provides a standardized way for MAFw to interact with various user interfaces including command-line,
    textual, and graphical interfaces. It defines the required methods that any concrete implementation must provide.

    The interface allows for task management, progress reporting, status updates, and user interaction capabilities.

    .. versionadded:: v1.0
    """

    always_display_progress_message = 10
    """
    Threshold for displaying progress messages.
    
    If the total number of events is below this value, then the progress message is always displayed, otherwise 
    follow the standard update frequency.
    """
    name = 'base'
    """The name of the interface"""

    def create_task(
        self,
        task_name: str,
        task_description: str = '',
        completed: int = 0,
        increment: int | None = None,
        total: int | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Create a new task.

        :param task_name: A unique identifier for the task. You cannot have more than 1 task with the same name in
            the whole execution. If you want to use the processor name, it is recommended to use the
            :attr:`~mafw.processor.Processor.unique_name`.
        :type task_name: str
        :param task_description: A short description for the task. Defaults to None.
        :type task_description: str, Optional
        :param completed: The amount of task already completed. Defaults to None.
        :type completed: int, Optional
        :param increment: How much of the task has been done since last update. Defaults to None.
        :type increment: int, Optional
        :param total: The total amount of task. Defaults to None.
        :type total: int, Optional
        """
        pass

    def update_task(
        self, task_name: str, completed: int = 0, increment: int | None = None, total: int | None = None, **kwargs: Any
    ) -> None:
        """
        Update an existing task.

        :param task_name: A unique identifier for the task. You cannot have more than 1 task with the same name in
            the whole execution. If you want to use the processor name, it is recommended to use the
            :attr:`~mafw.processor.Processor.unique_name`.
        :type task_name: str
        :param completed: The amount of task already completed. Defaults to None.
        :type completed: int, Optional
        :param increment: How much of the task has been done since last update. Defaults to None.
        :type increment: int, Optional
        :param total: The total amount of task. Defaults to None.
        :type total: int, Optional
        """
        pass

    def __enter__(self) -> Self:
        """Context enter dunder."""
        return self

    def __exit__(
        self, type_: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None
    ) -> None:
        """
        Context exit dunder.

        :param type_: Exception type.
        :param value: Exception value.
        :param traceback: Exception trace back.
        """
        pass

    def display_progress_message(self, message: str, i_item: int, n_item: int | None, frequency: float) -> None:
        """
        Display a message during the process execution.

        :param message: The message to be displayed.
        :type message: str
        :param i_item: The current item enumerator.
        :type i_item: int
        :param n_item: The total number of items or None for an indeterminate progress (while loop).
        :type n_item: int | None
        :param frequency: How often (in percentage of n_item) to display the message.
        :type frequency: float
        """
        pass

    def _is_time_to_display_lopping_message(self, i_item: int, n_item: int | None, frequency: float) -> bool:
        if n_item is None:
            # let's print the message everytime i_item is a multiple of 10.
            return i_item % 10 == 0

        if n_item > self.always_display_progress_message:
            always = False
        else:
            always = True
        if always:
            do_display = True
        else:
            mod = max([round(frequency * n_item), 1])
            do_display = i_item == 0 or i_item % mod == 0 or i_item == n_item - 1
        return do_display

    def change_of_processor_status(
        self, processor_name: str, old_status: ProcessorStatus, new_status: ProcessorStatus
    ) -> None:
        pass

    @contextmanager
    def enter_interactive_mode(self) -> Generator[None, Any, None]:
        """
        A context manager for entering interactive mode.

        This method provides a way to temporarily switch to interactive mode, allowing for direct user interaction
        during processing. It should be used as a context manager with a ``with`` statement.

        .. versionadded:: v2.0.0

        :returns: A context manager that yields control to the interactive section
        :rtype: Generator
        """
        try:
            yield
        finally:
            pass

    def prompt_question(self, question: str, **kwargs: Any) -> Any:
        """
        Prompt the user with a question and return their response.

        This method should display a question to the user and wait for their input. The implementation may vary
        depending on the specific user interface being used.

        .. versionadded:: v2.0.0

        :param question: The question to be asked to the user.
        :type question: str
        :param kwargs: Additional keyword arguments that might be used by specific implementations.
        :returns: The user's response to the question.
        :rtype: Any
        """
        pass  # pragma: no cover
