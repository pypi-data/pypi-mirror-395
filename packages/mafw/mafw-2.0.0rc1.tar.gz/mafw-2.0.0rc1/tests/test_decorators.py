#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Unit tests for decorators.py module.
"""

import warnings
from unittest.mock import Mock, patch

import pytest

from mafw.decorators import (
    class_depends_on_optional,
    database_required,
    depends_on_optional,
    execution_workflow,
    for_loop,
    orphan_protector,
    processor_depends_on_optional,
    single_loop,
    singleton,
    suppress_warnings,
    while_loop,
)
from mafw.enumerators import LoopType
from mafw.mafw_errors import MissingDatabase
from mafw.processor import Processor


class TestSingleton:
    """Test cases for the singleton decorator."""

    def test_singleton_creates_single_instance(self):
        """Test that singleton decorator creates only one instance."""

        @singleton
        class TestClass:
            def __init__(self, value):
                self.value = value

        instance1 = TestClass(1)
        instance2 = TestClass(2)

        assert instance1 is instance2
        assert instance1.value == 1  # First instance value is preserved
        assert instance2.value == 1

    def test_singleton_with_different_args(self):
        """Test singleton with different arguments still returns same instance."""

        @singleton
        class TestClass:
            def __init__(self, a=1, b=2):
                self.a = a
                self.b = b

        instance1 = TestClass(a=10, b=20)
        instance2 = TestClass(a=30, b=40)

        assert instance1 is instance2
        assert instance1.a == 10
        assert instance1.b == 20

    def test_singleton_reset_between_tests(self):
        """Test that different singleton classes don't interfere."""

        @singleton
        class TestClass1:
            def __init__(self):
                self.name = 'class1'

        @singleton
        class TestClass2:
            def __init__(self):
                self.name = 'class2'

        instance1 = TestClass1()
        instance2 = TestClass2()

        assert instance1 is not instance2
        assert instance1.name == 'class1'
        assert instance2.name == 'class2'


class TestDatabaseRequired:
    """Test cases for the database_required decorator."""

    @suppress_warnings
    def test_database_required_with_database(self):
        """Test that processor starts when database is available."""

        @database_required
        class TestProcessor(Processor):
            def __init__(self):
                super().__init__()
                self._database = Mock()  # Mock database
                self.started = False

            def start(self):
                self.started = True

        processor = TestProcessor()
        processor.start()
        assert processor.started is True

    @suppress_warnings
    def test_database_required_without_database(self):
        """Test that processor raises MissingDatabase when database is None."""

        @database_required
        class TestProcessor(Processor):
            def __init__(self):
                super().__init__()
                self._database = None
                self.name = 'TestProcessor'

            def start(self):
                pass

        processor = TestProcessor()
        with pytest.raises(MissingDatabase, match='TestProcessor requires an active database'):
            processor.start()

    @suppress_warnings
    def test_database_required_preserves_original_start(self):
        """Test that original start method is called when database exists."""
        original_start_called = False

        @database_required
        class TestProcessor(Processor):
            def __init__(self):
                super().__init__()
                self._database = Mock()

            def start(self):
                nonlocal original_start_called
                original_start_called = True

        processor = TestProcessor()
        processor.start()
        assert original_start_called is True


class TestOrphanProtector:
    """Test cases for the orphan_protector decorator."""

    @suppress_warnings
    def test_orphan_protector_sets_remove_orphan_files_false(self):
        """Test that orphan_protector sets remove_orphan_files to False."""

        @orphan_protector
        class TestProcessor(Processor):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

        processor = TestProcessor()
        assert not processor.remove_orphan_files

    @suppress_warnings
    def test_orphan_protector_with_other_kwargs(self):
        """Test orphan_protector works with other keyword arguments."""

        @orphan_protector
        class TestProcessor(Processor):
            def __init__(self, *args, custom_param=None, **kwargs):
                super().__init__(*args, **kwargs)
                self.custom_param = custom_param

        processor = TestProcessor(custom_param='test_value')
        assert processor.custom_param == 'test_value'
        assert not processor.remove_orphan_files

    @suppress_warnings
    def test_orphan_protector_with_args(self):
        """Test orphan_protector works with positional arguments."""

        @orphan_protector
        class TestProcessor(Processor):
            def __init__(self, arg1, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.arg1 = arg1

        processor = TestProcessor('test_arg')
        assert processor.arg1 == 'test_arg'
        assert not processor.remove_orphan_files


class TestExecutionWorkflow:
    """Test cases for execution_workflow decorator and its shortcuts."""

    @pytest.mark.parametrize(
        'loop_type,expected',
        [
            (LoopType.SingleLoop, LoopType.SingleLoop),
            (LoopType.ForLoop, LoopType.ForLoop),
            (LoopType.WhileLoop, LoopType.WhileLoop),
            ('single', 'single'),
            ('for_loop', 'for_loop'),
            ('while_loop', 'while_loop'),
        ],
    )
    @suppress_warnings
    def test_execution_workflow_with_different_loop_types(self, loop_type, expected):
        """Test execution_workflow decorator with different loop types."""

        @execution_workflow(loop_type)
        class TestProcessor(Processor):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

        processor = TestProcessor()
        assert processor.loop_type == expected

    @suppress_warnings
    def test_execution_workflow_default_loop_type(self):
        """Test execution_workflow decorator with default loop type."""

        @execution_workflow()
        class TestProcessor(Processor):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

        processor = TestProcessor()
        assert processor.loop_type == LoopType.ForLoop

    def test_single_loop_shortcut(self):
        """Test single_loop decorator shortcut."""

        @single_loop
        class TestProcessor(Processor):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

        processor = TestProcessor()
        assert processor.loop_type == LoopType.SingleLoop

    @suppress_warnings
    def test_for_loop_shortcut(self):
        """Test for_loop decorator shortcut."""

        @for_loop
        class TestProcessor(Processor):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

        processor = TestProcessor()
        assert processor.loop_type == LoopType.ForLoop

    @suppress_warnings
    def test_while_loop_shortcut(self):
        """Test while_loop decorator shortcut."""

        @while_loop
        class TestProcessor(Processor):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

        processor = TestProcessor()
        assert processor.loop_type == LoopType.WhileLoop


class TestDependsOnOptional:
    """Test cases for depends_on_optional decorator."""

    def test_depends_on_optional_module_found(self):
        """Test function execution when optional module is found."""
        with patch('mafw.decorators.find_spec') as mock_find_spec:
            mock_find_spec.return_value = Mock()  # Module found

            @depends_on_optional('existing_module')
            def test_function():
                return 'success'

            result = test_function()
            assert result == 'success'
            mock_find_spec.assert_called_once_with('existing_module')

    def test_depends_on_optional_module_not_found_with_warning(self):
        """Test function behavior when module not found with warning enabled."""
        with patch('mafw.decorators.find_spec') as mock_find_spec:
            mock_find_spec.return_value = None  # Module not found

            @depends_on_optional('missing_module', raise_ex=False, warn=True)
            def test_function():
                return 'success'

            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter('always')
                result = test_function()

                assert result is None
                assert len(w) == 1
                assert 'Optional dependency missing_module not found' in str(w[0].message)

    def test_depends_on_optional_module_not_found_with_exception(self):
        """Test function behavior when module not found with exception enabled."""
        with patch('mafw.decorators.find_spec') as mock_find_spec:
            mock_find_spec.return_value = None  # Module not found

            @depends_on_optional('missing_module', raise_ex=True)
            def test_function():
                return 'success'

            with pytest.raises(ImportError, match='Optional dependency missing_module not found'):
                test_function()

    def test_depends_on_optional_module_not_found_silent(self):
        """Test function behavior when module not found silently."""
        with patch('mafw.decorators.find_spec') as mock_find_spec:
            mock_find_spec.return_value = None  # Module not found

            @depends_on_optional('missing_module', raise_ex=False, warn=False)
            def test_function():
                return 'success'

            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter('always')
                result = test_function()

                assert result is None
                assert len(w) == 0  # No warnings

    def test_depends_on_optional_multiple_modules(self):
        """Test depends_on_optional with multiple modules."""
        with patch('mafw.decorators.find_spec') as mock_find_spec:
            # First module found, second not found
            mock_find_spec.side_effect = [Mock(), None]

            @depends_on_optional('module1;module2', raise_ex=False, warn=True)
            def test_function():
                return 'success'

            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter('always')
                result = test_function()

                assert result is None
                assert len(w) == 1
                assert 'Optional dependency module1;module2 not found' in str(w[0].message)

    def test_depends_on_optional_multiple_modules_all_found(self):
        """Test depends_on_optional with multiple modules all found."""
        with patch('mafw.decorators.find_spec') as mock_find_spec:
            mock_find_spec.return_value = Mock()  # Both modules found

            @depends_on_optional('module1;module2')
            def test_function():
                return 'success'

            result = test_function()
            assert result == 'success'
            assert mock_find_spec.call_count == 2

    def test_depends_on_optional_preserves_function_metadata(self):
        """Test that decorator preserves function metadata."""
        with patch('mafw.decorators.find_spec') as mock_find_spec:
            mock_find_spec.return_value = Mock()

            @depends_on_optional('existing_module')
            def test_function():
                """Test function docstring."""
                return 'success'

            assert test_function.__name__ == 'test_function'
            assert test_function.__doc__ == 'Test function docstring.'


class TestProcessorDependsOnOptional:
    """Test cases for processor_depends_on_optional decorator."""

    @suppress_warnings
    def test_processor_depends_on_optional_module_found(self):
        """Test class is returned as-is when module is found."""
        with patch('mafw.decorators.find_spec') as mock_find_spec:
            mock_find_spec.return_value = Mock()  # Module found

            @processor_depends_on_optional('existing_module')
            class TestProcessor(Processor):
                def __init__(self):
                    super().__init__()
                    self.test_attr = 'original'

            assert TestProcessor.__name__ == 'TestProcessor'
            processor = TestProcessor()
            assert processor.test_attr == 'original'

    def test_processor_depends_on_optional_module_not_found_with_warning(self):
        """Test processor behavior when module not found with warning."""
        with patch('mafw.decorators.find_spec') as mock_find_spec:
            mock_find_spec.return_value = None  # Module not found

            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter('always')

                @processor_depends_on_optional('missing_module', raise_ex=False, warn=True)
                class TestProcessor(Processor):
                    def __init__(self):
                        super().__init__()
                        self.test_attr = 'original'

                # The returned class should be a modified Processor
                assert 'Missing missing_module' in TestProcessor.__name__

                assert len(w) == 1
                assert 'Optional dependency missing_module not found' in str(w[0].message)

    def test_processor_depends_on_optional_module_not_found_with_exception(self):
        """Test processor behavior when module not found with exception."""
        with patch('mafw.decorators.find_spec') as mock_find_spec:
            mock_find_spec.return_value = None  # Module not found

            with pytest.raises(ImportError, match='Optional dependency missing_module not found'):

                @processor_depends_on_optional('missing_module', raise_ex=True)
                class TestProcessor(Processor):
                    pass

    def test_processor_depends_on_optional_module_not_found_silent(self):
        """Test processor behavior when module not found silently."""
        with patch('mafw.decorators.find_spec') as mock_find_spec:
            mock_find_spec.return_value = None  # Module not found

            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter('always')

                @processor_depends_on_optional('missing_module', raise_ex=False, warn=False)
                class TestProcessor(Processor):
                    def __init__(self):
                        super().__init__()
                        self.test_attr = 'original'

                assert 'Missing missing_module' in TestProcessor.__name__
                assert len(w) == 0  # No warnings

    def test_processor_depends_on_optional_multiple_modules(self):
        """Test processor_depends_on_optional with multiple modules."""
        with patch('mafw.decorators.find_spec') as mock_find_spec:
            # First module found, second not found
            mock_find_spec.side_effect = [Mock(), None]

            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter('always')

                @processor_depends_on_optional('module1;module2', raise_ex=False, warn=True)
                class TestProcessor(Processor):
                    pass

                assert 'Missing module1;module2' in TestProcessor.__name__
                assert len(w) == 1
                assert 'Optional dependency module1;module2 not found' in str(w[0].message)

    def test_processor_depends_on_optional_preserves_class_metadata(self):
        """Test that decorator preserves class metadata when module not found."""
        with patch('mafw.decorators.find_spec') as mock_find_spec:
            mock_find_spec.return_value = None  # Module not found

            with warnings.catch_warnings(record=True):
                warnings.simplefilter('always')

                @processor_depends_on_optional('missing_module', raise_ex=False, warn=False)
                class TestProcessor(Processor):
                    """Test processor docstring."""

                    def __init__(self):
                        super().__init__()

                assert TestProcessor.__doc__ == 'Test processor docstring.'
                assert 'TestProcessor' in TestProcessor.__qualname__

    @suppress_warnings
    def test_processor_depends_on_optional_multiple_modules_all_found(self):
        """Test processor_depends_on_optional with multiple modules all found."""
        with patch('mafw.decorators.find_spec') as mock_find_spec:
            mock_find_spec.return_value = Mock()  # Both modules found

            @processor_depends_on_optional('module1;module2')
            class TestProcessor(Processor):
                def __init__(self):
                    super().__init__()
                    self.test_attr = 'original'

            assert TestProcessor.__name__ == 'TestProcessor'
            processor = TestProcessor()
            assert processor.test_attr == 'original'
            assert mock_find_spec.call_count == 2


class TestEdgeCases:
    """Test edge cases and integration scenarios."""

    @suppress_warnings
    def test_combined_decorators(self):
        """Test combining multiple decorators."""
        with patch('mafw.decorators.find_spec') as mock_find_spec:
            mock_find_spec.return_value = Mock()

            @singleton
            @database_required
            @orphan_protector
            class TestProcessor(Processor):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    self._database = Mock()
                    self.started = False

                def start(self):
                    self.started = True

            processor1 = TestProcessor()
            processor2 = TestProcessor()

            # Should be singleton
            assert processor1 is processor2

            # Should be able to start (has database)
            processor1.start()
            assert processor1.started is True

    def test_depends_on_optional_with_method(self):
        """Test depends_on_optional decorator on class methods."""
        with patch('mafw.decorators.find_spec') as mock_find_spec:
            mock_find_spec.return_value = None  # Module not found

            with warnings.catch_warnings(record=True) as w:

                class TestClass:
                    @depends_on_optional('missing_module', raise_ex=False, warn=True)
                    def test_method(self):
                        return 'method_result'

                obj = TestClass()

                warnings.simplefilter('always')
                result = obj.test_method()

                assert result is None
                assert len(w) == 1
                assert 'test_method' in str(w[0].message)


class TestSuppressWarnings:
    """Test cases for the suppress_warnings decorator."""

    def test_suppress_warnings_suppresses_warnings(self):
        """Test that suppress_warnings decorator suppresses warnings."""

        @suppress_warnings
        def function_with_warning():
            warnings.warn('This is a test warning', UserWarning)
            return 'function_result'

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            result = function_with_warning()

            assert result == 'function_result'
            assert len(w) == 0  # No warnings should be recorded

    def test_suppress_warnings_multiple_warnings(self):
        """Test that suppress_warnings suppresses multiple warnings."""

        @suppress_warnings
        def function_with_multiple_warnings():
            warnings.warn('Warning 1', UserWarning)
            warnings.warn('Warning 2', DeprecationWarning)
            warnings.warn('Warning 3', RuntimeWarning)
            return 'success'

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            result = function_with_multiple_warnings()

            assert result == 'success'
            assert len(w) == 0  # No warnings should be recorded

    def test_suppress_warnings_preserves_exceptions(self):
        """Test that suppress_warnings doesn't suppress exceptions."""

        @suppress_warnings
        def function_with_exception():
            warnings.warn('This warning should be suppressed', UserWarning)
            raise ValueError('This exception should not be suppressed')

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            with pytest.raises(ValueError, match='This exception should not be suppressed'):
                function_with_exception()

            assert len(w) == 0  # Warning should be suppressed

    def test_suppress_warnings_preserves_function_metadata(self):
        """Test that suppress_warnings preserves function metadata."""

        @suppress_warnings
        def test_function():
            """Test function docstring."""
            return 'success'

        assert test_function.__name__ == 'test_function'
        assert test_function.__doc__ == 'Test function docstring.'

    def test_suppress_warnings_with_arguments(self):
        """Test suppress_warnings with function arguments."""

        @suppress_warnings
        def function_with_args(a, b, c=None):
            warnings.warn('Test warning', UserWarning)
            return a + b + (c or 0)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            result = function_with_args(1, 2, c=3)

            assert result == 6
            assert len(w) == 0  # Warning should be suppressed

    def test_suppress_warnings_nested_calls(self):
        """Test suppress_warnings with nested function calls."""

        def inner_function():
            warnings.warn('Inner warning', UserWarning)
            return 'inner'

        @suppress_warnings
        def outer_function():
            warnings.warn('Outer warning', UserWarning)
            return inner_function()

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            result = outer_function()

            assert result == 'inner'
            assert len(w) == 0  # All warnings should be suppressed


class TestClassDependsOnOptional:
    # @pytest.fixture
    # def sample_class(self) -> Type[Any]:
    #     """
    #     Fixture to provide a sample class for decoration.
    #     """
    #     class SampleClass:
    #         """Sample class for testing."""
    #         pass
    #
    #     return SampleClass

    def test_class_depends_on_optional_module_found(self):
        """Test class is returned as-is when module is found."""
        with patch('mafw.decorators.find_spec') as mock_find_spec:
            mock_find_spec.return_value = Mock()  # Module found

            @class_depends_on_optional('existing_module')
            class SampleClass:
                def __init__(self):
                    super().__init__()
                    self.test_attr = 'original'

            assert SampleClass.__name__ == 'SampleClass'
            my_class = SampleClass()
            assert my_class.test_attr == 'original'

    def test_class_depends_on_optional_module_not_found_with_warning(self):
        """Test class behavior when module not found with warning."""
        with patch('mafw.decorators.find_spec') as mock_find_spec:
            mock_find_spec.return_value = None  # Module not found

            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter('always')

                @class_depends_on_optional('missing_module', raise_ex=False, warn=True)
                class SampleClass:
                    def __init__(self):
                        super().__init__()
                        self.test_attr = 'original'

                # The returned class should be a modified Processor
                assert 'Missing missing_module' in SampleClass.__name__

                assert len(w) == 1
                assert 'Optional dependency missing_module not found' in str(w[0].message)

    def test_class_depends_on_optional_module_not_found_with_exception(self):
        """Test class behavior when module not found with exception."""
        with patch('mafw.decorators.find_spec') as mock_find_spec:
            mock_find_spec.return_value = None  # Module not found

            with pytest.raises(ImportError, match='Optional dependency missing_module not found'):

                @class_depends_on_optional('missing_module', raise_ex=True)
                class SampleClass:
                    pass

    def test_class_depends_on_optional_module_not_found_silent(self):
        """Test class behavior when module not found silently."""
        with patch('mafw.decorators.find_spec') as mock_find_spec:
            mock_find_spec.return_value = None  # Module not found

            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter('always')

                @class_depends_on_optional('missing_module', raise_ex=False, warn=False)
                class SampleClass:
                    def __init__(self):
                        super().__init__()
                        self.test_attr = 'original'

                assert 'Missing missing_module' in SampleClass.__name__
                assert len(w) == 0  # No warnings

    def test_class_depends_on_optional_multiple_modules(self):
        """Test class_depends_on_optional with multiple modules."""
        with patch('mafw.decorators.find_spec') as mock_find_spec:
            # First module found, second not found
            mock_find_spec.side_effect = [Mock(), None]

            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter('always')

                @class_depends_on_optional('module1;module2', raise_ex=False, warn=True)
                class SampleClass:
                    pass

                assert 'Missing module1;module2' in SampleClass.__name__
                assert len(w) == 1
                assert 'Optional dependency module1;module2 not found' in str(w[0].message)

    def test_class_depends_on_optional_preserves_class_metadata(self):
        """Test that decorator preserves class metadata when module not found."""
        with patch('mafw.decorators.find_spec') as mock_find_spec:
            mock_find_spec.return_value = None  # Module not found

            with warnings.catch_warnings(record=True):
                warnings.simplefilter('always')

                @class_depends_on_optional('missing_module', raise_ex=False, warn=False)
                class SampleClass:
                    """Test docstring."""

                    def __init__(self):
                        super().__init__()

                assert SampleClass.__doc__ == 'Test docstring.'
                assert 'SampleClass' in SampleClass.__qualname__

    def test_class_depends_on_optional_multiple_modules_all_found(self):
        """Test class_depends_on_optional with multiple modules all found."""
        with patch('mafw.decorators.find_spec') as mock_find_spec:
            mock_find_spec.return_value = Mock()  # Both modules found

            @class_depends_on_optional('module1;module2')
            class SampleClass:
                def __init__(self):
                    super().__init__()
                    self.test_attr = 'original'

            assert SampleClass.__name__ == 'SampleClass'
            klass = SampleClass()
            assert klass.test_attr == 'original'
            assert mock_find_spec.call_count == 2


# class TestClassDependsOnOptional:
#     """
#     Tests for the `class_depends_on_optional` decorator.
#     """
#
#     @pytest.fixture
#     def mock_module(self):
#         """
#         Fixture to mock the module import system.
#         """
#         with patch("mafw.decorators.find_spec") as mock_find_spec:
#             yield mock_find_spec
#
#     @pytest.fixture
#     def sample_class(self) -> Type[Any]:
#         """
#         Fixture to provide a sample class for decoration.
#         """
#         class SampleClass:
#             """Sample class for testing."""
#             pass
#
#         return SampleClass
#
#     @pytest.mark.parametrize("modules, found", [
#         ("existing_module", True),
#         ("non_existing_module", False),
#         ("existing_module;another_existing", True),
#         ("existing_module;non_existing_module", False),
#     ])
#     def test_decorator_behavior(self, mock_module, sample_class, modules, found):
#         """
#         Test decorator behavior with different module availability.
#
#         :param mock_module: A patched mock of the module import system.
#         :param sample_class: A sample class to apply the decorator.
#         :param modules: A string of modules to test, separated by ';'.
#         :param found: A boolean indicating if the module(s) should be found.
#         """
#         mock_module.side_effect = lambda name: ModuleType(name) if "existing" in name else None
#         decorated_class = class_depends_on_optional(modules)(sample_class)
#
#         if found:
#             assert decorated_class is sample_class
#         else:
#             assert decorated_class is not sample_class
#             assert issubclass(decorated_class, sample_class)
#
#     def test_raises_import_error(self, mock_module, sample_class):
#         """
#         Test decorator raises ImportError when raise_ex is True and a module is missing.
#
#         :param mock_module: A patched mock of the module import system.
#         :param sample_class: A sample class to apply the decorator.
#         """
#         mock_module.return_value = None
#         with pytest.raises(ImportError):
#             class_depends_on_optional("non_existing_module", raise_ex=True)(sample_class)
#
#     def test_warning_emitted(self, mock_module, sample_class):
#         """
#         Test that a warning is emitted when warn is True and a module is missing.
#
#         :param mock_module: A patched mock of the module import system.
#         :param sample_class: A sample class to apply the decorator.
#         """
#         mock_module.return_value = None
#         with pytest.warns(Warning):
#             class_depends_on_optional("non_existing_module", warn=True)(sample_class)
#
#     def test_no_warning_when_suppressed(self, mock_module, sample_class):
#         """
#         Test that no warning is emitted when warn is False and a module is missing.
#
#         :param mock_module: A patched mock of the module import system.
#         :param sample_class: A sample class to apply the decorator.
#         """
#         mock_module.return_value = None
#         with pytest.warns(None) as record:
#             class_depends_on_optional("non_existing_module", warn=False)(sample_class)
#         assert len(record) == 0
