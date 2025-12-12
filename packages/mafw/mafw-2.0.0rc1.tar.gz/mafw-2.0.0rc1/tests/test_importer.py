#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Unit tests for the importer.py module.

This test suite provides comprehensive coverage for the FilenameElement, FilenameParser, and Importer classes,
aiming for at least 90% code coverage.
"""

import re
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from mafw.decorators import suppress_warnings
from mafw.mafw_errors import MissingAttribute, ParserConfigurationError, ParsingError
from mafw.processor_library.importer import FilenameElement, FilenameParser, Importer


class TestFilenameElement:
    """Test class for FilenameElement functionality."""

    def test_init_basic(self):
        """Test basic initialization of FilenameElement."""
        element = FilenameElement('test', r'(?P<test>\d+)', int, 42)
        assert element.name == 'test'
        assert element.value == 42
        assert element.is_optional is True
        assert element.is_found is True

    def test_init_without_default(self):
        """Test initialization without default value."""
        element = FilenameElement('name', r'(?P<name>\w+)')
        assert element.name == 'name'
        assert element.value is None
        assert element.is_optional is False
        assert element.is_found is False

    def test_init_with_compiled_regex(self):
        """Test initialization with pre-compiled regex."""
        compiled_regex = re.compile(r'(?P<version>\d+\.\d+)')
        element = FilenameElement('version', compiled_regex, str)
        assert element.pattern == r'(?P<version>\d+\.\d+)'

    def test_validate_regexp_missing_named_group(self):
        """Test validation fails when regex doesn't contain named group."""
        with pytest.raises(ValueError, match='regular expression without a named group'):
            FilenameElement('test', r'\d+')

    def test_validate_regexp_with_wrong_named_group(self):
        """Test validation fails when regex contain a named group different from the FilenameElement name."""
        with pytest.raises(ValueError, match='regular expression without a named group.'):
            FilenameElement('test', r'(?P<version>\d+\.\d+)')

    def test_validate_regexp_wrong_named_group(self):
        """Test validation fails when named group doesn't match element name."""
        with pytest.raises(ValueError, match='regular expression without a named group'):
            FilenameElement('test', r'(?P<wrong>\d+)')

    @pytest.mark.parametrize(
        'default_value,value_type,should_raise',
        [
            (42, int, False),
            ('hello', str, False),
            (3.14, float, False),
            (None, str, False),
            ('42', int, True),
            (42, str, True),
            (42.0, int, True),
        ],
    )
    def test_validate_default_type(self, default_value, value_type, should_raise):
        """Test default value type validation."""
        if should_raise:
            with pytest.raises(TypeError, match='type of the default value'):
                FilenameElement('test', r'(?P<test>\w+)', value_type, default_value)
        else:
            element = FilenameElement('test', r'(?P<test>\w+)', value_type, default_value)
            assert element._default_value == default_value

    @pytest.mark.parametrize(
        'type_string,expected_type',
        [
            ('str', str),
            ('int', int),
            ('float', float),
        ],
    )
    def test_get_value_type_valid(self, type_string, expected_type):
        """Test _get_value_type with valid type strings."""
        result = FilenameElement._get_value_type(type_string)
        assert result == expected_type

    def test_get_value_type_invalid(self):
        """Test _get_value_type with invalid type string."""
        with pytest.raises(ValueError, match='not available value type'):
            FilenameElement._get_value_type('invalid_type')

    def test_reset(self):
        """Test reset functionality."""
        element = FilenameElement('test', r'(?P<test>\d+)', int, 42)
        element._value = 100  # Simulate found value
        element.reset()
        assert element.value == 42

    def test_from_dict_basic(self):
        """Test creating FilenameElement from dictionary."""
        info_dict = {'regexp': r'(?P<id>\d+)', 'type': 'int', 'default': 0}
        element = FilenameElement.from_dict('id', info_dict)
        assert element.name == 'id'
        assert element._value_type is int
        assert element._default_value == 0

    def test_from_dict_minimal(self):
        """Test creating FilenameElement from minimal dictionary."""
        info_dict = {'regexp': r'(?P<name>\w+)'}
        element = FilenameElement.from_dict('name', info_dict)
        assert element.name == 'name'
        assert element._value_type is str
        assert element._default_value is None

    def test_from_dict_missing_regexp(self):
        """Test from_dict raises KeyError when regexp is missing."""
        info_dict = {'type': 'str'}
        with pytest.raises(KeyError):
            FilenameElement.from_dict('test', info_dict)

    def test_from_dict_invalid_regexp_type(self):
        """Test from_dict raises TypeError for invalid regexp type."""
        info_dict = {'regexp': 123}
        with pytest.raises(TypeError, match='Problem with regexp'):
            FilenameElement.from_dict('test', info_dict)

    def test_from_dict_invalid_value_type(self):
        """Test from_dict raises ValueError for invalid value type."""
        info_dict = {
            'regexp': r'(?P<test>\w+)',
            'type': 123,  # Should be string
        }
        with pytest.raises(ValueError, match='wrong value type'):
            FilenameElement.from_dict('test', info_dict)

    @pytest.mark.parametrize(
        'name, search_string,pattern,expected_value,value_type',
        [
            ('number', 'file_123.txt', r'(?P<number>\d+)', 123, int),
            ('value', 'data_3.14_result.csv', r'(?P<value>\d+\.\d+)', 3.14, float),
            ('name', 'experiment_alpha.log', r'experiment_(?P<name>\w+)', 'alpha', str),
            ('missing', 'test_file.txt', r'(?P<missing>\d+)', None, int),  # Pattern not found
        ],
    )
    def test_search(self, name, search_string, pattern, expected_value, value_type):
        """Test search functionality with various patterns."""
        element = FilenameElement(name, pattern, value_type)
        element.search(search_string)
        assert element.value == expected_value

    def test_search_with_path(self):
        """Test search functionality with Path object."""
        element = FilenameElement('id', r'(?P<id>\d+)', int)
        path = Path('file_456.txt')
        element.search(path)
        assert element.value == 456

    def test_search_resets_value(self):
        """Test that search resets value before searching."""
        element = FilenameElement('test', r'(?P<test>\d+)', int, 0)
        element._value = 999  # Set some value
        element.search('no_match.txt')  # Search with no match
        assert element.value == 0  # Should reset to default

    def test_properties(self):
        """Test all properties of FilenameElement."""
        element = FilenameElement('test', r'(?P<test>\d+)', int, 42)
        assert element.name == 'test'
        assert element.value == 42
        assert element.is_optional is True
        assert element.is_found is True
        assert element.pattern == r'(?P<test>\d+)'


class TestFilenameParser:
    """Test class for FilenameParser functionality."""

    @pytest.fixture
    def sample_config_file(self):
        """Create a temporary TOML configuration file for testing."""
        config_content = r"""
elements = ["id", "version", "optional_param"]

[id]
regexp = "(?P<id>\\d+)"
type = "int"

[version]
regexp = "version_(?P<version>\\d+\\.\\d+)"
type = "float"

[optional_param]
regexp = "param_(?P<optional_param>\\w+)"
type = "str"
default = "default_value"
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
            f.write(config_content)
            f.flush()
            yield f.name
        Path(f.name).unlink()  # Clean up

    @pytest.fixture
    def invalid_config_file(self):
        """Create an invalid TOML configuration file for testing."""
        config_content = r"""
elements = ["missing_element"]

[existing_element]
regexp = "(?P<existing_element>\\w+)"
type = "str"
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
            f.write(config_content)
            f.flush()
            yield f.name
        Path(f.name).unlink()

    def test_init_with_filename(self, sample_config_file):
        """Test initialization with filename provided."""
        parser = FilenameParser(sample_config_file, 'test_file.txt')
        assert parser._filename == 'test_file.txt'
        assert len(parser.elements) == 3

    def test_init_without_filename(self, sample_config_file):
        """Test initialization without filename."""
        parser = FilenameParser(sample_config_file)
        assert parser._filename is None
        assert len(parser.elements) == 3

    def test_parser_configuration_invalid_file(self, invalid_config_file):
        """Test parser configuration with invalid file raises error."""
        with pytest.raises(ParserConfigurationError, match='Missing missing_element table'):
            FilenameParser(invalid_config_file)

    def test_elements_property(self, sample_config_file):
        """Test elements property returns correct dictionary."""
        parser = FilenameParser(sample_config_file)
        elements = parser.elements
        assert 'id' in elements
        assert 'version' in elements
        assert 'optional_param' in elements
        assert isinstance(elements['id'], FilenameElement)

    def test_interpret_with_constructor_filename(self, sample_config_file):
        """Test interpret using filename from constructor."""
        filename = 'file_123_version_2.5_param_test.txt'
        parser = FilenameParser(sample_config_file, filename)
        parser.interpret()

        assert parser.get_element_value('id') == 123
        assert parser.get_element_value('version') == 2.5
        assert parser.get_element_value('optional_param') == 'test'

    def test_interpret_with_method_filename(self, sample_config_file):
        """Test interpret using filename passed to method."""
        filename = 'data_456_version_1.0_param_special.log'
        parser = FilenameParser(sample_config_file)
        parser.interpret(filename)

        assert parser.get_element_value('id') == 456
        assert parser.get_element_value('version') == 1.0
        assert parser.get_element_value('optional_param') == 'special'

    def test_interpret_method_filename_precedence(self, sample_config_file):
        """Test that method filename takes precedence over constructor filename."""
        parser = FilenameParser(sample_config_file, 'old_file.txt')
        new_filename = 'new_789_version_3.0_updated.txt'
        parser.interpret(new_filename)

        assert parser._filename == new_filename
        assert parser.get_element_value('id') == 789

    def test_interpret_no_filename(self, sample_config_file):
        """Test interpret raises error when no filename is provided."""
        parser = FilenameParser(sample_config_file)
        with pytest.raises(MissingAttribute, match='Missing filename'):
            parser.interpret()

    def test_interpret_missing_compulsory_element(self, sample_config_file):
        """Test interpret raises ParsingError for missing compulsory element."""
        filename = 'file_without_id_version_new.txt'  # Missing id
        parser = FilenameParser(sample_config_file)
        with pytest.raises(ParsingError, match='Missing id'):
            parser.interpret(filename)

    def test_interpret_with_path_object(self, sample_config_file):
        """Test interpret with Path object."""
        filename = Path('analysis_999_version_4.2_final.dat')
        parser = FilenameParser(sample_config_file)
        parser.interpret(filename)

        assert parser.get_element_value('id') == 999
        assert parser.get_element_value('version') == 4.2

    def test_interpret_optional_element_missing(self, sample_config_file):
        """Test interpret succeeds when optional element is missing."""
        filename = 'experiment_777_version_5.1.txt'  # Missing optional_param
        parser = FilenameParser(sample_config_file)
        parser.interpret(filename)

        assert parser.get_element_value('id') == 777
        assert parser.get_element_value('version') == 5.1
        assert parser.get_element_value('optional_param') == 'default_value'

    def test_get_element_existing(self, sample_config_file):
        """Test get_element returns correct element."""
        parser = FilenameParser(sample_config_file)
        element = parser.get_element('id')
        assert element is not None
        assert element.name == 'id'

    def test_get_element_non_existing(self, sample_config_file):
        """Test get_element returns None for non-existing element."""
        parser = FilenameParser(sample_config_file)
        element = parser.get_element('non_existing')
        assert element is None

    def test_get_element_value_existing(self, sample_config_file):
        """Test get_element_value returns correct value."""
        filename = 'test_888_version_6.0_param_custom.txt'
        parser = FilenameParser(sample_config_file)
        parser.interpret(filename)

        assert parser.get_element_value('id') == 888
        assert parser.get_element_value('version') == 6.0
        assert parser.get_element_value('optional_param') == 'custom'

    def test_get_element_value_non_existing(self, sample_config_file):
        """Test get_element_value returns None for non-existing element."""
        parser = FilenameParser(sample_config_file)
        value = parser.get_element_value('non_existing')
        assert value is None

    def test_reset(self, sample_config_file):
        """Test reset functionality."""
        filename = 'file_111_version_1.1_test.txt'
        parser = FilenameParser(sample_config_file)
        parser.interpret(filename)

        # Verify values are set
        assert parser.get_element_value('id') == 111

        # Reset and verify values are back to defaults
        parser.reset()
        assert parser.get_element_value('id') is None  # No default for id
        assert parser.get_element_value('optional_param') == 'default_value'  # Has default


class TestImporter:
    """Test class for Importer functionality."""

    @pytest.fixture
    def mock_processor_base(self):
        """Mock the Processor base class."""
        with patch('mafw.processor.Processor') as mock:
            yield mock

    @pytest.fixture
    @suppress_warnings
    def sample_importer(self):
        """Create a sample Importer instance for testing."""
        return Importer()

    def test_init(self, sample_importer):
        """Test Importer initialization."""
        assert hasattr(sample_importer, 'parser_configuration')
        assert hasattr(sample_importer, 'input_folder')
        assert hasattr(sample_importer, 'recursive')

    @pytest.mark.order(0)
    def test_active_parameters(self, sample_importer):
        """Test ActiveParameter definitions."""
        assert sample_importer.get_parameter('parser_configuration').name == 'parser_configuration'
        assert sample_importer.get_parameter('parser_configuration').value == 'parser_configuration.toml'

        assert sample_importer.get_parameter('input_folder').name == 'input_folder'
        assert sample_importer.get_parameter('input_folder').value == str(Path.cwd())

        assert sample_importer.get_parameter('recursive').name == 'recursive'
        assert sample_importer.get_parameter('recursive').value is True

    @patch('mafw.processor_library.importer.FilenameParser')
    def test_start_method(self, mock_filename_parser, sample_importer):
        """Test start method creates FilenameParser."""

        sample_importer.parser_configuration = 'test_config.toml'
        sample_importer.start()

        # Verify FilenameParser was created
        mock_filename_parser.assert_called_once_with('test_config.toml')

    def test_format_progress_message(self, sample_importer):
        """Test format_progress_message method."""
        sample_importer.i_item = 5
        sample_importer.n_item = 10
        sample_importer.format_progress_message()

        expected_message = '[cyan]Importing element 6 of 10'
        assert sample_importer.progress_message == expected_message

    def test_format_progress_message_zero_indexed(self, sample_importer):
        """Test format_progress_message with zero-based indexing."""
        sample_importer.i_item = 0
        sample_importer.n_item = 5
        sample_importer.format_progress_message()

        expected_message = '[cyan]Importing element 1 of 5'
        assert sample_importer.progress_message == expected_message


@pytest.mark.integration_test
class TestIntegration:
    """Integration tests combining multiple components."""

    @pytest.fixture
    def complete_config_file(self):
        """Create a complete TOML configuration file for integration testing."""
        config_content = r"""
elements = ["experiment_id", "sample_type", "temperature", "batch"]

[experiment_id]
regexp = "exp_(?P<experiment_id>\\d+)"
type = "int"

[sample_type]
regexp = "type_(?P<sample_type>[a-zA-Z0-9]+)"
type = "str"

[temperature]
regexp = "temp_(?P<temperature>\\d+\\.\\d+)C"
type = "float"

[batch]
regexp = "batch_(?P<batch>\\w+)"
type = "str"
default = "unknown"
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
            f.write(config_content)
            f.flush()
            yield f.name
        Path(f.name).unlink()

    @pytest.mark.parametrize(
        'filename,expected_values',
        [
            (
                'exp_001_type_control_temp_25.5C_batch_A.dat',
                {'experiment_id': 1, 'sample_type': 'control', 'temperature': 25.5, 'batch': 'A'},
            ),
            (
                'exp_042_type_treatment_temp_37.0C_batch_B.txt',
                {'experiment_id': 42, 'sample_type': 'treatment', 'temperature': 37.0, 'batch': 'B'},
            ),
            (
                'exp_999_type_blank_temp_4.0C.log',  # Missing batch (should use default)
                {'experiment_id': 999, 'sample_type': 'blank', 'temperature': 4.0, 'batch': 'unknown'},
            ),
        ],
    )
    def test_complete_filename_parsing(self, complete_config_file, filename, expected_values):
        """Test complete filename parsing workflow."""
        parser = FilenameParser(complete_config_file)
        parser.interpret(filename)

        for element_name, expected_value in expected_values.items():
            actual_value = parser.get_element_value(element_name)
            assert actual_value == expected_value, (
                f'Mismatch for {element_name}: expected {expected_value}, got {actual_value}'
            )

    def test_filename_element_lifecycle(self):
        """Test complete lifecycle of FilenameElement."""
        # Create element
        element = FilenameElement('test_id', r'id_(?P<test_id>\d+)', int, 0)

        # Initial state
        assert element.value == 0
        assert element.is_optional is True
        assert element.is_found is True

        # Search for pattern
        element.search('file_id_123_data.txt')
        assert element.value == 123
        assert element.is_found is True

        # Reset
        element.reset()
        assert element.value == 0

        # Search without match
        element.search('file_without_id.txt')
        assert element.value == 0  # Should keep default value

    def test_error_handling_chain(self, complete_config_file):
        """Test error handling across the entire chain."""
        parser = FilenameParser(complete_config_file)

        # Test missing compulsory element
        with pytest.raises(ParsingError, match='Missing experiment_id'):
            parser.interpret('type_control_temp_25.0C.dat')  # Missing exp_

        # Test successful parsing after error
        parser.interpret('exp_123_type_test_temp_20.0C.dat')
        assert parser.get_element_value('experiment_id') == 123


# Additional edge cases and error conditions
class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_filename_element_empty_string_search(self):
        """Test FilenameElement search with empty string."""
        element = FilenameElement('test', r'(?P<test>\w+)', str, 'default')
        element.search('')
        assert element.value == 'default'

    def test_filename_element_special_characters(self):
        """Test FilenameElement with special characters in pattern."""
        element = FilenameElement('special', r'file\.(?P<special>\w+)\.txt', str)
        element.search('file.test.txt')
        assert element.value == 'test'

    def test_filename_parser_with_overlapping_patterns(self):
        """Test FilenameParser with potentially overlapping patterns."""
        config_content = r"""
elements = ["first", "second"]

[first]
regexp = "(?P<first>\\d+)"
type = "int"

[second]
regexp = "data_(?P<second>\\d+)"
type = "int"
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.toml', delete=False) as f:
            f.write(config_content)
            f.flush()

            try:
                parser = FilenameParser(f.name)
                parser.interpret('data_123_456.txt')

                # Both patterns should match their respective parts
                assert parser.get_element_value('first') in [123, 456]  # Could match either number
                assert parser.get_element_value('second') == 123  # Should match the one after "data_"
            finally:
                Path(f.name).unlink()

    def test_type_conversion_edge_cases(self):
        """Test type conversion edge cases."""
        # Test float that looks like int
        element = FilenameElement('value', r'(?P<value>\d+\.0)', float)
        element.search('test_5.0_file.txt')
        assert element.value == 5.0
        assert isinstance(element.value, float)

        # Test int conversion
        element = FilenameElement('count', r'(?P<count>\d+)', int)
        element.search('count_007_file.txt')
        assert element.value == 7
        assert isinstance(element.value, int)
