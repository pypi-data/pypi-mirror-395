#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
The module provides examples on how the user can change the looping structure in a looping processor using the
looping status.
"""

import logging
import math
from typing import Any, Collection

from mafw.decorators import for_loop, while_loop
from mafw.enumerators import LoopingStatus
from mafw.processor import ActiveParameter, Processor

log = logging.getLogger(__name__)


class ModifyLoopProcessor(Processor):
    """
    Example processor demonstrating how it is possible to change the looping structure.

    It is a looping processor where some events will be skipped, and at some point one event will trigger an abort.
    """

    total_item: ActiveParameter[int] = ActiveParameter('total_item', default=100, help_doc='Total item in the loop.')
    items_to_skip: ActiveParameter[list[int]] = ActiveParameter(
        'items_to_skip', default=[12, 16, 25], help_doc='List of items to be skipped.'
    )
    item_to_abort: ActiveParameter[int] = ActiveParameter('item_to_abort', default=65, help_doc='Item to abort')

    def __init__(self, *args, **kwargs):
        """
        Processor Parameters:

        :param total_item: The total number of items
        :type total_item: int
        :param items_to_skip: A list of items to skip.
        :type items_to_skip: list[int]
        :param item_to_abort: The item where to trigger an abort.
        :type item_to_abort: int

        """
        super().__init__(*args, **kwargs)
        self.skipped_items: [list[int]] = []
        """A list with the skipped items."""

    def start(self):
        """Resets the skipped item container."""
        super().start()
        self.skipped_items = []

    def get_items(self) -> list[int]:
        """Returns the list of items, the range from 0 to total_item."""
        return list(range(self.total_item))

    def process(self):
        """Processes the item"""
        if self.item in self.items_to_skip:
            self.looping_status = LoopingStatus.Skip
            return
        if self.item == self.item_to_abort:
            self.looping_status = LoopingStatus.Abort
            return

    def skip_item(self):
        """Add skipped item to the skipped item list."""
        self.skipped_items.append(self.item)


def is_prime(n: int) -> bool:
    """
    Check if n is a prime number.

    :param n: The integer number to be checked.
    :type n: int
    :return: True if n is a prime number. False, otherwise.
    :rtype: bool
    """
    prime = True
    if n < 2:
        prime = False
    elif n == 2:
        prime = True
    elif n % 2 == 0:
        prime = False
    else:
        sqrt_n = int(math.floor(math.sqrt(n)))
        for i in range(3, sqrt_n + 1, 2):
            if n % i == 0:
                prime = False

    return prime


@while_loop
class FindNPrimeNumber(Processor):
    """
    An example of Processor to search for N prime numbers starting from a given starting integer.

    This processor is meant to demonstrate the use of a while_loop execution workflow.

    Let us say we need to find 1000 prime numbers starting from 12347. One possible brute force approach to solve this
    problem is to start checking if the initial value is a prime number. If this is not the case, then check the next
    odd number. If it is the case, then add the current number to the list of found prime numbers and continue until
    the size of this list is 1000.

    This is a perfect application for a while loop execution workflow.
    """

    prime_num_to_find = ActiveParameter(
        'prime_num_to_find', default=100, help_doc='How many prime number we have to find'
    )
    start_from = ActiveParameter('start_from', default=50, help_doc='From which number to start the search')

    def __init__(self, *args: Any, **kwargs: Any):
        """
        Processor parameters:

        :param prime_num_to_find: The number of prime numbers to be found.
        :type prime_num_to_find: int
        :param start_from: The initial integer number from where to start the search.
        :type start_from: int
        """
        super().__init__(*args, **kwargs)
        self.prime_num_found: list[int] = []
        """The list with the found prime numbers"""

    def format_progress_message(self) -> None:
        self.progress_message = (
            f'Checking integer number: {self.item}, already found {len(self.prime_num_found)} prime numbers'
        )

    def while_condition(self) -> bool:
        """
        Define the while condition.

        First, it checks if the prime_num_to_find is positive. Otherwise, it does not make sense to start.
        Then it will check if the length of the list with the already found prime numbers is enough. If so, then we can
        stop the loop return False, otherwise, it will return True and continue the loop.

        Differently from the for_loop execution, we are responsible to assign the value to the looping variables
        :attr:`.Processor.i_item`, :attr:`.Processor.item` and :attr:`.Processor.n_item`.

        In this case, we will use the :attr:`.Processor.i_item` to count how many prime numbers we have found and :attr:`.Processor.n_item`
        will be our target. In this way, the progress bar will work as expected.

        In the while condition, we set the :attr:`.Processor.i_item` to the current length of the found prime number list.

        :return: True if the loop has to continue, False otherwise
        """
        if self.prime_num_to_find <= 0:
            log.warning('You requested to find a negative number of prime numbers. It makes no sense.')
            return False

        self.i_item = len(self.prime_num_found)
        return self.i_item < self.prime_num_to_find

    def start(self) -> None:
        """
        The overload of the start method.

        **Remember:** The start method is called just before the while loop is started. So all instructions in this
        method will be executed only once at the beginning of the process execution. Always put a call to its `super`
        when you overload start.

        First, we empty the list of found prime numbers. It should not be necessary, but it makes the code more readable.
        Then set the :attr:`.Processor.n_item` to the total number of prime numbers we need to find. In this way, the progress bar
        will display useful progress.

        If the start value is smaller than 2, then let's add 2 to the list of found prime number and set our first
        item to check at 3. In principle, we could already add 3 as well, but maybe the user wanted to find only 1
        prime number, and we are returning a list with two, that is not what he was expecting.

        Since prime numbers different from 2 can only be odd, if the starting number is even, increment it already by
        1 unit.
        """
        super().start()
        self.prime_num_found = []
        self.n_item = self.prime_num_to_find
        if self.start_from < 2:
            self.prime_num_found.append(2)
            self.start_from = 3

        if self.start_from % 2 == 0:
            self.item = self.start_from + 1
        else:
            self.item = self.start_from

    def process(self) -> None:
        """
        The overload of the process method.

        **Remember:** The process method is called inside the while loop. It has access to the looping parameters:
        :attr:`.Processor.i_item`, :attr:`.Processor.item` and :attr:`.Processor.n_item`.

        In our specific case, the process contains another while loop. We start by checking if the current
        :attr:`.Processor.item` is a prime number or not. If so, then we have found the next prime number, we add it to the list,
        we increment by two units the value of :attr:`.Processor.item` and we leave the process method ready for the next iteration.

        If :attr:`.Processor.item` is not prime, then increment it by 2 and check it again.
        """
        while not is_prime(self.item):
            self.item += 2
        self.prime_num_found.append(self.item)
        self.item += 2

    def finish(self) -> None:
        """
        Overload of the finish method.

        **Remember:** The finish method is called only once just after the last loop interaction.
        Always put a call to its `super` when you overload finish.

        The loop is over, it means that the while condition was returning false, and now we can do something with our
        list of prime numbers.
        """
        super().finish()
        log.info('Found the requested %s prime numbers' % len(self.prime_num_found))
        log.info('The smallest is %s', self.prime_num_found[0])
        log.info('The largest is %s', self.prime_num_found[-1])


@for_loop
class FindPrimeNumberInRange(Processor):
    """
    An example processor to find prime numbers in the defined interval from ``start_from`` to ``stop_at``.

    This processor is meant to demonstrate the use of a for_loop execution workflow.

    Let us say we want to select only the prime numbers in a user defined range. One possible brute force approach is
    to generate the list of integers between the range extremes and check if it is prime or not. If yes,
    then add it to the list of prime numbers, if not continue with the next element.

    This is a perfect application for a loop execution workflow.
    """

    start_from = ActiveParameter('start_from', default=50, help_doc='From which number to start the search')
    stop_at = ActiveParameter('stop_at', default=100, help_doc='At which number to stop the search')

    def __init__(self, *args: Any, **kwargs: Any):
        """
        Processor parameters:

        :param start_from: First element of the range under investigation.
        :type start_from: int
        :param stop_at: Last element of the range under investigation.
        :type stop_at: int
        """
        super().__init__(*args, **kwargs)
        self.prime_num_found: list[int] = []
        """The list with the found prime numbers"""

    def format_progress_message(self) -> None:
        self.progress_message = (
            f'Checking integer number: {self.item}, already found {len(self.prime_num_found)} prime numbers'
        )
        # end of format_progress_message

    def get_items(self) -> Collection[Any]:
        """
        Overload of the get_items method.

        This method must be overloaded when you select a for loop workflow.

        Here we generate the list of odd numbers between the start and stop that we need to check.
        We also check that the stop is actually larger than the start, otherwise we print an error message, and we
        return an empty list of items.

        :return: A list of odd integer numbers between start_from and stop_at.
        :rtype: list[int]
        """
        if self.start_from >= self.stop_at:
            log.critical('%s must be smaller than %s' % (self.start_from, self.stop_at))
            return []

        if self.start_from != 2 and self.start_from % 2 == 0:
            self.start_from += 1

        if self.stop_at != 2 and self.stop_at % 2 == 0:
            self.stop_at -= 1

        return list(range(self.start_from, self.stop_at, 2))

    def start(self) -> None:
        """
        Overload of the start method.

        **Remember:** to call the super method when you overload the start.

        In this specific case, we just make sure that the list of found prime numbers is empty.
        """
        super().start()
        self.prime_num_found = []

    def process(self) -> None:
        """
        The process method.

        In this case, it is very simple. We check if :attr:`.Processor.item` is a prime number, if so we added to the list,
        otherwise we let the loop continue.
        """
        if is_prime(self.item):
            self.prime_num_found.append(self.item)

    def finish(self) -> None:
        """
        Overload of the finish method.

        **Remember:** to call the super method when you overload the finish method.

        In this case, we just print out some information about the prime number found in the range.
        """
        super().finish()
        log.info(
            'Found %s prime numbers in the range from %s to %s'
            % (len(self.prime_num_found), self.start_from, self.stop_at)
        )
        if len(self.prime_num_found):
            log.info('The smallest is %s', self.prime_num_found[0])
            log.info('The largest is %s', self.prime_num_found[-1])
