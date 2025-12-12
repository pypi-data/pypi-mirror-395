#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
from unittest.mock import Mock, patch

import pytest
from peewee import CompositeKey, Field, fn

from mafw.db.db_model import MAFwBaseModel
from mafw.tools.db_tools import combine_fields, combine_pk, get_pk, make_kv


class TestMakeKv:
    """Test cases for make_kv function."""

    def test_basic_functionality(self):
        """Test basic key-value mapping functionality."""
        # Setup mock model and fields
        mock_model = Mock()
        mock_key_field = Mock(name='key_field')
        mock_value_field = Mock(name='value_field')
        mock_key_field.name = 'key'
        mock_value_field.name = 'value'

        # Setup mock rows
        mock_row1 = Mock()
        mock_row1.key = 'key1'
        mock_row1.value = 'value1'

        mock_row2 = Mock()
        mock_row2.key = 'key2'
        mock_row2.value = 'value2'

        # Make sure select returns an iterable
        mock_model.select.return_value = [mock_row1, mock_row2]

        # Call function
        result = make_kv(mock_model, mock_key_field, mock_value_field)

        # Verify results
        assert result == {'key1': 'value1', 'key2': 'value2'}
        mock_model.select.assert_called_once_with(mock_key_field, mock_value_field)

    def test_empty_result(self):
        """Test behavior with empty query results."""
        mock_model = Mock()
        mock_key_field = Mock(name='key_field')
        mock_value_field = Mock(name='value_field')
        mock_key_field.name = 'key'
        mock_value_field.name = 'value'

        # Make sure select returns an iterable
        mock_model.select.return_value = []

        result = make_kv(mock_model, mock_key_field, mock_value_field)

        assert result == {}
        mock_model.select.assert_called_once_with(mock_key_field, mock_value_field)

    def test_single_row(self):
        """Test behavior with single row result."""
        mock_model = Mock()
        mock_key_field = Mock(name='key_field')
        mock_value_field = Mock(name='value_field')
        mock_key_field.name = 'key'
        mock_value_field.name = 'value'

        mock_row = Mock()
        mock_row.key = 'single_key'
        mock_row.value = 'single_value'

        # Make sure select returns an iterable
        mock_model.select.return_value = [mock_row]

        result = make_kv(mock_model, mock_key_field, mock_value_field)

        assert result == {'single_key': 'single_value'}
        mock_model.select.assert_called_once_with(mock_key_field, mock_value_field)

    def test_duplicate_keys_behavior(self):
        """Test behavior when there are duplicate keys (last one wins)."""
        mock_model = Mock()
        mock_key_field = Mock(name='key_field')
        mock_value_field = Mock(name='value_field')
        mock_key_field.name = 'key'
        mock_value_field.name = 'value'

        # Two rows with same key but different values
        mock_row1 = Mock()
        mock_row1.key = 'duplicate_key'
        mock_row1.value = 'first_value'

        mock_row2 = Mock()
        mock_row2.key = 'duplicate_key'
        mock_row2.value = 'second_value'

        # Make sure select returns an iterable
        mock_model.select.return_value = [mock_row1, mock_row2]

        result = make_kv(mock_model, mock_key_field, mock_value_field)

        # Last value should win
        assert result == {'duplicate_key': 'second_value'}
        mock_model.select.assert_called_once_with(mock_key_field, mock_value_field)

    def test_different_data_types(self):
        """Test with different data types for keys and values."""
        mock_model = Mock()
        mock_key_field = Mock(name='key_field')
        mock_value_field = Mock(name='value_field')
        mock_key_field.name = 'key'
        mock_value_field.name = 'value'

        mock_row = Mock()
        mock_row.key = 123
        mock_row.value = [1, 2, 3]

        # Make sure select returns an iterable
        mock_model.select.return_value = [mock_row]

        result = make_kv(mock_model, mock_key_field, mock_value_field)

        assert result == {123: [1, 2, 3]}
        mock_model.select.assert_called_once_with(mock_key_field, mock_value_field)

    def test_invalid_model_type(self):
        """Test behavior with invalid model parameter."""
        mock_key_field = Mock(name='key_field')
        mock_value_field = Mock(name='value_field')
        mock_key_field.name = 'key'
        mock_value_field.name = 'value'

        # Test with non-model object
        with pytest.raises(AttributeError):
            make_kv('not_a_model', mock_key_field, mock_value_field)

    def test_invalid_field_types(self):
        """Test behavior with invalid field parameters."""
        mock_model = Mock()
        mock_model.select.return_value = [Mock()]
        mock_key_field = 'not_a_field'
        mock_value_field = Mock(name='value_field')
        mock_value_field.name = 'value'

        with pytest.raises(AttributeError):
            make_kv(mock_model, mock_key_field, mock_value_field)

    def test_make_kv_success(self):
        """Test successful execution of make_kv function."""
        # Create mock fields
        mock_key_field = Mock(name='key_field')
        mock_value_field = Mock(name='value_field')
        mock_key_field.name = 'key'
        mock_value_field.name = 'value'

        # Create mock row
        mock_row = Mock()
        mock_row.key = 'test_key'
        mock_row.value = 'test_value'

        # Mock the select method to return our mock row
        with patch.object(MAFwBaseModel, 'select') as mock_select:
            mock_select.return_value = [mock_row]

            # Test the function
            result = make_kv(MAFwBaseModel, mock_key_field, mock_value_field)

            # Verify results
            assert result == {'test_key': 'test_value'}
            mock_select.assert_called_once_with(mock_key_field, mock_value_field)


class TestGetPk:
    """Test cases for get_pk function."""

    def test_simple_primary_key(self):
        """Test get_pk with a simple primary key."""
        # Create a mock model with a simple primary key
        mock_field = Mock(spec=Field)
        mock_field.name = 'id'

        mock_meta = Mock()
        mock_meta.primary_key = mock_field
        mock_meta.fields = {'id': mock_field}

        mock_model = Mock()
        mock_model._meta = mock_meta

        result = get_pk(mock_model)
        assert result == [mock_field]

    def test_composite_primary_key(self):
        """Test get_pk with a composite primary key."""
        # Create mock fields for composite key
        field1 = Mock(spec=Field)
        field1.name = 'field1'
        field2 = Mock(spec=Field)
        field2.name = 'field2'

        # Create composite key
        composite_key = Mock(spec=CompositeKey)
        composite_key.field_names = ['field1', 'field2']

        mock_meta = Mock()
        mock_meta.primary_key = composite_key
        mock_meta.fields = {'field1': field1, 'field2': field2}

        mock_model = Mock()
        mock_model._meta = mock_meta

        result = get_pk(mock_model)
        assert result == [field1, field2]

    def test_model_with_non_field_primary_key(self):
        """Test get_pk with a non-field primary key."""
        mock_meta = Mock()
        mock_meta.primary_key = 'not_a_field'
        mock_meta.fields = {}

        mock_model = Mock()
        mock_model._meta = mock_meta

        # Should work with non-field primary key
        result = get_pk(mock_model)
        assert result == ['not_a_field']

    def test_multiple_fields_in_composite_key(self):
        """Test get_pk with multiple fields in composite key."""
        field1 = Mock(spec=Field)
        field1.name = 'field1'
        field2 = Mock(spec=Field)
        field2.name = 'field2'
        field3 = Mock(spec=Field)
        field3.name = 'field3'

        composite_key = Mock(spec=CompositeKey)
        composite_key.field_names = ['field1', 'field2', 'field3']

        mock_meta = Mock()
        mock_meta.primary_key = composite_key
        mock_meta.fields = {'field1': field1, 'field2': field2, 'field3': field3}

        mock_model = Mock()
        mock_model._meta = mock_meta

        result = get_pk(mock_model)
        assert result == [field1, field2, field3]

    def test_class_vs_instance_model(self):
        """Test get_pk works with both class and instance models."""
        # Test with class
        mock_field = Mock(spec=Field)
        mock_field.name = 'id'

        mock_meta = Mock()
        mock_meta.primary_key = mock_field
        mock_meta.fields = {'id': mock_field}

        mock_model_class = Mock()
        mock_model_class._meta = mock_meta

        result_class = get_pk(mock_model_class)
        assert result_class == [mock_field]

        # Test with instance
        mock_model_instance = Mock()
        mock_model_instance._meta = mock_meta

        result_instance = get_pk(mock_model_instance)
        assert result_instance == [mock_field]


class TestCombineFields:
    """Test the combine_fields function."""

    def test_combine_fields_single_field(self):
        """Test combining a single field."""
        field = Mock(spec=Field)
        field.name = 'field1'

        result = combine_fields([field])
        expected = fn.CONCAT(field)
        assert result == expected

    def test_combine_fields_multiple_fields(self):
        """Test combining multiple fields with the default separator."""
        field1 = Mock(spec=Field)
        field1.name = 'field1'
        field2 = Mock(spec=Field)
        field2.name = 'field2'
        field3 = Mock(spec=Field)
        field3.name = 'field3'

        result = combine_fields([field1, field2, field3])
        expected = fn.CONCAT(field1, ' x ', field2, ' x ', field3)
        assert result == expected

    def test_combine_fields_custom_separator(self):
        """Test combining fields with custom separator."""
        field1 = Mock(spec=Field)
        field1.name = 'field1'
        field2 = Mock(spec=Field)
        field2.name = 'field2'

        result = combine_fields([field1, field2], join_str=' - ')
        expected = fn.CONCAT(field1, ' - ', field2)
        assert result == expected

    def test_combine_fields_empty_list(self):
        """Test combining empty list of fields."""
        result = combine_fields([])
        expected = fn.CONCAT()
        assert result == expected


class TestCombinePk:
    """Test the combine_pk function which combines primary key fields."""

    def test_single_primary_key_with_default_alias(self):
        """Test combine_pk with single primary key and default alias."""
        # Mock a model with single primary key
        mock_model = Mock()
        mock_model._meta = Mock()
        mock_model._meta.primary_key = Mock()
        mock_model._meta.primary_key.name = 'id'

        # Mock the fields dictionary
        mock_field = Mock()
        mock_field.name = 'id'
        mock_model._meta.fields = {'id': mock_field}

        # Mock get_pk to return our mock field
        with patch('mafw.tools.db_tools.get_pk', return_value=[mock_field]) as mock_get_pk:
            # Mock the alias method on the field to return an Alias-like object
            with patch.object(mock_field, 'alias') as mock_alias:
                # Create a mock that behaves like an Alias object
                mock_alias_result = Mock()
                mock_alias_result._alias = 'combo_pk'
                mock_alias.return_value = mock_alias_result

                result = combine_pk(mock_model)

                # Verify that get_pk was called with the model
                mock_get_pk.assert_called_once_with(mock_model)
                # Verify that alias was called with the correct argument
                mock_alias.assert_called_once_with('combo_pk')

                # Verify the result has the expected alias
                assert result._alias == 'combo_pk'

    def test_single_primary_key_with_custom_alias(self):
        """Test combine_pk with single primary key and custom alias."""
        # Mock a model with single primary key
        mock_model = Mock()
        mock_model._meta = Mock()
        mock_model._meta.primary_key = Mock()
        mock_model._meta.primary_key.name = 'id'

        # Mock the fields dictionary
        mock_field = Mock()
        mock_field.name = 'id'
        mock_model._meta.fields = {'id': mock_field}

        # Mock get_pk to return our mock field
        with patch('mafw.tools.db_tools.get_pk', return_value=[mock_field]) as mock_get_pk:
            # Mock the alias method on the field to return an Alias-like object
            with patch.object(mock_field, 'alias') as mock_alias:
                # Create a mock that behaves like an Alias object
                mock_alias_result = Mock()
                mock_alias_result._alias = 'custom_alias'
                mock_alias.return_value = mock_alias_result

                result = combine_pk(mock_model, alias_name='custom_alias')

                # Verify that get_pk was called with the model
                mock_get_pk.assert_called_once_with(mock_model)
                # Verify that alias was called with the correct argument
                mock_alias.assert_called_once_with('custom_alias')

                # Verify the result has the expected alias
                assert result._alias == 'custom_alias'

    def test_composite_primary_key(self):
        """Test combine_pk with composite primary key."""
        # Mock a model with composite primary key
        mock_model = Mock()
        mock_model._meta = Mock()
        mock_model._meta.primary_key = Mock()
        mock_model._meta.primary_key.__class__ = CompositeKey
        mock_model._meta.primary_key.field_names = ['field1', 'field2']

        # Mock the fields dictionary
        mock_field1 = Mock()
        mock_field1.name = 'field1'
        mock_field2 = Mock()
        mock_field2.name = 'field2'
        mock_model._meta.fields = {'field1': mock_field1, 'field2': mock_field2}

        # Mock get_pk to return our mock fields
        with patch('mafw.tools.db_tools.get_pk', return_value=[mock_field1, mock_field2]) as mock_get_pk:
            # Mock combine_fields to return a specific result
            with patch('mafw.tools.db_tools.combine_fields') as mock_combine:
                # Create a mock that behaves like a combined field
                mock_combined_field = Mock()
                mock_combined_field.alias.return_value = Mock(_alias='combo_pk')
                mock_combine.return_value = mock_combined_field

                result = combine_pk(mock_model)

                # Verify that get_pk was called with the model
                mock_get_pk.assert_called_once_with(mock_model)
                # Verify that combine_fields was called with the right arguments
                mock_combine.assert_called_once_with([mock_field1, mock_field2], ' x ')

                # Verify the result has the expected alias
                assert result._alias == 'combo_pk'

    def test_composite_primary_key_with_custom_join_string(self):
        """Test combine_pk with composite primary key and custom join string."""
        # Mock a model with composite primary key
        mock_model = Mock()
        mock_model._meta = Mock()
        mock_model._meta.primary_key = Mock()
        mock_model._meta.primary_key.__class__ = CompositeKey
        mock_model._meta.primary_key.field_names = ['field1', 'field2']

        # Mock the fields dictionary
        mock_field1 = Mock()
        mock_field1.name = 'field1'
        mock_field2 = Mock()
        mock_field2.name = 'field2'
        mock_model._meta.fields = {'field1': mock_field1, 'field2': mock_field2}

        # Mock get_pk to return our mock fields
        with patch('mafw.tools.db_tools.get_pk', return_value=[mock_field1, mock_field2]) as mock_get_pk:
            # Mock combine_fields to return a specific result
            with patch('mafw.tools.db_tools.combine_fields') as mock_combine:
                # Create a mock that behaves like a combined field
                mock_combined_field = Mock()
                mock_combined_field.alias.return_value = Mock(_alias='combo_pk')
                mock_combine.return_value = mock_combined_field

                result = combine_pk(mock_model, join_str='|')

                # Verify that get_pk was called with the model
                mock_get_pk.assert_called_once_with(mock_model)
                # Verify that combine_fields was called with the right arguments
                mock_combine.assert_called_once_with([mock_field1, mock_field2], '|')

                # Verify the result has the expected alias
                assert result._alias == 'combo_pk'
