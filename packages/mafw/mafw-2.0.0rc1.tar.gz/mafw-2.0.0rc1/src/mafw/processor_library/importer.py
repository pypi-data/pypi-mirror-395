#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Provides a basic element importer.

The first step in the setting up of the analytical framework of a data analysis procedure is to add new elements to
the input set.
These elements can encompass a wide range of data, including results from experiments or simulations, as well as information
gathered through from webscraping or other data sources.

Independently of where the data are coming from, one common task is to add those data to your collection inside the
DB, so that the following analytical steps know where the data are and what they are.

This module provides a generic processor that the user can subclass and customize to their needs to import
input files. Thanks to a smart filename parsing, other information can be extracted from the filename itself and
used to populate additional columns in the dedicated database table.

"""

from __future__ import annotations

import logging
import re
import tomllib
from pathlib import Path
from typing import TYPE_CHECKING, Any

from mafw.mafw_errors import MissingAttribute, ParserConfigurationError, ParsingError
from mafw.processor import ActiveParameter, Processor

log = logging.getLogger(__name__)


class FilenameElement:
    """
    Helper class for the definition of filename element.

    While importing an element to the DB, several parameters can be retrieved directly from the filename. The role of
    this helper class is to provide an easy way to define patterns in the filename representing a specific piece of
    information that has to be transferred to the DB.

    The element is characterized by a name, a regular expression, the expected python type for the parsed value and an optional
    default value. The regular expression should contain a named group in the form ``?P<name>`` where name is matching
    the FilenameElement name.

    To make a filename element optional, it is enough to provide a default value different from None.
    In this case, if the parsing is failing, then the default value will be returned.
    """

    type_lut: dict[str, type[str] | type[int] | type[float]] = {'str': str, 'int': int, 'float': float}
    """A lookup table for converting type definition as string into python types"""

    def __init__(
        self,
        name: str,
        regex: str | re.Pattern[str],
        value_type: type = str,
        default_value: str | int | float | None = None,
    ) -> None:
        """
        Constructor parameters:

        :param name: The name of the filename element
        :type name: str
        :param regex: The regular expression associated to this filename element. It must contain a named group in the
            form ?P<name>.
        :type regex: str | re.Pattern[str]
        :param value_type: The type the output value should be converted into. It defaults to str.
        :type value_type: type, Optional
        :param default_value: The default value to assign to the filename element if the pattern is not found in the
            filename. It defaults to None
        :type default_value: Any, Optional
        """
        self._variable_name: str = name
        if not isinstance(regex, re.Pattern):
            regex = re.compile(regex)

        self._regex: re.Pattern[str] = regex
        self._value_type = value_type
        self._default_value = default_value
        self._value = default_value
        self._validate_default_type()
        self._validate_regexp()

    def _validate_regexp(self) -> None:
        """
        Checks if the regular expression contains a named group named after the element itself.

        :raise ValueError: if the regular expression is not valid.
        """
        pattern = self._regex.pattern
        group = rf'?P<{self._variable_name}>'
        if group not in pattern:
            raise ValueError('Attempt to create a FilenameElement with a regular expression without a named group.')

    def _validate_default_type(self) -> None:
        """
        Checks that the default has a type matching the value type. The check is actually performed if and only if a
        default value is provided. If None, then the validation is skipped.

        :raise TypeError: if the default value type does not match the declared value type.
        """
        if type(self._default_value) is not self._value_type and self._default_value is not None:
            raise TypeError(
                f'The type of the default value ({str(type(self._default_value))}) is not matching the '
                f'declared value type ({str(self._value_type)})'
            )

    @classmethod
    def _get_value_type(cls, type_as_string: str) -> type:
        """
        Returns the value type.

        This method is used by the class method constructor to check if the user provided type in the form of a
        string is a valid one.

        If so, then the corresponding python type is returned, otherwise a ValueError exception is raised.

        :param type_as_string: The type of the value as a string.
        :type type_as_string: str
        :return: The corresponding python type.
        :rtype: type
        :raise ValueError: if type_as_string is not any of the acceptable type for the value.
        """
        if type_as_string not in cls.type_lut:
            raise ValueError('Attempt to create a FilenameElement with a not available value type')

        return cls.type_lut[type_as_string]

    def reset(self) -> None:
        """
        Resets the value to the default value.

        **Remember:** that the default value is None for compulsory elements.
        """
        self._value = self._default_value

    @classmethod
    def from_dict(cls, name: str, info_dict: dict[str, str | int | float]) -> FilenameElement:
        """
        Generates a FilenameElement starting from external information stored in a dictionary.

        `info_dict` should contain the following three keys:
            - regexp: the Regular expression for the element search.
            - type: a string with the python type name (int, float, str) for the element conversion.
            - default (*optional*): a default value.

        :param name: The name of the element.
        :type name: str
        :param info_dict: The dictionary with the required parameters for the class constructor.
        :type info_dict: dict
        :return: An instance of FilenameElement.
        :rtype: FilenameElement
        """
        # get the regexp
        try:
            regexp = info_dict['regexp']
        except KeyError:
            log.critical('Attempt to create a FilenameElement without a regular expression')
            raise
        # now let's check that the type of the regexp is acceptable
        if not isinstance(regexp, str):
            raise TypeError('Problem with regexp')

        value_type_str = info_dict.get('type', 'str')
        # check that this is a string
        if not isinstance(value_type_str, str):
            raise ValueError('Attempt to create a FilenameElement with a wrong value type.')

        value_type = cls._get_value_type(value_type_str)

        return cls(name, regex=regexp, value_type=value_type, default_value=info_dict.get('default', None))

    @property
    def name(self) -> str:
        """Returns the class name"""
        return self._variable_name

    @property
    def value(self) -> str | int | float | None:
        """Returns the class value"""
        return self._value

    @property
    def is_optional(self) -> bool:
        """Returns if the element is optional"""
        return self._default_value is not None

    @property
    def is_found(self) -> bool:
        """Returns if the file element is found"""
        if self.is_optional:
            return True
        else:
            return self._value != self._default_value

    @property
    def pattern(self) -> str | bytes:
        """Returns the regular expression pattern"""
        return self._regex.pattern

    def search(self, string: str | Path) -> None:
        """
        Searches the string for the regular expression.

        If the pattern is found in the string, then the matched value is transferred to the FilenameElement value.

        .. note::

            This method is not returning the match value. It is only searching the input string for the
            registered pattern. If the pattern is found, then the user can retrieve the matched value by invoking the
            :meth:`.value` method. If the pattern is not found, the :meth:`.value` will return either None,
            for a compulsory element, or the default value for an optional one.

        :param string: The string to be parsed. In most of the case, this is a filename, that is why the method is
            accepting also a Path type.
        :type string: str | Path
        """
        self.reset()
        if isinstance(string, Path):
            string = str(string)
        result = re.search(self._regex, string)
        if result:
            self._value = self._value_type(result[self._variable_name])


class FilenameParser:
    r"""
    Helper class to interpret all elements in a filename.

    Inside a filename, there might be  many elements containing information about the item that must be stored in the DB.
    This class will parse the filename, and after a successful identification of them all, it will make them available
    for the importer class to fill in the fields in the database.

    The :class:`~FilenameParser` needs to be configured to be able to recognise each element in the filename.
    Such configuration is saved in a `toml` file.
    An example of such a configuration is provided :download:`here </_static/toml_files/filename_parser_conf.toml>`.

    Each element must start with its name and a valid regular expression and a python type (in string).
    If an element is optional, then a default value must be provided as well.

    After the configuration, the filename can be interpreted invoking the :meth:`~interpret` method.
    This will perform the actual parsing of the filename.
    If an error occurs during the parsing process, meaning that a compulsory element is not found, then the
    :class:`~.ParsingError` exception will be raised.
    So remember to protect the interpretation with a try/except block.

    The value of each file element is available upon request.
    The user has simply to invoke the :meth:`~get_element_value` providing the element name.
    """

    def __init__(self, configuration_file: str | Path, filename: str | Path | None = None) -> None:
        """
        Constructor parameters:

        :param filename: The filename to be interpreted.
        :type filename: str | Path
        :param configuration_file: The configuration file for the interpreter.
        :type configuration_file: str | Path
        :raise ParserConfigurationError: If the configuration file is invalid.
        """

        #: The filename for this interpreter. If None, it should be specified before interpretation.
        self._filename = str(filename) if filename is not None else None
        #: The configuration file for the interpreter.
        self._configuration_file = configuration_file
        #: A dictionary with all the FilenameElement
        self._element_dict: dict[str, FilenameElement] = {}

        self._parser_configuration()

    def _parser_configuration(self) -> None:
        """
        Loads the parser configuration, generates the required FilenameElement and adds them element dictionary.

        The configuration file is stored in a TOML file.

        This private method is automatically invoked by the class constructor.

        :raise ParserConfigurationError: if the provided configuration file is invalid.
        """
        with open(self._configuration_file, 'rb') as f:
            config = tomllib.load(f)

        for element in config['elements']:
            if element not in config:
                raise ParserConfigurationError(f'Missing {element} table.')

            self._element_dict[element] = FilenameElement.from_dict(element, config[element])

    @property
    def elements(self) -> dict[str, FilenameElement]:
        """Returns the filename element dictionary"""
        return self._element_dict

    def interpret(self, filename: str | Path | None = None) -> None:
        """
        Performs the interpretation of the filename.

        The filename can be provided either as constructor argument or here as an argument. If both, then the local
        one will have the precedence.

        :raises ParsingError: if a compulsory element is not found in the filename
        :raises MissingAttribute: if no filename has been specified.
        """
        if self._filename is None and filename is None:
            raise MissingAttribute('Missing filename')

        if filename:
            self.reset()
            self._filename = str(filename)

        if TYPE_CHECKING:
            # self._filename is either set by the constructor or by the interpret method
            # at this stage it cannot be None
            assert self._filename is not None

        for element in self._element_dict.values():
            element.search(self._filename)
            if not element.is_found:
                raise ParsingError(f'Missing {element.name}')

    def get_element(self, element_name: str) -> FilenameElement | None:
        """Gets the FilenameElement named element_name"""
        if element_name in self._element_dict:
            return self._element_dict[element_name]
        else:
            return None

    def get_element_value(self, element_name: str) -> str | int | float | None:
        """
        Gets the value of the FilenameElement named element_name.

        It is equivalent to call ``self.get_element('element_name').value``
        """
        if element_name in self._element_dict:
            return self._element_dict[element_name].value
        else:
            return None

    def reset(self) -> None:
        """Resets all filename elements"""
        for element in self._element_dict.values():
            element.reset()


class Importer(Processor):
    """
    Importer is the base class for importing elements in the Database structure.

    It provides an easy skeleton to be subclassed by a more specific importer related to a certain project.

    It can be customised with three processor parameters:

        * The ``parser_configuration``: the path to the configuration file for the :class:`~.FilenameParser`.
        * The ``input_folder``: the path where the input files to be imported are.
        * The ``recursive`` flag: to specify if all subfolders should be also scanned.

    For a concrete implementation, have a look at the :class:`~.ImporterExample` from the example library.
    """

    parser_configuration = ActiveParameter(
        'parser_configuration',
        default='parser_configuration.toml',
        help_doc='The path to the TOML file with the filename parser configuration ',
    )
    input_folder = ActiveParameter(
        'input_folder', default=str(Path.cwd()), help_doc='The input folder from where the images have to be imported.'
    )
    recursive = ActiveParameter('recursive', default=True, help_doc='Extend the search to sub-folder')

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._filename_parser: FilenameParser
        """The filename parser instance"""

    def format_progress_message(self) -> None:
        self.progress_message = f'[cyan]Importing element {self.i_item + 1} of {self.n_item}'

    def start(self) -> None:
        """
        The start method.

        The filename parser is created using the provided configuration file.

        :raise ParserConfigurationError: If the configuration file is not valid.
        """
        super().start()
        if TYPE_CHECKING:
            assert isinstance(self.parser_configuration, str)

        self._filename_parser = FilenameParser(self.parser_configuration)
