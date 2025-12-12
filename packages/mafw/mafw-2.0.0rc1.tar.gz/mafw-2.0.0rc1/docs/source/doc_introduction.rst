.. include:: substitutions.rst

.. tip::

    **Reading Path Recommendation**: This documentation follows a systematic approach, describing all the elements
    composing MAFw and their interactions before presenting a comprehensive practical example. However, we recognize that
    different users have varying learning preferences. If you prefer to begin with a concrete implementation to
    understand the library's capabilities before diving into theoretical foundations, you may jump directly to the
    :ref:`tutorial section <tutorial_note>`. After reviewing the practical application, you can return to this detailed
    documentation for a thorough understanding of the underlying concepts and architectural design.


.. _introduction:

Introduction
============

Statement of need
-----------------

MAFw addresses the need for a flexible and modular framework that enables data scientists to implement complex analytical tasks in a well-defined environment. Currently, data analysis workflows often require scientists to handle multiple tasks, such as data ingestion, processing, and visualization, which can be time-consuming and prone to errors. Moreover, the lack of standardization in data analysis pipelines can lead to difficulties in reproducing and sharing results.

MAFw aims to fill this gap by providing a Python-based tool that allows data scientists to focus on the analysis itself, rather than on the ancillary tasks. The framework is designed to be highly customizable, enabling users to create their own processors and integrate them into the workflow. A key feature of MAFw is its strong collaboration with a relational database structure, which simplifies the analysis workflow by providing a centralized location for storing and retrieving data. This database integration enables seamless data exchange between different processors, making it easier to manage complex data pipelines.

MAFw conceptual design
-----------------------

The concept behind MAFw is certainly not novel. Its functionality is so prevalent in data analysis that numerous developers, particularly data scientists, have attempted to create libraries with similar capabilities. MAFw's developers got inspired by :link:`MARLIN`: this object C++ oriented application framework, no longer being maintained, was offering a modular environment where particle physicists were developing their code in the form of shared libraries that could be loaded at run time in a plugin-like manner [#]_. One of MARLIN strengths was the strong connection with the serial I/O persistency data model offered by :link:`LCIO`.

Starting from those solid foundations, MAFw moved from C++ to python in order to facilitate the on-boarding of data scientists and to profit from the vast availability of analytical tools, replacing the obsolete :link:`LCIO` backend with a more flexible database supported input/output able to deal with large amount of data with categorical variables without severely impacting on I/O performance.

The general concept behind MAFw has been developed by the authors to perform image analysis on `autoradiography images <https://www.sciencedirect.com/science/article/pii/S0026265X24015601>`_, featuring an ultra simplified database interface (:link:`sqlite` only) along with some dedicated processors targeting autoradiography specific tasks.

Having understood the potentiality of this scheme, the authors decided to extract the core functionalities of the framework itself, expand the database interface making use of an ORM approach (:link:`peewee`), include a plugin system to simplify the integration of processors developed for different purposes in external projects and supply an extensive general and API documentation, before releasing the code to the public domain as open source.

The way ahead
-------------

The future development of MAFw is driven by code usability. The authors are trying their best to make the framework as functional as possible offering colleague scientists a platform where to perform their analyses. At the time of writing there are already three targets envisaged: improved user-friendliness via a GUI or at least a TUI, improved performance via parallel processing and improved interactivity.

A G- / T- UI for MAFw
+++++++++++++++++++++

For the time being, the authors focused their efforts in coding a functional framework leaving usability aspects for a later development stage. MAFw is able to :ref:`execute <doc_runner>` one or more processors one after the other from the command line following the instructions given in a human- and machine- readable (:link:`toml`) steering file. While users can generate examples of steering files to serve as a starting point, implementing a graphical or at least a textual user interface would significantly simplify the process of creating and executing these files.

Following the plugin approach already used elsewhere in the library, the authors are considering to implement a TUI based on :link:`textual` where the user is guided in the creation of steering files.

Parallel processing
+++++++++++++++++++

Python is often recognized for its slower performance compared to some other programming languages available today. Analytical tasks are often I/O and/or CPU demanding, making the performance of a single threaded single processor program somehow limited.

MAFw uses :link:`pandas` and :link:`numpy` when dealing with data and those libraries are already capable to perform concurrent operations under some specific circumstances.

The well-known `python GIL <https://docs.python.org/3/glossary.html#term-global-interpreter-lock>`_ is actually preventing multi-threaded applications to improve overall performance for CPU-bound tasks. In this respect, an important revolution is taking place with the release of the experimental `Free-threaded CPython <https://docs.python.org/3/whatsnew/3.13.html#whatsnew313-free-threaded-cpython>`_ implementation of python (added in version 3.13) and MAFw authors are closely observing those developments to identify the more convenient approach to improve computational performance.

Introduce interactivity
+++++++++++++++++++++++

Even though in the original implementation of MAFw precursor, interactive processors were already existing, they were temporary removed from the current implementation. The authors recognize that many data scientists prefer to conduct interactive analysis using :link:`jupyter` or :link:`marimo` notebooks. Therefore, they are actively exploring ways to seamlessly integrate interactivity into the processor workflow through these notebook environments.

.. rubric:: Footnotes

.. [#] One of MAFw developer was in charge of the original coding of :link:`EUTelescope`, a set of :link:`MARLIN` processors for the reconstruction of particle trajectories recorded with beam telescopes.
