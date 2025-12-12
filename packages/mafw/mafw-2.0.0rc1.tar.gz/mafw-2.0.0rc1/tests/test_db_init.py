#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""Unit tests for the database initialization processor module."""

import tempfile
from contextlib import nullcontext as does_not_raise
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import peewee
import pytest

from mafw.db.db_model import MAFwBaseModel
from mafw.db.std_tables import StandardTable
from mafw.db.trigger import MySQLDialect, PostgreSQLDialect, SQLiteDialect
from mafw.enumerators import LoopingStatus, ProcessorExitStatus
from mafw.mafw_errors import InvalidConfigurationError, UnsupportedDatabaseError
from mafw.processor_library.db_init import SQLScriptRunner, TableCreator, TriggerRefresher


@pytest.fixture
def mock_database():
    """Create a mock database object."""
    db = Mock()
    db.get_tables = Mock(return_value=[])
    db.create_tables = Mock()
    db.drop_tables = Mock()
    return db


@pytest.fixture
def mock_user_interface():
    """Create a mock user interface object."""
    ui = Mock()
    ui.name = 'rich'
    ui.enter_interactive_mode = Mock(return_value=Mock(__enter__=Mock(), __exit__=Mock()))
    ui.prompt_question = Mock(return_value=True)
    return ui


@pytest.fixture
def mock_model_register():
    """Create mock models for the model register."""
    # Create mock standard model
    mock_standard_model = Mock(spec=MAFwBaseModel)
    mock_standard_model._meta = Mock()
    mock_standard_model._meta.automatic_creation = True

    # Create mock non-standard model
    mock_non_standard_model = Mock(spec=MAFwBaseModel)
    mock_non_standard_model._meta = Mock()
    mock_non_standard_model._meta.automatic_creation = True

    # Create mock model with autocreation disabled
    mock_no_autocreate_model = Mock(spec=MAFwBaseModel)
    mock_no_autocreate_model._meta = Mock()
    mock_no_autocreate_model._meta.automatic_creation = False

    # Create mock standard table model
    mock_std_table_model = Mock(spec=type(StandardTable))
    mock_std_table_model._meta = Mock()
    mock_std_table_model._meta.automatic_creation = True
    mock_std_table_model.init = Mock()

    return {
        'test_table_1': mock_standard_model,
        'test_table_2': mock_non_standard_model,
        'no_autocreate_table': mock_no_autocreate_model,
        'prefix_table_1': mock_standard_model,
        'prefix_table_2': mock_non_standard_model,
        'std_table': mock_std_table_model,
    }


class TestTableCreator:
    """Test suite for the TableCreator processor."""

    def test_init(self, mock_database):
        """Test TableCreator initialization."""
        creator = TableCreator(database=mock_database)

        assert creator.existing_table_names == []
        assert creator.force_recreate is False
        assert creator.apply_only_to_prefix == []

    def test_init_with_parameters(self, mock_database):
        """Test TableCreator initialization with custom parameters."""
        creator = TableCreator(
            database=mock_database, force_recreate=True, apply_only_to_prefix=['prefix_'], soft_recreate=False
        )

        assert creator.force_recreate is True
        assert creator.soft_recreate is False
        assert creator.apply_only_to_prefix == ['prefix_']

    @pytest.mark.parametrize(
        'soft,force,expectation',
        [
            (True, True, pytest.raises(InvalidConfigurationError, match='Both force_recreate and soft_recreate')),
            (False, True, does_not_raise()),
            (True, False, does_not_raise()),
            (False, False, does_not_raise()),
        ],
    )
    def test_configuration_validation(self, soft, force, expectation, mock_database):
        with expectation:
            TableCreator(database=mock_database, soft_recreate=soft, force_recreate=force)

    @patch('mafw.processor_library.db_init.mafw_model_register')
    def test_process_creates_missing_tables(
        self, mock_register, mock_database, mock_user_interface, mock_model_register
    ):
        """Test that process creates only missing tables."""
        mock_register.items = Mock(return_value=mock_model_register.items())
        mock_database.get_tables.return_value = ['test_table_1']

        creator = TableCreator(database=mock_database, soft_recreate=False)
        creator._user_interface = mock_user_interface
        creator.process()

        # Should create tables for models with autocreation that don't exist
        mock_database.create_tables.assert_called_once()
        created_models = mock_database.create_tables.call_args[0][0]

        # test_table_1 already exists, no_autocreate_table has autocreation=False
        # Should create: test_table_2, prefix_table_1, prefix_table_2, std_table
        assert len(created_models) == 4

    @patch('mafw.processor_library.db_init.mafw_model_register')
    def test_process_soft_creates_missing_tables(
        self, mock_register, mock_database, mock_user_interface, mock_model_register
    ):
        """Test that process creates only missing tables."""
        mock_register.items = Mock(return_value=mock_model_register.items())
        mock_database.get_tables.return_value = ['test_table_1']

        creator = TableCreator(database=mock_database)
        creator._user_interface = mock_user_interface
        creator.process()

        # Should create tables for models with autocreation that don't exist
        mock_database.create_tables.assert_called_once()
        created_models = mock_database.create_tables.call_args[0][0]

        # no_autocreate_table has autocreation=False
        # Should create: test_table_1, test_table_2, prefix_table_1, prefix_table_2, std_table
        assert len(created_models) == 5

    @patch('mafw.processor_library.db_init.mafw_model_register')
    def test_process_with_no_missing_tables(
        self, mock_register, mock_database, mock_user_interface, mock_model_register
    ):
        """Test process when all tables already exist."""
        mock_register.items = Mock(return_value=mock_model_register.items())
        mock_database.get_tables.return_value = [
            'test_table_1',
            'test_table_2',
            'prefix_table_1',
            'prefix_table_2',
            'std_table',
        ]

        creator = TableCreator(database=mock_database, soft_recreate=False)
        creator._user_interface = mock_user_interface
        creator.process()

        # Should create empty list
        mock_database.create_tables.assert_called_once()
        created_models = mock_database.create_tables.call_args[0][0]
        assert len(created_models) == 0

    @patch('mafw.processor_library.db_init.mafw_model_register')
    def test_process_with_no_missing_tables_and_soft_recreate(
        self, mock_register, mock_database, mock_user_interface, mock_model_register
    ):
        """Test process when all tables already exist."""
        mock_register.items = Mock(return_value=mock_model_register.items())
        mock_database.get_tables.return_value = [
            'test_table_1',
            'test_table_2',
            'prefix_table_1',
            'prefix_table_2',
            'std_table',
        ]

        creator = TableCreator(
            database=mock_database,
        )
        creator._user_interface = mock_user_interface
        creator.process()

        # Should create empty list
        mock_database.create_tables.assert_called_once()
        created_models = mock_database.create_tables.call_args[0][0]
        assert len(created_models) == 5

    @patch('mafw.processor_library.db_init.mafw_model_register')
    def test_process_with_prefix_filter(self, mock_register, mock_database, mock_user_interface, mock_model_register):
        """Test process with apply_only_to_prefix parameter."""
        mock_register.items = Mock(return_value=mock_model_register.items())
        mock_database.get_tables.return_value = []

        creator = TableCreator(database=mock_database, soft_recreate=False, apply_only_to_prefix=['prefix_'])
        creator._user_interface = mock_user_interface
        creator.process()

        mock_database.create_tables.assert_called_once()
        created_models = mock_database.create_tables.call_args[0][0]

        # Should only create tables with 'prefix_' prefix
        assert len(created_models) == 2

    @pytest.mark.parametrize(
        'return_value',
        [
            [],
            ['prefix_table_1'],
            ['prefix_table_2'],
            ['prefix_table_1', 'prefix_table_2'],
            ['prefix_table_1', 'prefix_table_2', 'test_table_1'],
        ],
    )
    @patch('mafw.processor_library.db_init.mafw_model_register')
    def test_process_with_prefix_filter_and_soft_recreate(
        self, mock_register, return_value, mock_database, mock_user_interface, mock_model_register
    ):
        """Test process with apply_only_to_prefix parameter."""
        mock_register.items = Mock(return_value=mock_model_register.items())
        mock_database.get_tables.return_value = return_value

        creator = TableCreator(database=mock_database, soft_recreate=True, apply_only_to_prefix=['prefix_'])
        creator._user_interface = mock_user_interface
        creator.process()

        mock_database.create_tables.assert_called_once()
        created_models = mock_database.create_tables.call_args[0][0]

        # Should only create tables with 'prefix_' prefix
        assert len(created_models) == 2

    @patch('mafw.processor_library.db_init.mafw_model_register')
    def test_process_with_multiple_prefixes(
        self,
        mock_register,
        mock_database,
        mock_user_interface,
        mock_model_register,
    ):
        """Test process with multiple prefixes in apply_only_to_prefix."""
        mock_register.items = Mock(return_value=mock_model_register.items())
        mock_database.get_tables.return_value = []

        creator = TableCreator(database=mock_database, soft_recreate=False, apply_only_to_prefix=['prefix_', 'std_'])
        creator._user_interface = mock_user_interface
        creator.process()

        mock_database.create_tables.assert_called_once()
        created_models = mock_database.create_tables.call_args[0][0]

        # Should create tables with 'prefix_' or 'std_' prefix
        assert len(created_models) == 3

    @patch('mafw.processor_library.db_init.mafw_model_register')
    @patch('mafw.processor_library.db_init.log')
    def test_process_force_recreate_with_confirmation(
        self,
        mock_log,
        mock_register,
        mock_database,
        mock_user_interface,
        mock_model_register,
    ):
        """Test forced recreation with user confirmation."""
        mock_register.items = Mock(return_value=mock_model_register.items())
        mock_database.get_tables.return_value = []
        mock_user_interface.prompt_question.return_value = True

        creator = TableCreator(database=mock_database, soft_recreate=False, force_recreate=True)
        creator._user_interface = mock_user_interface
        creator.process()

        # Should drop tables first
        mock_database.drop_tables.assert_called_once()
        dropped_models = mock_database.drop_tables.call_args[0][0]
        assert len(dropped_models) == 5  # All models with autocreation=True

        # Should create tables
        mock_database.create_tables.assert_called_once()

        # Should prompt user
        mock_user_interface.prompt_question.assert_called_once()

        # Check the logging
        assert len(mock_log.mock_calls) == 4
        assert len(mock_log.warning.call_args_list) == 2
        assert len(mock_log.info.call_args_list) == 2

    @patch('mafw.processor_library.db_init.mafw_model_register')
    @patch('mafw.processor_library.db_init.log')
    def test_process_force_recreate_without_confirmation(
        self,
        mock_log,
        mock_register,
        mock_database,
        mock_user_interface,
        mock_model_register,
    ):
        """Test forced recreation aborted by user."""
        mock_register.items = Mock(return_value=mock_model_register.items())
        mock_user_interface.prompt_question.return_value = False

        creator = TableCreator(database=mock_database, soft_recreate=False, force_recreate=True)
        creator._user_interface = mock_user_interface
        creator.process()

        # Should not drop or create tables
        mock_database.drop_tables.assert_not_called()
        mock_database.create_tables.assert_not_called()

        # Should set exit status to Aborted
        assert creator.processor_exit_status == ProcessorExitStatus.Aborted

        # Check the logging
        assert len(mock_log.mock_calls) == 2
        assert len(mock_log.warning.call_args_list) == 2

    @patch('mafw.processor_library.db_init.mafw_model_register')
    def test_process_force_recreate_initializes_standard_tables(
        self, mock_register, mock_database, mock_user_interface, mock_model_register
    ):
        """Test that standard tables are initialized after forced recreation."""
        mock_register.items = Mock(return_value=mock_model_register.items())
        mock_database.get_tables.return_value = []
        mock_user_interface.prompt_question.return_value = True

        creator = TableCreator(database=mock_database, soft_recreate=False, force_recreate=True)
        creator._user_interface = mock_user_interface
        creator.process()

        # Check if init was called on standard table model
        std_table_model = mock_model_register['std_table']
        std_table_model.init.assert_called_once()

    @patch('mafw.processor_library.db_init.mafw_model_register')
    def test_process_skips_non_autocreation_models(
        self,
        mock_register,
        mock_database,
        mock_user_interface,
        mock_model_register,
    ):
        """Test that models with automatic_creation=False are skipped."""
        mock_register.items = Mock(return_value=mock_model_register.items())
        mock_database.get_tables.return_value = []

        creator = TableCreator(database=mock_database, soft_recreate=False)
        creator._user_interface = mock_user_interface
        creator.process()

        mock_database.create_tables.assert_called_once()
        created_models = mock_database.create_tables.call_args[0][0]

        # no_autocreate_table should not be in the list
        model_names = [name for name, model in mock_model_register.items() if model in created_models]
        assert 'no_autocreate_table' not in model_names

    @patch('mafw.processor_library.db_init.mafw_model_register')
    @patch('mafw.processor_library.db_init.log')
    def test_process_logs_creation_single_table(
        self, mock_log, mock_register, mock_database, mock_user_interface, mock_model_register
    ):
        """Test logging when creating a single table."""
        # Setup to create only one table
        single_model = {'test_table_1': mock_model_register['test_table_1']}
        mock_register.items = Mock(return_value=single_model.items())
        mock_database.get_tables.return_value = []

        creator = TableCreator(database=mock_database)
        creator._user_interface = mock_user_interface
        creator.process()

        # Check log message for singular form
        mock_log.info.assert_called_with('Successfully create 1 table.')

    @patch('mafw.processor_library.db_init.mafw_model_register')
    @patch('mafw.processor_library.db_init.log')
    def test_process_logs_creation_multiple_tables(
        self, mock_log, mock_register, mock_database, mock_user_interface, mock_model_register
    ):
        """Test logging when creating multiple tables."""
        mock_register.items = Mock(return_value=mock_model_register.items())
        mock_database.get_tables.return_value = []

        creator = TableCreator(database=mock_database)
        creator._user_interface = mock_user_interface
        creator.process()

        # Check log message for plural form
        assert any('tables.' in str(c) for c in mock_log.info.call_args_list)

    @patch('mafw.processor_library.db_init.mafw_model_register')
    def test_process_no_logging_when_no_tables_created(
        self, mock_register, mock_database, mock_user_interface, mock_model_register
    ):
        """Test that no success log when no tables are created."""
        mock_register.items = Mock(return_value=mock_model_register.items())
        # All tables already exist
        mock_database.get_tables.return_value = [
            'test_table_1',
            'test_table_2',
            'prefix_table_1',
            'prefix_table_2',
            'std_table',
        ]

        with patch('mafw.processor_library.db_init.log') as mock_log:
            creator = TableCreator(database=mock_database, soft_recreate=False)
            creator._user_interface = mock_user_interface
            creator.process()

            # Should not log success message
            info_calls = [str(call) for call in mock_log.info.call_args_list]
            assert not any('Successfully create' in call for call in info_calls)

    @patch('mafw.processor_library.db_init.mafw_model_register')
    def test_process_with_empty_prefix_list(
        self, mock_register, mock_database, mock_user_interface, mock_model_register
    ):
        """Test process with empty prefix list behaves like no prefix filter."""
        mock_register.items = Mock(return_value=mock_model_register.items())
        mock_database.get_tables.return_value = []

        creator = TableCreator(database=mock_database, apply_only_to_prefix=[], soft_recreate=False)
        creator._user_interface = mock_user_interface
        creator.process()

        mock_database.create_tables.assert_called_once()
        created_models = mock_database.create_tables.call_args[0][0]

        # Should create all autocreation tables
        assert len(created_models) == 5

    @patch('mafw.processor_library.db_init.mafw_model_register')
    def test_process_with_non_matching_prefix(
        self, mock_register, mock_database, mock_user_interface, mock_model_register
    ):
        """Test process with prefix that matches no tables."""
        mock_register.items = Mock(return_value=mock_model_register.items())
        mock_database.get_tables.return_value = []

        creator = TableCreator(database=mock_database, soft_recreate=False, apply_only_to_prefix=['nonexistent_'])
        creator._user_interface = mock_user_interface
        creator.process()

        mock_database.create_tables.assert_called_once()
        created_models = mock_database.create_tables.call_args[0][0]

        # Should create no tables
        assert len(created_models) == 0

    @patch('mafw.processor_library.db_init.mafw_model_register')
    @patch('mafw.processor_library.db_init.log')
    def test_force_recreate_warning_messages(
        self,
        mock_log,
        mock_register,
        mock_database,
        mock_user_interface,
        mock_model_register,
    ):
        """Test that appropriate warnings are logged for force recreate."""
        mock_register.items = Mock(return_value=mock_model_register.items())
        mock_database.get_tables.return_value = []
        mock_user_interface.prompt_question.return_value = True

        creator = TableCreator(database=mock_database, soft_recreate=False, force_recreate=True)
        creator._user_interface = mock_user_interface
        creator.process()

        # Check warning messages
        warning_calls = [str(call) for call in mock_log.warning.call_args_list]
        assert any('Forcing recreation' in call for call in warning_calls)
        assert any('All data' in call for call in warning_calls)

    @patch('mafw.processor_library.db_init.mafw_model_register')
    @patch('mafw.processor_library.db_init.log')
    def test_force_recreate_warning_messages_with_console_ui(
        self,
        mock_log,
        mock_register,
        mock_database,
        mock_user_interface,
        mock_model_register,
    ):
        """Test that appropriate warnings are logged for force recreate."""
        mock_register.items = Mock(return_value=mock_model_register.items())
        mock_database.get_tables.return_value = []
        mock_user_interface.name = 'console'
        mock_user_interface.prompt_question.return_value = True

        creator = TableCreator(database=mock_database, soft_recreate=False, force_recreate=True)
        creator._user_interface = mock_user_interface
        creator.process()

        # Check warning messages
        warning_calls = [str(call) for call in mock_log.warning.call_args_list]
        assert any('Forcing recreation' in call for call in warning_calls)
        assert any('All data' in call for call in warning_calls)

    @patch('mafw.processor_library.db_init.mafw_model_register')
    def test_existing_table_names_populated(
        self, mock_register, mock_database, mock_user_interface, mock_model_register
    ):
        """Test that existing_table_names attribute is populated."""
        mock_register.items = Mock(return_value=mock_model_register.items())
        existing_tables = ['test_table_1', 'test_table_2']
        mock_database.get_tables.return_value = existing_tables

        creator = TableCreator(database=mock_database, soft_recreate=False)
        creator._user_interface = mock_user_interface
        creator.process()

        assert creator.existing_table_names == existing_tables

    @patch('mafw.processor_library.db_init.mafw_model_register')
    def test_force_recreate_with_prefix_filter(
        self, mock_register, mock_database, mock_user_interface, mock_model_register
    ):
        """Test forced recreation combined with prefix filter."""
        mock_register.items = Mock(return_value=mock_model_register.items())
        mock_database.get_tables.return_value = []
        mock_user_interface.prompt_question.return_value = True

        creator = TableCreator(
            database=mock_database, force_recreate=True, apply_only_to_prefix=['prefix_'], soft_recreate=False
        )
        creator._user_interface = mock_user_interface
        creator.process()

        # Should only drop and create tables with prefix
        dropped_models = mock_database.drop_tables.call_args[0][0]
        assert len(dropped_models) == 2

        created_models = mock_database.create_tables.call_args[0][0]
        assert len(created_models) == 2

    @patch('mafw.processor_library.db_init.mafw_model_register')
    def test_user_interface_interactive_mode_context(
        self, mock_register, mock_database, mock_user_interface, mock_model_register
    ):
        """Test that interactive mode context manager is used correctly."""
        mock_register.items = Mock(return_value=mock_model_register.items())
        mock_database.get_tables.return_value = []

        context_manager = MagicMock()
        mock_user_interface.enter_interactive_mode.return_value = context_manager

        creator = TableCreator(database=mock_database, soft_recreate=False, force_recreate=True)
        creator._user_interface = mock_user_interface
        creator.process()

        # Verify context manager was entered and exited
        mock_user_interface.enter_interactive_mode.assert_called_once()
        context_manager.__enter__.assert_called_once()
        context_manager.__exit__.assert_called_once()


@pytest.mark.integration_test
class TestTableCreatorIntegration:
    """Integration tests for TableCreator with actual database."""

    @patch('mafw.processor_library.db_init.mafw_model_register')
    def test_full_table_creation_workflow(self, mock_register, mock_database, mock_user_interface):
        """Test complete workflow from model registration to table creation."""
        # Setup realistic model register
        model1 = Mock(spec=MAFwBaseModel)
        model1._meta = Mock(automatic_creation=True)

        model2 = Mock(spec=MAFwBaseModel)
        model2._meta = Mock(automatic_creation=True)

        mock_register.items = Mock(return_value=[('table1', model1), ('table2', model2)])

        # Simulate database state
        mock_database.get_tables.return_value = ['table1']

        creator = TableCreator(database=mock_database, soft_recreate=False)
        creator._user_interface = mock_user_interface
        creator.process()

        # Verify workflow
        mock_database.get_tables.assert_called_once()
        mock_database.create_tables.assert_called_once()

        created = mock_database.create_tables.call_args[0][0]
        assert len(created) == 1
        assert created[0] == model2


class TestTriggerRefresher:
    """Test suite for the TriggerRefresher processor."""

    def test_init(self, mock_database):
        """Test TriggerRefresher initialization."""
        refresher = TriggerRefresher(database=mock_database)

        assert refresher.dialect is None
        assert refresher.tables_to_be_rebuilt == set()

    def test_get_dialect_returns_cached_dialect(self, mock_database):
        """Test that get_dialect returns cached dialect if already set."""
        refresher = TriggerRefresher(database=mock_database)
        cached_dialect = SQLiteDialect()
        refresher.dialect = cached_dialect

        result = refresher.get_dialect()

        assert result is cached_dialect

    def test_get_dialect_default_sqlite_when_no_database(self):
        """Test that get_dialect returns SQLite dialect when database is None."""
        refresher = TriggerRefresher()

        result = refresher.get_dialect()

        assert isinstance(result, SQLiteDialect)

    def test_get_dialect_sqlite_database(self, mock_database):
        """Test get_dialect with SQLite database."""
        sqlite_db = Mock(spec=peewee.SqliteDatabase)
        mock_database_proxy = Mock(spec=peewee.DatabaseProxy)
        mock_database_proxy.obj = sqlite_db

        refresher = TriggerRefresher(database=mock_database_proxy)

        result = refresher.get_dialect()

        assert isinstance(result, SQLiteDialect)

    def test_get_dialect_mysql_database(self, mock_database):
        """Test get_dialect with MySQL database."""
        mysql_db = Mock(spec=peewee.MySQLDatabase)
        mock_database_proxy = Mock(spec=peewee.DatabaseProxy)
        mock_database_proxy.obj = mysql_db

        refresher = TriggerRefresher(database=mock_database_proxy)

        result = refresher.get_dialect()

        assert isinstance(result, MySQLDialect)

    def test_get_dialect_postgresql_database(self, mock_database):
        """Test get_dialect with PostgreSQL database."""
        postgres_db = Mock(spec=peewee.PostgresqlDatabase)
        mock_database_proxy = Mock(spec=peewee.DatabaseProxy)
        mock_database_proxy.obj = postgres_db

        refresher = TriggerRefresher(database=mock_database_proxy)

        result = refresher.get_dialect()

        assert isinstance(result, PostgreSQLDialect)

    def test_get_dialect_unsupported_database(self, mock_database):
        """Test get_dialect with unsupported database type."""
        unsupported_db = Mock()
        mock_database_proxy = Mock(spec=peewee.DatabaseProxy)
        mock_database_proxy.obj = unsupported_db

        refresher = TriggerRefresher(database=mock_database_proxy)

        with pytest.raises(UnsupportedDatabaseError, match='Unsupported database type'):
            refresher.get_dialect()

    def test_get_dialect_direct_sqlite_database(self):
        """Test get_dialect with direct SQLite database (not proxied)."""
        sqlite_db = Mock(spec=peewee.SqliteDatabase)

        refresher = TriggerRefresher(database=sqlite_db)

        result = refresher.get_dialect()

        assert isinstance(result, SQLiteDialect)

    def test_start_initializes_dialect(self, mock_database):
        """Test that start method initializes dialect."""
        refresher = TriggerRefresher(database=mock_database, remove_orphan_files=False)

        with patch.object(refresher, 'get_dialect', return_value=SQLiteDialect()) as mock_get_dialect:
            refresher.start()

            mock_get_dialect.assert_called_once()
            assert refresher.dialect is not None

    @patch('mafw.processor_library.db_init.mafw_model_register')
    def test_get_items_all_tables_rebuildable(self, mock_register, mock_database, mock_user_interface):
        """Test get_items when all tables are in the model register."""
        trigger_data = [
            ('trigger1', 'table1'),
            ('trigger2', 'table2'),
            ('trigger3', 'table1'),
        ]

        mock_result = Mock()
        mock_result.fetchall.return_value = trigger_data
        mock_database.execute_sql.return_value = mock_result

        mock_dialect = Mock()
        mock_dialect.select_all_trigger_sql.return_value = 'SELECT * FROM triggers'

        mock_register.get_table_names.return_value = ['table1', 'table2']

        refresher = TriggerRefresher(database=mock_database)
        refresher._user_interface = mock_user_interface
        refresher.dialect = mock_dialect

        items = refresher.get_items()

        assert list(items) == trigger_data
        assert refresher.tables_to_be_rebuilt == {'table1', 'table2'}
        mock_database.execute_sql.assert_called_once_with('SELECT * FROM triggers')

    @patch('mafw.processor_library.db_init.mafw_model_register')
    @patch('mafw.processor_library.db_init.log')
    def test_get_items_with_non_rebuildable_tables_quit(
        self, mock_log, mock_register, mock_database, mock_user_interface
    ):
        """Test get_items with non-rebuildable tables when user chooses quit."""
        trigger_data = [
            ('trigger1', 'table1'),
            ('trigger2', 'unknown_table'),
        ]

        mock_result = Mock()
        mock_result.fetchall.return_value = trigger_data
        mock_database.execute_sql.return_value = mock_result

        mock_dialect = Mock()
        mock_dialect.select_all_trigger_sql.return_value = 'SELECT * FROM triggers'

        mock_register.get_model_names.return_value = ['table1']
        mock_user_interface.prompt_question.return_value = 'Q'

        refresher = TriggerRefresher(database=mock_database)
        refresher._user_interface = mock_user_interface
        refresher.dialect = mock_dialect

        items = refresher.get_items()

        assert list(items) == []
        assert refresher.tables_to_be_rebuilt == set()
        assert refresher.processor_exit_status == ProcessorExitStatus.Aborted
        assert refresher.looping_status == LoopingStatus.Abort
        mock_log.warning.assert_called_once()

    @patch('mafw.processor_library.db_init.mafw_model_register')
    @patch('mafw.processor_library.db_init.log')
    def test_get_items_with_non_rebuildable_tables_only_rebuildable(
        self, mock_log, mock_register, mock_database, mock_user_interface
    ):
        """Test get_items with non-rebuildable tables when user chooses only rebuildable."""
        trigger_data = [
            ('trigger1', 'table1'),
            ('trigger2', 'unknown_table'),
            ('trigger3', 'table1'),
        ]

        mock_result = Mock()
        mock_result.fetchall.return_value = trigger_data
        mock_database.execute_sql.return_value = mock_result

        mock_dialect = Mock()
        mock_dialect.select_all_trigger_sql.return_value = 'SELECT * FROM triggers'

        mock_register.get_table_names.return_value = ['table1']
        mock_user_interface.prompt_question.return_value = 'O'

        refresher = TriggerRefresher(database=mock_database)
        refresher._user_interface = mock_user_interface
        refresher.dialect = mock_dialect

        items = refresher.get_items()

        expected_items = [('trigger1', 'table1'), ('trigger3', 'table1')]
        assert list(items) == expected_items
        assert refresher.tables_to_be_rebuilt == {'table1'}
        mock_log.warning.assert_called_once()

    @patch('mafw.processor_library.db_init.mafw_model_register')
    @patch('mafw.processor_library.db_init.log')
    def test_get_items_with_non_rebuildable_tables_all(
        self, mock_log, mock_register, mock_database, mock_user_interface
    ):
        """Test get_items with non-rebuildable tables when user chooses all."""
        trigger_data = [
            ('trigger1', 'table1'),
            ('trigger2', 'unknown_table'),
            ('trigger3', 'table1'),
        ]

        mock_result = Mock()
        mock_result.fetchall.return_value = trigger_data
        mock_database.execute_sql.return_value = mock_result

        mock_dialect = Mock()
        mock_dialect.select_all_trigger_sql.return_value = 'SELECT * FROM triggers'

        mock_register.get_table_names.return_value = ['table1']
        mock_user_interface.prompt_question.return_value = 'A'

        refresher = TriggerRefresher(database=mock_database)
        refresher._user_interface = mock_user_interface
        refresher.dialect = mock_dialect

        items = refresher.get_items()

        # All triggers removed, but only rebuildable tables marked for rebuild
        assert list(items) == trigger_data
        assert refresher.tables_to_be_rebuilt == {'table1'}
        mock_log.warning.assert_called_once()

    @patch('mafw.processor_library.db_init.mafw_model_register')
    @patch('mafw.processor_library.db_init.log')
    def test_get_items_with_non_rebuildable_tables_console_ui(
        self, mock_log, mock_register, mock_database, mock_user_interface
    ):
        """Test get_items with console UI (no rich formatting)."""
        trigger_data = [
            ('trigger1', 'table1'),
            ('trigger2', 'unknown_table'),
        ]

        mock_result = Mock()
        mock_result.fetchall.return_value = trigger_data
        mock_database.execute_sql.return_value = mock_result

        mock_dialect = Mock()
        mock_dialect.select_all_trigger_sql.return_value = 'SELECT * FROM triggers'

        mock_register.get_model_names.return_value = ['table1']
        mock_user_interface.name = 'console'
        mock_user_interface.prompt_question.return_value = 'O'

        refresher = TriggerRefresher(database=mock_database)
        refresher._user_interface = mock_user_interface
        refresher.dialect = mock_dialect

        refresher.get_items()

        # Verify question prompt was called
        mock_user_interface.prompt_question.assert_called_once()
        call_kwargs = mock_user_interface.prompt_question.call_args[1]
        # Console UI should not have rich formatting
        assert '[red][bold]' not in call_kwargs['question']

    def test_process_drops_trigger(self, mock_database):
        """Test that process method drops the trigger."""
        mock_dialect = Mock()
        mock_dialect.drop_trigger_sql.return_value = 'DROP TRIGGER trigger1'

        refresher = TriggerRefresher(database=mock_database)
        refresher.dialect = mock_dialect
        refresher.item = ('trigger1', 'table1')

        refresher.process()

        mock_database.execute_sql.assert_called_once_with('DROP TRIGGER trigger1')
        mock_dialect.drop_trigger_sql.assert_called_once_with('trigger1', safe=True, table_name='table1')

    @patch('mafw.processor_library.db_init.mafw_model_register')
    @patch('mafw.processor_library.db_init.log')
    def test_finish_recreates_triggers(self, mock_log, mock_register, mock_database):
        """Test that finish method recreates triggers on affected tables."""
        mock_model1 = Mock()
        mock_model2 = Mock()

        mock_register.get_model.side_effect = lambda name: {
            'table1': mock_model1,
            'table2': mock_model2,
        }[name]

        refresher = TriggerRefresher(database=mock_database)
        refresher.tables_to_be_rebuilt = {'table1', 'table2'}
        refresher.n_item = 5
        refresher.looping_status = LoopingStatus.Continue

        refresher.finish()

        mock_database.create_tables.assert_called_once()
        created_models = mock_database.create_tables.call_args[0][0]
        assert set(created_models) == {mock_model1, mock_model2}
        mock_log.info.assert_called_once()

    @patch('mafw.processor_library.db_init.log')
    def test_finish_skips_recreation_when_aborted(self, mock_log, mock_database):
        """Test that finish method skips recreation when looping status is Abort."""
        refresher = TriggerRefresher(database=mock_database)
        refresher.tables_to_be_rebuilt = {'table1', 'table2'}
        refresher.looping_status = LoopingStatus.Abort

        refresher.finish()

        mock_database.create_tables.assert_not_called()
        mock_log.info.assert_not_called()

    def test_format_progress_message(self, mock_database):
        """Test that format_progress_message sets correct message."""
        refresher = TriggerRefresher(database=mock_database)
        refresher.item = ('my_trigger', 'my_table')

        refresher.format_progress_message()

        assert refresher.progress_message == 'Dropping trigger my_trigger from table my_table'

    @patch('mafw.processor_library.db_init.mafw_model_register')
    def test_get_items_empty_result(self, mock_register, mock_database, mock_user_interface):
        """Test get_items when no triggers are found."""
        mock_result = Mock()
        mock_result.fetchall.return_value = []
        mock_database.execute_sql.return_value = mock_result

        mock_dialect = Mock()
        mock_dialect.select_all_trigger_sql.return_value = 'SELECT * FROM triggers'

        mock_register.get_model_names.return_value = ['table1', 'table2']

        refresher = TriggerRefresher(database=mock_database)
        refresher._user_interface = mock_user_interface
        refresher.dialect = mock_dialect

        items = refresher.get_items()

        assert list(items) == []
        assert refresher.tables_to_be_rebuilt == set()

    @patch('mafw.processor_library.db_init.mafw_model_register')
    def test_get_items_multiple_triggers_same_table(self, mock_register, mock_database, mock_user_interface):
        """Test get_items with multiple triggers on the same table."""
        trigger_data = [
            ('trigger1', 'table1'),
            ('trigger2', 'table1'),
            ('trigger3', 'table1'),
        ]

        mock_result = Mock()
        mock_result.fetchall.return_value = trigger_data
        mock_database.execute_sql.return_value = mock_result

        mock_dialect = Mock()
        mock_dialect.select_all_trigger_sql.return_value = 'SELECT * FROM triggers'

        mock_register.get_table_names.return_value = ['table1']

        refresher = TriggerRefresher(database=mock_database)
        refresher._user_interface = mock_user_interface
        refresher.dialect = mock_dialect

        items = refresher.get_items()

        assert list(items) == trigger_data
        assert refresher.tables_to_be_rebuilt == {'table1'}

    @patch('mafw.processor_library.db_init.mafw_model_register')
    @patch('mafw.processor_library.db_init.log')
    def test_get_items_case_insensitive_prompt(self, mock_log, mock_register, mock_database, mock_user_interface):
        """Test that prompt accepts case-insensitive answers."""
        trigger_data = [
            ('trigger1', 'table1'),
            ('trigger2', 'unknown_table'),
        ]

        mock_result = Mock()
        mock_result.fetchall.return_value = trigger_data
        mock_database.execute_sql.return_value = mock_result

        mock_dialect = Mock()
        mock_dialect.select_all_trigger_sql.return_value = 'SELECT * FROM triggers'

        mock_register.get_model_names.return_value = ['table1']
        mock_user_interface.prompt_question.return_value = 'o'  # lowercase

        refresher = TriggerRefresher(database=mock_database)
        refresher._user_interface = mock_user_interface
        refresher.dialect = mock_dialect

        refresher.get_items()

        # Verify the prompt was configured as case_insensitive
        call_kwargs = mock_user_interface.prompt_question.call_args[1]
        assert call_kwargs['case_sensitive'] is False

    @patch('mafw.processor_library.db_init.mafw_model_register')
    def test_get_items_shows_answer(self, mock_register, mock_database, mock_user_interface):
        """Test that prompt is configured to show the answer."""
        trigger_data = [
            ('trigger1', 'table1'),
            ('trigger2', 'unknown_table'),
        ]

        mock_result = Mock()
        mock_result.fetchall.return_value = trigger_data
        mock_database.execute_sql.return_value = mock_result

        mock_dialect = Mock()
        mock_dialect.select_all_trigger_sql.return_value = 'SELECT * FROM triggers'

        mock_register.get_model_names.return_value = ['table1']
        mock_user_interface.prompt_question.return_value = 'O'

        refresher = TriggerRefresher(database=mock_database)
        refresher._user_interface = mock_user_interface
        refresher.dialect = mock_dialect

        refresher.get_items()

        # Verify show_answer was set to True
        call_kwargs = mock_user_interface.prompt_question.call_args[1]
        assert call_kwargs['show_answer'] is True

    @patch('mafw.processor_library.db_init.mafw_model_register')
    def test_get_items_default_option(self, mock_register, mock_database, mock_user_interface):
        """Test that default option is 'O' (only rebuildable)."""
        trigger_data = [
            ('trigger1', 'table1'),
            ('trigger2', 'unknown_table'),
        ]

        mock_result = Mock()
        mock_result.fetchall.return_value = trigger_data
        mock_database.execute_sql.return_value = mock_result

        mock_dialect = Mock()
        mock_dialect.select_all_trigger_sql.return_value = 'SELECT * FROM triggers'

        mock_register.get_model_names.return_value = ['table1']
        mock_user_interface.prompt_question.return_value = 'O'

        refresher = TriggerRefresher(database=mock_database)
        refresher._user_interface = mock_user_interface
        refresher.dialect = mock_dialect

        refresher.get_items()

        # Verify default was set to 'O'
        call_kwargs = mock_user_interface.prompt_question.call_args[1]
        assert call_kwargs['default'] == 'O'
        assert call_kwargs['show_default'] is True

    @patch('mafw.processor_library.db_init.mafw_model_register')
    def test_get_items_interactive_mode_context(self, mock_register, mock_database, mock_user_interface):
        """Test that interactive mode context manager is used when needed."""
        trigger_data = [
            ('trigger1', 'table1'),
            ('trigger2', 'unknown_table'),
        ]

        mock_result = Mock()
        mock_result.fetchall.return_value = trigger_data
        mock_database.execute_sql.return_value = mock_result

        mock_dialect = Mock()
        mock_dialect.select_all_trigger_sql.return_value = 'SELECT * FROM triggers'

        mock_register.get_model_names.return_value = ['table1']
        mock_user_interface.prompt_question.return_value = 'O'

        context_manager = MagicMock()
        mock_user_interface.enter_interactive_mode.return_value = context_manager

        refresher = TriggerRefresher(database=mock_database)
        refresher._user_interface = mock_user_interface
        refresher.dialect = mock_dialect

        refresher.get_items()

        # Verify context manager was entered and exited
        mock_user_interface.enter_interactive_mode.assert_called_once()
        context_manager.__enter__.assert_called_once()
        context_manager.__exit__.assert_called_once()

    @patch('mafw.processor_library.db_init.mafw_model_register')
    @patch('mafw.processor_library.db_init.log')
    def test_finish_logs_correct_count(self, mock_log, mock_register, mock_database):
        """Test that finish logs the correct number of triggers and tables."""
        mock_model1 = Mock()
        mock_model2 = Mock()
        mock_model3 = Mock()

        mock_register.get_model.side_effect = lambda name: {
            'table1': mock_model1,
            'table2': mock_model2,
            'table3': mock_model3,
        }[name]

        refresher = TriggerRefresher(database=mock_database)
        refresher.tables_to_be_rebuilt = {'table1', 'table2', 'table3'}
        refresher.n_item = 7
        refresher.looping_status = LoopingStatus.Continue

        refresher.finish()

        # Check log message contains correct counts
        log_message = str(mock_log.info.call_args)
        assert '7' in log_message  # number of triggers
        assert '3' in log_message  # number of tables


@pytest.mark.integration_test
class TestTriggerRefresherIntegration:
    """Integration tests for TriggerRefresher."""

    @patch('mafw.processor_library.db_init.mafw_model_register')
    def test_full_trigger_refresh_workflow(self, mock_register, mock_database, mock_user_interface):
        """Test complete workflow from trigger detection to recreation."""
        trigger_data = [
            ('trigger1', 'table1'),
            ('trigger2', 'table2'),
        ]

        mock_result = Mock()
        mock_result.fetchall.return_value = trigger_data
        mock_database.execute_sql.return_value = mock_result

        mock_model1 = Mock()
        mock_model2 = Mock()

        mock_register.get_table_names.return_value = ['table1', 'table2']
        mock_register.get_model.side_effect = lambda name: {
            'table1': mock_model1,
            'table2': mock_model2,
        }[name]

        mock_dialect = Mock()
        mock_dialect.select_all_trigger_sql.return_value = 'SELECT * FROM triggers'
        mock_dialect.drop_trigger_sql.side_effect = lambda name, **kwargs: f'DROP TRIGGER {name}'

        refresher = TriggerRefresher(database=mock_database)
        refresher._user_interface = mock_user_interface
        refresher.dialect = mock_dialect

        # Get items
        items = list(refresher.get_items())

        # Process each item
        for item in items:
            refresher.item = item
            refresher.process()

        refresher.n_item = len(items)

        # Finish
        refresher.finish()

        # Verify workflow
        assert mock_database.execute_sql.call_count == 3  # 1 select + 2 drops
        mock_database.create_tables.assert_called_once()
        created_models = mock_database.create_tables.call_args[0][0]
        assert set(created_models) == {mock_model1, mock_model2}


class TestSQLScriptRunner:
    """Test class for SQLScriptRunner processor."""

    def test_validate_configuration_valid_files(self):
        """Test validation with valid existing files."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write('CREATE TABLE test (id INTEGER);')
            temp_file = Path(f.name)

        try:
            runner = SQLScriptRunner(sql_files=[temp_file])
            runner.validate_configuration()
            assert runner.sql_files == [temp_file]
        finally:
            temp_file.unlink()

    def test_validate_configuration_invalid_file(self):
        """Test validation with non-existent file raises error."""

        with pytest.raises(InvalidConfigurationError, match='There are issues with SQL file'):
            SQLScriptRunner(sql_files=[Path('/non/existent/file.sql')])

    def test_validate_configuration_directory_instead_of_file(self):
        """Test validation with directory instead of file raises error."""

        with pytest.raises(InvalidConfigurationError, match='There are issues with SQL file'):
            SQLScriptRunner(sql_files=[Path('/tmp')])

    def test_get_items_returns_correct_collection(self):
        """Test that get_items returns the correct collection of files."""
        file1 = Path('/tmp/test1.sql')
        file2 = Path('/tmp/test2.sql')

        runner = SQLScriptRunner()
        runner.sql_files = [file1, file2]

        items = runner.get_items()
        assert items == [file1, file2]

    @patch('builtins.open')
    @patch('mafw.processor_library.db_init.block_comment_re')
    @patch('mafw.processor_library.db_init.log')
    def test_process_no_statements_warning(self, mock_log, mock_block_comment_re, mock_open):
        """Test processing file with no statements logs warning."""
        mock_file_handle = Mock()
        mock_file_handle.read.return_value = '/* comment */'
        mock_open.return_value.__enter__.return_value = mock_file_handle
        mock_block_comment_re.sub.return_value = ''

        runner = SQLScriptRunner()
        runner.item = Path('/tmp/test.sql')
        runner._database = MagicMock()
        runner.database.atomic = MagicMock(return_value=MagicMock())
        runner.database.execute_sql = Mock()

        runner.process()

        mock_log.warning.assert_called_once_with('No SQL statements found to execute in test.sql.')
        mock_log.debug.assert_called_once_with('Found 0 statements to execute.')
        runner.database.atomic.assert_called_once()
        runner.database.execute_sql.assert_not_called()

    @patch('builtins.open')
    @patch('mafw.processor_library.db_init.block_comment_re')
    @patch('mafw.processor_library.db_init.log')
    def test_process_with_statements_executes_transaction(self, mock_log, mock_block_comment_re, mock_open):
        """Test processing file with statements executes within transaction."""
        mock_file_handle = Mock()
        mock_file_handle.read.return_value = 'CREATE TABLE test (id INTEGER); INSERT INTO test VALUES (1);'
        mock_open.return_value.__enter__.return_value = mock_file_handle
        mock_block_comment_re.sub.return_value = 'CREATE TABLE test (id INTEGER); INSERT INTO test VALUES (1);'

        runner = SQLScriptRunner()
        runner.item = Path('/tmp/test.sql')
        runner._database = Mock()
        runner.database.atomic = Mock(return_value=MagicMock())
        runner.database.execute_sql = Mock()

        runner.process()

        mock_log.debug.assert_called_once_with('Found 2 statements to execute.')
        runner.database.atomic.assert_called_once()
        assert runner.database.execute_sql.call_count == 2

    @patch('builtins.open')
    @patch('mafw.processor_library.db_init.block_comment_re')
    @patch('mafw.processor_library.db_init.log')
    def test_process_with_comments_removes_correctly(self, mock_log, mock_block_comment_re, mock_open):
        """Test that block comments are properly removed from SQL content."""
        mock_file_handle = Mock()
        mock_file_handle.read.return_value = (
            '/* This is a comment */ CREATE TABLE test (id INTEGER); /* Another comment */'
        )
        mock_open.return_value.__enter__.return_value = mock_file_handle
        mock_block_comment_re.sub.return_value = ' CREATE TABLE test (id INTEGER); '

        runner = SQLScriptRunner()
        runner.item = Path('/tmp/test.sql')
        runner._database = Mock()
        runner.database.atomic = Mock(return_value=MagicMock())
        runner.database.execute_sql = Mock()

        runner.process()

        # Verify that comments were removed and statements parsed correctly
        mock_block_comment_re.sub.assert_called_once()
        assert runner.database.execute_sql.call_count == 1

    @patch('builtins.open')
    @patch('mafw.processor_library.db_init.block_comment_re')
    @patch('mafw.processor_library.db_init.log')
    def test_process_exception_rolls_back_transaction(self, mock_log, mock_block_comment_re, mock_open):
        """Test that exceptions during execution roll back transaction."""
        mock_file_handle = Mock()
        mock_file_handle.read.return_value = 'CREATE TABLE test (id INTEGER);'
        mock_open.return_value.__enter__.return_value = mock_file_handle
        mock_block_comment_re.sub.return_value = 'CREATE TABLE test (id INTEGER);'

        runner = SQLScriptRunner()
        runner.item = Path('/tmp/test.sql')
        runner._database = Mock()
        runner.database.atomic = Mock(return_value=MagicMock())
        runner.database.execute_sql = Mock(side_effect=Exception('Database error'))

        with pytest.raises(Exception, match='Database error'):
            runner.process()

        mock_log.critical.assert_any_call('An error occurred while executing the SQL script test.sql.')
        mock_log.critical.assert_any_call('Rolling back the database to preserve integrity.')
        runner.database.atomic.assert_called_once()

    def test_format_progress_message(self):
        """Test progress message formatting."""
        runner = SQLScriptRunner()
        runner.item = Path('/tmp/test.sql')
        runner.format_progress_message()
        assert runner.progress_message == 'Processing SQL file test.sql'

    @patch('builtins.open')
    @patch('mafw.processor_library.db_init.block_comment_re')
    @patch('mafw.processor_library.db_init.log')
    def test_process_empty_file(self, mock_log, mock_block_comment_re, mock_open):
        """Test processing empty file."""
        mock_file_handle = Mock()
        mock_file_handle.read.return_value = ''
        mock_open.return_value.__enter__.return_value = mock_file_handle
        mock_block_comment_re.sub.return_value = ''

        runner = SQLScriptRunner()
        runner.item = Path('/tmp/test.sql')
        runner._database = Mock()
        runner.database.atomic = Mock(return_value=MagicMock())
        runner.database.execute_sql = Mock()

        runner.process()

        mock_log.warning.assert_called_once_with('No SQL statements found to execute in test.sql.')
        runner.database.atomic.assert_called_once()
        runner.database.execute_sql.assert_not_called()

    @patch('builtins.open')
    @patch('mafw.processor_library.db_init.block_comment_re')
    @patch('mafw.processor_library.db_init.log')
    def test_process_single_statement_no_semicolon(self, mock_log, mock_block_comment_re, mock_open):
        """Test processing single statement without semicolon."""
        mock_file_handle = Mock()
        mock_file_handle.read.return_value = 'CREATE TABLE test (id INTEGER)'
        mock_open.return_value.__enter__.return_value = mock_file_handle
        mock_block_comment_re.sub.return_value = 'CREATE TABLE test (id INTEGER)'

        runner = SQLScriptRunner()
        runner.item = Path('/tmp/test.sql')
        runner._database = Mock()
        runner.database.atomic = Mock(return_value=MagicMock())
        runner.database.execute_sql = Mock()

        runner.process()

        mock_log.debug.assert_called_once_with('Found 1 statements to execute.')
        runner.database.execute_sql.assert_called_once_with('CREATE TABLE test (id INTEGER);')

    @patch('builtins.open')
    @patch('mafw.processor_library.db_init.block_comment_re')
    @patch('mafw.processor_library.db_init.log')
    def test_process_multiple_statements(self, mock_log, mock_block_comment_re, mock_open):
        """Test processing multiple statements."""
        mock_file_handle = Mock()
        mock_file_handle.read.return_value = 'CREATE TABLE test1 (id INTEGER); CREATE TABLE test2 (id INTEGER);'
        mock_open.return_value.__enter__.return_value = mock_file_handle
        mock_block_comment_re.sub.return_value = 'CREATE TABLE test1 (id INTEGER); CREATE TABLE test2 (id INTEGER);'

        runner = SQLScriptRunner()
        runner.item = Path('/tmp/test.sql')
        runner._database = Mock()
        runner.database.atomic = Mock(return_value=MagicMock())
        runner.database.execute_sql = Mock()

        runner.process()

        mock_log.debug.assert_called_once_with('Found 2 statements to execute.')
        assert runner.database.execute_sql.call_count == 2

    @patch('builtins.open')
    @patch('mafw.processor_library.db_init.block_comment_re')
    @patch('mafw.processor_library.db_init.log')
    def test_process_whitespace_only_statements(self, mock_log, mock_block_comment_re, mock_open):
        """Test processing statements with only whitespace."""
        mock_file_handle = Mock()
        mock_file_handle.read.return_value = '   \n  \n  ;  \n\n  ;  \n'
        mock_open.return_value.__enter__.return_value = mock_file_handle
        mock_block_comment_re.sub.return_value = '   \n  \n  ;  \n\n  ;  \n'

        runner = SQLScriptRunner()
        runner.item = Path('/tmp/test.sql')
        runner._database = Mock()
        runner.database.atomic = Mock(return_value=MagicMock())
        runner.database.execute_sql = Mock()

        runner.process()

        mock_log.debug.assert_called_once_with('Found 0 statements to execute.')
        runner.database.execute_sql.assert_not_called()
