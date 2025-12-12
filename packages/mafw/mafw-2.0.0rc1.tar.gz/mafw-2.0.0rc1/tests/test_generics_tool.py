#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
from mafw.tools.generics import deep_update


class TestDeepUpdate:
    """Test cases for the deep_update function."""

    def test_basic_update_with_copy(self):
        """Test basic dictionary update with copy_first=True."""
        base_dict = {'a': 1, 'b': 2}
        update_dict = {'b': 3, 'c': 4}
        result = deep_update(base_dict, update_dict)

        assert result == {'a': 1, 'b': 3, 'c': 4}
        # Verify original dict is unchanged
        assert base_dict == {'a': 1, 'b': 2}

    def test_basic_update_without_copy(self):
        """Test basic dictionary update with copy_first=False."""
        base_dict = {'a': 1, 'b': 2}
        update_dict = {'b': 3, 'c': 4}
        result = deep_update(base_dict, update_dict, copy_first=False)

        assert result == {'a': 1, 'b': 3, 'c': 4}
        # Verify original dict is modified
        assert base_dict == {'a': 1, 'b': 3, 'c': 4}

    def test_nested_dict_update(self):
        """Test recursive update of nested dictionaries."""
        base_dict = {'a': 1, 'b': {'c': 2, 'd': 3}}
        update_dict = {'b': {'c': 5, 'e': 6}, 'f': 7}
        result = deep_update(base_dict, update_dict)

        assert result == {'a': 1, 'b': {'c': 5, 'd': 3, 'e': 6}, 'f': 7}
        # Verify original dict is unchanged
        assert base_dict == {'a': 1, 'b': {'c': 2, 'd': 3}}

    def test_nested_dict_update_no_copy(self):
        """Test recursive update of nested dictionaries with copy_first=False."""
        base_dict = {'a': 1, 'b': {'c': 2, 'd': 3}}
        update_dict = {'b': {'c': 5, 'e': 6}, 'f': 7}
        result = deep_update(base_dict, update_dict, copy_first=False)

        assert result == {'a': 1, 'b': {'c': 5, 'd': 3, 'e': 6}, 'f': 7}
        # Verify original dict is modified
        assert base_dict == {'a': 1, 'b': {'c': 5, 'd': 3, 'e': 6}, 'f': 7}

    def test_empty_dicts(self):
        """Test with empty dictionaries."""
        base_dict = {}
        update_dict = {}
        result = deep_update(base_dict, update_dict)

        assert result == {}
        assert base_dict == {}

    def test_update_dict_empty(self):
        """Test when update_dict is empty."""
        base_dict = {'a': 1, 'b': 2}
        update_dict = {}
        result = deep_update(base_dict, update_dict)

        assert result == {'a': 1, 'b': 2}
        assert base_dict == {'a': 1, 'b': 2}

    def test_base_dict_empty(self):
        """Test when base_dict is empty."""
        base_dict = {}
        update_dict = {'a': 1, 'b': 2}
        result = deep_update(base_dict, update_dict)

        assert result == {'a': 1, 'b': 2}
        assert base_dict == {}

    def test_deeply_nested_dicts(self):
        """Test deeply nested dictionary structures."""
        base_dict = {'a': 1, 'b': {'c': 2, 'd': {'e': 3, 'f': 4}}}
        update_dict = {'b': {'d': {'e': 5, 'g': 6}, 'h': 7}, 'i': 8}
        result = deep_update(base_dict, update_dict)

        expected = {'a': 1, 'b': {'c': 2, 'd': {'e': 5, 'f': 4, 'g': 6}, 'h': 7}, 'i': 8}
        assert result == expected
        assert base_dict == {'a': 1, 'b': {'c': 2, 'd': {'e': 3, 'f': 4}}}

    def test_mixed_types(self):
        """Test with mixed data types."""
        base_dict = {'string': 'hello', 'number': 42, 'list': [1, 2, 3], 'nested': {'inner': 'value'}}
        update_dict = {'string': 'world', 'number': 100, 'list': [4, 5], 'nested': {'inner': 'updated', 'new': 'field'}}
        result = deep_update(base_dict, update_dict)

        expected = {'string': 'world', 'number': 100, 'list': [4, 5], 'nested': {'inner': 'updated', 'new': 'field'}}
        assert result == expected
        assert base_dict == {'string': 'hello', 'number': 42, 'list': [1, 2, 3], 'nested': {'inner': 'value'}}

    def test_non_dict_values_override(self):
        """Test that non-dict values completely override existing ones."""
        base_dict = {'a': {'b': 1}, 'c': 2}
        update_dict = {'a': 3, 'c': {'d': 4}}
        result = deep_update(base_dict, update_dict)

        assert result == {'a': 3, 'c': {'d': 4}}
        assert base_dict == {'a': {'b': 1}, 'c': 2}

    def test_copy_first_false_modifies_original(self):
        """Test that copy_first=False modifies the original dictionary."""
        base_dict = {'a': 1, 'b': {'c': 2}}
        original_id = id(base_dict)
        update_dict = {'b': {'d': 3}}
        result = deep_update(base_dict, update_dict, copy_first=False)

        # Result should be the same object as base_dict
        assert id(result) == original_id
        assert base_dict == {'a': 1, 'b': {'c': 2, 'd': 3}}
        assert result == {'a': 1, 'b': {'c': 2, 'd': 3}}

    def test_deep_copy_preserves_structure(self):
        """Test that deep copy preserves the structure of nested objects."""
        base_dict = {'a': [1, 2, {'b': 3}], 'c': {'d': [4, 5]}}
        update_dict = {'a': [6, 7], 'c': {'d': [8, 9]}}
        result = deep_update(base_dict, update_dict)

        # Verify that nested lists and dicts are properly copied
        assert result == {'a': [6, 7], 'c': {'d': [8, 9]}}
        # Original should be unchanged
        assert base_dict == {'a': [1, 2, {'b': 3}], 'c': {'d': [4, 5]}}

    def test_complex_scenario(self):
        """Test a complex scenario with multiple operations."""
        base_dict = {
            'level1': {'level2': {'level3': {'key1': 'value1', 'key2': 'value2'}, 'key3': 'value3'}, 'key4': 'value4'},
            'top_level': 'top_value',
        }
        update_dict = {
            'level1': {
                'level2': {'level3': {'key1': 'new_value1', 'key5': 'value5'}, 'key6': 'value6'},
                'key7': 'value7',
            },
            'new_top': 'new_top_value',
        }
        result = deep_update(base_dict, update_dict)

        expected = {
            'level1': {
                'level2': {
                    'level3': {'key1': 'new_value1', 'key2': 'value2', 'key5': 'value5'},
                    'key3': 'value3',
                    'key6': 'value6',
                },
                'key4': 'value4',
                'key7': 'value7',
            },
            'top_level': 'top_value',
            'new_top': 'new_top_value',
        }
        assert result == expected
        assert base_dict == {
            'level1': {'level2': {'level3': {'key1': 'value1', 'key2': 'value2'}, 'key3': 'value3'}, 'key4': 'value4'},
            'top_level': 'top_value',
        }
