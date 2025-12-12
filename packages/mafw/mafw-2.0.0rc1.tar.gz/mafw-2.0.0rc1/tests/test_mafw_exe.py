#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Unit tests for the mafw_exe module.

This module contains comprehensive unit tests for the mafw execution framework,
covering all CLI commands, options, and their various combinations. The tests
use mocking to isolate functionality and ensure fast execution.

Test Classes:
    - TestLoggerSetup: Tests for logging configuration
    - TestReturnValue: Tests for return value enumeration
    - TestCLIMain: Tests for main CLI functionality
    - TestListCommand: Tests for the list processors command
    - TestSteeringCommand: Tests for steering file generation
    - TestRunCommand: Tests for the run command
    - TestDBCommands: Tests for database-related commands
    - TestDBWizardCommand: Tests for the database wizard command
"""

import logging
from unittest.mock import Mock, mock_open, patch

import pytest
from click.testing import CliRunner

from mafw import __version__
from mafw.enumerators import ProcessorExitStatus
from mafw.lazy_import import LazyImportProcessor
from mafw.mafw_errors import AbortProcessorException
from mafw.plugin_manager import LoadedPlugins
from mafw.scripts.mafw_exe import ReturnValue, cli, custom_formatwarning, display_exception, logger_setup


class TestDisplayException:
    """Test the display_exception function."""

    def test_display_exception_with_debug_flag(self, caplog):
        """Test display_exception with traceback flag enabled."""
        with caplog.at_level(logging.ERROR):
            exception = ValueError('Test error')
            display_exception(exception, show_traceback=True)

        assert 'A critical error occurred' in caplog.text
        assert 'Test error' in caplog.text

    def test_display_exception_without_debug_flag(self, caplog):
        """Test display_exception without traceback flag."""
        with caplog.at_level(logging.ERROR):
            exception = ValueError('Test error')
            display_exception(exception, show_traceback=False)

        assert 'A critical error occurred. Set option -D to get traceback output' in caplog.text
        assert 'ValueError: Test error' in caplog.text


class TestLoggerSetup:
    """
    Test class for logger setup functionality.

    This class tests the logger_setup function with different configurations
    including various log levels and UI types.
    """

    @pytest.fixture
    def mock_logger(self):
        """
        Fixture to provide a mocked logger.

        :return: Mock logger object
        :rtype: Mock
        """
        with patch('mafw.scripts.mafw_exe.log') as mock_log:
            yield mock_log

    @pytest.mark.parametrize(
        'level,expected_level',
        [
            ('debug', 10),
            ('info', 20),
            ('warning', 30),
            ('error', 40),
            ('critical', 50),
            ('DEBUG', 10),  # Test case insensitivity
            ('INFO', 20),
        ],
    )
    def test_logger_setup_levels(self, mock_logger, level, expected_level):
        """
        Test logger setup with different log levels.

        :param mock_logger: Mocked logger fixture
        :param level: Log level string to test
        :type level: str
        :param expected_level: Expected numeric log level
        :type expected_level: int
        """
        with patch('logging.StreamHandler'):
            logger_setup(level, 'console', False)
            mock_logger.setLevel.assert_called_once_with(expected_level)

    @pytest.mark.parametrize(
        'ui,tracebacks',
        [
            ('rich', True),
            ('rich', False),
            ('console', True),
            ('console', False),
            ('RICH', True),  # Test case insensitivity
            ('CONSOLE', False),
        ],
    )
    def test_logger_setup_ui_types(self, mock_logger, ui, tracebacks):
        """
        Test logger setup with different UI types and traceback settings.

        :param mock_logger: Mocked logger fixture
        :param ui: User interface type
        :type ui: str
        :param tracebacks: Whether to show tracebacks
        :type tracebacks: bool
        """
        with patch('mafw.scripts.mafw_exe.RichHandler') as mock_rich, patch('logging.StreamHandler') as mock_stream:
            logger_setup('info', ui, tracebacks)

            if ui.lower() == 'rich':
                mock_rich.assert_called_once_with(
                    rich_tracebacks=tracebacks, markup=True, show_path=False, log_time_format='%Y%m%d-%H:%M:%S'
                )
            else:
                mock_stream.assert_called_once()

    def test_custom_formatwarning(self):
        """
        Test the custom warning formatter.

        This test ensures that the custom warning formatter returns only
        the warning message without additional formatting.
        """
        message = 'Test warning message'
        category = UserWarning
        filename = 'test.py'
        lineno = 10

        result = custom_formatwarning(message, category, filename, lineno)
        assert result == str(message)


class TestReturnValue:
    """
    Test class for ReturnValue enumeration.

    This class tests the ReturnValue enum used for script exit codes.
    """

    def test_return_value_enum(self):
        """
        Test ReturnValue enumeration values.

        This test verifies that the enum values are correctly defined.
        """
        assert ReturnValue.OK == 0
        assert ReturnValue.Error == 1
        assert isinstance(ReturnValue.OK, int)
        assert isinstance(ReturnValue.Error, int)


class TestCLIMain:
    """
    Test class for main CLI functionality.

    This class tests the main CLI command group and its options.
    """

    @pytest.fixture
    def runner(self):
        """
        Fixture to provide a Click test runner.

        :return: CliRunner instance
        :rtype: CliRunner
        """
        return CliRunner()

    def test_cli_help(self, runner):
        """
        Test CLI help output.

        :param runner: Click test runner fixture
        """
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'Modular Analysis Framework execution' in result.output
        assert '--log-level' in result.output
        assert '--ui' in result.output
        assert '--debug' in result.output

    def test_cli_version(self, runner):
        """
        Test CLI version output.

        :param runner: Click test runner fixture
        """
        with patch('mafw.scripts.mafw_exe.__version__', __version__):
            result = runner.invoke(cli, ['--version'])
            assert result.exit_code == 0
            assert __version__ in result.output

    @pytest.mark.parametrize('log_level', ['debug', 'info', 'warning', 'error', 'critical'])
    def test_cli_log_levels(self, runner, log_level):
        """
        Test CLI with different log levels.

        :param runner: Click test runner fixture
        :param log_level: Log level to test
        :type log_level: str
        """
        with patch('mafw.scripts.mafw_exe.logger_setup') as mock_setup:
            result = runner.invoke(cli, ['--log-level', log_level])
            assert result.exit_code == 0
            mock_setup.assert_called_once_with(log_level, 'rich', False)

    @pytest.mark.parametrize('ui_type', ['console', 'rich'])
    def test_cli_ui_types(self, runner, ui_type):
        """
        Test CLI with different UI types.

        :param runner: Click test runner fixture
        :param ui_type: UI type to test
        :type ui_type: str
        """
        with patch('mafw.scripts.mafw_exe.logger_setup') as mock_setup:
            result = runner.invoke(cli, ['--ui', ui_type])
            assert result.exit_code == 0
            mock_setup.assert_called_once_with('info', ui_type, False)

    def test_cli_debug_flag(self, runner):
        """
        Test CLI debug flag.

        :param runner: Click test runner fixture
        """
        with patch('mafw.scripts.mafw_exe.logger_setup') as mock_setup:
            result = runner.invoke(cli, ['--debug'])
            assert result.exit_code == 0
            mock_setup.assert_called_once_with('info', 'rich', True)

    def test_cli_no_subcommand(self, runner):
        """
        Test CLI when no subcommand is provided.

        :param runner: Click test runner fixture
        """
        with patch('mafw.scripts.mafw_exe.rprint') as mock_rprint:
            result = runner.invoke(cli)
            assert result.exit_code == 0
            mock_rprint.assert_called_once_with('Use --help to get a quick help on the mafw command.')


class TestListCommand:
    """
    Test class for the list processors command.

    This class tests the list command functionality including processor
    discovery and display.
    """

    @pytest.fixture
    def runner(self):
        """
        Fixture to provide a Click test runner.

        :return: CliRunner instance
        :rtype: CliRunner
        """
        return CliRunner()

    @pytest.fixture
    def mock_processors(self):
        """
        Fixture to provide mock processor classes.

        :return: List of mock processor classes
        :rtype: list
        """
        processors = []
        for i, (pkg, mod) in enumerate([('mafw', 'processors.test'), ('external', 'pkg.mod')]):
            mock_proc = Mock()
            mock_proc.__name__ = f'TestProcessor{i}'
            mock_proc.__module__ = f'{pkg}.{mod}'
            processors.append(mock_proc)
        return processors

    @pytest.fixture
    def mock_processor_list(self):
        return [
            LazyImportProcessor('mafw.processors.test', 'MyProcessorLazy'),
            LazyImportProcessor('external.test', 'AnotherProcessorLazy'),
        ]

    @pytest.fixture
    def mock_processor_dict(self):
        return {
            'MyProcessorLazy': LazyImportProcessor('mafw.processors.test', 'MyProcessorLazy'),
            'AnotherProcessorLazy': LazyImportProcessor('external.test', 'AnotherProcessorLazy'),
        }

    @patch('mafw.scripts.mafw_exe.get_plugin_manager')
    def test_list_processors_default(self, mock_plugin_manager, runner, mock_processor_list, mock_processor_dict):
        """
        Test list processors command with default options.

        :param mock_plugin_manager: Mocked plugin manager
        :param runner: Click test runner fixture
        :param mock_processors: Mock processor fixtures
        """
        mock_pm = Mock()
        mock_pm.load_plugins.return_value = LoadedPlugins(
            processor_list=mock_processor_list, processor_dict=mock_processor_dict
        )
        mock_plugin_manager.return_value = mock_pm

        result = runner.invoke(cli, ['list'])
        assert result.exit_code == 0
        mock_plugin_manager.assert_called_once()

    @patch('mafw.scripts.mafw_exe.get_plugin_manager')
    def test_list_processors_with_exception(self, mock_plugin_manager, runner, mock_processors):
        """
        Test list processors command with default options.

        :param mock_plugin_manager: Mocked plugin manager
        :param runner: Click test runner fixture
        :param mock_processors: Mock processor fixtures
        """
        mock_pm = Mock()
        mock_pm.load_plugins.side_effect = [Exception]
        mock_plugin_manager.return_value = mock_pm

        result = runner.invoke(cli, ['list'])
        assert result.exit_code != 0
        assert 'A critical error occurred. Set option -D' in result.output
        mock_plugin_manager.assert_called_once()

    @patch('mafw.scripts.mafw_exe.get_plugin_manager')
    def test_list_processors_with_exception_width_debug(self, mock_plugin_manager, runner, mock_processors):
        """
        Test list processors command with default options.

        :param mock_plugin_manager: Mocked plugin manager
        :param runner: Click test runner fixture
        :param mock_processors: Mock processor fixtures
        """
        mock_pm = Mock()
        mock_pm.load_plugins.side_effect = [Exception]
        mock_plugin_manager.return_value = mock_pm

        result = runner.invoke(cli, ['-D', 'list'])
        assert result.exit_code != 0
        assert 'A critical error occurred' in result.output
        mock_plugin_manager.assert_called_once()


class TestSteeringCommand:
    """
    Test class for the steering file generation command.

    This class tests the steering command functionality including file
    generation, display, and editor options.
    """

    @pytest.fixture
    def runner(self):
        """
        Fixture to provide a Click test runner.

        :return: CliRunner instance
        :rtype: CliRunner
        """
        return CliRunner()

    @pytest.fixture
    def mock_processor_list(self):
        return [
            LazyImportProcessor('mafw.processors.test', 'MyProcessorLazy'),
            LazyImportProcessor('external.test', 'AnotherProcessorLazy'),
        ]

    @pytest.fixture
    def mock_processor_dict(self):
        return {
            'MyProcessorLazy': LazyImportProcessor('mafw.processors.test', 'MyProcessorLazy'),
            'AnotherProcessorLazy': LazyImportProcessor('external.test', 'AnotherProcessorLazy'),
        }

    @pytest.fixture
    def temp_steering_file(self, tmp_path):
        """
        Fixture to provide a temporary steering file path.

        :param tmp_path: Pytest temporary path fixture
        :return: Path to temporary steering file
        :rtype: pathlib.Path
        """
        return tmp_path / 'test_steering.toml'

    @patch('mafw.scripts.mafw_exe.get_plugin_manager')
    @patch('mafw.scripts.mafw_exe.generate_steering_file')
    @patch('mafw.scripts.mafw_exe.rprint')
    def test_steering_basic(
        self,
        mock_rprint,
        mock_generate,
        mock_plugin_manager,
        runner,
        temp_steering_file,
        mock_processor_list,
        mock_processor_dict,
    ):
        """
        Test basic steering file generation.

        :param mock_rprint: Mocked rich print function
        :param mock_generate: Mocked generate_steering_file function
        :param mock_plugin_manager: Mocked plugin manager
        :param runner: Click test runner fixture
        :param temp_steering_file: Temporary file path fixture
        """
        mock_pm = Mock()
        mock_pm.load_plugins.return_value = LoadedPlugins(
            processor_list=mock_processor_list, processor_dict=mock_processor_dict
        )
        mock_plugin_manager.return_value = mock_pm

        result = runner.invoke(cli, ['steering', str(temp_steering_file)])
        assert result.exit_code == 0
        mock_generate.assert_called_once()

    @patch('mafw.scripts.mafw_exe.get_plugin_manager')
    @patch('builtins.open', new_callable=mock_open, read_data='test content')
    def test_steering_with_show(
        self, mock_file, mock_plugin_manager, runner, temp_steering_file, mock_processor_list, mock_processor_dict
    ):
        """
        Test steering file generation with show option.

        :param mock_file: Mocked file open function
        :param mock_plugin_manager: Mocked plugin manager
        :param runner: Click test runner fixture
        :param temp_steering_file: Temporary file path fixture
        """
        mock_pm = Mock()
        mock_pm.load_plugins.return_value = LoadedPlugins()
        mock_plugin_manager.return_value = mock_pm

        result = runner.invoke(cli, ['steering', '--show', str(temp_steering_file)])
        assert result.exit_code == 0
        mock_file.assert_called_with(str(temp_steering_file))

    @patch('mafw.scripts.mafw_exe.get_plugin_manager')
    @patch('mafw.scripts.mafw_exe.generate_steering_file')
    @patch('click.edit')
    def test_steering_with_editor(self, mock_edit, mock_generate, mock_plugin_manager, runner, temp_steering_file):
        """
        Test steering file generation with editor option.

        :param mock_edit: Mocked click.edit function
        :param mock_generate: Mocked generate_steering_file function
        :param mock_plugin_manager: Mocked plugin manager
        :param runner: Click test runner fixture
        :param temp_steering_file: Temporary file path fixture
        """
        mock_pm = Mock()
        mock_pm.load_plugins.return_value = LoadedPlugins()
        mock_plugin_manager.return_value = mock_pm

        result = runner.invoke(cli, ['steering', '--open-editor', str(temp_steering_file)])
        assert result.exit_code == 0
        mock_edit.assert_called_once_with(filename=str(temp_steering_file))

    @pytest.mark.parametrize(
        'db_engine,db_url',
        [
            ('sqlite', ':memory:'),
            ('mysql', 'localhost:3306/test'),
            ('postgresql', 'localhost:5432/test'),
        ],
    )
    @patch('mafw.scripts.mafw_exe.get_plugin_manager')
    def test_steering_db_options(self, mock_plugin_manager, runner, temp_steering_file, db_engine, db_url):
        """
        Test steering file generation with different database options.

        :param mock_generate: Mocked generate_steering_file function
        :param mock_plugin_manager: Mocked plugin manager
        :param runner: Click test runner fixture
        :param temp_steering_file: Temporary file path fixture
        :param db_engine: Database engine to test
        :type db_engine: str
        :param db_url: Database URL to test
        :type db_url: str
        """
        mock_pm = Mock()
        mock_pm.load_plugins.return_value = LoadedPlugins()
        mock_plugin_manager.return_value = mock_pm

        result = runner.invoke(cli, ['steering', '--db-engine', db_engine, '--db-url', db_url, str(temp_steering_file)])
        assert result.exit_code == 0


class TestRunCommand:
    """
    Test class for the run command.

    This class tests the run command functionality including successful
    execution and error handling.
    """

    @pytest.fixture
    def runner(self):
        """
        Fixture to provide a Click test runner.

        :return: CliRunner instance
        :rtype: CliRunner
        """
        return CliRunner()

    @pytest.fixture
    def temp_steering_file(self, tmp_path):
        """
        Fixture to provide a temporary steering file path.

        :param tmp_path: Pytest temporary path fixture
        :return: Path to temporary steering file
        :rtype: pathlib.Path
        """
        steering_file = tmp_path / 'test_steering.toml'
        steering_file.write_text('# Test steering file')
        return steering_file

    @patch('mafw.scripts.mafw_exe.MAFwApplication')
    def test_run_success(self, mock_app_class, runner, temp_steering_file):
        """
        Test successful run command execution.

        :param mock_app_class: Mocked MAFwApplication class
        :param runner: Click test runner fixture
        :param temp_steering_file: Temporary file path fixture
        """
        mock_app = Mock()
        mock_app_class.return_value = mock_app

        mock_run = Mock(return_value=ProcessorExitStatus.Successful)
        mock_app.run = mock_run

        result = runner.invoke(cli, ['run', str(temp_steering_file)])
        assert result.exit_code == 0
        mock_app_class.assert_called_once_with(str(temp_steering_file))
        mock_run.assert_called_once()

    @patch('mafw.scripts.mafw_exe.MAFwApplication')
    def test_run_fail(self, mock_app_class, runner, temp_steering_file):
        """
        Test successful run command execution.

        :param mock_app_class: Mocked MAFwApplication class
        :param runner: Click test runner fixture
        :param temp_steering_file: Temporary file path fixture
        """
        mock_app = Mock()
        mock_app_class.return_value = mock_app

        mock_run = Mock(return_value=ProcessorExitStatus.Failed)
        mock_app.run = mock_run

        result = runner.invoke(cli, ['run', str(temp_steering_file)])
        assert result.exit_code == ReturnValue.Error
        mock_app_class.assert_called_once_with(str(temp_steering_file))
        mock_run.assert_called_once()

    @patch('mafw.scripts.mafw_exe.MAFwApplication')
    def test_run_abort(self, mock_app_class, runner, temp_steering_file):
        """
        Test successful run command execution.

        :param mock_app_class: Mocked MAFwApplication class
        :param runner: Click test runner fixture
        :param temp_steering_file: Temporary file path fixture
        """
        mock_app = Mock()
        mock_app_class.return_value = mock_app

        mock_run = Mock()
        mock_run.side_effect = AbortProcessorException()
        mock_app.run = mock_run

        result = runner.invoke(cli, ['run', str(temp_steering_file)])
        assert result.exit_code == ReturnValue.Error
        mock_app_class.assert_called_once_with(str(temp_steering_file))
        mock_run.assert_called_once()

    @patch('mafw.scripts.mafw_exe.MAFwApplication')
    @patch('mafw.scripts.mafw_exe.log')
    def test_run_exception_with_debug(self, mock_log, mock_app_class, runner, temp_steering_file):
        """
        Test run command with exception and debug enabled.

        :param mock_log: Mocked logger
        :param mock_app_class: Mocked MAFwApplication class
        :param runner: Click test runner fixture
        :param temp_steering_file: Temporary file path fixture
        """
        mock_app = Mock()
        mock_app.run.side_effect = Exception('Test error')
        mock_app_class.return_value = mock_app

        result = runner.invoke(cli, ['--debug', 'run', str(temp_steering_file)])
        assert result.exit_code == 1
        mock_log.critical.assert_called()
        mock_log.exception.assert_called()

    @patch('mafw.scripts.mafw_exe.MAFwApplication')
    @patch('mafw.scripts.mafw_exe.log')
    def test_run_exception_without_debug(self, mock_log, mock_app_class, runner, temp_steering_file):
        """
        Test run command with exception and debug disabled.

        :param mock_log: Mocked logger
        :param mock_app_class: Mocked MAFwApplication class
        :param runner: Click test runner fixture
        :param temp_steering_file: Temporary file path fixture
        """
        mock_app = Mock()
        exception = ValueError('Test error')
        mock_app.run.side_effect = exception
        mock_app_class.return_value = mock_app

        result = runner.invoke(cli, ['run', str(temp_steering_file)])
        assert result.exit_code == 1
        mock_log.exception.assert_called_with('ValueError: Test error', exc_info=False, stack_info=False, stacklevel=1)


class TestDBCommands:
    """
    Test class for database commands group.

    This class tests the database command group functionality.
    """

    @pytest.fixture
    def runner(self):
        """
        Fixture to provide a Click test runner.

        :return: CliRunner instance
        :rtype: CliRunner
        """
        return CliRunner()

    def test_db_help(self, runner):
        """
        Test database commands help output.

        :param runner: Click test runner fixture
        """
        result = runner.invoke(cli, ['db', '--help'])
        assert result.exit_code == 0
        assert 'Advanced database commands' in result.output
        assert 'wizard' in result.output


class TestDBWizardCommand:
    """
    Test class for the database wizard command.

    This class tests the database wizard functionality including different
    database engines, connection options, and file handling.
    """

    @pytest.fixture
    def runner(self):
        """
        Fixture to provide a Click test runner.

        :return: CliRunner instance
        :rtype: CliRunner
        """
        return CliRunner()

    @pytest.fixture
    def temp_output_file(self, tmp_path):
        """
        Fixture to provide a temporary output file path.

        :param tmp_path: Pytest temporary path fixture
        :return: Path to temporary output file
        :rtype: pathlib.Path
        """
        return tmp_path / 'test_model.py'

    @pytest.fixture
    def temp_db_file(self, tmp_path):
        """
        Fixture to provide a temporary database file path.

        :param tmp_path: Pytest temporary path fixture
        :return: Path to temporary database file
        :rtype: pathlib.Path
        """
        db_file = tmp_path / 'test.db'
        db_file.write_text('# Test database')
        return db_file

    @patch('mafw.scripts.mafw_exe.make_introspector')
    @patch('mafw.scripts.mafw_exe.dump_models')
    @patch('mafw.scripts.mafw_exe.log')
    def test_wizard_sqlite_success(
        self, mock_log, mock_dump, mock_introspector, runner, temp_output_file, temp_db_file
    ):
        """
        Test successful wizard execution with SQLite database.

        :param mock_log: Mocked logger
        :param mock_dump: Mocked dump_models function
        :param mock_introspector: Mocked make_introspector function
        :param runner: Click test runner fixture
        :param temp_output_file: Temporary output file fixture
        :param temp_db_file: Temporary database file fixture
        """
        mock_intro = Mock()
        mock_introspector.return_value = mock_intro

        result = runner.invoke(cli, ['db', 'wizard', '-o', str(temp_output_file), '-e', 'sqlite', str(temp_db_file)])

        assert result.exit_code == 0
        mock_introspector.assert_called_once()
        mock_dump.assert_called_once()
        mock_log.info.assert_called()

    @patch('mafw.scripts.mafw_exe.dump_models')
    @patch('mafw.scripts.mafw_exe.make_introspector')
    def test_wizard_postgresql_with_options(self, mock_introspector, mock_dumper, runner, temp_output_file):
        """
        Test wizard execution with PostgreSQL and connection options.

        :param mock_file: Mocked file open function
        :param mock_dump: Mocked dump_models function
        :param mock_introspector: Mocked make_introspector function
        :param runner: Click test runner fixture
        :param temp_output_file: Temporary output file fixture
        """
        mock_intro = Mock()
        mock_introspector.return_value = mock_intro

        mock_dump = Mock()
        mock_dumper.return_value = mock_dump

        result = runner.invoke(
            cli,
            [
                'db',
                'wizard',
                '-o',
                str(temp_output_file),
                '-e',
                'postgresql',
                '--host',
                'localhost',
                '--port',
                '5432',
                '--user',
                'testuser',
                '--password',
                'testpass',
                '--schema',
                'public',
                'testdb',
            ],
            input='testpass\n',
        )

        assert result.exit_code == 0
        mock_introspector.assert_called_once()
        mock_dumper.assert_called_once()

    @pytest.mark.parametrize(
        'tables',
        [
            [],
            ['table1'],
            ['table1', 'table2', 'table3'],
        ],
    )
    @patch('mafw.scripts.mafw_exe.make_introspector')
    @patch('mafw.scripts.mafw_exe.dump_models')
    def test_wizard_table_selection(self, mock_dump, mock_introspector, runner, temp_output_file, temp_db_file, tables):
        """
        Test wizard with different table selections.

        :param mock_introspector: Mocked make_introspector function
        :param runner: Click test runner fixture
        :param temp_output_file: Temporary output file fixture
        :param temp_db_file: Temporary database file fixture
        :param tables: List of tables to select
        :type tables: list
        """
        mock_intro = Mock()
        mock_introspector.return_value = mock_intro

        cmd = ['db', 'wizard', '-o', str(temp_output_file), '-e', 'sqlite']
        for table in tables:
            cmd.extend(['-t', table])
        cmd.append(str(temp_db_file))

        result = runner.invoke(cli, cmd)
        assert result.exit_code == 0

        # Check if dump_models was called with correct table parameter
        call_args = mock_dump.call_args
        if tables:
            assert call_args[0][2] == tuple(tables)
        else:
            assert call_args[0][2] is None

    @pytest.mark.parametrize(
        'overwrite,preserve_order,with_views,ignore_unknown,snake_case',
        [
            (True, True, False, False, True),
            (False, False, True, True, False),
            (True, False, False, True, True),
        ],
    )
    @patch('mafw.scripts.mafw_exe.make_introspector')
    @patch('mafw.scripts.mafw_exe.dump_models')
    def test_wizard_boolean_options(
        self,
        mock_dump,
        mock_introspector,
        runner,
        temp_output_file,
        temp_db_file,
        overwrite,
        preserve_order,
        with_views,
        ignore_unknown,
        snake_case,
    ):
        """
        Test wizard with different boolean option combinations.

        :param mock_dump: Mocked dump_models function
        :param mock_introspector: Mocked make_introspector function
        :param runner: Click test runner fixture
        :param temp_output_file: Temporary output file fixture
        :param temp_db_file: Temporary database file fixture
        :param overwrite: Overwrite option value
        :type overwrite: bool
        :param preserve_order: Preserve order option value
        :type preserve_order: bool
        :param with_views: With views option value
        :type with_views: bool
        :param ignore_unknown: Ignore unknown option value
        :type ignore_unknown: bool
        :param snake_case: Snake case option value
        :type snake_case: bool
        """
        mock_intro = Mock()
        mock_introspector.return_value = mock_intro

        cmd = ['db', 'wizard', '-o', str(temp_output_file), '-e', 'sqlite']

        # Add boolean flags based on values
        if overwrite:
            cmd.append('--overwrite')
        else:
            cmd.append('--no-overwrite')

        if preserve_order:
            cmd.append('--preserve-order')
        else:
            cmd.append('--no-preserve-order')

        if with_views:
            cmd.append('--with-views')
        else:
            cmd.append('--without-views')

        if ignore_unknown:
            cmd.append('--ignore-unknown')
        else:
            cmd.append('--no-ignore-unknown')

        if snake_case:
            cmd.append('--snake-case')
        else:
            cmd.append('--no-snake-case')

        cmd.append(str(temp_db_file))

        result = runner.invoke(cli, cmd)
        assert result.exit_code == 0

        # Verify dump_models was called with correct parameters
        call_args = mock_dump.call_args
        assert call_args[1]['preserve_order'] == preserve_order
        assert call_args[1]['include_views'] == with_views
        assert call_args[1]['ignore_unknown'] == ignore_unknown
        assert call_args[1]['snake_case'] == snake_case

    @pytest.mark.parametrize('debug', [False, True])
    @patch('mafw.scripts.mafw_exe.make_introspector')
    @patch('mafw.scripts.mafw_exe.log')
    def test_wizard_introspector_error(
        self, mock_log, mock_introspector, debug, runner, temp_output_file, temp_db_file
    ):
        """
        Test wizard with introspector error and debug enabled.

        :param mock_log: Mocked logger
        :param mock_introspector: Mocked make_introspector function
        :param runner: Click test runner fixture
        :param temp_output_file: Temporary output file fixture
        """
        mock_introspector.side_effect = Exception('Connection failed')

        if debug:
            cmd = ['-D', 'db', 'wizard', '-o', str(temp_output_file), '-e', 'sqlite', str(temp_db_file)]
        else:
            cmd = ['db', 'wizard', '-o', str(temp_output_file), '-e', 'sqlite', str(temp_db_file)]

        result = runner.invoke(cli, cmd)

        assert result.exit_code == 1
        mock_log.critical.assert_called()

    @pytest.mark.parametrize('debug', [False, True])
    @patch('mafw.scripts.mafw_exe.make_introspector')
    @patch('mafw.scripts.mafw_exe.dump_models')
    @patch('mafw.scripts.mafw_exe.log')
    def test_wizard_dump_error(
        self, mock_log, mock_dump, mock_introspector, debug, runner, temp_output_file, temp_db_file
    ):
        """
        Test wizard with dump_models error.

        :param mock_log: Mocked logger
        :param mock_dump: Mocked dump_models function
        :param mock_introspector: Mocked make_introspector function
        :param runner: Click test runner fixture
        :param temp_output_file: Temporary output file fixture
        :param temp_db_file: Temporary database file fixture
        """
        mock_intro = Mock()
        mock_introspector.return_value = mock_intro
        mock_dump.side_effect = Exception('Dump failed')

        if debug:
            cmd = ['-D', 'db', 'wizard', '-o', str(temp_output_file), '-e', 'sqlite', str(temp_db_file)]
        else:
            cmd = ['db', 'wizard', '-o', str(temp_output_file), '-e', 'sqlite', str(temp_db_file)]

        result = runner.invoke(cli, cmd)

        assert result.exit_code != 0
        mock_log.critical.assert_called()
        mock_log.exception.assert_called()

    @patch('pathlib.Path.exists')
    @patch('mafw.scripts.mafw_exe.Prompt.ask')
    @patch('mafw.scripts.mafw_exe.make_introspector')
    @patch('mafw.scripts.mafw_exe.dump_models')
    def test_wizard_overwrite_prompt_cancel(
        self, mock_dump, mock_introspector, mock_prompt, mock_exists, runner, temp_output_file, temp_db_file
    ):
        """
        Test wizard with overwrite prompt - cancel option.

        :param mock_dump: Mocked dump_models function
        :param mock_introspector: Mocked make_introspector function
        :param mock_prompt: Mocked Prompt.ask function
        :param mock_exists: Mocked Path.exists function
        :param runner: Click test runner fixture
        :param temp_output_file: Temporary output file fixture
        :param temp_db_file: Temporary database file fixture
        """
        mock_exists.return_value = True
        mock_prompt.return_value = 'c'  # Cancel

        result = runner.invoke(
            cli, ['db', 'wizard', '--no-overwrite', '-o', str(temp_output_file), '-e', 'sqlite', str(temp_db_file)]
        )

        assert result.exit_code == 0
        mock_introspector.assert_not_called()
        mock_dump.assert_not_called()

    @patch('pathlib.Path.exists')
    @patch('mafw.scripts.mafw_exe.Prompt.ask')
    @patch('shutil.copy')
    @patch('mafw.scripts.mafw_exe.make_introspector')
    @patch('mafw.scripts.mafw_exe.dump_models')
    def test_wizard_overwrite_prompt_backup(
        self, mock_dump, mock_introspector, mock_copy, mock_prompt, mock_exists, runner, temp_output_file, temp_db_file
    ):
        """
        Test wizard with overwrite prompt - backup option.

        :param mock_dump: Mocked dump_models function
        :param mock_introspector: Mocked make_introspector function
        :param mock_copy: Mocked shutil.copy function
        :param mock_prompt: Mocked Prompt.ask function
        :param mock_exists: Mocked Path.exists function
        :param runner: Click test runner fixture
        :param temp_output_file: Temporary output file fixture
        :param temp_db_file: Temporary database file fixture
        """
        mock_exists.return_value = True
        mock_prompt.return_value = 'b'  # Backup

        mock_intro = Mock()
        mock_introspector.return_value = mock_intro

        result = runner.invoke(
            cli, ['db', 'wizard', '--no-overwrite', '-o', str(temp_output_file), '-e', 'sqlite', str(temp_db_file)]
        )

        assert result.exit_code == 0
        mock_copy.assert_called_once()
        mock_introspector.assert_called_once()
        mock_dump.assert_called_once()

    @patch('pathlib.Path.exists')
    def test_wizard_engine_auto_detection_sqlite(self, mock_exists, runner, temp_output_file, temp_db_file):
        """
        Test wizard with automatic engine detection for SQLite.

        :param mock_exists: Mocked Path.exists function
        :param runner: Click test runner fixture
        :param temp_output_file: Temporary output file fixture
        :param temp_db_file: Temporary database file fixture
        """
        mock_exists.return_value = True

        with (
            patch('mafw.scripts.mafw_exe.make_introspector') as mock_introspector,
            patch('mafw.scripts.mafw_exe.dump_models'),
            patch('builtins.open', mock_open()),
        ):
            mock_intro = Mock()
            mock_introspector.return_value = mock_intro

            result = runner.invoke(cli, ['db', 'wizard', '-o', str(temp_output_file), str(temp_db_file)])

            assert result.exit_code == 0
            # Verify sqlite engine was used
            call_args = mock_introspector.call_args
            assert call_args[0][0] == 'sqlite'

    @patch('pathlib.Path.exists')
    def test_wizard_engine_auto_detection_postgresql(self, mock_exists, runner, temp_output_file):
        """
        Test wizard with automatic engine detection for PostgreSQL.

        :param mock_exists: Mocked Path.exists function
        :param runner: Click test runner fixture
        :param temp_output_file: Temporary output file fixture
        """
        mock_exists.return_value = False

        with (
            patch('mafw.scripts.mafw_exe.make_introspector') as mock_introspector,
            patch('builtins.open', mock_open()),
            patch('mafw.scripts.mafw_exe.dump_models') as mock_dumper,
        ):
            mock_intro = Mock()
            mock_introspector.return_value = mock_intro

            mock_dumper.return_value = Mock()

            result = runner.invoke(cli, ['db', 'wizard', '-o', str(temp_output_file), 'testdb'])

            assert result.exit_code == 0
            # Verify postgresql engine was used
            call_args = mock_introspector.call_args
            assert call_args[0][0] == 'postgresql'

    def test_wizard_help(self, runner):
        """
        Test wizard command help output.

        :param runner: Click test runner fixture
        """
        result = runner.invoke(cli, ['db', 'wizard', '--help'])
        assert result.exit_code == 0
        assert 'Reflect an existing DB into a python module' in result.output
        assert '--output-file' in result.output
        assert '--schema' in result.output
        assert '--tables' in result.output
        assert '--engine' in result.output

    @pytest.mark.parametrize('engine', ['sqlite', 'sqlite3', 'mysql', 'postgresql'])
    @patch('mafw.scripts.mafw_exe.make_introspector')
    @patch('mafw.scripts.mafw_exe.dump_models')
    def test_wizard_different_engines(self, mock_dumper, mock_introspector, runner, temp_output_file, engine):
        """
        Test wizard with different database engines.

        :param mock_introspector: Mocked make_introspector function
        :param runner: Click test runner fixture
        :param temp_output_file: Temporary output file fixture
        :param engine: Database engine to test
        :type engine: str
        """
        mock_intro = Mock()
        mock_introspector.return_value = mock_intro

        mock_dumper.return_value = Mock()

        result = runner.invoke(
            cli,
            [
                'db',
                'wizard',
                '-o',
                str(temp_output_file),
                '-e',
                engine,
                '--host',
                'localhost',
                '--port',
                '5432',
                '--user',
                'testuser',
                '--schema',
                'public',
                'testdb',
            ],
        )

        assert result.exit_code == 0
        mock_introspector.assert_called_once()
        mock_dumper.assert_called_once()

        # Verify correct connection options were passed
        call_args = mock_introspector.call_args
        if engine in ['sqlite', 'sqlite3']:
            # For SQLite, only schema should be in connection options
            expected_keys = {'schema'}
        else:
            # For other engines, all connection options should be present
            expected_keys = {'host', 'port', 'user', 'schema'}

        actual_keys = set(call_args[1].keys())
        assert expected_keys.issubset(actual_keys)


@pytest.mark.integration_test
class TestIntegration:
    """
    Integration test class for testing command combinations and workflows.

    This class tests realistic usage scenarios and command combinations
    that users might execute in practice.
    """

    @pytest.fixture
    def runner(self):
        """
        Fixture to provide a Click test runner.

        :return: CliRunner instance
        :rtype: CliRunner
        """
        return CliRunner()

    @pytest.fixture
    def temp_files(self, tmp_path):
        """
        Fixture to provide temporary file paths for integration tests.

        :param tmp_path: Pytest temporary path fixture
        :return: Dictionary of temporary file paths
        :rtype: dict
        """
        return {
            'steering': tmp_path / 'integration_steering.toml',
            'model': tmp_path / 'integration_model.py',
            'db': tmp_path / 'integration.db',
        }

    @patch('mafw.scripts.mafw_exe.get_plugin_manager')
    @patch('mafw.scripts.mafw_exe.generate_steering_file')
    @patch('mafw.scripts.mafw_exe.MAFwApplication')
    def test_steering_then_run_workflow(self, mock_app_class, mock_generate, mock_plugin_manager, runner, temp_files):
        """
        Test complete workflow: generate steering file then run it.

        :param mock_app_class: Mocked MAFwApplication class
        :param mock_generate: Mocked generate_steering_file function
        :param mock_plugin_manager: Mocked plugin manager
        :param runner: Click test runner fixture
        :param temp_files: Temporary files fixture
        """
        # Setup mocks
        mock_pm = Mock()
        mock_pm.hook.register_processors.return_value = [[]]
        mock_plugin_manager.return_value = mock_pm

        mock_app = Mock()
        mock_app_class.return_value = mock_app

        mock_run = Mock(return_value=ProcessorExitStatus.Successful)
        mock_app.run = mock_run

        # First, generate steering file
        result1 = runner.invoke(cli, ['steering', str(temp_files['steering'])])
        assert result1.exit_code == 0
        mock_generate.assert_called_once()

        # Create the file to simulate successful generation
        temp_files['steering'].write_text('# Generated steering file')

        # Then, run the steering file
        result2 = runner.invoke(cli, ['run', str(temp_files['steering'])])
        assert result2.exit_code == 0
        mock_app.run.assert_called_once()

    @patch('mafw.scripts.mafw_exe.make_introspector')
    @patch('mafw.scripts.mafw_exe.dump_models')
    def test_db_wizard_with_all_options(self, mock_dump, mock_introspector, runner, temp_files):
        """
        Test database wizard with comprehensive option set.

        :param mock_dump: Mocked dump_models function
        :param mock_introspector: Mocked make_introspector function
        :param runner: Click test runner fixture
        :param temp_files: Temporary files fixture
        """
        mock_intro = Mock()
        mock_introspector.return_value = mock_intro

        result = runner.invoke(
            cli,
            [
                '--log-level',
                'debug',
                '--ui',
                'console',
                'db',
                'wizard',
                '-o',
                str(temp_files['model']),
                '-s',
                'public',
                '-t',
                'table1',
                '-t',
                'table2',
                '--overwrite',
                '--preserve-order',
                '--with-views',
                '--ignore-unknown',
                '--snake-case',
                '--host',
                'localhost',
                '--port',
                '5432',
                '--user',
                'testuser',
                '-e',
                'postgresql',
                'testdb',
            ],
        )

        assert result.exit_code == 0
        mock_introspector.assert_called_once()
        mock_dump.assert_called_once()

        # Verify all options were passed correctly
        dump_call_args = mock_dump.call_args
        assert dump_call_args[0][2] == ('table1', 'table2')
        assert dump_call_args[1]['preserve_order'] is True
        assert dump_call_args[1]['include_views'] is True
        assert dump_call_args[1]['ignore_unknown'] is True
        assert dump_call_args[1]['snake_case'] is True

    def test_command_help_hierarchy(self, runner):
        """
        Test that all commands have proper help documentation.

        :param runner: Click test runner fixture
        """
        # Test main help
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'Modular Analysis Framework execution' in result.output

        # Test subcommand helps
        commands_to_test = [
            (['list', '--help'], 'Display the list of available processors'),
            (['steering', '--help'], 'Generates a steering file'),
            (['run', '--help'], 'Runs a steering file'),
            (['db', '--help'], 'Advanced database commands'),
            (['db', 'wizard', '--help'], 'Reflect an existing DB'),
        ]

        for cmd, expected_text in commands_to_test:
            result = runner.invoke(cli, cmd)
            assert result.exit_code == 0
            assert expected_text in result.output


class TestEdgeCases:
    """
    Test class for edge cases and error conditions.

    This class covers unusual inputs, boundary conditions, and
    error scenarios that might occur in real usage.
    """

    @pytest.fixture
    def mock_processor(self):
        mock_proc = Mock()
        mock_proc.__name__ = 'TestProcessor'
        mock_proc.__module__ = 'mafw.proclib'
        return mock_proc

    @pytest.fixture
    def mock_processor_list(self, mock_processor):
        return [
            LazyImportProcessor('mafw.processors.test', 'MyProcessorLazy'),
            LazyImportProcessor('external.test', 'AnotherProcessorLazy'),
            mock_processor,
        ]

    @pytest.fixture
    def mock_processor_dict(self, mock_processor):
        return {
            'MyProcessorLazy': LazyImportProcessor('mafw.processors.test', 'MyProcessorLazy'),
            'AnotherProcessorLazy': LazyImportProcessor('external.test', 'AnotherProcessorLazy'),
            'TestProcessor': mock_processor,
        }

    @pytest.fixture
    def runner(self):
        """
        Fixture to provide a Click test runner.

        :return: CliRunner instance
        :rtype: CliRunner
        """
        return CliRunner()

    @pytest.fixture
    def mock_processors(self):
        """
        Fixture to provide mock processor classes.

        :return: List of mock processor classes
        :rtype: list
        """
        processors = []
        for i, (pkg, mod) in enumerate([('mafw', 'processors.test'), ('external', 'pkg.mod')]):
            mock_proc = Mock()
            mock_proc.__name__ = f'TestProcessor{i}'
            mock_proc.__module__ = f'{pkg}.{mod}'
            processors.append(mock_proc)
        return processors

    def test_invalid_log_level(self, runner):
        """
        Test CLI with invalid log level.

        :param runner: Click test runner fixture
        """
        result = runner.invoke(cli, ['--log-level', 'invalid'])
        assert result.exit_code != 0
        assert 'Invalid value' in result.output

    def test_invalid_ui_type(self, runner):
        """
        Test CLI with invalid UI type.

        :param runner: Click test runner fixture
        """
        result = runner.invoke(cli, ['--ui', 'invalid'])
        assert result.exit_code != 0
        assert 'Invalid value' in result.output

    def test_invalid_db_engine(self, runner):
        """
        Test steering command with invalid database engine.

        :param runner: Click test runner fixture
        """
        result = runner.invoke(cli, ['steering', '--db-engine', 'invalid', 'test.toml'])
        assert result.exit_code != 0
        assert 'Invalid value' in result.output

    @patch('mafw.scripts.mafw_exe.MAFwApplication')
    def test_run_nonexistent_file(self, mock_app_class, runner):
        """
        Test run command with nonexistent steering file.

        :param mock_app_class: Mocked MAFwApplication class
        :param runner: Click test runner fixture
        """
        mock_app_class.side_effect = FileNotFoundError('File not found')

        result = runner.invoke(cli, ['run', 'nonexistent.toml'])
        assert result.exit_code == 1

    @pytest.mark.parametrize('alias', ['list', 'lis', 'li', 'l'])
    @patch('mafw.scripts.mafw_exe.get_plugin_manager')
    def test_abbreviation(self, mock_plugin_manager, alias, runner, mock_processor_list, mock_processor_dict):
        mock_pm = Mock()
        mock_pm.load_plugins.return_value = LoadedPlugins(
            processor_list=mock_processor_list, processor_dict=mock_processor_dict
        )
        mock_plugin_manager.return_value = mock_pm

        result = runner.invoke(cli, [alias])
        assert result.exit_code == 0
        mock_plugin_manager.assert_called_once()

    @patch('mafw.scripts.mafw_exe.get_plugin_manager')
    def test_missing_command(self, mock_plugin_manager, runner, mock_processor_list, mock_processor_dict):
        mock_pm = Mock()
        mock_pm.load_plugins.return_value = LoadedPlugins(
            processor_list=mock_processor_list, processor_dict=mock_processor_dict
        )
        mock_plugin_manager.return_value = mock_pm

        result = runner.invoke(cli, ['lista'])
        assert result.exit_code != 0

    @patch('mafw.scripts.mafw_exe.get_plugin_manager')
    @patch('mafw.scripts.mafw_exe.log')
    def test_steering_with_plugin_manager_error(self, mock_log, mock_plugin_manager, runner, tmp_path):
        """
        Test steering command when plugin manager fails.

        :param mock_log: Mocked logger
        :param mock_plugin_manager: Mocked plugin manager
        :param runner: Click test runner fixture
        :param tmp_path: Pytest temporary path fixture
        """
        mock_plugin_manager.side_effect = Exception('Plugin manager failed')
        steering_file = tmp_path / 'test.toml'

        runner.invoke(cli, ['steering', str(steering_file)])
        mock_log.exception.assert_called_with(
            'Exception: Plugin manager failed', exc_info=False, stack_info=False, stacklevel=1
        )

    @patch('mafw.scripts.mafw_exe.get_plugin_manager')
    @patch('mafw.scripts.mafw_exe.log')
    def test_steering_with_plugin_manager_error_with_debug(self, mock_log, mock_plugin_manager, runner, tmp_path):
        """
        Test steering command when plugin manager fails.

        :param mock_log: Mocked logger
        :param mock_plugin_manager: Mocked plugin manager
        :param runner: Click test runner fixture
        :param tmp_path: Pytest temporary path fixture
        """
        mock_plugin_manager.side_effect = Exception('Plugin manager failed')
        steering_file = tmp_path / 'test.toml'

        runner.invoke(cli, ['-D', 'steering', str(steering_file)])
        mock_log.critical.assert_called_with('A critical error occurred')


class TestMockingBehavior:
    """
    Test class to verify mocking behavior and test isolation.

    This class ensures that mocks are properly isolated between tests
    and that the testing infrastructure itself is working correctly.
    """

    @pytest.fixture
    def runner(self):
        """
        Fixture to provide a Click test runner.

        :return: CliRunner instance
        :rtype: CliRunner
        """
        return CliRunner()

    def test_mock_isolation(self, runner):
        """
        Test that mocks don't leak between test methods.

        :param runner: Click test runner fixture
        """
        # This test ensures that previous mocks don't affect this test
        with patch('mafw.scripts.mafw_exe.logger_setup') as mock_setup:
            result = runner.invoke(cli, ['--log-level', 'debug'])
            assert result.exit_code == 0
            mock_setup.assert_called_once_with('debug', 'rich', False)

    def test_fixture_behavior(self, runner):
        """
        Test that fixtures behave consistently.

        :param runner: Click test runner fixture
        """
        # Test that the runner fixture provides a clean CliRunner instance
        assert isinstance(runner, CliRunner)

        # Run a simple command to ensure the runner works
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'Modular Analysis Framework execution' in result.output

    @patch('mafw.scripts.mafw_exe.rprint')
    def test_patch_decorator_behavior(self, mock_rprint, runner):
        """
        Test that patch decorators work correctly.

        :param mock_rprint: Mocked rich print function
        :param runner: Click test runner fixture
        """
        result = runner.invoke(cli)
        assert result.exit_code == 0
        mock_rprint.assert_called_once_with('Use --help to get a quick help on the mafw command.')
