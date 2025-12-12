#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Test suite for abstract_plotter module.

This test suite provides comprehensive coverage for the abstract plotter classes and their functionality,
including mocking of external dependencies and testing of various scenarios.
"""

import logging
from unittest.mock import Mock, patch

import peewee
import pytest

from mafw.enumerators import LoopingStatus, LoopType
from mafw.processor_library.abstract_plotter import DataRetriever, FigurePlotter, GenericPlotter, PlotterMeta


class TestPlotterMeta:
    """Test the PlotterMeta metaclass."""

    def test_plotter_meta_inheritance(self):
        """Test that PlotterMeta properly inherits from Protocol and ProcessorMeta."""

        # Test that we can create a class with PlotterMeta
        class TestClass(metaclass=PlotterMeta):
            pass

        assert TestClass.__class__ == PlotterMeta


class TestDataRetriever:
    """Test the DataRetriever abstract base class."""

    def test_data_retriever_is_abstract(self):
        """Test that DataRetriever cannot be instantiated directly."""
        with pytest.raises(TypeError):
            DataRetriever()

    def test_data_retriever_init(self):
        """Test DataRetriever initialization with concrete implementation."""

        class ConcreteDataRetriever(DataRetriever):
            def get_data_frame(self):
                pass

            def patch_data_frame(self):
                pass

            def _attributes_valid(self):
                return True

        # Should be able to instantiate concrete implementation
        retriever = ConcreteDataRetriever()
        assert isinstance(retriever, DataRetriever)

    def test_abstract_methods_must_be_implemented(self):
        """Test that abstract methods must be implemented in subclasses."""

        class IncompleteDataRetriever(DataRetriever):
            pass

        with pytest.raises(TypeError):
            IncompleteDataRetriever()


class TestFigurePlotter:
    """Test the FigurePlotter abstract base class."""

    def test_figure_plotter_is_abstract(self):
        """Test that FigurePlotter cannot be instantiated directly."""
        with pytest.raises(TypeError):
            FigurePlotter()

    def test_figure_plotter_concrete_implementation(self):
        """Test concrete implementation of FigurePlotter."""

        class ConcreteFigurePlotter(FigurePlotter):
            def plot(self):
                pass

            def _attributes_valid(self):
                return True

        plotter = ConcreteFigurePlotter()
        assert isinstance(plotter, FigurePlotter)


class TestGenericPlotter:
    """Test the GenericPlotter class."""

    def test_generic_plotter_metaclass(self):
        """Test that GenericPlotter uses PlotterMeta."""
        assert GenericPlotter.__class__ == PlotterMeta


class TestGenericPlotterIsOutputExisting:
    """Test the is_output_existing method of GenericPlotter."""

    @pytest.fixture
    def plotter_with_db(self):
        """Create a plotter with database connection."""
        plotter = GenericPlotter(looper=LoopType.SingleLoop)
        plotter.name = 'test_plotter'
        plotter.replica_id = '123'
        plotter._database = Mock()
        return plotter

    @pytest.fixture
    def plotter_without_db(self):
        """Create a plotter without database connection."""
        plotter = GenericPlotter(looper=LoopType.SingleLoop)
        plotter.name = 'test_plotter'
        plotter._database = None
        return plotter

    def test_no_database_connection(self, plotter_without_db, caplog):
        """Test behavior when no database connection is available."""
        with caplog.at_level(logging.WARNING):
            result = plotter_without_db.is_output_existing()

        assert result is False
        assert 'No database connection available' in caplog.text

    @patch('mafw.processor_library.abstract_plotter.PlotterOutput')
    def test_no_existing_output_record(self, mock_plotter_output, plotter_with_db):
        """Test when no output record exists in database."""
        mock_plotter_output.get.side_effect = peewee.DoesNotExist()

        result = plotter_with_db.is_output_existing()

        assert result is False
        mock_plotter_output.get.assert_called_once()

    @patch('mafw.processor_library.abstract_plotter.TriggerDisabler')
    @patch('mafw.processor_library.abstract_plotter.PlotterOutput')
    def test_files_missing(self, mock_plotter_output, trigger_disabler, plotter_with_db):
        """Test when some files are missing."""
        # Mock query result
        mock_query = Mock()
        mock_file1 = Mock()
        mock_file1.exists.return_value = True
        mock_file2 = Mock()
        mock_file2.exists.return_value = False  # This file is missing
        mock_query.filename_list = [mock_file1, mock_file2]
        trigger_disabler.__enter__ = Mock()
        trigger_disabler.__exit__ = Mock()

        mock_plotter_output.get.return_value = mock_query
        mock_plotter_output.delete.return_value.where.return_value.execute.return_value = None

        result = plotter_with_db.is_output_existing()

        assert result is False
        mock_plotter_output.delete.assert_called_once()

    @patch('mafw.processor_library.abstract_plotter.TriggerDisabler')
    @patch('mafw.processor_library.abstract_plotter.PlotterOutput')
    @patch('mafw.processor_library.abstract_plotter.file_checksum')
    def test_checksum_mismatch(self, mock_file_checksum, mock_plotter_output, trigger_disabler, plotter_with_db):
        """Test when checksum doesn't match."""
        # Mock query result
        mock_query = Mock()
        mock_file = Mock()
        mock_file.exists.return_value = True
        mock_query.filename_list = [mock_file]
        mock_query.checksum = 'old_checksum'
        trigger_disabler.__enter__ = Mock()
        trigger_disabler.__exit__ = Mock()

        mock_plotter_output.get.return_value = mock_query
        mock_file_checksum.return_value = 'new_checksum'  # Different checksum
        mock_plotter_output.delete.return_value.where.return_value.execute.return_value = None

        result = plotter_with_db.is_output_existing()

        assert result is False
        mock_plotter_output.delete.assert_called_once()
        mock_file_checksum.assert_called_once_with([mock_file])

    @patch('mafw.processor_library.abstract_plotter.PlotterOutput')
    @patch('mafw.processor_library.abstract_plotter.file_checksum')
    def test_valid_existing_output(self, mock_file_checksum, mock_plotter_output, plotter_with_db):
        """Test when output exists and is valid."""
        # Mock query result
        mock_query = Mock()
        mock_file = Mock()
        mock_file.exists.return_value = True
        mock_query.filename_list = [mock_file]
        mock_query.checksum = 'matching_checksum'

        mock_plotter_output.get.return_value = mock_query
        mock_file_checksum.return_value = 'matching_checksum'  # Same checksum

        result = plotter_with_db.is_output_existing()

        assert result is True
        mock_file_checksum.assert_called_once_with([mock_file])


class TestGenericPlotterProcess:
    """Test the process method of GenericPlotter."""

    @pytest.fixture
    def plotter_with_mocks(self):
        """Create a plotter with all methods mocked."""
        plotter = GenericPlotter(looper=LoopType.SingleLoop)
        plotter.name = 'test_plotter'
        plotter.filter_register = Mock()
        plotter.filter_register.new_only = False

        # Mock all the methods that process() calls
        plotter.is_output_existing = Mock(return_value=False)
        plotter.in_loop_customization = Mock()
        plotter.get_data_frame = Mock()
        plotter.patch_data_frame = Mock()
        plotter.slice_data_frame = Mock()
        plotter.group_and_aggregate_data_frame = Mock()
        plotter.is_data_frame_empty = Mock(return_value=False)
        plotter.plot = Mock()
        plotter.customize_plot = Mock()
        plotter.save = Mock()
        plotter.update_db = Mock()

        return plotter

    def test_process_with_existing_output_and_new_only(self, plotter_with_mocks):
        """Test process method when output exists and new_only is True."""
        plotter_with_mocks.filter_register.new_only = True
        plotter_with_mocks.is_output_existing.return_value = True

        plotter_with_mocks.process()

        # Should return early, not calling other methods
        plotter_with_mocks.is_output_existing.assert_called_once()
        plotter_with_mocks.in_loop_customization.assert_not_called()

    def test_process_full_workflow(self, plotter_with_mocks):
        """Test full process workflow when data frame is not empty."""
        plotter_with_mocks.process()

        # Verify all methods are called in correct order
        plotter_with_mocks.in_loop_customization.assert_called_once()
        plotter_with_mocks.get_data_frame.assert_called_once()
        plotter_with_mocks.patch_data_frame.assert_called_once()
        plotter_with_mocks.slice_data_frame.assert_called_once()
        plotter_with_mocks.group_and_aggregate_data_frame.assert_called_once()
        plotter_with_mocks.is_data_frame_empty.assert_called_once()
        plotter_with_mocks.plot.assert_called_once()
        plotter_with_mocks.customize_plot.assert_called_once()
        plotter_with_mocks.save.assert_called_once()
        plotter_with_mocks.update_db.assert_called_once()

    def test_process_with_empty_data_frame(self, plotter_with_mocks):
        """Test process method when data frame is empty."""
        plotter_with_mocks.is_data_frame_empty.return_value = True

        plotter_with_mocks.process()

        # Should not call plotting methods when data frame is empty
        plotter_with_mocks.is_data_frame_empty.assert_called_once()
        plotter_with_mocks.plot.assert_not_called()
        plotter_with_mocks.customize_plot.assert_not_called()
        plotter_with_mocks.save.assert_not_called()
        plotter_with_mocks.update_db.assert_not_called()


class TestGenericPlotterDefaultMethods:
    """Test default implementations of GenericPlotter methods."""

    @pytest.fixture
    def generic_plotter(self):
        """Create a GenericPlotter instance."""

        plotter = GenericPlotter(looper=LoopType.SingleLoop)
        plotter.name = 'test_plotter'
        plotter.progress_message = ''
        return plotter

    def test_is_data_frame_empty_default(self, generic_plotter):
        """Test default implementation of is_data_frame_empty."""
        result = generic_plotter.is_data_frame_empty()
        assert result is False

    def test_in_loop_customization_default(self, generic_plotter):
        """Test default implementation of in_loop_customization."""
        # Should not raise any exception
        generic_plotter.in_loop_customization()

    def test_get_data_frame_default(self, generic_plotter):
        """Test default implementation of get_data_frame."""
        # Should not raise any exception (it's a pass statement)
        generic_plotter.get_data_frame()

    def test_format_progress_message(self, generic_plotter):
        """Test format_progress_message method."""
        generic_plotter.format_progress_message()
        assert generic_plotter.progress_message == 'test_plotter is working'

    def test_plot_default(self, generic_plotter):
        """Test default implementation of plot."""
        generic_plotter.plot()

    def test_customize_plot_default(self, generic_plotter):
        """Test default implementation of customize_plot."""
        generic_plotter.customize_plot()

    def test_save_default(self, generic_plotter):
        """Test default implementation of save."""
        generic_plotter.save()

    def test_update_db_default(self, generic_plotter):
        """Test default implementation of update_db."""
        generic_plotter.update_db()

    def test_slice_data_frame_default(self, generic_plotter):
        """Test default implementation of slice_data_frame."""
        generic_plotter.slice_data_frame()

    def test_group_and_aggregate_data_frame_default(self, generic_plotter):
        """Test default implementation of group_and_aggregate_data_frame."""
        generic_plotter.group_and_aggregate_data_frame()

    def test_patch_data_frame_default(self, generic_plotter):
        """Test default implementation of patch_data_frame."""
        generic_plotter.patch_data_frame()


class TestGenericPlotterFinish:
    """Test the finish method of GenericPlotter."""

    @pytest.fixture
    def plotter_with_finish_setup(self):
        """Create a plotter set up for testing finish method."""
        plotter = GenericPlotter(looper=LoopType.SingleLoop)
        plotter.looping_status = LoopingStatus.Continue
        plotter._update_plotter_db = Mock()
        return plotter

    @patch('mafw.processor_library.abstract_plotter.Processor.finish')
    def test_finish_with_continue_status(self, mock_super_finish, plotter_with_finish_setup):
        """Test finish method when looping status is Continue."""
        plotter_with_finish_setup.finish()

        plotter_with_finish_setup._update_plotter_db.assert_called_once()
        mock_super_finish.assert_called_once()

    @patch('mafw.processor_library.abstract_plotter.Processor.finish')
    def test_finish_with_other_status(self, mock_super_finish, plotter_with_finish_setup):
        """Test finish method when looping status is not Continue."""
        plotter_with_finish_setup.looping_status = LoopingStatus.Skip

        plotter_with_finish_setup.finish()

        plotter_with_finish_setup._update_plotter_db.assert_not_called()
        mock_super_finish.assert_called_once()


class TestGenericPlotterUpdatePlotterDb:
    """Test the _update_plotter_db method of GenericPlotter."""

    @pytest.fixture
    def plotter_with_db_setup(self):
        """Create a plotter set up for testing database update."""
        plotter = GenericPlotter(looper=LoopType.SingleLoop)
        plotter.name = 'test_plotter'
        plotter.output_filename_list = []
        return plotter

    def test_update_plotter_db_no_database(self, plotter_with_db_setup, caplog):
        """Test _update_plotter_db when no database connection exists."""
        plotter_with_db_setup._database = None

        with caplog.at_level(logging.WARNING):
            plotter_with_db_setup._update_plotter_db()

        assert 'No database connection available' in caplog.text

    def test_update_plotter_db_empty_output_list(self, plotter_with_db_setup):
        """Test _update_plotter_db when output filename list is empty."""
        plotter_with_db_setup._database = Mock()
        plotter_with_db_setup.output_filename_list = []

        # Should return early without doing anything
        plotter_with_db_setup._update_plotter_db()

    @patch('mafw.processor_library.abstract_plotter.PlotterOutput')
    def test_update_plotter_db_success(self, mock_plotter_output, plotter_with_db_setup):
        """Test successful database update."""
        plotter_with_db_setup._database = Mock()
        plotter_with_db_setup.output_filename_list = ['file1.png', 'file2.png']

        # Mock the upsert chain
        mock_upsert = Mock()
        mock_execute = Mock()
        mock_upsert.execute.return_value = mock_execute
        mock_plotter_output.std_upsert.return_value = mock_upsert

        plotter_with_db_setup._update_plotter_db()

        # Verify upsert was called with correct data
        mock_plotter_output.std_upsert.assert_called_once_with(
            {
                'plotter_name': 'test_plotter',
                'filename_list': ['file1.png', 'file2.png'],
                'checksum': ['file1.png', 'file2.png'],
            }
        )
        mock_upsert.execute.assert_called_once()


class TestGenericPlotterParametrized:
    """Parametrized tests for GenericPlotter."""

    @pytest.fixture
    def plotter_base(self):
        """Base plotter for parametrized tests."""

        plotter = GenericPlotter(looper=LoopType.SingleLoop)
        plotter.name = 'test_plotter'
        return plotter

    @pytest.mark.parametrize(
        'looping_status,should_update',
        [
            (LoopingStatus.Continue, True),
            (LoopingStatus.Abort, False),
            (LoopingStatus.Quit, False),
        ],
    )
    @patch('mafw.processor_library.abstract_plotter.Processor.finish')
    def test_finish_with_different_statuses(self, mock_super_finish, plotter_base, looping_status, should_update):
        """Test finish method with different looping statuses."""
        plotter_base.looping_status = looping_status
        plotter_base._update_plotter_db = Mock()

        plotter_base.finish()

        if should_update:
            plotter_base._update_plotter_db.assert_called_once()
        else:
            plotter_base._update_plotter_db.assert_not_called()

        mock_super_finish.assert_called_once()

    @pytest.mark.parametrize(
        'new_only,output_exists,should_continue',
        [
            (True, True, False),  # new_only=True and output exists -> should return early
            (True, False, True),  # new_only=True but no output -> should continue
            (False, True, True),  # new_only=False regardless of output -> should continue
            (False, False, True),  # new_only=False regardless of output -> should continue
        ],
    )
    def test_process_new_only_scenarios(self, plotter_base, new_only, output_exists, should_continue):
        """Test process method with different new_only and output existence scenarios."""
        plotter_base.filter_register = Mock()
        plotter_base.filter_register.new_only = new_only
        plotter_base.is_output_existing = Mock(return_value=output_exists)
        plotter_base.in_loop_customization = Mock()

        plotter_base.process()

        if should_continue:
            plotter_base.in_loop_customization.assert_called_once()
        else:
            plotter_base.in_loop_customization.assert_not_called()


@pytest.mark.integration_test
class TestIntegration:
    """Integration tests for abstract plotter components."""

    def test_mixed_class_creation(self):
        """Test creating a mixed class with DataRetriever and FigurePlotter."""

        class ConcreteDataRetriever(DataRetriever):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.data = ''

            def get_data_frame(self):
                self.data = 'retrieved'

            def patch_data_frame(self):
                self.data = 'patched'

            def _attributes_valid(self):
                return True

        class ConcreteFigurePlotter(FigurePlotter):
            def plot(self):
                self.plotted = True

            def _attributes_valid(self):
                return True

        # remember the generic plotter always at the end!
        class MixedPlotter(ConcreteDataRetriever, ConcreteFigurePlotter, GenericPlotter):
            pass

        mixed = MixedPlotter(looper=LoopType.SingleLoop)
        mixed.get_data_frame()
        mixed.patch_data_frame()
        mixed.plot()

        assert mixed.data == 'patched'
        assert mixed.plotted is True

    def test_abstract_method_enforcement(self):
        """Test that abstract methods are properly enforced."""

        # Test incomplete DataRetriever
        class IncompleteRetriever(DataRetriever):
            def get_data_frame(self):
                pass

            # Missing patch_data_frame and _attributes_valid

        with pytest.raises(TypeError):
            IncompleteRetriever()

        # Test incomplete FigurePlotter
        class IncompletePlotter(FigurePlotter):
            def plot(self):
                pass

            # Missing _attributes_valid

        with pytest.raises(TypeError):
            IncompletePlotter()


# Additional tests for edge cases and error handling
class TestEdgeCases:
    """Test edge cases and error handling."""

    @pytest.fixture
    def plotter_edge_case(self):
        """Create plotter for edge case testing."""

        plotter = GenericPlotter(looper=LoopType.SingleLoop)
        plotter.name = 'edge_case_plotter'
        return plotter

    def test_logging_configuration(self, plotter_edge_case):
        """Test logging is properly configured."""
        import mafw.processor_library.abstract_plotter as module

        assert hasattr(module, 'log')
        assert isinstance(module.log, logging.Logger)

    @patch('mafw.processor_library.abstract_plotter.PlotterOutput')
    def test_database_exception_handling(self, mock_plotter_output, plotter_edge_case):
        """Test handling of unexpected database exceptions."""
        plotter_edge_case._database = Mock()

        # Simulate unexpected database error
        mock_plotter_output.get.side_effect = Exception('Unexpected DB error')

        # Should not raise exception, but return False
        with pytest.raises(Exception):
            plotter_edge_case.is_output_existing()
