#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Unit tests for the ModelRegister class.
"""

import logging
from unittest.mock import MagicMock, patch

import peewee
import pytest

from mafw.db.db_model import MAFwBaseModel
from mafw.db.model_register import ModelRegister


class TestModelRegister:
    """Test cases for ModelRegister class."""

    @pytest.fixture
    def mock_model(self):
        mock_model = MagicMock(spec=peewee.Model)
        mock_model.__name__ = 'MockModel'
        return mock_model

    @pytest.fixture
    def mock_model2(self):
        mock_model2 = MagicMock(spec=peewee.Model)
        mock_model2.__name__ = 'MockModel2'
        return mock_model2

    def test_init(self):
        """Test initialization of ModelRegister."""
        register = ModelRegister()
        assert register.models == {}
        assert register.prefixes == []
        assert register.suffixes == []

    def test_register_model(self, mock_model):
        """Test registering a model."""
        register = ModelRegister()
        register.register_model('test_table', mock_model)
        assert register.models['test_table'] == mock_model

    def test_register_model_replace_warning(self, caplog, mock_model, mock_model2):
        """Test registering a model that already exists shows warning."""
        register = ModelRegister()
        register.register_model('test_table', mock_model)
        register.register_model('test_table', mock_model2)
        assert 'already exists' in caplog.text

    def test_register_prefix(self):
        """Test registering a prefix."""
        register = ModelRegister()
        register.register_prefix('prefix_')
        assert 'prefix_' in register.prefixes

    def test_register_prefix_duplicate(self):
        """Test registering duplicate prefix is ignored."""
        register = ModelRegister()
        register.register_prefix('prefix_')
        register.register_prefix('prefix_')
        assert register.prefixes == ['prefix_']

    def test_register_suffix(self):
        """Test registering a suffix."""
        register = ModelRegister()
        register.register_suffix('_suffix')
        assert '_suffix' in register.suffixes

    def test_register_suffix_duplicate(self):
        """Test registering duplicate suffix is ignored."""
        register = ModelRegister()
        register.register_suffix('_suffix')
        register.register_suffix('_suffix')
        assert register.suffixes == ['_suffix']

    @pytest.mark.parametrize('name', ['test_table', 'MockModel'])
    def test_get_model_exact_match(self, name, mock_model):
        """Test getting a model with exact table name match."""
        register = ModelRegister()
        register.register_model('test_table', mock_model)
        result = register.get_model(name)
        assert result == mock_model

    def test_get_model_with_prefix(self, mock_model):
        """Test getting a model with prefix match."""
        register = ModelRegister()
        register.register_prefix('app_')
        register.register_model('app_test_table', mock_model)
        result = register.get_model('test_table')
        assert result == mock_model

    def test_get_model_with_suffix(self, mock_model):
        """Test getting a model with suffix match."""
        register = ModelRegister()
        register.register_suffix('_table')
        register.register_model('test_table', mock_model)
        result = register.get_model('test')
        assert result == mock_model

    def test_get_model_with_prefix_and_suffix(self, mock_model):
        """Test getting a model with both prefix and suffix match."""
        register = ModelRegister()
        register.register_prefix('app_')
        register.register_suffix('_table')
        register.register_model('app_test_table', mock_model)
        result = register.get_model('test')
        assert result == mock_model

    def test_get_model_camel_case_conversion(self, mock_model):
        """Test getting a model with camelCase name conversion."""
        register = ModelRegister()
        register.register_prefix('app_')
        register.register_model('test_table', mock_model)
        result = register.get_model('TestTable')
        assert result == mock_model

    def test_get_model_not_found_raises_keyerror(self, caplog):
        """Test getting a non-existent model raises KeyError."""
        register = ModelRegister()
        with pytest.raises(KeyError, match='not registered'):
            register.get_model('non_existent')

    def test_get_model_not_found_logs_available_models(self, caplog, mock_model):
        """Test that error message includes available models."""
        register = ModelRegister()
        register.register_model('existing_table', mock_model)
        with pytest.raises(KeyError):
            register.get_model('non_existent')
        assert 'existing_table' in caplog.text

    def test_get_model_multiple_matches_raises_keyerror(self, caplog, mock_model, mock_model2):
        """Test getting a model with multiple similar matches raises KeyError."""
        register = ModelRegister()
        register.register_prefix('app_')
        register.register_suffix('_table')
        register.register_model('app_test', mock_model)
        register.register_model('test_table', mock_model2)
        with pytest.raises(KeyError, match='multiple similar'):
            register.get_model('test')

    def test_get_model_multiple_matches_logs_options(self, caplog, mock_model, mock_model2):
        """Test that error message includes multiple similar options."""
        register = ModelRegister()
        register.register_prefix('app_')
        register.register_suffix('_table')
        register.register_model('app_test', mock_model)
        register.register_model('test_table', mock_model2)
        with pytest.raises(KeyError):
            register.get_model('test')
        assert 'app_test' in caplog.text
        assert 'test_table' in caplog.text

    def test_get_model_warns_on_fallback(self, caplog, mock_model):
        """Test that fallback to similar model shows warning."""
        with caplog.at_level(logging.DEBUG):
            register = ModelRegister()
            register.register_prefix('app_')
            register.register_model('app_test_table', mock_model)
            result = register.get_model('test_table')
            assert 'not found, but' in caplog.text
            assert result == mock_model

    def test_get_table_names(self, mock_model, mock_model2):
        """Test getting list of registered model names."""
        register = ModelRegister()
        register.register_model('table1', mock_model)
        register.register_model('table2', mock_model2)
        result = register.get_table_names()
        assert set(result) == {'table1', 'table2'}

    def test_get_model_names(self, mock_model, mock_model2):
        """Test getting list of registered model names."""
        register = ModelRegister()
        register.register_model('table1', mock_model)
        register.register_model('table2', mock_model2)
        result = register.get_model_names()
        assert set(result) == {'MockModel', 'MockModel2'}

    @patch('peewee.make_snake_case')
    def test_get_model_with_mocked_make_snake_case(self, mock_make_snake_case, mock_model):
        """Test get_model with mocked peewee.make_snake_case function."""
        mock_make_snake_case.return_value = 'snake_case_name'
        register = ModelRegister()
        register.register_prefix('prefix_')
        register.register_model('prefix_snake_case_name', mock_model)
        result = register.get_model('camelCaseName')
        assert result == mock_model
        mock_make_snake_case.assert_called_with('camelCaseName')

    def test_empty_prefixes_and_suffixes_handling(self, mock_model):
        """Test handling when prefixes and suffixes lists are empty."""
        register = ModelRegister()
        register.register_model('test_table', mock_model)
        result = register.get_model('test_table')
        assert result == mock_model

    def test_items_returns_correct_items_view(self, mock_model, mock_model2):
        """Test that items() returns correct items view with registered models."""
        register = ModelRegister()
        register.register_model('table1', mock_model)
        register.register_model('table2', mock_model2)

        items = register.items()
        # Convert to dict to easily check contents
        items_dict = dict(items)
        assert 'table1' in items_dict
        assert 'table2' in items_dict
        assert items_dict['table1'] == mock_model
        assert items_dict['table2'] == mock_model2

    def test_items_returns_empty_when_no_models_registered(self):
        """Test that items() returns empty view when no models are registered."""
        register = ModelRegister()
        items = register.items()
        assert len(dict(items)) == 0

    def test_get_model_with_only_prefixes(self, mock_model):
        """Test get_model works correctly when only prefixes are registered."""
        register = ModelRegister()
        register.register_prefix('pre_')
        register.register_model('pre_test_table', mock_model)
        result = register.get_model('test_table')
        assert result == mock_model

    def test_get_model_with_only_suffixes(self, mock_model):
        """Test get_model works correctly when only suffixes are registered."""
        register = ModelRegister()
        register.register_suffix('_suf')
        register.register_model('test_table_suf', mock_model)
        result = register.get_model('test_table')
        assert result == mock_model

    def test_clear_removes_all_models_prefixes_suffixes(self, mock_model):
        """Test that clear() removes all registered models, prefixes, and suffixes."""
        register = ModelRegister()
        register.register_model('test_table', mock_model)
        register.register_prefix('prefix_')
        register.register_suffix('_suffix')

        register.clear()

        assert register.models == {}
        assert register.model_names == {}
        assert register.prefixes == []
        assert register.suffixes == []

    def test_clear_with_existing_models_prefixes_suffixes(self, caplog, mock_model, mock_model2):
        """Test that clear() properly resets the registry state."""
        register = ModelRegister()
        register.register_model('table1', mock_model)
        register.register_model('table2', mock_model2)
        register.register_prefix('pre_')
        register.register_suffix('_suf')

        register.clear()

        # Verify all structures are cleared
        assert register.models == {}
        assert register.model_names == {}
        assert register.prefixes == []
        assert register.suffixes == []

        # Verify that trying to get a model after clear raises KeyError
        with pytest.raises(KeyError, match='not registered'):
            register.get_model('table1')

    def test_clear_after_multiple_operations(self, mock_model, mock_model2):
        """Test clear() works correctly after multiple registration operations."""
        register = ModelRegister()

        # Register some models with prefixes and suffixes
        register.register_prefix('app_')
        register.register_suffix('_table')
        register.register_model('app_test_table', mock_model)
        register.register_model('app_another_table', mock_model2)

        # Verify initial state
        assert len(register.models) == 2
        assert len(register.prefixes) == 1
        assert len(register.suffixes) == 1

        # Clear the registry
        register.clear()

        # Verify everything is cleared
        assert register.models == {}
        assert register.prefixes == []
        assert register.suffixes == []

        # Verify that get_model still raises KeyError after clearing
        with pytest.raises(KeyError):
            register.get_model('test')

    # def test_get_standard_tables(self):
    #     """Test retrieving standard tables."""
    #     from mafw.db.std_tables import StandardTable
    #     model_register = ModelRegister()
    #     mock_model = MagicMock(spec=StandardTable)
    #     mock_model.__name__ = 'StandardTable'
    #     model_register.register_model("standard_table", mock_model)
    #     standard_tables = model_register.get_standard_tables()
    #     assert standard_tables == [mock_model]

    def test_get_standard_tables(self):
        # Create a mock class that simulates inheritance from StandardTable
        from mafw.db.std_tables import StandardTable

        mock_standard_table = MagicMock(spec=StandardTable)
        mock_standard_table.__bases__ = (StandardTable,)
        mock_standard_table.__name__ = 'StandardTable'

        # Create a mock class that does not inherit from StandardTable
        mock_non_standard_table = MagicMock()
        mock_non_standard_table.__bases__ = (MAFwBaseModel,)
        mock_non_standard_table.__name__ = 'NonStandardTable'

        # Initialize the ModelRegister and register mock models
        register = ModelRegister()
        register.register_model('standard_table', mock_standard_table)
        register.register_model('non_standard_table', mock_non_standard_table)

        # Retrieve standard tables
        standard_tables = register.get_standard_tables()

        # Assert that only the mock_standard_table is returned
        assert standard_tables == [mock_standard_table]
