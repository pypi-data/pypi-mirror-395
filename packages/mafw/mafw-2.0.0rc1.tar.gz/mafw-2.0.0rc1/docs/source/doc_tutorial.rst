.. _tutorial_note:

.. note::

    **Note for direct readers**: If you have navigated directly to this practical example without reading the preceding
    documentation, please be aware that this implementation demonstrates advanced concepts and methodologies that are
    thoroughly explained in the earlier sections. While this example is designed to be self-contained, some technical
    details, and design decisions may not be immediately clear without the foundational knowledge
    provided in the main documentation. Should you encounter unfamiliar concepts or require deeper understanding of the
    library's architecture and principles, we recommend referring back to the relevant sections of the complete
    documentation.

.. _tutorial:

A step by step tutorial for a real experimental case study
==========================================================

Congratulations! You have decided to give a try to MAFw for your next analysis, you have read all the documentation
provided, but you got overwhelmed by information and now you do not know from where to start.

Do not worry, we have a simple, but nevertheless complete example that will guide you through each and every steps of
your analysis.

Before start typing code, let's introduce the experimental scenario.

The experimental scenario
-------------------------

Let's imagine, that we have a measurement setup integrating the amount of UV radiation reaching a sensor
in a give amount of time.

The experimental data acquisition (DAQ) system is saving one file for each exposure containing the value read by the sensor.
The DAQ is encoding the duration of the acquisition in the file name and let's assume we acquired 25 different exposures,
starting from 0 up to 24 hours. The experimental procedure is repeated for three different detectors having different
type of response and the final goal of our experiment is to compare their performance.

It is an ultra simplified experimental case and you can easily make it as complex as you wish, just by adding other
variables (different UV lamps, detector operating conditions, background illumination...). Nevertheless this simple
scenario can be straightforward expanded to any real experimental campaign.

.. figure:: /_static/images/tutorial/tutorial-simplified-pipeline.png
    :width: 600
    :align: center
    :alt: The simplified pipeline for the tutorial example.

    The simplified pipeline for the tutorial example.

Task 0. Generating the data
+++++++++++++++++++++++++++

This is not really an analysis task, rather the real acquisition of the data, that's why it is represented with a
different color in schema above. Nevertheless it is important to include that in our planning, because new data might
be generated during or after some data have been already analyzed. In this case, it is important that our analysis
pipelines will be able to process only the new (or modified) data, without wasting time and resources re-doing what has
been done already. This is the reason why there is a dashed line looping back from the plot step to the data generation.
Since this is a simulated experiment, instead of collecting real data, we will use a :class:`.Processor` to generate
some synthetic data.

Task 1. Building your data bank
+++++++++++++++++++++++++++++++

From a conceptual point of view, the first thing you should do when using MAFw is to import all your data (in this case
the raw data files) into a relational database. You do not need to store the content of the file in the database,
otherwise it will soon explode in size, you can simply insert the full path from where the file can be retrieved and
its checksum, so that we can keep an eye on possible modifications.

Task 2. Do the analysis
+++++++++++++++++++++++

In the specific scenario the analysis is very easy. Each file contains only one number, so there is very little to be
done, but your case can be as complicated as needed. We will open each file, read the content and then put it in a second
database table containing the results of the analysis of each file. In your real life experiment, this stage can contain
several processors generating intermediate results stored as well in the database.

Task 3. Prepare a relation plot
+++++++++++++++++++++++++++++++

Using the data stored in the database, we can generate a plot representing the integral flux versus the exposure time for
the three different detectors using a relation plot.

The 'code'
----------

In the previous section, we have defined what we want to achieve with our analysis (it is always a good idea to have
a plan before start coding!). Now we are ready to start with setting up the project containing the required processors
to achieve the analytical goal described above.

If you want to use MAFw plugin mechanism, then you need to build your project as a proper python package. Let's start
then with the project specification contained in the ``pyproject.toml`` file.

.. literalinclude:: ../../tests/test_full_integration/plug/pyproject.toml
    :language: toml
    :linenos:
    :emphasize-lines: 32-33

The specificity of this configuration file is in the highlighted lines: we define an entry point where your processors
are made available to MAFw.

Now before start creating the rest of the project, prepare the directory structure according to the python packaging
specification. Here below is the expected directory structure.

.. code-block:: text

    plug
    ├── README.md
    ├── pyproject.toml
    └── src
        └── plug
            ├── __about__.py
            ├── db_model.py
            ├── plug_processor.py
            └── plugins.py

You can divide the code of your analysis in as many python modules as you wish, but for this simple project we will keep
all processors in one single module `plug_processor.py`. We will use a second module for the definition of the database
model classes (`db_model.py`). Additionally we will have to include a `plugins.py` module (this is the one declared in
the pyproject.toml entry point definition) where we will list the processors to be exported along with our additional standard
tables.

The database definition
+++++++++++++++++++++++

Let's move to the database definition.

Our database will contain tables corresponding to the three model classes: InputFile and Data, and one helper table
for the detectors along with all the :ref:`standard tables <std_tables>` that are automatically created by MAFw.

Before analysing the code let's visualize the database with the ERD.

.. figure:: /_static/images/tutorial/db-erd.png
    :width: 600
    :align: center
    :alt: The ERD of the database for our project

    The schematic representation of our database. The standard tables, automatically created are in green. The detector
    table (yellow) is exported as a standard table and its content is automatically restored every time mafw is
    executed.

The InputFile is the model where we will be storing all the data files that are generated in our experiment while the
Data model is where we will be storing the results of the analysis processor, in our specific case, the value contained
in the input file.

The rows of these two models are linked by a 1-to-1 relation defined by the primary key.

Remember that is always a good idea to add a checksum field every time you have a filename field, so that we can check if
the file has changed or not.

The InputFile model is also linked with the Detector model to be sure that only known detectors are added to the analysis.

Let's have a look at the way we have defined the three models.

.. literalinclude:: ../../tests/test_full_integration/plug/src/plug/db_model.py
    :linenos:
    :start-at: class Detector(StandardTable):
    :end-at:       ).execute()

The detector table is derived from the StandardTable, because we want the possibility to initialize the content of this
table every time the application is executed. This is obtained in the init method. The use of the on_conflict clause
assure that the three detectors are for sure present in the table with the value given in the data object. This means
that if the user manually changes the name of one of these three detectors, the next time the application is executed,
the original name will be restored.

.. literalinclude:: ../../tests/test_full_integration/plug/src/plug/db_model.py
    :linenos:
    :start-at: class InputFile(MAFwBaseModel):
    :end-before:     # finish input file

The InputFile has five columns, one of which is a foreign key linking it to the Detector model. Note that we have used
the FileNameField and FileChecksumField to take advantage of the :func:`.verify_checksum` function. InputFile has a
trigger that is executed after each update that is changing either the exposure or the file content (checksum). When
one of these conditions is verified, then the corresponding row in the Data file will be removed, because we want to
force the reprocessing of this file since it has changed.
A similar trigger on delete is actually not needed because the Data model is linked to this model with an on_delete
cascade option.

.. literalinclude:: ../../tests/test_full_integration/plug/src/plug/db_model.py
    :linenos:
    :start-at: class Data(MAFwBaseModel):
    :end-at: value = FloatField(help_text='The result of the measurement')

The Data model has only two columns, one foreign key linking to the InputFile and one with the value calculated by the
Analysis processor. It is featuring three triggers executed on INSERT, UPDATE and DELETE. In all these cases, we want
to be sure that the output of the PlugPlotter is removed so that a new one is generated. Keep in mind that when a
row is removed from the PlotterOutput model, the corresponding files are automatically added to the OrphanFile model for
removal from the filesystem the next time a processor is executed.

Via the use of the foreign key, it is possible to associate a detector and the exposure for this specific value.

The processor library
+++++++++++++++++++++

Let's now prepare one processor for each of the tasks that we have identified in our planning. We will create a
processor also for the data generation.

GenerateDataFiles
^^^^^^^^^^^^^^^^^

This processor will accomplish Task 0 and it is very simple. It will generate a given number of files containing one
single number calculated given the exposure, the slope and the intercept. The detector parameter is used to
differentiate the output file name. As you see here below, the code is very simple.

.. literalinclude:: ../../tests/test_full_integration/plug/src/plug/plug_processor.py
    :linenos:
    :start-at: class GenerateDataFiles(Processor)
    :end-at:         self.progress_message = f'Generating exposure {self.i_item} for detector {self.detector}'

In order to generate the different detectors, you run the same processor with different values for the parameters.

PlugImporter
^^^^^^^^^^^^

This processor will accomplish Task 1, i.e. import the raw data file into our database. This processor is inheriting
from the basic :class:`.Importer` so that we can use the functionalities of the :class:`.FilenameParser`.

.. literalinclude:: ../../tests/test_full_integration/plug/src/plug/plug_processor.py
    :linenos:
    :start-after: # importer start
    :end-at:         super().finish()

The get_items is using the :func:`.verify_checksum` to verify that the table is still actual and we apply the filter
to be sure to process only new or modified files. The process and finish are very standard. In this specific case,
we preferred to add all the relevant information in a list and insert them all in one single call to the database.
But also the opposite approach (no storing, multiple insert) is possible.

Analyser
^^^^^^^^

This processor will accomplish Task 2, i.e. the analysis of the files. In our case, we just need to open the file, read
the value and put it in the database.

.. literalinclude:: ../../tests/test_full_integration/plug/src/plug/plug_processor.py
    :linenos:
    :start-after: # start of analyser
    :end-at:         self.progress_message = f'Analysing {self.item.filename.name}'

Also in this case, the generation of the item list is done keeping in mind the possible :ref:`filters <filters>` the user is applying in the steering file.
In the process, we are inserting the data directly to the database, so we will have one query for each item.

PlugPlotter
^^^^^^^^^^^

This processor will accomplish the last task, i.e. the generation of a relation plot where the performance of the three
detectors is compared.

.. literalinclude:: ../../tests/test_full_integration/plug/src/plug/plug_processor.py
    :linenos:
    :start-after: # start of plotter
    :end-at: self.output_filename_list.append(output_plot_path)
    :emphasize-lines: 12, 24-37

This processor is a mixture of :class:`.SQLPdDataRetriever`, :class:`.RelPlot` and :class:`.SNSPlotter`. The :class:`.SNSPlotter` has already some parameters and with the `new_defaults` dictionary we :ref:`over ride <parameter_processor_inheritance>` value of the output_folder to point to the current folder.

Looking at the init method, you might notice a strange thing, the table_name variable is set to `data_view`, that does not corresponding to any of our tables. The reason for this strangeness is quickly explained.

The :class:`.SQLPdDataRetriever` is generating a :link:`pandas` Dataframe from a SQL query. In our database the data table contains only two columns: the file reference and the measured value, so we have no direct access to the exposure nor to the detector. To get these other fields we need to join the data table with the input_file and the detector ones. The solution for this problem is the creation of a temporary view containing this join query. Have a look at the start method. This view will be deleted as soon as the connection will be closed.

The plugin module
+++++++++++++++++

Everything is ready, we just have to make MAFw aware of our processors and our standard tables. We are missing just
a few lines of code in the plugins module

.. literalinclude:: ../../tests/test_full_integration/plug/src/plug/plugins.py
    :linenos:
    :start-at: import mafw

The code is self-explaining. We need to invoke the processor hooks and return the list of processors. Instead of passing the real processor, we will use the :class:`processors proxies <.LazyImportProcessor>`, so that we can defer the import of the processor modules when and if needed.

Run the code!
-------------

We are done with coding and we are ready to run our analysis.

First thing, we need to install our package in a separated python environment.

.. tab-set::
    :sync-group: shell-cmds

    .. tab-item:: Windows
        :sync: win

        .. code-block:: doscon

            c:\> python -m venv my_venv
            c:\> cd my_venv
            c:\my_venv> bin\activate
            (my_venv) c:\my_venv> pip install -e c:\path\to\plug

    .. tab-item:: linux & MacOS
        :sync: linux

        .. code-block:: bash

            $ python -m venv my_venv
            $ source my_venv/bin/activate
            (my_venv) $ pip install -e /path/to/plug

Now verify that the installation was successful. If you run mafw list command you should get the list of all
available processors including the three that you have created.

.. tab-set::
    :sync-group: shell-cmds

    .. tab-item:: Windows
        :sync: win

        .. code-block:: doscon

            (my_venv) c:\my_venv> mafw list

    .. tab-item:: linux & MacOS
        :sync: linux

        .. code-block:: bash

            (my_venv) $ mafw list

One last step, before running the analysis. We need to make the two steering files, one for the generation of the
synthetic data and one for the real analysis and also the configuration file for the importer.

.. tab-set::

    .. tab-item:: File generation

        .. code-block:: toml
            :name: generate-data-file.toml
            :linenos:

            # file: generate-file.toml
            processors_to_run = ["GenerateDataFiles#1", "GenerateDataFiles#2", "GenerateDataFiles#3"]

            # customise the name of the analysis
            analysis_name = "integration-test-p1"
            analysis_description = """Generating data files"""
            available_processors = ["GenerateDataFiles"]

            [GenerateDataFiles]
            n_files = 25 # The number of files being generated.
            output_path = "/tmp/full-int/data" # The path where the data files are stored.
            slope = 1.0 # The multiplication constant for the data stored in the files.
            detector = 1 # The detector id being used. See the detector table for more info.

            ["GenerateDataFiles#1"]
            intercept = 5.0 # The additive constant for the data stored in the files.
            slope = 1.0 # The multiplication constant for the data stored in the files.
            detector = 1 # The detector id being used. See the detector table for more info.

            ["GenerateDataFiles#2"]
            intercept = 15.0 # The additive constant for the data stored in the files.
            slope = 5.0 # The multiplication constant for the data stored in the files.
            detector = 2 # The detector id being used. See the detector table for more info.

            ["GenerateDataFiles#3"]
            intercept = 0.1 # The additive constant for the data stored in the files.
            slope = 0.2 # The multiplication constant for the data stored in the files.
            detector = 3 # The detector id being used. See the detector table for more info.

            [UserInterface] # Specify UI options
            interface = "rich" # Default "rich", backup "console"

    .. tab-item:: Analysis

        .. code-block:: toml
            :name: analysis.toml

            # file: analysis.toml
            processors_to_run = ["TableCreator","PlugImporter","Analyser", "PlugPlotter"]

            # customise the name of the analysis
            analysis_name = "integration-test-p2"
            analysis_description = """Analysing data"""
            available_processors = ["PlugImporter", "Analyser", "PlugPlotter"]
            new_only = true

            [DBConfiguration]
            URL = "sqlite:////tmp/full-int/plug.db" # Change the protocol depending on the DB type. Update this file to the path of your DB.

            [DBConfiguration.pragmas] # Leave these default values, unless you know what you are doing!
            journal_mode = "wal"
            cache_size = -64000
            foreign_keys = 1
            synchronous = 0

            [TableCreator] # Processor to create all tables in the database.
            apply_only_to_prefix = [] # Create only tables whose name start with the provided prefixes.
            force_recreate = false

            [PlugImporter]
            input_folder = "/tmp/full-int/raw_data" # The input folder from where the images have to be imported.
            parser_configuration = "/tmp/full-int/importer_config.toml" # The path to the TOML file with the filename parser configuration
            recursive = true

            [Analyser]

            [PlugPlotter]
            output_plot_path = "/tmp/full-int/output.png" # The filename of the output plot

            [UserInterface] # Specify UI options
            interface = "rich" # Default "rich", backup "console"

    .. tab-item:: Importer configuration

        .. code-block:: toml
            :linenos:

            # file: importer_config.toml
            elements = ['exposure', 'detector']

            [exposure]
            regexp = '[_-]*exp(?P<exposure>\d+\.*\d*)[_-]*'
            type='float'

            [detector]
            regexp = '[_-]*det(?P<detector>\d+)[_-]*'
            type='int'

Adapt the steering files, in particular the paths and you are ready to run!
In the analysis TOML file, you will also find the section concerning the database; for this simple case we used a
:link:`SQLite` single file DB, but you whatever :ref:`other DB <other_db>` would work exactly in the same way.

.. tab-set::
    :sync-group: shell-cmds

    .. tab-item:: Windows
        :sync: win

        .. code-block:: doscon

            (my_venv) c:\my_venv> mafw run generate-file.toml

    .. tab-item:: linux & MacOS
        :sync: linux

        .. code-block:: bash

                (my_venv) $ mafw run generate-file.toml

This will run the GenerateDataFiles processor three times, as specified in the three replicas, one for each detector. In the steering file, you can see that there are base settings specified in the base GenerateDataFiles table, plus some specific values for the three replicas. If you need are refresh on processor replicas, go back :ref:`here <processor_replica>`.
The three processor replicas will generate all our input data and we are ready to start the data analysis.

.. tab-set::
    :sync-group: shell-cmds

    .. tab-item:: Windows
        :sync: win

        .. code-block:: doscon

            (my_venv) c:\my_venv> mafw run analysis.toml

    .. tab-item:: linux & MacOS
        :sync: linux

        .. code-block:: bash

            (my_venv) $ mafw run analysis.toml

And here comes the magic! The three processors will be executed one after the other, the database is created and filled with all the provided data and the comparison plot is generated (default file name output.png).

.. figure:: /_static/images/tutorial/output.png
    :width: 600
    :align: center
    :alt: The comparison plot of the three detectors.

    The comparison plot of the three detectors.

This is just the beginning, now you can try all the benefits to use a clever database to drive your analysis pipeline.
Try, for example, to remove one file and re-run the analysis, you will see a warning message informing you that a file
was not found and that the corresponding row in the database has been removed as well. The rest of the analysis will
remain the same, but the output plot will be regenerated with a missing point.

Try to manually modify the content of a file and re-run the analysis. The :func:`.verify_checksum` will immediately
detect the change and force the re-analysis of that file and the generation of the output plot.

Try to rename one file changing the exposure value. You will see that mafw will detect that one file is gone missing
in action, but a new one has been found. The output file will be update.

Try to repeat the analysis without any change and mafw won't do anything! Try to delete the output plot and during the
next run mafw will regenerate it.

You can also play with the database. Open it in :link:`DBeaver` (be sure that the foreign_check is enforced) and remove one line
from the input_file table. Run the analysis and you will see that the output plot file is immediately removed because it
is no more actual and a new one is generated at the end of chain.

**It's not magic even if it really looks like so, it's just a powerful library for scientists written by scientists!**

