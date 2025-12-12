#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
import logging
from pathlib import Path
from typing import Any, Collection

from plug.db_model import Data, Detector, InputFile

from mafw.decorators import database_required, processor_depends_on_optional, single_loop
from mafw.enumerators import LoopingStatus
from mafw.mafw_errors import ParsingError
from mafw.processor import ActiveParameter, Processor
from mafw.processor_library.importer import Importer
from mafw.processor_library.sns_plotter import RelPlot, SNSPlotter, SQLPdDataRetriever
from mafw.tools.file_tools import verify_checksum

log = logging.getLogger(__name__)


class TestProcessor(Processor):
    def get_items(self) -> Collection[Any]:
        return list(range(10))


class GenerateDataFiles(Processor):
    n_files = ActiveParameter('n_files', default=25, help_doc='The number of 1-h increasing exposure')
    output_path = ActiveParameter(
        'output_path', default=Path.cwd(), help_doc='The path where the data files are stored.'
    )
    slope = ActiveParameter(
        'slope', default=1.0, help_doc='The multiplication constant for the data stored in the files.'
    )
    intercept = ActiveParameter(
        'intercept', default=5.0, help_doc='The additive constant for the data stored in the files.'
    )
    detector = ActiveParameter(
        'detector', default=1, help_doc='The detector id being used. See the detector table for more info.'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.n_digits = len(str(self.n_files))

    def start(self) -> None:
        super().start()
        self.output_path.mkdir(parents=True, exist_ok=True)

    def get_items(self) -> Collection[Any]:
        return list(range(self.n_files))

    def process(self) -> None:
        current_filename = self.output_path / f'rawfile_exp{self.i_item:0{self.n_digits}}_det{self.detector}.dat'
        value = self.i_item * self.slope + self.intercept
        with open(current_filename, 'wt') as f:
            f.write(str(value))

    def format_progress_message(self) -> None:
        self.progress_message = f'Generating exposure {self.i_item} for detector {self.detector}'


# importer start
@database_required
class PlugImporter(Importer):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._data_list: list[dict[str, Any]] = []

    def get_items(self) -> Collection[Any]:
        pattern = '**/*dat' if self.recursive else '*dat'
        input_folder_path = Path(self.input_folder)

        file_list = [file for file in input_folder_path.glob(pattern) if file.is_file()]

        # verify the checksum of the elements in the input table. if they are not up to date, then remove the row.
        verify_checksum(InputFile)

        if self.filter_register.new_only:
            # get the filenames that are already present in the input table
            existing_rows = InputFile.select(InputFile.filename).namedtuples()
            # create a set with the filenames
            existing_files = {row.filename for row in existing_rows}
            # filter out the file list from filenames that are already in the database.
            file_list = [file for file in file_list if file not in existing_files]

        return file_list

    def process(self) -> None:
        try:
            new_file = {}
            self._filename_parser.interpret(self.item.name)
            new_file['filename'] = self.item
            new_file['checksum'] = self.item
            new_file['exposure'] = self._filename_parser.get_element_value('exposure')
            new_file['detector'] = self._filename_parser.get_element_value('detector')
            self._data_list.append(new_file)
        except ParsingError:
            log.critical('Problem parsing %s' % self.item.name)
            self.looping_status = LoopingStatus.Skip

    def finish(self) -> None:
        InputFile.insert_many(self._data_list).on_conflict_replace(replace=True).execute()
        super().finish()


# start of analyser
@database_required
class Analyser(Processor):
    def get_items(self) -> Collection[Any]:
        self.filter_register.bind_all([InputFile])

        if self.filter_register.new_only:
            existing_entries = Data.select(Data.file_pk).execute()
            existing = ~InputFile.file_pk.in_([i.file_pk for i in existing_entries])
        else:
            existing = True

        query = (
            InputFile.select(InputFile, Detector)
            .join(Detector, attr='_detector')
            .where(self.filter_register.filter_all())
            .where(existing)
        )

        return query

    def process(self) -> None:
        with open(self.item.filename, 'rt') as fp:
            value = float(fp.read())

        Data.create(file_pk=self.item.file_pk, value=value)

    def format_progress_message(self) -> None:
        self.progress_message = f'Analysing {self.item.filename.name}'


# start of plotter
@database_required
@processor_depends_on_optional(module_name='seaborn')
@single_loop
class PlugPlotter(SQLPdDataRetriever, RelPlot, SNSPlotter):
    new_defaults = {
        'output_folder': Path.cwd(),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            table_name='data_view',
            required_cols=['exposure', 'value', 'detector_name'],
            x='exposure',
            y='value',
            hue='detector_name',
            facet_kws=dict(legend_out=False, despine=False),
            **kwargs,
        )

    def start(self) -> None:
        super().start()

        sql = """
        CREATE TEMP VIEW IF NOT EXISTS data_view AS
        SELECT 
            file_id, detector.detector_id, detector.name as detector_name, exposure, value
        FROM
            data
            JOIN input_file ON data.file_id = input_file.file_pk
            JOIN detector USING (detector_id)
        ORDER BY
            detector.detector_id ASC, 
            input_file.exposure ASC
            ;
        """
        self.database.execute_sql(sql)

    def customize_plot(self):
        self.facet_grid.set_axis_labels('Exposure', 'Value')
        self.facet_grid.figure.subplots_adjust(top=0.9)
        self.facet_grid.figure.suptitle('Data analysis results')
        self.facet_grid._legend.set_title('Detector type')

    def save(self) -> None:
        output_plot_path = self.output_folder / 'output.png'

        self.facet_grid.figure.savefig(output_plot_path)
        self.output_filename_list.append(output_plot_path)

    def plot(self) -> None:
        log.info('Generating plot')
        super().plot()
