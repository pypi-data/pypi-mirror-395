#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Unit tests for the sns_plotter.py module.

This module provides comprehensive tests for all plotter classes including
data retrievers, figure plotters, and the generic plotter processor.
"""

from pathlib import Path
from unittest.mock import Mock, patch

import pandas as pd
import peewee
import pytest

from mafw.enumerators import LoopingStatus, LoopType
from mafw.mafw_errors import PlotterMixinNotInitialized
from mafw.processor_library.abstract_plotter import DataRetriever, FigurePlotter

# Import the module under test
from mafw.processor_library.sns_plotter import (
    CatPlot,
    DisPlot,
    FromDatasetDataRetriever,
    HDFPdDataRetriever,
    LMPlot,
    PdDataRetriever,
    RelPlot,
    SNSFigurePlotter,
    SNSPlotter,
    SQLPdDataRetriever,
)


class TestDataRetriever:
    """Test cases for the DataRetriever protocol."""

    def test_data_retriever_init(self):
        """Test DataRetriever initialization."""
        # Since DataRetriever is a Protocol, we can't instantiate it directly
        # but we can test that it has the expected interface
        assert hasattr(DataRetriever, 'get_data_frame')
        assert hasattr(DataRetriever, 'patch_data_frame')
        assert hasattr(DataRetriever, '_attributes_valid')

    def test_data_retriever_default_methods(self):
        """Test default method implementations."""

        class TestRetriever(PdDataRetriever):
            def __init__(self):
                self.data_frame = pd.DataFrame()
                super().__init__()

        retriever = TestRetriever()
        # Test default implementations don't raise errors
        retriever.get_data_frame()
        retriever.patch_data_frame()
        assert retriever._attributes_valid() is True


class TestFromDatasetDataRetriever:
    """Test cases for FromDatasetDataRetriever."""

    def test_init_with_dataset_name(self):
        """Test initialization with dataset name."""
        retriever = FromDatasetDataRetriever(dataset_name='tips')
        assert retriever.dataset_name == 'tips'

    def test_init_without_dataset_name(self):
        """Test initialization without dataset name."""
        retriever = FromDatasetDataRetriever()
        assert retriever.dataset_name == ''

    @patch('mafw.processor_library.sns_plotter.sns')
    def test_attributes_valid_with_valid_dataset(self, mock_sns):
        """Test _attributes_valid with valid dataset."""
        mock_sns.get_dataset_names.return_value = ['tips', 'flights', 'iris']
        retriever = FromDatasetDataRetriever(dataset_name='tips')
        assert retriever._attributes_valid() is True

    @patch('mafw.processor_library.sns_plotter.sns')
    def test_attributes_valid_with_invalid_dataset(self, mock_sns):
        """Test _attributes_valid with invalid dataset."""
        mock_sns.get_dataset_names.return_value = ['tips', 'flights', 'iris']
        retriever = FromDatasetDataRetriever(dataset_name='invalid')
        assert retriever._attributes_valid() is False

    def test_attributes_valid_with_empty_dataset(self):
        """Test _attributes_valid with empty dataset name."""
        retriever = FromDatasetDataRetriever(dataset_name='')
        assert retriever._attributes_valid() is False

    @patch('mafw.processor_library.sns_plotter.sns')
    def test_get_data_frame_success(self, mock_sns):
        """Test successful data frame retrieval."""
        mock_df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
        mock_sns.load_dataset.return_value = mock_df
        mock_sns.get_dataset_names.return_value = ['tips']

        retriever = FromDatasetDataRetriever(dataset_name='tips')
        retriever.get_data_frame()

        mock_sns.load_dataset.assert_called_once_with('tips')
        pd.testing.assert_frame_equal(retriever.data_frame, mock_df)

    def test_get_data_frame_invalid_attributes(self):
        """Test get_data_frame with invalid attributes raises exception."""
        retriever = FromDatasetDataRetriever(dataset_name='')
        with pytest.raises(PlotterMixinNotInitialized):
            retriever.get_data_frame()


class TestSQLDataRetriever:
    """Test cases for SQLDataRetriever."""

    def test_init_with_all_params(self):
        """Test initialization with all parameters."""
        retriever = SQLPdDataRetriever(table_name='test_table', required_cols=['col1', 'col2'], where_clause='id > 10')
        assert retriever.table_name == 'test_table'
        assert list(retriever.required_columns) == ['col1', 'col2']
        assert retriever.where_clause == 'id > 10'

    def test_init_with_string_column_list(self):
        """Test initialization with single column as string."""
        retriever = SQLPdDataRetriever(table_name='test_table', required_cols='col1')
        assert list(retriever.required_columns) == ['col1']

    def test_init_with_defaults(self):
        """Test initialization with default values."""
        retriever = SQLPdDataRetriever()
        assert retriever.table_name == ''
        assert list(retriever.required_columns) == []
        assert retriever.where_clause == '1'

    @pytest.mark.parametrize(
        'table_name,required_cols,expected',
        [
            ('test_table', ['col1'], True),
            ('', ['col1'], False),
            ('test_table', [], False),
            ('test_table', None, False),
        ],
    )
    def test_attributes_valid(self, table_name, required_cols, expected):
        """Test _attributes_valid with various parameters."""
        retriever = SQLPdDataRetriever(table_name=table_name, required_cols=required_cols)
        assert retriever._attributes_valid() == expected

    @patch('mafw.processor_library.sns_plotter.pd.read_sql')
    def test_get_data_frame_success(self, mock_read_sql):
        """Test successful data frame retrieval from SQL."""
        mock_df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        mock_read_sql.return_value = mock_df
        mock_database = Mock()
        mock_database.connection.return_value = 'mock_connection'

        retriever = SQLPdDataRetriever(table_name='test_table', required_cols=['col1', 'col2'], where_clause='id > 10')
        retriever.database = mock_database
        retriever.get_data_frame()

        expected_sql = 'SELECT col1, col2 FROM test_table WHERE ?'
        mock_read_sql.assert_called_once_with(expected_sql, con='mock_connection', params=('id > 10',))
        pd.testing.assert_frame_equal(retriever.data_frame, mock_df)

    @patch('mafw.processor_library.sns_plotter.pd.read_sql')
    def test_get_data_frame_success_with_redefinition(self, mock_read_sql):
        """Test successful data frame retrieval from SQL."""
        mock_df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        mock_read_sql.return_value = mock_df
        mock_database = Mock()
        mock_database.connection.return_value = 'mock_connection'

        retriever = SQLPdDataRetriever(table_name='test_table', required_cols='col1', where_clause='id > 10')
        retriever.required_columns = 'col2'
        retriever.where_clause = ''
        retriever.database = mock_database
        retriever.get_data_frame()

        expected_sql = 'SELECT col2 FROM test_table WHERE ?'
        mock_read_sql.assert_called_once_with(expected_sql, con='mock_connection', params=(' 1 ',))
        pd.testing.assert_frame_equal(retriever.data_frame, mock_df)

    @patch('mafw.processor_library.sns_plotter.pd.read_sql')
    def test_get_data_frame_with_where_prefix(self, mock_read_sql):
        """Test data frame retrieval with WHERE prefix in clause."""
        mock_df = pd.DataFrame({'col1': [1, 2]})
        mock_read_sql.return_value = mock_df
        mock_database = Mock()
        mock_database.connection.return_value = 'mock_connection'

        retriever = SQLPdDataRetriever(table_name='test_table', required_cols=['col1'], where_clause='WHERE id > 10')
        retriever.database = mock_database
        retriever.get_data_frame()

        expected_sql = 'SELECT col1 FROM test_table WHERE ?'
        mock_read_sql.assert_called_once_with(expected_sql, con='mock_connection', params=('id > 10',))

    def test_get_data_frame_invalid_attributes(self):
        """Test get_data_frame with invalid attributes raises exception."""
        retriever = SQLPdDataRetriever()
        with pytest.raises(PlotterMixinNotInitialized):
            retriever.get_data_frame()


class TestHDFDataRetriever:
    """Test cases for HDFDataRetriever."""

    def test_init_with_params(self):
        """Test initialization with parameters."""
        retriever = HDFPdDataRetriever(hdf_filename='test.h5', key='data')
        assert retriever.hdf_filename == Path('test.h5')
        assert retriever.key == 'data'

    def test_init_with_defaults(self):
        """Test initialization with default values."""
        retriever = HDFPdDataRetriever()
        assert retriever.hdf_filename == Path()
        assert retriever.key == ''

    def test_init_with_path_object(self):
        """Test initialization with Path object."""
        path_obj = Path('test.h5')
        retriever = HDFPdDataRetriever(hdf_filename=path_obj)
        assert retriever.hdf_filename == path_obj

    @patch('pathlib.Path.is_file')
    @pytest.mark.parametrize('file_exists,attribute_valid', [(True, True), (False, False)])
    def test_attributes_valid(self, mock_is_file, file_exists, attribute_valid):
        """Test _attributes_valid with valid parameters."""
        mock_is_file.return_value = file_exists
        retriever = HDFPdDataRetriever(hdf_filename='test.h5', key='data')
        assert retriever._attributes_valid() is attribute_valid

    def test_attributes_valid_empty_filename(self):
        """Test _attributes_valid with empty filename."""
        retriever = HDFPdDataRetriever(key='data')
        assert retriever._attributes_valid() is False

    @patch('pathlib.Path.is_file')
    def test_attributes_valid_empty_key(self, mock_is_file):
        """Test _attributes_valid with empty key."""
        mock_is_file.return_value = True
        retriever = HDFPdDataRetriever(hdf_filename='test.h5')
        assert retriever._attributes_valid() is False

    @patch('mafw.processor_library.sns_plotter.pd.read_hdf')
    @patch('pathlib.Path.is_file')
    def test_get_data_frame_success(self, mock_is_file, mock_read_hdf):
        """Test successful data frame retrieval from HDF."""
        mock_is_file.return_value = True
        mock_df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
        mock_read_hdf.return_value = mock_df

        retriever = HDFPdDataRetriever(hdf_filename='test.h5', key='data')
        retriever.get_data_frame()

        mock_read_hdf.assert_called_once_with(Path('test.h5'), 'data')
        pd.testing.assert_frame_equal(retriever.data_frame, mock_df)

    def test_get_data_frame_invalid_attributes(self):
        """Test get_data_frame with invalid attributes raises exception."""
        retriever = HDFPdDataRetriever()
        with pytest.raises(PlotterMixinNotInitialized):
            retriever.get_data_frame()


class TestFigurePlotter:
    """Test cases for the FigurePlotter protocol."""

    def test_figure_plotter_interface(self):
        """Test FigurePlotter has expected interface."""
        assert hasattr(FigurePlotter, 'plot')
        assert hasattr(FigurePlotter, '_attributes_valid')

    def test_figure_plotter_default_methods(self):
        """Test default method implementations."""

        class TestPlotter(SNSFigurePlotter):
            def __init__(self):
                self.data_frame = pd.DataFrame()
                self.facet_grid = None
                super().__init__()

        plotter = TestPlotter()
        plotter.plot()  # Should not raise
        assert plotter._attributes_valid() is True


class TestRelPlot:
    """Test cases for RelPlot."""

    def test_init_with_defaults(self):
        """Test initialization with default values."""
        plotter = RelPlot()
        assert plotter.x is None
        assert plotter.y is None
        assert plotter.hue is None
        assert plotter.row is None
        assert plotter.col is None
        assert plotter.palette is None
        assert plotter.kind == 'scatter'
        assert plotter.legend == 'auto'
        assert plotter.plot_kws == {}
        assert plotter.facet_kws is None

    def test_init_with_params(self):
        """Test initialization with parameters."""
        plot_kws = {'alpha': 0.5}
        facet_kws = {'height': 4}

        plotter = RelPlot(
            x='x_col', y='y_col', hue='hue_col', kind='line', legend=False, plot_kws=plot_kws, facet_kws=facet_kws
        )

        assert plotter.x == 'x_col'
        assert plotter.y == 'y_col'
        assert plotter.hue == 'hue_col'
        assert plotter.kind == 'line'
        assert plotter.legend is False
        assert plotter.plot_kws == plot_kws
        assert plotter.facet_kws == facet_kws

    @patch('mafw.processor_library.sns_plotter.sns.relplot')
    def test_plot_method(self, mock_relplot):
        """Test the plot method."""
        mock_facet_grid = Mock()
        mock_relplot.return_value = mock_facet_grid

        plotter = RelPlot(x='x', y='y', kind='scatter')
        plotter.data_frame = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
        plotter.plot()

        mock_relplot.assert_called_once_with(
            data=plotter.data_frame,
            x='x',
            y='y',
            hue=None,
            row=None,
            col=None,
            palette=None,
            kind='scatter',
            legend='auto',
            facet_kws=None,
        )
        assert plotter.facet_grid == mock_facet_grid


class TestDisPlot:
    """Test cases for DisPlot."""

    def test_init_with_defaults(self):
        """Test initialization with default values."""
        plotter = DisPlot()
        assert plotter.x is None
        assert plotter.y is None
        assert plotter.kind == 'hist'
        assert plotter.legend is True
        assert plotter.rug is False
        assert plotter.rug_kws is None
        assert plotter.plot_kws == {}

    def test_init_with_params(self):
        """Test initialization with parameters."""
        rug_kws = {'height': 0.05}
        plot_kws = {'bins': 20}

        plotter = DisPlot(x='x_col', kind='kde', legend=False, rug=True, rug_kws=rug_kws, plot_kws=plot_kws)

        assert plotter.x == 'x_col'
        assert plotter.kind == 'kde'
        assert plotter.legend is False
        assert plotter.rug is True
        assert plotter.rug_kws == rug_kws
        assert plotter.plot_kws == plot_kws

    @patch('mafw.processor_library.sns_plotter.sns.displot')
    def test_plot_method(self, mock_displot):
        """Test the plot method."""
        mock_facet_grid = Mock()
        mock_displot.return_value = mock_facet_grid

        plotter = DisPlot(x='x', kind='hist')
        plotter.data_frame = pd.DataFrame({'x': [1, 2, 3, 4, 5]})
        plotter.plot()

        mock_displot.assert_called_once_with(
            data=plotter.data_frame,
            x='x',
            y=None,
            hue=None,
            row=None,
            col=None,
            palette=None,
            kind='hist',
            legend=True,
            rug=False,
            rug_kws=None,
            facet_kws=None,
        )
        assert plotter.facet_grid == mock_facet_grid


class TestLMPlot:
    """Test cases for LMPlot."""

    def test_init_with_defaults(self):
        plotter = LMPlot()
        assert plotter.x is None
        assert plotter.y is None
        assert plotter.hue is None
        assert plotter.row is None
        assert plotter.col is None
        assert plotter.palette is None
        assert plotter.scatter_kws is None
        assert plotter.line_kws is None
        assert plotter.facet_kws is None

    def test_init_with_params(self):
        """Test initialization with parameters."""
        line_kws = {'height': 0.05}
        scatter_kws = {'bins': 20}

        plotter = LMPlot(x='x_col', legend=False, line_kws=line_kws, scatter_kws=scatter_kws)

        assert plotter.x == 'x_col'
        assert plotter.legend is False
        assert plotter.line_kws == line_kws
        assert plotter.scatter_kws == scatter_kws

    @patch('mafw.processor_library.sns_plotter.sns.lmplot')
    def test_plot_method(self, mock_lmplot):
        """Test the plot method."""
        mock_facet_grid = Mock()
        mock_lmplot.return_value = mock_facet_grid

        plotter = LMPlot(x='x', col='c')
        plotter.data_frame = pd.DataFrame({'x': [1, 2, 3, 4, 5]})
        plotter.plot()

        mock_lmplot.assert_called_once_with(
            data=plotter.data_frame,
            x='x',
            y=None,
            hue=None,
            row=None,
            col='c',
            palette=None,
            legend=True,
            scatter_kws=None,
            line_kws=None,
            facet_kws=None,
        )
        assert plotter.facet_grid == mock_facet_grid


class TestCatPlot:
    """Test cases for CatPlot."""

    def test_init_with_defaults(self):
        """Test initialization with default values."""
        plotter = CatPlot()
        assert plotter.x is None
        assert plotter.y is None
        assert plotter.kind == 'strip'
        assert plotter.legend == 'auto'
        assert plotter.native_scale is False
        assert plotter.plot_kws == {}

    def test_init_with_params(self):
        """Test initialization with parameters."""
        plot_kws = {'size': 4}

        plotter = CatPlot(x='category', y='value', kind='box', legend='full', native_scale=True, plot_kws=plot_kws)

        assert plotter.x == 'category'
        assert plotter.y == 'value'
        assert plotter.kind == 'box'
        assert plotter.legend == 'full'
        assert plotter.native_scale is True
        assert plotter.plot_kws == plot_kws

    @patch('mafw.processor_library.sns_plotter.sns.catplot')
    def test_plot_method(self, mock_catplot):
        """Test the plot method."""
        mock_facet_grid = Mock()
        mock_catplot.return_value = mock_facet_grid

        plotter = CatPlot(x='cat', y='val', kind='box')
        plotter.data_frame = pd.DataFrame({'cat': ['A', 'B', 'A', 'B'], 'val': [1, 2, 3, 4]})
        plotter.plot()

        mock_catplot.assert_called_once_with(
            data=plotter.data_frame,
            x='cat',
            y='val',
            hue=None,
            row=None,
            col=None,
            palette=None,
            kind='box',
            legend='auto',
            native_scale=False,
            facet_kws=None,
        )
        assert plotter.facet_grid == mock_facet_grid


class TestGenericPlotter:
    """Test cases for SNSPlotter."""

    def test_init_with_defaults(self):
        """Test initialization with default values."""
        plotter = SNSPlotter(looper=LoopType.SingleLoop)
        assert plotter.slicing_dict is None
        assert plotter.grouping_columns is None
        assert plotter.aggregation_functions is None
        assert plotter.matplotlib_backend == 'agg'
        assert isinstance(plotter.data_frame, pd.DataFrame)
        assert plotter.data_frame.empty
        assert plotter.output_filename_list == []
        assert plotter.facet_grid is None

    def test_init_with_params(self):
        """Test initialization with parameters."""
        slicing_dict = {'col1': 'value1'}
        grouping_columns = ['col2', 'col3']
        aggregation_functions = ['mean', 'sum']

        plotter = SNSPlotter(
            slicing_dict=slicing_dict,
            grouping_columns=grouping_columns,
            aggregation_functions=aggregation_functions,
            matplotlib_backend='TkAgg',
            looper=LoopType.SingleLoop,
        )

        assert plotter.slicing_dict == slicing_dict
        assert plotter.grouping_columns == grouping_columns
        assert plotter.aggregation_functions == aggregation_functions
        assert plotter.matplotlib_backend == 'tkagg'

    @patch('mafw.processor_library.sns_plotter.plt')
    def test_start_method_backend_switch(self, mock_plt):
        """Test start method switches matplotlib backend."""
        mock_plt.get_backend.return_value = 'Qt5Agg'

        plotter = SNSPlotter(matplotlib_backend='Agg', looper=LoopType.SingleLoop)
        plotter.start()

        mock_plt.switch_backend.assert_called_once_with('agg')

    @patch('mafw.processor_library.sns_plotter.plt')
    def test_start_method_same_backend(self, mock_plt):
        """Test start method when backend is already correct."""
        mock_plt.get_backend.return_value = 'Agg'

        plotter = SNSPlotter(matplotlib_backend='Agg', looper=LoopType.SingleLoop)
        plotter.start()

        mock_plt.switch_backend.assert_not_called()

    @patch('mafw.processor_library.sns_plotter.plt')
    def test_start_method_invalid_backend(self, mock_plt):
        """Test start method with invalid backend raises exception."""
        mock_plt.get_backend.return_value = 'Qt5Agg'
        mock_plt.switch_backend.side_effect = ModuleNotFoundError()

        plotter = SNSPlotter(matplotlib_backend='InvalidBackend', looper=LoopType.SingleLoop)
        with pytest.raises(ModuleNotFoundError):
            plotter.start()

    @patch.object(SNSPlotter, 'is_output_existing')
    @patch.object(SNSPlotter, 'plot')
    def test_process_with_new_only_and_existing_output(self, mock_workflow, mock_existing):
        """Test process method when new_only is True and output exists."""
        mock_existing.return_value = True

        plotter = SNSPlotter(looper=LoopType.SingleLoop)
        plotter.data_frame = pd.DataFrame({'cat': ['A', 'B', 'A', 'B'], 'val': [1, 2, 3, 4]})
        plotter.filter_register = Mock()
        plotter.filter_register.new_only = True

        plotter.execute()

        mock_existing.assert_called_once()
        mock_workflow.assert_not_called()

    @patch.object(SNSPlotter, 'is_output_existing')
    @patch.object(SNSPlotter, 'plot')
    def test_process_with_new_only_and_no_existing_output(self, mock_workflow, mock_existing):
        """Test process method when new_only is True and output doesn't exist."""
        mock_existing.return_value = False

        plotter = SNSPlotter(looper=LoopType.SingleLoop)
        plotter.filter_register = Mock()
        plotter.filter_register.new_only = True
        plotter.data_frame = pd.DataFrame({'cat': ['A', 'B', 'A', 'B'], 'val': [1, 2, 3, 4]})

        plotter.execute()

        mock_existing.assert_called_once()
        mock_workflow.assert_called_once()

    @patch.object(SNSPlotter, 'plot')
    def test_process_without_new_only(self, mock_workflow):
        """Test process method when new_only is False."""
        plotter = SNSPlotter(looper=LoopType.SingleLoop)
        plotter.filter_register = Mock()
        plotter.filter_register.new_only = False
        plotter.data_frame = pd.DataFrame({'cat': ['A', 'B', 'A', 'B'], 'val': [1, 2, 3, 4]})

        plotter.execute()

        mock_workflow.assert_called_once()

    @patch('mafw.processor_library.sns_plotter.plt.close')
    @patch.object(SNSPlotter, 'update_db')
    @patch.object(SNSPlotter, 'save')
    @patch.object(SNSPlotter, 'customize_plot')
    @patch.object(SNSPlotter, 'plot')
    @patch.object(SNSPlotter, 'group_and_aggregate_data_frame')
    @patch.object(SNSPlotter, 'slice_data_frame')
    @patch.object(SNSPlotter, 'patch_data_frame')
    @patch.object(SNSPlotter, 'get_data_frame')
    @patch.object(SNSPlotter, 'in_loop_customization')
    @patch.object(SNSPlotter, 'is_output_existing')
    def test_process_with_new_only_false(
        self,
        mock_existing,
        mock_custom,
        mock_get_df,
        mock_patch_df,
        mock_slice_df,
        mock_group_df,
        mock_plot,
        mock_customize,
        mock_save,
        mock_update_db,
        mock_plt_close,
    ):
        """Test process method when new_only is False."""
        plotter = SNSPlotter(looper=LoopType.SingleLoop)
        plotter.filter_register = Mock()
        plotter.filter_register.new_only = False
        plotter.data_frame = pd.DataFrame({'x': [1, 2, 3]})

        plotter.process()

        mock_existing.assert_not_called()
        mock_custom.assert_called_once()
        mock_get_df.assert_called_once()
        mock_patch_df.assert_called_once()
        mock_slice_df.assert_called_once()
        mock_group_df.assert_called_once()
        mock_plot.assert_called_once()
        mock_customize.assert_called_once()
        mock_save.assert_called_once()
        mock_update_db.assert_called_once()
        mock_plt_close.assert_called_once_with('all')

    @patch('mafw.processor_library.sns_plotter.plt.close')
    @patch.object(SNSPlotter, 'update_db')
    @patch.object(SNSPlotter, 'save')
    @patch.object(SNSPlotter, 'customize_plot')
    @patch.object(SNSPlotter, 'plot')
    @patch.object(SNSPlotter, 'group_and_aggregate_data_frame')
    @patch.object(SNSPlotter, 'slice_data_frame')
    @patch.object(SNSPlotter, 'patch_data_frame')
    @patch.object(SNSPlotter, 'get_data_frame')
    @patch.object(SNSPlotter, 'in_loop_customization')
    def test_execute_plot_workflow_with_data(
        self,
        mock_custom,
        mock_get_df,
        mock_patch_df,
        mock_slice_df,
        mock_group_df,
        mock_plot,
        mock_customize,
        mock_save,
        mock_update_db,
        mock_plt_close,
    ):
        """Test the complete plot workflow with data."""
        plotter = SNSPlotter(looper=LoopType.SingleLoop)
        plotter.data_frame = pd.DataFrame({'x': [1, 2, 3]})  # Non-empty dataframe
        plotter.execute()

        mock_custom.assert_called_once()
        mock_get_df.assert_called_once()
        mock_patch_df.assert_called_once()
        mock_slice_df.assert_called_once()
        mock_group_df.assert_called_once()
        mock_plot.assert_called_once()
        mock_customize.assert_called_once()
        mock_save.assert_called_once()
        mock_update_db.assert_called_once()
        mock_plt_close.assert_called_once_with('all')

    @patch('mafw.processor_library.sns_plotter.plt.close')
    @patch.object(SNSPlotter, 'update_db')
    @patch.object(SNSPlotter, 'save')
    @patch.object(SNSPlotter, 'customize_plot')
    @patch.object(SNSPlotter, 'plot')
    @patch.object(SNSPlotter, 'group_and_aggregate_data_frame')
    @patch.object(SNSPlotter, 'slice_data_frame')
    @patch.object(SNSPlotter, 'patch_data_frame')
    @patch.object(SNSPlotter, 'get_data_frame')
    @patch.object(SNSPlotter, 'in_loop_customization')
    def test_execute_plot_workflow_empty_data(
        self,
        mock_custom,
        mock_get_df,
        mock_patch_df,
        mock_slice_df,
        mock_group_df,
        mock_plot,
        mock_customize,
        mock_save,
        mock_update_db,
        mock_plt_close,
    ):
        """Test the complete plot workflow with empty data."""
        plotter = SNSPlotter(looper=LoopType.SingleLoop)
        plotter.data_frame = pd.DataFrame()  # Empty dataframe
        plotter.execute()

        mock_custom.assert_called_once()
        mock_get_df.assert_called_once()
        mock_patch_df.assert_called_once()
        mock_slice_df.assert_called_once()
        mock_group_df.assert_called_once()
        # These should not be called for empty dataframe
        mock_plot.assert_not_called()
        mock_customize.assert_not_called()
        mock_save.assert_not_called()
        mock_update_db.assert_not_called()
        mock_plt_close.assert_not_called()

    @patch('mafw.processor_library.sns_plotter.slice_data_frame')
    def test_slice_data_frame_with_slicing_dict(self, mock_slice):
        """Test slice_data_frame with slicing dictionary."""
        original_df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
        sliced_df = pd.DataFrame({'x': [1, 2], 'y': [4, 5]})
        mock_slice.return_value = sliced_df

        plotter = SNSPlotter(slicing_dict={'x': [1, 2]}, looper=LoopType.SingleLoop)
        plotter.data_frame = original_df
        plotter.slice_data_frame()

        mock_slice.assert_called_once_with(original_df, {'x': [1, 2]})
        pd.testing.assert_frame_equal(plotter.data_frame, sliced_df)

    def test_slice_data_frame_without_slicing_dict(self):
        """Test slice_data_frame without slicing dictionary."""
        original_df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})

        plotter = SNSPlotter(looper=LoopType.SingleLoop)
        plotter.data_frame = original_df
        plotter.slice_data_frame()

        # DataFrame should remain unchanged
        pd.testing.assert_frame_equal(plotter.data_frame, original_df)

    @patch('mafw.processor_library.sns_plotter.group_and_aggregate_data_frame')
    def test_group_and_aggregate_data_frame_with_params(self, mock_group_agg):
        """Test group_and_aggregate_data_frame with parameters."""
        original_df = pd.DataFrame({'group': ['A', 'A', 'B'], 'value': [1, 2, 3]})
        aggregated_df = pd.DataFrame({'group': ['A', 'B'], 'value': [1.5, 3.0]})
        mock_group_agg.return_value = aggregated_df

        plotter = SNSPlotter(grouping_columns=['group'], aggregation_functions=['mean'], looper=LoopType.SingleLoop)
        plotter.data_frame = original_df
        plotter.group_and_aggregate_data_frame()

        mock_group_agg.assert_called_once_with(original_df, ['group'], ['mean'])
        pd.testing.assert_frame_equal(plotter.data_frame, aggregated_df)

    def test_format_progress_message(self):
        """Test format_progress_message method."""
        plotter = SNSPlotter(looper=LoopType.SingleLoop)
        plotter.name = 'TestPlotter'
        plotter.format_progress_message()
        assert plotter.progress_message == 'TestPlotter is working'

    @patch.object(SNSPlotter, '_update_plotter_db')
    def test_finish_method_continue_status(self, mock_update_db):
        """Test finish method when looping status is Continue."""
        plotter = SNSPlotter(looper=LoopType.SingleLoop)
        plotter.looping_status = LoopingStatus.Continue

        plotter.finish()

        mock_update_db.assert_called_once()

    @patch.object(SNSPlotter, '_update_plotter_db')
    def test_finish_method_break_status(self, mock_update_db):
        """Test finish method when looping status is not Continue."""
        plotter = SNSPlotter(looper=LoopType.SingleLoop)
        plotter.looping_status = LoopingStatus.Abort

        plotter.finish()

        mock_update_db.assert_not_called()

    def test_empty_methods_default_implementation(self):
        """Test that empty methods don't raise errors."""
        plotter = SNSPlotter(looper=LoopType.SingleLoop)
        plotter.data_frame = pd.DataFrame({'x': [1, 2, 3]})

        # These should not raise any exceptions
        plotter.in_loop_customization()
        plotter.get_data_frame()
        plotter.plot()
        plotter.customize_plot()
        plotter.save()
        plotter.update_db()
        plotter.patch_data_frame()


class TestGenericPlotterDatabaseOperations:
    """Test database-related operations in SNSPlotter."""

    @patch('mafw.processor_library.abstract_plotter.log')
    def test_is_output_existing_no_database(self, mock_log):
        """Test is_output_existing when no database connection."""
        plotter = SNSPlotter(looper=LoopType.SingleLoop)
        plotter._database = None

        result = plotter.is_output_existing()

        assert result is False
        mock_log.warning.assert_called_once()

    @patch('mafw.processor_library.abstract_plotter.PlotterOutput')
    def test_is_output_existing_not_found(self, mock_plotter_output):
        """Test is_output_existing when output not found in database."""
        mock_plotter_output.get.side_effect = peewee.DoesNotExist()

        plotter = SNSPlotter(looper=LoopType.SingleLoop)
        plotter._database = Mock()
        plotter.name = 'TestPlotter'

        result = plotter.is_output_existing()

        assert result is False

    @patch('mafw.processor_library.abstract_plotter.TriggerDisabler')
    @patch('mafw.processor_library.abstract_plotter.PlotterOutput')
    def test_is_output_existing_files_missing(self, mock_plotter_output, trigger_disabler):
        """Test is_output_existing when files are missing."""
        mock_query = Mock()
        mock_query.filename_list = [Path('missing_file.png')]
        mock_plotter_output.get.return_value = mock_query
        mock_plotter_output.delete.return_value.where.return_value.execute.return_value = None
        trigger_disabler.__enter__ = Mock()
        trigger_disabler.__exit__ = Mock()

        plotter = SNSPlotter(looper=LoopType.SingleLoop)
        plotter._database = Mock()
        plotter.name = 'TestPlotter'

        with patch.object(Path, 'exists', return_value=False):
            result = plotter.is_output_existing()

        assert result is False
        mock_plotter_output.delete.assert_called_once()

    @patch('mafw.processor_library.abstract_plotter.TriggerDisabler')
    @patch('mafw.processor_library.abstract_plotter.file_checksum')
    @patch('mafw.processor_library.abstract_plotter.PlotterOutput')
    def test_is_output_existing_checksum_mismatch(self, mock_plotter_output, mock_checksum, trigger_disabler):
        """Test is_output_existing when checksum doesn't match."""
        mock_query = Mock()
        mock_query.filename_list = [Path('existing_file.png')]
        mock_query.checksum = 'old_checksum'
        mock_plotter_output.get.return_value = mock_query
        mock_plotter_output.delete.return_value.where.return_value.execute.return_value = None
        mock_checksum.return_value = 'new_checksum'
        trigger_disabler.__enter__ = Mock()
        trigger_disabler.__exit__ = Mock()

        plotter = SNSPlotter(looper=LoopType.SingleLoop)
        plotter._database = Mock()
        plotter.name = 'TestPlotter'

        with patch.object(Path, 'exists', return_value=True):
            result = plotter.is_output_existing()

        assert result is False
        mock_plotter_output.delete.assert_called_once()

    @patch('mafw.processor_library.abstract_plotter.file_checksum')
    @patch('mafw.processor_library.abstract_plotter.PlotterOutput')
    def test_is_output_existing_valid_output(self, mock_plotter_output, mock_checksum):
        """Test is_output_existing when output is valid."""
        mock_query = Mock()
        mock_query.filename_list = [Path('existing_file.png')]
        mock_query.checksum = 'valid_checksum'
        mock_plotter_output.get.return_value = mock_query
        mock_checksum.return_value = 'valid_checksum'

        plotter = SNSPlotter(looper=LoopType.SingleLoop)
        plotter._database = Mock()
        plotter.name = 'TestPlotter'

        with patch.object(Path, 'exists', return_value=True):
            result = plotter.is_output_existing()

        assert result is True

    @patch('mafw.processor_library.abstract_plotter.log')
    def test_update_plotter_db_no_database(self, mock_log):
        """Test _update_plotter_db when no database connection."""
        plotter = SNSPlotter(looper=LoopType.SingleLoop)
        plotter._database = None

        plotter._update_plotter_db()

        mock_log.warning.assert_called_once()

    @patch('mafw.processor_library.abstract_plotter.PlotterOutput')
    def test_update_plotter_db_no_files(self, mock_plotter_output):
        """Test _update_plotter_db when no output files."""
        plotter = SNSPlotter(looper=LoopType.SingleLoop)
        plotter._database = Mock()
        plotter.output_filename_list = []

        plotter._update_plotter_db()

        mock_plotter_output.std_upsert.assert_not_called()

    @patch('mafw.processor_library.abstract_plotter.PlotterOutput')
    def test_update_plotter_db_with_files(self, mock_plotter_output):
        """Test _update_plotter_db with output files."""
        mock_upsert = Mock()
        mock_plotter_output.std_upsert.return_value = mock_upsert

        plotter = SNSPlotter(looper=LoopType.SingleLoop)
        plotter._database = Mock()
        plotter.name = 'TestPlotter'
        plotter.output_filename_list = [Path('test.png')]

        plotter._update_plotter_db()

        mock_plotter_output.std_upsert.assert_called_once_with(
            {'plotter_name': 'TestPlotter', 'filename_list': [Path('test.png')], 'checksum': [Path('test.png')]}
        )
        mock_upsert.execute.assert_called_once()


class TestDataFrameOperations:
    """Test data frame operations in SNSPlotter."""

    @patch('mafw.processor_library.sns_plotter.group_and_aggregate_data_frame')
    def test_group_and_aggregate_data_frame_without_params(self, mock_group_agg):
        """Test group_and_aggregate_data_frame without parameters."""
        plotter = SNSPlotter(looper=LoopType.SingleLoop)
        plotter.data_frame = pd.DataFrame({'x': [1, 2, 3]})

        plotter.group_and_aggregate_data_frame()

        mock_group_agg.assert_not_called()

    @patch('mafw.processor_library.sns_plotter.group_and_aggregate_data_frame')
    def test_group_and_aggregate_data_frame_missing_functions(self, mock_group_agg):
        """Test group_and_aggregate_data_frame with columns but no functions."""
        plotter = SNSPlotter(grouping_columns=['group'], looper=LoopType.SingleLoop)
        plotter.data_frame = pd.DataFrame({'group': ['A', 'B'], 'value': [1, 2]})

        plotter.group_and_aggregate_data_frame()

        mock_group_agg.assert_not_called()

    @patch('mafw.processor_library.sns_plotter.group_and_aggregate_data_frame')
    def test_group_and_aggregate_data_frame_missing_columns(self, mock_group_agg):
        """Test group_and_aggregate_data_frame with functions but no columns."""
        plotter = SNSPlotter(aggregation_functions=['mean'], looper=LoopType.SingleLoop)
        plotter.data_frame = pd.DataFrame({'group': ['A', 'B'], 'value': [1, 2]})

        plotter.group_and_aggregate_data_frame()

        mock_group_agg.assert_not_called()


class TestCompositionPatterns:
    """Test composition patterns combining DataRetriever and FigurePlotter mixins."""

    def test_dataset_retriever_relplot_composition(self):
        """Test composition of FromDatasetDataRetriever with RelPlot."""

        class DatasetRelPlotterSNS(FromDatasetDataRetriever, RelPlot, SNSPlotter):
            pass

        with patch('seaborn.get_dataset_names', return_value=['tips']):
            with patch('seaborn.load_dataset') as mock_load:
                with patch('seaborn.relplot') as mock_relplot:
                    mock_df = pd.DataFrame({'x': [1, 2], 'y': [3, 4]})
                    mock_load.return_value = mock_df
                    mock_facet = Mock()
                    mock_relplot.return_value = mock_facet

                    plotter = DatasetRelPlotterSNS(
                        dataset_name='tips', x='total_bill', y='tip', kind='scatter', looper=LoopType.SingleLoop
                    )

                    plotter.get_data_frame()
                    assert plotter.data_frame.equals(mock_df)

                    plotter.plot()
                    mock_relplot.assert_called_once_with(
                        data=mock_df,
                        x='total_bill',
                        y='tip',
                        hue=None,
                        row=None,
                        col=None,
                        palette=None,
                        kind='scatter',
                        legend='auto',
                        facet_kws=None,
                    )
                    assert plotter.facet_grid == mock_facet

    def test_sql_retriever_displot_composition(self):
        """Test composition of SQLDataRetriever with DisPlot."""

        class SQLDisPlotterSNS(SQLPdDataRetriever, DisPlot, SNSPlotter):
            pass

        mock_db = Mock()
        mock_connection = Mock()
        mock_db.connection.return_value = mock_connection

        with patch('pandas.read_sql') as mock_read_sql:
            with patch('seaborn.displot') as mock_displot:
                mock_df = pd.DataFrame({'value': [1, 2, 3, 4]})
                mock_read_sql.return_value = mock_df
                mock_facet = Mock()
                mock_displot.return_value = mock_facet

                plotter = SQLDisPlotterSNS(
                    table_name='test_table',
                    required_cols=['value'],
                    where_clause='value > 0',
                    x='value',
                    kind='hist',
                    looper=LoopType.SingleLoop,
                )
                plotter._database = mock_db

                plotter.get_data_frame()
                mock_read_sql.assert_called_once()

                plotter.plot()
                mock_displot.assert_called_once_with(
                    data=mock_df,
                    x='value',
                    y=None,
                    hue=None,
                    row=None,
                    col=None,
                    palette=None,
                    kind='hist',
                    legend=True,
                    rug=False,
                    rug_kws=None,
                    facet_kws=None,
                )

    def test_hdf_retriever_catplot_composition(self):
        """Test composition of HDFDataRetriever with CatPlot."""

        class HDFCatPlotterSNS(HDFPdDataRetriever, CatPlot, SNSPlotter):
            pass

        test_file = Path('test.hdf')

        with patch.object(Path, 'is_file', return_value=True):
            with patch('pandas.read_hdf') as mock_read_hdf:
                with patch('seaborn.catplot') as mock_catplot:
                    mock_df = pd.DataFrame({'category': ['A', 'B'], 'value': [1, 2]})
                    mock_read_hdf.return_value = mock_df
                    mock_facet = Mock()
                    mock_catplot.return_value = mock_facet

                    plotter = HDFCatPlotterSNS(
                        hdf_filename=test_file,
                        key='data',
                        x='category',
                        y='value',
                        kind='box',
                        looper=LoopType.SingleLoop,
                    )

                    plotter.get_data_frame()
                    mock_read_hdf.assert_called_once_with(test_file, 'data')

                    plotter.plot()
                    mock_catplot.assert_called_once_with(
                        data=mock_df,
                        x='category',
                        y='value',
                        hue=None,
                        row=None,
                        col=None,
                        palette=None,
                        kind='box',
                        legend='auto',
                        native_scale=False,
                        facet_kws=None,
                    )

    def test_multiple_mixin_inheritance_order(self):
        """Test that mixin inheritance order is handled correctly."""

        class ComplexPlotterSNS(SQLPdDataRetriever, RelPlot, SNSPlotter):
            def patch_data_frame(self):
                # Custom implementation that should call super
                self.data_frame['new_col'] = 'test'
                super().patch_data_frame()

        mock_db = Mock()
        plotter = ComplexPlotterSNS(
            table_name='test', required_cols=['x', 'y'], database=mock_db, looper=LoopType.SingleLoop
        )

        # Test that all parent classes are properly initialized
        assert hasattr(plotter, 'table_name')
        assert hasattr(plotter, 'x')
        assert hasattr(plotter, 'data_frame')

    def test_composition_with_custom_methods(self):
        """Test composition with custom method overrides."""

        class CustomPlotterSNS(FromDatasetDataRetriever, RelPlot, SNSPlotter):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.custom_attr = 'test'
                self.i_item = 0

            def in_loop_customization(self):
                self.custom_attr = f'iteration_{self.i_item}'

            def customize_plot(self):
                if self.facet_grid:
                    self.facet_grid.figure.suptitle(self.custom_attr)

        with patch('seaborn.get_dataset_names', return_value=['tips']):
            plotter = CustomPlotterSNS(dataset_name='tips', looper=LoopType.SingleLoop)

            # Test custom initialization
            assert plotter.custom_attr == 'test'

            # Test custom method execution
            plotter.in_loop_customization()
            assert plotter.custom_attr == 'iteration_0'

            # Test that customize_plot doesn't fail
            plotter.facet_grid = Mock()
            plotter.customize_plot()


class TestEdgeCasesAndErrorHandling:
    """Test edge cases and error handling scenarios."""

    def test_generic_plotter_with_all_none_parameters(self):
        """Test SNSPlotter with all None parameters."""
        plotter = SNSPlotter(
            slicing_dict=None, grouping_columns=None, aggregation_functions=None, looper=LoopType.SingleLoop
        )

        assert plotter.slicing_dict is None
        assert plotter.grouping_columns is None
        assert plotter.aggregation_functions is None

    def test_generic_plotter_with_empty_dataframe_edge_cases(self):
        """Test behavior with various empty DataFrame scenarios."""
        plotter = SNSPlotter(looper=LoopType.SingleLoop)

        # Test with completely empty DataFrame
        plotter.data_frame = pd.DataFrame()
        plotter.slice_data_frame()
        plotter.group_and_aggregate_data_frame()

        # Test with DataFrame with columns but no rows
        plotter.data_frame = pd.DataFrame(columns=['x', 'y'])
        plotter.slice_data_frame()
        plotter.group_and_aggregate_data_frame()

    @patch('mafw.processor_library.sns_plotter.slice_data_frame')
    def test_slice_data_frame_with_complex_slicing_dict(self, mock_slice):
        """Test slice_data_frame with complex slicing dictionary."""
        complex_dict = {
            'category': ['A', 'B'],
            'value': lambda x: x > 5,
            'date': pd.date_range('2023-01-01', periods=3),
        }

        original_df = pd.DataFrame({'category': ['A', 'B', 'C'], 'value': [1, 6, 10]})
        sliced_df = pd.DataFrame({'category': ['A', 'B'], 'value': [1, 6]})
        mock_slice.return_value = sliced_df

        plotter = SNSPlotter(slicing_dict=complex_dict, looper=LoopType.SingleLoop)
        plotter.data_frame = original_df
        plotter.slice_data_frame()

        mock_slice.assert_called_once_with(original_df, complex_dict)

    def test_method_resolution_order(self):
        """Test that method resolution order works correctly in complex inheritance."""

        class MultiInheritancePlotterSNS(SQLPdDataRetriever, HDFPdDataRetriever, RelPlot, SNSPlotter):
            pass

        plotter = MultiInheritancePlotterSNS(looper=LoopType.SingleLoop)

        # Should have attributes from all parent classes
        assert hasattr(plotter, 'table_name')  # from SQLDataRetriever
        assert hasattr(plotter, 'hdf_filename')  # from HDFDataRetriever
        assert hasattr(plotter, 'x')  # from RelPlot
        assert hasattr(plotter, 'data_frame')  # from SNSPlotter

    @pytest.mark.parametrize(
        'backend,should_switch',
        [
            ('agg', False),
            ('tkagg', True),
            ('qt5agg', True),
        ],
    )
    @patch('mafw.processor_library.sns_plotter.plt')
    def test_backend_switching_scenarios(self, mock_plt, backend, should_switch):
        """Test various backend switching scenarios."""
        mock_plt.get_backend.return_value = 'Agg'

        plotter = SNSPlotter(matplotlib_backend=backend, looper=LoopType.SingleLoop)
        plotter.start()

        if should_switch:
            mock_plt.switch_backend.assert_called_once_with(backend)
        else:
            mock_plt.switch_backend.assert_not_called()


class TestProtocolImplementations:
    """Test that Protocol implementations work correctly."""

    def test_data_retriever_protocol_compliance(self):
        """Test that DataRetriever implementations comply with protocol."""

        # Test all DataRetriever implementations have required methods
        for cls in [FromDatasetDataRetriever, SQLPdDataRetriever, HDFPdDataRetriever]:
            instance = cls()
            assert hasattr(instance, 'get_data_frame')
            assert hasattr(instance, 'patch_data_frame')
            assert hasattr(instance, '_attributes_valid')

    def test_figure_plotter_protocol_compliance(self):
        """Test that FigurePlotter implementations comply with protocol."""

        # Test all FigurePlotter implementations have required methods
        for cls in [RelPlot, DisPlot, CatPlot, LMPlot]:
            instance = cls()
            assert hasattr(instance, 'plot')
            assert hasattr(instance, '_attributes_valid')

    def test_protocol_method_calls_super(self):
        """Test that protocol methods properly call super()."""

        class TestDataRetriever(PdDataRetriever):
            def __init__(self, *args, **kwargs):
                self.init_called = True
                super().__init__(*args, **kwargs)

            def patch_data_frame(self):
                self.patch_called = True
                super().patch_data_frame()

        class TestPlotterSNS(TestDataRetriever, SNSPlotter):
            def patch_data_frame(self):
                self.plotter_patch_called = True
                super().patch_data_frame()

        plotter = TestPlotterSNS(looper=LoopType.SingleLoop)
        assert plotter.init_called

        plotter.patch_data_frame()
        assert plotter.patch_called
        assert plotter.plotter_patch_called
