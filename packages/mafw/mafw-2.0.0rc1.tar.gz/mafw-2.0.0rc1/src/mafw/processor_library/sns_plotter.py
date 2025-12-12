#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Module implements a Seaborn plotter processor with a mixin structure to generate seaborn plots.

This module implements the :mod:`.abstract_plotter` functionalities using :link:`seaborn` and :link:`pandas`.

These two packages are not installed in the default installation of MAFw, unless the user decided to include the
optional feature `seaborn`.

Along with the :class:`SNSPlotter`, it includes a set of standard data retriever specific for pandas data frames.
"""

import logging
import re
import typing
import warnings
from collections.abc import Callable, Iterable, Mapping, MutableMapping, Sequence
from pathlib import Path
from typing import Any, TypeAlias

import peewee

from mafw.decorators import class_depends_on_optional, processor_depends_on_optional
from mafw.mafw_errors import MissingOptionalDependency, PlotterMixinNotInitialized
from mafw.processor_library.abstract_plotter import DataRetriever, FigurePlotter, GenericPlotter

log = logging.getLogger(__name__)

try:
    import matplotlib.colors
    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sns
    from matplotlib.typing import ColorType
    from seaborn._core.typing import ColumnName

    from mafw.tools.pandas_tools import group_and_aggregate_data_frame, slice_data_frame

    # noinspection PyProtectedMember
    _Palette: TypeAlias = str | Sequence[ColorType] | Mapping[Any, ColorType]

    @class_depends_on_optional('pandas')
    class PdDataRetriever(DataRetriever):
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, **kwargs)
            self.data_frame: pd.DataFrame

        def get_data_frame(self) -> None:
            pass

        def patch_data_frame(self) -> None:
            super().patch_data_frame()  # type: ignore[safe-super]

        def _attributes_valid(self) -> bool:
            return True

    @class_depends_on_optional('pandas')
    class FromDatasetDataRetriever(PdDataRetriever):
        """
        A data retriever to get a dataframe from a seaborn dataset
        """

        def __init__(self, dataset_name: str | None = None, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, **kwargs)
            self.dataset_name = dataset_name if dataset_name is not None else ''

        def _attributes_valid(self) -> bool:
            """Checks if the attributes of the mixin are all valid"""
            if self.dataset_name == '':
                return False

            return self.dataset_name in sns.get_dataset_names()

        def get_data_frame(self) -> None:
            """Gets the data frame from the standard seaborn datasets"""
            if not self._attributes_valid():
                raise PlotterMixinNotInitialized()
            self.data_frame = sns.load_dataset(self.dataset_name)

    @class_depends_on_optional('pandas')
    class SQLPdDataRetriever(PdDataRetriever):
        """
        A specialized data retriever to get a data frame from a database table.

        The idea is to implement an interface to the pandas ``read_sql``. The user has to provide the :attr:`table name
        <.table_name>`, the :attr:`the list of required columns <.required_columns>` and an optional :attr:`where clause
        <.where_clause>`.
        """

        database: peewee.Database
        """The database instance. It comes from the main class"""

        def __init__(
            self,
            table_name: str | None = None,
            required_cols: Iterable[str] | str | None = None,
            where_clause: str | None = None,
            *args: Any,
            **kwargs: Any,
        ) -> None:
            """
            Constructor parameters:

            :param table_name: The name of the table from where to get the data
            :type table_name: str, Optional
            :param required_cols: A list of columns to be selected from the table and transferred as column in the dataframe.
            :type required_cols:  Iterable[str] | str | None, Optional
            :param where_clause: The where clause used in the select SQL statement. If None is provided, then all rows will
                be selected.
            :type where_clause: str, Optional
            """
            super().__init__(*args, **kwargs)
            self.table_name: str
            """The table from where the data should be taken."""
            if table_name is None:
                self.table_name = ''
            else:
                self.table_name = table_name

            self.required_columns: Iterable[str]
            """
            The iterable of columns.
    
            Those are the column names to be selected from the :attr:`~.table_name` and included in the dataframe. 
            """
            if required_cols is None:
                self.required_columns = []
            elif isinstance(required_cols, str):
                self.required_columns = [required_cols]
            else:
                self.required_columns = required_cols

            self.where_clause: str
            """The where clause of the SQL statement"""

            if where_clause is None:
                self.where_clause = '1'
            else:
                self.where_clause = where_clause

        def get_data_frame(self) -> None:
            """
            Retrieve the dataframe from a database table.

            :raise PlotterMixinNotInitialized: If some of the required attributes are missing.
            """
            if not self._attributes_valid():
                raise PlotterMixinNotInitialized

            if isinstance(self.required_columns, str):
                self.required_columns = [self.required_columns]

            if self.where_clause == '':
                where_clause = ' 1 '
            else:
                where_clause = self.where_clause.strip()
                m = re.match('where', where_clause, re.I)
                if m:
                    where_clause = where_clause.replace(m[0], '').strip()

            # todo:
            #   sqlite does not allow to have column and table names parametrized.
            #   so we need to concatenate the strings.
            #   see https://www.sqlite.org/cintro.html#binding_parameters_and_reusing_prepared_statements
            #   we should actually do a check for SQL injection for those elements, but I have no idea at the moment how
            #   this could be implemented.
            sql = f'SELECT {", ".join(self.required_columns)} FROM {self.table_name} WHERE ?'
            params = (where_clause,)

            data_frame = pd.read_sql(sql, con=self.database.connection(), params=params)  # type: ignore[no-untyped-call]

            self.data_frame = data_frame

        def _attributes_valid(self) -> bool:
            """Check if all required parameters are provided and valid."""
            if self.table_name == '':
                return False
            if not self.required_columns:
                return False
            return True

    @class_depends_on_optional('pandas')
    class HDFPdDataRetriever(DataRetriever):
        """
        Retrieve a data frame from a HDF file

        This data retriever is getting a dataframe from a HDF file provided the filename and the object key.
        """

        def __init__(
            self, hdf_filename: str | Path | None = None, key: str | None = None, *args: Any, **kwargs: Any
        ) -> None:
            """
            Constructor parameters:

            :param hdf_filename: The filename of the HDF file
            :type hdf_filename: str | Path, Optional
            :param key: The key of the HDF store with the dataframe
            :type key: str, Optional
            """
            super().__init__(*args, **kwargs)
            self.hdf_filename: Path
            if hdf_filename is None:
                self.hdf_filename = Path()
            else:
                self.hdf_filename = Path(hdf_filename)

            self.key: str
            if key is None:
                self.key = ''
            else:
                self.key = key

        def get_data_frame(self) -> None:
            """
            Retrieve the dataframe from a HDF file

            :raise PlotterMixinNotInitialized: if some of the required attributes are not initialised or invalid.
            """
            if not self._attributes_valid():
                raise PlotterMixinNotInitialized

            self.data_frame = typing.cast(pd.DataFrame, pd.read_hdf(self.hdf_filename, self.key))

        def patch_data_frame(self) -> None:
            super().patch_data_frame()  # type: ignore[safe-super]

        def _attributes_valid(self) -> bool:
            if self.hdf_filename == Path():
                return False
            elif not self.hdf_filename.is_file():
                # hdf is not a file or it does not exist.
                log.warning('%s is not a valid HDF file' % self.hdf_filename)
                return False

            if self.key == '':
                return False

            return True

    @class_depends_on_optional('seaborn;pandas')
    class SNSFigurePlotter(FigurePlotter):
        """Base mixin class to generate a seaborn Figure level plot"""

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            self.data_frame: pd.DataFrame
            """The dataframe instance shared with the main class"""
            self.facet_grid: sns.FacetGrid
            """The facet grid instance shared with the main class"""
            super().__init__(*args, **kwargs)

        def plot(self) -> None:
            pass

        def _attributes_valid(self) -> bool:
            return True

    @class_depends_on_optional('seaborn;pandas')
    class RelPlot(SNSFigurePlotter):
        """
        The relational plot mixin.

        This mixin will produce either a scatter or a line figure level plot.

        The full documentation of the relplot object can be read at `this link <https://seaborn.pydata.org/generated/seaborn.relplot.html>`_.
        """

        def __init__(
            self,
            x: ColumnName | Iterable[float | complex | int] | None = None,
            y: ColumnName | Iterable[float | complex | int] | None = None,
            hue: ColumnName | Iterable[float | complex | int] | None = None,
            row: ColumnName | Iterable[float | complex | int] | None = None,
            col: ColumnName | Iterable[float | complex | int] | None = None,
            palette: _Palette | matplotlib.colors.Colormap | None = None,
            kind: typing.Literal['scatter', 'line'] = 'scatter',
            legend: typing.Literal['auto', 'brief', 'full'] | bool = 'auto',
            plot_kws: Mapping[str, Any] | None = None,
            facet_kws: dict[str, Any] | None = None,
            *args: Any,
            **kwargs: Any,
        ) -> None:
            """
            Constructor parameters:

            :param x: The name of the x variable or an iterable containing the x values.
            :type x: str | Iterable, Optional
            :param y: The name of the y variable or an iterable containing the y values.
            :type y: str | Iterable, Optional
            :param hue: The name of the hue variable or an iterable containing the hue values.
            :type hue: str | Iterable, Optional
            :param row: The name of the row category or an iterable containing the row values.
            :type row: str | Iterable, Optional
            :param col: The name of the column category or an iterable containing the column values.
            :type col: str | Iterable, Optional
            :param palette: The colour palette to be used.
            :type palette: str | Colormap, Optional
            :param kind: The type of relational plot (scatter or line). Defaults to scatter.
            :type kind: str, Optional
            :param legend: How to draw the legend. If “brief”, numeric hue and size variables will be represented with a
                sample of evenly spaced values. If “full”, every group will get an entry in the legend.
                If “auto”, choose between brief or full representation based on number of levels.
                If False, no legend data is added and no legend is drawn. Defaults to auto.
            :type legend: str | bool, Optional
            :param plot_kws: A dictionary like list of keywords passed to the underlying `seaborn.relplot
                <https://seaborn.pydata.org/generated/seaborn.relplot.html#seaborn.relplot>`_.
            :type plot_kws: dict[str, Any], Optional
            :param facet_kws: A dictionary like list of keywords passed to the underlying
                `seaborn.FacetGrid <https://seaborn.pydata.org/generated/seaborn.FacetGrid.html#seaborn-facetgrid>`_
            :type facet_kws: dict[str, Any], Optional
            """
            super().__init__(*args, **kwargs)
            self.x = x
            self.y = y
            self.hue = hue
            self.row = row
            self.col = col
            self.palette = palette
            self.kind = kind
            self.legend = legend
            self.plot_kws = plot_kws if plot_kws is not None else {}
            self.facet_kws = facet_kws

        def plot(self) -> None:
            """Implements the plot method of a figure-level relational graph."""
            self.facet_grid = sns.relplot(
                data=self.data_frame,
                x=self.x,
                y=self.y,
                hue=self.hue,
                row=self.row,
                col=self.col,
                palette=self.palette,
                kind=self.kind,
                legend=self.legend,
                facet_kws=self.facet_kws,
                **self.plot_kws,
            )

    @class_depends_on_optional('seaborn;pandas')
    class DisPlot(SNSFigurePlotter):
        """
        The distribution plot mixin.

        This mixin is the MAFw implementation of the `seaborn displot
        <https://seaborn.pydata.org/generated/seaborn.displot.html#seaborn.displot>`_ and will produce one of the following figure level plots:

        * **histplot**: a simple `histogram
          plot <https://seaborn.pydata.org/generated/seaborn.histplot.html#seaborn.histplot>`_

        * **kdeplot**: a `kernel density <https://seaborn.pydata.org/generated/seaborn.kdeplot.html#seaborn.kdeplot>`_
          estimate plot

        * **ecdfplot**: an `empirical cumulative distribution functions
          <https://seaborn.pydata.org/generated/seaborn.ecdfplot.html#seaborn.ecdfplot>`_  plot

        * **rugplot**: a plot of the `marginal distributions
          <https://seaborn.pydata.org/generated/seaborn.rugplot.html#seaborn.rugplot>`_ as ticks.
        """

        def __init__(
            self,
            x: ColumnName | Iterable[float | complex | int] | None = None,
            y: ColumnName | Iterable[float | complex | int] | None = None,
            hue: ColumnName | Iterable[float | complex | int] | None = None,
            row: ColumnName | Iterable[float | complex | int] | None = None,
            col: ColumnName | Iterable[float | complex | int] | None = None,
            palette: _Palette | matplotlib.colors.Colormap | None = None,
            kind: typing.Literal['hist', 'kde', 'ecdf'] = 'hist',
            legend: bool = True,
            rug: bool = False,
            rug_kws: dict[str, Any] | None = None,
            plot_kws: Mapping[str, Any] | None = None,
            facet_kws: dict[str, Any] | None = None,
            *args: Any,
            **kwargs: Any,
        ):
            """
            Constructor parameters:

            :param x: The name of the x variable or an iterable containing the x values.
            :type x: str | Iterable, Optional
            :param y: The name of the y variable or an iterable containing the y values.
            :type y: str | Iterable, Optional
            :param hue: The name of the hue variable or an iterable containing the hue values.
            :type hue: str | Iterable, Optional
            :param row: The name of the row category or an iterable containing the row values.
            :type row: str | Iterable, Optional
            :param col: The name of the column category or an iterable containing the column values.
            :type col: str | Iterable, Optional
            :param palette: The colour palette to be used.
            :type palette: str | Colormap, Optional
            :param kind: The type of distribution plot (hist, kde or ecdf). Defaults to hist.
            :type kind: str, Optional
            :param legend: If false, suppress the legend for the semantic variables. Defaults to True.
            :type legend: bool, Optional
            :param rug: If true, show each observation with marginal ticks. Defaults to False.
            :type rug: bool, Optional
            :param rug_kws: Parameters to control the appearance of the rug plot.
            :type rug_kws: Mapping[str, Any], Optional
            :param plot_kws: Parameters passed to the underlying plotting object.
            :type plot_kws: Mapping[str, Any], Optional
            :param facet_kws: Parameters passed to the facet grid object.
            :type facet_kws: Mapping[str, Any], Optional
            """
            super().__init__(*args, **kwargs)
            self.x = x
            self.y = y
            self.hue = hue
            self.row = row
            self.col = col
            self.palette = palette
            self.kind = kind
            self.legend = legend
            self.rug = rug
            self.rug_kws = rug_kws
            self.plot_kws = plot_kws if plot_kws is not None else {}
            self.facet_kws = facet_kws

        def plot(self) -> None:
            """Implements the plot method for a figure-level distribution graph"""
            self.facet_grid = sns.displot(
                data=self.data_frame,
                x=self.x,
                y=self.y,
                hue=self.hue,
                row=self.row,
                col=self.col,
                palette=self.palette,
                kind=self.kind,
                legend=self.legend,
                rug=self.rug,
                rug_kws=self.rug_kws,
                facet_kws=self.facet_kws,
                **self.plot_kws,
            )

    @class_depends_on_optional('seaborn;pandas')
    class CatPlot(SNSFigurePlotter):
        """
        The categorical plot mixin.

        This mixin will produce a figure level categorical plot as described `here
        <https://seaborn.pydata.org/generated/seaborn.catplot.html>`_.

        .. note:

            By default this function treats one of the variables (typically x) as categorical, this means that even if
            this variable is numeric, its value will not be considered. If you want to use the actual value of this
            categorical variable, set native_scale = True.
        """

        def __init__(
            self,
            x: ColumnName | Iterable[float | complex | int] | None = None,
            y: ColumnName | Iterable[float | complex | int] | None = None,
            hue: ColumnName | Iterable[float | complex | int] | None = None,
            row: ColumnName | Iterable[float | complex | int] | None = None,
            col: ColumnName | Iterable[float | complex | int] | None = None,
            palette: _Palette | None = None,
            kind: typing.Literal['strip', 'swarm', 'box', 'violin', 'boxen', 'point', 'bar', 'count'] = 'strip',
            legend: typing.Literal['auto', 'brief', 'full'] | bool = 'auto',
            native_scale: bool = False,
            plot_kws: Mapping[str, Any] | None = None,
            facet_kws: dict[str, Any] | None = None,
            *args: Any,
            **kwargs: Any,
        ) -> None:
            """
            Constructor parameters:

            :param x: The name of the x variable or an iterable containing the x values.
            :type x: str | Iterable, Optional
            :param y: The name of the y variable or an iterable containing the y values.
            :type y: str | Iterable, Optional
            :param hue: The name of the hue variable or an iterable containing the hue values.
            :type hue: str | Iterable, Optional
            :param row: The name of the row category or an iterable containing the row values.
            :type row: str | Iterable, Optional
            :param col: The name of the column category or an iterable containing the column values.
            :type col: str | Iterable, Optional
            :param palette: The colour palette to be used.
            :type palette: str, Optional
            :param kind: The type of relational plot (scatter or line). Defaults to scatter.
            :type kind: str, Optional
            :param legend: How to draw the legend. If “brief”, numeric hue and size variables will be represented with a
                sample of evenly spaced values. If “full”, every group will get an entry in the legend.
                If “auto”, choose between brief or full representation based on number of levels.
                If False, no legend data is added and no legend is drawn. Defaults to auto.
            :type legend: str | bool, Optional
            :param native_scale: When True, numeric or datetime values on the categorical axis will maintain their original
                scaling rather than being converted to fixed indices. Defaults to False.
            :type native_scale: bool, Optional
            :param plot_kws: A dictionary like list of keywords passed to the underlying `seaborn.catplot
                <https://seaborn.pydata.org/generated/seaborn.relplot.html#seaborn.catplot>`_.
            :type plot_kws: dict[str, Any], Optional
            :param facet_kws: A dictionary like list of keywords passed to the underlying
                `seaborn.FacetGrid <https://seaborn.pydata.org/generated/seaborn.FacetGrid.html#seaborn-facetgrid>`_
            :type facet_kws: dict[str, Any], Optional
            """
            super().__init__(*args, **kwargs)
            self.x = x
            self.y = y
            self.hue = hue
            self.row = row
            self.col = col
            self.palette = palette
            self.kind = kind
            self.legend = legend
            self.native_scale = native_scale
            self.plot_kws = plot_kws if plot_kws is not None else {}
            self.facet_kws = facet_kws

        def plot(self) -> None:
            """Implements the plot method of a figure-level categorical graph."""
            self.facet_grid = sns.catplot(
                data=self.data_frame,
                x=self.x,
                y=self.y,
                hue=self.hue,
                row=self.row,
                col=self.col,
                palette=self.palette,
                kind=self.kind,
                legend=self.legend,
                native_scale=self.native_scale,
                facet_kws=self.facet_kws,
                **self.plot_kws,
            )

    class LMPlot(SNSFigurePlotter):
        """
        The linear regression model plot mixin.

        This mixin will produce a figure level regression model as described `here <https://seaborn.pydata.org/generated/seaborn.lmplot.html#seaborn.lmplot>`__
        """

        def __init__(
            self,
            x: str | None = None,
            y: str | None = None,
            hue: str | None = None,
            row: str | None = None,
            col: str | None = None,
            palette: _Palette | None = None,
            legend: bool = True,
            scatter_kws: dict[str, Any] | None = None,
            line_kws: dict[str, Any] | None = None,
            facet_kws: dict[str, Any] | None = None,
            *args: Any,
            **kwargs: Any,
        ) -> None:
            """
            Constructor parameters:

            :param x: The name of the x variable or an iterable containing the x values.
            :type x: str, Optional
            :param y: The name of the y variable or an iterable containing the y values.
            :type y: str, Optional
            :param hue: The name of the hue variable or an iterable containing the hue values.
            :type hue: str, Optional
            :param row: The name of the row category or an iterable containing the row values.
            :type row: str, Optional
            :param col: The name of the column category or an iterable containing the column values.
            :type col: str, Optional
            :param palette: The colour palette to be used.
            :type palette: str, Optional
            :param legend: If True and there is a hue variable, add a legend.
            :type legend: bool, Optional
            :param scatter_kws: A dictionary like list of keywords passed to the underlying `scatter
                <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.scatter.html#matplotlib.pyplot.scatter>`_.
            :type scatter_kws: dict[str, Any], Optional
            :param scatter_kws: A dictionary like list of keywords passed to the underlying `scatter
                <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.scatter.html#matplotlib.pyplot.scatter>`_.
            :type line_kws: dict[str, Any], Optional
            :param line_kws: A dictionary like list of keywords passed to the underlying `plot
                <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html#matplotlib.pyplot.plot>`_.
            :param facet_kws: A dictionary like list of keywords passed to the underlying
                `seaborn.FacetGrid <https://seaborn.pydata.org/generated/seaborn.FacetGrid.html#seaborn-facetgrid>`_
            :type facet_kws: dict[str, Any], Optional
            """
            super().__init__(*args, **kwargs)
            self.x = x
            self.y = y
            self.hue = hue
            self.row = row
            self.col = col
            self.palette = palette
            self.legend = legend
            self.scatter_kws = scatter_kws
            self.line_kws = line_kws
            self.facet_kws = facet_kws
            self.other_kws = kwargs

        def plot(self) -> None:
            """Implements the plot method for a figure-level regression model."""
            self.facet_grid = sns.lmplot(
                data=self.data_frame,
                x=self.x,
                y=self.y,
                hue=self.hue,
                row=self.row,
                col=self.col,
                palette=self.palette,
                legend=self.legend,
                scatter_kws=self.scatter_kws,
                line_kws=self.line_kws,
                facet_kws=self.facet_kws,
                **self.other_kws,
            )

    @processor_depends_on_optional(module_name='pandas;seaborn', warn=True, raise_ex=False)
    class SNSPlotter(GenericPlotter):
        """
        The Generic Plotter processor.

        This is a subclass of a Processor with advanced functionality to fetch data in the form of a dataframe and to
        produce plots.

        The key difference with respect to a normal processor is it :meth:`.process` method that has been already
        implemented as follows:

        .. literalinclude:: ../../../src/mafw/processor_library/sns_plotter.py
            :pyobject: SNSPlotter.process
            :dedent:

        This actually means that when you are subclassing a SNSPlotter you do not have to implement the process method
        as you would do for a normal Processor, but you will have to implement the following methods:

            * :meth:`~.in_loop_customization`.

                The processor execution workflow (LoopType) can be any of the available, so
                actually the process method might be invoked only once, or multiple times inside a loop structure
                (for or while).
                If the execution is cyclic, then you may want to have the possibility to do some customisation for each
                iteration, for example, changing the plot title, or modifying the data selection, or the filename where the
                plots will be saved.

                You can use this method also in case of a single loop processor, in this case you will not have access to
                the loop parameters.

            * :meth:`~.get_data_frame`.

                This method has the task to get the data to be plotted in the form of a pandas DataFrame. The processor has
                the :attr:`~.data_frame` attribute where the data will be stored to make them accessible from all other
                methods.

            * :meth:`~.GenericPlotter.patch_data_frame`.

                A convenient method to apply data frame manipulation to the data just retrieved.

            * :meth:`~.GenericPlotter.plot`.

                This method is where the actual plotting occurs. Use the :attr:`~.data_frame` to plot the quantities
                you want.

            * :meth:`~.customize_plot`.

                This method can be optionally used to customize the appearance of the facet grid produced by the
                :meth:`~.GenericPlotter.plot` method. It is particularly useful when the user is mixing this class with one of the
                :class:`~.FigurePlotter` mixin, thus not having direct access to the plot method.

            * :meth:`~.save`.

                This method is where the produced plot is saved in a file. Remember to append the output file name to the
                :attr:`list of produced outputs <.output_filename_list>` so that the :meth:`~.GenericPlotter._update_plotter_db` method
                will automatically store this file in the database during the :meth:`~.GenericPlotter.finish` execution.

            * :meth:`~.update_db`.

                If the user wants to update a specific table in the database, they can use this method.

                It is worth reminding that all plotters are saving all generated files in the standard table PlotterOutput.
                This is automatically done by the :meth:`~.GenericPlotter._update_plotter_db` method that is called in the
                :meth:`~.GenericPlotter.finish` method.

        You do not need to overload the :meth:`~.slice_data_frame` nor the :meth:`~.group_and_aggregate_data_frame`
        methods, but you can simply use them by setting the :attr:`~.slicing_dict` and the :attr:`~.grouping_columns`
        and the :attr:`~.aggregation_functions`.

        The processor comes with two processors parameters that can be used by user-defined subclasses:

            1. The output_folder that is the path where the output file will be saved
            2. The force_replot flag to be used whether the user wants the plot to be regenerated even if the output
               file already exists.

        The default value of these parameters can be changed using the :attr:`.Processor.new_defaults` dictionary as
        shown in :ref:`this example <parameter_inheritance>`.
        """

        def __init__(
            self,
            slicing_dict: MutableMapping[str, Any] | None = None,
            grouping_columns: Iterable[str] | None = None,
            aggregation_functions: Iterable[str | Callable[[Any], Any]] | None = None,
            matplotlib_backend: str = 'agg',
            *args: Any,
            **kwargs: Any,
        ) -> None:
            """
            Constructor parameters:

            :param slicing_dict: A dictionary with key, value pairs to slice the input data frame before the plotting
                occurs.
            :type slicing_dict: dict[str, Any], Optional
            :param grouping_columns: A list of columns for the groupby operation on the data frame.
            :type grouping_columns: list[str], Optional
            :param aggregation_functions: A list of functions for the aggregation on the grouped data frame.
            :type aggregation_functions: list[str | Callable[[Any], Any], Optional
            :param matplotlib_backend: The name of the matplotlib backend to be used. Defaults to 'Agg'
            :type matplotlib_backend: str, Optional
            :param output_folder: The path where the output file will be saved
            :type output_folder: Path, Optional
            :param force_replot: Whether to force re-plotting even if the output file already exists.
            :type force_replot: bool, Optional
            """
            super().__init__(*args, **kwargs)

            # attributes that can be set in the constructor

            self.slicing_dict: MutableMapping[str, Any] | None = slicing_dict
            """The dictionary for slicing the input data frame"""

            self.grouping_columns: Iterable[str] | None = grouping_columns
            """The list of columns for grouping the data frame"""

            self.aggregation_functions: Iterable[str | Callable[[Any], Any]] | None = aggregation_functions
            """The list of aggregation functions to be applied to the grouped dataframe"""

            self.matplotlib_backend: str = matplotlib_backend.lower()
            """The backend to be used for matplotlib."""

            # internal use attributes.

            self.data_frame: pd.DataFrame = pd.DataFrame()
            """The pandas DataFrame containing the data to be plotted."""

            self.output_filename_list: list[Path] = []
            """The list of produced filenames."""

            self.facet_grid: sns.FacetGrid | None = None
            """The reference to the facet grid."""

            # private attributes

            # be sure that some additional methods if implemented are calling the super.
            # TODO: check if this is really needed
            self._methods_to_be_checked_for_super.extend([('patch_data_frame', SNSPlotter)])  # type: ignore[list-item]

        def start(self) -> None:
            """
            Overload of the start method.

            The :class:`~.SNSPlotter` is overloading the :meth:`~.Processor.start` in order to allow the user to
            change the matplotlib backend.

            The user can selected which backend to use either directly in the class constructor or assign it to the class
            attribute :attr:`~.matplotlib_backend`.
            """
            super().start()
            try:
                if plt.get_backend().lower() != self.matplotlib_backend:
                    plt.switch_backend(self.matplotlib_backend)
            except ModuleNotFoundError:
                log.critical('%s is not a valid plt backend' % self.matplotlib_backend)
                raise

        def get_data_frame(self) -> None:
            """
            Specific implementation of the get data frame for the Seaborn plotter.

            It must be overloaded.

            The method is **NOT** returning the data_frame, but in your implementation you need to assign the data frame
            to the class :attr:`.data_frame` attribute.
            """
            pass

        def process(self) -> None:
            """
            Specific implementation of the process method for the Seaborn plotter.

            It is almost the same as the GenericProcessor, with the addition that all open pyplot figures are closed
            after the process is finished.

            This part cannot be moved upward to the :class:`~.GenericPlotter` because the user might have selected
            another plotting library different from :link:`matplotlib`.
            """
            super().process()
            if not self.is_data_frame_empty():
                plt.close('all')

        def group_and_aggregate_data_frame(self) -> None:
            """
            Performs groupyby and aggregation of the data frame.

            If the user provided some :attr:`grouping columns <.grouping_columns>` and :attr:`aggregation functions
            <.aggregation_functions>` then the :func:`~.group_and_aggregate_data_frame` is invoked accordingly.

            The user can update the values of those attributes during each cycle iteration within the implementation of
            the :meth:`~.in_loop_customization`.

            .. seealso::
                This method is simply invoking the :func:`~.group_and_aggregate_data_frame` function from the :mod:`~.pandas_tools`.
            """
            if self.grouping_columns and self.aggregation_functions:
                self.data_frame = group_and_aggregate_data_frame(
                    self.data_frame, self.grouping_columns, self.aggregation_functions
                )

        def is_data_frame_empty(self) -> bool:
            if len(self.data_frame.index) == 0:
                return True
            return False

        def slice_data_frame(self) -> None:
            """
            Perform data frame slicing

            The user can set some slicing criteria in the :attr:`~.slicing_dict` to select some specific data subset. The
            values of the slicing dict can be changed during each iteration within the implementation of the
            :meth:`~.in_loop_customization`.

            .. seealso::
                This method is simply invoking the :func:`~.slice_data_frame` function from the :mod:`~.pandas_tools`.
            """
            if self.slicing_dict:
                self.data_frame = slice_data_frame(self.data_frame, self.slicing_dict)

except ImportError:
    msg = (
        'Trying to use the seaborn Plotter implementation without having installed the required dependencies.\n'
        'Consider installing mafw with the optional feature seaborn. For example:\n'
        '\npip install mafw[seaborn]\n\n'
    )
    warnings.warn(MissingOptionalDependency(msg), stacklevel=2)
    raise
