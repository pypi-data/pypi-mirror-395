#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""Unit tests for file_tools module."""

import hashlib
from pathlib import Path
from unittest.mock import MagicMock, Mock, mock_open, patch

import pytest
from peewee import Model

from mafw.db.fields import FileChecksumField, FileNameField, FileNameListField
from mafw.mafw_errors import ModelError
from mafw.tools.file_tools import file_checksum, remove_widow_db_rows, verify_checksum


class TestFileChecksum:
    """Test cases for file_checksum function."""

    @pytest.fixture
    def sample_file_content(self):
        """Sample file content for testing."""
        return b'Hello, World! This is test content.'

    @pytest.fixture
    def expected_checksum(self, sample_file_content):
        """Expected SHA256 checksum for sample content."""
        return hashlib.sha256(sample_file_content).hexdigest()

    def test_file_checksum_single_string_filename(self, sample_file_content, expected_checksum):
        """Test checksum calculation for a single string filename."""
        with patch('builtins.open', mock_open(read_data=sample_file_content)):
            result = file_checksum('test_file.txt')
            assert result == expected_checksum

    def test_file_checksum_single_path_filename(self, sample_file_content, expected_checksum):
        """Test checksum calculation for a single Path filename."""
        with patch('builtins.open', mock_open(read_data=sample_file_content)):
            result = file_checksum(Path('test_file.txt'))
            assert result == expected_checksum

    def test_file_checksum_multiple_files(self, sample_file_content):
        """Test checksum calculation for multiple files."""
        # Create combined content for multiple files
        combined_content = sample_file_content + sample_file_content
        expected_checksum = hashlib.sha256(combined_content).hexdigest()

        with patch('builtins.open', mock_open(read_data=sample_file_content)):
            result = file_checksum(['file1.txt', 'file2.txt'])
            assert result == expected_checksum

    def test_file_checksum_mixed_types_list(self, sample_file_content, expected_checksum):
        """Test checksum calculation for mixed string and Path types."""
        with patch('builtins.open', mock_open(read_data=sample_file_content)):
            result = file_checksum([Path('file1.txt'), 'file2.txt'])
            # Should process both files with same content
            combined_content = sample_file_content + sample_file_content
            expected = hashlib.sha256(combined_content).hexdigest()
            assert result == expected

    @pytest.mark.parametrize('buf_size', [1024, 8192, 65536])
    def test_file_checksum_different_buffer_sizes(self, sample_file_content, expected_checksum, buf_size):
        """Test checksum calculation with different buffer sizes."""
        with patch('builtins.open', mock_open(read_data=sample_file_content)):
            result = file_checksum('test_file.txt', buf_size=buf_size)
            assert result == expected_checksum

    def test_file_checksum_large_file_chunked_reading(self):
        """Test checksum calculation for large file with chunked reading."""
        # Create content larger than buffer size
        large_content_size = 100000  # 100KB content
        buf_size = 1024
        large_content = b'x' * large_content_size
        expected_checksum = hashlib.sha256(large_content).hexdigest()

        # Mock file that returns content in chunks
        def side_effect(size):
            if not hasattr(side_effect, 'position'):
                side_effect.position = 0

            start = side_effect.position
            end = min(start + size, len(large_content))

            if start >= len(large_content):
                return b''

            chunk = large_content[start:end]
            side_effect.position = end
            return chunk

        # Create a mock file object
        mock_file = MagicMock()
        mock_file.read.side_effect = side_effect

        # Create a mock context manager that returns our mock file
        mock_context_manager = MagicMock()
        mock_context_manager.__enter__.return_value = mock_file
        mock_context_manager.__exit__.return_value = None

        with patch('builtins.open', return_value=mock_context_manager):
            result = file_checksum('large_file.txt', buf_size=buf_size)
            assert result == expected_checksum

        call_counts = large_content_size // buf_size + 1
        if large_content_size % buf_size != 0:
            call_counts += 1
        assert mock_file.read.call_count == call_counts

    def test_file_checksum_empty_file(self):
        """Test checksum calculation for empty file."""
        expected_checksum = hashlib.sha256(b'').hexdigest()

        with patch('builtins.open', mock_open(read_data=b'')):
            result = file_checksum('empty_file.txt')
            assert result == expected_checksum

    def test_file_checksum_file_not_found(self):
        """Test file_checksum raises exception when file doesn't exist."""
        with patch('builtins.open', side_effect=FileNotFoundError):
            with pytest.raises(FileNotFoundError):
                file_checksum('nonexistent.txt')


class TestRemoveWidowDbRows:
    """Test cases for remove_widow_db_rows function."""

    @pytest.fixture
    def mock_model_instance(self):
        """Create a mock model instance."""
        mock_instance = Mock(spec=Model)
        mock_instance._meta = Mock()
        mock_instance._meta.fields = {}
        return mock_instance

    @pytest.fixture
    def mock_model_class(self):
        """Create a mock model class."""
        mock_class = Mock(spec=type(Model))
        mock_class._meta = Mock()
        mock_class._meta.fields = {}
        # Setup the method chain properly
        mock_query = Mock()
        mock_query.execute.return_value = []

        mock_select = Mock()
        mock_select.select.return_value = mock_query

        mock_class.select = mock_select
        return mock_class

    @patch('mafw.db.std_tables.TriggerDisabler')
    def test_remove_widow_db_rows_single_model_instance(self, trigger_disabler, mock_model_instance):
        """Test remove_widow_db_rows with single model instance."""
        # Setup mock field that exists
        mock_field = Mock(spec=FileNameField)
        mock_path = Mock(spec=Path)
        mock_path.exists.return_value = True

        trigger_disabler.__enter__ = Mock()
        trigger_disabler.__exit__ = Mock()

        mock_model_instance._meta.fields = {'filename': mock_field}
        setattr(mock_model_instance, 'filename', mock_path)

        remove_widow_db_rows(mock_model_instance)

        # Should not delete instance since file exists
        mock_model_instance.delete_instance.assert_not_called()

    @patch('mafw.db.std_tables.TriggerDisabler')
    def test_remove_widow_db_rows_single_model_instance_missing_file(self, trigger_disabler, mock_model_instance):
        """Test remove_widow_db_rows with single model instance and missing file."""
        # Setup mock field that doesn't exist
        mock_field = Mock(spec=FileNameField)
        mock_path = Mock(spec=Path)
        mock_path.exists.return_value = False
        trigger_disabler.__enter__ = Mock()
        trigger_disabler.__exit__ = Mock()

        mock_model_instance._meta.fields = {'filename': mock_field}
        setattr(mock_model_instance, 'filename', mock_path)

        remove_widow_db_rows(mock_model_instance)

        # Should delete instance since file doesn't exist
        mock_model_instance.delete_instance.assert_called_once()

    @patch('mafw.db.std_tables.TriggerDisabler')
    def test_remove_widow_db_rows_filename_list_field_all_exist(self, trigger_disabler, mock_model_instance):
        """Test remove_widow_db_rows with FileNameListField where all files exist."""
        mock_field = Mock(spec=FileNameListField)
        trigger_disabler.__enter__ = Mock()
        trigger_disabler.__exit__ = Mock()

        # Mock the split result and Path objects
        mock_model_instance._meta.fields = {'filenames': mock_field}
        setattr(mock_model_instance, 'filenames', Mock())
        mock_model_instance.filenames.split.return_value = ['file1.txt', 'file2.txt']

        with patch('mafw.tools.file_tools.Path') as mock_path_class:
            mock_path1 = Mock()
            mock_path1.exists.return_value = True
            mock_path2 = Mock()
            mock_path2.exists.return_value = True
            mock_path_class.side_effect = [mock_path1, mock_path2]

            remove_widow_db_rows(mock_model_instance)

        mock_model_instance.delete_instance.assert_not_called()

    @patch('mafw.db.std_tables.TriggerDisabler')
    def test_remove_widow_db_rows_filename_list_field_some_missing(self, trigger_disabler, mock_model_instance):
        """Test remove_widow_db_rows with FileNameListField where some files are missing."""
        mock_field = Mock(spec=FileNameListField)

        trigger_disabler.__enter__ = Mock()
        trigger_disabler.__exit__ = Mock()

        mock_model_instance._meta.fields = {'filenames': mock_field}
        setattr(mock_model_instance, 'filenames', Mock())
        mock_model_instance.filenames.split.return_value = ['file1.txt', 'file2.txt']

        with patch('mafw.tools.file_tools.Path') as mock_path_class:
            mock_path1 = Mock()
            mock_path1.exists.return_value = True
            mock_path2 = Mock()
            mock_path2.exists.return_value = False  # Missing file
            mock_path_class.side_effect = [mock_path1, mock_path2]

            remove_widow_db_rows(mock_model_instance)

        mock_model_instance.delete_instance.assert_called_once()

    @patch('mafw.db.std_tables.TriggerDisabler')
    def test_remove_widow_db_rows_model_class(self, trigger_disabler, mock_model_class):
        """Test remove_widow_db_rows with model class."""
        # Setup mock instances returned by select
        mock_instance1 = Mock(spec=Model)
        mock_instance1._meta = Mock()
        mock_instance1._meta.fields = {}

        trigger_disabler.__enter__ = Mock()
        trigger_disabler.__exit__ = Mock()

        mock_instance2 = Mock(spec=Model)
        mock_instance2._meta = Mock()
        mock_instance2._meta.fields = {}

        # Properly mock the method chain
        mock_query = Mock()
        mock_query.execute.return_value = [mock_instance1, mock_instance2]
        mock_model_class.select.return_value = mock_query

        remove_widow_db_rows(mock_model_class)

        # Verify select was called
        mock_model_class.select.assert_called_once()
        mock_query.execute.assert_called_once()

    @patch('mafw.db.std_tables.TriggerDisabler')
    def test_remove_widow_db_rows_list_of_models(self, trigger_disabler, mock_model_instance, mock_model_class):
        """Test remove_widow_db_rows with list of models."""
        mock_instance = Mock(spec=Model)
        mock_instance._meta = Mock()
        mock_instance._meta.fields = {}

        trigger_disabler.__enter__ = Mock()
        trigger_disabler.__exit__ = Mock()

        mock_query = Mock()
        mock_query.execute.return_value = [mock_instance]
        mock_model_class.select.return_value = mock_query

        models = [mock_model_instance, mock_model_class]

        remove_widow_db_rows(models)

        # Should process both models
        mock_model_class.select.assert_called_once()

    @patch('mafw.db.std_tables.TriggerDisabler')
    def test_remove_widow_db_rows_invalid_type(self, trigger_disabler):
        """Test remove_widow_db_rows with invalid model type."""

        trigger_disabler.__enter__ = Mock()
        trigger_disabler.__exit__ = Mock()

        with pytest.raises(TypeError, match='models must be'):
            remove_widow_db_rows('invalid_type')

    @patch('mafw.db.std_tables.TriggerDisabler')
    def test_remove_widow_db_rows_mixed_field_types(self, trigger_disabler, mock_model_instance):
        """Test remove_widow_db_rows with both FileNameField and FileNameListField."""
        filename_field = Mock(spec=FileNameField)
        filelist_field = Mock(spec=FileNameListField)
        regular_field = Mock()  # Not a filename field

        trigger_disabler.__enter__ = Mock()
        trigger_disabler.__exit__ = Mock()

        mock_model_instance._meta.fields = {
            'filename': filename_field,
            'filenames': filelist_field,
            'other_field': regular_field,
        }

        # Setup filename field
        mock_path = Mock(spec=Path)
        mock_path.exists.return_value = True
        setattr(mock_model_instance, 'filename', mock_path)

        # Setup filenames field
        setattr(mock_model_instance, 'filenames', Mock())
        mock_model_instance.filenames.split.return_value = ['file1.txt']

        with patch('mafw.tools.file_tools.Path') as mock_path_class:
            mock_path_list = Mock()
            mock_path_list.exists.return_value = True
            mock_path_class.return_value = mock_path_list

            remove_widow_db_rows(mock_model_instance)

        mock_model_instance.delete_instance.assert_not_called()


class TestVerifyChecksum:
    """Test cases for verify_checksum function."""

    @pytest.fixture
    def mock_model_with_checksum(self):
        """Create a mock model with checksum field."""
        mock_instance = Mock(spec=Model)
        mock_instance._meta = Mock()

        # Setup FileNameField with checksum
        mock_field = Mock(spec=FileNameField)
        mock_field.checksum_field = 'file_checksum'

        mock_instance._meta.fields = {'filename': mock_field}

        # Setup the file path and checksum
        mock_path = Mock(spec=Path)
        mock_path.exists.return_value = True
        setattr(mock_instance, 'filename', mock_path)
        setattr(mock_instance, 'file_checksum', 'stored_checksum_value')

        return mock_instance

    @patch('mafw.db.std_tables.TriggerDisabler')
    def test_verify_checksum_valid_checksum(self, trigger_disabler, mock_model_with_checksum):
        """Test verify_checksum with valid checksum."""
        trigger_disabler.__enter__ = Mock()
        trigger_disabler.__exit__ = Mock()

        with patch('mafw.tools.file_tools.file_checksum', return_value='stored_checksum_value'):
            verify_checksum(mock_model_with_checksum)

        # Should not delete instance since checksums match
        mock_model_with_checksum.delete_instance.assert_not_called()

    @patch('mafw.db.std_tables.TriggerDisabler')
    def test_verify_checksum_invalid_checksum(self, trigger_disabler, mock_model_with_checksum):
        """Test verify_checksum with invalid checksum."""
        trigger_disabler.__enter__ = Mock()
        trigger_disabler.__exit__ = Mock()

        with patch('mafw.tools.file_tools.file_checksum', return_value='different_checksum'):
            verify_checksum(mock_model_with_checksum)

        # Should delete instance since checksums don't match
        mock_model_with_checksum.delete_instance.assert_called_once()

    @patch('mafw.db.std_tables.TriggerDisabler')
    def test_verify_checksum_missing_file(self, trigger_disabler, mock_model_with_checksum):
        """Test verify_checksum with missing file."""
        trigger_disabler.__enter__ = Mock()
        trigger_disabler.__exit__ = Mock()

        mock_model_with_checksum.filename.exists.return_value = False

        # with patch("warnings.warn") as mock_warn:
        with pytest.warns(UserWarning, match='does not exist'):
            verify_checksum(mock_model_with_checksum)

        # Should delete instance
        mock_model_with_checksum.delete_instance.assert_called_once()

    @patch('mafw.db.std_tables.TriggerDisabler')
    def test_verify_checksum_filename_list_field_valid(self, trigger_disabler):
        """Test verify_checksum with FileNameListField and valid checksums."""
        mock_instance = Mock(spec=Model)
        mock_instance._meta = Mock()
        trigger_disabler.__enter__ = Mock()
        trigger_disabler.__exit__ = Mock()

        # Setup FileNameListField with checksum
        mock_field = Mock(spec=FileNameListField)
        mock_field.checksum_field = 'files_checksum'

        mock_instance._meta.fields = {'filenames': mock_field}
        setattr(mock_instance, 'filenames', ['file1.txt', 'file2.txt'])
        setattr(mock_instance, 'files_checksum', 'stored_checksum')

        with patch('mafw.tools.file_tools.Path') as mock_path_class:
            mock_path1 = Mock()
            mock_path1.exists.return_value = True
            mock_path2 = Mock()
            mock_path2.exists.return_value = True
            mock_path_class.side_effect = [mock_path1, mock_path2]

            with patch('mafw.tools.file_tools.file_checksum', return_value='stored_checksum'):
                verify_checksum(mock_instance)

        mock_instance.delete_instance.assert_not_called()

    @patch('mafw.db.std_tables.TriggerDisabler')
    def test_verify_checksum_filename_list_field_missing_files(self, trigger_disabler):
        """Test verify_checksum with FileNameListField and missing files."""
        mock_instance = Mock(spec=Model)
        mock_instance._meta = Mock()
        mock_field = Mock(spec=FileNameListField)
        mock_field.checksum_field = 'files_checksum'
        trigger_disabler.__enter__ = Mock()
        trigger_disabler.__exit__ = Mock()

        # Setup FileNameListField with checksum
        mock_field = Mock(spec=FileNameListField)
        mock_field.checksum_field = 'files_checksum'

        mock_check = Mock(spec=FileChecksumField)

        mock_instance._meta.fields = {'filenames': mock_field, 'files_checksum': mock_check}
        setattr(mock_instance, 'filenames', ['file1.txt', 'file2.txt'])
        setattr(mock_instance, 'files_checksum', 'stored_checksum')

        with patch('mafw.tools.file_tools.Path') as mock_path_class:
            mock_path1 = Mock()
            mock_path1.exists.return_value = True
            mock_path2 = Mock()
            mock_path2.exists.return_value = False  # Missing file
            mock_path_class.side_effect = [mock_path1, mock_path2]

            with pytest.warns(UserWarning, match='A file is missing from the list'):
                verify_checksum(mock_instance)

        mock_instance.delete_instance.assert_called_once()

    @patch('mafw.db.std_tables.TriggerDisabler')
    def test_verify_checksum_no_checksum_field(self, trigger_disabler):
        """Test verify_checksum with field that has no checksum field."""
        mock_instance = Mock(spec=Model)
        mock_instance._meta = Mock()
        trigger_disabler.__enter__ = Mock()
        trigger_disabler.__exit__ = Mock()

        # Setup FileNameField without checksum
        mock_field = Mock(spec=FileNameField)
        mock_field.checksum_field = None

        mock_instance._meta.fields = {'filename': mock_field}

        verify_checksum(mock_instance)

        # Should not process anything
        mock_instance.delete_instance.assert_not_called()

    @patch('mafw.db.std_tables.TriggerDisabler')
    def test_verify_checksum_missing_checksum_field_attribute(self, trigger_disabler):
        """Test verify_checksum when model doesn't have the checksum field attribute."""
        mock_instance = Mock(spec=Model)
        mock_instance._meta = Mock()
        trigger_disabler.__enter__ = Mock()
        trigger_disabler.__exit__ = Mock()

        # Setup FileNameField with checksum field name
        mock_field = Mock(spec=FileNameField)
        mock_field.checksum_field = 'nonexistent_checksum'

        mock_instance._meta.fields = {'filename': mock_field}

        # Remove the checksum attribute
        del mock_instance.nonexistent_checksum

        with pytest.raises(ModelError, match='is referring to nonexistent_checksum'):
            verify_checksum(mock_instance)

    @patch('mafw.db.std_tables.TriggerDisabler')
    def test_verify_checksum_model_class(self, trigger_disabler):
        """Test verify_checksum with model class."""
        # Setup mock instances
        mock_instance = Mock(spec=Model)
        mock_instance._meta = Mock()
        mock_instance._meta.fields = {}
        trigger_disabler.__enter__ = Mock()
        trigger_disabler.__exit__ = Mock()

        # Setup mock class
        mock_class = Mock(spec=type(Model))
        mock_class._meta = Mock()
        mock_class._meta.fields = {}
        # Setup the method chain properly
        mock_query = Mock()
        mock_query.execute.return_value = [mock_instance]
        mock_select = Mock()
        mock_select.return_value = mock_query
        mock_class.select = mock_select

        verify_checksum(mock_class)

        mock_class.select.assert_called_once()

    @patch('mafw.db.std_tables.TriggerDisabler')
    def test_verify_checksum_list_of_models(self, trigger_disabler):
        """Test verify_checksum with list of models."""
        mock_instance = Mock(spec=Model)
        mock_instance._meta = Mock()
        mock_instance._meta.fields = {}

        trigger_disabler.__enter__ = Mock()
        trigger_disabler.__exit__ = Mock()

        # Setup mock class
        mock_class = Mock(spec=type(Model))
        mock_class._meta = Mock()
        mock_class._meta.fields = {}
        # Setup the method chain properly
        mock_query = Mock()
        mock_query.execute.return_value = [mock_instance]
        mock_select = Mock()
        mock_select.return_value = mock_query
        mock_class.select = mock_select

        verify_checksum([mock_instance, mock_class])

        mock_class.select.assert_called_once()

    @patch('mafw.db.std_tables.TriggerDisabler')
    def test_verify_checksum_invalid_type(self, trigger_disabler):
        """Test verify_checksum with invalid model type."""
        trigger_disabler.__enter__ = Mock()
        trigger_disabler.__exit__ = Mock()
        with pytest.raises(TypeError, match='models must be'):
            verify_checksum('invalid_type')

    @pytest.mark.parametrize('field_type', [FileNameField, FileNameListField])
    @patch('mafw.db.std_tables.TriggerDisabler')
    def test_verify_checksum_different_field_types(self, trigger_disabler, field_type):
        """Test verify_checksum with different field types."""
        mock_instance = Mock(spec=Model)
        mock_instance._meta = Mock()
        trigger_disabler.__enter__ = Mock()
        trigger_disabler.__exit__ = Mock()

        mock_field = Mock(spec=field_type)
        mock_field.checksum_field = None  # No checksum field

        mock_instance._meta.fields = {'test_field': mock_field}

        verify_checksum(mock_instance)

        # Should not process since no checksum field
        mock_instance.delete_instance.assert_not_called()


@pytest.mark.integration_test
class TestIntegration:
    """Integration tests combining multiple functions."""

    @patch('mafw.db.std_tables.TriggerDisabler')
    def test_file_checksum_integration_with_verify_checksum(self, trigger_disabler):
        """Test integration between file_checksum and verify_checksum."""
        trigger_disabler.__enter__ = Mock()
        trigger_disabler.__exit__ = Mock()

        # Create test content
        test_content = b'Integration test content'
        expected_checksum = hashlib.sha256(test_content).hexdigest()

        # Create mock model
        mock_instance = Mock(spec=Model)
        mock_instance._meta = Mock()

        mock_field = Mock(spec=FileNameField)
        mock_field.checksum_field = 'file_checksum'

        mock_instance._meta.fields = {'filename': mock_field}

        mock_path = Mock(spec=Path)
        mock_path.exists.return_value = True
        setattr(mock_instance, 'filename', mock_path)
        setattr(mock_instance, 'file_checksum', expected_checksum)

        with patch('builtins.open', mock_open(read_data=test_content)):
            verify_checksum(mock_instance)

        # Should not delete since checksums match
        mock_instance.delete_instance.assert_not_called()

    @patch('mafw.db.std_tables.TriggerDisabler')
    def test_edge_case_empty_fields_dict(self, trigger_disabler):
        """Test edge case with empty fields dictionary."""
        mock_instance = Mock(spec=Model)
        mock_instance._meta = Mock()
        mock_instance._meta.fields = {}

        trigger_disabler.__enter__ = Mock()
        trigger_disabler.__exit__ = Mock()

        # Should not raise any exceptions
        remove_widow_db_rows(mock_instance)
        verify_checksum(mock_instance)

        mock_instance.delete_instance.assert_not_called()

    @pytest.mark.slow_integration_test
    @patch('mafw.db.std_tables.TriggerDisabler')
    def test_real_database_integration(self, trigger_disabler, tmp_path):
        """
        Full integration test with real SQLite database and actual files.

        This test creates real files, a real database model, and tests the complete
        workflow of adding files to database, then running verify_checksum and
        remove_widow_db_rows after modifying/removing some files.
        """
        from peewee import SqliteDatabase

        trigger_disabler.__enter__ = Mock()
        trigger_disabler.__exit__ = Mock()

        # Create a temporary in-memory SQLite database
        test_db = SqliteDatabase(':memory:')

        # Define a test model with filename and checksum fields
        class TestFileModel(Model):
            filename = FileNameField(checksum_field='file_checksum')
            file_checksum = FileChecksumField()

            class Meta:
                database = test_db

        # Create the table
        test_db.create_tables([TestFileModel])

        try:
            # Create test files with different content
            test_files = []
            test_contents = [
                b'Content of file 1 - Hello World!',
                b'Content of file 2 - Integration test data',
                b'Content of file 3 - More test content here',
                b'Content of file 4 - This file will be deleted',
                b'Content of file 5 - This file will be modified',
            ]

            # Create actual test files
            for i, content in enumerate(test_contents, 1):
                test_file = tmp_path / f'test_file_{i}.txt'
                test_file.write_bytes(content)
                test_files.append(test_file)

            # Calculate checksums and insert into database
            records = []
            for test_file in test_files:
                record = TestFileModel.create(filename=test_file, file_checksum=test_file)
                records.append(record)

            # Verify initial state - all 5 records should exist
            assert TestFileModel.select().count() == 5

            # Test 1: Remove a file and run remove_widow_db_rows
            test_files[3].unlink()  # Remove test_file_4.txt

            remove_widow_db_rows(TestFileModel)
            # Should have 4 records now (one removed due to missing file)
            remaining_records = list(TestFileModel.select())
            assert len(remaining_records) == 4

            # Verify the deleted file's record is gone
            deleted_file_records = TestFileModel.select().where(TestFileModel.filename == str(test_files[3]))
            assert len(list(deleted_file_records)) == 0

            # Test 2: Modify a file and run verify_checksum
            modified_content = b'MODIFIED - This content has been changed!'
            test_files[4].write_bytes(modified_content)

            verify_checksum(TestFileModel)

            # Should have 3 records now (one more removed due to checksum mismatch)
            final_records = list(TestFileModel.select())
            assert len(final_records) == 3

            # Verify the modified file's record is gone
            modified_file_records = TestFileModel.select().where(TestFileModel.filename == str(test_files[4]))
            assert len(list(modified_file_records)) == 0

            # Test 3: Verify remaining files still have correct checksums
            for record in final_records:
                file_path = Path(record.filename)
                if file_path.exists():
                    actual_checksum = file_checksum(file_path)
                    assert actual_checksum == record.file_checksum, f'Checksum mismatch for {file_path}'

            print('Integration test completed successfully!')
            print(f'Final database state: {TestFileModel.select().count()} records')
            print(f'Test files created in: {tmp_path}')

        finally:
            # Clean up
            test_db.close()

        # Verify test files cleanup
        existing_files = [f for f in test_files if f.exists()]
        print(f'Remaining test files: {len(existing_files)}')
        assert len(existing_files) == 4  # Files 1, 2, 3 and modified file 5 should remain
