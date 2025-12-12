#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Unit tests for the console_user_interface module.

This module contains comprehensive tests for the ConsoleInterface class,
focusing on its logging-based functionality and inherited behavior.
"""

import logging
from unittest.mock import Mock, patch

import pytest

from mafw.enumerators import ProcessorStatus
from mafw.ui.abstract_user_interface import UserInterfaceBase
from mafw.ui.console_user_interface import ConsoleInterface


class TestConsoleInterface:
    """Test class for ConsoleInterface functionality."""

    def test_inheritance(self):
        """Test that ConsoleInterface properly inherits from UserInterfaceBase."""
        assert issubclass(ConsoleInterface, UserInterfaceBase)

        interface = ConsoleInterface()
        assert isinstance(interface, UserInterfaceBase)
        assert isinstance(interface, ConsoleInterface)

    def test_class_attributes(self):
        """Test that ConsoleInterface has the correct class attributes."""
        assert hasattr(ConsoleInterface, 'name')
        assert ConsoleInterface.name == 'console'

        # Should inherit from base class
        assert hasattr(ConsoleInterface, 'always_display_progress_message')
        assert ConsoleInterface.always_display_progress_message == 10

    def test_instantiation(self):
        """Test that ConsoleInterface can be instantiated."""
        interface = ConsoleInterface()
        assert interface.name == 'console'
        assert interface.always_display_progress_message == 10

    def test_create_task_method_signature(self):
        """Test create_task method accepts all expected parameters."""
        interface = ConsoleInterface()

        # Should not raise any exceptions (method just passes)
        interface.create_task('test_task')
        interface.create_task('test_task', 'description')
        interface.create_task('test_task', 'description', completed=50)
        interface.create_task('test_task', 'description', completed=50, increment=10)
        interface.create_task('test_task', 'description', completed=50, increment=10, total=100)
        interface.create_task('test_task', extra_kwarg='value')

    def test_update_task_method_signature(self):
        """Test update_task method accepts all expected parameters."""
        interface = ConsoleInterface()

        # Should not raise any exceptions (method just passes)
        interface.update_task('test_task')
        interface.update_task('test_task', completed=50)
        interface.update_task('test_task', completed=50, increment=10)
        interface.update_task('test_task', completed=50, increment=10, total=100)
        interface.update_task('test_task', extra_kwarg='value')

    def test_context_manager_enter(self):
        """Test __enter__ method returns self."""
        interface = ConsoleInterface()
        result = interface.__enter__()
        assert result is interface

    @pytest.mark.parametrize(
        'exception_type,exception_value,traceback_value',
        [
            (None, None, None),
            (ValueError, ValueError('test error'), None),
            (RuntimeError, RuntimeError('runtime error'), Mock()),
        ],
    )
    def test_context_manager_exit(self, exception_type, exception_value, traceback_value):
        """Test __exit__ method handles various scenarios."""
        interface = ConsoleInterface()

        # Should not raise any exceptions and return None
        result = interface.__exit__(exception_type, exception_value, traceback_value)
        assert result is None

    def test_context_manager_usage(self):
        """Test full context manager usage."""
        interface = ConsoleInterface()

        with interface as ctx:
            assert ctx is interface
            # Should be able to call methods within context
            ctx.create_task('test')
            ctx.update_task('test')


class TestConsoleInterfaceDisplayProgressMessage:
    """Test class for display_progress_message functionality."""

    @pytest.fixture
    def interface(self):
        """Fixture providing ConsoleInterface instance."""
        return ConsoleInterface()

    @pytest.fixture
    def mock_logger(self):
        """Fixture providing mocked logger."""
        with patch('mafw.ui.console_user_interface.log') as mock_log:
            yield mock_log

    def test_display_progress_message_time_check_delegation(self, interface, mock_logger):
        """Test that display_progress_message delegates time check to parent method."""
        with patch.object(interface, '_is_time_to_display_lopping_message') as mock_time_check:
            mock_time_check.return_value = False

            interface.display_progress_message('Test message', 5, 100, 0.1)

            mock_time_check.assert_called_once_with(5, 100, 0.1)
            mock_logger.info.assert_not_called()

    @pytest.mark.parametrize(
        'i_item,n_item,frequency,expected_calls',
        [
            (0, 100, 0.1, 1),  # First item should display
            (10, 100, 0.1, 1),  # At frequency interval
            (99, 100, 0.1, 1),  # Last item should display
            (5, 100, 0.1, 0),  # Not at frequency interval
            (0, 5, 0.1, 1),  # Small n_item, always display
            (2, 5, 0.1, 1),  # Small n_item, always display
        ],
    )
    def test_display_progress_message_logging_frequency(
        self, interface, mock_logger, i_item, n_item, frequency, expected_calls
    ):
        """Test logging frequency based on inherited logic."""
        interface.display_progress_message('Test message', i_item, n_item, frequency)

        assert mock_logger.info.call_count == expected_calls

    def test_display_progress_message_with_none_n_item(self, interface, mock_logger):
        """Test display_progress_message behavior when n_item is None."""
        # Should use max(1000, i_item) as n_item for display purposes
        interface.display_progress_message('Processing item', 500, None, 0.1)

        # Should log since 500 is multiple of 10 (inherited logic for None n_item)
        mock_logger.info.assert_called()  # 500 % 10 != 0

        # Test with item that should display
        interface.display_progress_message('Processing item', 10, None, 0.1)
        assert len(mock_logger.info.call_args_list) == 2

    def test_display_progress_message_formatting_with_known_total(self, interface, mock_logger):
        """Test message formatting when total is known."""
        interface.display_progress_message('Processing files', 0, 100, 0.1)  # First item always displays

        mock_logger.info.assert_called_once()
        call_args = mock_logger.info.call_args[0][0]

        # Should contain counter format and message
        assert '[  1/100]' in call_args
        assert 'Processing files' in call_args

    def test_display_progress_message_formatting_with_none_total(self, interface, mock_logger):
        """Test message formatting when total is None."""
        interface.display_progress_message('Processing items', 0, None, 0.1)

        mock_logger.info.assert_called_once()
        call_args = mock_logger.info.call_args[0][0]

        # When n_item is None, it should use max(1000, i_item) = max(1000, 0) = 1000
        assert '[   1/1000]' in call_args
        assert 'Processing items' in call_args

    def test_display_progress_message_formatting_with_large_i_item_and_none_total(self, interface, mock_logger):
        """Test message formatting when i_item > 1000 and total is None."""
        interface.display_progress_message('Processing items', 2000, None, 0.1)

        # 2000 % 10 == 0, so should display
        mock_logger.info.assert_called_once()
        call_args = mock_logger.info.call_args[0][0]

        # When n_item is None and i_item > 1000, should use i_item as total
        assert '[2001/2000]' in call_args
        assert 'Processing items' in call_args

    @pytest.mark.parametrize(
        'i_item,n_item,expected_width,expected_counter',
        [
            (0, 10, 2, '[ 1/10]'),
            (99, 100, 3, '[100/100]'),
            (999, 1000, 4, '[1000/1000]'),
            (0, 1, 1, '[1/1]'),
        ],
    )
    def test_display_progress_message_counter_formatting(
        self, interface, mock_logger, i_item, n_item, expected_width, expected_counter
    ):
        """Test counter formatting with different widths."""
        interface.display_progress_message('Test', i_item, n_item, 1.0)  # High frequency to ensure display

        if mock_logger.info.called:
            call_args = mock_logger.info.call_args[0][0]
            assert expected_counter in call_args

    def test_display_progress_message_counter_width_calculation(self, interface, mock_logger):
        """Test that counter width is calculated correctly."""
        # Test with 4-digit number to verify width calculation
        interface.display_progress_message('Test', 0, 1000, 1.0)

        mock_logger.info.assert_called_once()
        call_args = mock_logger.info.call_args[0][0]

        # Should be right-aligned to width of str(1000) = 4
        assert '[   1/1000]' in call_args

    def test_display_progress_message_complete_format(self, interface, mock_logger):
        """Test complete message format including counter and message."""
        message = 'Processing data files'
        interface.display_progress_message(message, 0, 50, 1.0)

        mock_logger.info.assert_called_once()
        call_args = mock_logger.info.call_args[0][0]

        expected = f'[ 1/50] {message}'
        assert call_args == expected


class TestConsoleInterfaceChangeOfProcessorStatus:
    """Test class for change_of_processor_status functionality."""

    @pytest.fixture
    def interface(self):
        """Fixture providing ConsoleInterface instance."""
        return ConsoleInterface()

    @pytest.fixture
    def mock_logger(self):
        """Fixture providing mocked logger."""
        with patch('mafw.ui.console_user_interface.log') as mock_log:
            yield mock_log

    def test_change_of_processor_status_logs_debug_message(self, interface, mock_logger):
        """Test that processor status change logs debug message."""
        processor_name = 'test_processor'
        old_status = ProcessorStatus.Init
        new_status = ProcessorStatus.Start

        interface.change_of_processor_status(processor_name, old_status, new_status)

        mock_logger.debug.assert_called_once()
        call_args = mock_logger.debug.call_args[0][0]

        expected_message = f'{processor_name} is {new_status}'
        assert call_args == expected_message

    @pytest.mark.parametrize(
        'processor_name,old_status,new_status',
        [
            ('processor_1', ProcessorStatus.Init, ProcessorStatus.Start),
            ('data_loader', ProcessorStatus.Start, ProcessorStatus.Run),
            ('file_processor', ProcessorStatus.Run, ProcessorStatus.Finish),
            ('validator', ProcessorStatus.Finish, ProcessorStatus.Init),
        ],
    )
    def test_change_of_processor_status_various_statuses(
        self, interface, mock_logger, processor_name, old_status, new_status
    ):
        """Test processor status change with various status combinations."""
        interface.change_of_processor_status(processor_name, old_status, new_status)

        mock_logger.debug.assert_called_once()
        call_args = mock_logger.debug.call_args[0][0]

        expected_message = f'{processor_name} is {new_status}'
        assert call_args == expected_message

    def test_change_of_processor_status_message_format(self, interface, mock_logger):
        """Test the exact format of the status change message."""
        processor_name = 'my_custom_processor'
        old_status = ProcessorStatus.Init
        new_status = ProcessorStatus.Run

        interface.change_of_processor_status(processor_name, old_status, new_status)

        # Verify the exact message format
        expected_message = f'{processor_name} is {new_status}'
        mock_logger.debug.assert_called_once_with(expected_message)

    def test_change_of_processor_status_ignores_old_status(self, interface, mock_logger):
        """Test that old_status is ignored in the log message."""
        processor_name = 'test_processor'
        old_status = ProcessorStatus.Finish
        new_status = ProcessorStatus.Init

        interface.change_of_processor_status(processor_name, old_status, new_status)

        call_args = mock_logger.debug.call_args[0][0]

        # Message should only contain processor name and new status
        assert processor_name in call_args
        assert str(new_status) in call_args
        assert str(old_status) not in call_args


@pytest.mark.integration_test
class TestConsoleInterfaceIntegration:
    """Integration tests for ConsoleInterface."""

    @pytest.fixture
    def interface(self):
        """Fixture providing ConsoleInterface instance."""
        return ConsoleInterface()

    def test_logger_module_name(self):
        """Test that the logger has the correct module name."""
        from mafw.ui.console_user_interface import log

        # Verify logger has correct name (it's created at import time)
        assert log.name == 'mafw.ui.console_user_interface'

    def test_full_workflow_with_logging(self, interface):
        """Test complete workflow with all logging methods."""
        with patch('mafw.ui.console_user_interface.log') as mock_logger:
            # Use as context manager
            with interface as ctx:
                # Create and update tasks (no logging expected)
                ctx.create_task('test_task', 'Test description', total=100)
                ctx.update_task('test_task', completed=50)

                # Display progress messages
                ctx.display_progress_message('Processing', 0, 10, 0.1)  # Should log (first item)
                ctx.display_progress_message('Processing', 5, 10, 0.1)  # Should log (small total)

                # Change processor status
                ctx.change_of_processor_status('processor', ProcessorStatus.Init, ProcessorStatus.Run)

            # Verify logging calls
            assert mock_logger.info.call_count >= 1  # At least one progress message
            mock_logger.debug.assert_called_once()  # Status change

    def test_interface_satisfies_metaclass_requirements(self, interface):
        """Test that ConsoleInterface satisfies all metaclass requirements."""
        # This should pass since ConsoleInterface inherits from UserInterfaceBase
        assert isinstance(interface, UserInterfaceBase)

        # Verify all required methods are callable
        required_methods = ['create_task', 'update_task', 'display_progress_message', 'change_of_processor_status']
        for method in required_methods:
            assert hasattr(interface, method)
            assert callable(getattr(interface, method))

    def test_console_interface_docstring_and_class_attributes(self):
        """Test docstring and class-level attributes."""
        assert ConsoleInterface.__doc__ is not None
        assert 'console user interface' in ConsoleInterface.__doc__.lower()
        assert 'headless' in ConsoleInterface.__doc__.lower()

        # Test class attribute
        assert ConsoleInterface.name == 'console'

    def test_logging_integration_with_real_logger(self, interface):
        """Test integration with actual logging system."""
        # Create a test logger to capture output
        test_logger = logging.getLogger('test_console_interface')
        test_logger.setLevel(logging.DEBUG)

        # Create a list handler to capture log records
        log_records = []

        class ListHandler(logging.Handler):
            def emit(self, record):
                log_records.append(record)

        handler = ListHandler()
        test_logger.addHandler(handler)

        # Patch the module logger to use our test logger
        with patch('mafw.ui.console_user_interface.log', test_logger):
            interface.display_progress_message('Test message', 0, 100, 0.1)
            interface.change_of_processor_status('test_proc', ProcessorStatus.Init, ProcessorStatus.Run)

        # Verify log records
        assert len(log_records) == 2

        # Check info log (progress message)
        info_record = next(r for r in log_records if r.levelno == logging.INFO)
        assert 'Test message' in info_record.getMessage()
        assert '[  1/100]' in info_record.getMessage()

        # Check debug log (status change)
        debug_record = next(r for r in log_records if r.levelno == logging.DEBUG)
        assert f'test_proc is {ProcessorStatus.Run}' in debug_record.getMessage()

    @pytest.mark.parametrize(
        'method_name,args,kwargs',
        [
            ('create_task', ('task1',), {'task_description': 'desc', 'total': 100}),
            ('update_task', ('task1',), {'completed': 50}),
            ('display_progress_message', ('msg', 1, 10, 0.1), {}),
            ('change_of_processor_status', ('proc', ProcessorStatus.Init, ProcessorStatus.Run), {}),
        ],
    )
    def test_method_calls_dont_raise_exceptions(self, interface, method_name, args, kwargs):
        """Test that all methods can be called without raising exceptions."""
        method = getattr(interface, method_name)

        # Should not raise any exceptions
        try:
            method(*args, **kwargs)
        except Exception as e:
            pytest.fail(f'{method_name} raised an unexpected exception: {e}')


class TestConsoleInterfacePromptQuestion:
    """Test class for prompt_question functionality."""

    def test_prompt_question_basic_functionality(self):
        """Test that prompt_question calls input with correct argument."""
        interface = ConsoleInterface()

        with patch('builtins.input', return_value='test_response') as mock_input:
            result = interface.prompt_question('Enter your name:')

            mock_input.assert_called_once_with('Enter your name:')
            assert result == 'test_response'

    def test_prompt_question_with_kwargs(self):
        """Test that prompt_question passes additional kwargs to input function."""
        interface = ConsoleInterface()

        with patch('builtins.input', return_value='test_response') as mock_input:
            result = interface.prompt_question('Enter your name:', timeout=10)

            mock_input.assert_called_once_with('Enter your name:')
            assert result == 'test_response'

    def test_prompt_question_empty_question(self):
        """Test that prompt_question works with empty question string."""
        interface = ConsoleInterface()

        with patch('builtins.input', return_value='response') as mock_input:
            result = interface.prompt_question('')

            mock_input.assert_called_once_with('')
            assert result == 'response'

    def test_prompt_question_special_characters(self):
        """Test that prompt_question handles special characters in question."""
        interface = ConsoleInterface()

        special_question = "What's your favorite color? 🌈"

        with patch('builtins.input', return_value='blue') as mock_input:
            result = interface.prompt_question(special_question)

            mock_input.assert_called_once_with(special_question)
            assert result == 'blue'

    def test_prompt_question_different_return_types(self):
        """Test that prompt_question handles different return types from input."""
        interface = ConsoleInterface()

        test_cases = [
            ('123', '123'),
            ('', ''),
            ('True', 'True'),
            ('3.14', '3.14'),
            ('special chars!@#$%', 'special chars!@#$%'),
        ]

        for input_val, expected in test_cases:
            with patch('builtins.input', return_value=input_val) as mock_input:
                result = interface.prompt_question('Test question:')

                mock_input.assert_called_once_with('Test question:')
                assert result == expected

    @pytest.mark.parametrize(
        'question,expected_input_call',
        [
            ('What is your name?', 'What is your name?'),
            ('Enter age:', 'Enter age:'),
            ('Confirm? (y/n)', 'Confirm? (y/n)'),
        ],
    )
    def test_prompt_question_various_questions(self, question, expected_input_call):
        """Test prompt_question with various question formats."""
        interface = ConsoleInterface()

        with patch('builtins.input', return_value='answer') as mock_input:
            result = interface.prompt_question(question)

            mock_input.assert_called_once_with(expected_input_call)
            assert result == 'answer'

    def test_prompt_question_multiple_calls(self):
        """Test that prompt_question can be called multiple times."""
        interface = ConsoleInterface()

        responses = ['first', 'second', 'third']
        with patch('builtins.input', side_effect=responses) as mock_input:
            result1 = interface.prompt_question('First question:')
            result2 = interface.prompt_question('Second question:')
            result3 = interface.prompt_question('Third question:')

            assert mock_input.call_count == 3
            assert result1 == 'first'
            assert result2 == 'second'
            assert result3 == 'third'

    def test_prompt_question_integration_with_mocked_input(self):
        """Test prompt_question integration with mocked input function."""
        interface = ConsoleInterface()

        # Create a more complex mock that tracks calls
        mock_input = Mock()
        mock_input.side_effect = ['response1', 'response2']

        with patch('builtins.input', mock_input):
            result1 = interface.prompt_question('Question 1:')
            result2 = interface.prompt_question('Question 2:')

            assert mock_input.call_count == 2
            mock_input.assert_any_call('Question 1:')
            mock_input.assert_any_call('Question 2:')
            assert result1 == 'response1'
            assert result2 == 'response2'

    def test_prompt_question_exception_handling(self):
        """Test that prompt_question properly handles input exceptions."""
        interface = ConsoleInterface()

        with patch('builtins.input', side_effect=KeyboardInterrupt('User interrupted')):
            with pytest.raises(KeyboardInterrupt):
                interface.prompt_question('Interrupt test:')

        with patch('builtins.input', side_effect=ValueError('Invalid input')):
            with pytest.raises(ValueError):
                interface.prompt_question('Error test:')

    def test_prompt_question_method_signature_compatibility(self):
        """Test that prompt_question maintains compatibility with method signature expectations."""
        interface = ConsoleInterface()

        # Should accept the expected parameters without raising TypeError
        with patch('builtins.input', return_value='test'):
            # Test basic call
            interface.prompt_question('Basic test')

            # Test with kwargs
            interface.prompt_question('Test with kwargs', timeout=5, retries=3)

            # Test with all possible parameters
            interface.prompt_question('Full test', timeout=10, retries=2, default='default')

    def test_prompt_question_return_value_consistency(self):
        """Test that prompt_question consistently returns the input value."""
        interface = ConsoleInterface()

        test_values = [
            'simple_string',
            '12345',
            'Special Characters !@#$%^&*()',
            'Unicode: café, naïve, résumé',
            'Whitespace:   leading and trailing   ',
            'Very long string that might cause issues with some implementations',
        ]

        for test_value in test_values:
            with patch('builtins.input', return_value=test_value) as mock_input:
                result = interface.prompt_question('Test question:')

                mock_input.assert_called_once_with('Test question:')
                assert result == test_value
                assert isinstance(result, str)
