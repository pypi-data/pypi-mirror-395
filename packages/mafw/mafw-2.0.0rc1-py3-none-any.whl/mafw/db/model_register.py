#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Module for registering and retrieving database models.

This module provides functionality to register database models with table names as key
and retrieve them using flexible naming conventions that support prefixes and suffixes.

.. versionadded:: v2.0.0
"""

import itertools
import logging
import threading
from typing import TYPE_CHECKING, List, Type

import peewee

if TYPE_CHECKING:
    from mafw.db.std_tables import StandardTable

log = logging.getLogger(__name__)


class ModelRegister:
    """
    A registry for database models with support for prefixes and suffixes.

    This class allows registration of database models with table names and
    provides flexible retrieval mechanisms that can handle different naming conventions.

    The following implemented methods are thread-safe:
        - :meth:`.register_model`
        - :meth:`.register_prefix`
        - :meth:`.register_suffix`
        - :meth:`.get_model`
        - :meth:`.get_model_names`
        - :meth:`.get_table_names`
        - :meth:`.items`

    Accessing the class underling containers is instead **not** thread safe.


    .. versionadded:: v2.0.0
    """

    def __init__(self) -> None:
        self.models: dict[str, peewee.ModelBase] = {}
        self.model_names: dict[str, str] = {}  # this dictionary goes from ModelName to table_name
        self.prefixes: list[str] = []
        self.suffixes: list[str] = []
        self._lock = threading.Lock()

    def register_model(self, table_name: str, model: peewee.ModelBase) -> None:
        """
        Register a model with a specific table name.

        If a model with the same table name already exists, it will be replaced
        with a warning message.

        :param table_name: The table name to register the model under
        :type table_name: str
        :param model: The peewee Model class to register
        :type model: peewee.Model
        """
        with self._lock:
            if table_name in self.models:
                log.warning(f'A model with the same name ({table_name}) already exists. Replacing it.')
            self.models[table_name] = model
            self.model_names[model.__name__] = table_name

    def register_prefix(self, prefix: str) -> None:
        """
        Register a prefix to be used when searching for models.

        :param prefix: The prefix string to register
        :type prefix: str
        """
        with self._lock:
            if prefix not in self.prefixes:
                self.prefixes.append(prefix)

    def register_suffix(self, suffix: str) -> None:
        """
        Register a suffix to be used when searching for models.

        :param suffix: The suffix string to register
        :type suffix: str
        """
        with self._lock:
            if suffix not in self.suffixes:
                self.suffixes.append(suffix)

    def get_model(self, name: str) -> peewee.ModelBase:
        """
        Retrieve a model by name, supporting prefixes and suffixes.

        `name` could be either the table_name or the ModelName.

        This method attempts to find a model by the given name, considering
        registered prefixes and suffixes. It also handles conversion between
        CamelCase model names and snake_case table names using peewee's utility.

        :param name: The name to search for
        :type name: str
        :return: The registered peewee Model class
        :rtype: peewee.Model
        :raises KeyError: If no matching model is found or multiple similar models exist
        """
        with self._lock:
            if name in self.models:
                # let's assume we got a table_name
                return self.models[name]
            elif name in self.model_names:
                # let's try with a ModelName
                return self.models[self.model_names[name]]
            else:
                # let's try some combinations as a last resort!
                prefixes = ['']
                prefixes.extend(self.prefixes)

                names = [name]
                if peewee.make_snake_case(name) not in names:  # type: ignore[attr-defined]
                    names.append(peewee.make_snake_case(name))  # type: ignore[attr-defined]

                suffixes = ['']
                suffixes.extend(self.suffixes)

                combinations = itertools.product(prefixes, names, suffixes)

                possible_names = []
                for p, n, s in combinations:
                    name_under_test = p + n + s
                    if name_under_test in self.models:
                        possible_names.append(name_under_test)
                possible_names = list(set(possible_names))

                if len(possible_names) == 0:
                    log.error(f'Model {name} not found in the registered models')
                    log.error(f'Available models: {", ".join(self.models.keys())}')
                    raise KeyError(f'Model {name} not registered')
                elif len(possible_names) == 1:
                    log.debug(f'Model {name} not found, but {possible_names[0]} is available. Using this model.')
                    return self.models[possible_names[0]]
                else:
                    log.error(f'Model {name} not found in the registered models')
                    log.error(f'Following similar models found: {", ".join(possible_names)}')
                    raise KeyError(f'Model {name} not registered, but multiple similar ones found.')

    def get_model_names(self) -> list[str]:
        """
        Get a list of all registered model names.

        :return: List of registered model names
        :rtype: list[str]
        """
        with self._lock:
            return list(self.model_names.keys())

    def get_table_names(self) -> list[str]:
        """
        Get a list of all registered table names.

        :return: List of registered table names
        :rtype: list[str]
        """
        with self._lock:
            return list(self.models.keys())

    def items(self) -> list[tuple[str, peewee.ModelBase]]:
        """
        Return the items list of the registered models dictionary.

        This method provides access to all registered models through a dictionary-like
        items view, allowing iteration over key-value pairs of table names and their
        corresponding model classes.

        In order to release the thread lock as soon as possible, instead of providing an iterator a list of the
        current snapshot of the dictionary is provided.

        :return: An items view of the registered models
        :rtype: list[[str, peewee.ModelBase]]
        """
        with self._lock:
            return list(self.models.items())

    def get_standard_tables(self) -> List[Type['StandardTable']]:
        """
        Retrieve all registered models that are instances of :class:`~mafw.db.std_tables.StandardTable`.

        This method filters the registered models and returns only those that inherit from
        the :class:`~mafw.db.std_tables.StandardTable` base class.

        This is useful for identifying and working with standard database tables that follow a specific
        structure or interface.

        Since the introduction of the :class:`~.ModelRegister`, there is no need any more for a standard table
        plugin hook, instead the user can use this method to retrieve all standard tables.

        :return: A list of registered model classes that are standard tables
        :rtype: list[peewee.ModelBase]
        """
        from mafw.db.std_tables import StandardTable

        return [t for t in self.models.values() if issubclass(t, StandardTable)]

    def clear(self) -> None:
        """
        Clear all registered models, prefixes, and suffixes from the registry.

        This method removes all entries from the internal dictionaries and lists,
        effectively resetting the ModelRegister to its initial empty state.

        .. note::
           This operation cannot be undone. All previously registered models
           and naming conventions will be lost after calling this method.

        :rtype: None
        """
        self.models = {}
        self.model_names = {}
        self.prefixes = []
        self.suffixes = []
