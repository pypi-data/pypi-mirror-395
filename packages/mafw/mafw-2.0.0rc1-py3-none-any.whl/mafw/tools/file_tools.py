#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""The module provides utilities for handling file, filename, hashing and so on."""

import hashlib
import warnings
from collections.abc import Sequence
from pathlib import Path
from typing import cast

from peewee import Model

import mafw.db.fields
from mafw.db.db_types import PeeweeModelWithMeta
from mafw.mafw_errors import ModelError


def file_checksum(filenames: str | Path | Sequence[str | Path], buf_size: int = 65536) -> str:
    """
    Generates the hexadecimal digest of a file or a list of files.

    The digest is calculated using the sha256 algorithm.

    :param filenames: The filename or the list of filenames for digest calculations.
    :type filenames: str, Path, list
    :param buf_size: The buffer size in bytes for reading the input files. Defaults to 64kB.
    :type buf_size: int, Optional
    :return: The hexadecimal digest.
    :rtype: str
    """
    if isinstance(filenames, (str, Path)):
        filenames = [filenames]

    hasher = hashlib.sha256()

    for filename in filenames:
        with open(filename, 'rb') as file:
            while True:
                data = file.read(buf_size)
                if not data:
                    break
                hasher.update(data)

    return hasher.hexdigest()


# noinspection PyUnresolvedReferences
def remove_widow_db_rows(models: list[Model | type[Model]] | Model | type[Model]) -> None:
    """Removes widow rows from a database table.

    According to MAFw architecture, the Database is mainly providing I/O support to the various processors.

    This means that the processor retrieves a list of items from a database table for processing and subsequently
    updates a result table with the newly generated outputs.

    Very often the input and output data are not stored directly in the database, but rather in files saved on the
    disc. In this case, the database is just providing a valid path where the input (or output) data can be found.

    From this point of view, a **widow row** is a database entry in which the file referenced by the FilenameField
    has been deleted. A typical example is the following: the user wants a certain processor to regenerate a given
    result stored inside an output file. Instead of setting up a complex filter so that the processor receives only
    this element to process, the user can delete the actual output file and ask the processor to process all new items.

    The provided ``models`` can be either a list or a single element, representing either an instance of a DB model
    or a model class. If a model class is provided, then a select over all its entries is performed.

    The function will look at all fields of :class:`~mafw.db.fields.FileNameField` and
    :class:`~mafw.db.fields.FileNameListField` and check if it corresponds to an existing path or list of paths. If not,
    then the corresponding row is removed from the DB table.

    :param models: A list or a single Model instance or Model class for widow rows removal.
    :type models: list[Model | type(Model)] | Model | type(Model)
    :raises TypeError: if ``models`` is not of the right type.
    """
    from mafw.db.std_tables import TriggerDisabler

    # noinspection PyUnresolvedReferences,PyProtectedMember
    def _check_row(r: Model) -> None:
        """Internal function performing the check and removal on a single instance"""
        # this is just to make mypy happy
        # r0 and r are exactly the same thing!
        r0 = cast(PeeweeModelWithMeta, r)
        for k, f in r0._meta.fields.items():
            # since FileNameListField is a subclass of FileNameField, we first have to check for
            # the case of a list and then of a simple field.
            if isinstance(f, mafw.db.fields.FileNameListField):
                files = [Path(p) for p in getattr(r, k).split(';')]
                for file in files:
                    if not file.exists():
                        r.delete_instance()
                        break
            elif isinstance(f, mafw.db.fields.FileNameField):
                if not getattr(r, k).exists():
                    r.delete_instance()

    if isinstance(models, (Model, type(Model))):
        models = [models]

    with TriggerDisabler(trigger_type_id=4):
        for m in models:
            if isinstance(m, Model):
                _check_row(m)
            elif isinstance(m, type(Model)):
                # this is just to make mypy happy
                # m0 and m are exactly the same thing!
                m0 = cast(PeeweeModelWithMeta, m)
                for row in m0.select().execute():
                    _check_row(row)
            else:
                raise TypeError('models must be list[Model | type(Model)] | Model | type(Model)')


# noinspection PyUnresolvedReferences
def verify_checksum(models: list[Model | type[Model]] | Model | type[Model]) -> None:
    """
    Verifies the goodness of FileChecksumField.

    If in a model there is a FileChecksumField, this must be connected to a FileNameField or a FileNameListField in
    the same model. The goal of this function is to recalculate the checksum of the FileNameField / FileNameListField
    and compare it with the actual stored value. If the newly calculated value differs from the stored one, the
    corresponding row in the model will be removed, as it is no longer valid.

    If a file is missing, then the checksum check is not performed, but the row is removed right away.

    This function can be CPU and I/O intensive and last a lot, so use it with care, especially when dealing with long
    tables and large files.

    :param models: A list or a single Model instance or Model class for checksum verification.
    :type models: list[Model | type(Model)] | Model | type(Model)
    :raises TypeError: if ``models`` is not of the right type.
    :raises mafw.mafw_errors.ModelError: if the FileCheckSumField is referring to a FilenameField that does not exist.
    """
    from mafw.db.std_tables import TriggerDisabler

    # noinspection PyUnresolvedReferences,PyProtectedMember
    def _check_row(r: Model) -> None:
        def _check_file(file: str | Path | Sequence[str | Path], stored_checksum: str) -> None:
            checksum = file_checksum(file)
            if checksum != getattr(r, stored_checksum):
                r.delete_instance()

        for k, f in r._meta.fields.items():  # type: ignore[attr-defined]  # it looks like it is a problem with peewee
            if isinstance(f, (mafw.db.fields.FileNameField, mafw.db.fields.FileNameListField)):
                # f is a filename field or a filename list field
                # this might be linked to a Checksum field
                if f.checksum_field is None:
                    continue

                if not hasattr(r, f.checksum_field):
                    raise ModelError(
                        f'FileNameField {k} is referring to {f.checksum_field}, but Model '
                        f'{r.__class__.__name__} has not such field'
                    )

                if isinstance(f, mafw.db.fields.FileNameListField):
                    files: list[Path] = [Path(p) for p in getattr(r, k)]
                    if not all([file.exists() for file in files]):
                        r.delete_instance()
                        warnings.warn('A file is missing from the list, removing the whole row from the DB.')
                    else:
                        _check_file(files, f.checksum_field)
                else:  # isinstance(f, FileNameField)
                    file = getattr(r, k)
                    if not file.exists():
                        warnings.warn(f'{str(file)} does not exist, removing the corresponding row from the DB')
                        r.delete_instance()
                    else:
                        _check_file(file, f.checksum_field)

    if isinstance(models, (Model, type(Model))):
        models = [models]

    with TriggerDisabler(trigger_type_id=4):
        for m in models:
            if isinstance(m, Model):
                _check_row(m)
            elif isinstance(m, type(Model)):
                for row in m.select().execute():  # type: ignore[no-untyped-call]  # problem with peewee
                    _check_row(row)
            else:
                raise TypeError('models must be list[Model | type(Model)] | Model | type(Model)')
