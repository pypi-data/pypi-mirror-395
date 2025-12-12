#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
The module provides some basic processors with DB interaction for
demonstrating the basic functionalities.
"""

import datetime
from pathlib import Path

from peewee import DateTimeField, IntegerField, TextField

import mafw.processor
from mafw.db.db_configurations import db_scheme, default_conf
from mafw.db.db_model import MAFwBaseModel
from mafw.decorators import database_required
from mafw.tools.file_tools import file_checksum


class File(MAFwBaseModel, do_not_register=True):
    """The Model class representing the table in the database"""

    filename = TextField(primary_key=True)
    digest = TextField()
    creation_date = DateTimeField()
    file_size = IntegerField()


class FileDoesNotExist(Exception):
    """Exception raised if the table corresponding to the File model does not exist."""


@database_required
class FillFileTableProcessor(mafw.processor.Processor):
    """Processor to fill a table with the content of a directory"""

    root_folder: Path = mafw.processor.ActiveParameter(
        'root_folder', default=Path.cwd(), help_doc='The root folder for the file listing'
    )

    def __init__(self, *args, **kwargs):
        """
        Constructor parameter:

        :param root_folder: ActiveParameter corresponding to the directory from
            where to start the recursive search
        :type root_folder: Path, Optional
        """
        super().__init__(*args, **kwargs)
        self.data: list[dict] = []

    def format_progress_message(self):
        self.progress_message = f'Upserting {self.item.name}'

    def start(self):
        """Starts the execution.

        Be sure that the table corresponding to the File model exists.
        It it does already exists, it is not a problem.
        """
        super().start()
        self.database.create_tables((File,))

    def get_items(self) -> list[Path]:
        """Retrieves the list of files.

        Insert or update the files from the root folder to the database

        :return: The list of full filename
        :rtype: list[Path]
        """
        file_list = []
        if self.root_folder.is_file():
            return [self.root_folder]
        elif self.root_folder.is_dir():
            for f in self.root_folder.glob('**/*'):
                if f.is_file():
                    file_list.append(f)
        else:  # root_file is a glob
            for f in self.root_folder.parent.glob(self.root_folder.name):
                file_list.append(f)
        return file_list

    def process(self):
        """Add all information to the data list"""
        self.data.append(
            dict(
                filename=str(self.item),
                digest=file_checksum(self.item),
                file_size=self.item.stat().st_size,
                creation_date=datetime.datetime.fromtimestamp(self.item.stat().st_mtime),
            )
        )

    def finish(self):
        """Transfers all the data to the File table via an atomic transaction."""
        with self.database.atomic():
            File.insert_many(self.data).on_conflict_replace().execute()
        super().finish()


@database_required
class CountStandardTables(mafw.processor.Processor):
    """A processor to count the number of standard tables"""

    n_tables = mafw.processor.ActiveParameter('n_tables', default=-1, help_doc='The number of standard tables')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, looper='single', **kwargs)

    def process(self):
        self.n_tables = len(self.database.get_tables())


if __name__ == '__main__':
    database_conf = default_conf['sqlite']
    database_conf['URL'] = db_scheme['sqlite'] + str(Path.cwd() / Path('test.db'))
    db_proc = FillFileTableProcessor(
        root_folder=r'C:\Users\bulghao\Documents\autorad-analysis\EdgeTrimming', database_conf=database_conf
    )
    db_proc.execute()
