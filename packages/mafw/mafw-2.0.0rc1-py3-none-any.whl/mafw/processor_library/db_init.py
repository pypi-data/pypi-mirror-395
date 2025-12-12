#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Database initialisation processor module.

This module contains the following processors:

:class:`TableCreator`
    processor which handles the creation of database tables based on registered models. It provides functionality to
    create tables automatically while respecting existing tables and offering options for forced recreation.

:class:`TriggerRefresher`
    processor to safely update the trigger definitions. It removes all existing triggers and regenerates them
    according to the new definition. Particularly useful when debugging triggers, it can also be left at the
    beginning of all analysis pipelines since it does not cause any loss of data.

:class:`SQLScriptRunner`
    processor to execute SQL scripts from files against the database. It reads SQL files, removes block comments,
    splits the content into individual statements, and executes them within a transaction.

.. versionadded:: v2.0.0
"""

import logging
import re
from pathlib import Path
from typing import TYPE_CHECKING, Any, Collection, Optional

import peewee
from rich.prompt import Confirm, Prompt

from mafw.db.db_model import mafw_model_register
from mafw.db.std_tables import StandardTable
from mafw.db.trigger import MySQLDialect, PostgreSQLDialect, SQLiteDialect, TriggerDialect
from mafw.decorators import database_required, single_loop
from mafw.enumerators import LoopingStatus, ProcessorExitStatus
from mafw.mafw_errors import InvalidConfigurationError, UnsupportedDatabaseError
from mafw.processor import ActiveParameter, Processor

log = logging.getLogger(__name__)

block_comment_re = re.compile(r'/\*.*?\*/', re.DOTALL)


@database_required
@single_loop
class TableCreator(Processor):
    """
    Processor to create all tables in the database.

    This processor can be included in all pipelines in order to create all tables in the database. Its functionality
    is based on the fact that all :class:`.MAFwBaseModel` subclasses are automatically included in a global register
    (:data:`.mafw_model_register`).

    This processor will perform the following:

        #. Get a list of all tables already existing in the database.
        #. Prune from the lists of models the ones for which already exist in the database.
        #. Create the remaining tables.


    This overall behaviour can be modified via the following parameters:

        * *force_recreate* (bool, default = False): Use with extreme care. When set to True, all tables in the
          database and in the model register will be first dropped and then recreated. It is almost equivalent to a re-initialization of the
          whole DB with all the data being lost.

        * *soft_recreate* (bool, default = True): When set to true, all tables whose model is in the mafw model
          register will be recreated with the safe flag. It means that there won't be any table drop. If a table is
          already existing, nothing will happen. If a new trigger is added to the table this will be created. When
          set to False, only tables whose model is in the register and that are not existing will be created.

        * *apply_only_to_prefix* (list[str], default = []): This parameter allows to create only the tables that do
          not already exist and whose name start with one of the provided prefixes.

    .. versionadded:: v2.0.0

    """

    force_recreate = ActiveParameter(
        name='force_recreate', default=False, help_doc='First drop and then create the tables. LOSS OF ALL DATA!!!'
    )
    """
    Force recreate (bool, default = False).
    
    Use with extreme care. When set to True, all tables in the database and in the model register will be first 
    dropped and then recreated. It is almost equivalent to a re-initialization of the whole DB with all the data 
    being lost. 
    """

    soft_recreate = ActiveParameter(
        name='soft_recreate', default=True, help_doc='Safe recreate tables without dropping. No data loss'
    )
    """
    Soft recreate (bool default = True).
    
    When set to true, all tables whose model is in the mafw model register will be recreated with the safe flag. It 
    means that there won't be any table drop. If a table is already existing, nothing will happen. If a new trigger 
    is added to the table, this will be created. When set to False, only tables whose model is in the register and 
    that are not existing will be created.   
    """

    apply_only_to_prefix = ActiveParameter[list[str]](
        name='apply_only_to_prefix',
        default=[],
        help_doc='Create only tables whose name start with the provided prefixes.',
    )
    """
    Apply only to tables starting with prefix (list[str], default = []).
    
    This parameter allows to create only the tables that do not already exist and whose name start with one of the 
    provided prefixes. 
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.existing_table_names: list[str] = []
        """The list of all existing tables in the database."""

    def validate_configuration(self) -> None:
        """
        Configuration validation

        :attr:`force_recreate` and :attr:`soft_recreate` cannot be both valid.

        :raises InvalidConfigurationError: if both recreate types are True.
        """
        if self.force_recreate and self.soft_recreate:
            raise InvalidConfigurationError(
                'Both force_recreate and soft_recreate set to True. Incompatible configuration'
            )

    def process(self) -> None:
        """
        Execute the table creation process.

        This method performs the following steps:

            #. Identify all models that have automatic creation enabled.
            #. Filter models based on the apply_only_to_prefix parameter if specified.
            #. Handle forced recreation if requested, including user confirmation.
            #. Handle soft recreation if requested, letting all tables with a known model be recreated.
            #. Create the required tables.
            #. Initialise standard tables after recreation if needed.

        If user cancel the creation, the processor exit status is set to :attr:`.ProcessorExitStatus.Aborted` so that
        the whole processor list is blocked.
        """
        # get all tables with autocreation flag
        autocreation_table_names = [
            name
            for name, model in mafw_model_register.items()
            if model._meta.automatic_creation  # type: ignore[attr-defined]
        ]

        if self.apply_only_to_prefix:
            # remove tables with all given prefixes
            autocreation_table_names = [
                name
                for name in autocreation_table_names
                if any([name.startswith(prefix) for prefix in self.apply_only_to_prefix])  # type: ignore[union-attr]
            ]

        # in the case of force_recreation, we need to have user confirmation
        if self.force_recreate:
            log.warning(f'Forcing recreation of {len(autocreation_table_names)} tables in the database.')
            log.warning('All data in these tables will be lost.')

            with self._user_interface.enter_interactive_mode():
                question = 'Are you really sure?'
                if self._user_interface.name == 'rich':
                    question = '[red][bold]' + question + '[/red][/bold]'
                confirmation = self._user_interface.prompt_question(
                    question=question, prompt_type=Confirm, default=False, show_default=True, case_sensitive=True
                )
                if not confirmation:
                    self.processor_exit_status = ProcessorExitStatus.Aborted
                    return
                else:
                    log.info(f'Removing {len(autocreation_table_names)} tables from the database.')
                    models = [model for name, model in mafw_model_register.items() if name in autocreation_table_names]
                    self.database.drop_tables(models)  # type: ignore[arg-type]

        if self.soft_recreate:
            # recreate all tables in the mafw register
            models = [model for name, model in mafw_model_register.items() if name in autocreation_table_names]
        else:
            # recreate all tables in the mafw register and that are not yet existing
            self.existing_table_names = self.database.get_tables()
            models = [
                model
                for name, model in mafw_model_register.items()
                if name in autocreation_table_names and name not in self.existing_table_names
            ]
        self.database.create_tables(models)  # type: ignore[arg-type]

        if self.force_recreate:
            # in the case of a recreation, do the initialisation of all dropped standard tables.
            for model in models:
                if isinstance(model, type(StandardTable)):
                    model.init()

        n = len(models)
        if n > 0:
            if n == 1:
                plu = ''
            else:
                plu = 's'
            log.info(f'Successfully create {len(models)} table{plu}.')


@database_required
class TriggerRefresher(Processor):
    """
    Processor to recreate all triggers.

    Triggers are database objects, and even though they could be created, dropped and modified at any moment,
    within the MAFw execution cycle they are normally created along with the table they are targeting.

    When the table is created, also all its triggers are created,
    but unless differently specified, with the safe flag on, that means that they are created if they do not exist.

    This might be particularly annoying when modifying an existing trigger, because you need to manually drop the
    trigger to let the table creation mechanism to create the newer version.

    The goal of this processor is to drop all existing triggers and then recreate the corresponding tables so to have
    an updated version of the triggers.

    The processor is relying on the fact that all subclasses of :class:`.MAFwBaseModel`
    are automatically inserted in the :data:`.mafw_model_register` so that the model class can be retrieved from the
    table name.

    Before removing any trigger, the processor will build a list with all the affected tables and check if all of
    them are in the :data:`.mafw_model_register`, if so, it will proceed without asking any further confirmation.
    Otherwise, if some affected tables are not in the register, then it will ask the user to decide what to do:

        - Remove only the triggers whose tables are in the register and thus recreated afterward.
        - Remove all triggers, in this case, some of them will not be recreated.
        - Abort the processor.

    Trigger manipulations (drop and creation) are not directly implemented in :link:`peewee` and are an extension
    provided by MAFw. In order to be compatible with the three main databases (:link:`sqlite`, :link:`mysql` and
    :link:`postgresql`), the SQL generation is obtained via the :class:`.TriggerDialect` interface.

    .. seealso::

        The :class:`.Trigger` class and also the :ref:`trigger chapter <triggers>` for a deeper explanation on triggers.

        The :class:`.ModelRegister` class, the :data:`.mafw_model_register` and the :ref:`related chapter
        <auto_registration>` on the automatic registration mechanism.

        The :class:`.TriggerDialect` and its subclasses, for a database independent way to generate SQL statement
        related to triggers.

    .. versionadded:: v2.0.0
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.dialect: Optional[TriggerDialect] = None
        self.tables_to_be_rebuilt: set[str] = set()

    def get_dialect(self) -> TriggerDialect:
        """
        Get the valid SQL dialect based on the type of Database

        :return: The SQL trigger dialect
        :type: :class:`.TriggerDialect`
        :raises: :class:`.UnsupportedDatabaseError` if there is no dialect for the current DB.
        """
        if self.dialect is not None:
            return self.dialect

        if self._database is None:
            # Default to SQLite dialect
            return SQLiteDialect()

        db = self._database
        if isinstance(db, peewee.DatabaseProxy):
            db = db.obj  # Get the actual database from the proxy

        dialect: TriggerDialect
        if isinstance(db, peewee.SqliteDatabase):
            dialect = SQLiteDialect()
        elif isinstance(db, peewee.MySQLDatabase):
            dialect = MySQLDialect()
        elif isinstance(db, peewee.PostgresqlDatabase):
            dialect = PostgreSQLDialect()
        else:
            raise UnsupportedDatabaseError(f'Unsupported database type: {type(db)}')

        return dialect

    def start(self) -> None:
        super().start()
        self.dialect = self.get_dialect()

    def get_items(self) -> Collection[Any]:
        """
        Retrieves a list of database triggers and interacts with the user to determine which ones to process.

        This method fetches all currently defined database triggers. If any tables
        associated with these triggers are not known (i.e., not registered in
        :data:`.mafw_model_register`), it enters an interactive mode to prompt the user for
        a course of action:

        1.  **Remove All Triggers (A):** Processes all triggers for subsequent removal,
            but only marks 'rebuildable' tables for rebuilding.
        2.  **Remove Only Rebuildable Triggers (O):** Processes only triggers associated
            with 'rebuildable' tables.
        3.  **Quit (Q):** Aborts the entire process.

        If no unknown tables are found, or the user chooses to process rebuildable tables,
        the list of triggers and the set of tables to be rebuilt are prepared for the next stage.

        :return: A collection of database triggers to be processed, in the for tuple trigger_name, table_name
        :rtype: List[Tuple[str, str]]
        """
        if TYPE_CHECKING:
            assert self.dialect is not None

        s: list[tuple[str, str]] = self.database.execute_sql(self.dialect.select_all_trigger_sql()).fetchall()
        tables = [r[1] for r in s]

        affected_tables = set(tables)
        known_tables = mafw_model_register.get_table_names()
        rebuildable_tables = set([t for t in affected_tables if t in known_tables])
        not_rebuildable_tables = affected_tables - rebuildable_tables

        if len(not_rebuildable_tables) > 0:
            log.warning(f'There are some tables ({len(not_rebuildable_tables)}) that cannot be rebuild')
            with self._user_interface.enter_interactive_mode():
                question = 'Remove all triggers (A), remove only rebuildable triggers (O), quit (Q)'
                if self._user_interface.name == 'rich':
                    question = '[red][bold]' + question + '[/red][/bold]'

                class TriggerPrompt(Prompt):
                    response_type = str
                    validate_error_message = '[prompt.invalid]Please enter A, O or Q'
                    choices: list[str] = ['A', 'O', 'Q']

                answer = self._user_interface.prompt_question(
                    question=question,
                    prompt_type=TriggerPrompt,
                    default='O',
                    show_default=True,
                    case_sensitive=False,
                    show_answer=True,
                )

                if answer == 'Q':
                    s = []
                    affected_tables = set()
                    self.processor_exit_status = ProcessorExitStatus.Aborted
                    self.looping_status = LoopingStatus.Abort

                elif answer == 'O':
                    s = [r for r in s if r[1] in rebuildable_tables]
                    affected_tables = rebuildable_tables

                else:  # equivalent to 'A'
                    # remove all triggers
                    # but rebuilds only rebuildable_tables
                    affected_tables = rebuildable_tables

        self.tables_to_be_rebuilt = affected_tables
        return s

    def process(self) -> None:
        """Delete the current trigger from its table"""
        if TYPE_CHECKING:
            assert self.dialect is not None

        self.database.execute_sql(self.dialect.drop_trigger_sql(self.item[0], safe=True, table_name=self.item[1]))

    def finish(self) -> None:
        """
        Recreate the tables from which triggers were dropped.

        This is only done if the user did not abort the process.
        """
        if self.looping_status != LoopingStatus.Abort:
            log.info(f'Recreating {self.n_item} triggers on {len(self.tables_to_be_rebuilt)} tables...')
            models = [mafw_model_register.get_model(table_name) for table_name in self.tables_to_be_rebuilt]

            self.database.create_tables(models)  # type: ignore[arg-type]
        super().finish()

    def format_progress_message(self) -> None:
        self.progress_message = f'Dropping trigger {self.item[0]} from table {self.item[1]}'


@database_required
class SQLScriptRunner(Processor):
    """
    Processor to execute SQL scripts from files against the database.

    This processor reads SQL files, removes multi-line block comments, splits the content into individual
    statements, and executes them within a transaction. It is designed to handle SQL script execution
    in a safe manner by wrapping all statements in a single atomic transaction.

    The processor accepts a list of SQL files through the :attr:`sql_files` parameter. Each file is validated
    to ensure it exists and is a regular file before processing. Block comments (`/* ... */`) are removed
    from the SQL content before statement parsing.

    .. versionadded:: v2.0.0
    """

    sql_files = ActiveParameter[list[Path]]('sql_files', default=[], help_doc='A list of SQL files to be processed')
    """List of SQL files to be processed"""

    def validate_configuration(self) -> None:
        """
        Validate the configuration of SQL script runner.

        Ensures that all specified SQL files exist and are regular files.

        :raises InvalidConfigurationError: if any of the specified files does not exist or is not a regular file.
        """
        if TYPE_CHECKING:
            # we need to convince mypy that the sql_files is not and ActiveParameter but
            # the content of the ActiveParameter
            assert isinstance(self.sql_files, list)

        self.sql_files = [Path(file) for file in self.sql_files]
        for file in self.sql_files:
            if not file.exists() or not file.is_file():
                raise InvalidConfigurationError(f'There are issues with SQL file "{file.resolve()}". Please verify.')

    def get_items(self) -> Collection[Any]:
        """
        Get the collection of SQL files to be processed.

        :return: A collection of SQL file paths to be processed
        :rtype: Collection[Any]
        """
        if TYPE_CHECKING:
            # we need to convince mypy that the sql_files is not and ActiveParameter but
            # the content of the ActiveParameter
            assert isinstance(self.sql_files, list)

        return self.sql_files

    def process(self) -> None:
        """
        Process a single SQL file by reading, parsing, and executing its statements.

        Reads the SQL file content, removes multi-line block comments, splits the content
        into individual SQL statements, and executes them within a transaction.

        If no statements are found in the file, a warning is logged. If an error occurs
        during execution, the transaction is rolled back and the exception is re-raised.

        :raises Exception: If an error occurs during SQL statement execution.
        """
        with open(self.item, 'rt') as sql_file:
            sql_content = sql_file.read()

        # remove the multi-line block comments (/* ... */)
        sql_content = block_comment_re.sub('', sql_content)

        statements = [s.strip() + ';' for s in sql_content.split(';') if s.strip()]

        if not statements:
            log.warning(f'No SQL statements found to execute in {self.item.name}.')

        log.debug(f'Found {len(statements)} statements to execute.')

        try:
            # use an atomic transaction to wrap the execution of all statements.
            with self.database.atomic():  # type: ignore[no-untyped-call]
                for statement in statements:
                    self.database.execute_sql(statement)

        except Exception as e:
            log.critical(f'An error occurred while executing the SQL script {self.item.name}.')
            log.critical('Rolling back the database to preserve integrity.')
            log.critical(f'Error details: {e}')
            raise

    def format_progress_message(self) -> None:
        self.progress_message = f'Processing SQL file {self.item.name}'
