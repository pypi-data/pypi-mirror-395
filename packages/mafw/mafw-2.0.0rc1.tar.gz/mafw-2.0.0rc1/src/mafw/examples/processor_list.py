#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
The module provides some examples on how to use ProcessorList to combine several processors.
"""


def run_simple_processor_list():
    """Simplest way to run several processors in a go."""
    from mafw.examples.sum_processor import AccumulatorProcessor, GaussAdder
    from mafw.processor import ProcessorList

    # create the list. name and description are optional
    new_list = ProcessorList(name='AddingProcessor', description='Summing up numbers')

    # append the processors. you can pass parameters to the processors in the standard way
    max_value = 120
    new_list.append(AccumulatorProcessor(last_value=max_value))
    new_list.append(GaussAdder(last_value=max_value))

    # execute the list. This will execute all the processors in the list
    new_list.execute()

    # you can access single processors in the list, in the standard way.
    # remember that the ProcessorList is actually a list!
    assert new_list[0].accumulated_value == new_list[1].sum_value


def run_processor_list_with_loop_modifier():
    """Example on deal with processors inside a processor list changing the loop structure.

    In this example there are two processors, one that will run until the end and the other that will set the looping
    status to abort half way. The user can see what happens when the :class:`~mafw.processor.ProcessorList` is executed.
    """
    import time

    from mafw.enumerators import LoopingStatus, ProcessorExitStatus, ProcessorStatus
    from mafw.mafw_errors import AbortProcessorException
    from mafw.processor import ActiveParameter, Processor, ProcessorList

    class GoodProcessor(Processor):
        n_loop = ActiveParameter('n_loop', default=100, help_doc='The n of the loop')
        sleep_time = ActiveParameter('sleep_time', default=0.01, help_doc='So much work')

        def get_items(self) -> list[int]:
            return list(range(self.n_loop))

        def process(self):
            # pretend to do something, but actually sleep
            time.sleep(self.sleep_time)

        def finish(self):
            super().finish()
            print(f'{self.name} just finished with status: {self.processor_exit_status.name}')

    class BadProcessor(Processor):
        n_loop = ActiveParameter('n_loop', default=100, help_doc='The n of the loop')
        sleep_time = ActiveParameter('sleep_time', default=0.01, help_doc='So much work')
        im_bad = ActiveParameter('im_bad', default=50, help_doc='I will crash it!')

        def get_items(self) -> list[int]:
            return list(range(self.n_loop))

        def process(self):
            if self.item == self.im_bad:
                self.looping_status = LoopingStatus.Abort
                return
            # let me do my job
            time.sleep(self.sleep_time)

        def finish(self):
            super().finish()
            print(f'{self.name} just finished with status: {self.processor_exit_status.name}')

    proc_list = ProcessorList(name='with exception')
    proc_list.extend([GoodProcessor(), BadProcessor(), GoodProcessor()])
    try:
        proc_list.execute()
    except AbortProcessorException:
        print('I know you were a bad guy')
    assert proc_list.processor_exit_status == ProcessorExitStatus.Aborted
    assert proc_list[0].processor_exit_status == ProcessorExitStatus.Successful
    assert proc_list[1].processor_exit_status == ProcessorExitStatus.Aborted
    assert proc_list[2].processor_status == ProcessorStatus.Init
