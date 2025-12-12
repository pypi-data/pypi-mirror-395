#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Module implements a simple timer to measure the execution duration.

Basic usage:

.. code-block:: python

    from mafw import timer

    with Timer() as timer:
        do_long_lasting_operation()

When exiting from the context manager, a message with the duration of the process is printed.

"""

import logging
from datetime import timedelta
from time import perf_counter
from types import TracebackType


def pretty_format_duration(duration_s: float, n_digits: int = 1) -> str:
    """
    Return a formatted version of the duration with increased human readability.

    :param duration_s: The duration to be printed in seconds. If negative, a ValueError exception is raised.
    :type duration_s: float
    :param n_digits: The number of decimal digits to show. Defaults to 1. If negative, a ValueError exception is raised.
    :type n_digits: int, Optional
    :return: The formatted string.
    :rtype: str
    :raises ValueError: if a negative duration or a negative number of digits is provided
    """
    if duration_s < 0:
        raise ValueError(f'Duration ({duration_s}) cannot be a negative value')
    if n_digits < 0:
        raise ValueError('The number of decimal digits cannot be a negative value')
    td = timedelta(seconds=duration_s)
    days = td.days
    hours = td.seconds // 3600
    minutes = (td.seconds - hours * 3600) // 60
    seconds = round((td.seconds - hours * 3600 - minutes * 60) + td.microseconds / 1e6, n_digits)
    time_array = tuple([days, hours, minutes, seconds])
    if time_array <= (0, 0, 0, 0):
        return f'< {time_array[3]:.{n_digits}f} seconds'
    up = ['days', 'hours', 'minutes', 'seconds']
    us = ['day', 'hour', 'minute', 'second']
    msg = ''
    for ti, usi, upi in zip(time_array, us, up):
        if ti == 0:
            pass
        elif ti == 1:
            msg += f'{ti} {usi}, '
        else:
            msg += f'{ti} {upi}, '

    return rreplace(msg.rstrip(', '), ', ', ' and ', 1)


def rreplace(inp_string: str, old_string: str, new_string: str, counts: int) -> str:
    """
    Utility function to replace a substring in a given string a certain number of times starting from the right-most one.

    This function is mimicking the behavior of the string.replace method, but instead of replacing from the left, it
    is replacing from the right.

    :param inp_string: The input string
    :type inp_string: str
    :param old_string: The old substring to be matched. If empty, a ValueError is raised.
    :type old_string: str
    :param new_string: The new substring to be replaced
    :type new_string: str
    :param counts: The number of times the old substring has to be replaced.
    :type counts: int
    :return: The modified string
    :rtype: str
    :raises ValueError: if old_string is empty.
    """
    if old_string == '':
        raise ValueError('old_string cannot be empty')
    li = inp_string.rsplit(old_string, counts)
    return new_string.join(li)


class Timer:
    """
    The timer class.
    """

    def __init__(self, suppress_message: bool = False) -> None:
        """
        Constructor parameter:

        :param suppress_message: A boolean flag to mute the timer
        :type suppress_message: bool
        """
        self._suppress_message = suppress_message
        self.start = 0.0
        self.end = 0.0

    def __enter__(self) -> 'Timer':
        """
        Context manager enter dunder method.

        When an instance of the Timer class is created via the context manager, the start time attribute is set to the
        current time, while the end is set to zero.

        :return: The class instance.
        """
        self.start = perf_counter()
        self.end = 0.0
        return self

    def __exit__(
        self, type_: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None
    ) -> None:
        """
        Context manager exit dunder method.

        When the method is invoked, the end time is set to the current time, and, if the timer is not muted, a log
        message with the total duration is printed.

        :param type_: Exception type causing the context manager to exit. Defaults to None.
        :type type_: type[BaseException], Optional
        :param value: Exception that caused the context manager to exit. Defaults to None.
        :type value: BaseException, Optional
        :param traceback: Traceback. Defaults to None.
        :type traceback: TracebackType
        """
        self.end = perf_counter()
        if not self._suppress_message:
            logging.getLogger(__name__).info('Total execution time: %s' % self.format_duration())

    @property
    def duration(self) -> float:
        """
        The elapsed time of the timer.

        :return: Elapsed time in seconds.
        """
        return self.end - self.start

    def format_duration(self) -> str:
        """
        Nicely format the timer duration.

        :return: A string with the timer duration in a human-readable formatted string
        :rtype: str
        """
        return pretty_format_duration(self.duration)
