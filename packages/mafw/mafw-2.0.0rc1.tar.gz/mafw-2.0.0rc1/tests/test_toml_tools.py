#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Unit tests for toml_tools module.
"""

import datetime
import tempfile
from pathlib import Path, PosixPath, WindowsPath
from unittest.mock import Mock, patch

import pytest
from tomlkit import TOMLDocument
from tomlkit.exceptions import ConvertError
from tomlkit.items import StringType

import mafw
from mafw.decorators import single_loop
from mafw.mafw_errors import InvalidSteeringFile, UnknownDBEngine
from mafw.processor import ActiveParameter, PassiveParameter, Processor
from mafw.tools import toml_tools


class TestPathItem:
    """Test cases for PathItem class."""

    def test_path_item_unwrap_posix(self):
        """Test PathItem unwrap method returns Path object."""
        path_item = toml_tools.PathItem.from_raw('/test/path', type_=StringType.SLB, escape=False)
        result = path_item.unwrap()
        assert isinstance(result, Path)
        assert str(result) == '/test/path'


class TestPathEncoder:
    """Test cases for path_encoder function."""

    @patch('mafw.tools.toml_tools.isinstance')
    def test_path_encoder_posix_path(self, mock_isinstance):
        """Test encoding PosixPath objects."""
        # Create a mock object that will represent a PosixPath
        mock_path = Mock()
        mock_path.__str__ = Mock(return_value='/test/path')

        # Configure isinstance to return True for PosixPath, False for WindowsPath
        def isinstance_side_effect(obj, class_or_tuple):
            if obj is mock_path:
                if class_or_tuple is PosixPath:
                    return True
                elif class_or_tuple is WindowsPath:
                    return False
            # For other calls, use the real isinstance
            return isinstance(obj, class_or_tuple)

        mock_isinstance.side_effect = isinstance_side_effect

        result = toml_tools.path_encoder(mock_path)

        assert isinstance(result, toml_tools.PathItem)
        assert result._t == StringType.SLB

    @patch('mafw.tools.toml_tools.isinstance')
    def test_path_encoder_windows_path(self, mock_isinstance):
        """Test encoding WindowsPath objects."""
        # Create a mock object that will represent a WindowsPath
        mock_path = Mock()
        mock_path.__str__ = Mock(return_value='C:\\test\\path')

        # Configure isinstance to return True for WindowsPath, False for PosixPath
        def isinstance_side_effect(obj, class_or_tuple):
            if obj is mock_path:
                if class_or_tuple is WindowsPath:
                    return True
                elif class_or_tuple is PosixPath:
                    return False
            # For other calls, use the real isinstance
            return isinstance(obj, class_or_tuple)

        mock_isinstance.side_effect = isinstance_side_effect

        result = toml_tools.path_encoder(mock_path)

        assert isinstance(result, toml_tools.PathItem)
        assert result._t == StringType.SLL

    def test_path_encoder_invalid_object(self):
        """Test path_encoder raises ConvertError for invalid objects."""
        with pytest.raises(ConvertError):
            toml_tools.path_encoder('not_a_path')


class TestProcessorValidator:
    """Test cases for processor_validator function."""

    @pytest.fixture
    def mock_processor_class(self):
        """Create a mock processor class."""

        @single_loop
        class MockProcessor(Processor):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

        return MockProcessor

    @pytest.fixture
    def mock_processor_instance(self, mock_processor_class):
        """Create a mock processor instance."""
        return mock_processor_class()

    def test_processor_validator_valid_classes(self, mock_processor_class):
        """Test validator accepts processor classes."""
        result = toml_tools.processor_validator([mock_processor_class])
        assert result is True

    def test_processor_validator_valid_instances(self, mock_processor_instance):
        """Test validator accepts processor instances."""
        result = toml_tools.processor_validator([mock_processor_instance])
        assert result is True

    def test_processor_validator_mixed_valid(self, mock_processor_class, mock_processor_instance):
        """Test validator accepts mixed classes and instances."""
        result = toml_tools.processor_validator([mock_processor_class, mock_processor_instance])
        assert result is True

    def test_processor_validator_invalid_objects(self):
        """Test validator rejects invalid objects."""
        result = toml_tools.processor_validator(['not_a_processor', 123])
        assert result is False

    def test_processor_validator_mixed_valid_and_invalid(self, mock_processor_class, mock_processor_instance):
        result = toml_tools.processor_validator([mock_processor_class, mock_processor_instance, str])
        assert result is False


class TestNewTomlDoc:
    """Test cases for _new_toml_doc function."""

    @patch('mafw.tools.toml_tools.datetime')
    def test_new_toml_doc_structure(self, mock_datetime):
        """Test _new_toml_doc creates proper document structure."""
        mock_datetime.datetime.now.return_value = datetime.datetime(2024, 1, 1, 12, 0, 0)

        doc = toml_tools._new_toml_doc()

        assert isinstance(doc, TOMLDocument)
        assert 'analysis_name' in doc
        assert 'analysis_description' in doc
        assert doc['analysis_name'] == 'mafw analysis'
        assert doc['analysis_description'] == 'Summing up numbers'
        assert 'new_only' in doc
        assert 'mafw_version' in doc
        assert doc['mafw_version'] == mafw.__about__.__version__
        assert 'create_standard_tables' in doc
        assert doc['create_standard_tables'] is True
        assert '# MAFw steering file generated on 2024-01-01 12:00:00' in doc.as_string()


class TestAddDbConfiguration:
    """Test cases for _add_db_configuration function."""

    @pytest.fixture
    def sample_db_config_option1(self):
        """Sample database configuration in option1 format."""
        return {
            'DBConfiguration': {
                'URL': 'sqlite:///:memory:',
                'pragmas': {
                    'journal_mode': 'wal',
                    'cache_size': -64000,
                },
            }
        }

    @pytest.fixture
    def sample_db_config_option2(self):
        """Sample database configuration in option2 format."""
        return {
            'URL': 'sqlite:///:memory:',
            'pragmas': {
                'journal_mode': 'wal',
                'cache_size': -64000,
            },
        }

    @patch('mafw.tools.toml_tools.default_conf', {'sqlite': {'URL': 'sqlite:///:memory:', 'pragmas': {}}})
    def test_add_db_configuration_none_config(self):
        """Test _add_db_configuration with None config uses default."""
        doc = toml_tools._add_db_configuration(None, 'sqlite')

        assert 'DBConfiguration' in doc
        assert doc['DBConfiguration']['URL'] == 'sqlite:///:memory:'

    def test_add_db_configuration_option1(self, sample_db_config_option1):
        """Test _add_db_configuration with option1 format."""
        doc = toml_tools._add_db_configuration(sample_db_config_option1, 'sqlite')

        assert 'DBConfiguration' in doc
        assert doc['DBConfiguration']['URL'] == 'sqlite:///:memory:'
        assert 'pragmas' in doc['DBConfiguration']

    def test_add_db_configuration_option2(self, sample_db_config_option2):
        """Test _add_db_configuration with option2 format."""
        doc = toml_tools._add_db_configuration(sample_db_config_option2, 'sqlite')

        assert 'DBConfiguration' in doc
        assert doc['DBConfiguration']['URL'] == 'sqlite:///:memory:'
        assert 'pragmas' in doc['DBConfiguration']

    @patch('mafw.tools.toml_tools.default_conf', {})
    def test_add_db_configuration_unknown_engine(self):
        """Test _add_db_configuration raises error for unknown engine."""
        with pytest.raises(UnknownDBEngine):
            toml_tools._add_db_configuration(None, 'unknown_engine')

    @patch('mafw.tools.toml_tools.default_conf', {'sqlite': {'pragmas': {}}})
    def test_add_db_configuration_unknown_engine2(self):
        """Test _add_db_configuration raises error for unknown engine."""
        with pytest.raises(UnknownDBEngine):
            toml_tools._add_db_configuration(None, 'unknown_engine')

    @patch('mafw.tools.toml_tools.default_conf', {'sqlite': {'URL': 'sqlite:///:memory:'}})
    def test_add_db_configuration_invalid_option1(self):
        """Test _add_db_configuration handles invalid option1 format."""
        invalid_config = {'DBConfiguration': {'not_url': 'value'}}
        doc = toml_tools._add_db_configuration(invalid_config, 'sqlite')

        assert 'DBConfiguration' in doc
        assert doc['DBConfiguration']['URL'] == 'sqlite:///:memory:'

    @patch('mafw.tools.toml_tools.default_conf', {'sqlite': {'URL': 'sqlite:///:memory:'}})
    def test_add_db_configuration_invalid_option2(self):
        """Test _add_db_configuration handles invalid option2 format."""
        invalid_config = {'not_url': 'value'}
        doc = toml_tools._add_db_configuration(invalid_config, 'sqlite')

        assert 'DBConfiguration' in doc
        assert doc['DBConfiguration']['URL'] == 'sqlite:///:memory:'


class TestAddProcessorParametersToTomlDoc:
    """Test cases for _add_processor_parameters_to_toml_doc function."""

    @pytest.fixture
    def mock_processor_with_params(self):
        """Create a mock processor with parameters."""

        @single_loop
        class MockProcessor(Processor):
            """A test processor."""

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.param1 = PassiveParameter('param1', default='value1', help_doc='Parameter 1')
                self.param2 = PassiveParameter('param2', default=42, help_doc='Parameter 2')
                self.bool_param = PassiveParameter('bool_param', default=True, help_doc='Boolean parameter')

        return MockProcessor

    @pytest.fixture
    def mock_another_processor_with_params(self):
        """Create a mock processor with parameters."""

        @single_loop
        class MockAnotherProcessor(Processor):
            """A test processor."""

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.param1 = PassiveParameter('param1', default='value1', help_doc='Parameter 1')
                self.param2 = PassiveParameter('param2', default=42, help_doc='Parameter 2')
                self.bool_param = PassiveParameter('bool_param', default=True, help_doc='Boolean parameter')

        return MockAnotherProcessor

    def test_add_processor_parameters_single_processor(self, mock_processor_with_params):
        """Test adding single processor parameters."""
        doc = toml_tools._add_processor_parameters_to_toml_doc(mock_processor_with_params)

        assert 'available_processors' in doc
        assert mock_processor_with_params.__name__ in doc['available_processors']
        assert mock_processor_with_params.__name__ in doc

    def test_add_processor_parameters_processor_list(
        self, mock_processor_with_params, mock_another_processor_with_params
    ):
        """Test adding multiple processor parameters."""
        processors = [mock_processor_with_params, mock_another_processor_with_params]
        doc = toml_tools._add_processor_parameters_to_toml_doc(processors)

        assert 'available_processors' in doc
        assert len(doc['available_processors']) == 2

    def test_add_processor_parameters_processor_instance(self, mock_processor_with_params):
        """Test adding processor instance parameters."""
        instance = mock_processor_with_params()
        doc = toml_tools._add_processor_parameters_to_toml_doc(instance)

        assert 'available_processors' in doc
        assert instance.name in doc['available_processors']
        assert instance.name in doc

    def test_add_processor_parameters_processor_mixed_instance_class(
        self, mock_processor_with_params, mock_another_processor_with_params
    ):
        """Test adding processor instance parameters."""
        instance = mock_processor_with_params()
        doc = toml_tools._add_processor_parameters_to_toml_doc([instance, mock_another_processor_with_params])

        assert 'available_processors' in doc
        assert instance.name in doc['available_processors']
        assert instance.name in doc

    def test_add_processor_parameters_invalid_processors(self):
        """Test adding invalid processors raises TypeError."""
        with pytest.raises(TypeError):
            toml_tools._add_processor_parameters_to_toml_doc(['not_a_processor'])


class TestAddUserInterfaceConfiguration:
    """Test cases for _add_user_interface_configuration function."""

    def test_add_user_interface_configuration(self):
        """Test adding user interface configuration."""
        doc = toml_tools._add_user_interface_configuration()

        assert 'UserInterface' in doc
        assert doc['UserInterface']['interface'] == 'rich'


class TestGenerateSteeringFile:
    """Test cases for generate_steering_file function."""

    @pytest.fixture
    def mock_processor(self):
        """Create a mock processor."""

        @single_loop
        class MockProcessor(Processor):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.param = PassiveParameter('param', default='test', help_doc='Test parameter')

        return MockProcessor

    @patch('mafw.tools.toml_tools.default_conf', {'sqlite': {'URL': 'sqlite:///:memory:'}})
    def test_generate_steering_file_string_path(self, mock_processor):
        """Test generate_steering_file with string path."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.toml') as tmp:
            tmp_path = tmp.name

        try:
            toml_tools.generate_steering_file(tmp_path, mock_processor)

            # Verify file was created and has expected content
            with open(tmp_path, 'r') as f:
                content = f.read()
                assert 'analysis_name' in content
                assert 'DBConfiguration' in content
                assert 'UserInterface' in content
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    @patch('mafw.tools.toml_tools.default_conf', {'sqlite': {'URL': 'sqlite:///:memory:'}})
    def test_generate_steering_file_path_object(self, mock_processor):
        """Test generate_steering_file with Path object."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.toml') as tmp:
            tmp_path = Path(tmp.name)

        try:
            toml_tools.generate_steering_file(tmp_path, mock_processor)

            # Verify file was created
            assert tmp_path.exists()
            content = tmp_path.read_text()
            assert 'analysis_name' in content
        finally:
            tmp_path.unlink(missing_ok=True)

    @patch('mafw.tools.toml_tools.default_conf', {'postgresql': {'URL': 'postgresql://localhost'}})
    def test_generate_steering_file_custom_db_engine(self, mock_processor):
        """Test generate_steering_file with custom database engine."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.toml') as tmp:
            tmp_path = tmp.name

        try:
            toml_tools.generate_steering_file(tmp_path, mock_processor, db_engine='postgresql')

            with open(tmp_path, 'r') as f:
                content = f.read()
                assert 'postgresql' in content
        finally:
            Path(tmp_path).unlink(missing_ok=True)


class TestDumpProcessorParametersToToml:
    """Test cases for dump_processor_parameters_to_toml function."""

    @pytest.fixture
    def mock_processor(self):
        """Create a mock processor."""

        @single_loop
        class MockProcessor(Processor):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.param = PassiveParameter('param', default='test', help_doc='Test parameter')

        return MockProcessor

    def test_dump_processor_parameters_to_toml(self, mock_processor):
        """Test dumping processor parameters to TOML file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.toml') as tmp:
            tmp_path = tmp.name

        try:
            toml_tools.dump_processor_parameters_to_toml(mock_processor, tmp_path)

            # Verify file was created and has expected content
            with open(tmp_path, 'r') as f:
                content = f.read()
                assert 'available_processors' in content
                assert mock_processor.__name__ in content
        finally:
            Path(tmp_path).unlink(missing_ok=True)


class TestLoadSteeringFile:
    """Test cases for load_steering_file function."""

    @pytest.fixture
    def valid_toml_content(self):
        """Sample valid TOML content."""
        return """
processors_to_run = ["TestProcessor"]
analysis_name = "test"

[UserInterface]
interface = "rich"

[TestProcessor]
param = "value"
"""

    @pytest.fixture
    def valid_toml_content_with_replica(self):
        return """
processors_to_run = ["TestProcessor", "TestProcessor#123", "TestProcessor#456"]
analysis_name = "test"

[UserInterface]
interface = "rich"

[TestProcessor]
param = "value"

[\"TestProcessor#123\"]
param = "value_123"
"""

    @pytest.fixture
    def invalid_toml_content(self):
        """Sample invalid TOML content (missing required fields)."""
        return """
analysis_name = "test"
"""

    def test_load_steering_file_valid(self, valid_toml_content):
        """Test loading valid steering file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.toml') as tmp:
            tmp.write(valid_toml_content)
            tmp_path = tmp.name

        try:
            result = toml_tools.load_steering_file(tmp_path)

            assert 'processors_to_run' in result
            assert 'UserInterface' in result
            assert 'TestProcessor' in result
            assert result['processors_to_run'] == ['TestProcessor']
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    def test_load_steering_file_valid_with_replica(self, valid_toml_content_with_replica):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.toml') as tmp:
            tmp.write(valid_toml_content_with_replica)
            tmp_path = tmp.name

        try:
            result = toml_tools.load_steering_file(tmp_path)

            assert 'processors_to_run' in result
            assert 'UserInterface' in result
            assert 'TestProcessor' in result
            assert 'TestProcessor#123' in result
            # validation is still successful even if no TestProcessor#456 found because the base is there
            assert 'TestProcessor#456' not in result
            assert result['processors_to_run'] == ['TestProcessor', 'TestProcessor#123', 'TestProcessor#456']
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    def test_load_steering_file_invalid_missing_processors_to_run(self, invalid_toml_content):
        """Test loading steering file missing processors_to_run raises error."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.toml') as tmp:
            tmp.write(invalid_toml_content)
            tmp_path = tmp.name

        try:
            with pytest.raises(InvalidSteeringFile, match='Missing processors_to_run'):
                toml_tools.load_steering_file(tmp_path)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    def test_load_steering_file_invalid_missing_user_interface(self):
        """Test loading steering file missing UserInterface raises error."""
        content = """
processors_to_run = ["TestProcessor"]
analysis_name = "test"

[TestProcessor]
param = "value"
"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.toml') as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        try:
            with pytest.raises(InvalidSteeringFile, match='Missing UserInterface'):
                toml_tools.load_steering_file(tmp_path)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    def test_load_steering_file_missing_processor_section(self):
        """Test loading steering file missing processor section raises error."""
        content = """
processors_to_run = ["MissingProcessor"]
analysis_name = "test"

[UserInterface]
interface = "rich"
"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.toml') as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        try:
            with pytest.raises(InvalidSteeringFile, match='Missing MissingProcessor'):
                toml_tools.load_steering_file(tmp_path)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    def test_load_steering_file_no_validation(self, invalid_toml_content):
        """Test loading steering file without validation succeeds."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.toml') as tmp:
            tmp.write(invalid_toml_content)
            tmp_path = tmp.name

        try:
            result = toml_tools.load_steering_file(tmp_path, validate=False)
            assert 'analysis_name' in result
            assert result['analysis_name'] == 'test'
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    def test_load_steering_file_nonexistent(self):
        """Test loading non-existent steering file raises FileNotFoundError."""
        with pytest.raises(Exception):  # TOMLFile.read() raises various exceptions for missing files
            toml_tools.load_steering_file('/nonexistent/path.toml')


@pytest.mark.integration_test
class TestIntegration:
    """Integration tests combining multiple functions."""

    @pytest.fixture
    def full_processor_setup(self):
        """Create a complete processor setup for integration testing."""

        @single_loop
        class ActiveProcessor(Processor):
            """An active parameter processor."""

            active_param = ActiveParameter('active_param', default=10, help_doc='Active parameter')

        @single_loop
        class PassiveProcessor(Processor):
            """A passive parameter processor."""

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.passive_param = PassiveParameter('passive_param', default=20, help_doc='Passive parameter')

        return [ActiveProcessor, PassiveProcessor()]

    @patch('mafw.tools.toml_tools.default_conf', {'sqlite': {'URL': 'sqlite:///:memory:', 'pragmas': {}}})
    def test_generate_and_load_steering_file(self, full_processor_setup):
        """Test complete cycle of generating and loading steering file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.toml') as tmp:
            tmp_path = tmp.name

        try:
            # Generate steering file
            toml_tools.generate_steering_file(tmp_path, full_processor_setup)

            # Load and verify structure
            result = toml_tools.load_steering_file(tmp_path, validate=False)

            assert 'analysis_name' in result
            assert 'DBConfiguration' in result
            assert 'UserInterface' in result
            assert 'available_processors' in result

            # Check processors are listed
            processor_names = [p.__name__ if hasattr(p, '__name__') else p.name for p in full_processor_setup]
            for name in processor_names:
                assert name in result['available_processors']

        finally:
            Path(tmp_path).unlink(missing_ok=True)


# Additional parametrized tests for better coverage
class TestParametrized:
    """Parametrized tests for various scenarios."""

    @pytest.mark.parametrize(
        'db_engine,expected_url',
        [
            ('sqlite', 'sqlite:///:memory:'),
            ('postgresql', 'postgresql://localhost:5432/test'),
        ],
    )
    @patch(
        'mafw.tools.toml_tools.default_conf',
        {'sqlite': {'URL': 'sqlite:///:memory:'}, 'postgresql': {'URL': 'postgresql://localhost:5432/test'}},
    )
    def test_add_db_configuration_engines(self, db_engine, expected_url):
        """Test _add_db_configuration with different engines."""
        doc = toml_tools._add_db_configuration(None, db_engine)
        assert doc['DBConfiguration']['URL'] == expected_url

    @pytest.mark.parametrize(
        'processor_input', ['single_class', 'single_instance', 'list_classes', 'list_instances', 'mixed_list']
    )
    def test_processor_parameters_various_inputs(self, processor_input):
        """Test _add_processor_parameters_to_toml_doc with various input types."""

        @single_loop
        class TestProcessor(Processor):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.param = PassiveParameter('param', default='test', help_doc='Test param')

        @single_loop
        class AnotherTestProcessor(Processor):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.param = PassiveParameter('param', default='test', help_doc='Test param')

        if processor_input == 'single_class':
            processors = TestProcessor
        elif processor_input == 'single_instance':
            processors = TestProcessor()
        elif processor_input == 'list_classes':
            processors = [TestProcessor, AnotherTestProcessor]
        elif processor_input == 'list_instances':
            processors = [TestProcessor(), AnotherTestProcessor()]
        elif processor_input == 'mixed_list':
            processors = [TestProcessor, AnotherTestProcessor()]
        else:
            processors = []

        doc = toml_tools._add_processor_parameters_to_toml_doc(processors)
        assert 'available_processors' in doc
        assert len(doc['available_processors']) >= 1


# Mock-based tests for error handling and edge cases
class TestMockedBehavior:
    """Tests using mocks to test error conditions and edge cases."""

    @patch('builtins.open', side_effect=IOError('Disk full'))
    def test_generate_steering_file_write_error(self, mock_open):
        """Test generate_steering_file handles write errors."""

        @single_loop
        class MockProcessor(Processor):
            pass

        with pytest.raises(IOError, match='Disk full'):
            toml_tools.generate_steering_file('/fake/path.toml', MockProcessor)

    @patch('tomlkit.dump', side_effect=Exception('TOML error'))
    def test_dump_processor_parameters_toml_error(self, mock_dump):
        """Test dump_processor_parameters_to_toml handles TOML errors."""

        @single_loop
        class MockProcessor(Processor):
            pass

        with pytest.raises(Exception):
            toml_tools.dump_processor_parameters_to_toml(MockProcessor, '/fake/path.toml')

    @patch('mafw.tools.toml_tools.log')
    def test_logging_behavior(self, mock_log):
        """Test that logging is called appropriately."""
        invalid_config = {'not_url': 'value'}

        with patch('mafw.tools.toml_tools.default_conf', {'sqlite': {'URL': 'sqlite:///:memory:'}}):
            toml_tools._add_db_configuration(invalid_config, 'sqlite')

        mock_log.error.assert_called()
