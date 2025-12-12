"""
The console user interface.

The module provides a simple, still efficient user interface ideal for code execution of a headless system where it is
not possible to observe the output in real-time.
Nevertheless, important messages are logged via the logging library and thus it is also possible to save them to a file,
if a proper logging handler is set up.
"""

#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
from __future__ import annotations

import logging
from types import TracebackType
from typing import Any, Self

from mafw.enumerators import ProcessorStatus
from mafw.ui.abstract_user_interface import UserInterfaceBase

log = logging.getLogger(__name__)


class ConsoleInterface(UserInterfaceBase):
    """
    A console user interface.

    Ideal for execution in a headless environment.

    Messages are sent via the logging system, so they can also be saved to a file is a logging handler is properly set
    up in the execution framework.
    """

    name = 'console'

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
        self,
        task_name: str,
        completed: int | None = None,
        increment: int | None = None,
        total: int | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Update an existing task.

        :param task_name: A unique identifier for the task. You cannot have more than one task with the same name in
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
        Display a progress message with item counter.

        This method displays progress information at specified intervals based on the frequency parameter.
        It formats the message with a counter showing the current item and total items.

        :param message: The progress message to display.
        :type message: str
        :param i_item: The current item number (0-based index).
        :type i_item: int
        :param n_item: The total number of items, or None if unknown.
        :type n_item: int | None
        :param frequency: The frequency at which messages should be displayed (in seconds).
        :type frequency: float
        """
        if self._is_time_to_display_lopping_message(i_item, n_item, frequency):
            if n_item is None:
                n_item = max(1000, i_item)
            width = len(str(n_item))
            counter = f'[{i_item + 1:>{width}}/{n_item}] '
            msg = counter + message
            log.info(msg)

    def change_of_processor_status(
        self, processor_name: str, old_status: ProcessorStatus, new_status: ProcessorStatus
    ) -> None:
        """
        Log a processor status change.

        This method logs when a processor changes its status, using debug level logging.

        :param processor_name: The name of the processor whose status changed.
        :type processor_name: str
        :param old_status: The previous status of the processor.
        :type old_status: ProcessorStatus
        :param new_status: The new status of the processor.
        :type new_status: ProcessorStatus
        """
        msg = f'{processor_name} is {new_status}'
        log.debug(msg)

    def prompt_question(self, question: str, **kwargs: Any) -> Any:
        """
        Prompt the user with a question and return their input.

        This method displays a question to the user and waits for their input.
        Additional keyword arguments can be passed through to the underlying input function.

        .. versionadded:: v2.0.0

        :param question: The question to display to the user.
        :type question: str
        :param kwargs: Additional keyword arguments to pass to the input function.
        :return: The user's input.
        :rtype: Any
        """
        return input(question)
