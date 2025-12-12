.. _examples:

Processor Examples
------------------

From this page, you can see a few example of processors in order to simplify the creation of your first processor sub class.

.. _loopers:

Simple and looping processors
+++++++++++++++++++++++++++++

The first two examples of this library are demonstrating how you can implement a simple processor that execute all calculations in one go and a looping processor where you need to loop over a list of items to get either a cumulative results.

:class:`~mafw.examples.sum_processor.AccumulatorProcessor` is calculating the sum of the first N integer numbers in a loop. The processor takes the *last_number* as an input to include and put the output in the *accumulated_value* parameter. This process is very inefficient, but it is here to demonstrate how to subclass a looping processor.

.. literalinclude:: ../../src/mafw/examples/sum_processor.py
    :linenos:
    :pyobject: AccumulatorProcessor


:class:`~mafw.examples.sum_processor.GaussAdder` is calculating exactly the same result using the Gauss formula, eliminating the need for any looping. Indeed the looping is disabled and the output is the same.

.. literalinclude:: ../../src/mafw/examples/sum_processor.py
    :linenos:
    :pyobject: GaussAdder
    :emphasize-lines: 28

If you carefully look at line 28, you will notice that in the GaussAdder constructor, the looper option is set to SingleLoop and as we have :ref:`seen <execution_workflow>`, it means that that the processor will follow the single loop execution workflow.

The definition of the looper parameter in the init method can be sometimes hard to remember and unpractical especially if you have to overload the init method just to set the value of the looper. In such circumstances the use of a class decorator can be very handy. MAFw makes you available three class decorators for this purpose, to transform a processor in a :func:`single loop <mafw.decorators.single_loop>`, a :func:`for loop <mafw.decorators.for_loop>` or a :func:`while loop <mafw.decorators.while_loop>`.

Using the decorator approach the GaussAdder above can be re-written in this way:

.. code-block:: python

    @single_loop
    class GaussAdder(Processor):
        # the rest of the implementation remains the same


And here below is an example of execution of the two.

.. testcode::

    from mafw.examples.sum_processor import GaussAdder, AccumulatorProcessor

    n = 35

    # create the two processors
    accumulator = AccumulatorProcessor(last_value=n)
    gauss = GaussAdder(last_value=n)

    # execute them
    accumulator.execute()
    gauss.execute()

    # print the calculated results
    print(accumulator.accumulated_value)
    print(gauss.sum_value)

This will generate the following output:

.. testoutput::

    595
    595

.. _mod_loop:

Modify the `for loop` cycle using the :class:`~mafw.enumerators.LoopingStatus`
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

In a looping processor, the :meth:`~mafw.processor.Processor.process` method is invoked inside a loop, but the user can decide to skip a certain item and even to interrupt the (abort or quit) the loop.

The tool to achieve this is the :class:`~mafw.enumerators.LoopingStatus`. This is set to Continue at the beginning of each iteration, but the user can turn it Skip, Abort or Quit inside the implementation of :meth:`~mafw.processor.Processor.process`.

When set to Skip, a special callback is invoked :meth:`~mafw.processor.Processor.skip_item` where the user can do actions accordingly.
When set to Abort or Quit, the loop is broken and the user can decide what to do in the :meth:`~mafw.processor.Processor.finish` method. Those two statuses seams to be redundant, but this gives the user the freedom to decide if everything was wasted (Abort) or if what done so far was still acceptable (Quit).

Here below is the implementation of a simple processor demonstrating such a functionality.

.. literalinclude:: ../../src/mafw/examples/loop_modifier.py
    :linenos:
    :pyobject: ModifyLoopProcessor

And here below is how the processor can be used.

.. code-block:: python
    :linenos:

    import random
    from mafw.examples.loop_modifier import ModifyLoopProcessor

    # generate a random number corresponding to the last item
    last_value = random.randint(10, 1000)

    # get a sample with event to be skipped
    skip_items = random.sample(range(last_value), k=4)

    # find an event to abort after the last skipped one
    max_skip = max(skip_items)
    if max_skip + 1 < last_value:
        abort_item = max_skip + 1
    else:
        abort_item = last_value - 1

    # create the processor and execute it
    mlp = ModifyLoopProcessor(total_item=last_value, items_to_skip=skip_items, item_to_abort=abort_item)
    mlp.execute()

    # compare the recorded skipped items with the list we provided.
    assert mlp.skipped_items == list(sorted(skip_items))

    # check that the last item was the abort item.
    assert mlp.item == abort_item

.. _for_and_while:

For and while loop execution workflow
+++++++++++++++++++++++++++++++++++++

We have seen in the previous chapter that there are different type of loopers and in the previous section we have seen in practice the execution workflow of a single loop and a while loop processor.

In this example, we will explore the difference between the **for loop** and the **while loop** execution workflow. Both processors will run the :meth:`.Processor.process` method inside a loop, but for the former we will loop over a pre-established list of items, while for the latter we will continue repeating the process until a certain condition is valid.

Both processors will work with prime number and we will use this :func:`helper function <.is_prime>` to check if an integer number is prime or not.

.. literalinclude:: ../../src/mafw/examples/loop_modifier.py
    :linenos:
    :pyobject: is_prime

The task of the **for loop** processor is to find all prime numbers included in a given user defined range of integer numbers. In other words, we want to find all prime numbers between 1000 and 2000, for example. The brute force approach is to start a loop on 1000, check if it is prime and if not check the next one until you get to 2000. If a number is actually prime, then store it in a list for further use.

For the sake of clarity, along with the :class:`API documentation <.FindPrimeNumberInRange>`, we are copying here also the processor source code.

.. literalinclude:: ../../src/mafw/examples/loop_modifier.py
    :linenos:
    :pyobject: FindPrimeNumberInRange
    :end-at: """The list with the found prime numbers"""

This is the class definition with its constructor. As you can see, we have decorated the class with the :func:`for loop decorator <.for_loop>` even though it is not strictly required because the for loop is the default execution workflow.

We have added two processor parameters, the ``start_from`` and the ``stop_at`` to allow the user to specify a range on interest where to look for prime numbers.

In the init method, we create a list of integer to store all the prime numbers that we will finding during the process.

Now let us overload all compulsory methods for a **for loop** processor.

.. literalinclude:: ../../src/mafw/examples/loop_modifier.py
    :linenos:
    :dedent:
    :pyobject: FindPrimeNumberInRange
    :start-at: def get_items(self) -> Collection[Any]:
    :end-at: return list(range(self.start_from, self.stop_at, 2))

The get items method is expected to return a list of items, that will be processed by the :meth:`.Processor.process` method. It is absolutely compulsory to overload this method, otherwise the whole loop structure will not have a list to loop over.

And now, let us have a look at the three stages: start, process and finish.

.. literalinclude:: ../../src/mafw/examples/loop_modifier.py
    :linenos:
    :dedent:
    :pyobject: FindPrimeNumberInRange
    :start-at: def start(self) -> None:
    :end-at: log.info('The largest is %s', self.prime_num_found[-1])

These three methods are the core of the execution workflow, so it is obvious that you have to overload them. Keep in mind to always include a call to the super method when you overload the start and finish because they perform some tasks also in the basic processor implementation. The code is written in a straightforward manner and includes clear, thorough explanations in the docstring.

The looping parameters: :attr:`.Processor.i_item`, :attr:`.Processor.n_item` and :attr:`.Processor.item` can be used while implementing the :meth:`~.Processor.process` and :meth:`~.Processor.finish`. The :attr:`~.Processor.n_item` is calculated soon after the list of items is returned, while :attr:`~.Processor.item`, :attr:`~.Processor.i_item` are assigned in the for loop as the current item and its enumeration.

Optionally, one can overload the :meth:`~.Processor.format_progress_message` in order to generate a nice progress message informing the user that something is happening. This is an example:

.. literalinclude:: ../../src/mafw/examples/loop_modifier.py
    :linenos:
    :dedent:
    :pyobject: FindPrimeNumberInRange
    :start-at: def format_progress_message(self) -> None:
    :end-before: # end of format_progress_message

The task for the **while loop** processor is again about prime number finding but different. We want to find a certain number of prime numbers starting from an initial value. We cannot generate a list of integer number and loop over that in the :class:`.FindPrimeNumberInRange`, but we need to reorganize our workflow in order to loop until the number of found primes is equal to the requested one.

This is how such a task can be implemented using the while loop execution framework. You can find the example in the :class:`API documentation <.FindNPrimeNumber>` and an explanation of the here below.

Let us start again from the class definition.

.. literalinclude:: ../../src/mafw/examples/loop_modifier.py
    :linenos:
    :dedent:
    :pyobject: FindNPrimeNumber
    :end-at: """The list with the found prime numbers"""

The first difference compared to the previous case is the use of the :func:`.while_loop` decorator, this time it is really necessary to specify the processor :class:`.LoopType` because the while loop is not the default strategy.

The processor has two parameters, the number of prime number to find and from where to start. Similarly as before, in the init method, we define a list of integer to store all the prime numbers that we have found.

For while loop processor, we don't have a list of items, but we need to have a condition either to continue or to stop the loop. For this reason we need to overload the :meth:`~.Processor.while_condition` method, keeping in mind that we return True if we want the cycle to continue for another iteration and False otherwise.

Here is the implementation of the :meth:`~.FindNPrimeNumber.while_condition` for the :class:`.FindNPrimeNumber`.

.. literalinclude:: ../../src/mafw/examples/loop_modifier.py
    :linenos:
    :dedent:
    :pyobject: FindNPrimeNumber
    :start-at: def while_condition(self) -> bool:
    :end-at: return self.i_item < self.prime_num_to_find

For a while loop, it is not easy to define an enumeration parameter and also the total number of items might be misleading. It is left to the user to decide if they want to use them or not. If yes, their definition and incrementation is under their responsability. For this processor, it was natural to consider the requested number of primes as the :attr:`.n_item` and consequently the value of :attr:`.i_item` can be utilized to keep track of the quantity of prime numbers that have already been discovered.
This choice is very convenient because then progress bar that uses :attr:`.i_item` and :attr:`.n_item` to calculate the progress will show the actual progress. In case, you do not have any way to assign a value to :attr:`.n_item`, do not do it, or set it to None. In this way, the progress bar will display an `indeterminate progress <https://rich.readthedocs.io/en/latest/progress.html#indeterminate-progress>`_ . You can set the value of :attr:`.n_item` either in the :meth:`~.Processor.start` or in the :meth:`~.Processor.while_condition`, with a performance preference with the first option because it is executed only once before the start of the loop.

Here below is the implementation of the three stages.

.. literalinclude:: ../../src/mafw/examples/loop_modifier.py
    :linenos:
    :dedent:
    :pyobject: FindNPrimeNumber
    :start-at: def start(self) -> None:
    :end-at: log.info('The largest is %s', self.prime_num_found[-1])

Let us have a look at the :meth:`.FindNPrimeNumber.start`. First of all we set the value of :attr:`.Processor.n_item` to our target value of primes. We use the :attr:`.Processor.item` to store the current integer number being tested, so we initialize it to start_from or the first not prime odd number following it.
In the :meth:`.FindNPrimeNumber.process` we need to include another while loop, this time we need to check the current value of :attr:`.Processor.item` if it is a prime number. If yes, then we add it to the storage list, we increment it by two units (*remember that for while loop processors it is your responsibility to increment the loop parameters*) and we get ready for the next loop iteration. As for the other processor, we :meth:`.FindNPrimeNumber.finish` printing some statistics.

.. _importer:

Importing elements to the database
++++++++++++++++++++++++++++++++++

.. note::

    This example is using concepts that have not yet been introduced, in particular the database. So in a first instance, you can simply skip it and come back later.

Importing elements in the database is a very common task, that is required in all analytical projects. To accomplish this task, mafw is providing a dedicated base class (the :class:`~.Importer`) that heavily relies on the use of the :class:`~.FilenameParser` to extract parameters from the filenames.

The :class:`~.ImporterExample` is a concrete implementation of the base Importer that can be used by the user to get inspiration in the development of their importer subclass.

Before diving into the :class:`~.ImporterExample` code analysis, we should understand the role and the functionality of other two helper classes: the :class:`~.FilenameElement` and the :class:`~.FilenameParser`.

Retrieving information from filenames
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When setting up an experimental plan involving the acquisition of several data files, there are different approaches.

    #. The **descriptive** approach, where the filename is used to store information about the measurement itself,
    #. the **metadata** approach, where the same information are stored inside the file in a metadata section,
    #. or the **logbook** approach, where the filename is just a unique identifier and the measurement information are stored in a logbook (another file, database, piece of paper...) using the same unique identifier.

The **descriptive** approach, despite being sometime a bit messy because it may end up with very long filenames, it is actually very practical. You do not need to be a hacker including the metadata in the file itself and you do not risk to forget to add the parameters to the logbook.

The tricky part is to include those information to the database containing all your experiments, and you do not want to do this by hand to avoid errors.

The best way is to use `regular expression <https://docs.python.org/3/library/re.html#module-re>`_ that is a subject in which python is performing excellently and MAFw is helping you with two helpers.

The first helper is the :class:`~.FilenameElement`. This represents one single piece of information that is stored in the filename.

Let us assuming that you have a file named as ``sample_12_energy_10_repetition_2.dat``. You can immediately spot that there are three different pieces of information stored in the filename. The sample name, the value of the energy in some unit that you should known, and the value of the repetition. Very likely there is also a repetition_1 file saved on disc.

In order to properly interpret the information stored in the filename, we need to define three :class:`~.FilenameElement` s, one for each of them!

If you look at the documentation of the :class:`~.FilenameElement`, you will see that you need four arguments to build it:

    * its **name**, this is easy. Take one, and use it to name a named group in the regular expression.
    * its **regular expression**, this is tricky. This is the pattern that python is using to read and parse the actual element.
    * its **type**, this is the expected type for the element. It can be a string, an integer or a floating point number.
    * its **default** value, this is used to make the element optional. It means that if the element is not found, then the default value is returned. If no default value is provided and the element is not found then an error is raised.

Let us see how you could use :class:`~.FilenameElement` class to parse the example filename.

.. code-block:: python

    filename = 'sample_12_energy_10_repetition_2.dat'

    sample = FilenameElement('sample', r'[_]*(?P<sample>sample_\d+)[_]*', value_type=str)
    energy = FilenameElement('energy', r'[_]*energy_(?P<energy>\d+\.*\d*)[_]*', value_type=float)
    repetition = FilenameElement(
        'repetition', r'[_]*repetition_(?P<repetition>\d+)[_]*', value_type=int, default_value=1
    )

    sample.search(filename)
    assert sample.value == 'sample_12'

    energy.search(filename)
    assert energy.value == 10

    repetition.search(filename)
    assert repetition.value == 2

The interesting thing is that you can swap the position of the elements in the filename, for example starting with the energy, and it will still be working absolutely fine.

Just open a python interpreter, import the FilenameElement class and give it a try yourself to familiarize with the regular expression. Be careful, when you write the regular expression pattern, since it usually contains a lot of '\\', it may be useful to prefix the string with a r, in order to inform python that what is coming must be interpreted as a raw string.

If you want to gain confidence with regular expressions, make some tests and understand their power, we recommend to play around with one of the many online tools available on the web, like `pythex <https://pythex.org/>`_.

The :class:`~.FilenameElement` is already very helpful, but if you have several elements in the filename, the readability of your code will quickly degrade.
To help you further, you can enjoy the :class:`~.FilenameParser`.

This is actually a combination of filename elements and when you will try to interpret the filename by invoking :meth:`~.FilenameParser.interpret` all of the filename elements will be parsed and thus you can retrieve all parameters in a much easier way.

If you look at the :class:`~.FilenameParser` documentation, you will see that you need a configuration file to build an instance of it. This configuration file is actually containing the information to build all the filename element.

In the two tabs here below you can see the configuration file and the python code.

.. tab-set::

    .. tab-item:: Parser configuration

        .. code-block:: toml
            :name: example_conf.toml

            # FilenameParser configuration file
            #
            # General idea:
            #
            # The file contains the information required to build all the FilenameElement requested by the importer.
            #
            # Prepare a table for each element and in each table add the regexp, the type and optionally the default.
            # Adding the default field, will make the element optional.
            #
            # Add the table name in the elements array. The order is irrelevant. The division in compulsory and optional elements
            # is also irrelevant. It is provided here just for the sake of clarity.
            #
            # You can have as many element tables as you like, but only the one listed in the elements array will be used to
            # configure the Importer.
            #
            elements = [
                # compulsory elements:
                'sample', 'energy',
                # optional elements:
                'repetition'
            ]


            [sample]
            regexp = '[_]*(?P<sample>sample_\d+)[_]*'
            type='str'

            [energy]
            regexp = '[_]*energy_(?P<energy>\d+\.*\d*)[_]*'
            type='float'

            [repetition]
            regexp = '[_]*repetition_(?P<repetition>\d+)[_]*'
            type='int'
            default = 1

    .. tab-item:: Python test code

        .. code-block:: python
            :name: filename_parser.py

            filename = 'energy_10.3_sample_12.dat'

            parser = FilenameParser('example_conf.toml')
            parser.interpret(filename)

            assert parser.get_element_value('sample') == 'sample_12'
            assert parser.get_element_value('energy') == 10.3
            assert parser.get_element_value('repetition') == 1

The configuration file must contain a top level ``elements`` array with the name of all the filename elements that are included into the filename. For each value in ``elements``, there must be a dedicated table with the same name containing the definition of the regular expression, the type and optionally the default value.

.. important::
    In TOML configuration files, the use of single quotation marks allows to treat a string as a raw string, that is very important when passing expression containing backslashes. If you prefer to use double quotation marks, then you have to escape all backslashes.

The order of the elements in the ``elements`` array is irrelevant and also the fact we have divided them in compulsory and optional is just for the sake of clarity.

In the python tab, you can see how the use of :class:`~.FilenameParser` makes your code looking much tidier and easier to read. In this second example, we have removed the optional specification of the ``repetition`` element and you can see that the parser is returning the default value of 1 for such element and we have swapped the energy field with the sample name. Moreover, now the energy field is actually a floating number with a decimal figure.

The basic importer
~~~~~~~~~~~~~~~~~~

With the power of these two helper classes, building a processor for parsing all our measurement filenames is a piece of a cake. In the :mod:`~.processor_library` package, you can find a basic implementation of a generic :class:`~.Importer` processor, that you can use as a base class for your specific importer.

The idea behind this importer is that you are interested in files inside an ``input_folder`` and possibly all its subfolders. You can force the processor to look recursively in all subfolder by turning the processor parameter ``recursive`` to True. The last parameter of this processor is the ``parser_configuration`` that is the path to the :class:`~.FilenameParser` configuration file.

This configuration file is used during the :meth:`~.Importer.start` method of :class:`~.Importer` (or any of its subclasses) to configure its :class:`~.FilenameParser`, so that you do not have to worry of this step. In your subclass process method, the filename parser will be straight away ready to use.

Let us have a loop and the :class:`~.ImporterExample` processor (available in the :mod:`~.examples` package) for a concrete implementation of an importer processor.

The ImportExample processor
~~~~~~~~~~~~~~~~~~~~~~~~~~~

We will build a subclass of the :class:`~.Importer` processor following the *for_loop* execution workflow.

In the :meth:`~.ImporterExample.start` method, we will assure that the target table in the database is existing. The definition of the target database Model (:class:`~.importer_example.InputElement` in this example) should be done in a separate database model module to facilitate import statements from other modules as well.

.. code-block:: python

    class InputElement(MAFwBaseModel):
        """A model to store the input elements"""

        element_id = AutoField(primary_key=True, help_text='Primary key for the input element table')
        filename = FileNameField(unique=True, checksum_field='checksum', help_text='The filename of the element')
        checksum = FileChecksumField(help_text='The checksum of the element file')
        sample = TextField(help_text='The sample name')
        exposure = FloatField(help_text='The exposure time in hours')
        resolution = IntegerField(default=25, help_text='The readout resolution in µm')


.. literalinclude:: ../../src/mafw/examples/importer_example.py
    :dedent:
    :pyobject: ImporterExample
    :start-at: def start(self) -> None:
    :end-at: self.database.create_tables([InputElement])

In the :meth:`~.ImporterExample.get_items`, we create a list of all files, in this case matching the fact that the extension is `.tif`, included in the ``input_folder``. We use the ``recursive`` flag to decide if we want to include also all subfolders.

The :ref:`steering <gen_steering>` file may contain a GlobalFilter section (see :ref:`the Filter section <filters>`) and we use the new_only flag of the filter_register, to further filter the input list from all files that have been already included in the database. It is also important to check that the table is update because you may have an entry pointing to the same filename that in the mean time has been modified. For this purpose the :func:`~.verify_checksum` can be very useful.
A more detailed explanation of this function will be presented in a :ref:`subsequent section <verify_checksum>`.

.. literalinclude:: ../../src/mafw/examples/importer_example.py
    :dedent:
    :pyobject: ImporterExample
    :start-at:     def get_items(self) -> Collection[Any]:
    :end-at:         return file_list

The :class:`~.ImporterExample` follows an implementation approach that tries to maximise the efficiency of the database transaction. It means that instead of making one transaction for each element to be added to the database, all elements are collected inside a list and then transferred to the database with a cumulative transaction at the end of the process itself. This approach, as said, is very efficient from the database point of view, but it can be a bit more demanding from the memory point of view. The best approach depends on the typical number of items to be added for each run and the size of each element.

The implementation of the :meth:`~.ImporterExample.process` is rather simple and as you can see from the source code it is retrieving the parameter values encoded in the filename via the :class:`~.FilenameParser`. If you are wondering why we have assigned the filename to the filename and to the checksum field, have a look at the section about :ref:`custom fields <mafw_fields>`.

.. literalinclude:: ../../src/mafw/examples/importer_example.py
    :dedent:
    :pyobject: ImporterExample
    :start-at:     def process(self):
    :end-at:         self.looping_status = LoopingStatus.Skip

The :meth:`~.ImporterExample.finish` is where the real database transaction is occurring. All the elements have been collected into a list, so we can use an insert_many statement to transfer them all to the corresponding model in the database. Since we have declared the filename field as unique (this was our implementation decision, but the user is free to relax this requirement), we have added a ``on_conflict`` clause to deal with the case the user is updating an entry with the same filename.

Since the :meth:`super method <.Processor.finish>` is printing the execution statistics, we are leaving its call at the end of the implementation.

.. literalinclude:: ../../src/mafw/examples/importer_example.py
    :dedent:
    :pyobject: ImporterExample
    :start-at: def finish(self) -> None:
    :end-at: super().finish()