#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Module implements the abstract base interface to a processor to generate plots.

This abstract interface is needed because MAFw does not force the user to select a specific plot and data manipulation
library.

The basic idea is to have a :class:`basic processor class <.GenericPlotter>` featuring a modified
:meth:`~.GenericPlotter.process` method where a skeleton of the standard operations required to generate a graphical
representation of a dataset is provided.

The user has the possibility to compose the :class:`~.GenericPlotter` by mixing it with one :class:`~.DataRetriever`
and a :class:`~.FigurePlotter`.

For a specific implementation based on :link:`seaborn`, please refer to :mod:`.sns_plotter`.
"""

import logging
import typing
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Protocol

import peewee

from mafw.db.std_tables import PlotterOutput, TriggerDisabler
from mafw.enumerators import LoopingStatus
from mafw.processor import ActiveParameter, Processor, ProcessorMeta
from mafw.tools.file_tools import file_checksum

log = logging.getLogger(__name__)


class PlotterMeta(type(Protocol), ProcessorMeta):  # type: ignore[misc]
    """Metaclass for the plotter mixed classes"""

    pass


class DataRetriever(ABC):
    """Base mixin class to retrieve a data frame from an external source"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # leave it here, otherwise the Protocol init will not call the main class init.
        # not sure why this is happening, but it costs nothing to have it here.

        """The dataframe instance. It will be filled for the main class"""
        super().__init__(*args, **kwargs)

    @abstractmethod
    def get_data_frame(self) -> None:
        """The mixin implementation of the shared method with the base class"""
        pass  # pragma: no cover

    @abstractmethod
    def patch_data_frame(self) -> None:
        """The mixin implementation of the shared method with the base class"""
        pass  # pragma: no cover

    @abstractmethod
    def _attributes_valid(self) -> bool:
        pass  # pragma: no cover


class FigurePlotter(ABC):
    @abstractmethod
    def plot(self) -> None:
        pass  # pragma: no cover

    @abstractmethod
    def _attributes_valid(self) -> bool:
        pass  # pragma: no cover


class GenericPlotter(Processor, metaclass=PlotterMeta):
    """
    The Generic Plotter processor.

    This is a subclass of a Processor with advanced functionality to fetch data in the form of a dataframe and to
    produce plots. When mentioning dataframe in the context of the generic plotter, we do not have in mind any
    specific dataframe implementation.

    The GenericPlotter is actually a kind of abstract class: since MAFw is not forcing you to use any specific
    plotting and data manipulation library, you need to subclass the GenericPlotter in your code, be sure that the
    required dependencies are available for import and use it as a normal processor.

    If you are ok with using :link:`seaborn` (with :link:`matplotlib` as a graphical backend and :link:`pandas` for
    data storage and manipulation), then be sure to install mafw with the optional feature `seaborn` (``pip install
    mafw[seaborn]``) and have a look at the :mod:`~.sns_plotter` for an already prepared implementation of a Plotter.

    The key difference with respect to a normal processor is its :meth:`.process` method that has been already
    implemented as follows:

    .. literalinclude:: ../../../src/mafw/processor_library/abstract_plotter.py
        :pyobject: GenericPlotter.process
        :dedent:

    This actually means that when you are subclassing a GenericPlotter you do not have to implement the process method
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

            This method has the task to get the data to be plotted. Since it is an almost abstract class, you need to

        * :meth:`~.patch_data_frame`.

            A convenient method to apply data frame manipulation to the data just retrieved. A typical use case is for
            conversion of unit of measurement. Imagine you saved the data in the S.I. units, but for the visualization
            you prefer to use practical units, so you can subclass this method to add a new column containing the same
            converted values of the original one.

        * :meth:`~.slice_data_frame`.

            Slicing a dataframe is similar as applying a where clause in a SQL query. Implement this method to select
            which row should be used in the generation of your plot.

        * :meth:`~.group_and_aggregate_data_frame`.

            In this method, you can manipulate your data frame to perform row grouping and aggregation.

        * :meth:`~.is_data_frame_empty`.

            A simple method to test if the dataframe contains any data to be plotted. In fact, after the slicing, grouping
            and aggregation operations, it is possible that the dataframe is now left without any row. In this case,
            it makes no sense to waste time in plotting an empty graph.

        * :meth:`~.plot`.

            This method is where the actual plotting occurs.

        * :meth:`~.customize_plot`.

            This method can be optionally used to customize the appearance of the facet grid produced by the
            :meth:`~plot` method. It is particularly useful when the user is mixing this class with one of the
            :class:`~.FigurePlotter` mixin, thus not having direct access to the plot method.

        * :meth:`~.save`.

            This method is where the produced plot is saved in a file. Remember to append the output file name to the
            :attr:`list of produced outputs <.output_filename_list>` so that the :meth:`~._update_plotter_db` method
            will automatically store this file in the database during the :meth:`~.finish` execution.

        * :meth:`~.update_db`.

            If the user wants to update a specific table in the database, they can use this method.

            It is worth reminding that all plotters are saving all generated files in the standard table PlotterOutput.
            This is automatically done by the :meth:`~._update_plotter_db` method that is called in the
            :meth:`~.finish` method.

    """

    output_folder = ActiveParameter(
        'output_folder', default=Path.cwd(), help_doc='The path where the output file will be saved'
    )

    force_replot = ActiveParameter(
        'force_replot', default=False, help_doc='Whether to force re-plotting even if the output file already exists'
    )
    """Flag to force the regeneration of the output file even if it is already existing."""

    @typing.no_type_check
    def is_output_existing(self) -> bool:
        """
        Check for plotter output existence.

        Generally, plotter subclasses do not have a real output that can be saved to a database. This class is meant to
        generate one or more graphical output files.

        One of the biggest advantages of having the output of a processor stored in the database is the ability to
        conditionally execute the processor if, and only if, the output is missing or changed.

        In order to allow also plotter processor to benefit from this feature, a :class:`dedicated table
        <.PlotterOutput>` is available among the :ref:`standard tables <std_tables>`.

        If a connection to the database is provided, then this method is invoked at the beginning of the
        :meth:`~.process` and a select query over the :class:`~.PlotterOutput` model is executed filtering by
        processor name. All files in the filename lists are checked for existence and also the checksum is verified.

        Especially during debugging phase of the processor, it is often needed to generate the plot several times, for
        this reason the user can switch the :attr:`.force_replot` parameter to True in the steering file and the output
        file will be generated even if it is already existing.

        This method will return True, if the output of the processor is already existing and valid, False, otherwise.

        .. versionchanged:: v2.0.0
            Using :attr:`.Processor.replica_name` instead of :attr:`.Processor.name` for storage in the :class:`.PlotterOutput`

        :return: True if the processor output exists and it is valid.
        :rtype: bool
        """
        if self.force_replot:
            return False

        if self._database is None:
            # no active database connection. it makes no sense to continue. inform the user and return
            log.warning('No database connection available. Impossible to check for existing output')
            return False

        try:
            query = PlotterOutput.get(PlotterOutput.plotter_name == self.replica_name)
            # check if all files exist:
            if not all([f.exists() for f in query.filename_list]):
                # at least one file is missing.
                # delete the whole row and continue
                with TriggerDisabler(trigger_type_id=4):
                    PlotterOutput.delete().where(PlotterOutput.plotter_name == self.name).execute()

                return False
            else:
                # all files exist.
                # check that they are still actual
                if query.checksum != file_checksum(query.filename_list):
                    # at least one file is changed.
                    # delete the whole row and continue
                    with TriggerDisabler(trigger_type_id=4):
                        PlotterOutput.delete().where(PlotterOutput.plotter_name == self.name).execute()
                    return False
                else:
                    # all files exit and the checksum is the same.
                    # we stop it here
                    return True

        except peewee.DoesNotExist:
            # no output for this plotter processor found in the DB.
            return False

    def process(self) -> None:
        """
        Process method overload.

        In the case of a plotter subclass, the process method is already implemented and the user should not overload
        it. On the contrary, the user must overload the other implementation methods described in the general
        :class:`class description <.SNSPlotter>`.
        """
        if self.filter_register.new_only:
            if self.is_output_existing():
                return

        self.in_loop_customization()
        self.get_data_frame()
        self.patch_data_frame()
        self.slice_data_frame()
        self.group_and_aggregate_data_frame()
        if not self.is_data_frame_empty():
            self.plot()
            self.customize_plot()
            self.save()
            self.update_db()

    def is_data_frame_empty(self) -> bool:
        """Check if the data frame is empty"""
        return False

    def in_loop_customization(self) -> None:
        """
        Customize the parameters for the output or input data for each execution iteration.
        """
        pass

    def get_data_frame(self) -> None:
        """
        Get the data frame with the data to be plotted.

        This method can be either implemented in the SNSPlotter subclass or via a :class:`.DataRetriever` mixin
        class.
        """
        # it must be overloaded.
        pass

    def format_progress_message(self) -> None:
        self.progress_message = f'{self.name} is working'

    def plot(self) -> None:
        """
        The plot method.

        This is where the user has to implement the real plot generation
        """
        pass

    def customize_plot(self) -> None:
        """
        The customize plot method.

        The user can overload this method to customize the output produced by the :meth:`~.plot` method, like, for
        example, adding meaningful axis titles, changing format, and so on.

        As usual, it is possible to use the :attr:`~.Processor.item`, :attr:`~.Processor.i_item` and
        :attr:`~.Processor.n_item` to
        access the loop
        parameters.
        """
        pass

    def save(self) -> None:
        """
        The save method.

        This is where the user has to implement the saving of the plot on disc.
        """
        pass

    def update_db(self) -> None:
        """
        The update database method.

        This is where the user has to implement the optional update of the database.

        .. seealso:

            The plotter output table is automatically update by :meth:`~._update_plotter_db`.
        """
        pass

    def slice_data_frame(self) -> None:
        pass

    def group_and_aggregate_data_frame(self) -> None:
        pass

    def finish(self) -> None:
        if self.looping_status == LoopingStatus.Continue:
            self._update_plotter_db()  # type: ignore[no-untyped-call]
        super().finish()

    def patch_data_frame(self) -> None:
        """
        Modify the data frame

        This method can be used to perform operation on the data frame, like adding new columns.
        It can be either implemented in the plotter processor subclasses or via a mixin class.
        """
        pass

    @typing.no_type_check
    def _update_plotter_db(self) -> None:
        """
        Updates the Plotter DB.

        A plotter subclass primarily generates plots as output in most cases, which means that no additional information
        needs to be stored in the database. This is sufficient to prevent unnecessary execution of the processor
        when it is not required.

        This method is actually protected against execution without a valid database instance.

        .. versionchanged:: v2.0.0
            Using the :attr:`.Processor.replica_name` instead of the :attr:`.Processor.name` as plotter_name in the
            :class:`.PlotterOutput` Model.

        """
        if self._database is None:
            # there is no active database connection. No need to continue. Inform the user and continue
            log.warning('No database connection available. Impossible to update the plotter output')
            return

        if len(self.output_filename_list) == 0:
            # there is no need to make an entry because there are no saved file
            return

        PlotterOutput.std_upsert(
            {
                'plotter_name': self.replica_name,
                'filename_list': self.output_filename_list,
                'checksum': self.output_filename_list,
            }
        ).execute()
