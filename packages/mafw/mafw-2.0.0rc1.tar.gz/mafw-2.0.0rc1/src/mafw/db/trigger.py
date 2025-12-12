#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Module provides a Trigger class and related tools to create triggers in the database via the ORM.

It supports SQLite, MySQL and PostgreSQL with dialect-specific SQL generation.
"""

from abc import ABC, abstractmethod
from enum import StrEnum
from typing import Any, Self, cast

import peewee
from peewee import Model

from mafw.db.db_types import PeeweeModelWithMeta
from mafw.mafw_errors import MissingSQLStatement, UnsupportedDatabaseError
from mafw.tools.regexp import normalize_sql_spaces


def and_(*conditions: str) -> str:
    """
    Concatenates conditions with logical AND.

    :param conditions: The condition to join.
    :type conditions: str
    :return: The and-concatenated string of conditions
    :rtype: str
    """
    conditions_l = [f'({c})' for c in conditions]
    return ' AND '.join(conditions_l)


def or_(*conditions: str) -> str:
    """
    Concatenates conditions with logical OR.

    :param conditions: The condition to join.
    :type conditions: str
    :return: The or-concatenated string of conditions.
    :rtype: str
    """
    conditions_l = [f'({c})' for c in conditions]
    return ' OR '.join(conditions_l)


class TriggerWhen(StrEnum):
    """String enumerator for the trigger execution time (Before, After or Instead Of)"""

    Before = 'BEFORE'
    After = 'AFTER'
    Instead = 'INSTEAD OF'


class TriggerAction(StrEnum):
    """String enumerator for the trigger action (Delete, Insert, Update)"""

    Delete = 'DELETE'
    Insert = 'INSERT'
    Update = 'UPDATE'


class TriggerDialect(ABC):
    """Abstract base class for database-specific trigger SQL generation."""

    @abstractmethod
    def create_trigger_sql(self, trigger: 'Trigger') -> str:
        """
        Generate the SQL to create a trigger for a specific database dialect.

        :param trigger: The trigger object
        :return: SQL string to create the trigger
        """
        pass  # pragma: no cover

    @abstractmethod
    def drop_trigger_sql(self, trigger_name: str, safe: bool = True, table_name: str | None = None) -> str:
        """
        Generate the SQL to drop a trigger for a specific database dialect.

        :param trigger_name: The name of the trigger to drop
        :type trigger_name: str
        :param safe: If True, add an IF EXISTS clause. Defaults to True.
        :type safe: bool, Optional
        :param table_name: The name of the target table for the trigger. Defaults to None.
        :type table_name: str, Optional
        :return: SQL string to drop the trigger
        :rtype: str
        """
        pass  # pragma: no cover

    @abstractmethod
    def select_all_trigger_sql(self) -> str:
        pass  # pragma: no cover

    @abstractmethod
    def supports_trigger_type(self, when: TriggerWhen, action: TriggerAction, on_view: bool = False) -> bool:
        """
        Check if the database supports the specified trigger type.

        :param when: When the trigger should fire (BEFORE, AFTER, INSTEAD OF)
        :param action: The action that triggers the trigger (INSERT, UPDATE, DELETE)
        :param on_view: Whether the trigger is on a view
        :return: True if supported, False otherwise
        """
        pass  # pragma: no cover

    @abstractmethod
    def supports_safe_create(self) -> bool:
        """
        Check if the database supports IF NOT EXISTS for triggers.

        :return: True if supported, False otherwise
        """
        pass  # pragma: no cover

    @abstractmethod
    def supports_update_of_columns(self) -> bool:
        """
        Check if the database supports column-specific UPDATE triggers.

        :return: True if supported, False otherwise
        """
        pass  # pragma: no cover

    @abstractmethod
    def supports_when_clause(self) -> bool:
        """
        Check if the database supports WHEN conditions.

        :return: True if supported, False otherwise
        """
        pass  # pragma: no cover


class SQLiteDialect(TriggerDialect):
    """SQLite-specific trigger SQL generation."""

    def create_trigger_sql(self, trigger: 'Trigger') -> str:
        """Generate SQLite trigger SQL."""
        if_not_exists = 'IF NOT EXISTS' if trigger.safe else ''
        of_columns = (
            f'OF {", ".join(trigger.update_columns)}'
            if trigger.trigger_action == TriggerAction.Update and trigger.update_columns
            else ''
        )
        for_each_row = 'FOR EACH ROW' if trigger.for_each_row else ''
        when_clause = f'WHEN {" AND ".join(trigger._when_list)}' if trigger._when_list else ''
        sql_statements = '\n'.join(trigger._sql_list)

        return normalize_sql_spaces(
            f'CREATE TRIGGER {if_not_exists} {trigger.trigger_name}\n'
            f'{trigger.trigger_when} {trigger.trigger_action} {of_columns} ON {trigger.target_table}\n'
            f'{for_each_row} {when_clause}\n'
            f'BEGIN\n'
            f'{sql_statements}\n'
            f'END;'
        )

    def drop_trigger_sql(self, trigger_name: str, safe: bool = True, table_name: str | None = None) -> str:
        """Generate SQLite drop trigger SQL."""
        return normalize_sql_spaces(f'DROP TRIGGER {"IF EXISTS" if safe else ""} {trigger_name}')

    def select_all_trigger_sql(self) -> str:
        return "SELECT name AS trigger_name, tbl_name AS table_name FROM sqlite_master WHERE type = 'trigger';"

    def supports_trigger_type(self, when: TriggerWhen, action: TriggerAction, on_view: bool = False) -> bool:
        """SQLite supports all trigger types except INSTEAD OF on tables (only on views)."""
        if when == TriggerWhen.Instead and not on_view:
            return False
        return True

    def supports_safe_create(self) -> bool:
        """SQLite supports IF NOT EXISTS for triggers."""
        return True

    def supports_update_of_columns(self) -> bool:
        """SQLite supports column-specific UPDATE triggers."""
        return True

    def supports_when_clause(self) -> bool:
        """SQLite supports WHEN conditions."""
        return True


class MySQLDialect(TriggerDialect):
    """MySQL-specific trigger SQL generation."""

    def create_trigger_sql(self, trigger: 'Trigger') -> str:
        """Generate MySQL trigger SQL."""
        # MySQL doesn't support INSTEAD OF triggers
        # MySQL doesn't support column-specific UPDATE triggers
        # MySQL requires FOR EACH ROW

        if_not_exists = 'IF NOT EXISTS' if trigger.safe else ''

        # In MySQL, we need to convert WHEN conditions to IF/THEN/END IF blocks
        sql_statements = []

        # If there are conditional statements, wrap them in IF blocks
        if trigger._when_list:
            condition = ' AND '.join(trigger._when_list)
            # Start the IF block
            sql_statements.append(f'IF {condition} THEN')

            # Add the SQL statements with indentation
            for stmt in trigger._sql_list:
                sql_statements.append(f'  {stmt}')

            # Close the IF block
            sql_statements.append('END IF;')
        else:
            # No conditions, just add the SQL statements directly
            sql_statements.extend(trigger._sql_list)

        # Join all statements
        trigger_body = '\n'.join(sql_statements)

        # Construct the final SQL
        sql = (
            f'CREATE TRIGGER {if_not_exists} {trigger.trigger_name}\n'
            f'{trigger.trigger_when} {trigger.trigger_action} ON {trigger.target_table}\n'
            f'FOR EACH ROW\n'
            f'BEGIN\n'
            f'{trigger_body}\n'
            f'END;'
        )
        return normalize_sql_spaces(sql)

    def select_all_trigger_sql(self) -> str:
        return 'SELECT trigger_name, event_object_table AS table_name FROM information_schema.TRIGGERS WHERE TRIGGER_SCHEMA = DATABASE();'

    def drop_trigger_sql(self, trigger_name: str, safe: bool = True, table_name: str | None = None) -> str:
        """Generate MySQL drop trigger SQL."""
        return normalize_sql_spaces(f'DROP TRIGGER {"IF EXISTS" if safe else ""} {trigger_name}')

    def supports_trigger_type(self, when: TriggerWhen, action: TriggerAction, on_view: bool = False) -> bool:
        """MySQL doesn't support INSTEAD OF triggers."""
        return when != TriggerWhen.Instead

    def supports_safe_create(self) -> bool:
        """MySQL supports IF NOT EXISTS for triggers."""
        return True

    def supports_update_of_columns(self) -> bool:
        """MySQL doesn't support column-specific UPDATE triggers."""
        return False

    def supports_when_clause(self) -> bool:
        """MySQL supports conditions but through WHERE instead of WHEN."""
        return True


class PostgreSQLDialect(TriggerDialect):
    """PostgreSQL-specific trigger SQL generation."""

    def create_trigger_sql(self, trigger: 'Trigger') -> str:
        """Generate PostgreSQL trigger SQL."""
        # PostgreSQL handles INSTEAD OF differently
        # PostgreSQL uses functions for trigger bodies

        function_name = f'fn_{trigger.trigger_name}'

        # First create the function
        function_sql = f'CREATE OR REPLACE FUNCTION {function_name}() RETURNS TRIGGER AS $$\nBEGIN\n'

        # Add WHEN condition as IF statements if needed
        if trigger._when_list:
            when_condition = ' AND '.join(trigger._when_list)
            function_sql += f'  IF {when_condition} THEN\n'
            # Indent SQL statements
            sql_statements = '\n'.join(['    ' + self._clean_sql(sql) for sql in trigger._sql_list])
            function_sql += f'{sql_statements}\n  END IF;\n'
        else:
            # Indent SQL statements
            sql_statements = '\n'.join(['    ' + self._clean_sql(sql) for sql in trigger._sql_list])
            function_sql += f'{sql_statements}\n'

        # For AFTER triggers, we need to return NULL or NEW
        if trigger.trigger_when == TriggerWhen.After:
            function_sql += '  RETURN NULL;\n'
        # For BEFORE or INSTEAD OF triggers, we need to return NEW
        else:
            function_sql += '  RETURN NEW;\n'

        function_sql += 'END;\n$$ LANGUAGE plpgsql;'

        # Then create the trigger - PostgreSQL doesn't support IF NOT EXISTS for triggers before v14
        # We'll handle this through a conditional drop
        drop_if_exists = ''
        if trigger.safe:
            drop_if_exists = f'DROP TRIGGER IF EXISTS {trigger.trigger_name} ON {trigger.target_table} CASCADE;\n'

        # PostgreSQL uses different syntax for INSTEAD OF (only allowed on views)
        trigger_when = trigger.trigger_when

        # Column-specific triggers in PostgreSQL
        of_columns = (
            f'OF {", ".join(trigger.update_columns)}'
            if trigger.update_columns and trigger.trigger_action == TriggerAction.Update
            else ''
        )

        for_each = 'FOR EACH ROW' if trigger.for_each_row else 'FOR EACH STATEMENT'

        trigger_sql = (
            f'{drop_if_exists}'
            f'CREATE TRIGGER  {trigger.trigger_name}\n'
            f'{trigger_when} {trigger.trigger_action} {of_columns} ON {trigger.target_table}\n'
            f'{for_each}\n'
            f'EXECUTE FUNCTION {function_name}();'
        )

        sql = f'{function_sql}\n\n{trigger_sql}'

        return normalize_sql_spaces(sql)

    def _clean_sql(self, sql: str) -> str:
        """
        Remove RETURNING clauses from SQL statements for PostgreSQL trigger functions.

        :param sql: The SQL statement
        :return: SQL statement without RETURNING clause
        """
        # Find the RETURNING clause position - case insensitive search
        sql_upper = sql.upper()
        returning_pos = sql_upper.find('RETURNING')

        # If RETURNING exists, remove it and everything after it up to the semicolon
        if returning_pos != -1:
            semicolon_pos = sql.find(';', returning_pos)
            if semicolon_pos != -1:
                return sql[:returning_pos] + ';'
            return sql[:returning_pos]
        return sql

    def drop_trigger_sql(self, trigger_name: str, safe: bool = True, table_name: str | None = None) -> str:
        """Generate PostgreSQL drop trigger SQL."""
        if table_name is None:
            raise RuntimeError('Cannot drop a trigger in PostgreSQL without a table_name')

        function_name = f'fn_{trigger_name}'
        return normalize_sql_spaces(
            f'DROP TRIGGER {"IF EXISTS" if safe else ""} {trigger_name} ON {table_name};\n'
            f'DROP FUNCTION {"IF EXISTS" if safe else ""} {function_name}();'
        )

    def select_all_trigger_sql(self) -> str:
        return "SELECT trigger_name, event_object_table AS table_name FROM information_schema.triggers WHERE trigger_schema NOT IN ('pg_catalog', 'information_schema');"

    def supports_trigger_type(self, when: TriggerWhen, action: TriggerAction, on_view: bool = False) -> bool:
        """PostgreSQL supports INSTEAD OF only on views."""
        if when == TriggerWhen.Instead and not on_view:
            return False
        return True

    def supports_safe_create(self) -> bool:
        """PostgreSQL doesn't support IF NOT EXISTS for triggers before v14, but we implement safety differently."""
        return True  # We report True but handle it with DROP IF EXISTS

    def supports_update_of_columns(self) -> bool:
        """PostgreSQL supports column-specific UPDATE triggers."""
        return True

    def supports_when_clause(self) -> bool:
        """PostgreSQL supports WHEN conditions."""
        return True


class Trigger:
    """Trigger template wrapper for use with peewee ORM."""

    # noinspection PyProtectedMember
    def __init__(
        self,
        trigger_name: str,
        trigger_type: tuple[TriggerWhen, TriggerAction],
        source_table: type[Model] | Model | str,
        safe: bool = False,
        for_each_row: bool = False,
        update_columns: list[str] | None = None,
        on_view: bool = False,  # Added parameter to indicate if the target is a view
    ):
        """
        Constructor parameters:

        :param trigger_name: The name of this trigger. It needs to be unique!
        :type trigger_name: str
        :param trigger_type: A tuple with :class:`TriggerWhen` and :class:`TriggerAction` to specify on which action
            the trigger should be invoked and if before, after or instead of.
        :type trigger_type: tuple[TriggerWhen, TriggerAction]
        :param source_table: The table originating the trigger. It can be a model class, instance, or also the name of
            the table.
        :type source_table: type[Model] | Model | str
        :param safe: A boolean flag to define if in the trigger creation statement a 'IF NOT EXISTS' clause should be
            included. Defaults to False
        :type safe: bool, Optional
        :param for_each_row: A boolean flag to repeat the script content for each modified row in the table.
            Defaults to False.
        :type for_each_row: bool, Optional
        :param update_columns: A list of column names. When defining a trigger on a table update, it is possible to
            restrict the firing of the trigger to the cases when a subset of all columns have been updated. An column
            is updated also when the new value is equal to the old one. If you want to discriminate this case, use the
            :meth:`add_when` method. Defaults to None.
        :type update_columns: list[str], Optional
        :param on_view: A boolean flag to indicate if the target is a view. This affects the support for INSTEAD OF.
            Defaults to False.
        :type on_view: bool, Optional
        """
        self.trigger_name = trigger_name
        self.trigger_type = trigger_type
        self._trigger_when, self._trigger_op = self.trigger_type
        self.update_columns = update_columns or []
        self.on_view = on_view

        if isinstance(source_table, type):
            model_cls = cast(PeeweeModelWithMeta, source_table)
            self.target_table = model_cls._meta.table_name
        elif isinstance(source_table, Model):
            model_instance = cast(PeeweeModelWithMeta, source_table)
            self.target_table = model_instance._meta.table_name
        else:
            self.target_table = source_table

        self.safe = safe
        self.for_each_row = for_each_row

        self._when_list: list[str] = []
        self._sql_list: list[str] = []
        self._database: peewee.Database | peewee.DatabaseProxy | None = None
        self._dialect: TriggerDialect | None = None

    @property
    def trigger_action(self) -> TriggerAction:
        return self._trigger_op

    @trigger_action.setter
    def trigger_action(self, action: TriggerAction) -> None:
        self._trigger_op = action

    @property
    def trigger_when(self) -> TriggerWhen:
        return self._trigger_when

    @trigger_when.setter
    def trigger_when(self, when: TriggerWhen) -> None:
        self._trigger_when = when

    def __setattr__(self, key: Any, value: Any) -> None:
        if key == 'safe':
            self.if_not_exists = 'IF NOT EXISTS' if value else ''
        elif key == 'for_each_row':
            self._for_each_row = 'FOR EACH ROW' if value else ''
        else:
            super().__setattr__(key, value)

    def __getattr__(self, item: str) -> Any:
        """
        Custom attribute getter for computed properties.

        :param item: The attribute name to get
        :return: The attribute value
        :raises AttributeError: If the attribute doesn't exist
        """
        if item == 'safe':
            return hasattr(self, 'if_not_exists') and self.if_not_exists == 'IF NOT EXISTS'
        elif item == 'for_each_row':
            return hasattr(self, '_for_each_row') and self._for_each_row == 'FOR EACH ROW'
        else:
            # Raise AttributeError for non-existent attributes (standard Python behaviour)
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")

    def add_sql(self, sql: str | peewee.Query) -> Self:
        """
        Add an SQL statement to be executed by the trigger.

        The ``sql`` can be either a string containing the sql statement, or it can be any other peewee Query.

        For example:

        .. code-block:: python

            # assuming you have created a trigger ...

            sql = AnotherTable.insert(
                field1=some_value, field2=another_value
            )
            trigger.add_sql(sql)

        In this way the SQL code is generated with parametric placeholder if needed.

        :param sql: The SQL statement.
        :type sql: str | peewee.Query
        :return: self for easy chaining
        :rtype: Trigger
        """
        if not isinstance(sql, str):
            sql = str(sql)
        sql = sql.strip()
        sql = chr(9) + sql
        if not sql.endswith(';'):
            sql += ';'
        self._sql_list.append(sql)
        return self

    def add_when(self, *conditions: str | peewee.Node) -> Self:
        """
        Add conditions to the `when` statements.

        Conditions are logically ANDed.
        To have mixed `OR` and `AND` logic, use the functions :func:`and_` and :func:`or_`.

        The ``conditions`` can be either strings containing SQL conditions, or peewee Node objects
        (such as Expression or Query objects).

        For example:

        .. code-block:: python

            # String condition
            trigger.add_when("NEW.status = 'active'")

            # Peewee expression
            subq = TriggerStatus.select(TriggerStatus.status).where(
                TriggerStatus.trigger_type == 'DELETE_FILES'
            )
            trigger.add_when(Value(1) == subq)

        .. versionchanged:: v2.0.0
            The argument can also be a generic peewee Node.

        :param conditions: Conditions to be added with logical AND. Can be strings or peewee Node objects.
        :type conditions: str | peewee.Node
        :return: self for easy chaining
        :rtype: Trigger
        """
        conditions_l = []
        for c in conditions:
            if isinstance(c, str):
                # Handle string conditions
                condition_str = c.strip()
            else:
                # Handle peewee Node/Expression/Query objects
                # Convert to SQL with parameters interpolated
                condition_str = self._node_to_sql(c).strip()

            conditions_l.append(f'({condition_str})')

        self._when_list.append(f'({" AND ".join(conditions_l)})')
        return self

    def _node_to_sql(self, node: peewee.Node) -> str:
        """
        Convert a peewee Node (Expression, Query, etc.) to a SQL string with interpolated parameters.

        This is based on peewee's internal query_to_string function for debugging/logging purposes.

        .. versionadded:: v2.0.0

        :param node: A peewee Node object
        :return: SQL string with parameters interpolated
        """
        from peewee import Context, Expression, Select

        # Check if this is an Expression with lhs and rhs attributes (like comparisons)
        if isinstance(node, Expression) and hasattr(node, 'lhs') and hasattr(node, 'rhs'):
            # Recursively convert left and right sides
            lhs_sql = self._node_to_sql(node.lhs) if isinstance(node.lhs, peewee.Node) else self._value_to_sql(node.lhs)
            rhs_sql = self._node_to_sql(node.rhs) if isinstance(node.rhs, peewee.Node) else self._value_to_sql(node.rhs)

            # Get the operator (e.g., '=', '>', '<', etc.)
            op = getattr(node, 'op', '=')

            # For subqueries on either side, wrap them in parentheses
            if isinstance(node.lhs, Select):
                lhs_sql = f'({lhs_sql})'
            if isinstance(node.rhs, Select):
                rhs_sql = f'({rhs_sql})'

            return f'{lhs_sql} {op} {rhs_sql}'

        # For other node types, use the standard Context approach
        # Get database context if available, otherwise use a default Context
        db = self._database
        if db is not None and isinstance(db, peewee.DatabaseProxy):
            db = db.obj  # Get the actual database from the proxy

        if db is not None:
            ctx = db.get_sql_context()
        else:
            ctx = Context()

        # Generate SQL with parameters
        sql, params = ctx.sql(node).query()

        # If no parameters, return as-is
        if not params:
            return cast(str, sql)

        # Interpolate parameters into the SQL string
        # This is safe for trigger definitions (not for execution)
        param_placeholder = getattr(ctx.state, 'param', '?') or '?'
        if param_placeholder == '?':
            sql = sql.replace('?', '%s')

        # Transform parameters to SQL-safe values
        transformed_params = [self._value_to_sql(v) for v in params]

        interpolated_str = sql % tuple(transformed_params)
        return cast(str, interpolated_str)

    def _value_to_sql(self, value: Any) -> str:
        """
        Convert a Python value to its SQL representation.

        .. versionadded:: v2.0.0

        :param value: A Python value (string, int, float, None, etc.)
        :return: SQL string representation of the value
        """
        if isinstance(value, str):
            # Escape single quotes by doubling them
            escaped = value.replace("'", "''")
            return f"'{escaped}'"
        elif isinstance(value, bool):  # bools are numbers as well!
            return '1' if value else '0'
        elif isinstance(value, (int, float)):
            return str(value)
        elif value is None:
            return 'NULL'
        else:
            return str(value)

    def set_database(self, database: peewee.Database | peewee.DatabaseProxy) -> Self:
        """
        Set the database to use for this trigger.

        :param database: The database instance
        :return: self for easy chaining
        """
        self._database = database
        return self

    def _get_dialect(self) -> TriggerDialect:
        """
        Get the appropriate dialect based on the database type.

        :return: A dialect instance
        """
        if self._dialect is not None:
            return self._dialect

        if self._database is None:
            # Default to SQLite dialect
            return SQLiteDialect()

        db = self._database
        if isinstance(db, peewee.DatabaseProxy):
            db = db.obj  # Get the actual database from the proxy

        if isinstance(db, peewee.SqliteDatabase):
            self._dialect = SQLiteDialect()
        elif isinstance(db, peewee.MySQLDatabase):
            self._dialect = MySQLDialect()
        elif isinstance(db, peewee.PostgresqlDatabase):
            self._dialect = PostgreSQLDialect()
        else:
            raise UnsupportedDatabaseError(f'Unsupported database type: {type(db)}')

        return self._dialect

    def create(self) -> str:
        """
        Generates the SQL create statement.

        :return: The trigger creation statement.
        :raise MissingSQLStatement: if no SQL statements are provided.
        :raise UnsupportedDatabaseError: if the trigger type is not supported by the database.
        """
        if len(self._sql_list) == 0:
            raise MissingSQLStatement('No SQL statements provided')

        dialect = self._get_dialect()

        # Check if the trigger type is supported
        if not dialect.supports_trigger_type(self.trigger_when, self.trigger_action, self.on_view):
            raise UnsupportedDatabaseError(
                f'Trigger type {self.trigger_when} {self.trigger_action} is not supported by the database'
            )

        # Check if safe create is supported
        if self.safe and not dialect.supports_safe_create():
            # We can either ignore and continue without safe, or raise an error
            # For now, we'll just ignore and continue
            self.safe = False

        # Check if update columns are supported
        if self.update_columns and not dialect.supports_update_of_columns():
            # We can either ignore and continue without column-specific updates, or raise an error
            # For now, we'll ignore and continue
            self.update_columns = []

        # Generate the SQL
        return dialect.create_trigger_sql(self)

    def drop(self, safe: bool = True) -> str:
        """
        Generates the SQL drop statement.

        :param safe: If True, add an IF EXIST. Defaults to True.
        :type safe: bool, Optional
        :return: The drop statement
        :rtype: str
        """
        dialect = self._get_dialect()
        return dialect.drop_trigger_sql(self.trigger_name, safe)
