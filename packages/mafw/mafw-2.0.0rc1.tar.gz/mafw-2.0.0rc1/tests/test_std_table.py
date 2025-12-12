#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Test suite for the std_tables module.

This module contains unit tests for the classes and methods defined in the std_tables module.
The tests are grouped into classes corresponding to the classes in std_tables.py and use
pytest for testing. The tests are designed to achieve at least 90% coverage.
"""

from types import TracebackType
from typing import Optional, Type
from unittest.mock import Mock, patch

import pytest
from peewee import SqliteDatabase

from mafw.db.db_configurations import default_conf
from mafw.db.db_model import database_proxy
from mafw.db.std_tables import OrphanFile, PlotterOutput, TriggerDisabler, TriggerStatus


# Setup an in-memory SQLite database for testing
@pytest.fixture(scope='class')
def db():
    """
    Fixture to set up a mock database for testing.

    :return: A peewee database instance for testing.
    """
    test_db = SqliteDatabase(':memory:', pragmas=default_conf['sqlite']['pragmas'])
    database_proxy.initialize(test_db)
    test_db.bind([TriggerStatus, OrphanFile, PlotterOutput], bind_refs=False, bind_backrefs=False)
    test_db.connect()
    test_db.create_tables([TriggerStatus, OrphanFile, PlotterOutput])
    yield test_db
    test_db.drop_tables([TriggerStatus, OrphanFile, PlotterOutput])
    test_db.close()


class TestTriggerStatus:
    """
    Tests for the TriggerStatus model.
    """

    def test_trigger_status_initialization(self, db):
        """
        Test the initialization of the TriggerStatus table.
        """
        TriggerStatus.init()
        triggers = TriggerStatus.select()
        assert len(triggers) == 4

    def test_trigger_status_fields(self, db):
        """
        Test the fields of the TriggerStatus model.
        """
        trigger = TriggerStatus.create(trigger_type='INSERT', status=True)
        assert trigger.trigger_type == 'INSERT'
        assert trigger.status is True


class TestOrphanFile:
    """
    Tests for the OrphanFile model.
    """

    def test_orphan_file_creation(self, db):
        """
        Test the creation of an OrphanFile entry.
        """
        orphan_file = OrphanFile.create(filenames=['path/to/file'], checksum='dummychecksum')
        assert orphan_file.filenames == ['path/to/file']
        assert orphan_file.checksum == 'dummychecksum'


class TestPlotterOutput:
    """
    Tests for the PlotterOutput model.
    """

    def test_plotter_output_creation(self, db):
        """
        Test the creation of a PlotterOutput entry.
        """
        plotter_output = PlotterOutput.create(
            plotter_name='TestPlotter', filename_list=['output/file'], checksum='outputchecksum'
        )
        assert plotter_output.plotter_name == 'TestPlotter'
        assert plotter_output.filename_list == ['output/file']
        assert plotter_output.checksum == 'outputchecksum'

    def test_plotter_output_triggers(self, db):
        """
        Test the triggers of the PlotterOutput model.
        """
        TriggerStatus.init()
        orphan_files = OrphanFile.select().where(OrphanFile.checksum == 'outputchecksum2')
        assert len(orphan_files) == 0
        plotter_output = PlotterOutput.create(
            plotter_name='TestPlotter2', filename_list=['output/file.txt'], checksum='outputchecksum2'
        )
        plotter_output.delete_instance()
        orphan_files = OrphanFile.select().where(OrphanFile.checksum == 'outputchecksum2')
        assert len(orphan_files) == 1


class TestTriggerDisabler:
    """Test suite for TriggerDisabler class."""

    @pytest.fixture
    def mock_trigger_status(self):
        """Mock the TriggerStatus model to avoid database interactions."""
        with patch('mafw.db.std_tables.TriggerStatus') as mock:
            # Mock the update query chain
            mock_update = Mock()
            mock_where = Mock()
            mock_execute = Mock()

            mock.update.return_value = mock_update
            mock_update.where.return_value = mock_where
            mock_where.execute.return_value = mock_execute

            yield mock

    @pytest.fixture
    def trigger_disabler(self):
        """Create a TriggerDisabler instance for testing."""
        return TriggerDisabler(trigger_type_id=1)

    @pytest.mark.parametrize('trigger_type_id', [1, 5, 10, 999])
    def test_init_with_different_trigger_type_ids(self, trigger_type_id):
        """Test initialization with various trigger type IDs."""
        disabler = TriggerDisabler(trigger_type_id)
        assert disabler.trigger_type_id == trigger_type_id

    @pytest.mark.parametrize('trigger_type_id', [0, -1, -999])
    def test_init_with_edge_case_trigger_type_ids(self, trigger_type_id):
        """Test initialization with edge case trigger type IDs."""
        disabler = TriggerDisabler(trigger_type_id)
        assert disabler.trigger_type_id == trigger_type_id

    def test_disable_calls_correct_update_query(self, trigger_disabler, mock_trigger_status):
        """Test that disable() calls the correct database update query."""
        trigger_disabler.disable()

        # Verify the update query was called with status: 0
        mock_trigger_status.update.assert_called_once_with({mock_trigger_status.status: 0})

        # Verify the where clause was called with the correct trigger_type_id
        update_result = mock_trigger_status.update.return_value
        update_result.where.assert_called_once_with(
            mock_trigger_status.trigger_type_id == trigger_disabler.trigger_type_id
        )

        # Verify execute was called
        where_result = update_result.where.return_value
        where_result.execute.assert_called_once()

    def test_enable_calls_correct_update_query(self, trigger_disabler, mock_trigger_status):
        """Test that enable() calls the correct database update query."""
        trigger_disabler.enable()

        # Verify the update query was called with status: 1
        mock_trigger_status.update.assert_called_once_with({mock_trigger_status.status: 1})

        # Verify the where clause was called with the correct trigger_type_id
        update_result = mock_trigger_status.update.return_value
        update_result.where.assert_called_once_with(
            mock_trigger_status.trigger_type_id == trigger_disabler.trigger_type_id
        )

        # Verify execute was called
        where_result = update_result.where.return_value
        where_result.execute.assert_called_once()

    @pytest.mark.parametrize('trigger_type_id', [1, 2, 100])
    def test_disable_with_different_trigger_types(self, trigger_type_id, mock_trigger_status):
        """Test disable functionality with different trigger type IDs."""
        disabler = TriggerDisabler(trigger_type_id)
        disabler.disable()

        update_result = mock_trigger_status.update.return_value
        update_result.where.assert_called_once_with(mock_trigger_status.trigger_type_id == trigger_type_id)

    @pytest.mark.parametrize('trigger_type_id', [3, 7, 50])
    def test_enable_with_different_trigger_types(self, trigger_type_id, mock_trigger_status):
        """Test enable functionality with different trigger type IDs."""
        disabler = TriggerDisabler(trigger_type_id)
        disabler.enable()

        update_result = mock_trigger_status.update.return_value
        update_result.where.assert_called_once_with(mock_trigger_status.trigger_type_id == trigger_type_id)

    def test_context_manager_enter_returns_self(self, trigger_disabler, mock_trigger_status):
        """Test that __enter__ returns self and calls disable."""
        with patch.object(trigger_disabler, 'disable') as mock_disable:
            result = trigger_disabler.__enter__()

            assert result is trigger_disabler
            mock_disable.assert_called_once()

    @pytest.mark.parametrize(
        'exception_type,exception_value,traceback_value',
        [
            (None, None, None),  # Normal exit
            (ValueError, ValueError('test error'), None),  # Exception exit
            (RuntimeError, RuntimeError('runtime error'), None),  # Different exception
            (KeyboardInterrupt, KeyboardInterrupt(), None),  # Keyboard interrupt
        ],
    )
    def test_context_manager_exit_calls_enable(
        self,
        trigger_disabler,
        mock_trigger_status,
        exception_type: Optional[Type[BaseException]],
        exception_value: Optional[BaseException],
        traceback_value: Optional[TracebackType],
    ):
        """Test that __exit__ calls enable regardless of exception status."""
        with patch.object(trigger_disabler, 'enable') as mock_enable:
            trigger_disabler.__exit__(exception_type, exception_value, traceback_value)
            mock_enable.assert_called_once()

    def test_context_manager_full_workflow(self, mock_trigger_status):
        """Test the complete context manager workflow."""
        trigger_type_id = 42

        with (
            patch('mafw.db.std_tables.TriggerDisabler.disable') as mock_disable,
            patch('mafw.db.std_tables.TriggerDisabler.enable') as mock_enable,
        ):
            with TriggerDisabler(trigger_type_id) as disabler:
                assert disabler.trigger_type_id == trigger_type_id
                # Verify disable was called on enter
                mock_disable.assert_called_once()

            # Verify enable was called on exit
            mock_enable.assert_called_once()

    def test_context_manager_with_exception(self, mock_trigger_status):
        """Test that enable is called even when an exception occurs in the context."""
        with patch('mafw.db.std_tables.TriggerDisabler.enable') as mock_enable:
            try:
                with TriggerDisabler(1):
                    raise ValueError('Test exception')
            except ValueError:
                pass  # Expected exception

            # Verify enable was still called despite the exception
            mock_enable.assert_called_once()

    def test_manual_disable_enable_workflow(self, trigger_disabler, mock_trigger_status):
        """Test the manual disable/enable workflow without context manager."""
        # Test disable
        trigger_disabler.disable()

        # Verify disable was called correctly
        mock_trigger_status.update.assert_called_with({mock_trigger_status.status: 0})

        # Reset the mock
        mock_trigger_status.reset_mock()

        # Test enable
        trigger_disabler.enable()

        # Verify enable was called correctly
        mock_trigger_status.update.assert_called_with({mock_trigger_status.status: 1})

    def test_multiple_disable_calls(self, trigger_disabler, mock_trigger_status):
        """Test that multiple disable calls work correctly."""
        trigger_disabler.disable()
        trigger_disabler.disable()

        # Should have been called twice
        assert mock_trigger_status.update.call_count == 2

        # Both calls should be with status: 0
        for call in mock_trigger_status.update.call_args_list:
            assert call[0][0] == {mock_trigger_status.status: 0}

    def test_multiple_enable_calls(self, trigger_disabler, mock_trigger_status):
        """Test that multiple enable calls work correctly."""
        trigger_disabler.enable()
        trigger_disabler.enable()

        # Should have been called twice
        assert mock_trigger_status.update.call_count == 2

        # Both calls should be with status: 1
        for call in mock_trigger_status.update.call_args_list:
            assert call[0][0] == {mock_trigger_status.status: 1}

    def test_database_exception_handling_disable(self, trigger_disabler, mock_trigger_status):
        """Test behavior when database operations fail during disable."""
        # Make the execute method raise an exception
        mock_trigger_status.update.return_value.where.return_value.execute.side_effect = RuntimeError(
            'Database connection failed'
        )

        with pytest.raises(RuntimeError, match='Database connection failed'):
            trigger_disabler.disable()

    def test_database_exception_handling_enable(self, trigger_disabler, mock_trigger_status):
        """Test behavior when database operations fail during enable."""
        # Make the execute method raise an exception
        mock_trigger_status.update.return_value.where.return_value.execute.side_effect = RuntimeError(
            'Database connection failed'
        )

        with pytest.raises(RuntimeError, match='Database connection failed'):
            trigger_disabler.enable()

    def test_context_manager_exception_in_exit_overrides_original(self, mock_trigger_status):
        """Test that if enable() fails in __exit__, the RuntimeError is raised (overriding original exception)."""
        with patch('mafw.db.std_tables.TriggerDisabler.enable', side_effect=RuntimeError('Enable failed')):
            with pytest.raises(RuntimeError, match='Enable failed'):  # RuntimeError should be raised
                with TriggerDisabler(1):
                    raise ValueError('Original exception')

    def test_context_manager_normal_exception_propagation(self, mock_trigger_status):
        """Test that when enable() succeeds, the original exception from the with block is propagated."""
        with patch('mafw.db.std_tables.TriggerDisabler.enable') as mock_enable:  # enable() succeeds (no exception)
            with pytest.raises(ValueError, match='Original exception'):
                with TriggerDisabler(1):
                    raise ValueError('Original exception')

            # Verify enable was still called
            mock_enable.assert_called_once()

    @pytest.mark.parametrize('call_count', [1, 3, 5])
    def test_performance_multiple_operations(self, mock_trigger_status, call_count):
        """Test performance characteristics with multiple operations."""
        disabler = TriggerDisabler(1)

        # Perform multiple disable/enable cycles
        for _ in range(call_count):
            disabler.disable()
            disabler.enable()

        # Verify the correct number of database calls were made
        assert mock_trigger_status.update.call_count == call_count * 2

        # Verify all execute calls were made
        execute_calls = 0
        for call in mock_trigger_status.update.return_value.where.return_value.execute.call_args_list:
            execute_calls += 1

        assert execute_calls == call_count * 2

    def test_type_annotations_compliance(self):
        """Test that the class methods have correct type annotations."""
        import inspect

        # Test __init__ signature
        init_sig = inspect.signature(TriggerDisabler.__init__)
        assert 'trigger_type_id' in init_sig.parameters
        assert init_sig.parameters['trigger_type_id'].annotation is int
        assert init_sig.return_annotation is None

        # Test __enter__ return type
        enter_sig = inspect.signature(TriggerDisabler.__enter__)
        assert enter_sig.return_annotation == 'TriggerDisabler'

        # Test __exit__ signature
        exit_sig = inspect.signature(TriggerDisabler.__exit__)
        assert exit_sig.return_annotation is None
