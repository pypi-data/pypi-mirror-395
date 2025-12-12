#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
A collection of useful convenience functions for common pandas operations
"""

import typing
import warnings
from collections.abc import Callable, Iterable, MutableMapping
from typing import Any

from mafw.decorators import depends_on_optional
from mafw.mafw_errors import MissingOptionalDependency

try:
    import pandas as pd

    @depends_on_optional(module_name='pandas')
    def slice_data_frame(
        input_data_frame: pd.DataFrame, slicing_dict: MutableMapping[str, Any] | None = None, **kwargs: Any
    ) -> pd.DataFrame:
        """
        Slice a data frame according to `slicing_dict`.

        The input data frame will be sliced using the items of the `slicing_dict` applying the loc operator in this way:
        :python:`sliced = input_data_frame[(input_data_frame[key]==value)]`.

        If the slicing_dict is empty, then the full input_data_frame is returned.

        Instead of the slicing_dict, the user can also provide key and value pairs as keyword arguments.

        :python:`slice_data_frame(data_frame, {'A':14})`

        is equivalent to

        :python:`slice_data_frame(data_frame, A=14)`.

        If the user provides a keyword argument that also exists in the slicing_dict, then the keyword argument will update
        the slicing_dict.

        No checks on the column name is done, should a label be missing, the loc method will raise a KeyError.

        :param input_data_frame: The data frame to be sliced.
        :type input_data_frame: pd.DataFrame
        :param slicing_dict: A dictionary with columns and values for the slicing. Defaults to None
        :type slicing_dict: dict, Optional
        :param kwargs: Keyword arguments to be used instead of the slicing dictionary.
        :return: The sliced dataframe
        :rtype: pd.DataFrame
        """
        if slicing_dict is None:
            slicing_dict = {}

        slicing_dict.update(kwargs)

        if not slicing_dict or len(input_data_frame) == 0:
            return input_data_frame

        sliced: pd.DataFrame = input_data_frame
        for key, value in slicing_dict.items():
            sliced = sliced.loc[(sliced[key] == value)]

        return sliced

    @depends_on_optional(module_name='pandas')
    def group_and_aggregate_data_frame(
        data_frame: pd.DataFrame,
        grouping_columns: Iterable[str],
        aggregation_functions: Iterable[str | Callable[[Any], Any]],
    ) -> pd.DataFrame:
        """
        Utility function to perform dataframe groupby and aggregation.

        This function is a simple wrapper to perform group by and aggregation operations on a dataframe. The user must
        provide a list of columns to perform the group by on and a list of functions for the aggregation of the other
        columns.

        The output dataframe will have the aggregated columns renamed as originalname_aggregationfunction.

        .. note::
            Only numeric columns (and columns that can be aggregated) will be included in the aggregation.
            String columns that are not used for grouping will be automatically excluded from aggregation.

        :param data_frame: The input data frame
        :type data_frame: pandas.DataFrame
        :param grouping_columns: The list of columns to group by on.
        :type grouping_columns: Iterable[str]
        :param aggregation_functions: The list of functions to be used for the aggregation of the not grouped columns.
        :type aggregation_functions: Iterable[str | Callable[[Any], Any]
        :return: The aggregated dataframe after the groupby operation.
        :rtype: pandas.DataFrame
        """
        # typing of this function is a nightmare.
        # I have not understood anything about these errors
        if grouping_columns:
            grouped_df = data_frame.groupby(grouping_columns)  # type: ignore

            # Get columns that are not used for grouping
            grouping_columns_list = list(grouping_columns)
            non_grouping_columns = [col for col in data_frame.columns if col not in grouping_columns_list]

            # Filter to only numeric/aggregatable columns
            # We'll try to aggregate only numeric columns and datetime columns
            aggregatable_columns = []
            for col in non_grouping_columns:
                if pd.api.types.is_numeric_dtype(data_frame[col]) or pd.api.types.is_datetime64_any_dtype(
                    data_frame[col]
                ):
                    aggregatable_columns.append(col)

            # If we have aggregatable columns, perform aggregation on them
            if aggregatable_columns:
                aggregated_df = typing.cast(
                    pd.DataFrame, grouped_df[aggregatable_columns].agg(aggregation_functions).reset_index()
                )
                chain = '_'
                aggregated_df.columns = [chain.join(col).strip(chain) for col in aggregated_df.columns.values]  # type: ignore
            else:
                # If no aggregatable columns, just return the grouped columns with their unique combinations
                aggregated_df = typing.cast(pd.DataFrame, grouped_df.size().reset_index(name='count'))

        else:
            aggregated_df = data_frame

        return aggregated_df

except ImportError:
    msg = (
        'Trying to use the seaborn Plotter implementation without having installed the required dependencies.\n'
        'Consider installing mafw with the optional feature seaborn. For example:\n'
        '\npip install mafw[seaborn]\n\n'
    )
    warnings.warn(MissingOptionalDependency(msg), stacklevel=2)
    raise
