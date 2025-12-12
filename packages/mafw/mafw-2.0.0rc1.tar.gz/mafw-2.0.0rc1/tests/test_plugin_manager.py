#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
from unittest.mock import MagicMock, patch

import pytest

from mafw.plugin_manager import LoadedPlugins, MAFwPluginManager, get_plugin_manager


@pytest.fixture
def plugin_manager():
    """Fixture for creating a plugin manager instance."""
    return MAFwPluginManager()


class TestMAFwPluginManager:
    """Tests for the MAFwPluginManager class."""

    def test_initialization(self, plugin_manager):
        """Test initialization of MAFwPluginManager."""
        assert plugin_manager.project_name == 'mafw'
        assert plugin_manager._executor._max_workers == 4

    @patch('mafw.plugin_manager.importlib.import_module')
    def test_load_db_models_plugins(self, mock_import, plugin_manager):
        """Test loading of database model plugins."""
        mock_hook = MagicMock()
        mock_hook.register_db_model_modules.return_value = [['db_module1', 'db_module2']]
        plugin_manager.hook = mock_hook

        result = plugin_manager.load_db_models_plugins()
        assert result == ['db_module1', 'db_module2']
        mock_import.assert_any_call('db_module1')
        mock_import.assert_any_call('db_module2')

    def test_load_processor_plugins(self, plugin_manager):
        """Test loading of processor plugins."""
        mock_hook = MagicMock()
        p1 = MagicMock(plugin_name='processor1')
        p2 = MagicMock(__name__='Processor2')
        delattr(p2, 'plugin_name')
        mock_hook.register_processors.return_value = [[p1, p2]]
        plugin_manager.hook = mock_hook

        processor_list, processor_dict = plugin_manager.load_processor_plugins()
        assert len(processor_list) == 2
        assert processor_dict['processor1'].plugin_name == 'processor1'
        assert processor_dict['Processor2'].__name__ == 'Processor2'

    def test_load_user_interface_plugins(self, plugin_manager):
        """Test loading of user interface plugins."""
        mock_hook = MagicMock()
        u1 = MagicMock()
        u1.name = 'UI1'
        u2 = MagicMock()
        u2.name = 'UI2'
        mock_hook.register_user_interfaces.return_value = [[u1, u2]]
        plugin_manager.hook = mock_hook

        ui_list, ui_dict = plugin_manager.load_user_interface_plugins()
        assert len(ui_list) == 2
        assert ui_dict['UI1'].name == 'UI1'
        assert ui_dict['UI2'].name == 'UI2'

    @patch('mafw.plugin_manager.ThreadPoolExecutor.submit')
    def test_load_plugins(self, mock_submit, plugin_manager):
        """Test loading plugins with different types."""
        # Mock futures for different plugin types
        mock_processor_future = MagicMock()
        mock_processor_future.result.return_value = ([], {})

        mock_ui_future = MagicMock()
        mock_ui_future.result.return_value = ([], {})

        mock_db_modules_future = MagicMock()
        mock_db_modules_future.result.return_value = []

        # Setup mock return values based on plugin type
        mock_submit.side_effect = [mock_processor_future, mock_ui_future, mock_db_modules_future, MagicMock()]
        loaded_plugins = plugin_manager.load_plugins(['processors', 'ui', 'db_modules'])
        assert isinstance(loaded_plugins, LoadedPlugins)
        assert loaded_plugins.processor_list == []
        assert loaded_plugins.ui_list == []
        assert loaded_plugins.db_model_modules == []

    @patch('mafw.plugin_manager.ThreadPoolExecutor.submit')
    def test_load_plugins_duplicates(self, mock_submit, plugin_manager):
        """Test loading plugins with different types."""
        # Mock futures for different plugin types
        mock_processor_future = MagicMock()
        mock_processor_future.result.return_value = ([], {})

        mock_ui_future = MagicMock()
        mock_ui_future.result.return_value = ([], {})

        mock_db_modules_future = MagicMock()
        mock_db_modules_future.result.return_value = []

        # Setup mock return values based on plugin type
        mock_submit.side_effect = [mock_processor_future, mock_ui_future, mock_db_modules_future, MagicMock()]
        loaded_plugins = plugin_manager.load_plugins(['processors', 'ui', 'db_modules', 'ui'])
        assert isinstance(loaded_plugins, LoadedPlugins)
        assert loaded_plugins.processor_list == []
        assert loaded_plugins.ui_list == []
        assert loaded_plugins.db_model_modules == []

    @patch('mafw.plugin_manager.ThreadPoolExecutor.submit')
    def test_load_plugins_no_plugins(self, mock_submit, plugin_manager):
        """Test loading plugins with different types."""
        # Mock futures for different plugin types
        loaded_plugins = plugin_manager.load_plugins([])
        assert isinstance(loaded_plugins, LoadedPlugins)
        assert loaded_plugins.processor_list == []
        assert loaded_plugins.ui_list == []
        assert loaded_plugins.db_model_modules == []

    @patch('mafw.plugin_manager.ThreadPoolExecutor.submit')
    def test_load_plugins_invalid(self, mock_submit, plugin_manager):
        """Test loading plugins with different types."""
        # Mock futures for different plugin types
        loaded_plugins = plugin_manager.load_plugins(['INVALID'])
        assert isinstance(loaded_plugins, LoadedPlugins)
        assert loaded_plugins.processor_list == []
        assert loaded_plugins.ui_list == []
        assert loaded_plugins.db_model_modules == []


class TestGetPluginManager:
    """Tests for the get_plugin_manager function."""

    def test_get_plugin_manager(self):
        """Test retrieval of the plugin manager."""
        pm = get_plugin_manager()
        assert isinstance(pm, MAFwPluginManager)

    def test_force_recreate(self):
        """Test force recreation of the plugin manager."""
        pm1 = get_plugin_manager()
        pm2 = get_plugin_manager(force_recreate=True)
        assert pm1 is not pm2


@pytest.mark.integration_test
def test_integration_plugin_loading():
    """Integration test for plugin loading."""
    pm = get_plugin_manager()
    loaded_plugins = pm.load_plugins(['processors', 'ui', 'db_modules'])
    assert isinstance(loaded_plugins, LoadedPlugins)


class TestDelayedStatusMessage:
    """Tests for the _delayed_status_message method."""

    def test_delayed_status_message_logs_warning(self, plugin_manager, caplog):
        """Test that a warning is logged if plugin loading takes longer than expected."""
        # Create mock futures
        completed_future = MagicMock()
        completed_future.done.return_value = True

        incomplete_future = MagicMock()
        incomplete_future.done.return_value = False

        futures = [completed_future, incomplete_future]

        # Call the method
        plugin_manager._delayed_status_message(futures)

        # Check log output
        assert 'Plugin loading is taking longer than expected, please be patient.' in caplog.text

    def test_delayed_status_message_no_warning(self, plugin_manager, caplog):
        """Test that no warning is logged if all futures are completed."""
        # Create mock futures
        completed_future = MagicMock()
        completed_future.done.return_value = True

        futures = [completed_future, completed_future]

        # Call the method
        plugin_manager._delayed_status_message(futures)

        # Check log output
        assert 'Plugin loading is taking longer than expected, please be patient.' not in caplog.text
