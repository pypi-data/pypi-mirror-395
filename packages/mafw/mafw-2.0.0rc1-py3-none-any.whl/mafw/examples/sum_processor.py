#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
The module provides some examples for the user to develop their own processors.

Those implemented here are mainly used in the test suit.
"""

from mafw.enumerators import LoopType
from mafw.processor import ActiveParameter, Processor


class AccumulatorProcessor(Processor):
    r"""
    A processor to calculate the sum of the first n values via a looping approach.

    In mathematical terms, this processor solves this easy equation:

    .. math::

        N = \sum_{i=0}^{n}{i}

    by looping. It is a terribly inefficient approach, but it works as a demonstration of the looping structure.

    The user can get the results by retrieving the `accumulated_value` parameter at the end of the processor
    execution.
    """

    last_value = ActiveParameter('last_value', default=100, help_doc='Last value of the series')

    def __init__(self, *args, **kwargs):
        """Constructor parameters:

        :param last_value: The `n` in the equation above. Defaults to 100
        :type last_value: int
        :param accumulated_value: The `N` in the equation above at the end of the process.
        :type accumulated_value: int
        """
        super().__init__(*args, **kwargs)
        self.accumulated_value: int = 0

    def start(self):
        """Resets the accumulated value to 0 before starting."""
        super().start()
        self.accumulated_value = 0

    def get_items(self) -> list[int]:
        """Returns the list of the first `last_value` integers."""
        return list(range(self.last_value))

    def process(self):
        """Increase the accumulated value by the current item."""
        self.accumulated_value += self.item


class GaussAdder(Processor):
    r"""
    A processor to calculate the sum of the first n values via the so called *Gauss formula*.

    In mathematical terms, this processor solves this easy equation:

    .. math::

        N = \frac{n * (n - 1)}{2}

    without any looping

    The user can get the results by retrieving the `sum_value` parameter at the end of the processor
    execution.
    """

    last_value = ActiveParameter('last_value', default=100, help_doc='Last value of the series.')

    def __init__(self, *args, **kwargs):
        """
        Constructor parameters:

        :param last_value: The `n` in the equation above. Defaults to 100
        :type last_value: int
        :param sum_value: The `N` in the equation above.
        :type sum_value: int
        """
        super().__init__(looper=LoopType.SingleLoop, *args, **kwargs)
        self.sum_value: int = 0

    def start(self):
        """Sets the sum value to 0."""
        super().start()
        self.sum_value = 0

    def process(self):
        """Compute the sum using the Gauss formula."""
        self.sum_value = int(self.last_value * (self.last_value - 1) / 2)
