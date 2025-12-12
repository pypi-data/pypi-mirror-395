#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Unit tests for the timer module.
"""

from time import sleep
from unittest.mock import MagicMock, call, patch

import pytest

from mafw.timer import Timer, pretty_format_duration, rreplace


class TestPrettyFormatDuration:
    """Test class for the pretty_format_duration function."""

    @pytest.mark.parametrize(
        'duration_s,n_digits,expected',
        [
            # Test various time durations
            (0.0, 1, '< 0.0 seconds'),
            (0.5, 1, '0.5 seconds'),
            (1.0, 1, '1.0 second'),
            (2.5, 1, '2.5 seconds'),
            (60.0, 1, '1 minute'),
            (61.0, 1, '1 minute and 1.0 second'),
            (62.5, 1, '1 minute and 2.5 seconds'),
            (120.0, 1, '2 minutes'),
            (3600.0, 1, '1 hour'),
            (3661.0, 1, '1 hour, 1 minute and 1.0 second'),
            (7322.5, 1, '2 hours, 2 minutes and 2.5 seconds'),
            (86400.0, 1, '1 day'),
            (90061.0, 1, '1 day, 1 hour, 1 minute and 1.0 second'),
            (172800.0, 1, '2 days'),
            # Test different precision
            (1.23456, 2, '1.23 seconds'),
            (1.23456, 3, '1.235 seconds'),
            # Test edge cases
            (0.001, 1, '< 0.0 seconds'),  # Very small duration
        ],
    )
    def test_pretty_format_duration_parametrized(self, duration_s, n_digits, expected):
        """Test pretty_format_duration with various inputs."""
        result = pretty_format_duration(duration_s, n_digits)
        assert result == expected

    def test_pretty_format_with_negative_duration(self):
        with pytest.raises(ValueError, match='cannot be a negative value'):
            pretty_format_duration(-1, 2)

    def test_pretty_format_with_negative_n_digits(self):
        with pytest.raises(ValueError, match='cannot be a negative value'):
            pretty_format_duration(121, -2)

    def test_pretty_format_duration_default_digits(self):
        """Test pretty_format_duration with default n_digits parameter."""
        result = pretty_format_duration(1.5)
        assert result == '1.5 seconds'

    def test_pretty_format_duration_microseconds(self):
        """Test pretty_format_duration with microseconds."""
        # Test with a duration that has microseconds
        result = pretty_format_duration(1.000001, 6)
        assert result == '1.000001 seconds'


class TestRreplace:
    """Test class for the rreplace function."""

    @pytest.mark.parametrize(
        'inp_string,old_string,new_string,counts,expected',
        [
            # Basic replacements
            ('hello world world', 'world', 'python', 1, 'hello world python'),
            ('hello world world', 'world', 'python', 2, 'hello python python'),
            ('a,b,c,d', ',', ' and ', 1, 'a,b,c and d'),
            ('test,test,test', 'test', 'case', 2, 'test,case,case'),
            # Edge cases
            ('hello', 'world', 'python', 1, 'hello'),  # substring not found
            ('', 'test', 'case', 1, ''),  # empty string
            ('testtest', 'test', '', 1, 'test'),  # empty new_string
            # # Zero counts
            ('hello world', 'world', 'python', 0, 'hello world'),
            # # Multiple occurrences
            ('a b a b a', 'a', 'x', 2, 'a b x b x'),
        ],
    )
    def test_rreplace_parametrized(self, inp_string, old_string, new_string, counts, expected):
        """Test rreplace function with various inputs."""
        result = rreplace(inp_string, old_string, new_string, counts)
        assert result == expected

    def test_rreplace_empty_old_string(self):
        with pytest.raises(ValueError, match='old_string cannot be empty'):
            rreplace('any string', '', 'whatever', 1)

    def test_rreplace_complex_strings(self):
        """Test rreplace with more complex string patterns."""
        # Test with longer patterns
        inp = 'the quick brown fox jumps over the lazy dog the end'
        result = rreplace(inp, 'the', 'a', 2)
        expected = 'the quick brown fox jumps over a lazy dog a end'
        assert result == expected


class TestTimer:
    """Test class for the Timer class."""

    def test_timer_initialization_default(self):
        """Test Timer initialization with default parameters."""
        timer = Timer()
        assert timer._suppress_message is False
        assert timer.start == 0.0
        assert timer.end == 0.0

    def test_timer_initialization_suppress_message(self):
        """Test Timer initialization with suppress_message=True."""
        timer = Timer(suppress_message=True)
        assert timer._suppress_message is True
        assert timer.start == 0.0
        assert timer.end == 0.0

    @patch('mafw.timer.perf_counter')
    def test_timer_context_manager_enter(self, mock_perf_counter):
        """Test Timer context manager __enter__ method."""
        mock_perf_counter.return_value = 123.456

        timer = Timer()
        result = timer.__enter__()

        assert result is timer
        assert timer.start == 123.456
        assert timer.end == 0.0
        mock_perf_counter.assert_called_once()

    @patch('mafw.timer.perf_counter')
    @patch('mafw.timer.logging.getLogger')
    def test_timer_context_manager_exit_with_logging(self, mock_get_logger, mock_perf_counter):
        """Test Timer context manager __exit__ method with logging enabled."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_perf_counter.side_effect = [100.0, 103.5]  # start, end times

        timer = Timer(suppress_message=False)
        timer.__enter__()
        timer.__exit__(None, None, None)

        assert timer.end == 103.5
        mock_logger.info.assert_called_once()
        # Verify the log message format
        call_args = mock_logger.info.call_args[0][0]
        assert 'Total execution time:' in call_args

    @patch('mafw.timer.perf_counter')
    @patch('mafw.timer.logging.getLogger')
    def test_timer_context_manager_exit_suppressed(self, mock_get_logger, mock_perf_counter):
        """Test Timer context manager __exit__ method with logging suppressed."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_perf_counter.side_effect = [100.0, 103.5]

        timer = Timer(suppress_message=True)
        timer.__enter__()
        timer.__exit__(None, None, None)

        assert timer.end == 103.5
        mock_logger.info.assert_not_called()

    @patch('mafw.timer.perf_counter')
    def test_timer_context_manager_exit_with_exception(self, mock_perf_counter):
        """Test Timer context manager __exit__ method when called with exception parameters."""
        mock_perf_counter.side_effect = [100.0, 103.5]

        timer = Timer(suppress_message=True)
        timer.__enter__()

        # Simulate exit with exception
        exception_type = ValueError
        exception_value = ValueError('test error')
        traceback = None

        timer.__exit__(exception_type, exception_value, traceback)

        assert timer.end == 103.5

    @patch('mafw.timer.perf_counter')
    def test_timer_duration_property(self, mock_perf_counter):
        """Test Timer duration property."""
        mock_perf_counter.side_effect = [100.0, 103.5]

        timer = Timer()
        timer.__enter__()
        timer.__exit__(None, None, None)

        assert timer.duration == 3.5

    @patch('mafw.timer.perf_counter')
    @patch('mafw.timer.pretty_format_duration')
    @pytest.mark.parametrize('suppress,num_calls', [(True, 1), (False, 2)])
    def test_timer_format_duration(self, mock_pretty_format, mock_perf_counter, suppress, num_calls):
        """Test Timer format_duration method."""
        mock_perf_counter.side_effect = [100.0, 103.5]
        mock_pretty_format.return_value = '3.5 seconds'

        timer = Timer(suppress_message=suppress)
        timer.__enter__()
        timer.__exit__(None, None, None)

        result = timer.format_duration()

        assert result == '3.5 seconds'
        if suppress:
            mock_pretty_format.assert_called_once_with(3.5)
        else:
            call_list = mock_pretty_format.call_args_list
            assert len(call_list) == 2
            assert call_list == [call(3.5) for i in call_list]

    def test_timer_context_manager_integration(self):
        """Test Timer as context manager with actual timing (integration test)."""
        with Timer(suppress_message=True) as timer:
            sleep(0.01)  # Sleep for 10ms

        # Verify that duration is reasonable (should be at least 10ms)
        assert timer.duration >= 0.01
        assert timer.start > 0
        assert timer.end > timer.start

    @patch('mafw.timer.logging.getLogger')
    def test_timer_logging_integration(self, mock_get_logger):
        """Test Timer logging integration."""
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        with Timer(suppress_message=False):
            sleep(0.001)  # Very short sleep

        # Verify logger was called
        mock_get_logger.assert_called_with('mafw.timer')
        mock_logger.info.assert_called_once()

    def test_timer_duration_before_exit(self):
        """Test Timer duration calculation before context manager exit."""
        timer = Timer()
        timer.start = 100.0
        timer.end = 0.0

        # Duration should be negative when end hasn't been set
        assert timer.duration == -100.0

    @pytest.mark.parametrize('suppress_message', [True, False])
    def test_timer_suppress_message_parameter(self, suppress_message):
        """Test Timer with different suppress_message values."""
        timer = Timer(suppress_message=suppress_message)
        assert timer._suppress_message == suppress_message


class TestTimerEdgeCases:
    """Test class for Timer edge cases and error conditions."""

    @patch('mafw.timer.perf_counter')
    def test_timer_zero_duration(self, mock_perf_counter):
        """Test Timer with zero duration."""
        mock_perf_counter.return_value = 100.0  # Same start and end time

        timer = Timer(suppress_message=True)
        timer.__enter__()
        timer.__exit__(None, None, None)

        assert timer.duration == 0.0

    @patch('mafw.timer.perf_counter')
    def test_timer_negative_duration(self, mock_perf_counter):
        """Test Timer with negative duration (edge case)."""
        mock_perf_counter.side_effect = [100.0, 99.0]  # end < start

        timer = Timer(suppress_message=True)
        timer.__enter__()
        timer.__exit__(None, None, None)

        assert timer.duration == -1.0

    def test_timer_manual_start_end_modification(self):
        """Test Timer with manually modified start and end times."""
        timer = Timer()
        timer.start = 50.0
        timer.end = 75.5

        assert timer.duration == 25.5
        assert '25.5 seconds' in timer.format_duration()
