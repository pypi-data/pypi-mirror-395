.. include:: substitutions.rst

.. _plugins:

Plugins: import your processors
===============================

We are almost half-way through our tutorial on MAFw. We have learned what a |processor| is and how we can create our own processors just by subclassing the base class. With the |processor_list| we have seen an easy way to chain the execution of many processors. So by now, you might be tempted to open your IDE and start coding stuff... But please hold on your horses for another minute, MAFw has much more to offer.

In the previous pages of this tutorial, we always coded our |processors| and then executed them manually, either from the python console or via an ad-hoc script. This is already helpful, but not really practical, because everytime you want to change which |processors| are executed or one of their parameters, we need to change the script code. This seems very likely the job for a configuration file, doesn't it?

MAFw is providing you with exactly this capability, a generic script that will read your configuration file (**steering file** in the MAFw language) and execute it. Here comes the problem, *how can the execution framework load your* |processors| *since they are not living in the same library*?

To this problem there are two solutions: a quick and dirty and a clean and effective! Of course you will have the tendency to prefer the first one, but really consider the benefits of the second one before giving up reading!

The quick and dirty: code inside MAFw
-------------------------------------

When you install MAFw on your system, you can always do it in development mode (for ``pip`` this corresponds to the `-e` option). In this way, you will be allowed to code your |processors| library directly inside your locally installed MAFw.

It is very quick, because you can start coding right away, but it is also rather dirty, because it will be much harder to install MAFw updates and after a while the project will become too big and messy.

For these and many other reasons, we are convinced that this is not the right way to go.

The clean and effective: turn your library into a plugin
--------------------------------------------------------

It may seem more challenging than it actually is, but in reality, it is quite simple. MAFw uses the plugin system developed by `pluggy <https://pluggy.readthedocs.io/en/stable/>`_, that is very powerful and at the same time relatively easy to deploy.

After you have installed MAFw in your system (you can do it in development mode if you want to contribute!), create a new project to store your processor. How to create a project is well described in details `here <https://packaging.python.org/en/latest/tutorials/packaging-projects/>`_ with a step by step guide. You don't need to upload your package tp PyPI, you can stop as soon as you are able to build a wheel of your package and install it in a virtual environment.

To achieve this, you would need to have a `pyproject.toml` file, with the project metadata, the list of dependencies and other things.
Here below is an example of what you should have:

.. code-block:: toml
    :linenos:
    :name: ex_pyproject
    :caption: An example of pyproject.toml for a plugin
    :emphasize-lines: 40,41

    [build-system]
    requires = ["hatchling"]
    build-backend = "hatchling.build"

    [project]
    name = "fantastic_analysis"
    dynamic = ["version"]
    description = 'My processor library'
    readme = "README.md"
    requires-python = ">=3.8"
    license = "MIT"
    keywords = []
    authors = [
      { name = "Surname Name", email = "this.is.me@my.domain.com" },
    ]
    classifiers = [
      "Development Status :: 4 - Beta",
      "Programming Language :: Python",
      "Programming Language :: Python :: 3.8",
      "Programming Language :: Python :: 3.9",
      "Programming Language :: Python :: 3.10",
      "Programming Language :: Python :: 3.11",
      "Programming Language :: Python :: 3.12",
      "Programming Language :: Python :: Implementation :: CPython",
      "Programming Language :: Python :: Implementation :: PyPy",
    ]

    dependencies = ['mafw'] # plus all your other dependencies

    [project.urls]
    Documentation = "https://github.com/..."
    Issues = "https://github.com/..."
    Source = "https://github.com/."

    ## THIS IS THE KEY PART
    ## --------------------
    # you can add as many lines you want to the table.
    # always use unique names for the entry.

    [project.entry-points.'mafw']
    fantastic_analysis_plugin = 'fantastic_analysis.plugins'

    [tool.hatch.version]
    path = "src/fantastic_analysis/__about__.py"

Particularly important are lines 40 and 41. There you declare that when installed in an environment, your package is providing a plugin for MAFw, in particular this plugin that you named `fantastic_analysis_plugin` is located inside your package in a file named plugins.py.

So now, let us have a look at what do you have to have inside this file:

.. code-block:: python
    :linenos:
    :name: ex_plugins.py
    :caption: Example of plugins.py

    """
    This is the module that will be exposed via the entry point declaration.

    Make sure to have all processors that you need to export in the list.
    """

    import mafw
    from mafw.processor import Processor
    from fantastic_analysis import my_processor_lib

    @mafw.mafw_hookimpl
    def register_processors() -> list[mafw.processor.Processor]:
        return [my_processor_lib.Processor1, my_processor_lib.Processor2]


In this python file you need to import mafw in order to have access to the :attr:`~mafw.mafw_hookimpl` decorator. This is a marker for pluggy so that it knows that this function should return something for the host application. The second import statement is needed only for the typing of the return value. The third one is to import your library with the processors. It can be one or as many as you have.

Inside the returned list, just put all the processors you want to export and the trick is done!

Now install in development mode your package and MAFw will be able to access all your processor library, without you having to do anything else!

.. _lazy_import_processor:

Using a proxy instead of a real processor
+++++++++++++++++++++++++++++++++++++++++

Exporting all your processor is as easy as listing them in the `register_processors` hook. There is a limitation with this approach and it becomes clear as soon as you have many processors. Imagine to have a dozen of processors, each of them importing large modules (pandas, matplotlib, TensorFlow...). When MAFw will retrieve the processor list from your plugin, it will have to import your modules triggering the import of all other dependency. In other words, your calculation have not started yet and all the modules are imported, including the ones that are needed by processors that will not be executed!

The solution is to use a so-called *lazy proxy*, it is to say an object that will behave like the real processor class during the plugin discovery, but it will reify in the real processor when it is needed! If you are interested in the implementation, have a look at the proxy :mod:`API <.lazy_import>`.

The performance gain following this approach is really impressive and it cost you nothing. The code below is totally equivalent to the :ref:`previous one <ex_plugins.py>`, but faster!

.. code-block:: python
    :linenos:
    :name: proxy_plugins
    :caption: Example of plugins.py with proxy

    """
    This is the module that will be exposed via the entry point declaration.

    Make sure to have all processors that you need to export in the list.
    """
    import mafw
    from mafw.lazy_import import LazyImportProcessor, ProcessorClassProtocol

    @mafw.mafw_hookimpl
    def register_processors() -> list[ProcessorClassProtocol]:
        return [
            LazyImportProcessor('fantastic_analysis.my_processor_lib', 'Processor1'),
            LazyImportProcessor('fantastic_analysis.my_processor_lib', 'Processor2')
        ]

.. admonition:: Migration from MAFw v1.4
    :collapsible: open

    If you are migrating from v1.4 to v2, then you may have noticed that the plugin hook to export the standard tables has disappeared.

    If fact, the standard table plugin became useless with the introduction of the :class:`.ModelRegister`, where all database Models are stored automatically. The same applies to models inheriting to :class:`.StandardTable`, so you can easily retrieve them via the :class:`model register <.ModelRegister>`.

    Refer to these two other paragraphs: :ref:`auto_registration` and :ref:`std_tables`.


What's next
-----------

If you are still reading this tutorial, it means that you are aware of the benefits that MAFw can bring to your daily analysis task.
And the best part is, there is even more to discover! On the following section, you will discover how to efficiently manage your complex analytical process by simply listing all the sequential steps in a steering file.