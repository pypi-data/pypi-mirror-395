#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Database Type Definitions

This module provides type definitions for database models and related components.

It defines Protocol classes that represent the expected interfaces for database models,
helping with static type checking when working with ORM frameworks like Peewee.

"""

from typing import Any, Protocol


class PeeweeModelWithMeta(Protocol):
    """
    Protocol defining the interface for Peewee model classes with metadata.

    This Protocol helps with static type checking for Peewee ORM models,
    ensuring that objects passed to functions expecting Peewee models
    have the necessary methods and attributes.

    Attributes
    ----------
    `_meta : Any`
        The metadata object associated with the Peewee model class.
        Contains information about the table, fields, and other model properties.

    Methods
    -------
    `select(*args: Any, **kwargs: Any) -> Any`
        Select records from the database.

    `delete(*args: Any, **kwargs: Any) -> Any`
        Delete records from the database.

    """

    _meta: Any

    def select(self, *args: Any, **kwargs: Any) -> Any: ...

    def delete(self, *args: Any, **kwargs: Any) -> Any: ...
