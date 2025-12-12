#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Module provides a set of enumerators for dealing with standard tasks.
"""

from __future__ import annotations

from enum import Enum, IntEnum, StrEnum, auto


class ProcessorExitStatus(IntEnum):
    """The processor exit status enumerator class

    * Successful: means that the processor reached the end with success
    * Failed: means that the processor did not reach the end with success
    * Aborted: means that the user aborted the processor execution

    """

    Successful = auto()
    """The processor execution was successfully concluded"""

    Failed = auto()
    """The processor execution was failed"""

    Aborted = auto()
    """The processor execution was aborted by the user"""


class ProcessorStatus(StrEnum):
    """Enumerator to describe the status of a processor."""

    Unknown = 'unknown'
    """Unknown status"""
    Init = 'initializing'
    """Initialized"""
    Start = 'starting'
    """Started"""
    Run = 'processing'
    """Running"""
    Finish = 'finishing'
    """Finished"""


class LoopingStatus(IntEnum):
    """
    Enumerator to modify the looping cycle.

    In the case of a looping Processor, the user has the ability to slightly modify the looping structure using this
    enumerator.

    In the :meth:`~mafw.processor.Processor.process` the user can set the variable `looping_status` to one of the following values:

    - :attr:`LoopingStatus.Continue`. It means that everything is working well and the loop cycle must go ahead as
      foreseen and the :meth:`~mafw.processor.Processor.accept_item` will be invoked.

    - :attr:`LoopingStatus.Skip`. The :meth:`~mafw.processor.Processor.skip_item` will be called soon after the
      :meth:`~mafw.processor.Processor.process` is finished. The status will be reset to Continue and the next item will be processed.

    - :attr:`LoopingStatus.Abort`. The cycle is broken immediately.

    - :attr:`LoopingStatus.Quit`. The cycle is broken immediately.

    The last two options are apparently identical, but they offer the possibility to implement a different behaviour
    in the :meth:`~mafw.processor.Processor.finish` method. When abort is used, then the
    :class:`~mafw.mafw_errors.AbortProcessorException` will be raised. For example, the user can decide to rollback
    all changes if an abort as occurred or to save what done so far in case of a quit.
    """

    Continue = auto()
    """The loop can continue"""

    #: Skip this item.
    Skip = auto()

    #: Break the loop and force the outside container (:class:`mafw.processor.ProcessorList`) to quit.
    Abort = auto()

    #: Break the loop but let the outside container (:class:`mafw.processor.ProcessorList`) to continue.
    Quit = auto()


class LoopType(StrEnum):
    """
    The loop strategy for the processor.

    Each processor can be executed in one of the following modes:

        #. **Single mode.** The process method is executed only once.

        #. **For loop mode.** The process method is executed inside a for loop after the start and before the finish. The
           loop is based on a list of elements, the user **must** overload the :meth:`~mafw.processor.Processor.get_items`
           method to define the list of items for the loop.

        #. **While loop mode.** The process method is executed inside a while loop after the start and before the finish.
           The user **must** overload the :meth:`~mafw.processor.Processor.while_condition` to define when to stop the loop.

    .. admonition:: Future development

        Implement concurrent loop. Depending on the development of the `free-threading capabilities
        <https://docs.python.org/3/howto/free-threading-python.html>`_ of future python releases, this concurrent
        looping strategy might be based on threads or a porting of the ``autorad`` multi-processor approach.
    """

    SingleLoop = 'single'
    """Value for the single mode execution."""

    ForLoop = 'for_loop'
    """Value for the for loop on item list execution."""

    WhileLoop = 'while_loop'
    """Value for the while loop execution."""


class LogicalOp(Enum):
    """
    Enumeration of supported logical operations.

    .. versionadded:: v1.3.0
    """

    EQ = '=='  # Equal
    NE = '!='  # Not equal
    LT = '<'  # Less than
    LE = '<='  # Less than or equal
    GT = '>'  # Greater than
    GE = '>='  # Greater than or equal
    GLOB = 'GLOB'  # String pattern matching
    LIKE = 'LIKE'  # SQL LIKE pattern matching
    REGEXP = 'REGEXP'  # Regular expression matching
    IN = 'IN'  # Value in list
    NOT_IN = 'NOT_IN'  # Value not in list
    BETWEEN = 'BETWEEN'  # Value between two bounds
    BIT_AND = 'BIT_AND'  # Bitwise AND
    BIT_OR = 'BIT_OR'  # Bitwise OR
    IS_NULL = 'IS_NULL'  # Field is NULL
    IS_NOT_NULL = 'IS_NOT_NULL'  # Field is not NULL
