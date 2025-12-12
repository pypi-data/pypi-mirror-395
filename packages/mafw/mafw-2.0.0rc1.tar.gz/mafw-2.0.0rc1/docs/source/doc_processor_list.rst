.. _processor_list:

ProcessorList: Combine your processors in one go
================================================

So far we have seen how a :class:`~mafw.processor.Processor` can be coded to perform a simple task with a certain degree of generality offered by the configurable parameters. But analytical tasks are normally rather complex and coding the whole task in a single processor will actually go against the mantra of simplicity and code reusability of MAFw.

To tackle your complex analytical task, MAFw proposes a solution that involves chaining multiple processors together. The following processors can start where the previous one stopped so that like in a building game, scientists can put together their analytical solution with simple blocks.

From a practical point of view, this is achieved via the :class:`~mafw.processor.ProcessorList` that is an evolution of the basic python list, which can contain only instances of processor subclasses or other ProcessorLists.

Once you have appended the processors in the order you want them to be executed, just call the :meth:`~mafw.processor.ProcessorList.execute` method of the list and it will take care of running all the processors.

As simple as that:

.. literalinclude:: ../../src/mafw/examples/processor_list.py
    :linenos:
    :pyobject: run_simple_processor_list
    :name: processor_list_snippet1

.. _exit_status:

The :class:`~mafw.enumerators.ProcessorExitStatus`
--------------------------------------------------

We have seen in a :ref:`previous section <execution_workflow>` that the user can modify the looping behavior of a processor by using the :class:`~mafw.enumerators.LoopingStatus` enumerator. In a similar manner, the execution loop of a processor list can be modified looking at the :class:`~mafw.enumerators.ProcessorExitStatus` of each processors.

When one processor in the list is finishing its task, the :class:`~mafw.processor.ProcessorList` is checking for its exit status before moving to the next item. If a processor is finishing with an Abort status, then the processor list will raise a :class:`~mafw.mafw_errors.AbortProcessorException` that will cause the loop to be interrupted.

Let us have a look at the snippet here below:

.. literalinclude:: ../../src/mafw/examples/processor_list.py
    :linenos:
    :pyobject: run_processor_list_with_loop_modifier
    :name: processor_list_snippet2

We created two processors, a good and a bad one. The good one is doing nothing, but getting till the end of its job. The bad one is also doing nothing but giving up before the end of the item list. In the process method, the bad processor is setting the looping status to abort, causing the for loop to break immediately and to call finish right away. In the processor finish method, we check if the status was aborted and in such a case we set the exit status of the processor to Aborted.

At line 47, we create a list and we populate it with three elements, a good, a bad and another good processor and we execute it inside a try/except block. The execution of the first good processor finished properly as you can see from the print out and also from the fact that its status (line 54) is Successful. The second processor did not behave, the exception was caught by the except clause and this is confirmed at line 55 by its exit status. The third processor was not even started because the whole processor list got stopped in the middle of processor 2.

Resources acquisition and distribution
--------------------------------------

While it may seems somewhat technical for this for this tutorial, it is worth highlighting an intriguing implementation detail.
If you look at the constructor of the :class:`~mafw.processor.Processor` class, you will notice that you can provide some resources, like the Timer and UserInterface even though we have never done this so far. The idea is that when you execute a single processor, it is fully responsible of creating the required resources by itself, using them during the execution and then closing them when finishing.

Just as an example, consider the case of the use of a database interface. The processor is opening the connection, doing all the needed transactions and finally closing the connection. This approach is also very practical because it is much easier to keep expectations under control.

If you run a :class:`~mafw.processor.ProcessorList`, you may want to move the responsibility of handling the resources from the single Processor to the output ProcessorList.
This approach allows all processors to share the same resources efficiently, eliminating the need to repeatedly open and close the database connection each time the ProcessorList advances to the next item.

You do not have to care about this shift in responsibility, it is automatically done behind the scene when you add a processor to the processor lists.

What's next
-----------

In this part we have seen how we can chain the execution of any number of processors all sharing the same resources. Moreover, we have seen how we can change the looping among different processors using the exit status.

Now it is time to move forward and see how you can add your own processor library!