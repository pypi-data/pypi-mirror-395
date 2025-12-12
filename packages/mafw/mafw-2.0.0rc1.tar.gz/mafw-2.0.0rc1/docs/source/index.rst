MAFw: Modular Analysis Framework
================================


.. image:: /_static/images/general/mafw-logo.svg
    :width: 200 px

A software library for scientists written by scientists!

Description
-----------
Modular Analysis Framework (**MAFw**) is a python tool to run analytical steps in a consistent manner and to generate suitable outputs in the form of graphs and database tables.

The idea behind MAFw is to offer data scientists a framework where they will be able to implement complex analytical tasks in a well defined environment in a way that they can focus only on the data analysis without bothering with all other ancillary things, like interfaces to database, job submission and so on. In order for this scheme to work, the developer / scientist needs to respect some boundary conditions when drafting the code, but the overall advantage will enormously exceed the small imposed freedom limitations.

The core of MAFw is the **Processor**, the class that is responsible to perform the analytical task. The Processor I/O is based on a strong collaboration between a relational database structure and files on disc. The use of the database is *per se* not compulsory, but it will greatly simplify the analysis workflow.

In general the processor is:

* gathering the relevant input from one or more DB tables (location of input files, processing parameters...),
* performing its analytical job,
* and updating a DB output table with the main outcome including the location where output files are saved on disc.

By inheriting from the base Processor class, user developed processors will come with some *superpowers*, like the ability to exchange data with the database back-end, displaying progress to the user, generating output graphs and so on. The scientist tasks will be limited to the implementation of the analysis code.

Once the data scientists have created their processor libraries, they will be able to chain processors one after the other in a very simple way inside a so-called *steering file* and MAFw will take care to run them.

Are you ready to embark? Let us start with our :ref:`tutorial <doc_processor>` and you will master MAFw in a couple of hours!

This documentation is also available as a `PDF file <../pdf_downloads.html>`_.

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   doc_getting_started
   doc_introduction
   doc_processor
   doc_examples
   doc_processor_list
   doc_plugins
   doc_runner
   doc_database
   doc_filters
   doc_plotting
   doc_tutorial
   api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

