#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Unit tests for the MAFwApplication runner module.
"""

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from mafw import mafw_errors
from mafw.db.std_tables import StandardTable
from mafw.decorators import single_loop
from mafw.enumerators import ProcessorExitStatus
from mafw.plugin_manager import LoadedPlugins
from mafw.processor import Processor
from mafw.runner import MAFwApplication
from mafw.ui.abstract_user_interface import UserInterfaceBase
from mafw.ui.console_user_interface import ConsoleInterface
from mafw.ui.rich_user_interface import RichInterface


class MockUserInterface(UserInterfaceBase):
    """Mock user interface for testing."""

    name = 'mock_ui'

    def __init__(self):
        pass


@pytest.fixture
def mock_plugin_manager():
    """Fixture providing a mocked plugin manager."""
    manager = Mock()
    manager.hook = Mock()
    return manager


@pytest.fixture
def mock_user_interface():
    """Fixture providing a mocked user interface."""
    ui = Mock()
    ui.name = 'test_ui'
    return ui


@pytest.fixture
def sample_steering_file(tmp_path):
    """Fixture providing a temporary steering file path."""
    steering = tmp_path / 'steering.toml'
    steering.write_text("""
analysis_name = "test_analysis"
analysis_description = "Test Description"
processors_to_run = ["TestProcessor"]

[UserInterface]
interface = "console"
""")
    return steering


@pytest.fixture
def mock_processor():
    """Fixture providing a mock processor class."""
    processor = Mock()
    processor.__name__ = 'TestProcessor'
    return processor


@single_loop
class MockProcessor(Processor):
    """Mock processor for testing."""

    def __init__(self, *args, config=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config

    def execute(self):
        return ProcessorExitStatus.Successful


class MockStandardTable(StandardTable):
    """Mock standard table for testing."""

    pass


class TestMAFwApplicationInit:
    """Test class for MAFwApplication initialization."""

    @pytest.fixture
    def mock_plugin_manager(self):
        """Fixture providing a mock plugin manager."""
        manager = Mock()
        manager.load_plugins.return_value = LoadedPlugins(
            ui_dict={'console': ConsoleInterface},
            ui_list=[RichInterface],
            processor_list=[MockProcessor],
            processor_dict={'MockProcessor': MockProcessor},
        )
        return manager

    @pytest.fixture
    def sample_config(self):
        """Fixture providing sample configuration data."""
        return {
            'analysis_name': 'test_analysis',
            'analysis_description': 'Test analysis description',
            'processors_to_run': ['MockProcessor'],
            'UserInterface': {'interface': 'console'},
            'DBConfiguration': {'host': 'localhost'},
        }

    def test_init_without_parameters(self, mock_plugin_manager):
        """Test initialization without any parameters."""
        with patch('mafw.runner.get_plugin_manager', return_value=mock_plugin_manager):
            app = MAFwApplication()

            assert app.name == 'MAFwApplication'
            assert app.plugin_manager == mock_plugin_manager
            assert app.exit_status == ProcessorExitStatus.Successful
            assert app.user_interface is None
            assert app.steering_file is None
            assert not app._initialized

    def test_init_with_ui(self, mock_plugin_manager):
        """Test initialization without any parameters."""
        with patch('mafw.runner.get_plugin_manager', return_value=mock_plugin_manager):
            ui = ConsoleInterface()

            app = MAFwApplication(user_interface=ui)

            assert app.name == 'MAFwApplication'
            assert app.plugin_manager == mock_plugin_manager
            assert app.exit_status == ProcessorExitStatus.Successful
            assert app.user_interface is ui
            assert app.steering_file is None
            assert not app._initialized

    def test_init_with_string_steering_file(self, sample_config, tmp_path):
        """Test initialization with string steering file path."""
        steering_file = tmp_path / 'test_steering.toml'

        mock_plugin_manager = Mock()
        mock_plugin_manager.load_plugins.return_value = LoadedPlugins(ui_dict={'console': MockUserInterface})

        with (
            patch('mafw.runner.get_plugin_manager', return_value=mock_plugin_manager),
            patch('mafw.tools.toml_tools.load_steering_file', return_value=sample_config),
        ):
            app = MAFwApplication(steering_file=str(steering_file))

            assert app.steering_file == steering_file
            assert app._initialized

    def test_init_with_path_steering_file(self, sample_config, tmp_path):
        """Test initialization with Path steering file."""
        steering_file = tmp_path / 'test_steering.toml'

        mock_plugin_manager = Mock()
        mock_plugin_manager.load_plugins.return_value = LoadedPlugins(ui_dict={'console': MockUserInterface})

        with (
            patch('mafw.runner.get_plugin_manager', return_value=mock_plugin_manager),
            patch('mafw.tools.toml_tools.load_steering_file', return_value=sample_config),
        ):
            app = MAFwApplication(steering_file=steering_file)

            assert app.steering_file == steering_file
            assert app._initialized

    @pytest.mark.parametrize(
        'ui_input,expected_type',
        [
            ('mock_ui', MockUserInterface),
            ('console', MockUserInterface),
        ],
    )
    def test_init_with_different_user_interfaces(self, mock_plugin_manager, ui_input, expected_type):
        """Test initialization with different user interface types."""
        console_ui = MockUserInterface
        console_ui.name = 'console'
        mock_plugin_manager.load_plugins.return_value = LoadedPlugins(ui_dict={ui_input: MockUserInterface})

        with patch('mafw.runner.get_plugin_manager', return_value=mock_plugin_manager):
            app = MAFwApplication(user_interface=ui_input)

            assert isinstance(app.user_interface, expected_type)

    def test_init_with_custom_plugin_manager(self, sample_config, tmp_path):
        """Test initialization with custom plugin manager."""
        steering_file = tmp_path / 'test_steering.toml'
        custom_manager = Mock()
        custom_manager.load_plugins.return_value = LoadedPlugins(ui_dict={'console': MockUserInterface})

        with patch('mafw.tools.toml_tools.load_steering_file', return_value=sample_config):
            app = MAFwApplication(steering_file=steering_file, plugin_manager=custom_manager)

            assert app.plugin_manager == custom_manager


class TestMAFwApplicationUserInterface:
    """Test class for user interface related methods."""

    @pytest.fixture
    def app_with_mock_manager(self):
        """Fixture providing an app with mock plugin manager."""
        manager = Mock()
        console_ui = ConsoleInterface
        rich_ui = RichInterface

        manager.load_plugins.return_value = LoadedPlugins(ui_dict={'console': console_ui, 'rich': rich_ui})

        with patch('mafw.runner.get_plugin_manager', return_value=manager):
            return MAFwApplication(), manager

    def test_get_user_interface_existing(self, app_with_mock_manager):
        """Test getting an existing user interface."""
        app, _ = app_with_mock_manager

        ui = app.get_user_interface('console')

        assert isinstance(ui, MockUserInterface)

    def test_get_user_interface_non_existing(self, app_with_mock_manager):
        """Test getting a non-existing user interface falls back to console."""
        app, _ = app_with_mock_manager

        with patch('mafw.runner.log') as mock_log:
            ui = app.get_user_interface('non_existing')

            assert isinstance(ui, MockUserInterface)
            assert ui.name == 'console'
            mock_log.warning.assert_called_once()


class TestMAFwApplicationInitMethod:
    """Test class for the init method."""

    @pytest.fixture
    def app_uninitialized(self):
        """Fixture providing an uninitialized app."""
        manager = Mock()
        console_ui = ConsoleInterface
        rich_ui = RichInterface

        manager.load_plugins.return_value = LoadedPlugins(ui_dict={'console': console_ui, 'rich': rich_ui})
        with patch('mafw.runner.get_plugin_manager', return_value=manager):
            return MAFwApplication()

    @pytest.fixture
    def sample_config(self):
        """Fixture providing sample configuration data."""
        return {
            'analysis_name': 'test_analysis',
            'analysis_description': 'Test analysis description',
            'processors_to_run': ['MockProcessor'],
            'UserInterface': {'interface': 'console'},
            'DBConfiguration': {'host': 'localhost'},
        }

    def test_init_with_string_path(self, app_uninitialized, sample_config):
        """Test init method with string path."""
        with patch('mafw.tools.toml_tools.load_steering_file', return_value=sample_config):
            app_uninitialized.init('/path/to/steering.toml')

            assert app_uninitialized._initialized
            assert app_uninitialized.steering_file == Path('/path/to/steering.toml')
            assert app_uninitialized.name == 'test_analysis'

    def test_init_with_path_object(self, app_uninitialized, sample_config):
        """Test init method with Path object."""
        path = Path('/path/to/steering.toml')

        with patch('mafw.tools.toml_tools.load_steering_file', return_value=sample_config):
            app_uninitialized.init(path)

            assert app_uninitialized._initialized
            assert app_uninitialized.steering_file == path

    def test_init_sets_user_interface_from_config(self, app_uninitialized, sample_config):
        """Test that init sets user interface from configuration."""

        with patch('mafw.tools.toml_tools.load_steering_file', return_value=sample_config):
            app_uninitialized.init('/path/to/steering.toml')

            assert app_uninitialized.user_interface is not None

    def test_init_preserves_existing_user_interface(self, app_uninitialized, sample_config):
        """Test that init preserves existing user interface."""
        existing_ui = MockUserInterface()
        app_uninitialized.user_interface = existing_ui

        with patch('mafw.tools.toml_tools.load_steering_file', return_value=sample_config):
            app_uninitialized.init('/path/to/steering.toml')

            assert app_uninitialized.user_interface == existing_ui


class TestMAFwApplicationRun:
    """Test class for the run method."""

    @pytest.fixture
    def sample_config(self):
        """Fixture providing sample configuration."""
        return {
            'analysis_name': 'test_analysis',
            'analysis_description': 'Test description',
            'processors_to_run': ['MockProcessor', 'MockProcessor#123'],
            'UserInterface': {'interface': 'console'},
            'DBConfiguration': {'host': 'localhost'},
        }

    @pytest.fixture
    def initialized_app(self, sample_config):
        """Fixture providing an initialized app."""
        manager = Mock()
        console_ui = MockUserInterface
        console_ui.name = 'console'
        manager.load_plugins.return_value = LoadedPlugins(
            ui_dict={'console': console_ui},
            ui_list=[console_ui],
            processor_list=[MockProcessor],
            processor_dict={'MockProcessor': MockProcessor},
        )

        with (
            patch('mafw.runner.get_plugin_manager', return_value=manager),
            patch('mafw.tools.toml_tools.load_steering_file', return_value=sample_config),
        ):
            return MAFwApplication(steering_file='/path/to/steering.toml')

    def test_run_not_initialized_raises_error(self):
        """Test that running uninitialized app raises error."""
        with patch('mafw.runner.get_plugin_manager'):
            app = MAFwApplication()

            with pytest.raises(mafw_errors.RunnerNotInitialized):
                app.run()

    def test_run_with_steering_file_parameter(self, sample_config):
        """Test run with steering file parameter."""
        manager = Mock()
        console_ui = MockUserInterface
        console_ui.name = 'console'
        manager.load_plugins.return_value = LoadedPlugins(
            ui_dict={'console': console_ui},
            ui_list=[console_ui],
            processor_list=[MockProcessor],
            processor_dict={'MockProcessor': MockProcessor},
        )

        with (
            patch('mafw.runner.get_plugin_manager', return_value=manager),
            patch('mafw.tools.toml_tools.load_steering_file', return_value=sample_config),
            patch('mafw.runner.ProcessorList') as mock_processor_list,
        ):
            mock_list_instance = Mock()
            mock_list_instance.execute.return_value = ProcessorExitStatus.Successful
            mock_processor_list.return_value = mock_list_instance

            app = MAFwApplication()
            result = app.run('/new/path/to/steering.toml')

            assert result == ProcessorExitStatus.Successful
            assert app.steering_file == Path('/new/path/to/steering.toml')

    def test_run_unknown_processor_raises_error(self, initialized_app):
        """Test that unknown processor raises error."""
        # Modify config to include unknown processor
        initialized_app._configuration_dict['processors_to_run'] = ['UnknownProcessor']

        with pytest.raises(mafw_errors.UnknownProcessor):
            initialized_app.run()

    def test_run_successful_execution(self, initialized_app):
        """Test successful run execution."""
        with patch('mafw.runner.ProcessorList') as mock_processor_list:
            mock_list_instance = Mock()
            mock_list_instance.execute.return_value = ProcessorExitStatus.Successful
            mock_processor_list.return_value = mock_list_instance

            result = initialized_app.run()

            assert result == ProcessorExitStatus.Successful
            mock_processor_list.assert_called_once()
            assert mock_list_instance.append.call_count == 2
            mock_list_instance.execute.assert_called_once()

    @pytest.mark.parametrize(
        'config_key,config_value',
        [
            ('analysis_description', None),
            ('processors_to_run', []),
            ('DBConfiguration', None),
            ('create_standard_tables', None),
        ],
    )
    def test_run_with_missing_config_values(self, initialized_app, config_key, config_value):
        """Test run with missing configuration values."""
        initialized_app._configuration_dict[config_key] = config_value

        with patch('mafw.processor.ProcessorList') as mock_processor_list:
            mock_list_instance = Mock()
            mock_list_instance.execute.return_value = ProcessorExitStatus.Successful
            mock_processor_list.return_value = mock_list_instance

            result = initialized_app.run()

            assert result == ProcessorExitStatus.Successful

    def test_run_processor_list_creation_parameters(self, initialized_app):
        """Test that ProcessorList is created with correct parameters."""
        with patch('mafw.runner.ProcessorList') as mock_processor_list:
            mock_list_instance = Mock()
            mock_list_instance.execute.return_value = ProcessorExitStatus.Successful
            mock_processor_list.return_value = mock_list_instance

            initialized_app.run()

            mock_processor_list.assert_called_once_with(
                name='test_analysis',
                description='Test description',
                user_interface=initialized_app.user_interface,
                database_conf={'host': 'localhost'},
                create_standard_tables=True,
            )


@pytest.mark.integration_test
class TestMAFwApplicationIntegration:
    """Integration tests for MAFwApplication."""

    def test_full_workflow_with_mocks(self, tmp_path):
        """Test complete workflow from initialization to execution."""
        # Create temporary steering file
        steering_file = tmp_path / 'test_steering.toml'

        # Mock configuration data
        config = {
            'analysis_name': 'integration_test',
            'analysis_description': 'Integration test description',
            'processors_to_run': ['MockProcessor'],
            'UserInterface': {'interface': 'console'},
            'DBConfiguration': {'host': 'localhost'},
            'create_standard_tables': True,
        }

        # Setup mocks
        manager = Mock()
        console_ui = MockUserInterface
        console_ui.name = 'console'
        manager.load_plugins.return_value = LoadedPlugins(
            ui_dict={'console': console_ui},
            ui_list=[console_ui],
            processor_list=[MockProcessor],
            processor_dict={'MockProcessor': MockProcessor},
        )

        with (
            patch('mafw.runner.get_plugin_manager', return_value=manager),
            patch('mafw.tools.toml_tools.load_steering_file', return_value=config),
            patch('mafw.runner.ProcessorList') as mock_processor_list,
        ):
            mock_list_instance = Mock()
            mock_list_instance.execute.return_value = ProcessorExitStatus.Successful
            mock_processor_list.return_value = mock_list_instance

            # Create and run application
            app = MAFwApplication(steering_file=steering_file)
            result = app.run()

            # Assertions
            assert result == ProcessorExitStatus.Successful
            assert app.name == 'integration_test'
            assert app._initialized
            assert app.steering_file == steering_file

            # Verify ProcessorList was created and executed
            mock_processor_list.assert_called_once()
            mock_list_instance.execute.assert_called_once()

    def test_error_handling_during_execution(self, tmp_path):
        """Test error handling during execution."""
        steering_file = tmp_path / 'test_steering.toml'

        config = {
            'analysis_name': 'error_test',
            'processors_to_run': ['NonExistentProcessor'],
            'UserInterface': {'interface': 'console'},
        }

        manager = Mock()
        console_ui = MockUserInterface
        console_ui.name = 'console'
        manager.load_plugins.return_value = LoadedPlugins(
            ui_dict={'console': console_ui},
            ui_list=[console_ui],
            processor_list=[MockProcessor],
            processor_dict={'MockProcessor': MockProcessor},
        )

        with (
            patch('mafw.runner.get_plugin_manager', return_value=manager),
            patch('mafw.tools.toml_tools.load_steering_file', return_value=config),
        ):
            app = MAFwApplication(steering_file=steering_file)

            with pytest.raises(mafw_errors.UnknownProcessor):
                app.run()
