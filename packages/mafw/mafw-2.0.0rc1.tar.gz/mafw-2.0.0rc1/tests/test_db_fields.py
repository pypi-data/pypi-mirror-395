#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Unit tests for MAFw custom model fields.
"""

from pathlib import Path
from unittest.mock import patch

import pytest
from peewee import Model, SqliteDatabase

from mafw.db.fields import FileChecksumField, FileNameField, FileNameListField


class TestFileNameFieldAccessor:
    """Test cases for FileNameFieldAccessor functionality."""

    @pytest.fixture
    def mock_db(self):
        """Create test database."""
        return SqliteDatabase(':memory:')

    @pytest.fixture
    def model_with_checksum(self, mock_db):
        """Create model with filename field linked to checksum field."""

        class TestModel(Model):
            filename = FileNameField(checksum_field='checksum')
            checksum = FileChecksumField()

            class Meta:
                database = mock_db

        mock_db.create_tables([TestModel])
        return TestModel

    @pytest.fixture
    def model_without_checksum(self, mock_db):
        """Create model with filename field not linked to any checksum field."""

        class TestModel(Model):
            filename = FileNameField()

            class Meta:
                database = mock_db

        mock_db.create_tables([TestModel])
        return TestModel

    def test_filename_field_without_checksum_link(self, model_without_checksum):
        """Test FileNameField when no checksum field is linked."""
        instance = model_without_checksum()
        instance.filename = Path('test_file.txt')

        assert str(instance.filename) == 'test_file.txt'
        assert isinstance(instance.filename, Path)

    def test_filename_field_sets_checksum_when_not_initialized(self, model_with_checksum):
        """Test that setting filename automatically sets checksum when checksum not initialized."""
        instance = model_with_checksum()
        instance.filename = 'test_file.txt'

        assert str(instance.filename) == 'test_file.txt'
        assert instance.checksum == 'test_file.txt'
        assert hasattr(instance, 'init_checksum')
        assert getattr(instance, 'init_checksum') is False

    def test_filename_field_does_not_overwrite_initialized_checksum(self, model_with_checksum):
        """Test that setting filename does not overwrite manually set checksum."""
        instance = model_with_checksum()
        # First set checksum manually
        instance.checksum = 'manual_checksum_value'
        # Then set filename
        instance.filename = 'test_file.txt'

        assert str(instance.filename) == 'test_file.txt'
        assert instance.checksum == 'manual_checksum_value'  # Should not be overwritten
        assert getattr(instance, 'init_checksum') is True

    def test_multiple_filename_changes_with_uninitialized_checksum(self, model_with_checksum):
        """Test multiple filename changes when checksum remains uninitialized."""
        instance = model_with_checksum()

        instance.filename = 'first_file.txt'
        assert instance.checksum == 'first_file.txt'

        instance.filename = 'second_file.txt'
        assert instance.checksum == 'second_file.txt'

        assert getattr(instance, 'init_checksum') is False


class TestFileChecksumFieldAccessor:
    """Test cases for FileChecksumFieldAccessor functionality."""

    @pytest.fixture
    def mock_db(self):
        """Create test database."""
        return SqliteDatabase(':memory:')

    @pytest.fixture
    def model_with_checksum(self, mock_db):
        """Create model with checksum field."""

        class TestModel(Model):
            checksum = FileChecksumField()

            class Meta:
                database = mock_db

        mock_db.create_tables([TestModel])
        return TestModel

    def test_checksum_field_sets_init_flag_when_assigned(self, model_with_checksum):
        """Test that manually setting checksum field sets initialization flag."""
        instance = model_with_checksum()
        instance.checksum = 'manual_checksum'

        assert instance.checksum == 'manual_checksum'
        assert hasattr(instance, 'init_checksum')
        assert getattr(instance, 'init_checksum') is True

    def test_checksum_field_multiple_assignments(self, model_with_checksum):
        """Test multiple assignments to checksum field."""
        instance = model_with_checksum()

        instance.checksum = 'first_checksum'
        assert getattr(instance, 'init_checksum') is True

        instance.checksum = 'second_checksum'
        assert instance.checksum == 'second_checksum'
        assert getattr(instance, 'init_checksum') is True


class TestFileNameField:
    """Test cases for FileNameField class."""

    def test_init_without_checksum_field(self):
        """Test FileNameField initialization without checksum field."""
        field = FileNameField()
        assert field.checksum_field is None

    def test_init_with_checksum_field(self):
        """Test FileNameField initialization with checksum field."""
        field = FileNameField(checksum_field='my_checksum')
        assert field.checksum_field == 'my_checksum'

    def test_init_with_additional_args(self):
        """Test FileNameField initialization with additional TextField args."""
        field = FileNameField(checksum_field='my_checksum', null=True)
        assert field.checksum_field == 'my_checksum'

    @pytest.mark.parametrize(
        'input_value,expected',
        [
            ('test_file.txt', 'test_file.txt'),
            (Path('test_file.txt'), 'test_file.txt'),
            (Path('/absolute/path/file.txt'), '/absolute/path/file.txt'),
            ('', ''),
        ],
    )
    def test_db_value_conversion(self, input_value, expected):
        """Test db_value method converts various inputs to string."""
        field = FileNameField()
        result = field.db_value(input_value)
        assert result == expected
        assert isinstance(result, str)

    @pytest.mark.parametrize(
        'input_value',
        [
            'test_file.txt',
            '/absolute/path/file.txt',
            'relative/path/file.txt',
        ],
    )
    def test_python_value_conversion(self, input_value):
        """Test python_value method converts string to Path."""
        field = FileNameField()
        result = field.python_value(input_value)
        assert isinstance(result, Path)
        assert str(result) == input_value


class TestFileNameListField:
    """Test cases for FileNameListField class."""

    def test_inherits_from_filename_field(self):
        """Test that FileNameListField inherits from FileNameField."""
        field = FileNameListField()
        assert isinstance(field, FileNameField)

    @pytest.mark.parametrize(
        'input_value,expected',
        [
            # Single string
            ('single_file.txt', 'single_file.txt'),
            # Single Path
            (Path('single_file.txt'), 'single_file.txt'),
            # List of strings
            (['file1.txt', 'file2.txt'], 'file1.txt;file2.txt'),
            # List of Paths
            ([Path('file1.txt'), Path('file2.txt')], 'file1.txt;file2.txt'),
            # Mixed list
            (['file1.txt', Path('file2.txt')], 'file1.txt;file2.txt'),
            # Empty list
            ([], ''),
            # Single item list
            (['single.txt'], 'single.txt'),
        ],
    )
    def test_db_value_conversion(self, input_value, expected):
        """Test db_value method with various input types."""
        field = FileNameListField()
        result = field.db_value(input_value)
        assert result == expected
        assert isinstance(result, str)

    @pytest.mark.parametrize(
        'input_value,expected_count,expected_paths',
        [
            ('file1.txt;file2.txt', 2, ['file1.txt', 'file2.txt']),
            ('single_file.txt', 1, ['single_file.txt']),
            ('file1.txt;file2.txt;file3.txt', 3, ['file1.txt', 'file2.txt', 'file3.txt']),
            ('/abs/path1.txt;/abs/path2.txt', 2, ['/abs/path1.txt', '/abs/path2.txt']),
        ],
    )
    def test_python_value_conversion(self, input_value, expected_count, expected_paths):
        """Test python_value method converts string to list of Paths."""
        field = FileNameListField()
        result = field.python_value(input_value)

        assert isinstance(result, list)
        assert len(result) == expected_count

        for path, expected_path in zip(result, expected_paths):
            assert isinstance(path, Path)
            assert str(path) == expected_path


class TestFileChecksumField:
    """Test cases for FileChecksumField class."""

    @pytest.fixture
    def temp_file(self, tmp_path):
        """Create a temporary file for testing."""
        file_path = tmp_path / 'test_file.txt'
        file_path.write_text('test content')
        return file_path

    @pytest.fixture
    def temp_files(self, tmp_path):
        """Create multiple temporary files for testing."""
        file1 = tmp_path / 'file1.txt'
        file2 = tmp_path / 'file2.txt'
        file1.write_text('content1')
        file2.write_text('content2')
        return [file1, file2]

    def test_python_value_returns_string(self):
        """Test python_value method returns string unchanged."""
        field = FileChecksumField()
        test_value = 'test_checksum_123'
        result = field.python_value(test_value)
        assert result == test_value
        assert isinstance(result, str)

    @patch('mafw.tools.file_tools.file_checksum')
    def test_db_value_with_path_object(self, mock_checksum):
        """Test db_value method with Path object."""
        mock_checksum.return_value = 'computed_checksum_123'
        field = FileChecksumField()

        test_path = Path('test_file.txt')
        result = field.db_value(test_path)

        mock_checksum.assert_called_once_with(test_path)
        assert result == 'computed_checksum_123'

    @patch('mafw.tools.file_tools.file_checksum')
    def test_db_value_with_path_list(self, mock_checksum):
        """Test db_value method with list of paths."""
        mock_checksum.return_value = 'list_checksum_456'
        field = FileChecksumField()

        test_paths = [Path('file1.txt'), Path('file2.txt')]
        result = field.db_value(test_paths)

        mock_checksum.assert_called_once_with(test_paths)
        assert result == 'list_checksum_456'

    @patch('mafw.tools.file_tools.file_checksum')
    def test_db_value_with_existing_file_string(self, mock_checksum, temp_file):
        """Test db_value method with string path to existing file."""
        mock_checksum.return_value = 'file_checksum_789'
        field = FileChecksumField()

        result = field.db_value(str(temp_file))

        mock_checksum.assert_called_once_with(temp_file)
        assert result == 'file_checksum_789'

    @patch('mafw.tools.file_tools.file_checksum')
    def test_db_value_with_nonexistent_file_string(self, mock_checksum):
        """Test db_value method with string that's not a valid file path."""
        field = FileChecksumField()
        checksum_string = 'direct_checksum_abc123'

        result = field.db_value(checksum_string)

        # Should not call file_checksum since file doesn't exist
        mock_checksum.assert_not_called()
        assert result == checksum_string

    @patch('mafw.tools.file_tools.file_checksum')
    def test_db_value_with_mixed_string_path_list(self, mock_checksum):
        """Test db_value method with list containing both strings and Paths."""
        mock_checksum.return_value = 'mixed_list_checksum'
        field = FileChecksumField()

        test_paths = ['file1.txt', Path('file2.txt')]
        result = field.db_value(test_paths)

        mock_checksum.assert_called_once_with(test_paths)
        assert result == 'mixed_list_checksum'


@pytest.mark.integration_test
class TestIntegrationScenarios:
    """Integration tests for complete field functionality."""

    @pytest.fixture
    def mock_db(self):
        """Create test database."""
        return SqliteDatabase(':memory:')

    @pytest.fixture
    def complete_model(self, mock_db):
        """Create model with all field types."""

        class CompleteModel(Model):
            filename = FileNameField(checksum_field='checksum', null=True)
            filenames = FileNameListField(checksum_field='list_checksum', null=True)
            checksum = FileChecksumField(null=True)
            list_checksum = FileChecksumField(null=True)

            class Meta:
                database = mock_db

        mock_db.create_tables([CompleteModel])
        return CompleteModel

    def test_filename_to_checksum_linking(self, complete_model):
        """Test automatic linking between filename and checksum fields."""
        instance = complete_model()

        # Set filename - should automatically set checksum
        instance.filename = 'test_file.txt'
        assert instance.checksum == 'test_file.txt'

        # Manual checksum setting should prevent automatic updates
        instance.checksum = 'manual_checksum'
        instance.filename = 'new_file.txt'
        assert instance.checksum == 'manual_checksum'  # Should not change

    def test_filename_list_to_checksum_linking(self, complete_model):
        """Test automatic linking between filename list and checksum fields."""
        instance = complete_model()

        # Set filename list - should automatically set list_checksum
        instance.filenames = ['file1.txt', 'file2.txt']
        assert instance.list_checksum == ['file1.txt', 'file2.txt']

        # Manual list_checksum setting should prevent automatic updates
        instance.list_checksum = 'manual_list_checksum'
        instance.filenames = ['new1.txt', 'new2.txt']
        assert instance.list_checksum == 'manual_list_checksum'  # Should not change

    @patch('mafw.tools.file_tools.file_checksum')
    def test_checksum_field_with_real_file_calculation(self, mock_checksum, complete_model, tmp_path):
        """Test checksum field calculating real file checksums."""
        mock_checksum.return_value = 'real_file_checksum_123'

        # Create a real file
        test_file = tmp_path / 'real_test_file.txt'
        test_file.write_text('test content for checksum')

        instance = complete_model()
        instance.filename = test_file
        instance.save()

        mock_checksum.assert_called_once_with(test_file)
        assert instance.checksum == test_file
        assert complete_model.get(complete_model.filename == test_file).checksum == 'real_file_checksum_123'

    @patch('mafw.tools.file_tools.file_checksum')
    def test_database_persistence(self, mock_checksum, complete_model):
        """Test that field values persist correctly in database."""
        mock_checksum.side_effect = ['chk1', 'chk2+3']

        # Create and save instance
        instance = complete_model()
        instance.filename = Path('persistent_file.txt')
        instance.filenames = ['file1.txt', 'file2.txt']
        instance.save()

        # Retrieve from database
        retrieved = complete_model.get(complete_model.id == instance.id)

        assert str(retrieved.filename) == 'persistent_file.txt'
        assert isinstance(retrieved.filename, Path)
        assert len(retrieved.filenames) == 2
        assert all(isinstance(p, Path) for p in retrieved.filenames)
        assert str(retrieved.filenames[0]) == 'file1.txt'
        assert str(retrieved.filenames[1]) == 'file2.txt'
        assert retrieved.checksum == 'chk1'
        assert retrieved.list_checksum == 'chk2+3'
        mock_checksum.assert_any_call(instance.filename)
        mock_checksum.assert_called_with(instance.filenames)
