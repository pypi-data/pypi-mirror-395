"""
The rich user interface.

The module provides an implementation of the abstract user interface that takes advantage from the `rich` library.
Progress bars and spinners are shown during the processor execution along with log messages including markup language.
In order for this logging message to appear properly rendered, the logger should be connected to a RichHandler.
"""

#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
import logging
from contextlib import contextmanager
from types import TracebackType
from typing import Any, Generator, Self

import rich.prompt
from rich.progress import Progress, SpinnerColumn, TaskID, TimeElapsedColumn

from mafw.enumerators import ProcessorStatus
from mafw.ui.abstract_user_interface import UserInterfaceBase

log = logging.getLogger(__name__)


class RichInterface(UserInterfaceBase):
    """
    Implementation of the interface for rich.

    :param progress_kws: A dictionary of keywords passed to the `rich.Progress`. Defaults to None
    :type progress_kws: dict, Optional
    """

    name = 'rich'

    def __init__(self, progress_kws: dict[str, Any] | None = None) -> None:
        if progress_kws is None:
            progress_kws = dict(auto_refresh=True, expand=True)

        self.progress = Progress(SpinnerColumn(), *Progress.get_default_columns(), TimeElapsedColumn(), **progress_kws)
        self.task_dict: dict[str, TaskID] = {}

    def __enter__(self) -> Self:
        """
        Context enter dunder.

        It manually starts the progress extension and then return the class instance.
        """
        self.progress.start()
        return self

    def __exit__(
        self, type_: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None
    ) -> None:
        """
        Context exit dunder.

        It manually stops the progress bar.

        :param type_: Exception type.
        :param value: Exception value.
        :param traceback: Exception trace back.
        """
        self.progress.stop()

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
        :param task_description: A short description for the task. Defaults to ''.
        :type task_description: str, Optional
        :param completed: The amount of task already completed. Defaults to 0.
        :type completed: int, Optional
        :param increment: How much of the task has been done since last update. Defaults to None.
        :type increment: int, Optional
        :param total: The total amount of task. Defaults to None.
        :type total: int, Optional
        """
        if task_name in self.task_dict:
            log.warning('A task with this name (%s) already exists. Replacing it with the new one.' % task_name)
            log.warning('Be sure to use unique names.')

        self.task_dict[task_name] = self.progress.add_task(
            task_description, total=total, completed=completed, increment=increment
        )

    def update_task(
        self, task_name: str, completed: int = 0, increment: int | None = None, total: int | None = None, **kwargs: Any
    ) -> None:
        """
        Update an existing task.

        :param task_name: A unique identifier for the task. You cannot have more than one task with the same name in
            the whole execution. If you want to use the processor name, it is recommended to use the
            :attr:`~~mafw.processor.Processor.unique_name`.
        :type task_name: str
        :param completed: The amount of task already completed. Defaults to 0.
        :type completed: int, Optional
        :param increment: How much of the task has been done since last update. Defaults to None.
        :type increment: int, Optional
        :param total: The total amount of task. Defaults to None.
        :type total: int, Optional
        """
        if task_name not in self.task_dict:
            log.warning('A task with this name (%s) does not exist.' % task_name)
            log.warning('Skipping updates')
            return

        self.progress.update(
            self.task_dict[task_name], completed=completed, advance=increment, total=total, visible=completed != total
        )

    def display_progress_message(self, message: str, i_item: int, n_item: int | None, frequency: float) -> None:
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
        Display a message when a processor status changes.

        This method logs a debug message indicating that a processor has changed its status.
        The message uses rich markup to highlight the processor name and new status.

        :param processor_name: The name of the processor whose status has changed.
        :type processor_name: str
        :param old_status: The previous status of the processor.
        :type old_status: ProcessorStatus
        :param new_status: The new status of the processor.
        :type new_status: ProcessorStatus
        """
        msg = f'[red]{processor_name}[/red] is [bold]{new_status}[/bold]'
        log.debug(msg)

    @contextmanager
    def enter_interactive_mode(self) -> Generator[None, Any, None]:
        """
        Context manager to temporarily switch to interactive mode.

        This method temporarily stops the progress display to allow for interactive input
        while preserving the original transient state. After yielding control, it restores
        the progress display with appropriate spacing to avoid overwriting previous output.

        .. versionadded:: v2.0.0

        .. note::
           This method should be used within a ``with`` statement to ensure proper cleanup.
        """
        transient = self.progress.live.transient  # save the old value
        self.progress.live.transient = True
        self.progress.stop()
        self.progress.live.transient = transient  # restore the old value
        try:
            yield
        finally:
            # make space for the progress to use so it doesn't overwrite any previous lines
            visible_tasks = [task for task in self.progress.tasks if task.visible]
            print('\n' * (len(visible_tasks) - 2))
            self.progress.start()

    def prompt_question(self, question: str, **kwargs: Any) -> Any:
        """
        Prompt the user with a question and return their response.

        This method uses the rich library's prompt functionality to ask the user a question.
        It supports various prompt types including confirmation, input, and choice prompts.

        .. versionadded:: v2.0.0

        :param question: The question to ask the user.
        :type question: str
        :param kwargs: Additional arguments to pass to the prompt function.
        :return: The user's response based on the prompt type.
        :rtype: Any
        :param prompt_type: The type of prompt to use. Defaults to :class:`rich.prompt.Confirm`.
        :param console: The console to use for the prompt. Defaults to None.
        :param password: Whether to hide input when prompting for passwords. Defaults to False.
        :param choices: List of valid choices for choice prompts. Defaults to None.
        :param default: Default value for prompts that support it. Defaults to None.
        :param show_default: Whether to show the default value. Defaults to True.
        :param show_choices: Whether to show available choices. Defaults to True.
        :param case_sensitive: Whether choices are case sensitive. Defaults to True.
        """
        prompt_type = kwargs.pop('prompt_type', rich.prompt.Confirm)
        console = kwargs.pop('console', None)
        password = kwargs.pop('password', False)
        choices = kwargs.pop('choices', None)
        default = kwargs.pop('default', None)
        show_default = kwargs.pop('show_default', True)
        show_choices = kwargs.pop('show_choices', True)
        case_sensitive = kwargs.pop('case_sensitive', True)

        return prompt_type.ask(
            question,
            console=console,
            password=password,
            choices=choices,
            default=default,
            case_sensitive=case_sensitive,
            show_default=show_default,
            show_choices=show_choices,
        )
