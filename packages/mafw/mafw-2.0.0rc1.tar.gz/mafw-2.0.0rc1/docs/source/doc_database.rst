.. include:: substitutions.rst

.. _database:

Database: your new buddy!
=========================

As a scientist you are used to work with many software tools and often you need to write your own programs because the ones available do not really match your needs. Databases are not so common among scientists, we do not really understand why, but nevertheless their strength is beyond question.

The demonstration of the power and usefulness of a database assisted analysis framework will become clear and evident during our :ref:`tutorial <tutorial>` where we will build a small analytical experiment from scratch one step at the time.

For the time being, let us concentrate a bit on the technical aspect without delving too deeply into the specifics.

Database: one name, many implementations
----------------------------------------

Database is really a generic term and, from a technical point of view, one should try to be more specific and define better what kind of database we are talking about. We are not just referring to the brand or the producing software house: there are indeed different database architectures, but the one best suited for our application is the **relational database**, where each entity can be related directly to one or more other entities. You can read about relational databases on `wikipedia <https://en.wikipedia.org/wiki/Relational_database>`_ for example, and if you find it too complicated, have a look at `this shorter and easier version <https://cloud.google.com/learn/what-is-a-relational-database>`_.

The software market is full of relational databases, from the very common :link:`MySQL` to the very famous :link:`ORACLE`, passing through the open source :link:`PostgreSQL` to finish with :link:`SQLite` the simplest and most used database in the world. As you may have guessed from their names, they are all sharing the same query language (*SQL*: structured query language), making it rather simple to have an abstract interface, that is to say a layer in between the user and the actual database that allows your code to work in the same way irrespectively of the specific implementation.

Peewee: a simple and small ORM
------------------------------

Of course there are also lots of different abstract interfaces, some more performing than the others. We have selected :link:`peewee`, because it is lightweight, easy to understand and to use, and it works with several different implementations.

:link:`peewee` is a ORM (promised this is the last acronym for this page!), it is to say an object relational mappers, or in simpler words a smart way to connect the tables in your database with python classes in your code. Have a look at this interesting `article <https://www.fullstackpython.com/object-relational-mappers-orms.html>`_ for a more detailed explanation.

:link:`peewee` offers at least three different backends: SQLite, MySQL and PostgreSQL. If the size of your project is small to medium and the analysis is mainly performed on a single computer, then we recommend SQLite: the entire database will be living in a single file on your disc, eliminating the need for IT experts to set up a database server.
If you are aiming for a much bigger project with distributed computing power, then the other two choices are probably equally good and your local IT helpdesk may suggest you what is best for your configuration and the available IT infrastructure. As you see, MAFw is always offering you a tailored solution!

Now, take a short break from this page, move to the :link:`peewee` documentation and read the *Quickstart* section before coming back here.

Database drivers
++++++++++++++++

If you have installed MAFw via pip without specifying the `all-db` optional features, then your python environment is
very likely missing the python drivers to connect to MySQL and PostgreSQL. This is not a bug, but more a feature,
because MAFw gives you the freedom to select the database implementation that fits your needs. Sqlite is natively
supported by python, so you do not need to install anything extra, but if you want to use MySQL, PostgreSQL or any
other DB supported by :link:`peewee` than it is your responsibility to install in your environment the proper driver.
`Here <https://docs.peewee-orm.com/en/latest/peewee/database.html#initializing-a-database>`__ you can find a list of DB
driver compatible with :link:`peewee`.

If you want, you can install MAFw adding the `all-db` optional feature and in this way the standard MySQL and
PostgreSQL drivers will also be installed.

One class for each table
------------------------

As mentioned before, the goal of an ORM is to establish a link between a database table and a python class. You can use the class to retrieve existing rows or to add new ones, and as always, you do not need take care of the boring parts, like establishing the connection, creating the table and so on, because this is the task of MAFw and we do it gladly for you!

Let us have a look together to the following example. We want a processor that lists recursively all files starting from a given directory and adds the filenames and the file hash digests to a table in the database.

Let us start with some imports

.. literalinclude:: ../../src/mafw/examples/db_processors.py
    :linenos:
    :start-at: import datetime
    :end-at: from mafw.tools.file_tools import file_checksum
    :emphasize-lines: 4, 8

The crucial one is at line 8, where we import :class:`~mafw.db.db_model.MAFwBaseModel` that is the base model for all the tables we want to handle with MAFw. Your tables **must inherit** from that one, if you want the |processor| to take care of handling the link between the class and the table in the database.
At line 4, we import some classes from peewee, that will define the columns in our model class and consequently in our DB table.

Now let us create the model class for our table of files.

.. code-block:: python
    :name: file_first
    :linenos:

    class File(MAFwBaseModel):
        """The Model class representing the table in the database"""

        filename = TextField(primary_key=True)
        digest = TextField()
        creation_date = DateTimeField()
        file_size = IntegerField()

.. note::
    A much better implementation of a similar class will be given :ref:`later on <mafw_fields>` demonstrating the power of custom defined fields.

As you can see the class definition is extremely simple. We define a class attribute for each of the columns we want to have in the table and we can choose the field type from a long list of `available ones <http://docs.peewee-orm.com/en/latest/peewee/models.html#fields>`_ or we can even easily implement our owns. The role of a field is to adapt the type of the column from the native python type to the native database type and vice versa.

Our table will have just four columns, but you can have as many as you like. We will have one text field with the full filename, another text containing the hexadecimal hashlib digest of the file, the creation date for which we will use a datetime field, and finally a file_size field of integer type. We will be using the filename column as a primary key, because there cannot be two files with the same filename. On the contrary, there might be two identical files having the same hash but different filenames. According to many good database experts, using a not numeric primary key is not a good practice, but for our small example it is very practical.

If you do not specify any primary key, the ORM will add an additional number auto-incrementing column for this purpose. If you want to specify multiple primary keys, `this <http://docs.peewee-orm.com/en/latest/peewee/models.html#composite-key>`_ is what you should do. If you want to create a model without a primary key, `here <http://docs.peewee-orm.com/en/latest/peewee/models.html#models-without-a-primary-key>`_ is what you need to do.

The ORM will define the actual name of the table in the database and the column names. You do not need to worry about this!

And now comes the processor that will be doing the real work, it is to say, filling the File table.

.. literalinclude:: ../../src/mafw/examples/db_processors.py
    :name: first_db_processor
    :linenos:
    :pyobject: FillFileTableProcessor
    :emphasize-lines: 1, 30, 65-66

The first thing to notice is at line 1, where we used the decorator :func:`~mafw.decorators.database_required`. The use of this decorator is actually not compulsory, its goal is to raise an exception if the user tries to execute the processor without having a properly initialized database.

At line 30, in the `start` method we ask the database to create the table corresponding to our :class:`~mafw.examples.db_processors.File` model. If the table already exists, then nothing will happen.

In the `process` method we will store all the information we have collected from the files into a list and we interact with the database only in the `finish` method. At line 65, we use a context manager to create an `atomic <https://en.wikipedia.org/wiki/Atomicity_(database_systems)>`_ transaction and then, at line 66, we insert in the :class:`~mafw.examples.db_processors.File` all our entries and in case a row with the same primary key exists, then it is replaced.

We could have used several different insert approaches, here below are few examples:

.. code-block:: python

    # create an instance of File with all fields initialized
    new_file = File(filename=str(self.item),
                  digest=file_checksum(self.item),
                  file_size=self.item.stat().st_size,
                  creation_date=datetime.datetime.fromtimestamp(self.item.stat().st_mtime))
    new_file.save() # new_file is now stored in the database

    # create an instance of File and add the fields later
    new_file = File()
    new_file.filename = str(self.item)
    new_file.digest = file_checksum(self.item)
    new_file.file_size = self.item.stat().st_size
    new_file.creation_data = datetime.datetime.fromtimestamp(self.item.stat().st_mtime)
    new_file.save()

    # create and insert directly
    new_file = File.create(filename=str(self.item),
                  digest=file_checksum(self.item),
                  file_size=self.item.stat().st_size,
                  creation_date=datetime.datetime.fromtimestamp(self.item.stat().st_mtime))

The approach to follow depends on various factor. Keep in mind that :link:`peewee` operates by default in `auto commit mode <http://docs.peewee-orm.com/en/latest/peewee/database.html#autocommit-mode>`_, meaning that for each database interaction, it creates a transaction to do the operation and it closes afterwards.

To be more performant from the database point of view, especially when you have several operations that can be grouped together, you can create an `atomic transaction <http://docs.peewee-orm.com/en/latest/peewee/querying.html#atomic-updates>`_ where the ORM will open one transaction only to perform all the required operations.

What we have done in the `finish` method is actually known as an `upsert <http://docs.peewee-orm.com/en/latest/peewee/querying.html#upsert>`_. It means that we will be inserting new items or updating them if they exist already.

Ready, go!
----------

We have prepared the code, now we can try to run it. We can do it directly from a script

.. code-block:: python

    if __name__ == '__main__':
        database_conf = default_conf['sqlite']
        database_conf['URL'] = db_scheme['sqlite'] + str( Path.cwd() / Path('test.db'))

        db_proc = FillFileTableProcessor(root_folder =r'C:\Users\bulghao\Documents\autorad-analysis\EdgeTrimming',
                                         database_conf=database_conf)

        db_proc.execute()

or in a more elegant way we can use the mafw app to run, but first we need to generate the proper steering file.

.. tab-set::

    .. tab-item:: Console

        .. code-block:: doscon
            :name: gen_db_steering

            c:\> mafw steering db-processor.toml
            A generic steering file has been saved in db-processor.toml.
            Open it in your favourite text editor, change the processors_to_run list and save it.

            To execute it launch: mafw run db-processor.toml.

    .. tab-item:: TOML

        .. code-block:: toml
            :name: db-processor.toml
            :linenos:
            :emphasize-lines: 11-12, 14-18

            # MAFw steering file generated on 2024-11-24 22:13:38.248423

            # uncomment the line below and insert the processors you want to run from the available processor list
            processors_to_run = ["FillFileTableProcessor"]

            # customise the name of the analysis
            analysis_name = "mafw analysis"
            analysis_description = "Using the DB"
            available_processors = ["AccumulatorProcessor", "GaussAdder", "ModifyLoopProcessor", "FillFileTableProcessor", "PrimeFinder"]

            [DBConfiguration]
            URL = "sqlite:///file-db.db" # Change the protocol depending on the DB type. Update this file to the path of your DB.

            [DBConfiguration.pragmas] # Leave these default values, unless you know what you are doing!
            journal_mode = "wal"
            cache_size = -64000
            foreign_keys = 1
            synchronous = 0

            [FillFileTableProcessor] # Processor to fill a table with the content of a directory
            root_folder = 'C:\Users\bulghao\PycharmProjects\mafw' # The root folder for the file listing

            [UserInterface] # Specify UI options
            interface = "rich" # Default "rich", backup "console"


If you look at the steering file, you will notice that there is a ``DBConfiguration`` section, where we define the most important variable, it is to say the DB URL. This is not only specifying where the database can be found, but also the actual implementation of the database. In this case, it will be a sqlite database located in the file ``file-db.db`` inside the current directory.

There is also an additional sub table, named pragmas, containing advanced options for the sqlite DB. Unless you really know what you are doing, otherwise, you should leave them as they are.

In the following :ref:`other_db`, we will cover the case you want to use another DB implementation different from SQLite.

In the ``FillFileTableProcessor`` you can find the standard configuration of its processor parameters.

Now we are really ready to run our first DB processor and with a bit of luck, you should get your DB created and filled.

.. admonition:: How to check the content of a DB?

    There are several tools serving this purpose. One of those is :link:`dbeaver` that works with all kind of databases offering an open source community version that you can download and install.

.. _other_db:

Configuring other types of databases
++++++++++++++++++++++++++++++++++++

In the previous example, we have seen how to configure a simple SQLite database. For this database, you just need to
indicate in the URL field the path on the local disc where the database file is stored.

SQLite does not require any user name nor password and there are no other fields to be provided. Nevertheless, it is
worth adding the previously mentioned pragmas section to assure the best functionality of peewee.

In the case of MySQL and PostgreSQL, the URL should point to the server where the database is running. This could be
the localhost but also any other network destination. Along with the server destination, you need also to specify the
port, the database name, the user name and the password to establish the connection.

Of course, it is not a good idea to write your database password as plain text in a steering file that might be
shared among colleagues or even worse included in a Git repository. To avoid this security issue, it is recommended
to follow some other authentication approach.

Both MySQL and PostgreSQL offers the possibility to store the password in a separate file, that, at least in linux,
should have a very limited access right. Have a look at the exemplary steering files with the corresponding password
files here below.

.. tab-set::

    .. tab-item:: SQLite

        .. code-block:: toml

            [DBConfiguration]
            URL = "sqlite:///file-db.db" # change the filename to the absolute path of the db

            [DBConfiguration.pragmas] # Leave these default values, unless you know what you are doing!
            journal_mode = "wal"
            cache_size = -64000
            foreign_keys = 1
            synchronous = 0

    .. tab-item:: PostgreSQL

        .. code-block:: toml

            [DBConfiguration]
            # Update the database server and the database name to reflect your configuration
            URL = "postgresql://database-server:5432/database-name"

            # change it to your username
            user = 'username'

            # if you want, you can leave the pragmas section from the SQLite default configuration because it
            # want be used.


        Instruction on how to create a PostgreSQL password file are provided `here <https://www.postgresql.org/docs/current/libpq-pgpass.html>`__. This is an example:

        .. code-block:: unixconfig

            database-server:5432:database-name:username:password

    .. tab-item:: MySQL

        .. code-block:: toml

            [DBConfiguration]
            # Update the database server and the database name to reflect your configuration
            URL = "mysql://database-server:3306/database-name"

            # update to specify your username
            user = 'username'

            # update to specify the password file
            read_default_file = '~/.my.cnf'

            # if you want, you can leave the pragmas section from the SQLite default configuration because it
            # want be used.


        Instruction on how to create a MySQL password file are provided `here <https://dev.mysql.com/doc/refman/8.4/en/password-security-user.html>`__. This is an example:

        .. code-block:: ini

            [client]
            user=username
            password=password
            host=database-server


.. _mafw_base_model:

The advantages of using MAFwBaseModel
-------------------------------------

In the previous code snippets we have implemented our Model classes as sub-class of :class:`.MAFwBaseModel`. This is not just a detail because :class:`.MAFwBaseModel` is offering some embedded advantages compared to the base model class of :link:`peewee`. In the following subsections we will explicitly describe them all. For additional details, you can also read the API documentation of :class:`.MAFwBaseModel` and of :class:`.RegisteredMeta` the meta class where all this magic is taking place.

.. _auto_registration:

Automatic model registration
++++++++++++++++++++++++++++

We will explain you the relevance of this point with an example.

Imagine that you have a processor that is performing some calculations; the processor can operate on real data or on simulated data following the same workflow, the only difference is that we will be taking input items from two different tables, one for real data and one for simulated data. Similarly we would like to save the output into two different tables.

The most convenient approach would be to set the input and output Models as processor parameters, but a Model is a python class and we could not provide this via our steering file. There we can imagine to provide a string representing the name of the corresponding DB table, but :link:`peewee` is missing the capability to retrieve the Model class given the name of the corresponding DB table or the model name, the last possibility would be to build up a custom selection logic based on *if/else* blocks.

The automatic registration and the :data:`~.mafw.db.db_model.mafw_model_register` are there exactly to fill this hole. When you define a new model class inheriting from :class:`.MAFwBaseModel`, this will be automatically added to model register and then you will be able to retrieve it using the :meth:`.ModelRegister.get_model` method [#]_.

Here is a little example to make it simpler.

.. tab-set::

    .. tab-item:: db_model.py

        .. code-block:: python
            :linenos:

            # file: db_model.py
            # this is the module where all our models are defined

            from peewee import IntegerField
            from mafw.db_model import MAFwBaseModel

            class MyRegisteredModel(MAFwBaseModel):
                integer_num = IntegerField(primary_key=True)

    .. tab-item:: my_processor.py

        .. code-block:: python
            :linenos:
            :emphasize-lines: 7

            # file: my_processor.py
            # this it the module where the processors are defined

            from mafw.processor import Processor
            from mafw.db.db_model import mafw_model_register

            import db_model.py

            class MyProcessor(Processor):
                # put here all your definitions...
                def get_items(self):
                    # we want to process all items in the input model.
                    input_model = mafw_model_register.get_model('my_registered_model')
                    return input_model.select()

In the my_processor.py file you can see how to retrieve a Model class from the register. You can use either the full table name or if you wish the Model name (MyRegisteredModel) as a key. It is important to notice line 7 where we import db_model with all our model definitions. This is necessary because the automatic registration occurs when the interpreter is processing the definition of a class inheriting from :class:`.MAFwBaseModel`. The imported module is actually not used in the processor, but we need to be sure that the interpreter has read the definition of the model. In a :ref:`following section <db_module_plugin>`, you will see a smart method to avoid this useless import.

Exclude from automatic registration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There might be cases, not many to be honest, in which you want a Model class not to be registered. A typical example is the case of a Model class used in your project as a base for all your models. It makes no sense to have this *abstract* model in the registry because you will never use it.

If you want to prevent the automatic registration then you simply have to specify it in the model definition as in the following example:

.. code-block:: python
    :linenos:

    from mafw.db.db_model import MAFwBaseModel

    class MyBaseModel(MAFwBaseModel, do_not_register=True):
        pass

    class MyConcreteModel(MyBaseModel):
        pass

Have a look at the definition of MyBaseModel. Along with the specification of the base class, we provided as well the extra keyword argument `do_not_register`. In this example, MyBaseModel will not be registered in the :data:`.mafw_model_register`, while MyConcreteModel is.

.. _db_module_plugin:

Automatic import of db modules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Having the automatic registration is for sure a big step forward, something less for you to take care, but having to import the module with the model class definition is a bit annoying, in particular if your code is using a linter where `unused_import (F401) <https://docs.astral.sh/ruff/rules/unused-import/>`__ are often automatically removed.

The idea is to use once again the plugin mechanism of MAFw to inform the runner (``mafw``), that the module including all the db models should be imported. This is how you can achieve this:

.. code-block::python
    :caption: Exporting the DB model module to the plugin.

    import mafw

    # add also the register_processors() hook, if you want your processor to be discovered

    @mafw.mafw_hookimpl
    def register_db_model_modules() -> list[str]:
        return ['my_project.db.db_model', 'my_project.db.db_simulation_model']

The `register_db_model_modules` is expected to return a list of module fully qualified module names. Those strings will be then automatically passed to the importlib.import_module function in order to be loaded. It is important that the string is properly formatted and the module is correctly spelled, otherwise MAFw will raise an ImportError.


Trigger support
+++++++++++++++

The use of triggers and their advantages for an efficient and reliable data analysis will be discussed at length in the :ref:`following chapter <triggers>`. Some special triggers can also be automatically generated as explained :ref:`here <auto_triggers>`.


Customizable table name
+++++++++++++++++++++++

The default naming convention adopted by  :link:`peewee` is to transform the CamelCase model name is a snake_case table name. Unless you want to access the tables using low level SQL statements or from an external tool like :link:`dbeaver`, then knowing the actual table name is not very important.

:link:`Peewee` offers the possibility to `customize the table names <https://docs.peewee-orm.com/en/latest/peewee/models.html#table-names>`__ and MAFwBaseModel expand this even further, with the possibility to add a prefix, a suffix or both to the camel_case table name. This feature is very handy when you are handling a large database with several tens of tables. When browsing the database index from :link:`dbeaver`, tables are normally sorted in alphabetical order and thus finding a specific table can be frustrating. You may want to prefix all the tables belonging to a specific part of your experiment with a given word, in order to have them all grouped together [#]_.

This is how:

.. code-block:: python

    from mafw.db.db_model import MAFwBaseModel

    class SimulationModel(MAFwBaseModel, do_not_register=True):
        class Meta:
            prefix = 'simul'

    class SimulationResult(SimulationModel):
        # put here your fields
        pass

    class DataModel(MAFwBaseModel, do_not_register=True):
        class Meta:
            prefix = 'data'

    class DataResult(DataModel):
        # put here your fields
        pass

In this example we have defined two base models (that are not registered automatically), one for simulation and one for real data results. In the Meta class definition of the two base models we have assigned a value to the attribute ``prefix``. This attribute will be inherited by all their subclasses, so that the table name corresponding to SimulationResult will be `simul_simulation_result`. A similar effect can be obtained setting the ``suffix`` parameter.

.. seealso::

    See also :func:`.make_prefixed_suffixed_name` for more details on the naming convention.

Automatic table creation
++++++++++++++++++++++++

In our first :ref:`processor using the database <first_db_processor>`, we have created the table corresponding to the File model manually in the start method. This operation must be done before we try to access the content of the table, otherwise the database will generate an error. If a table is already existing, then the create_table command is actually ignored.

One of the biggest advantage of inheriting from :class:`.MAFwBaseModel` is that the creation of all models can be automatized by using a processor included in MAFw library: the :class:`.TableCreator`. You can simply include this processor in your TOML steering file, possibly as a first processor in the list and afterwards you can forget about creating tables.

This processor is customizable via two parameters:

    1. *apply_only_to_prefix*: allows to restrict the creation of tables whose name is starting with a given prefix. More than one prefix can be provided.

    2. *force_recreate*: will force the tables to be recreated in the case they are already existing. This is rather **dangerous** because, the processor will actually drop all tables before creating them causing the loss of all your data. Use it with extreme care!!!

You still have the freedom to disable this automatic feature by setting the `automatic_creation` flag in the Meta class to False, like in this example:

.. code-block:: python

    from mafw.db.db_model import MAFwBaseModel

    class NoAutoModel(MAFwBaseModel):
        # put here your fields
        class Meta:
            automatic_creation = False


Remember: only registered models can have tables automatically created. If you decided not to register a model, then you will have to manually create the corresponding table before using it.

.. _triggers:

Triggers: when the database works on its own
--------------------------------------------

In the next paragraphs we will spend a few minutes understanding the roles of Triggers. Those are database entities performing some actions in response of specific events. You can have, for example, a trigger that is inserting a row in TableB whenever a row is inserted in TableA. If you are not really familiar with triggers, this is a `brief introduction <https://www.sqlite.org/lang_createtrigger.html>`_.

Triggers are very handy for many applications, and in our :ref:`tutorial <tutorial>` we will see an interesting case, but they tend to struggle with ORM in general. In fact, no ORM system is natively supporting triggers. The reason is very simple. In an ORM, the application (the python code, if you wish) is the main actor and the database is just playing the role of the passive buddy. From the point of view of an ORM based application, if you want to have a trigger, then just write the needed lines of python code to have the actions performed in the other tables. It makes totally sense, you have only one active player and it simplifies the debugging because if something is going wrong, it can only be a fault of the application.

The standard implementation of trigger-like functions with ORM is to use `signals <https://docs.peewee-orm.com/en/latest/peewee/playhouse.html#signals>`_, where you can have callbacks called before and after high level ORM APIs calls to the underlying database. Signals are good, but they are not free from disadvantages: at a first glance, they look like a neat solution, but as soon as the number of callbacks is growing, it may become difficult to follow a linear path in the application debugging. Second, if you do a change in the database from another application, like the :link:`dbeaver` browser, then none of your codified triggers will be executed. Moreover in the case of :link:`Peewee`, signals work only on Model instances, so all bulk inserts and updates are excluded.

Having triggers in the database would assure that irrespectively of the source of the change, they will always be executed, but as mentioned above, the user will have to be more careful in the debug because also the database is now playing an active role.

We let you decide what is the best solution. If you want to follow the pure ORM approach, then all models inheriting from :class:`~mafw.db.db_model.MAFwBaseModel` have the possibility to use signals. If you want to have triggers, you can also do so. An example for both approaches is shown here below.

The signal approach
+++++++++++++++++++

As mentioned above, the signal approach is the favourite one if you plan to make all changes to the database only via your python code. If you are considering making changes also from other applications, then you should better use the trigger approach.

Another limitation is that only model instances emit signals. Everytime you use a `classmethod` of a Model, then no signals will be emitted.

The signal dispatching pattern functionality is achieved by linking the signal emitted by a sender in some specific circumstances to a handler that is receiving this signal and performing some additional operations (not necessarily database operations).

Every model class has five different signals:

    1. **pre_save**: emitted just before that a model instance is saved;
    2. **post_save**: emitted just after the saving of a model instance in the DB;
    3. **pre_delete**: emitted just before deleting a model instance in the DB;
    4. **post_delete**: emitted just after deleting a model instance from the DB;
    5. **pre_init**: emitted just after the init method of the class is invoked. Note that the *pre* is actually a *post* in the case of init.

Let us try to understand how this works with the next example.

.. code-block:: python
    :linenos:
    :name: test_signals
    :caption: A test with signal
    :emphasize-lines: 11-28, 42, 53

    class MyTable(MAFwBaseModel):
        id_ = AutoField(primary_key=True)
        integer = IntegerField()
        float_num = FloatField()

    class TargetTable(MAFwBaseModel):
        id_ = ForeignKeyField(MyTable, on_delete='cascade', primary_key=True, backref='half')
        another_float_num = FloatField()

        @post_save(sender=MyTable, name='my_table_after_save_handler')
        def post_save_of_my_table(sender: type(MAFwBaseModel), instance: MAFwBaseModel, created: bool):
            """
            Handler for the post save signal.

            The post_save decorator is taking care of making the connection.
            The sender specified in the decorator argument is assuring that only signals generated from MyClass will be
            dispatched to this handler.

            The name in the decorator is optional and can be use if we want to disconnect the signal from the handler.

            :param sender: The Model class sending this signal.
            :type sender: type(Model)
            :param instance: The actual instance sending the signal.
            :type instance: Model
            :param created: Bool flag if the instance has been created.
            :type created: bool
            """
            TargetTable.insert({'id__id': instance.id, 'another_float_num': instance.float_num / 2}).execute()

    database: Database = SqliteDatabase(':memory:', pragmas=default_conf['sqlite']['pragmas'])
    database.connect()
    database_proxy.initialize(database)
    database.create_tables([MyTable, TargetTable], safe=True)

    MyTable.delete().execute()
    TargetTable.delete().execute()

    # insert a single row in MyTable with the save method.
    my_table = MyTable()
    my_table.integer = 20
    my_table.float_num = 32.16
    my_table.save()
    # after the save query is done, the signal mechanism will call the
    # post_save_trigger_of_my_table and perform an insert on the target
    # table as well.
    assert MyTable.select().count() == 1
    assert TargetTable.select().count() == 1

    # add some bulk data to MyTable
    data = []
    for i in range(100):
        data.append(dict(integer=random.randint(i, 10 * i), float_num=random.gauss(i, 2 * i)))
    MyTable.insert_many(data).execute()
    # this is done via the Model class and not via a concrete instance of the Model, so no signals will be emitted.

    assert MyTable.select().count() == 101
    assert TargetTable.select().count() == 1



We created two tables linked via a foreign key. The goal is that everytime we fill in a row in ``MyTable``, a row is
also added to TargetTable with the same id but where the value of another_float_num is just half of the original
float_num. The example is stupid, but it is good enough for our demonstration.

The signal part is coded in the lines from 11 to 28 (mainly doc strings). We use the ``post_save`` decorator to connect
MyTable to the ``post_save_of_my_table`` function where an insert in the TargetTable will be made.

The code is rather simple to follow. Just to be sure, we empty the two tables, then we create an instance of the
MyTable model, to set the integer and the float_num column. When we save the new row, the post_save signal of MyTable
is emitted and the handler is reacting by creating an entry in the TargetTable as well.
In fact the number of rows of both tables are equal to 1.

What happens later is to demonstrate the weak point of signals. At line 53, we insert several rows via a
``insert_many``. It must be noted that the insert_many is a classmethod applied directly to the model class.
The consequence is that the signal handler will not be invoked and no extra rows will be added to the TargetTable.

The trigger approach
++++++++++++++++++++

In order to use a trigger you need to create it. This is an entity that lives in the database, so you would need the database itself to create it.

MAFw is providing a :class:`~mafw.db.trigger.Trigger` class that helps you in creating the required SQL query that needed to be issued in order to create the trigger. Once it is created it will operate continuously.

If you have a look at the `CREATE TRIGGER SQL command <https://www.sqlite.org/lang_createtrigger.html>`_ you will see that it starts with the definition of when the trigger is entering into play (BEFORE/AFTER) and which operation (INSERT/DELETE/UPDATE) of which table. Then there is a section enclosed by the BEGIN and END keywords, where you can have as many SQL queries as you like.

The same structure is reproduced in the :class:`~mafw.db.trigger.Trigger` class. In the constructor, we will pass the arguments related to the configuration of the trigger itself. Then you can add as many SQL statement as you wish.

.. tab-set::

    .. tab-item:: Python

        .. code-block:: python
            :linenos:
            :name: trigger_python
            :caption: python Trigger class

            from mafw.db.db_model import Trigger

            new_trigger = Trigger('trigger_after_update', (TriggerWhen.After,
                    TriggerAction.Update), 'my_table', safe=False, for_each_row=False)
            new_trigger.add_sql('INSERT INTO another_table (col1, col2) VALUES (1, 2)')
            new_trigger.add_sql('INSERT INTO third_table (col1, col2) VALUES (2, 3)'))
            new_trigger.create()

    .. tab-item:: SQL

        .. code-block:: SQL
            :linenos:
            :name: trigger_sql
            :caption: emitted SQL

            CREATE TRIGGER trigger_after_update
            AFTER UPDATE  ON my_table

            BEGIN
                INSERT INTO another_table (col1, col2) VALUES (1, 2);
                INSERT INTO third_table (col1, col2) VALUES (2, 3);
            END;

Now let us have a look at how you can use this, following one of our test benches.

Standalone triggers
^^^^^^^^^^^^^^^^^^^

.. code-block:: python
    :linenos:
    :emphasize-lines: 20-22
    :name: test_manually_created_trigger
    :caption: A test Trigger created manually

    def test_manually_created_trigger():
        class MyTable(MAFwBaseModel):
            id_ = AutoField(primary_key=True)
            integer = IntegerField()
            float_num = FloatField()

        class TargetTable(MAFwBaseModel):
            id_ = ForeignKeyField(MyTable, on_delete='cascade', primary_key=True, backref='half')
            half_float_num = FloatField()

        database: Database = SqliteDatabase(':memory:', pragmas=default_conf['sqlite']['pragmas'])
        database.connect()
        database_proxy.initialize(database)
        database.create_tables([MyTable, TargetTable], safe=True)

        MyTable.delete().execute()
        TargetTable.delete().execute()

        # manually create a trigger
        trig = Trigger('mytable_after_insert', (TriggerWhen.After, TriggerAction.Insert), MyTable, safe=True)
        trig.add_sql('INSERT INTO target_table (id__id, half_float_num) VALUES (NEW.id_, NEW.float_num / 2)')
        database.execute_sql(trig.create())

        # add some data for testing to the first table
        data = []
        for i in range(100):
            data.append(dict(integer=random.randint(i, 10 * i), float_num=random.gauss(i, 2 * i)))
        MyTable.insert_many(data).execute()

        # check that the target table got the right entries
        for row in MyTable.select(MyTable.float_num, TargetTable.half_float_num).join(TargetTable).namedtuples():
            assert row.float_num == 2 * row.half_float_num

        assert MyTable.select().count() == TargetTable.select().count()


In lines 20 - 22, we create a trigger and we ask the database to execute the generated SQL statement.

We insert 100 rows using the insert many class method and the trigger is doing its job in the background filling the other table. We can check that the values in the two tables are matching our expectations.

The drawback of this approach is that you may have triggers created all around your code, making your code a bit messy.

.. _model_embedded_triggers:

Model embedded triggers
^^^^^^^^^^^^^^^^^^^^^^^

An alternative approach is to define the trigger within the Model class, allowing it to be created simultaneously with model table. This is demonstrated in the code example below.

.. code-block:: python
    :linenos:
    :name: test_automatically_created_trigger
    :caption: A test Trigger created within the Model
    :emphasize-lines: 8-13,22

    # the trigger is directly defined in the class.
    class MyTable(MAFwBaseModel):
        id_ = AutoField(primary_key=True)
        integer = IntegerField()
        float_num = FloatField()

        @classmethod
        def triggers(cls):
            return [
                Trigger('mytable_after_insert', (TriggerWhen.After, TriggerAction.Insert), cls, safe=True).add_sql(
                    'INSERT INTO target_table (id__id, half_float_num) VALUES (NEW.id_, NEW.float_num / 2)'
                )
            ]

    class TargetTable(MAFwBaseModel):
        id_ = ForeignKeyField(MyTable, on_delete='cascade', primary_key=True, backref='half')
        half_float_num = FloatField()

    database: Database = SqliteDatabase(':memory:', pragmas=default_conf['sqlite']['pragmas'])
    database.connect()
    database_proxy.initialize(database)
    database.create_tables([MyTable, TargetTable], safe=True)

This approach is much cleaner. The Trigger is stored directly in the Model (lines 8 - 13). In the specific case, the triggers method returned one trigger only, but you can return as many as you like. When the tables are created (line 22), all the triggers will also be created.

In the example above, you have written the SQL statement directly, but nobody is preventing you to use :link:`peewee` queries for this purpose. See below, how exactly the same trigger might be re-written, using an insert statement:

.. code-block:: python
    :linenos:
    :name: test_automatically_created_trigger_with_peewee_query
    :caption: A test Trigger created within the Model using an Insert statement
    :emphasize-lines: 9, 13-14

    class MyTable(MAFwBaseModel):
        id_ = AutoField(primary_key=True)
        integer = IntegerField()
        float_num = FloatField()

        @classmethod
        def triggers(cls):
            trigger = Trigger('mytable_after_insert', (TriggerWhen.After, TriggerAction.Insert), cls, safe=True)
            sql = TargetTable.insert(id_=SQL('NEW.id_'), half_float_num=SQL('NEW.float_num/2'))
            trigger.add_sql(sql)
            return [trigger]

        class Meta:
            depends_on = [TargetTable]

The key point here is at line 9, where the actual insert statement is generated by :link:`peewee` (just for your information, you have generated the statement, but you have not *execute it*) and added to the existing trigger.

In the last two highlighted lines, we are overloading the Meta class, specifying that MyTable, depends on TargetTable, so that when the create_tables is issued, they are built in the right order. This is not necessary if you follow the previous approach because the trigger will be very likely executed only after that the tables have been created.

.. warning::

    Even though starting from MAFw release v1.1.0, triggers are now properly generated for the three main :ref:`database backends <trigger_on_different_dbs>`, its use has been deeply tested only with SQLite. For this reason, we (MAFw developers) encourage the user community to work also with other DBs and, in case, submit bugs or feature request.


Disabling triggers
^^^^^^^^^^^^^^^^^^

Not all database implementations provide the same option to temporarily disable one or more triggers. In order to cope with this limitation, MAFw is providing a general solution that is always working independently of the concrete implementation of the database.

The standard SQL trigger definition allows to have one or more WHEN clauses [#]_, meaning that the firing of a trigger script might be limited to the case in which some other external conditions are met.

In order to achieve that, we use one of our :ref:`standard tables <std_tables>`, that are automatically created in every MAFw database.

This is the TriggerStatus table as you can see it in the snippet below:

.. literalinclude:: ../../src/mafw/db/std_tables.py
    :dedent:
    :pyobject: TriggerStatus
    :name: TriggerStatus
    :caption: TriggerStatus model


You can use the ``trigger_type`` column to specify a generic family of triggers (DELETE/INSERT/UPDATE) or the name of a specific trigger. By default a trigger is active (status = 1), but you can easily disable it by changing its status to 0.

To use this functionality, the Trigger definition should include a WHEN clause as described in this modified model definition.

.. code-block:: python
    :name: MyTableTriggerWhen
    :caption: Trigger definition with when conditions.

    class MyTable(MAFwBaseModel):
        id_ = AutoField(primary_key=True)
        integer = IntegerField()
        float_num = FloatField()

        @classmethod
        def triggers(cls):
            return [
                Trigger('mytable_after_insert', (TriggerWhen.After, TriggerAction.Insert), cls, safe=True)
                .add_sql('INSERT INTO target_table (id__id, half_float_num) VALUES (NEW.id_, NEW.float_num / 2)')
                .add_when('1 == (SELECT status FROM trigger_status WHERE trigger_type == "INSERT")')
            ]

To facilitate the temporary disabling of a specific trigger family, MAFw provides a special class
:class:`~.TriggerDisabler` that can be easily used as a context manager in your code. This is an ultra simplified
snippet.

.. code-block:: python
    :name: TriggerDisablerContext
    :caption: Use of a context manager to disable a trigger

    with TriggerDisabler(trigger_type_id = 1):
        # do something without triggering the execution of any trigger of type 1
        # in case of exceptions thrown within the block, the context manager is restoring
        # the trigger status to 1.

.. _trigger_on_different_dbs:

Triggers on different databases
+++++++++++++++++++++++++++++++

We have seen that Peewee provides an abstract interface that allows interaction with various SQL databases
like :link:`MySQL`, :link:`PostgreSQL`, and :link:`SQLite`.

This abstraction simplifies database operations by enabling the same codebase to work across different
database backends, thanks to the common SQL language they all support. However, while these databases share SQL as
their query language, they differ in how they handle certain features, such as triggers. Each database has its own
peculiarities and syntax for defining and managing triggers, which can lead to inconsistencies when using a single
approach across all databases.

To address this challenge, the MAFw introduced the :class:`.TriggerDialect` abstract class and three specific
implementations for the main databases. Relying on the use of the TriggerDialect class, a syntactically correct SQL
statement for the creation or removal of triggers is generated. But, MAFw cannot read the mind of the user (yet!) and
given the very different behaviour of the databases, the operation of the triggers will be different.

Have a look at the table below for an illustrative comparison on how triggers are handled by the different databases.

.. list-table::
    :width: 100%
    :widths: 15 28 28 28
    :header-rows: 1
    :stub-columns: 1
    :class: wrap-table

    * - Feature
      - MySQL
      - PostgreSQL
      - SQLite
    * - Trigger Event
      -  - INSERT
         - UPDATE
         - DELETE
      -  - INSERT
         - UPDATE
         - DELETE
         - TRUNCATE
      -  - INSERT
         - UPDATE
         - DELETE
    * - Trigger Time
      - - BEFORE
        - AFTER
      - - BEFORE
        - AFTER
        - INSTEAD OF
      - - BEFORE
        - AFTER
        - INSTEAD OF
    * - Activation
      - Row-level only
      - Row-level and statement-level
      - Row-level and statement-level
    * - Implementation
      - BEGIN-END block with SQL statements
        (supports non-standard SQL like SET statements)
      - Functions written in PL/pgSQL, PL/Perl, PL/Python, etc.
      - BEGIN-END block with SQL  statements
    * - Trigger Per Event
      - Multiple triggers allowed ordered by creation time
      - Multiple triggers allowed ordered alphabetically by default, can be specified
      - Multiple triggers allowed but unspecified execution order
    * - Privileges required
      - TRIGGER privilege on the table and SUPER or SYSTEM_VARIABLES_ADMIN for DEFINER
      - CREATE TRIGGER privilege on schema and TRIGGER privilege on table
      - No specific privilege model
    * - Foreign Key Cascading
      - Cascaded foreign key actions do not activate triggers
      - Triggers are activated by cascaded foreign key actions
      - Triggers are activated by cascaded foreign key actions
    * - Disabled/Enabled Trigger
      - Yes, using ALTER TABLE ... DISABLE/ENABLE TRIGGER
      - Yes, using ALTER TABLE ... DISABLE/ENABLE TRIGGER
      - No direct mechanism to disable

PostgreSQL offers the most comprehensive trigger functionality, with built-in support for both row-level and
statement-level triggers, INSTEAD OF triggers for views, and the widest range of programming languages for
implementation. Its trigger functions can be written in any supported procedural language, providing considerable
flexibility.

MySQL implements triggers using SQL statements within BEGIN-END blocks and only supports row-level
triggers. It allows non-standard SQL statements like SET within trigger bodies, making it somewhat more flexible for
certain operations. A critical limitation is that MySQL triggers are not activated by cascaded foreign key actions,
unlike the other databases. This is a strong limiting factor and the user should consider it when designing the
database model to store their data. In this case, it might be convenient to not rely at all on the cascading
operations, but to have dedicated triggers for this purpose.

SQLite provides more trigger capabilities than it might initially appear. While its
implementation is simpler than PostgreSQL's, it supports both row-level and statement-level triggers (statement-level
being the default if FOR EACH ROW is not specified). Like PostgreSQL, SQLite triggers are activated by cascaded
foreign key actions, which creates an important behavioral difference compared to MySQL.

When designing database applications that may need to work across different database systems, these implementation
differences can lead to subtle bugs, especially around foreign key cascading behavior. MySQL applications that rely
on triggers not firing during cascaded operations might behave differently when migrated to PostgreSQL or SQLite.
Similarly, applications that depend on statement-level triggers will need to be redesigned when moving from
PostgreSQL or SQLite to MySQL.

All so said, even though MAFw provides a way to handle triggers creation and removal in the same way across all the
databases, the user who wants to move from one DB implementation to the other should carefully review the content of
the trigger body to ensure that the resulting behavior is what is expected.


Debugging triggers
++++++++++++++++++

The challenges connected to debugging triggers have been already mentioned several times. It is a block of code that is executed outside the application in full autonomy and you cannot put a breakpoint in the database.  If you see that your code is not behaving as expected and you doubt that triggers can be behind the malfunctioning, then the general recommendation is to proceed one step at the time, trying to simplify as much as possible the trigger function.

In all these cases, you will need to drop the triggers from the database and recreate them with the simplified / corrected implementation. This is a bit annoying because it cannot be done directly from the application because very likely you have :ref:`embedded <model_embedded_triggers>` your triggers in the target class, so you have no way to retrieve them.

The solution is to use the :class:`.TriggerRefresher` processor. It will take care of dropping all triggers in the database and recreate them from the corresponding model definition. The idea of dropping something is generally rather scary, because it is a undoable operation; but if you put all your trigger definitions inside the various models and they are all subclasses of :class:`.MAFwBaseModel`, then they will all recreated using their latest definition.

You can even leave the :class:`.TriggerRefresher` processor in your analysis pipelines all the times!

.. _std_tables:

Standard tables
---------------

In the previous section, we discussed a workaround implemented by MAFw to address the limitations of database backends that cannot temporarily disable trigger execution. This is achieved querying a table where the status of a specific trigger or a family of triggers can be toggled from active to inactive and vice-versa.

This :class:`~mafw.db.std_tables.TriggerStatus` model is one of the so-called MAFw standard tables,

The main differences between a Model inheriting from :class:`.MAFwBaseModel` and one inheriting from :class:`.StandardTable` are two:

    1. A standard table has an additional :meth:`initialisation method <.StandardTable.init>`, that can be used to set or restore the default content of the table.
    2. Automatic creation and initialisation performed by MAFw when the database connection is established. In other words, as soon as your processor connect to a database, it will retrieve from the :class:`.ModelRegister` all the standard tables, create them and initialise them.

.. note::

    To avoid useless multiple creation and initialisation of standard tables, only the first :class:`.Processor` or :class:`.ProcessorList` that is establishing a connection to the database, is taking the responsibility to proceed with the standard table creation and initialisation task.

    This means that if you manually connect to a database and you pass the database object to your :class:`.Processor`/:class:`.ProcessorList`, then the standard table creation and initialisation will be skipped, because your :class:`.Processor`/:class:`.ProcessorList` will think that it was already done when the database connection was established.

    The automatic creation and initialisation can be disabled, either using the :attr:`.Processor.create_standard_tables` argument in the :class:`.Processor` or :class:`.ProcessorList` constructor, or, if you run the pipelines via the mafw executables using the top level `create_standard_table` variable in your steering file.


The role of those tables is to support the functionality of the whole analysis pipeline, they are rarely the direct input / output of a specific processor. If you want to add your own, just create a model inheriting from :class:`.StandardTable` or make your own subclass, to customize for example the prefix, and the automatic registration in the model register will do the trick.


Default standard tables
+++++++++++++++++++++++

Along with the TriggerStatus, there are two other relevant standard tables: the :class:`~mafw.db.std_tables.OrphanFile` and the :class:`~mafw.db.std_tables.PlotterOutput`.


    :class:`~mafw.db.std_tables.OrphanFile`: the house of files without a row

        This table can be profitably used in conjunction with Triggers. The user can define a trigger fired when a row in a table is deleted. The trigger will then insert all file references contained in the deleted row into the OrphanFile model.

        The next time a processor (it does not matter which one) having access to the database is executed, it will query the full list of files from the :class:`~mafw.db.std_tables.OrphanFile` and remove them.

        This procedure is needed to avoid having files on your disc without a reference in the database. It is kind of a complementary cleaning up with respect to :func:`another function <mafw.tools.file_tools.remove_widow_db_rows>` you will discover in a moment.

        Additional details about this function are provided directly in the :func:`API <mafw.processor.Processor._remove_orphan_files>`.

    :class:`~mafw.db.std_tables.PlotterOutput`: where all figures go.

        :class:`Plotters <mafw.processor_library.sns_plotter.SNSPlotter>` are special |processor| subclasses with the goal of generating a graphical representation of some data you have produced in a previous step.

        The output of a plotter is in many cases one or more figure files and instead of having to define a specific table to store just one line, MAFw is providing a common table for all plotters where they can store the reference to their output files linked to the plotter name.

        It is very useful because it allows the user to skip the execution of a plotter if its output file already exists on disc.

        Triggers are again very relevant, because when a change is made in the data used to generate a plotter output, then the corresponding rows in this table should also be removed, in order to force the regeneration of the output figures with the updated data.

.. _mafw_fields:

Custom fields
-------------

We have seen in a previous section that there are plenty of field types for you to build up your model classes and that it is also possible to add additional `ones <http://docs.peewee-orm.com/en/latest/peewee/models.html#fields>`_. We have made a few for you that are very useful from the point of view of MAFw. The full list is available :mod:`here <mafw.db.fields>`.

The role of the database in MAFw is to support the input / output operation. You do not need to worry about specifying filenames or paths. Simply instruct the database to retrieve a list of items, and it will automatically provide the various processors with the necessary file paths for analysis.

With this in mind, we have created a :class:`~mafw.db.fields.FileNameField`, that is the evolution of a text field accepting a Path object as a python type and converting it into a string for database storage. On top of :class:`~mafw.db.fields.FileNameField`, we have made :class:`~mafw.db.fields.FileNameListField` that can contain a list of filenames. This second one is more appropriate when your processor is generating a group of files as output. The filenames are stored in the database as a ';' separated string, and they are seen by the python application as a list of Path objects.

Similarly, we have also a :class:`~mafw.db.fields.FileChecksumField` to store the string of hexadecimal characters corresponding to the checksum of a file (or a list of files). From the python side, you can assign either the checksum directly, as generated for example by :func:`~mafw.tools.file_tools.file_checksum` or the path to the file, and the field will calculate the checksum automatically.

The :class:`~mafw.db.fields.FileNameField` and :class:`~mafw.db.fields.FileNameListField` accept an additional argument in their constructor, called ``checksum_field``. If you set it to the name of a :class:`~mafw.db.fields.FileChecksumField` in the same table, then you do not even have to set the value of the checksum field because this will be automatically calculated when the row is saved.

With these custom fields in mind, our initial definition of a :ref:`File table <file_first>`, can be re-factored as follows:

.. code-block:: python
    :name: file_second
    :linenos:

    from peewee import AutoField

    from mafw.db.db_model import MAFwBaseModel
    from mafw.db.fields import FileNameField, FileChecksumField

    class File(MAFwBaseModel):
        file_id = AutoField(primary_key=True, help_text='The primary key')
        file_name = FileNameField(checksum_field='file_digest', help_text='The full filename')
        file_digest = FileChecksumField(help_text='The hex digest of the file')

Pay attention at the definition of the file_name field. The FileNameField constructor takes an optional parameter ``checksum_field`` that is actually pointing to the variable of the FileChecksumField.

You can use the two custom fields as normal, for example you can do:

.. code-block:: python
    :linenos:
    :emphasize-lines: 5,6

    new_file = File()
    # you can assign a Path object.
    new_file.file_name = Path('/path/to/some/file')
    # the real checksum will be calculated automatically.
    # this next line is totally optional, you can leave it out and it will work in the same way.
    new_file.file_digest = Path('/path/to/some/file')

The super power of these two custom fields is that you can remove useless rows from the database, just issuing one command.

Removing widow rows
+++++++++++++++++++
Due to its I/O support, the database content should always remain aligned with the files on your disc. If you have a row in your database pointing to a missing file, this may cause troubles, because sooner or later, you will try to access this missing file causing an application crash.

In MAFw nomenclature, those rows are called *widows*, following a similar concept in `typesetting <https://en.wikipedia.org/wiki/Widows_and_orphans>`_, because they are a fully valid database entry, but their data counter part on disc disappeared.

To avoid any problem with widow rows, MAFw is supplying a :func:`function <mafw.tools.file_tools.remove_widow_db_rows>` that the processor can invoke in the start method on the Model classes used as input:

.. code-block:: python

    class MyProcessor(Processor):

        def start():
            super().start()
            remove_widow_db_rows(InputData)

The :func:`~mafw.tools.file_tools.remove_widow_db_rows` will check that all the :class:`~mafw.db.fields.FileNameField` fields in the table are pointing to existing files on disc. If not, then the row is removed from the database.

The function is not automatically called by any of the Processor super methods. It is up to the user to decide if and when to use it. Its recommended use is in the overload of the :meth:`~.Processor.start` method or as a first action in the :meth:`~.Processor.get_items` in the case of a *for loop* workflow, so that you are sure to re-generate the rows that have been removed.

Pruning orphan files
++++++++++++++++++++
The opposite situation is when you have a file on disc that is not linked to an entry in the database anymore. This situation could be even more perilous than the previous one and may occur more frequently than you realize. The consequences of this mismatch can be severe, imagine that during the *testing / development phase* of your |processor| you generate an output figure saved on disc. You then realize that the plot is wrong and you fix the bug and update the DB, but for some reasons you have forgotten to delete the figure file from the disc. Afterwards, while looking for the processor output, you find this file and believe it is a valid result and you use it for your publication.  In order to prevent this to happen, you just have to follow some simple rules, and then the reliable machinery of MAFw will do the rest.

The key point is to use a specific trigger in every table that has a file name field. This trigger has to react before any delete query on such a table and inserting all FileNameFields or FileNameListFields in the OrphanFile table. You will see an example of such a trigger in the next paragraphs. This standard tables will be queried by the next processor being executed and during the start super method, all files in the Orphan table will be removed from the disc.

Let us try to understand this better with a step-by-step example. For simplicity, we have removed the import statements from the code snippet, but it should not be too difficult to understand the code anyway.

We begin with the declaration of our input model:

.. code-block:: python
    :name: FileWithTrigger
    :caption: File model definition with trigger

    class File(MAFwBaseModel):
        file_id = AutoField(primary_key=True, help_text='primary key')
        file_name = FileNameField(checksum_field='check_sum', help_text='the file name')
        check_sum = FileChecksumField(help_text='checksum')

        @classmethod
        def triggers(cls) -> list[Trigger]:
            file_delete_file = Trigger(
                'file_delete_file',
                (TriggerWhen.Before, TriggerAction.Delete),
                source_table=cls,
                safe=True,
                for_each_row=True,
            )
            file_delete_file.add_when('1 == (SELECT status FROM trigger_status WHERE trigger_type = "DELETE_FILES")')
            file_delete_file.add_sql(OrphanFile.insert(filenames=SQL('OLD.file_name'), checksum=SQL('OLD.file_name')))
            return [file_delete_file]

        class Meta:
            depends_on = [OrphanFile]


Here you see the trigger definition: it is a before delete type and when triggered it is adding the filename field to the OrphanFile table. It is important to notice that this trigger has a when condition and will only be executed when the trigger type DELETE_FILES is enabled. This is necessary for the pruning mechanism to work, just copy this line in your trigger definition.

And now let us define some fake processors. First we import some files into our model, then we remove some rows from the file table and finally other two processors, doing nothing but useful to demonstrate the effect of the orphan removal.

.. code-block:: python
    :name: ProcessorDefinition
    :caption: Some example processors

    @database_required
    class FileImporter(Processor):
        input_folder = ActiveParameter('input_folder', default=Path.cwd(), help_doc='From where to import')

        def __init__(self, *args, **kwargs):
            super().__init__(*args, looper=LoopType.SingleLoop, **kwargs)
            self.n_files: int = -1

        def start(self):
            super().start()
            self.database.create_tables([File])
            File.delete().execute()

        def process(self):
            data = [(f, f) for f in self.input_folder.glob('**/*dat')]
            File.insert_many(data, fields=['file_name', 'check_sum']).execute()
            self.n_files = len(data)

        def finish(self):
            super().finish()
            if File.select().count() != self.n_files:
                self.processor_exit_status = ProcessorExitStatus.Failed

    @database_required
    class RowRemover(Processor):
        n_rows = ActiveParameter('n_rows', default=0, help_doc='How many rows to be removed')

        def __init__(self, *args, **kwargs):
            super().__init__(*args, looper=LoopType.SingleLoop, **kwargs)
            self.n_initial = 0

        def start(self):
            super().start()
            self.database.create_tables([File])

        def process(self):
            self.n_initial = File.select().count()
            query = File.select().order_by(fn.Random()).limit(self.n_rows).execute()
            ids = [q.file_id for q in query]
            File.delete().where(File.file_id.in_(ids)).execute()

        def finish(self):
            super().finish()
            if File.select().count() != self.n_initial - self.n_rows or OrphanFile.select().count() != self.n_rows:
                self.processor_exit_status = ProcessorExitStatus.Failed

    @orphan_protector
    @database_required
    class OrphanProtector(Processor):
        def __init__(self, *args, **kwargs):
            super().__init__(looper=LoopType.SingleLoop, *args, **kwargs)
            self.n_orphan = 0

        def start(self):
            self.n_orphan = OrphanFile.select().count()
            super().start()

        def finish(self):
            super().finish()
            if OrphanFile.select().count() != self.n_orphan:
                self.processor_exit_status = ProcessorExitStatus.Failed

    @single_loop
    class LazyProcessor(Processor):
        def finish(self):
            super().finish()
            if OrphanFile.select().count() != 0:
                self.processor_exit_status = ProcessorExitStatus.Failed

The **FileImporter** [#]_ is very simple, it reads all dat files in a directory and loads them in the File model along with their checksum. Just to be sure we empty the File model in the start and in the finish we check that the number of rows in File is the same as the number of files in the folder.

The **RowRemover** is getting an integer number of rows to be removed. Even though the File model is already created, it is a good practice to repeat the statement again in the start method. Then we select some random rows from File and we delete them. At this point, we have created some orphan files on disc without related rows in the DB.
Finally (in the finish method), we verify that the number of remaining rows in the database aligns with our expectations. Additionally, we ensure that the trigger functioned correctly, resulting in the appropriate rows being added to the OrphanFile model.

The **OrphanProtector** does even less than the others. But if you look carefully, you will see that along with the :func:`~mafw.decorators.database_required` there is also the :func:`~mafw.decorators.orphan_protector` decorator. This will prevent the processor to perform the check on the OrphanFile model and deleting the unrelated files.
In the start method, we record the number of orphan files in the OrphanFile model and we confirm that they are still there in the finish. Since the actual removal of the orphan files happens in the processor start method, we need to count the number of orphans before calling the super start.

The **LazyProcessor** is responsible to check that there are no rows left in the OrphanFile, meaning that the removal was successful.

And now let us put everything together and run it.

.. code-block:: python
    :name: execution
    :caption: ProcessorList execution

    db_conf = default_conf['sqlite']
    db_conf['URL'] = 'sqlite:///:memory:'
    plist = ProcessorList(name='Orphan test', description='dealing with orphan files', database_conf=db_conf)
    importer = FileImporter(input_folder=tmp_path)
    remover = RowRemover(n_rows=n_delete)
    protector = OrphanProtector()
    lazy = LazyProcessor()
    plist.extend([importer, remover, protector, lazy])
    plist.execute()

    assert importer.processor_exit_status == ProcessorExitStatus.Successful
    assert remover.processor_exit_status == ProcessorExitStatus.Successful
    assert protector.processor_exit_status == ProcessorExitStatus.Successful
    assert lazy.processor_exit_status == ProcessorExitStatus.Successful


In practice, the only thing you have to take care of is to add a dedicated trigger to each of your tables having at least a file field and then the rest will be automatically performed by MAFw.

.. warning::

    You should be very careful if your processor is removing rows from the target table (where you should be storing the processor's results). This might be the case of a processor that wants to reset the status of your analysis to a previous step, for example. In this case, as soon as `ProcessorA` removes the rows from the model, the trigger will inserts all FileNameFields in the OrphanFile model in order to be deleted. This is a lazy operation and will be performed by the following processor to be executed either in the same pipeline or in the next. When `ProcessorA` will have finished its work, the target table will be repopulated and the same will happen to the folders on the disc. Now the next processor will empty the orphan file model and possibly remove the freshly generated files.

    You have two solutions for this problem: either you block the execution of the trigger when deleting the rows (you can use the :class:`~.TriggerDisabler` for this purpose), in this way the rows in the model will be removed, but not the files from disc with the risks we have already mentioned. The second possibility is to force the processor to immediately take care of the orphan file pruning. This is the suggested procedure and you only need to include a call to the :meth:`~.Processor._remove_orphan_files` soon after the delete query.

.. _auto_triggers:

Automatic creation of *file removal* trigger
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the definition of :ref:`File model <FileWithTrigger>` we have manually created a trigger that is fired every time a row is removed from the table. The action of this trigger is to insert in the :class:`.OrphanFile` model the content of the :class:`.FileNameField` that is actually the specifically designed Field type to store a path to a file.

This trigger creation part can be totally automatized, if you want to insert in the :class:`.OrphanFile` the content of all :class:`.FileNameField` and :class:`.FileNameListField` fields. The automatic creation is another advantage of using the :class:`.MAFwBaseModel`. This functionality can be activated very simply by setting a flag in the metadata class.

.. code-block:: python
    :name: FileWithAutoTrigger
    :caption: File model definition with automatic trigger

    class File(MAFwBaseModel):
        file_id = AutoField(primary_key=True, help_text='primary key')
        file_name = FileNameField(checksum_field='check_sum', help_text='the file name')
        check_sum = FileChecksumField(help_text='checksum')

        class Meta:
            depends_on = [OrphanFile]
            file_trigger_auto_create = True

This model class is absolutely identical to the :ref:`previous one <FileWithTrigger>`; MAFw base model will take care of generating the necessary trigger.

It is worth remembering that `file_trigger_auto_create` is inherited by subclasses, so if you want all the models in your project to have this feature, you can simply set it to true in your base model.

.. warning::

    We have already mentioned the main disadvantage of working with triggers, that is to say the difficult debugging. Triggers are pieces of code that are executed in full autonomy by the database, so when you are trying to understand why your analysis pipeline is not working as expected a part from looking at your python code, you should also keep in mind that triggers might be the source of the problem.

    This effect is amplified, if you turn on the automatic trigger creation, because you don't even see the trigger definition in your python code and you may have forgotten about the auto trigger flag. As always with great power comes even greater responsibility!

.. _verify_checksum:

Keeping the entries updated
+++++++++++++++++++++++++++
One aspect is that the file exists; another is that the file content remains unchanged. You may have replaced an input file with a newer one and the database will not know it. If your processors are only executed on items for which there is still no output generated, then this replaced file may go unnoticed causing issues to your analysis.

For this reason, we are strongly recommending to always add a checksum field for each file field in your table. Calculating a checksum is just a matter of a split second on modern CPU while the time for the debugging your analysis code is for sure longer.

The function :func:`~mafw.tools.file_tools.verify_checksum` takes a Model as argument and will verify that all checksums are still valid. In other words, for each FileNameField (or FileNameListField) with a link to a checksum field in the table, the function will compare the actual digest with the stored one. If it is different, then the DB row will be removed.

Also this function is not automatically called by any processor super methods. It is ultimately the user's responsibility to decide whether to proceed, bearing in mind that working with long tables and large files may result in delays in processor execution.

The implementation is very similar to the previous one, just change the function name. Keep in mind that the :func:`~mafw.tools.file_tools.verify_checksum` will implicitly check for the existence of files and warn you if some items are missing, so you can avoid the :func:`~mafw.tools.file_tools.remove_widow_db_rows`, if you perform the checksum verification.

.. code-block:: python

    class MyProcessor(Processor):

        def start():
            super().start()
            verify_checksum(InputData)



.. _multi_primary:

Multi-primary key columns
-------------------------

Special attention is required when you need to have a primary key that is spanning over two or more columns of your model. So far we have seen how we can identify one column in the model as the primary key and now we will see what to do if you want to use more than one column as primary key and, even more important, how you can use this composite primary key as a foreign key in another model.

To describe this topic, we will make use of an example that you can also find in the examples modules of MAFw named :mod:`~mafw.examples.multi_primary`.

Let us start with the model definition.

.. literalinclude:: ../../src/mafw/examples/multi_primary.py
    :name: multi_primary_models
    :linenos:
    :dedent:
    :start-at: class Sample(MAFwBaseModel
    :end-before: # end of model
    :emphasize-lines: 35-50, 57-58, 53-55, 72-77

As always, one single picture can convey more than a thousand lines of code. Here below the ERDs of Image and of CalibratedImage.

.. figure:: /_static/images/db/multi-erd1.png
    :width: 600
    :align: center
    :alt: Image ERD

    The ERD of the Image Model

.. figure:: /_static/images/db/multi-erd2.png
    :width: 600
    :align: center
    :alt: CalibratedImage ERD

    The ERD of the CalibratedImage Model

In the diagrams, the fields with bold font represent primary keys, also highlighted by the separation line, while the arrow are the standard relation.

As in the examples above, we have images of different samples acquired with different resolutions entering the Image model. We use those lines to make some calculations and we obtain the rows in the ProcessedImage model. These two tables are in 1 to 1 relation and this relation is enforced with a delete cascade, meaning that if we delete an element in the Image model, the corresponding one in the ProcessedImage will also be deleted.

The CalibrationMethod model contains different sets of calibration constants to bring each row from the ProcessedImage model to the CalibratedImage one. It is natural to assume that the ``image_id`` and the ``method_id`` are the best candidates to be a combined primary key.
To achieve this, in the CalibratedImage model, we need to add (line 57-58) an overload of the Meta class, where we specify our ``CompositeKey``. Pay attention to an important detail: the CompositeKey constructor takes the name of the fields and not the name of the columns, that in the case of foreign keys differ of '_id'. Optionally we can also define a primary_key property (line 53-55) to quickly retrieve the values of our keys.

From the application point of view, we want all the processed images to be calibrated with all possible calibration methods, that means we need to make a cross join as described below:

.. literalinclude:: ../../src/mafw/examples/multi_primary.py
    :linenos:
    :dedent:
    :start-after: # make the multi calibration
    :end-at: calibrated_image.save(force_insert=True)


Up to this point we have seen what we have to do to specify a composite primary key, we cannot use the AutoField or the primary_key parameter, but we need to go through the Meta class in the way shown in the example.

The next step is to have another table (ColoredImage in our imaginary case) that is in relation with CalibratedImage. We would need to have again a composite primary key that is also a composite foreign key. :link:`Peewee` does not support composite foreign keys, but we can use the workaround shown at lines 72-77. Along with the CompositeKey definition, we need to add a Constraint as well using the SQL function to convert a string into a valid SQL statement. This time, since we are using low level SQL directives, we have to use the column names (additional '_id') instead of the field name.

And in a similar way we can insert items in the ColoredImage model.

.. literalinclude:: ../../src/mafw/examples/multi_primary.py
    :linenos:
    :dedent:
    :start-after: # fill in the ColoredImage
    :end-at: colored_image.save(force_insert=True)

Now, with all the tables linked to each other, try to delete one from a table, and guess what will happen to all other tables.

This tutorial might be a bit more complex than the examples we have seen so far, but we believed you have appreciated the power of such a relational tool.



Importing an existing DB
------------------------

The last section of this long chapter on database will show you how to deal with an existing DB. It is possible that before you have adopted MAFw for your analysis tasks, you were already employing a relational database to store your dataset and results. So far we have seen how to create tables in a database starting from an object oriented description (a model) in a python library. But what do we have to do if the database already exists? Can we create the classes starting from a database? This process goes under the name of **reflection** and it is the subject of this section.

The reflection of tables in python classes cannot be performed automatically at 100% by definition. A typical case is the use of application specific fields. Consider, for example, the FileNameField that we have discussed earlier. This field corresponds to a Path object when you look at it from the application point of view, but the actual path is saved as a text field in the concrete database implementation. If you now read the metadata of this table from the database point of view, you will see that the field will contain a text variable and thus the reflected class will not have any FileNameField.

Let us try to understand the process looking at the picture below. If we create the model in python, then we can assign special field descriptors to the table columns, but their concrete implementation in the database must be done using types that are available in the database itself. So when we perform the reverse process, we get only a good approximation of the initial definition.

.. figure:: /_static/images/db/reflection-original.png
    :name: reflection-original
    :width: 350
    :align: center
    :alt: Original implementation

    This is the model implementation as you would code it making use of the specific field definitions.

.. figure:: /_static/images/db/database-implementation.png
    :name: database-implementation
    :width: 150
    :align: center
    :alt: Database implementation

    During the actual implementation of the model as a database table, python column definitions will be translated into database types.

.. figure:: /_static/images/db/reflection-reflected.png
    :name: reflection-reflected
    :width: 350
    :align: center
    :alt: Reflected implementation

    The reflection process will translate the database implementation in a generic model implementation, not necessarily including all the specific field definition.

Nevertheless the process is rather efficient and can generate an excellent starting point that we can use to customize the model classes to make them more useful in our application.

From a practical point of view, you just have to open a console and type the command ``mafw db wizard --help`` to get some help on the tool and also read its `documentation <generated/mafw.scripts.mafw_exe.html#mafw-db-wizard>`_. You need to provide the name of the database and how to connect to it, in the case of Sqlite DB, it is enough to provide the filename, and you have to specify the name of the output python file that will contain all the model classes. This module is ready to go, you could theoretically import it into your project and use it, but it is strongly recommended to accurately check that everything is really the way you want it to be.

The reflection process is absolutely safe for your existing database, so it is worth to give it a try!

.. _script_execution:

Execute SQL scripts
-------------------

If you are not new to databases, you might have some SQL script files hanging around. Something link initialisation or optimisation procedure. If this is the case, you can include those in your analysis pipelines.

The :class:`~mafw.processor_library.db_init.SQLScriptRunner` processor provides a convenient way to execute SQL scripts against your database. This is particularly useful when you need to perform database operations that are not easily expressed through the ORM or when you want to leverage database-specific features.

To use the SQLScriptRunner, you need to configure it in your steering file by specifying a list of SQL files to be processed. Here's an example configuration:

.. code-block:: toml

    [SQLScriptRunner]
    sql_files = ["./scripts/init_schema.sql", "./scripts/populate_data.sql"]

The processor will:

1. Validate that all specified SQL files exist and are regular files
2. Read each SQL file content
3. Remove multi-line block comments (`/* ... */`) from the SQL content
4. Split the content into individual SQL statements
5. Execute all statements within a single atomic transaction

This ensures that either all statements are executed successfully, or none are applied if an error occurs, maintaining database integrity.

Each SQL file should contain one or more valid SQL statements separated by semicolons. The processor automatically handles the transaction boundaries, so you don't need to include explicit BEGIN/COMMIT statements in your SQL files.

.. warning::

    Since all statements are executed within a single transaction, very large SQL files or operations that take a long time to complete might impact database performance. Consider breaking large scripts into smaller chunks if needed.


What's next
-----------

Congratulations! You reached the end of the most difficult chapter in this tutorial. It is difficult because as a scientist you might not be used to deal with databases everyday, but their power is incredible, isn't it?

The next chapter is about efficiency! You will learn how to process only the data you want and that need to be analysed. Get ready to understand database filters!

.. rubric:: Footnotes

.. [#] The automatic registration of a class at his definition is a nice piece of syntactic sugar obtained via the use metaclasses. See the :class:`API <.RegisteredMeta>` for more.

.. [#] MySQL does not directly support adding WHEN conditions to the trigger, but a similar behaviour is obtainable using an IF statement in the trigger SQL body. This adaptation is automatically implemented by the :class:`~.MySQLDialect`.

.. [#] In some databases, like :link:`mysql`, one can use the `schema` to group tables together.

.. [#] A much better implementation of an Importer could be achieved using a subclass of the :class:`~.Importer`. See, for example, the :class:`~.ImporterExample` class and its :ref:`documentation <importer>`.


