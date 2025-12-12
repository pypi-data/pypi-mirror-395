#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
The module provides one concrete implementation of an Importer, as it was used in the autorad paper2.
"""

import logging
from pathlib import Path
from typing import Any, Collection

import peewee
from peewee import AutoField, FloatField, IntegerField, TextField

import mafw.processor_library.importer
from mafw.db.db_model import MAFwBaseModel
from mafw.db.fields import FileChecksumField, FileNameField
from mafw.decorators import database_required
from mafw.enumerators import LoopingStatus
from mafw.mafw_errors import ParsingError
from mafw.tools.file_tools import verify_checksum

log = logging.getLogger(__name__)


class InputElement(MAFwBaseModel, do_not_register=True):
    """A model to store the input elements"""

    element_id = AutoField(primary_key=True, help_text='Primary key for the input element table')
    filename = FileNameField(unique=True, checksum_field='checksum', help_text='The filename of the element')
    checksum = FileChecksumField(help_text='The checksum of the element file')
    sample = TextField(help_text='The sample name')
    exposure = FloatField(help_text='The exposure time in hours')
    resolution = IntegerField(default=25, help_text='The readout resolution in µm')


class InputElementDoesNotExist(peewee.DoesNotExist):
    """Exception raised if the InputElement does not exist"""


@database_required
class ImporterExample(mafw.processor_library.importer.Importer):
    """
    An exemplary implementation of an importer processor.

    This importer subclass is looking for tif files in the ``input_folder`` and using the information stored in the
    filename, all required database fields will be obtained.

    For this importer, we will use a filename parser including two compulsory elements and one optional ones. Those are:

        * Sample name, in the form of sample_xyz, where xyz are three numerical digits  (**compulsory**).

        * Exposure time, in the form of expYh, where Y is the exposure time in hours. It can be an integer number or
          a floating number using `.` as decimal separator (**compulsory**).

        * Resolution, in the form of rXYu, where XY is the readout granularity in micrometer. It is optional and its
          default is 25 µm if not provided.

    This processor is subclassing:

        #. The :meth:`~.start`: in order to be sure that the database table is existing.

        #. The :meth:`~.get_items`: where the list of input files is retrieved. There we also verify that the table is
           still updated using the :func:`~.verify_checksum` and in case the user wants to process only new files,
           we will have to filter out from the list all items already stored in the database.

        #. The :meth:`~.process`: where we create a dictionary with the values to be stored in the database. This
           approach allows a much more efficient database transaction.

        #. The :meth:`~.finish`: where we actually do the database insert in a single go.

        #. The :meth:`~.format_progress_message`: to keep the user informed about the progress (optional).

    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._data_list: list[dict[str, Any]] = []

    def start(self) -> None:
        """
        The start method.

        The filename parser is ready to use because it has been already configured in the super method.
        We need to be sure that the input table exists, otherwise we create it from scratch.
        """
        super().start()
        self.database.create_tables([InputElement])

    def get_items(self) -> Collection[Any]:
        r"""Retrieves the list of element to be imported.

        The base folder is provided in the configuration file, along with the recursive flags and all the filter options.

        :return: The list of items full file names to be processed.
        :rtype: list[Path]
        """
        pattern = '**/*tif' if self.recursive else '*tif'
        input_folder_path = Path(self.input_folder)

        file_list = [file for file in input_folder_path.glob(pattern) if file.is_file()]

        # verify the checksum of the elements in the input table. if they are not up to date, then remove the row.
        verify_checksum(InputElement)

        if self.filter_register.new_only:
            # get the filenames that are already present in the input table
            existing_rows = InputElement.select(InputElement.filename).namedtuples()
            # create a set with the filenames
            existing_files = {row.filename for row in existing_rows}
            # filter out the file list from filenames that are already in the database.
            file_list = [file for file in file_list if file not in existing_files]

        return file_list

    def format_progress_message(self) -> None:
        self.progress_message = f'Importing element {self.item.name}'

    def process(self):
        """
        The process method overload.

        This is where the whole list of files is scanned.

        The current item is a filename, so we can feed it directly to the FilenameParser interpret command, to have it
        parsed. To maximise the efficiency of the database transaction, instead of inserting each file
        singularly, we are collecting them all in a list and then insert all of them in the :meth:`~.finish` method.

        In case the parsing is failing, then the element is skipped and an error message is printed.
        """
        try:
            new_element = {}
            self._filename_parser.interpret(self.item.name)
            new_element['sample'] = self._filename_parser.get_element_value('sample_name')
            new_element['exposure'] = self._filename_parser.get_element_value('exposure')
            new_element['resolution'] = self._filename_parser.get_element_value('resolution')
            new_element['filename'] = self.item
            new_element['checksum'] = self.item
            self._data_list.append(new_element)
        except ParsingError:
            log.critical('Problem parsing %s' % self.item.name)
            self.looping_status = LoopingStatus.Skip

    def finish(self) -> None:
        """
        The finish method overload.

        Here is where we do the database insert with a on_conflict_replace to cope with the unique constraint.
        """
        # we are ready to insert the lines in the database
        InputElement.insert_many(self._data_list).on_conflict_replace(replace=True).execute()

        # the super is printing the statistics, so we call it after the implementation
        super().finish()
