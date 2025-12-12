.. include:: substitutions.rst

.. _doc_processor:

Processor: The core of MAFw
===========================

The Processor is responsible to carry out a specific analytical task, in other simple words, it takes some input data, it does some calculations or manipulations, and it produces some output data.

The input and output data can be of any type: a simple list of numbers, a structured data frame, a path to a file where data are stored, an output graph or a link to a web resource, a database table, and so on.

In ultra simplified words, a Processor does three sequential actions:

#. Prepare the conditions to operate (:meth:`~mafw.processor.Processor.start`)
#. Process the data (:meth:`~mafw.processor.Processor.process`)
#. Clean up what is left (:meth:`~mafw.processor.Processor.finish`).

.. _execution_workflow:

Execution workflow
------------------

There are instances where tasks can be executed in a single operation across your entire dataset, such as generating a graph from the data. However, there are also situations where you need to iterate over a list of similar items, applying the same process repeatedly. Additionally, you may need to continue a process until a specific condition is met. The |processor| can actually accomplish all those different execution workflows just by changing a variable: :class:`the loop type <mafw.enumerators.LoopType>`.

You will be presented a more detailed description of the different workflows in the following sections.

The single loop execution
+++++++++++++++++++++++++

The first family has a simplified execution workflow schematically shown here below:

.. image:: /_static/graphviz/single_shot.png
    :name: single_loop
    :align: center
    :width: 400px

The distinction of roles between the three methods is purely academic, one could implement all the preparation, the real calculation and the clean up in one method and the processor will work in the same way. The methods are anyhow preserved to offer a similar execution scheme also for the other looping scheme.


The for loop execution
+++++++++++++++++++++++

In python a for loop is generally performed on a list of items and MAFw is actually following the same strategy. Here below is the schematic workflow.


.. image:: /_static/graphviz/for_loop.png
    :name: looper
    :align: center
    :width: 400px

As you can see, after having called the :meth:`~mafw.processor.Processor.start`, the user must provide a list of items to be processed implementing the :meth:`~mafw.processor.Processor.get_items`. This can be the list of files in a directory, or the rows in a DB table or even a list of simple numbers; whatever best suit the user's needs. You will soon learn how to deal with :ref:`database <database>` entries and how to :ref:`filter <filters>` them.

Now everything is ready to start the loop and call the :meth:`~mafw.processor.Processor.process` as many times as the items in the input list. In the process implementation, the user can realize that something went wrong with a particular item and can modify what is executed next (:meth:`~mafw.processor.Processor.accept_item` or :meth:`~mafw.processor.Processor.skip_item`). See an example of such a possibility :ref:`here <mod_loop>`.
At the end of the loop it is time to clean up everything, saving files, updating DBs and so one. This is again the task of the :meth:`~mafw.processor.Processor.finish` method.

The while loop execution
++++++++++++++++++++++++

From a programming point of view, the for loop and the while loop execution are rather similar. Between the execution of the start and the finish method, the process is repeated for a certain number of times until a certain condition is met.

.. image:: /_static/graphviz/while_loop.png
    :name: while_loop
    :align: center
    :width: 600px

In this case, there is no list of items to loop over, but a condition that should be checked. Thus the user has to overload the :meth:`~mafw.processor.Processor.while_condition` method to return a boolean value: True if the loop has to continue or False if it has to stop and go to the finish.

How to switch from one loop type to another
+++++++++++++++++++++++++++++++++++++++++++

It is extremely simple to switch from one execution scheme to another. The |processor| class takes the argument :attr:`~mafw.processor.Processor.loop_type`, just change this value in the processor init and the rest will come automatically.

Remember that, by default a processor is set to work with a *for loop* workflow, and thus you have to implement the :meth:`~mafw.processor.Processor.get_items`. If you switch to *while loop*, then you need to implement :meth:`~mafw.processor.Processor.while_condition` for the system to work.


The last thing, you need to know is how to run a processor. First you create an instance of your processor, then you call the :meth:`~mafw.processor.Processor.execute` method. There are other more practical ways, not involving any coding that we will discuss :ref:`later on <doc_runner>`.

A comparison between the **for loop** and the **while loop** execution workflow is described in the :ref:`example page <for_and_while>`.

Subclassing
-----------

The basic processor provided in the library does nothing specifically, it is only used as a skeleton for the execution. In order to
perform some real analysis, the user has to subclass it and overload some methods. Having gained a clear understanding of the role of each steps in the execution workflow, read the list of methods that can be overloaded here below and then you are ready to see some simple :ref:`examples`.

List of methods to be overloaded
++++++++++++++++++++++++++++++++

The :meth:`~mafw.processor.Processor.process` method.

    This is the central part of the processor, and it must contain all the calculations. If the
    processor is looping on a list of input items, the user can access the current item via the :attr:`~mafw.processor.Processor.item`
    attribute.

The :meth:`~mafw.processor.Processor.start` method.

    This is useful to prepare the condition to operate. For example, it is a good idea to open files and do all
    the preparatory work. In a looping processor, this method is called just before the cycle starts.

The :meth:`~mafw.processor.Processor.finish` method.

    This is useful to clean up after the work. For example, to save files, update DB tables and so on. In a
    looping processor this is performed just after the last iteration. Here is also the place where you can set the
    value of the :class:`~.ProcessorExitStatus`. This attribute is particularly relevant when several processors are
    executed in a daisy-chained manner. See more about this :ref:`here <exit_status>` and :ref:`here <exit_code>`.

Specifically for processors with a looping workflow, these methods need to be subclassed.

The :meth:`~mafw.processor.Processor.get_items` method.

    This is where the input collection of items is generated. Very likely this can be a list of files resulting from a
    glob or the rows of an input table or similar. This is required only for **for_loop** processors and must return an
    iterable object.

The :meth:`~mafw.processor.Processor.while_condition` method.

    This is the point at which the decision is made to either continue or terminate the loop. This is required only for **while_loop**
    processors and must return a boolean value.

The :meth:`~mafw.processor.Processor.accept_item` and :meth:`~mafw.processor.Processor.skip_item` methods (optional).

    The execution of the for loop can be slightly modified using the :class:`~mafw.enumerators.LoopingStatus` (see this
    :ref:`example <mod_loop>`). If the current iteration was successful, then the user can decide to perform some
    actions, otherwise if the current iteration was failing, then some other actions can be taken.

The :meth:`~mafw.processor.Processor.format_progress_message` (optional).

    During the process execution, your console may look frozen because your CPU is working out your analysis, thus it may
    be relevant to have every now and then an update on the progress. The |processor| will automatically display regular messages via the
    logging system about the progress (more or less every 10% of the total number of items), but the
    message it is using is rather generic and does not contain any information about the current item.

    By overloading this method, you can include information about the current item and customize the content of the
    message. You can use :attr:`~mafw.processor.Processor.item` to refer to the current item being processed. Here below
    is an example:

    .. code-block:: python

        def format_progress_message(self):
            self.progress_message = f'{self.name} is processing {self.item}'


    Be aware that if your items are objects without a good __repr__ or string conversion, the output may be a little
    messy.

The :meth:`~.Processor.validate_configuration` (optional).

    If your processor has several parameters, it might be a good idea that the configuration provided by the user via :class:`.ActiveParameter` is validated. For this purpose the user can subclass the :meth:`~.Processor.validate_configuration` method, where the validation of the configuration should silently take place. If the configuration is invalid, then the method should raise a :class:`.InvalidConfigurationError`. You will read more on processor parameters and how to use it in one of the next :ref:`section <parameters>`.

Customize and document you processor
++++++++++++++++++++++++++++++++++++

You are a scientist, we know, the only text you like to write is the manuscript with your last research results. Nevertheless, documenting your code, in particular your processor is a very helpful approach. We strongly recommend to use `docstring` to give a description of what a processor does. If you do so, you will get a surprise when you will :ref:`generate your first steering file <gen_steering>`.

It is also a very good practice to provide help/doc information to your parameters using the help_doc argument of the :class:`~mafw.processor.ActiveParameter`. If you do so, your :ref:`first steering file <gen_steering>` will be much more readable.

One more point, each |processor| has a class attribute named :attr:`~mafw.processor.Processor.description`, this is a short string that is used by some user interfaces (like :class:`~mafw.ui.rich_user_interface.RichInterface`) to make the progress bars more meaningful.



.. _parameters:

Processor parameters
--------------------

One super power of MAFw is its capability to re-use code, that means less work, less bugs and more efficiency.

In order to boost code re-usability, one should implement Processor accomplishing one single task and possibly doing it with a lot of general freedom. If you have a processor to calculate the Threshold of B/W images and you have hard coded the threshold algorithm and tomorrow you decide to give a try to another algorithm, then you have to recode a processor that actually already exists.

The solution is to have processor parameters, kind of variables that can be changed in order to make your processor more general and more useful. A note of caution, if you opt for too many parameters, then it may become too difficult to configure your processor. As always, the optimal solution often lies in finding a balance.

You can have parameters implemented in the processor subclass as normal attributes, but then you would need to modify the code in order to change them and this is far from being practical. You can have them as specific variables passed to the processor init, but then you would need to code the command line script to pass this value or to implement a way to read a configuration file.

MAFw has already done all this for you as long as you use the right way to declare processor parameters.

Let us start with a bit of code.

.. code-block:: python

    class MyProcessor(Processor):
        """
        This is my wonderful processor.

        It needs to know the folder where the input files are stored.
        Let us put this in a processor parameter.

        :param input_folder: The input folder.
        """
        input_folder = ActiveParameter(name='input_folder', default=Path.cwd(),
                                       help_doc='This is the input folder for the file')

        def __init__(self, *args, **kwargs):
            super().__init(*args, **kwargs)

            # change the input folder to something else
            self.input_folder = Path(r'D:\data')

            # get the value of the parameter
            print(self.input_folder)


Some important notes: input_folder is defined as a class attribute rather then as an instance attribute, it is to say it is outside the init method. **This must always be the case for processor parameters**. The fact that the variable and the parameter names are the same is not compulsory, but why do you want to make your life more complicated!

We have declared `input_folder` as an :class:`~mafw.processor.ActiveParameter`, but if you put a break point in the code execution and you inspect the type of `self.input_folder` you will see that it is a Path object. This is because :class:`~mafw.processor.ActiveParameter` is a `descriptor <https://docs.python.org/3/glossary.html#term-descriptor>`_, a very pythonic way to have a double interface for one single variable.

If your processor is subclassing the `__init__` method, then never forget to include right at the beginning a call to its super, this is ensuring that the processor, and its parameters, are properly initialized and ready to be used.


What's behind an :class:`~mafw.processor.ActiveParameter`
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. note::

    This is a very technical paragraph, you can skip it if you are not interested in the *behind the scene* of processor parameters.

Have a look at the code in the previous snippet. When you define `input_folder`, you use up to four parameters in the :class:`~mafw.processor.ActiveParameter` init, but if you try to access those attributes from input_folder you will get an error message, because class Path does not have the attributes you are looking for. Where are then those values gone?

When you create an :class:`~mafw.processor.ActiveParameter`, there is a lot of work behind the scene: each processor instance has a dictionary (:attr:`.Processor._processor_parameters`) where the parameter name is used as a key and the corresponding value is an instance of :class:`.PassiveParameter`. This helper class has a very similar structure as the active counter part and it is used to store the current value of the parameter and all its metadata (default value and help string) defined when the active parameter was created.

The set and get dunder methods of the input_file are overloaded to operate directly on the private interface, more or less in the same way like when you define `property` setter and getter, but here it is done all automatically.

If you want to access the private interface, you can still do it. You can always use the processor :meth:`~mafw.processor.Processor.get_parameter` using the parameter name as a key, to retrieve the :class:`.PassiveParameter` instance. Theoretically you can even set the value of the parameter using the private interface (:meth:`~mafw.processor.Processor.set_parameter_value`), but this is equivalent to set it via the public interface directly.

Let us summarize all this with an example:

.. testcode::

    from mafw.processor import Processor, ActiveParameter

    class MyFavProcessor(Processor):
        useful_param = ActiveParameter('useful_param', default=0, help_doc='Important parameter')

    # create your processor, initialize the parameter with a keyword argument.
    my_fav = MyFavProcessor(useful_param=10)

    # print the value of useful_param in all possible ways
    print(my_fav.useful_param)
    print(my_fav.get_parameter('useful_param').value)

    # change the value of useful_param in all possible ways
    my_fav.useful_param += 1
    my_fav.get_parameter('useful_param').value += 1

    print(my_fav.useful_param)

    # access other fields of the parameter
    print(my_fav.get_parameter('useful_param').doc)

This is the output that will be generated:

.. testoutput::

    10
    10
    12
    Important parameter

Parameter configuration
+++++++++++++++++++++++

We have seen how to add flexibility to a processor including parameters, but how do you configure the parameters?

You have probably noticed that :class:`~mafw.processor.ActiveParameter` has the possibility to pass a default value, that is a very good practice, especially for very advanced parameters that will remain untouched most of the time.

If you want to set a value for a parameter, the easiest way is via the processor `__init__` method. The basic Processor accepts any number of keyword arguments that can be used exactly for this purpose. Just add a keyword argument named after the parameter and the processor will take care of the rest.

Have a look at the example below covering both the case of Active and Passive parameters:

.. code-block:: python
    :linenos:
    :name: parameter_keyword
    :caption: Parameter setting via kwargs

    class MyProcessor(Processor):
        active_param = ActiveParameter('value', default=0, help_doc='An active parameter')
        active_string = ActiveParameter('string', default=0, help_doc='An active parameter')

    my_p = MyProcessor(value=100, string='a better string', looper='single')

    print(my_p.active_param)  # we get 100
    assert my_p.active_param == 100

    print(my_p.active_string)  # we get 'a better string'
    assert my_p.active_string == 'a better string'

Note that the best way is to avoid to explicitly include the parameter names in the init signature. They will be collected anyhow through keyword arguments and registered automatically.

The second approach is to use a configuration object, it is to say a dictionary containing all the parameters key and value pairs. This is particularly handy when using a configuration file. Exactly for this reason, the configuration object can have one of the two following structures.
In both cases the configuration object has to be passed to the class using the keyword `config`

.. code-block:: python
    :linenos:
    :name: parameter_configuration
    :caption: Parameter setting via configuration object

    @single_loop
    class ConfigProcessor(Processor):
        p1 = ActiveParameter('param1', default='value')
        p2 = ActiveParameter('param2', default='value')


    cp = ConfigProcessor(config=dict(param1='new_value', param2='better_value', param3='do not exists'))
    assert cp.p1 == 'new_value'
    assert cp.p2 == 'better_value'
    dumped_config = cp.dump_parameter_configuration(option=2)
    assert dumped_config == dict(param1='new_value', param2='better_value')

    config = {'ConfigProcessor': {'param1': '1st', 'param2': '2nd'}}
    cp = ConfigProcessor(config=config)
    assert cp.p1 == '1st'
    assert cp.p2 == '2nd'
    dumped_config = cp.dump_parameter_configuration()
    assert config == dumped_config

.. note::

    **Migration from MAFw v1 to v2**

    If you were using MAFw already in its early day of version 1, you might remember that users could also use :class:`.PassiveParameter` directly as processor parameters. They had the disadvantage of requiring the dot notation (`.value`) to access the data member, but everything else was identical to an :class:`.ActiveParameter`. This was a consequence of the implementation of the old parameter initialisation. This procedure has been totally reviewed in version 2 and now there is no need anymore to use :class:`.PassiveParameter`. On the contrary, the user is recommended not to use :class:`.PassiveParameter`, but only their active counterpart.

.. _parameter_dump:

Saving parameter configuration
++++++++++++++++++++++++++++++

We have seen that we can configure processor using a dictionary with parameter / value pairs. This is very handy, because we can load toml file with the configuration to be used for all the processors we want to execute.

We don't want you to write toml file by hand, for this we have a function :func:`~mafw.tools.toml_tools.dump_processor_parameters_to_toml` that will generate an output file with all the parameter values.

But which value is stored? The default or the actual one? Good question! The actual answer is: *it depends*!

Let us have a look at the following example.

.. code-block:: python
    :name: definition
    :caption: Processors definition

    from mafw.processor import ActiveParameter, PassiveParameter

    class ActiveParameterProcessor(Processor):
        """A processor with one active parameter."""

        active_param = ActiveParameter('active_param', default=-1,
                                       help_doc='An active parameter with default value -1')


    class AnotherActiveParameterProcessor(Processor):
        """Another processor with one active parameter."""

        active_param = ActiveParameter('active_param', default=-1,
                                       help_doc='An active parameter with default value -1')



We have defined two different processors with one parameter each.

Now let us have a look at what happens when we attempt to dump the configuration of these processors.

.. code-block:: python
    :name: example1
    :caption: Case 1: all processor types

    processor_list = [ActiveParameterProcessor, AnotherActiveParameterProcessor]

    dump_processor_parameters_to_toml(processor_list, 'test1.toml')


We have not created any instances of the two processors, and the processor_list consists of two classes. When passed to the :func:`~mafw.tools.toml_tools.dump_processor_parameters_to_toml` function, an instance of each class type is created and the parameter dictionary is retrieved. The creation of an instance is required because only after __init__ all parameters are registered.

Inside the function, the instances are created without passing any parameters, so it means that for all parameters the dumped value will be the initial value of the parameter, if specified, or the default value if a
value is not given in the parameter definition.

The output of the :ref:`first example <example1>` will show the two processors with their parameters listed and connected to their default values.

.. code-block:: toml
    :name: test1.toml
    :caption: Output of case 1: test1.toml

    [ActiveParameterProcessor] # A processor with one active parameter.
    active_param = -1 # An active parameter with default value -1

    [AnotherActiveParameterProcessor] # Another processor with one active parameter.
    active_param = -1 # An active parameter with default value -1

Now, let us take a step forward and add a bit more complexity to the situation. See the next snippet:

.. code-block:: python
    :name: example2
    :caption: Case 2: mixed instances and classes

    # create an instance of ActiveParameterProcessor with a specific value of the parameter
    # but we will include the class in the processor list.
    active_processor_instance = ActiveParameterProcessor(active_param=100)

    # create an instance of AnotherActiveParameterProcessor with a specific value of the parameter
    # and we will submit the instance
    another_active_processor_instance = AnotherActiveParameterProcessor(active_param=101)


    processor_list = [
        ActiveParameterProcessor,  # a class
        another_active_processor_instance,  # an instance
    ]
    dump_processor_parameters_to_toml(processor_list, 'test2.toml')


This time we have a mixed list, the first item is a class, so the function will have to create an instance of this. The new instance created inside the dumping function will not have any parameter initial value specified in the constructor, so it will dump the default value -1. For the second one, since we are passing a living instance, the dumping function will use the actual value of the parameter, in this case 101.


Here is the produced configuration file:

.. code-block:: toml
    :name: test2.toml
    :caption: Output of case 2: test2.toml

    [ActiveParameterProcessor] # A processor with one active parameter.
    active_param = -1 # An active parameter with default value -1

    [AnotherActiveParameterProcessor] # Another processor with one active parameter.
    active_param = 101 # An active parameter with default value -1

Ultimately, the values that will be output depends on the fact if you pass an instance of the processor or its class. But in the end, this is not really important because the user should dump TOML configuration files as a sort of template to be checked, modified and adapted by the user for a specific run.

.. _parameter_processor_inheritance:

Parameter and processor inheritance
+++++++++++++++++++++++++++++++++++

Parameters, like any other class attributes and methods, can be inherited via subclassing and this can turn out to be very useful. Imagine to have a full class of processors having some parameters in common (the most simple example is the base path for the produced output), then the user might consider to have an intermediate subclass between MAFw Processor and their final Processors defining all these common parameters.

Have a look at the example below:

.. code-block:: python
    :name: parameter_inheritance

    @single_loop
    class BaseProcessor(Processor):
        my_param = ActiveParameter('my_param', default=5, help_doc='An integer value')

    class SameDefaultProcessor(BaseProcessor):
        pass

    class OtherDefaultProcessor(BaseProcessor):
        new_defaults = {'my_param': 885}

    dump_processor_parameters_to_toml([BaseProcessor, SameDefaultProcessor, OtherDefaultProcessor], 'test.toml')


All processors have a parameter names `my_param`. Since the parameter has been defined only once (in the base processor), it is born with the same default value for all subclasses. But this can be changed setting the processor instance variable `new_defaults` as done in the OtherDefaultProcessor. In fact, the TOML configuration file is exactly showing this situation:

.. code-block:: toml

    [BaseProcessor]
    my_param = 5 # An integer value

    [SameDefaultProcessor]
    my_param = 5 # An integer value

    [OtherDefaultProcessor]
    my_param = 885 # An integer value

Parameter typing
++++++++++++++++

When creating an Active parameter, you have the option to directly specify the parameter's type using the typing template, but you can also do it, and probably in a simpler way assigning a reasonable default value. While this is not really important for numbers, it is extremely important if you want to interpret string as Path object.

If you declare the default value as a Path, for example Path.cwd(), then the string read from the configuration file will be automatically converted in a Path.

.. note::

    If you intend to have a float parameter, use a decimal number, for example 0., as default, otherwise the interpreter will assume it is an integer and convert to int the parameter being read from the configuration file.

One more note about parameters. Theoretically speaking you could also have custom objects / classes as parameters, but this will become a problem when you will be loading the parameters from a TOML file. Actually two problems:

    1. The TOML writer is not necessarily able to convert your custom type to a valid TOML type (number, string...). If your custom type has a relatively easy string representation then you can add an encoder to the TOML writer and teach it how to write your object. See for example the encoder for the Path object.

        .. literalinclude:: ../../src/mafw/tools/toml_tools.py
            :linenos:
            :name: toml_encoder
            :pyobject: path_encoder

    2. Even though you managed to write your class to the TOML steering file, you have now the problem of reading back the steering file information and build your custom type with that.

One way to overcome this limitation might be to write to the steering file the ``__repr__`` of your custom class and at read back time to use eval to transform it back to your class. This below would be a more concrete implementation:

.. tab-set::

    .. tab-item:: python

        .. code-block:: python
            :linenos:
            :name: eval_repr.py

            import tomlkit
            from tomlkit.items import  String, Item, ConvertError
            from tomlkit.toml_file import TOMLFile

            class MyClass:
                """A custom class to be used as a processor parameter"""
                def __init__(self, a, b):
                    self.a = a
                    self.b = b

                def __repr__(self):
                    """IT MUST BE IMPLEMENTED"""
                    return f"{self.__class__.__name__}({self.a}, {self.b})"

            class MyClassItem(String):
                """TOML item representing a MyClass"""
                def unwrap(self) -> MyClass:
                    return MyClass(*super().unwrap())

            def my_class_encoder(obj: MyClassItem) -> Item:
                """Encoder for MyClassItem."""
                if isinstance(obj, MyClass):
                    # we write the class as a string using the class repr.
                    return MyClassItem.from_raw(repr(obj))
                else:
                    raise ConvertError

            # register the encoder
            tomlkit.register_encoder(my_class_encoder)

            # ------------------
            # write to TOML file
            # ------------------

            my_class = MyClass(10,24)
            doc = tomlkit.document()
            doc.add('my_class', my_class)
            doc.add('simple_i', 15)

            with open('test.toml', 'w') as fd:
                tomlkit.dump(doc, fd)

            # ------------------------
            # read back from TOML file
            # ------------------------

            doc = TOMLFile('test.toml').read()
            read_back_class = eval(doc['my_class'])
            try:
                simple_i = eval(doc['simple_i'])
            except TypeError:
                simple_i = doc['simple_i']

            assert isinstance(read_back_class, MyClass)
            assert read_back_class.a == my_class.a

            assert isinstance(simple_i, int)
            assert simple_i == 15

    .. tab-item:: TOML

        .. code-block:: TOML

            my_class = "MyClass(10, 24)"
            simple_i = 15

This approach, even though possible, is rather risky, we all know how dangerous ``eval`` can be especially when using it directly with information coming from external files.
Furthermore, it is worth considering whether having a custom class as a parameter in a processor is truly necessary. Often, there are simpler and safer alternatives available.

What's next
-----------

You reached the end of the first part. It means that by now you have understood what a processor is and how you can subclass the basic class to implement your analytical tasks, both with looping or single shot workflow. You learned a lot about parameters and how you can configure it.

The next section will be about chaining more processors one after the other using the :class:`~mafw.processor.ProcessorList`.
