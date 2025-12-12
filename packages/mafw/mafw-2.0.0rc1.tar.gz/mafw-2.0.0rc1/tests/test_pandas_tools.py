#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Unit tests for pandas_tools module
"""

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from mafw.tools.pandas_tools import group_and_aggregate_data_frame, slice_data_frame


class TestSliceDataFrame:
    """Test class for slice_data_frame function"""

    @pytest.fixture
    def sample_dataframe(self):
        """Fixture providing a sample DataFrame for testing"""
        return pd.DataFrame(
            {
                'A': [1, 2, 3, 4, 5],
                'B': ['x', 'y', 'x', 'y', 'x'],
                'C': [10.1, 20.2, 30.3, 40.4, 50.5],
                'D': [True, False, True, False, True],
            }
        )

    @pytest.fixture
    def empty_dataframe(self):
        """Fixture providing an empty DataFrame for testing"""
        return pd.DataFrame({'A': [], 'B': [], 'C': []})

    def test_slice_with_single_condition_dict(self, sample_dataframe):
        """Test slicing with a single condition using dictionary"""

        result = slice_data_frame(sample_dataframe, {'A': 3})
        expected = sample_dataframe[sample_dataframe['A'] == 3]

        assert_frame_equal(result, expected)
        assert len(result) == 1
        assert result.iloc[0]['A'] == 3

    def test_slice_with_multiple_conditions_dict(self, sample_dataframe):
        """Test slicing with multiple conditions using dictionary"""

        result = slice_data_frame(sample_dataframe, {'A': 1, 'B': 'x'})
        expected = sample_dataframe[(sample_dataframe['A'] == 1) & (sample_dataframe['B'] == 'x')]

        assert_frame_equal(result, expected)
        assert len(result) == 1

    def test_slice_with_kwargs(self, sample_dataframe):
        """Test slicing using keyword arguments"""

        result = slice_data_frame(sample_dataframe, A=2, B='y')
        expected = sample_dataframe[(sample_dataframe['A'] == 2) & (sample_dataframe['B'] == 'y')]

        assert_frame_equal(result, expected)
        assert len(result) == 1

    def test_slice_kwargs_override_dict(self, sample_dataframe):
        """Test that kwargs override dictionary values"""

        result = slice_data_frame(sample_dataframe, {'A': 1}, A=3)
        expected = sample_dataframe[sample_dataframe['A'] == 3]

        assert_frame_equal(result, expected)
        assert len(result) == 1
        assert result.iloc[0]['A'] == 3

    def test_slice_with_none_dict(self, sample_dataframe):
        """Test slicing with None as slicing_dict"""

        result = slice_data_frame(sample_dataframe, None)

        assert_frame_equal(result, sample_dataframe)

    def test_slice_with_empty_dict(self, sample_dataframe):
        """Test slicing with empty dictionary"""

        result = slice_data_frame(sample_dataframe, {})

        assert_frame_equal(result, sample_dataframe)

    def test_slice_empty_dataframe(self, empty_dataframe):
        """Test slicing an empty DataFrame"""

        result = slice_data_frame(empty_dataframe, {'A': 1})

        assert_frame_equal(result, empty_dataframe)

    def test_slice_no_matching_rows(self, sample_dataframe):
        """Test slicing with conditions that match no rows"""

        result = slice_data_frame(sample_dataframe, {'A': 999})
        expected = sample_dataframe[sample_dataframe['A'] == 999]

        assert_frame_equal(result, expected)
        assert len(result) == 0

    def test_slice_with_boolean_column(self, sample_dataframe):
        """Test slicing with boolean column"""

        result = slice_data_frame(sample_dataframe, {'D': True})
        expected = sample_dataframe[sample_dataframe['D'] == True]  # noqa: E712

        assert_frame_equal(result, expected)
        assert len(result) == 3

    def test_slice_with_float_column(self, sample_dataframe):
        """Test slicing with float column"""

        result = slice_data_frame(sample_dataframe, {'C': 20.2})
        expected = sample_dataframe[sample_dataframe['C'] == 20.2]

        assert_frame_equal(result, expected)
        assert len(result) == 1

    def test_slice_invalid_column_raises_keyerror(self, sample_dataframe):
        """Test that slicing with invalid column raises KeyError"""

        with pytest.raises(KeyError):
            slice_data_frame(sample_dataframe, {'invalid_column': 1})

    @pytest.mark.parametrize(
        'slicing_condition,expected_length',
        [
            ({'A': 1}, 1),
            ({'B': 'x'}, 3),
            ({'D': False}, 2),
            ({'A': 1, 'B': 'x'}, 1),
            ({'A': 999}, 0),
        ],
    )
    def test_slice_parametrized(self, sample_dataframe, slicing_condition, expected_length):
        """Parametrized test for various slicing conditions"""

        result = slice_data_frame(sample_dataframe, slicing_condition)
        assert len(result) == expected_length


class TestGroupAndAggregateDataFrame:
    """Test class for group_and_aggregate_data_frame function"""

    @pytest.fixture
    def sample_dataframe_for_grouping(self):
        """Fixture providing a sample DataFrame for grouping tests"""
        return pd.DataFrame(
            {
                'category': ['A', 'B', 'A', 'B', 'A', 'C'],
                'subcategory': ['X', 'Y', 'X', 'Y', 'Z', 'X'],
                'value1': [10, 20, 30, 40, 50, 60],
                'value2': [1.1, 2.2, 3.3, 4.4, 5.5, 6.6],
                'count': [1, 1, 1, 1, 1, 1],
            }
        )

    def test_group_single_column_single_aggregation(self, sample_dataframe_for_grouping):
        """Test grouping by single column with single aggregation function"""

        result = group_and_aggregate_data_frame(sample_dataframe_for_grouping, ['category'], ['sum'])

        assert 'category' in result.columns
        # Only numeric columns should be present
        assert 'value1_sum' in result.columns
        assert 'value2_sum' in result.columns
        assert 'count_sum' in result.columns

        # String column should not be aggregated
        assert 'subcategory_sum' not in result.columns

        # Check specific values
        category_a_row = result[result['category'] == 'A'].iloc[0]
        assert category_a_row['value1_sum'] == 90  # 10 + 30 + 50
        assert category_a_row['count_sum'] == 3

    def test_group_multiple_columns_single_aggregation(self, sample_dataframe_for_grouping):
        """Test grouping by multiple columns with single aggregation function"""

        result = group_and_aggregate_data_frame(sample_dataframe_for_grouping, ['category', 'subcategory'], ['mean'])

        assert 'category' in result.columns
        assert 'subcategory' in result.columns
        # Only numeric columns should be aggregated
        assert 'value1_mean' in result.columns
        assert 'value2_mean' in result.columns
        assert 'count_mean' in result.columns

        # Should have 4 unique combinations
        assert len(result) == 4

    def test_group_single_column_multiple_aggregations(self, sample_dataframe_for_grouping):
        """Test grouping by single column with multiple aggregation functions"""

        result = group_and_aggregate_data_frame(sample_dataframe_for_grouping, ['category'], ['sum', 'mean', 'count'])

        assert 'category' in result.columns
        assert 'value1_sum' in result.columns
        assert 'value1_mean' in result.columns
        assert 'value1_count' in result.columns

        # subcategory column should not be present in result since it's a string column
        # and not used for grouping
        assert 'subcategory_sum' not in result.columns
        assert 'subcategory_mean' not in result.columns
        assert 'subcategory_count' not in result.columns

        # Check that we have 3 categories
        assert len(result) == 3

    def test_group_with_callable_aggregation(self, sample_dataframe_for_grouping):
        """Test grouping with callable aggregation function"""

        def custom_agg(x):
            return x.max() - x.min()

        result = group_and_aggregate_data_frame(sample_dataframe_for_grouping, ['category'], [custom_agg])

        assert 'category' in result.columns
        # Column names should include the function name
        assert any('custom_agg' in col for col in result.columns)

    def test_group_empty_grouping_columns(self, sample_dataframe_for_grouping):
        """Test with empty grouping columns list"""

        result = group_and_aggregate_data_frame(sample_dataframe_for_grouping, [], ['sum'])

        # Should return the original dataframe when no grouping columns
        assert_frame_equal(result, sample_dataframe_for_grouping)

    def test_group_excludes_string_columns(self, sample_dataframe_for_grouping):
        """Test that string columns are excluded from aggregation when not used for grouping"""

        result = group_and_aggregate_data_frame(sample_dataframe_for_grouping, ['category'], ['sum'])

        # Only numeric columns should be aggregated
        assert 'category' in result.columns  # grouping column
        assert 'value1_sum' in result.columns  # numeric column
        assert 'value2_sum' in result.columns  # numeric column
        assert 'count_sum' in result.columns  # numeric column

        # String column should be excluded from aggregation
        assert 'subcategory_sum' not in result.columns

    def test_group_with_only_string_columns_to_aggregate(self):
        """Test grouping when only string columns are available for aggregation"""

        df = pd.DataFrame(
            {'category': ['A', 'B', 'A', 'B'], 'text1': ['x', 'y', 'z', 'w'], 'text2': ['p', 'q', 'r', 's']}
        )

        result = group_and_aggregate_data_frame(df, ['category'], ['sum'])

        # Should return grouped categories with count since no numeric columns to aggregate
        assert 'category' in result.columns
        assert 'count' in result.columns
        assert len(result) == 2

    def test_group_with_mixed_string_and_callable_aggr(self, sample_dataframe_for_grouping):
        """Test grouping with mixed string and callable aggregations"""

        def range_func(x):
            return x.max() - x.min()

        result = group_and_aggregate_data_frame(
            sample_dataframe_for_grouping, ['category'], ['sum', 'mean', range_func]
        )

        assert 'category' in result.columns
        assert 'value1_sum' in result.columns
        assert 'value1_mean' in result.columns
        # Should have a column with the custom function name
        custom_cols = [col for col in result.columns if 'range_func' in col]
        assert len(custom_cols) > 0

    @pytest.mark.parametrize(
        'grouping_cols,agg_funcs,expected_groups',
        [
            (['category'], ['sum'], 3),
            (['category', 'subcategory'], ['mean'], 4),
            (['subcategory'], ['count'], 3),
        ],
    )
    def test_group_parametrized(self, sample_dataframe_for_grouping, grouping_cols, agg_funcs, expected_groups):
        """Parametrized test for various grouping scenarios"""

        result = group_and_aggregate_data_frame(sample_dataframe_for_grouping, grouping_cols, agg_funcs)

        assert len(result) == expected_groups
        # Check that grouping columns are present
        for col in grouping_cols:
            assert col in result.columns


class TestEdgeCases:
    """Test class for edge cases and error conditions"""

    @pytest.fixture
    def dataframe_with_duplicates(self):
        """Fixture providing a DataFrame with duplicate values"""
        return pd.DataFrame({'A': [1, 1, 2, 2, 3], 'B': ['x', 'x', 'y', 'y', 'z'], 'C': [10, 10, 20, 30, 40]})

    @pytest.fixture
    def dataframe_with_nulls(self):
        """Fixture providing a DataFrame with null values"""
        return pd.DataFrame(
            {'A': [1, 2, None, 4, 5], 'B': ['x', None, 'z', 'w', 'v'], 'C': [10.1, 20.2, 30.3, None, 50.5]}
        )

    def test_slice_with_duplicates(self, dataframe_with_duplicates):
        """Test slicing DataFrame with duplicate values"""

        result = slice_data_frame(dataframe_with_duplicates, {'A': 1})
        assert len(result) == 2
        assert all(result['A'] == 1)

    def test_slice_with_null_values(self, dataframe_with_nulls):
        """Test slicing DataFrame with null values"""

        # Test slicing with non-null value
        result = slice_data_frame(dataframe_with_nulls, {'A': 1})
        assert len(result) == 1
        assert result.iloc[0]['A'] == 1

    def test_group_with_null_values(self, dataframe_with_nulls):
        """Test grouping DataFrame with null values"""

        # Create a DataFrame without nulls in grouping column for this test
        df_no_null_groups = dataframe_with_nulls.dropna(subset=['B'])

        result = group_and_aggregate_data_frame(df_no_null_groups, ['B'], ['count'])

        assert len(result) >= 1
        assert 'B' in result.columns

    def test_slice_preserves_dataframe_structure(self):
        """Test that slicing preserves DataFrame structure and dtypes"""

        df = pd.DataFrame(
            {
                'int_col': [1, 2, 3],
                'float_col': [1.1, 2.2, 3.3],
                'str_col': ['a', 'b', 'c'],
                'bool_col': [True, False, True],
            }
        )

        result = slice_data_frame(df, {'int_col': 2})

        # Check that dtypes are preserved
        assert result['int_col'].dtype == df['int_col'].dtype
        assert result['float_col'].dtype == df['float_col'].dtype
        assert result['str_col'].dtype == df['str_col'].dtype
        assert result['bool_col'].dtype == df['bool_col'].dtype

    def test_group_column_naming_edge_cases(self):
        """Test column naming in grouping with edge cases"""

        df = pd.DataFrame(
            {'group_col': ['A', 'A', 'B'], 'value_col_with_underscore': [1, 2, 3], 'another_value': [10, 20, 30]}
        )

        result = group_and_aggregate_data_frame(df, ['group_col'], ['sum', 'mean'])

        # Check that column names are properly formatted
        expected_cols = [
            'group_col',
            'value_col_with_underscore_sum',
            'value_col_with_underscore_mean',
            'another_value_sum',
            'another_value_mean',
        ]

        for col in expected_cols:
            assert col in result.columns

    def test_empty_dataframe_grouping(self):
        """Test grouping an empty DataFrame"""

        df = pd.DataFrame({'A': [], 'B': [], 'C': []})

        result = group_and_aggregate_data_frame(df, ['A'], ['sum'])

        # Should return empty DataFrame with proper structure
        assert len(result) == 0
        assert 'A' in result.columns
