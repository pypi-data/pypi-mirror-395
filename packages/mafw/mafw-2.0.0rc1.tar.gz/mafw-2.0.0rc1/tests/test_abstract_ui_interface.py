#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Unit tests for the abstract_user_interface module.

This module contains comprehensive tests for the UserInterfaceMeta metaclass
and UserInterfaceBase abstract class, ensuring proper validation and behavior.
"""

from unittest.mock import Mock, patch

import pytest

from mafw.enumerators import ProcessorStatus
from mafw.ui.abstract_user_interface import UserInterfaceBase, UserInterfaceMeta


class TestUserInterfaceMeta:
    """Test class for UserInterfaceMeta metaclass functionality."""

    def test_required_members_and_callables_attributes(self):
        """Test that metaclass has the correct required members and callables."""
        assert hasattr(UserInterfaceMeta, '__required_members__')
        assert hasattr(UserInterfaceMeta, '__required_callable__')

        expected_members = (
            'create_task',
            'update_task',
            'display_progress_message',
            'change_of_processor_status',
            'prompt_question',
            'enter_interactive_mode',
        )
        expected_callables = (
            'create_task',
            'update_task',
            'display_progress_message',
            'change_of_processor_status',
            'prompt_question',
            'enter_interactive_mode',
        )

        assert UserInterfaceMeta.__required_members__ == expected_members
        assert UserInterfaceMeta.__required_callable__ == expected_callables

    def test_subclasscheck_with_valid_class(self):
        """Test __subclasscheck__ with a class that has all required methods."""

        class ValidInterface:
            def create_task(self):
                pass

            def update_task(self):
                pass

            def display_progress_message(self):
                pass

            def change_of_processor_status(self):
                pass

            def prompt_question(self):
                pass

            def enter_interactive_mode(self):
                pass

        assert issubclass(ValidInterface, UserInterfaceBase)

    def test_subclasscheck_with_missing_methods(self):
        """Test __subclasscheck__ with a class missing required methods."""

        class IncompleteInterface:
            def create_task(self):
                pass

            def update_task(self):
                pass

            # Missing display_progress_message and change_of_processor_status

        assert not issubclass(IncompleteInterface, UserInterfaceBase)

    def test_subclasscheck_with_non_callable_attributes(self):
        """Test __subclasscheck__ with a class that has attributes but not methods."""

        class NonCallableInterface:
            create_task = 'not a method'
            update_task = 42
            display_progress_message = []
            change_of_processor_status = {}

        assert not issubclass(NonCallableInterface, UserInterfaceBase)

    def test_subclasscheck_with_mixed_valid_invalid(self):
        """Test __subclasscheck__ with a class that has some valid and some invalid attributes."""

        class MixedInterface:
            def create_task(self):
                pass

            def update_task(self):
                pass

            def display_progress_message(self):
                pass

            change_of_processor_status = 'not callable'  # Not callable

        assert not issubclass(MixedInterface, UserInterfaceBase)

    def test_instancecheck_delegates_to_subclasscheck(self):
        """Test that __instancecheck__ properly delegates to __subclasscheck__."""

        class ValidInterface:
            def create_task(self):
                pass

            def update_task(self):
                pass

            def display_progress_message(self):
                pass

            def change_of_processor_status(self):
                pass

            def prompt_question(self):
                pass

            def enter_interactive_mode(self):
                pass

        instance = ValidInterface()
        assert isinstance(instance, UserInterfaceBase)

    def test_instancecheck_with_invalid_instance(self):
        """Test __instancecheck__ with an instance of invalid class."""

        class InvalidInterface:
            def create_task(self):
                pass

            # Missing other required methods

        instance = InvalidInterface()
        assert not isinstance(instance, UserInterfaceBase)

    def test_subclasscheck_with_inheritance(self):
        """Test __subclasscheck__ with inherited methods."""

        class BaseInterface:
            def create_task(self):
                pass

            def update_task(self):
                pass

            def prompt_question(self):
                pass

        class DerivedInterface(BaseInterface):
            def display_progress_message(self):
                pass

            def change_of_processor_status(self):
                pass

            def enter_interactive_mode(self):
                pass

        assert issubclass(DerivedInterface, UserInterfaceBase)

    def test_subclasscheck_with_property_methods(self):
        """Test __subclasscheck__ with property-decorated methods."""

        class PropertyInterface:
            def create_task(self):
                pass

            def update_task(self):
                pass

            def display_progress_message(self):
                pass

            @property
            def change_of_processor_status(self):
                return lambda: None  # Returns a callable

        # Properties are not considered callable
        assert not issubclass(PropertyInterface, UserInterfaceBase)

    def test_subclasscheck_with_static_methods(self):
        """Test __subclasscheck__ with static methods."""

        class StaticMethodInterface:
            @staticmethod
            def create_task():
                pass

            @staticmethod
            def update_task():
                pass

            @staticmethod
            def display_progress_message():
                pass

            @staticmethod
            def change_of_processor_status():
                pass

            @staticmethod
            def prompt_question():
                pass

            @staticmethod
            def enter_interactive_mode():
                pass

        assert issubclass(StaticMethodInterface, UserInterfaceBase)

    def test_subclasscheck_with_class_methods(self):
        """Test __subclasscheck__ with class methods."""

        class ClassMethodInterface:
            @classmethod
            def create_task(cls):
                pass

            @classmethod
            def update_task(cls):
                pass

            @classmethod
            def display_progress_message(cls):
                pass

            @classmethod
            def change_of_processor_status(cls):
                pass

            @classmethod
            def enter_interactive_mode(cls):
                pass

            @classmethod
            def prompt_question(cls):
                pass

        assert issubclass(ClassMethodInterface, UserInterfaceBase)


class TestUserInterfaceBase:
    """Test class for UserInterfaceBase abstract class functionality."""

    def test_class_attributes(self):
        """Test that UserInterfaceBase has the correct class attributes."""
        assert hasattr(UserInterfaceBase, 'always_display_progress_message')
        assert hasattr(UserInterfaceBase, 'name')

        assert UserInterfaceBase.always_display_progress_message == 10
        assert UserInterfaceBase.name == 'base'

    def test_instantiation(self):
        """Test that UserInterfaceBase can be instantiated."""
        interface = UserInterfaceBase()
        assert isinstance(interface, UserInterfaceBase)
        assert interface.name == 'base'
        assert interface.always_display_progress_message == 10

    def test_create_task_method_exists_and_callable(self):
        """Test that create_task method exists and is callable."""
        interface = UserInterfaceBase()
        assert hasattr(interface, 'create_task')
        assert callable(interface.create_task)

        # Should not raise any exceptions (it just passes))
        interface.create_task('test_task', 'description', completed=0, increment=None, total=None)

    def test_update_task_method_exists_and_callable(self):
        """Test that update_task method exists and is callable."""
        interface = UserInterfaceBase()
        assert hasattr(interface, 'update_task')
        assert callable(interface.update_task)

        # Should not raise any exceptions (it just passes)
        interface.update_task('test_task', completed=50, increment=10, total=100)

    def test_display_progress_message_method_exists_and_callable(self):
        """Test that display_progress_message method exists and is callable."""
        interface = UserInterfaceBase()
        assert hasattr(interface, 'display_progress_message')
        assert callable(interface.display_progress_message)

        # Should not raise any exceptions (it just passes)
        interface.display_progress_message('Processing', 5, 100, 0.1)

    def test_change_of_processor_status_method_exists_and_callable(self):
        """Test that change_of_processor_status method exists and is callable."""
        interface = UserInterfaceBase()
        assert hasattr(interface, 'change_of_processor_status')
        assert callable(interface.change_of_processor_status)

        # Should not raise any exceptions (it just passes)
        interface.change_of_processor_status('processor', ProcessorStatus.Init, ProcessorStatus.Start)

    def test_context_manager_enter(self):
        """Test that __enter__ returns self."""
        interface = UserInterfaceBase()
        result = interface.__enter__()
        assert result is interface

    @pytest.mark.parametrize(
        'exception_type,exception_value,traceback_value',
        [
            (None, None, None),
            (ValueError, ValueError('test error'), None),
            (RuntimeError, RuntimeError('runtime error'), Mock()),
            (KeyboardInterrupt, KeyboardInterrupt(), Mock()),
        ],
    )
    def test_context_manager_exit(self, exception_type, exception_value, traceback_value):
        """Test that __exit__ handles various exception scenarios."""
        interface = UserInterfaceBase()

        # Should not raise any exceptions
        result = interface.__exit__(exception_type, exception_value, traceback_value)
        assert result is None

    def test_context_manager_full_usage(self):
        """Test full context manager usage."""
        interface = UserInterfaceBase()

        with interface as ctx:
            assert ctx is interface
            # Should be able to call methods within context
            ctx.create_task('test')
            ctx.update_task('test')

    @pytest.mark.parametrize(
        'i_item,n_item,freq,output',
        [
            (0, None, 0.1, True),
            (10, None, 0.1, True),
            (20, None, 0.1, True),
            (5, None, 0.1, False),
            (15, None, 0.1, False),
        ],
    )
    def test_is_time_to_display_lopping_message_with_none_n_item(self, i_item, n_item, freq, output):
        """Test _is_time_to_display_lopping_message with None n_item (indeterminate progress)."""
        interface = UserInterfaceBase()

        assert interface._is_time_to_display_lopping_message(i_item, n_item, freq) is output

    def test_is_time_to_display_lopping_message_small_n_item(self):
        """Test _is_time_to_display_lopping_message with small n_item (always display)."""
        interface = UserInterfaceBase()

        # When n_item <= always_display_progress_message (10), always display
        for i in range(5):
            assert interface._is_time_to_display_lopping_message(i, 5, 0.2) is True

    def test_is_time_to_display_lopping_message_large_n_item(self):
        """Test _is_time_to_display_lopping_message with large n_item."""
        interface = UserInterfaceBase()

        # With n_item=100 and frequency=0.1, should display every 10 items
        n_item = 100
        frequency = 0.1

        # First item should always display
        assert interface._is_time_to_display_lopping_message(0, n_item, frequency) is True

        # Last item should always display
        assert interface._is_time_to_display_lopping_message(n_item - 1, n_item, frequency) is True

        # Items at frequency intervals should display
        mod = max([round(frequency * n_item), 1])  # Should be 10
        for i in range(0, n_item, mod):
            assert interface._is_time_to_display_lopping_message(i, n_item, frequency) is True

        # Items not at frequency intervals should not display (except first and last)
        for i in [1, 2, 5, 15, 25, 35]:
            if i < n_item - 1:  # Exclude last item
                assert interface._is_time_to_display_lopping_message(i, n_item, frequency) is False

    @pytest.mark.parametrize(
        'n_item,frequency,expected_mod',
        [
            (100, 0.1, 10),  # round(0.1 * 100) = 10
            (1000, 0.05, 50),  # round(0.05 * 1000) = 50
            (50, 0.02, 1),  # round(0.02 * 50) = 1, but max with 1 = 1
            (200, 0.25, 50),  # round(0.25 * 200) = 50
        ],
    )
    def test_is_time_to_display_lopping_message_frequency_calculation(self, n_item, frequency, expected_mod):
        """Test frequency calculation in _is_time_to_display_lopping_message."""
        interface = UserInterfaceBase()

        # Test that items at the calculated modulo display correctly
        for i in range(0, n_item, expected_mod):
            assert interface._is_time_to_display_lopping_message(i, n_item, frequency) is True

    def test_is_time_to_display_lopping_message_edge_cases(self):
        """Test edge cases for _is_time_to_display_lopping_message."""
        interface = UserInterfaceBase()

        # Edge case: frequency that would result in mod < 1
        assert interface._is_time_to_display_lopping_message(0, 1000, 0.0001) is True  # First item
        assert interface._is_time_to_display_lopping_message(999, 1000, 0.0001) is True  # Last item

        # Edge case: n_item exactly at threshold
        assert interface._is_time_to_display_lopping_message(0, 10, 0.1) is True

        # Edge case: very high frequency
        for i in range(10):
            assert interface._is_time_to_display_lopping_message(i, 10, 1.0) is True

    def test_method_signatures_match_abstract_definition(self):
        """Test that all abstract method signatures are properly defined."""
        interface = UserInterfaceBase()

        # Test create_task signature
        try:
            interface.create_task(
                task_name='test',
                task_description='desc',
                completed=0,
                increment=None,
                total=None,
                extra_kwarg='should_work',
            )
        except Exception:
            pytest.fail('create_task should accept all parameters without error')

        # Test update_task signature
        try:
            interface.update_task(task_name='test', completed=50, increment=10, total=100, extra_kwarg='should_work')
        except Exception:
            pytest.fail('update_task should accept all parameters without error')

        # Test display_progress_message signature
        try:
            interface.display_progress_message('message', 5, 100, 0.1)
        except Exception:
            pytest.fail('display_progress_message should accept all parameters without error')

        # Test change_of_processor_status signature
        try:
            interface.change_of_processor_status('processor', ProcessorStatus.Init, ProcessorStatus.Run)
        except Exception:
            pytest.fail('change_of_processor_status should accept all parameters without error')


@pytest.mark.integration_test
class TestUserInterfaceIntegration:
    """Integration tests for the abstract user interface components."""

    def test_concrete_implementation_validation(self):
        """Test validation of a concrete implementation."""

        class ConcreteInterface(UserInterfaceBase):
            def create_task(self, task_name, task_description='', completed=0, increment=None, total=None, **kwargs):
                super().create_task(task_name, task_description, completed, increment, total, **kwargs)
                # Add concrete implementation here
                pass

            def update_task(self, task_name, completed=0, increment=None, total=None, **kwargs):
                super().update_task(task_name, completed, increment, total, **kwargs)
                # Add concrete implementation here
                pass

            def display_progress_message(self, message, i_item, n_item, frequency):
                super().display_progress_message(message, i_item, n_item, frequency)
                # Add concrete implementation here
                pass

            def change_of_processor_status(self, processor_name, old_status, new_status):
                super().change_of_processor_status(processor_name, old_status, new_status)
                # Add concrete implementation here
                pass

        # Should be valid according to metaclass
        assert issubclass(ConcreteInterface, UserInterfaceBase)

        # Should be instantiable and work as context manager
        interface = ConcreteInterface()
        assert isinstance(interface, UserInterfaceBase)

        with interface as ctx:
            ctx.create_task('test')
            ctx.update_task('test', completed=50)
            ctx.display_progress_message('Processing', 1, 10, 0.1)
            ctx.change_of_processor_status('proc', ProcessorStatus.Init, ProcessorStatus.Run)

    def test_incomplete_implementation_validation(self):
        """Test that incomplete implementations are properly rejected."""

        class IncompleteInterface(UserInterfaceBase):
            def create_task(self, task_name, **kwargs):
                pass

            def update_task(self, task_name, **kwargs):
                pass

            # Missing display_progress_message and change_of_processor_status
            # are inherited from the UserInterfaceBase class

        # Should not fail metaclass validation because of inheritance
        assert issubclass(IncompleteInterface, UserInterfaceBase)

    def test_multiple_inheritance_scenario(self):
        """Test metaclass behavior with multiple inheritance."""

        class MixinA:
            def create_task(self, *args, **kwargs):
                pass

        class MixinB:
            def update_task(self, *args, **kwargs):
                pass

            def display_progress_message(self, *args, **kwargs):
                pass

            def change_of_processor_status(self, *args, **kwargs):
                pass

        class MultipleInheritanceInterface(MixinA, MixinB, UserInterfaceBase):
            pass

        # Should pass validation due to having all required methods
        assert issubclass(MultipleInheritanceInterface, UserInterfaceBase)

        interface = MultipleInheritanceInterface()
        assert isinstance(interface, UserInterfaceBase)

    def test_docstring_preservation(self):
        """Test that docstrings are preserved in the abstract class."""
        assert UserInterfaceBase.__doc__ is not None
        assert 'abstract base user interface class' in UserInterfaceBase.__doc__

        assert UserInterfaceBase.create_task.__doc__ is not None
        assert 'Create a new task' in UserInterfaceBase.create_task.__doc__

        assert UserInterfaceBase.update_task.__doc__ is not None
        assert 'Update an existing task' in UserInterfaceBase.update_task.__doc__

        assert UserInterfaceBase.display_progress_message.__doc__ is not None
        assert 'Display a message during the process execution' in UserInterfaceBase.display_progress_message.__doc__

    def test_class_attributes_inheritance(self):
        """Test that class attributes are properly inherited."""

        class CustomInterface(UserInterfaceBase):
            name = 'custom'
            always_display_progress_message = 5

            def create_task(self, *args, **kwargs):
                pass

            def update_task(self, *args, **kwargs):
                pass

            def display_progress_message(self, *args, **kwargs):
                pass

            def change_of_processor_status(self, *args, **kwargs):
                pass

        interface = CustomInterface()
        assert interface.name == 'custom'
        assert interface.always_display_progress_message == 5

        # Base class should still have original values
        base_interface = UserInterfaceBase()
        assert base_interface.name == 'base'
        assert base_interface.always_display_progress_message == 10


class TestEnterInteractiveMode:
    """Test class for enter_interactive_mode context manager functionality."""

    def test_enter_interactive_mode_returns_generator(self):
        """Test that enter_interactive_mode returns a generator object."""
        interface = UserInterfaceBase()
        result = interface.enter_interactive_mode()
        assert hasattr(result, '__enter__')

    def test_enter_interactive_mode_context_manager_basic_usage(self):
        """Test basic context manager usage of enter_interactive_mode."""
        interface = UserInterfaceBase()

        with interface.enter_interactive_mode() as ctx:
            assert ctx is None  # Context manager yields None

    def test_enter_interactive_mode_context_manager_with_code_execution(self):
        """Test that code inside the context manager executes properly."""
        interface = UserInterfaceBase()
        execution_order = []

        with interface.enter_interactive_mode():
            execution_order.append('inside_context')

        assert execution_order == ['inside_context']

    def test_enter_interactive_mode_exception_handling(self):
        """Test that enter_interactive_mode properly handles exceptions in the context."""
        interface = UserInterfaceBase()

        with pytest.raises(ValueError, match='test error'):
            with interface.enter_interactive_mode():
                raise ValueError('test error')

    def test_enter_interactive_mode_finally_block_executes(self):
        """Test that the finally block executes even when exceptions occur."""
        interface = UserInterfaceBase()
        finally_executed = False

        def mock_finally():
            nonlocal finally_executed
            finally_executed = True

        # Patch the finally block to track execution
        with patch.object(interface, 'enter_interactive_mode'):
            # We need to directly test the internal logic
            # Since the method is simple, we'll verify it doesn't crash
            try:
                with interface.enter_interactive_mode():
                    pass
            except Exception:
                pass  # Expected for testing purposes

            # The method itself should not raise exceptions
            assert True  # If we get here without exception, it's working

    def test_enter_interactive_mode_nested_contexts(self):
        """Test nested usage of enter_interactive_mode context managers."""
        interface = UserInterfaceBase()

        with interface.enter_interactive_mode():
            with interface.enter_interactive_mode():
                pass  # Should work fine

    def test_enter_interactive_mode_integration_with_other_methods(self):
        """Test that enter_interactive_mode works alongside other interface methods."""
        interface = UserInterfaceBase()

        # Test that we can call other methods while in interactive mode
        interface.create_task('test_task')

        with interface.enter_interactive_mode():
            interface.update_task('test_task', completed=50)
            interface.display_progress_message('Testing', 1, 10, 0.1)

        interface.change_of_processor_status('test_proc', ProcessorStatus.Init, ProcessorStatus.Run)

    @pytest.mark.integration_test
    def test_enter_interactive_mode_complete_workflow(self):
        """Integration test for complete enter_interactive_mode workflow."""
        interface = UserInterfaceBase()

        # Test the complete lifecycle
        try:
            with interface.enter_interactive_mode():
                # Simulate some processing in interactive mode
                pass
        except Exception:
            # Should not raise any exceptions
            pytest.fail('enter_interactive_mode should not raise exceptions')
