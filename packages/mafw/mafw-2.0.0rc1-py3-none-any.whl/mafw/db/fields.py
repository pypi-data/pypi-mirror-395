#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Module provides customised model fields specific for MAFw.
"""

from pathlib import Path
from typing import Any

from peewee import FieldAccessor, TextField

import mafw.tools.file_tools


class FileNameFieldAccessor(FieldAccessor):
    """
    A field accessor specialized for filename fields.

    In the constructor of the :class:`FileNameField` and subclasses, the user can specify the name of a checksum
    field linked to this filename. This is very useful because in this way, the user does not have to manually assign
    any value to this field that will simply be automatically updated when the filename field is updated.

    The user can disable this automatic feature either removing the link in the :class:`FileNameField` or simply
    assigning a value to the :class:`FileChecksumField`.
    """

    # noinspection PyProtectedMember
    def __set__(self, instance: Any, value: Any) -> None:
        """
        Sets the value of field in the instance data dictionary.

        If the field has a checksum field specified and this has not been initialised, then this one as well get
        assigned the same value.

        :param instance: a Model instance.
        :param value: the value to be assigned to the Field.
        """
        # do whatever is needed by the normal FieldAccessor
        super().__set__(instance, value)
        # if there is a linked field, continue here; otherwise, you have already finished.
        if self.field.checksum_field is not None:
            # check if the model has an attribute to store the initialisation of the linked field,
            # if not, create one and set it to False
            if not hasattr(instance, 'init_' + self.field.checksum_field):
                setattr(instance, 'init_' + self.field.checksum_field, False)

            # if the linked field has not been initialised, then set its value to the same value
            # of this field.
            if not getattr(instance, 'init_' + self.field.checksum_field):
                instance.__data__[self.field.checksum_field] = value
                instance._dirty.add(self.field.checksum_field)


# noinspection PyProtectedMember
class FileChecksumFieldAccessor(FieldAccessor):
    """
    Field accessor specialized for file checksum fields.

    When the field is directly set, then an initialization flag in the model instance is turned to True to avoid
    that the linked primary field will overrule this value again.

    For each checksum field named my_checksum, the model instance will get an attribute: init_my_checksum to be
    used as an initialization flag.

    Once the field is manually set, to re-establish the automatic mechanism, the user has to manually toggle the
    initialization flag.
    """

    def __set__(self, instance: Any, value: Any) -> None:
        """
        Sets the value of the field in the instance data dictionary.

        When the field is directly set, then the initialisation flag in the instance is also turned to True to avoid
        that the primary field will overrule this value again.

        For each checksum field named my_checksum, the model instance will get an attribute: init_my_checksum to be
        used as an initialisation flag.

        Once the field is manually set, to re-establish the automatic mechanism, the user has to manually toggle the
        initialisation flag.

        :param instance: a Model instance.
        :param value: the value to be assigned to the Field.
        """
        # do whatever is needed.
        super().__set__(instance, value)
        # check if the model has an attribute to store the initialisation of this field.
        # if not, create one and set it to False
        if not hasattr(instance, 'init_' + self.name):
            setattr(instance, 'init_' + self.name, False)
        # the field has been initialised, so set it to True, to avoid the primary field to overrule it.
        setattr(instance, 'init_' + self.name, True)


class FileNameField(TextField):
    """
    Field to be used for filenames.

    It is just an overload of TextField, that allows to apply filters and python functions specific to filenames.

    If the user specifies the name of a file checksum field, then when this field is updated, the checksum one will
    also be automatically updated.

    .. seealso::

        * :class:`~mafw.db.fields.FileNameListField` for a field able to store a list of filenames.

        * :func:`~mafw.tools.file_tools.remove_widow_db_rows` for a function removing entries from a database table
          where the corresponding files on disk are missing.

        * :func:`~mafw.tools.file_tools.verify_checksum` for a function comparing the actual checksum with the
          stored one and in case removing outdated entries from the DB.

    """

    accessor_class = FileNameFieldAccessor
    """The specific accessor class"""

    def __init__(self, checksum_field: str | None = None, *args: Any, **kwargs: Any) -> None:
        """
        Constructor parameter:

        :param checksum_field: The name of the checksum field linked to this filename. Defaults to None.
        :type checksum_field: str, Optional
        """
        super().__init__(*args, **kwargs)
        self.checksum_field = checksum_field

    def db_value(self, value: str | Path) -> str:
        """Converts the input python value into a string for the DB."""
        return str(value)

    def python_value(self, value: str) -> Path | None:
        """Converts the db value from str to Path

        The return value might also be None, if the user set the field value to null.

        :param value: The value of the field as stored in the database.
        :type value: str
        :return: The converted value as a path. It can be None, if value was stored as null.
        :rtype: Path | None
        """
        return Path(value) if value is not None else None


class FileNameListField(FileNameField):
    """
    A field for a list of file names.

    The evolution of the :class:`~mafw.db.fields.FileNameField`, this field is able to store a list of filenames as a
    ';' separated string of full paths.

    It is meant to be used when a processor is saving a bunch of correlated files that are to be used all together.

    In a similar way as its parent class, it can be link to a checksum field, in this case, the checksum of the whole
    file list will be calculated.
    """

    def db_value(self, value: list[str | Path] | str | Path) -> str:
        """Converts the list of paths in a ';' separated string"""
        if isinstance(value, (str, Path)):
            value = [value]
        return ';'.join([str(v) for v in value])

    def python_value(self, value: str) -> list[Path]:  # type: ignore[override]
        """Converts the ';' separated string in a list of paths"""
        if value is None:  # this might be the case, when the database field is actually set to null.
            return []
        return [Path(p) for p in value.split(';')]


class FileChecksumField(TextField):
    """
    A field to be used for file checksum.

    It is the evolution of the TextField for storing file checksum hexadecimal digest.

    If linked to a :class:`FileNameField` or :class:`FileNameListField`, then it will be automatically filled when the
    primary file name (or list of file names) field is set.

    If the user decides to set its value manually, then he can provide either the string with the hexadecimal
    characters as calculated by :func:`~mafw.tools.file_tools.file_checksum`, or simply the filename (or filename
    list) and the field will perform the calculation automatically.

    """

    accessor_class = FileChecksumFieldAccessor
    """The specific field accessor class"""

    def db_value(self, value: str | Path | list[str | Path]) -> str:
        """
        Converts the python assigned value to the DB type.

        The checksum will be stored in the DB as a string containing only hexadecimal characters
        (see `hexdigest <https://docs.python.org/3/library/hashlib.html#hashlib.hash.hexdigest>`_).

        The user can provide the checksum directly or the path to the file or a list of path to files. If a Path,
        or list of Path,  is provided, then the checksum will be calculated, if a str (a path converted into a
        string) is provided, the function will try to see if a file with that path exists. If so, the checksum will
        be calculated, if not, the original string is assumed to be the checksum.

        :param value: The checksum or path to the file, or list of path to files for which the checksum has to be
            stored.
        :type value: str | Path | list[str | Path]
        :return: The checksum string for the database storage.
        :rtype: str
        """

        if isinstance(value, Path):
            # we got the filename, not the digest. we need to calculate it
            value = mafw.tools.file_tools.file_checksum(value)
        elif isinstance(value, list):
            # we got a list of path, not the digest. we need to calculate the digest
            # of the whole list
            value = mafw.tools.file_tools.file_checksum(value)
        else:
            test_value = Path(value)
            if test_value.exists():
                # with a very high probability, the user passed a str to a path.
                value = mafw.tools.file_tools.file_checksum(test_value)
        return value

    def python_value(self, value: str) -> str:
        return value
