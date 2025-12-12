#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
from unittest.mock import MagicMock, patch

import pytest

from mafw.lazy_import import LazyImportProcessor, LazyImportUserInterface
from mafw.processor import Processor
from mafw.ui.abstract_user_interface import UserInterfaceBase


class TestLazyImportPlugin:
    """Tests for LazyImportPlugin class."""

    @patch('importlib.import_module')
    def test_lazy_import_plugin_load(self, mock_import_module):
        """Test loading of a class using LazyImportPlugin."""
        mock_module = MagicMock()
        mock_class = MagicMock()
        mock_import_module.return_value = mock_module
        mock_module.SomeClass = mock_class

        plugin = LazyImportProcessor('mock_module', 'SomeClass')
        loaded_class = plugin._load()

        assert loaded_class == mock_class
        mock_import_module.assert_called_once_with('mock_module')

    @patch('importlib.import_module')
    def test_lazy_import_plugin_getattr(self, mock_import_module):
        """Test accessing attributes of lazily loaded class."""
        mock_module = MagicMock()
        mock_class = MagicMock()
        mock_import_module.return_value = mock_module
        mock_module.SomeClass = mock_class
        mock_class.some_attribute = 'value'

        plugin = LazyImportProcessor('mock_module', 'SomeClass')
        assert plugin.some_attribute == 'value'

    @patch('importlib.import_module')
    def test_lazy_import_plugin_call(self, mock_import_module):
        """Test instantiation of lazily loaded class."""
        mock_module = MagicMock()
        mock_class = MagicMock()
        mock_instance = MagicMock()
        mock_import_module.return_value = mock_module
        mock_module.SomeClass = mock_class
        mock_class.return_value = mock_instance

        plugin = LazyImportProcessor('mock_module', 'SomeClass')
        instance = plugin()

        assert instance == mock_instance
        mock_class.assert_called_once()


class TestLazyImportProcessor:
    """Tests for LazyImportProcessor class."""

    @patch('importlib.import_module')
    def test_lazy_import_processor_load(self, mock_import_module):
        """Test loading of a Processor class using LazyImportProcessor."""
        mock_module = MagicMock()
        mock_processor_class = MagicMock(spec=Processor)
        mock_import_module.return_value = mock_module
        mock_module.ProcessorClass = mock_processor_class

        processor_plugin = LazyImportProcessor('mock_module', 'ProcessorClass')
        loaded_class = processor_plugin._load()

        assert processor_plugin._cached is not None
        assert loaded_class == mock_processor_class

        # try reloading it,
        loaded_class2 = processor_plugin._load()
        assert loaded_class2 == mock_processor_class
        # should be called only once
        mock_import_module.assert_called_once_with('mock_module')

    def test_repr(self):
        ui_plugin = LazyImportProcessor('mock_module', 'Processor')
        assert ui_plugin.__repr__() == 'LazyImportProcessor("mock_module", "Processor")'


class TestLazyImportUserInterface:
    """Tests for LazyImportUserInterface class."""

    @patch('importlib.import_module')
    def test_lazy_import_user_interface_load(self, mock_import_module):
        """Test loading of a UserInterface class using LazyImportUserInterface."""
        mock_module = MagicMock()
        mock_ui_class = MagicMock(spec=UserInterfaceBase)
        mock_import_module.return_value = mock_module
        mock_module.UIClass = mock_ui_class
        mock_ui_class.name = 'TestUI'

        ui_plugin = LazyImportUserInterface('mock_module', 'UIClass', 'TestUI')
        loaded_class = ui_plugin._load()

        assert loaded_class == mock_ui_class
        mock_import_module.assert_called_once_with('mock_module')

    @patch('importlib.import_module')
    def test_lazy_import_user_interface_name_mismatch(self, mock_import_module):
        """Test name mismatch in LazyImportUserInterface raises ValueError."""
        mock_module = MagicMock()
        mock_ui_class = MagicMock(spec=UserInterfaceBase)
        mock_import_module.return_value = mock_module
        mock_module.UIClass = mock_ui_class
        mock_ui_class.name = 'WrongName'

        ui_plugin = LazyImportUserInterface('mock_module', 'UIClass', 'ExpectedName')

        with pytest.raises(ValueError, match='UserInterface class .* has inconsistent .name: expected ExpectedName'):
            ui_plugin._load()

    def test_repr(self):
        ui_plugin = LazyImportUserInterface('mock_module', 'UIClass', 'ExpectedName')
        assert ui_plugin.__repr__() == 'LazyImportUserInterface("mock_module", "UIClass", "ExpectedName")'
