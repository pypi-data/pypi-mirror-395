#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Database Tools

This module provides utility functions for working with database models using the Peewee ORM.
It offers helper functions for creating key-value mappings, retrieving primary key information,
and combining fields for composite keys or display purposes.
"""

from typing import TYPE_CHECKING, Any, cast

from peewee import Alias, CompositeKey, Field, Function, fn

from mafw.db.db_model import MAFwBaseModel


def make_kv(model: MAFwBaseModel | type[MAFwBaseModel], key: Field, value: Field) -> dict[Any, Any]:
    """
    Create a key-value mapping from a database model.

    This function selects data from a given model using specified key and value fields,
    and returns a dictionary where keys are values from the key field and values are
    values from the value field.

    :param model: The database model or model class to query.
    :type model: MAFwBaseModel | type[MAFwBaseModel]
    :param key: The field to use as dictionary keys.
    :type key: peewee.Field
    :param value: The field to use as dictionary values.
    :type value: peewee.Field
    :return: A dictionary mapping key field values to value field values.
    :rtype: dict[Any, Any]
    :raises AttributeError: If the model parameter doesn't have the required methods.
    """
    # Validate that model has the required methods
    if not hasattr(model, 'select'):
        raise AttributeError(f"Model {model} does not have a 'select' method")

    lut = {}
    for row in model.select(key, value):  # type: ignore[no-untyped-call]
        lut[getattr(row, key.name)] = getattr(row, value.name)
    return lut


def get_pk(model: MAFwBaseModel | type[MAFwBaseModel]) -> list[Field]:
    """
    Retrieve the primary key fields of a database model.

    This function examines the primary key of the provided model and returns
    a list of field objects that constitute the primary key. For composite
    primary keys, it returns all constituent fields; for simple primary keys,
    it returns a list containing just the primary key field.

    :param model: The database model or model class to examine.
    :type model: MAFwBaseModel | type[MAFwBaseModel]
    :return: A list of field objects representing the primary key fields.
    :rtype: list[peewee.Field]
    """
    if TYPE_CHECKING:
        assert hasattr(model, '_meta')

    if isinstance(model._meta.primary_key, CompositeKey):
        pk_fields = [model._meta.fields[field_name] for field_name in model._meta.primary_key.field_names]
    else:
        pk_fields = [model._meta.primary_key]

    return pk_fields


def combine_fields(fields: list[Field], join_str: str = ' x ') -> Function:
    """
    Combine multiple database fields into a single concatenated string expression.

    This function creates an SQL CONCAT expression that combines multiple field values
    into a single string using the specified separator. It's particularly useful for
    creating composite keys or display strings from multiple fields.

    :param fields: List of field objects to be combined.
    :type fields: list[peewee.Field]
    :param join_str: String to use as separator between fields. Defaults to ' x '.
    :type join_str: str
    :return: A SQL CONCAT function expression combining the fields.
    :rtype: peewee.Function
    """
    # Handle empty list case
    if not fields:
        return cast(Function, fn.CONCAT())

    # Handle single field case
    if len(fields) == 1:
        return cast(Function, fn.CONCAT(fields[0]))

    interspersed = [val for pair in zip(fields, [join_str] * (len(fields) - 1)) for val in pair] + [fields[-1]]
    return cast(Function, fn.CONCAT(*interspersed))


def combine_pk(
    model: MAFwBaseModel | type[MAFwBaseModel], alias_name: str = 'combo_pk', join_str: str = ' x '
) -> Alias:
    """
    Combine primary key fields of a database model into a single aliased field expression.

    This function retrieves the primary key fields from the given model using :func:`get_pk` and combines them into a single field expression. For models with a single primary key field,
    it simply aliases that field. For composite primary keys, it uses :func:combine_fields`
    to concatenate the fields with the specified separator.

    :param model: The database model or model class to examine for primary key fields.
    :type model: MAFwBaseModel | type[MAFwBaseModel]
    :param alias_name: The alias name to apply to the resulting field expression. Defaults to 'combo_pk'.
    :type alias_name: str
    :param join_str: String to use as separator between primary key fields when combining. Defaults to ' x '.
    :type join_str: str
    :return: An aliased field expression representing the combined primary key.
    :rtype: peewee.Alias
    """
    pk_fields = get_pk(model)
    if len(pk_fields) == 1:
        return cast(Alias, pk_fields[0].alias(alias_name))  # type: ignore[no-untyped-call]

    return cast(Alias, combine_fields(pk_fields, join_str).alias(alias_name))  # type: ignore[no-untyped-call]
