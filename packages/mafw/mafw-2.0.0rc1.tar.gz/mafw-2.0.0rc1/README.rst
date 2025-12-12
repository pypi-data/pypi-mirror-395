MAFw: Modular Analysis Framework
================================
A software library for scientists written by scientists!

.. image:: https://code.europa.eu/kada/mafw/badges/main/pipeline.svg
   :target: https://code.europa.eu/kada/mafw/-/pipelines
   :alt: Pipeline Status

.. image:: https://code.europa.eu/kada/mafw/badges/main/coverage.svg 
   :target: https://code.europa.eu/kada/mafw/-/commits/main 
   :alt: coverage report

.. image:: https://code.europa.eu/kada/mafw/-/badges/release.svg 
   :target: https://code.europa.eu/kada/mafw/-/releases 
   :alt: Latest Release

.. image:: https://joss.theoj.org/papers/10.21105/joss.08449/status.svg
   :target: https://doi.org/10.21105/joss.08449
   :alt: JOSS paper

Description
-----------
Modular Analysis Framework is a python tool to run analytical steps in a consistent manner and to generate suitable output graphs and tables.

The idea behind MAFw is to offer data scientists a framework where they will be able to implement complex analytical tasks in a well defined environment where they can focus only on the data analysis without bothering with all other ancillary things, like interfaces to database, job submission and so on.

The core of MAFw is the **Processor**, the class that is responsible to perform the analytical task. The Processor I/O is based on a strong collaboration between a relational database structure and files on disc.
In general, the processor is gathering the relevant input from one or more DB tables (location of input files, processing parameters...), performing its analytical job and update a DB output table with the main outcomes including the location where the output files are saved on disc.

By inheriting from the base Processor class, user-developed processors will come with some *superpowers*, like the ability to exchange data with the database back-end, displaying progress to the user, generating output graphs and so on. The scientist tasks will be limited to the implementation of the analysis code.

Once the data scientists have created their processor libraries, they will be able to chain them one after the other in a very simple way inside a so-called *steering file* and MAFw will take care to run them.

A full documentation of the library API along with a general description is available `here <https://mafw-e8abfd.pages.code.europa.eu/doc>`_.

Installation
------------
MAFw can be installed using pip in a separated virtual environment.

On Windows, you can do:

.. code-block:: doscon

    D:\mafw>python -m venv mafw-env
    D:\mafw>cd mafw-env
    D:\mafw\mafw-env>Scripts\activate
    (mafw-env) D:\mafw\mafw-env>pip install mafw

Similarly, on linux or MacOS, follow these instructions:

.. code-block:: bash

    $ python -m venv mafw-env
    $ cd mafw-env
    $ source bin/activate
    (mafw-env) $ pip install mafw

MAFw dependencies will be automatically installed by pip.

Requirements
++++++++++++

MAFw has been developed using python version 3.11 and tested with newer versions up to the current stable release (3.
13). Apart from some *typing* issues, we do not expect problems when running it with older releases. It is our
intention to follow the future advancement of python and possibly use the NO-GIL option starting from version 3.14 to improve the overall performances.

Concerning dependencies, all packages required by MAFw are specified in the pyproject file and will be automatically installed by pip. Nevertheless, if you are curious to know what comes with MAFw, here is a list of direct dependencies with the indication of what their role is inside the library.

    - **pluggy** (>=1.5): to implement the plugin mechanism and let the users develop their own processors;
    - **click** (>=8.1): to implement the command line interface for the mafw execution engine;
    - **tomlkit** (>0.13): to implement the reading and writing of steering files;
    - **peewee** (>3.17): to implement the ORM database interface;
    - **Deprecated** (>1.2): to inform the user about deprecated usages;
    - **typing-extensions** (>4.13 only for python <=3.11) to have access to typing annotations.

If mafw is installed with the additional features provided with by **seaborn**, then those packages will also be installed.

    - **seaborn** (>=0.13): to implement the generation of high level graphical outputs;
    - **matplotlib** (>=3.1): the low level graphics interface;
    - **pandas[hdf5]** (>=2.2): to allow the use of dataframes for data manipulations.

Usage
-----

The project's documentation is available `here <https://mafw-e8abfd.pages.code.europa.eu/doc>`_ also as a `PDF file <https://mafw-e8abfd.pages.code.europa.eu/doc/mafw.pdf>`_.

Contributing
------------
Contributions to the software development are very much welcome. Contributions to the software development are very much welcome. A more detailed guide on how to contribute or to get help for the development of your processors can be found in `CONTRIBUTING.md <https://code.europa.eu/kada/mafw/-/blob/main/CONTRIBUTING.md>`__.

If you want to join the developer efforts, the best way is to clone/fork this repository on your system and start working.

For the sake of simplicity, the following commands are shown as if they were typed from a Windows system. They are
substantially the same also in the case of a linux or MacOS shell, with the main difference being the way the prompt is
displayed.

The development team has adopted `hatch <https://hatch.pypa.io/latest/>`_ for basic tasks. So, once you have downloaded
the git repository to your system, open a shell there and type:

.. code-block:: doscon

    D:\mafw> hatch env create dev
    D:\mafw> hatch env find dev
    C:\path\to\.venv\mafw\KVhWIDtq\dev.py3.11
    C:\path\to\.venv\mafw\KVhWIDtq\dev.py3.12
    C:\path\to\.venv\mafw\KVhWIDtq\dev.py3.13

to generate the python environments for the development. This command will actually create the whole environment matrix,
that means one environment for each supported python version. If you intend to work primarily with one single python
version, simply specify it in the create command, for example:

.. code-block:: doscon

    D:\mafw> hatch env create dev.py3.13
    D:\mafw> hatch env find dev.py3.13
    C:\path\to\.venv\mafw\KVhWIDtq\dev.py3.13


hatch will take care of installing MAFw in development mode with all the required dependencies. Use the output of the
find command, if you want to add the same virtual environment to your favorite IDE.
Once done, you can spawn a shell in the development environment just be typing:

.. code-block:: doscon

    D:\mafw> hatch shell dev.py3.13
    (dev.py3.13) D:\mafw>

and from there you can simply run mafw and all other scripts.

.. note::

    If you are not familiar hatch, we strongly encorage to have a look at their `website <https://hatch.pypa.io/latest/>`__. This powerful tool, similar to `poetry <https://python-poetry.org/>`__ and `uv <https://docs.astral.sh/uv/>`__, it is simplifying the creation of a matrix of virtual
    environments for developing and testing your code with different combination of requirements.

    We strongly recommend to install hatch via `pipx <https://pipx.pypa.io/stable/>`__, so to have the executable available systemwide, but nevertheless running in a separate environment.


MAFw uses `pre-commit <https://pre-commit.com/>`_ to assure a high quality code. The pre-commit package will be
automatically installed into your environment, but it needs to be initialised before first use. So just enter:

.. code-block:: doscon

    (dev.py3.13) D:\mafw> pre-commit install

And now you are really ready to go with your coding!

Before pushing all your commits to the remote branch, we encourage you to run the pre-push tests to be sure that
everything still works as expected. You can do this by typing:

.. code-block:: doscon

    D:\mafw> hatch run dev.py3.13:pre-push


if you are not in an activated development shell, or

.. code-block:: doscon

    (dev.py3.13) D:\mafw> hatch run pre-push

if you are already in the dev environment.

Testing
-------

MAFw comes with an extensive unit test suite of more than 1000 test cases for an overall code coverage of 99%.

Tests have been coded using `pytest <https://docs.pytest.org/en/stable/>`__ best practice and are aiming to prove the
functionality of each unit of code taken individually. Given the high level of interoperability of MAFw with other
libraries (toml, peewee and seaborn just to name a few), unit tests rely heavily on patched objects to assure
reproducibility.

Nevertheless full integration tests are also included in the test suite. These tests will cover all relevant aspects of
MAFw, including:

1. Installation of MAFw and of a Plugin project in a isolated environment
2. Use of MAFw executable to create some data files and analyse them to create a graphical output.
3. Use of a database to store the collected data.
4. Check the database trigger functionalities to avoid repeating useless analysis steps, for example when a new file is
   added, removed or changed.

If you plan to collaborate in the development of MAFw, you must include unit tests for your contributions.

As already mentioned, MAFw is using hatch as project management. In the pyproject.toml file, hatch is configured to have
a matrix of test environment in order to run the whole test suite with the supported version of pythons
(3.11, 3.12 and 3.13).

**Running the suite is very easy**. Navigate to the folder where you have your local copy of MAFw and type ``hatch test``.
Hatch will take care of installing the proper environment and run the tests. Should one or more test(s) fail, then the
slow integration tests will be skipped to spare some time.

Have a look at the hatch test options, in particular the `-a`, to test over all the environments in the matrix and the `-c`
to generate coverage data for the production of a coverage report.

Authors and acknowledgment
---------------------------
`Antonio Bulgheroni <mailto:antonio.bulgheroni@ec.europa.eu>`__
`Michael Krachler <mailto:michael.krachler@ec.europa.eu>`__

License
-------
This software is licensed under EUPL 1.2

Project status
--------------
Ready to crunch some data! Open for contributions.

Citing MAFw
-----------

If you used MAFw in your research and you would like to acknoledge the project in your academic publication we suggest citing the following paper:

    - Bulgheroni et al., (2025). MAFw: A Modular Analysis Framework for Streamlining and Optimizing Data Analysis Workflows. Journal of Open Source Software, 10(114), 8449, https://doi.org/10.21105/joss.08449

or as BibTeX format:

.. code-block:: bibtex

    @article{Bulgheroni2025,
        doi = {10.21105/joss.08449},
        url = {https://doi.org/10.21105/joss.08449},
        year = {2025},
        publisher = {The Open Journal},
        volume = {10},
        number = {114},
        pages = {8449},
        author = {Bulgheroni, Antonio and Krachler, Michael},
        title = {MAFw: A Modular Analysis Framework for Streamlining and Optimizing Data Analysis Workflows},
        journal = {Journal of Open Source Software}
    }

