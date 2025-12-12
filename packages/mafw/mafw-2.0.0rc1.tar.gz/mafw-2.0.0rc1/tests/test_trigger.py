#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Unit tests for trigger.py module.

Tests for and_, or_, TriggerWhen, TriggerAction, and Trigger classes.
"""

import sys
from unittest.mock import MagicMock, Mock, patch

import peewee
import pytest
from peewee import Model

from mafw.db.trigger import (
    Trigger,
    TriggerAction,
    TriggerWhen,
    and_,
    or_,
)
from mafw.mafw_errors import MissingSQLStatement, UnsupportedDatabaseError


class TestLogicalOperators:
    """Test cases for and_ and or_ functions."""

    def test_and_single_condition(self):
        """Test and_ function with single condition."""
        result = and_('condition1')
        assert result == '(condition1)'

    def test_and_multiple_conditions(self):
        """Test and_ function with multiple conditions."""
        result = and_('condition1', 'condition2', 'condition3')
        assert result == '(condition1) AND (condition2) AND (condition3)'

    def test_and_empty_conditions(self):
        """Test and_ function with no conditions."""
        result = and_()
        assert result == ''

    def test_or_single_condition(self):
        """Test or_ function with single condition."""
        result = or_('condition1')
        assert result == '(condition1)'

    def test_or_multiple_conditions(self):
        """Test or_ function with multiple conditions."""
        result = or_('condition1', 'condition2', 'condition3')
        assert result == '(condition1) OR (condition2) OR (condition3)'

    def test_or_empty_conditions(self):
        """Test or_ function with no conditions."""
        result = or_()
        assert result == ''

    def test_and_with_complex_conditions(self):
        """Test and_ function with complex conditions containing spaces and operators."""
        result = and_("field1 = 'value1'", 'field2 > 10', 'field3 IS NOT NULL')
        expected = "(field1 = 'value1') AND (field2 > 10) AND (field3 IS NOT NULL)"
        assert result == expected

    def test_or_with_complex_conditions(self):
        """Test or_ function with complex conditions containing spaces and operators."""
        result = or_("field1 = 'value1'", 'field2 > 10', 'field3 IS NOT NULL')
        expected = "(field1 = 'value1') OR (field2 > 10) OR (field3 IS NOT NULL)"
        assert result == expected


class TestTriggerWhen:
    """Test cases for TriggerWhen enum."""

    def test_trigger_when_values(self):
        """Test that TriggerWhen enum has correct values."""
        assert TriggerWhen.Before == 'BEFORE'
        assert TriggerWhen.After == 'AFTER'
        assert TriggerWhen.Instead == 'INSTEAD OF'

    def test_trigger_when_string_representation(self):
        """Test string representation of TriggerWhen enum values."""
        assert str(TriggerWhen.Before) == 'BEFORE'
        assert str(TriggerWhen.After) == 'AFTER'
        assert str(TriggerWhen.Instead) == 'INSTEAD OF'

    @pytest.mark.skipif(sys.version_info < (3, 12), reason='bug in python < 3.12')
    def test_trigger_when_enum_membership(self):
        """Test membership in TriggerWhen enum."""
        assert 'BEFORE' in TriggerWhen
        assert 'AFTER' in TriggerWhen
        assert 'INSTEAD OF' in TriggerWhen
        assert 'INVALID' not in TriggerWhen


class TestTriggerAction:
    """Test cases for TriggerAction enum."""

    def test_trigger_action_values(self):
        """Test that TriggerAction enum has correct values."""
        assert TriggerAction.Delete == 'DELETE'
        assert TriggerAction.Insert == 'INSERT'
        assert TriggerAction.Update == 'UPDATE'

    def test_trigger_action_string_representation(self):
        """Test string representation of TriggerAction enum values."""
        assert str(TriggerAction.Delete) == 'DELETE'
        assert str(TriggerAction.Insert) == 'INSERT'
        assert str(TriggerAction.Update) == 'UPDATE'

    @pytest.mark.skipif(sys.version_info < (3, 12), reason='bug in python < 3.12')
    def test_trigger_action_enum_membership(self):
        """Test membership in TriggerAction enum."""
        assert 'DELETE' in TriggerAction
        assert 'INSERT' in TriggerAction
        assert 'UPDATE' in TriggerAction
        assert 'INVALID' not in TriggerAction


class TestTrigger:
    """Test cases for Trigger class."""

    @pytest.fixture
    def mock_model_class(self):
        """Mock model class with _meta attribute."""
        mock_class = Mock(spec=type)
        mock_class._meta = Mock()
        mock_class._meta.table_name = 'test_table'
        return mock_class

    @pytest.fixture
    def mock_model_instance(self):
        """Mock model instance with _meta attribute."""
        mock_instance = Mock(spec=Model)
        mock_instance._meta = Mock()
        mock_instance._meta.table_name = 'test_table'
        return mock_instance

    @pytest.fixture
    def mock_database(self):
        """Mock database instance."""
        return Mock(spec=peewee.SqliteDatabase)

    @pytest.fixture
    def mock_database_proxy(self):
        """Mock database proxy instance."""
        proxy = Mock(spec=peewee.DatabaseProxy)
        proxy.obj = Mock(spec=peewee.SqliteDatabase)
        return proxy

    @pytest.fixture
    def basic_trigger(self):
        """Basic trigger instance for testing."""
        return Trigger(
            trigger_name='test_trigger',
            trigger_type=(TriggerWhen.After, TriggerAction.Insert),
            source_table='test_table',
        )

    def test_trigger_init_with_string_table(self):
        """Test Trigger initialization with string table name."""
        trigger = Trigger(
            trigger_name='test_trigger',
            trigger_type=(TriggerWhen.After, TriggerAction.Insert),
            source_table='test_table',
        )

        assert trigger.trigger_name == 'test_trigger'
        assert trigger.trigger_when == TriggerWhen.After
        assert trigger.trigger_action == TriggerAction.Insert
        assert trigger.target_table == 'test_table'
        assert trigger.safe is False
        assert trigger.for_each_row is False
        assert trigger.update_columns == []
        assert trigger.on_view is False

    def test_trigger_init_with_model_class(self, mock_model_class):
        """Test Trigger initialization with model class."""
        trigger = Trigger(
            trigger_name='test_trigger',
            trigger_type=(TriggerWhen.Before, TriggerAction.Update),
            source_table=mock_model_class,
        )

        assert trigger.target_table == 'test_table'

    def test_trigger_init_with_model_instance(self, mock_model_instance):
        """Test Trigger initialization with model instance."""
        trigger = Trigger(
            trigger_name='test_trigger',
            trigger_type=(TriggerWhen.Instead, TriggerAction.Delete),
            source_table=mock_model_instance,
        )

        assert trigger.target_table == 'test_table'

    def test_trigger_init_with_optional_parameters(self):
        """Test Trigger initialization with all optional parameters."""
        trigger = Trigger(
            trigger_name='test_trigger',
            trigger_type=(TriggerWhen.Before, TriggerAction.Update),
            source_table='test_table',
            safe=True,
            for_each_row=True,
            update_columns=['col1', 'col2'],
            on_view=True,
        )

        assert trigger.safe is True
        assert trigger.for_each_row is True
        assert trigger.update_columns == ['col1', 'col2']
        assert trigger.on_view is True

    def test_trigger_property_setters(self, basic_trigger):
        """Test trigger action and when property setters."""
        basic_trigger.trigger_action = TriggerAction.Update
        basic_trigger.trigger_when = TriggerWhen.Before

        assert basic_trigger.trigger_action == TriggerAction.Update
        assert basic_trigger.trigger_when == TriggerWhen.Before

    def test_setattr_safe_property(self, basic_trigger):
        """Test __setattr__ for safe property."""
        basic_trigger.safe = True
        assert hasattr(basic_trigger, 'if_not_exists')
        assert basic_trigger.if_not_exists == 'IF NOT EXISTS'

        basic_trigger.safe = False
        assert basic_trigger.if_not_exists == ''

    def test_setattr_for_each_row_property(self, basic_trigger):
        """Test __setattr__ for for_each_row property."""
        basic_trigger.for_each_row = True
        assert hasattr(basic_trigger, '_for_each_row')
        assert basic_trigger._for_each_row == 'FOR EACH ROW'

        basic_trigger.for_each_row = False
        assert basic_trigger._for_each_row == ''

    def test_getattr_safe_property(self, basic_trigger):
        """Test __getattr__ for safe property."""
        basic_trigger.if_not_exists = 'IF NOT EXISTS'
        result = basic_trigger.__getattr__('safe')
        assert result is True

        basic_trigger.if_not_exists = ''
        result = basic_trigger.__getattr__('safe')
        assert result is False

    def test_getattr_for_each_row_property(self, basic_trigger):
        """Test __getattr__ for for_each_row property."""
        basic_trigger._for_each_row = 'FOR EACH ROW'
        result = basic_trigger.__getattr__('for_each_row')
        assert result is True

        basic_trigger._for_each_row = ''
        result = basic_trigger.__getattr__('for_each_row')
        assert result is False

    def test_getattr_nonexistent_attribute(self, basic_trigger):
        """Test __getattr__ for non-existent attribute raises AttributeError."""
        with pytest.raises(AttributeError, match="'Trigger' object has no attribute 'nonexistent'"):
            basic_trigger.__getattr__('nonexistent')

    def test_getattr_safe_property_without_if_not_exists(self, basic_trigger):
        """Test __getattr__ for safe property when if_not_exists doesn't exist."""
        # Don't set if_not_exists at all
        result = basic_trigger.__getattr__('safe')
        assert result is False

    def test_getattr_for_each_row_without_internal_attr(self, basic_trigger):
        """Test __getattr__ for for_each_row property when _for_each_row doesn't exist."""
        # Don't set _for_each_row at all
        result = basic_trigger.__getattr__('for_each_row')
        assert result is False

    def test_add_sql_with_string(self, basic_trigger):
        """Test add_sql method with string input."""
        sql = "INSERT INTO another_table VALUES (1, 'test')"
        result = basic_trigger.add_sql(sql)

        assert result is basic_trigger  # Method should return self for chaining
        assert len(basic_trigger._sql_list) == 1
        assert basic_trigger._sql_list[0] == "\tINSERT INTO another_table VALUES (1, 'test');"

    def test_add_sql_with_query_object(self, basic_trigger):
        """Test add_sql method with peewee Query object."""
        mock_query = Mock()
        mock_query.__str__ = Mock(return_value='SELECT * FROM test')

        result = basic_trigger.add_sql(mock_query)

        assert result is basic_trigger
        assert len(basic_trigger._sql_list) == 1
        assert basic_trigger._sql_list[0] == '\tSELECT * FROM test;'

    def test_add_sql_with_semicolon(self, basic_trigger):
        """Test add_sql method with SQL that already has semicolon."""
        sql = 'DELETE FROM test_table WHERE id = 1;'
        basic_trigger.add_sql(sql)

        assert basic_trigger._sql_list[0] == '\tDELETE FROM test_table WHERE id = 1;'

    def test_add_sql_multiple_statements(self, basic_trigger):
        """Test adding multiple SQL statements."""
        basic_trigger.add_sql('INSERT INTO table1 VALUES (1)')
        basic_trigger.add_sql("UPDATE table2 SET col1 = 'value'")

        assert len(basic_trigger._sql_list) == 2
        assert basic_trigger._sql_list[0] == '\tINSERT INTO table1 VALUES (1);'
        assert basic_trigger._sql_list[1] == "\tUPDATE table2 SET col1 = 'value';"

    def test_add_when_single_condition(self, basic_trigger):
        """Test add_when method with single condition."""
        result = basic_trigger.add_when('NEW.field1 > OLD.field1')

        assert result is basic_trigger
        assert len(basic_trigger._when_list) == 1
        assert basic_trigger._when_list[0] == '((NEW.field1 > OLD.field1))'

    def test_add_when_multiple_conditions(self, basic_trigger):
        """Test add_when method with multiple conditions."""
        basic_trigger.add_when('NEW.field1 > OLD.field1', 'NEW.field2 IS NOT NULL')

        assert len(basic_trigger._when_list) == 1
        assert basic_trigger._when_list[0] == '((NEW.field1 > OLD.field1) AND (NEW.field2 IS NOT NULL))'

    def test_add_when_multiple_calls(self, basic_trigger):
        """Test multiple calls to add_when method."""
        basic_trigger.add_when('condition1')
        basic_trigger.add_when('condition2', 'condition3')

        assert len(basic_trigger._when_list) == 2
        assert basic_trigger._when_list[0] == '((condition1))'
        assert basic_trigger._when_list[1] == '((condition2) AND (condition3))'

    def test_set_database(self, basic_trigger, mock_database):
        """Test set_database method."""
        result = basic_trigger.set_database(mock_database)

        assert result is basic_trigger
        assert basic_trigger._database is mock_database

    @patch('mafw.db.trigger.SQLiteDialect')
    def test_get_dialect_sqlite(self, mock_sqlite_dialect, basic_trigger, mock_database):
        """Test _get_dialect method with SQLite database."""
        mock_sqlite_db = Mock(spec=peewee.SqliteDatabase)
        basic_trigger._database = mock_sqlite_db

        basic_trigger._get_dialect()

        mock_sqlite_dialect.assert_called_once()
        assert basic_trigger._dialect is not None

    @patch('mafw.db.trigger.MySQLDialect')
    def test_get_dialect_mysql(self, mock_mysql_dialect, basic_trigger):
        """Test _get_dialect method with MySQL database."""
        mock_mysql_db = Mock(spec=peewee.MySQLDatabase)
        basic_trigger._database = mock_mysql_db

        basic_trigger._get_dialect()

        mock_mysql_dialect.assert_called_once()

    @patch('mafw.db.trigger.PostgreSQLDialect')
    def test_get_dialect_postgresql(self, mock_postgresql_dialect, basic_trigger):
        """Test _get_dialect method with PostgreSQL database."""
        mock_postgresql_db = Mock(spec=peewee.PostgresqlDatabase)
        basic_trigger._database = mock_postgresql_db

        basic_trigger._get_dialect()

        mock_postgresql_dialect.assert_called_once()

    def test_get_dialect_database_proxy(self, basic_trigger, mock_database_proxy):
        """Test _get_dialect method with database proxy."""
        basic_trigger._database = mock_database_proxy

        with patch('mafw.db.trigger.SQLiteDialect') as mock_sqlite_dialect:
            basic_trigger._get_dialect()
            mock_sqlite_dialect.assert_called_once()

    def test_get_dialect_unsupported_database(self, basic_trigger):
        """Test _get_dialect method with unsupported database."""
        unsupported_db = Mock()
        basic_trigger._database = unsupported_db

        with pytest.raises(UnsupportedDatabaseError):
            basic_trigger._get_dialect()

    def test_get_dialect_no_database_defaults_to_sqlite(self, basic_trigger):
        """Test _get_dialect method with no database set (defaults to SQLite)."""
        with patch('mafw.db.trigger.SQLiteDialect') as mock_sqlite_dialect:
            basic_trigger._get_dialect()
            mock_sqlite_dialect.assert_called_once()

    def test_get_dialect_caching(self, basic_trigger, mock_database):
        """Test that _get_dialect caches the dialect instance."""
        basic_trigger._database = mock_database

        with patch('mafw.db.trigger.SQLiteDialect') as mock_sqlite_dialect:
            dialect1 = basic_trigger._get_dialect()
            dialect2 = basic_trigger._get_dialect()

            # Should only be called once due to caching
            mock_sqlite_dialect.assert_called_once()
            assert dialect1 is dialect2

    def test_create_no_sql_statements(self, basic_trigger):
        """Test create method with no SQL statements raises error."""
        with pytest.raises(MissingSQLStatement):
            basic_trigger.create()

    def test_create_with_sql_statements(self, basic_trigger):
        """Test create method with SQL statements."""
        basic_trigger.add_sql('INSERT INTO test VALUES (1)')

        with patch.object(basic_trigger, '_get_dialect') as mock_get_dialect:
            mock_dialect = Mock()
            mock_dialect.supports_trigger_type.return_value = True
            mock_dialect.supports_safe_create.return_value = True
            mock_dialect.supports_update_of_columns.return_value = True
            mock_dialect.create_trigger_sql.return_value = 'CREATE TRIGGER test_sql'
            mock_get_dialect.return_value = mock_dialect

            result = basic_trigger.create()

            assert result == 'CREATE TRIGGER test_sql'
            mock_dialect.supports_trigger_type.assert_called_once_with(
                basic_trigger.trigger_when, basic_trigger.trigger_action, basic_trigger.on_view
            )
            mock_dialect.create_trigger_sql.assert_called_once_with(basic_trigger)

    def test_create_unsupported_trigger_type(self, basic_trigger):
        """Test create method with unsupported trigger type."""
        basic_trigger.add_sql('INSERT INTO test VALUES (1)')

        with patch.object(basic_trigger, '_get_dialect') as mock_get_dialect:
            mock_dialect = Mock()
            mock_dialect.supports_trigger_type.return_value = False
            mock_get_dialect.return_value = mock_dialect

            with pytest.raises(UnsupportedDatabaseError):
                basic_trigger.create()

    def test_create_unsupported_safe_create(self, basic_trigger):
        """Test create method when safe create is not supported."""
        basic_trigger.add_sql('INSERT INTO test VALUES (1)')
        basic_trigger.safe = True

        with patch.object(basic_trigger, '_get_dialect') as mock_get_dialect:
            mock_dialect = Mock()
            mock_dialect.supports_trigger_type.return_value = True
            mock_dialect.supports_safe_create.return_value = False
            mock_dialect.supports_update_of_columns.return_value = True
            mock_dialect.create_trigger_sql.return_value = 'CREATE TRIGGER test_sql'
            mock_get_dialect.return_value = mock_dialect

            result = basic_trigger.create()

            assert basic_trigger.safe is False
            assert result == 'CREATE TRIGGER test_sql'

    def test_create_unsupported_update_columns(self, basic_trigger):
        """Test create method when update columns are not supported."""
        basic_trigger.add_sql('INSERT INTO test VALUES (1)')
        basic_trigger.update_columns = ['col1', 'col2']

        with patch.object(basic_trigger, '_get_dialect') as mock_get_dialect:
            mock_dialect = Mock()
            mock_dialect.supports_trigger_type.return_value = True
            mock_dialect.supports_safe_create.return_value = True
            mock_dialect.supports_update_of_columns.return_value = False
            mock_dialect.create_trigger_sql.return_value = 'CREATE TRIGGER test_sql'
            mock_get_dialect.return_value = mock_dialect

            result = basic_trigger.create()

            assert basic_trigger.update_columns == []
            assert result == 'CREATE TRIGGER test_sql'

    def test_drop_default_safe(self, basic_trigger):
        """Test drop method with default safe parameter."""
        with patch.object(basic_trigger, '_get_dialect') as mock_get_dialect:
            mock_dialect = Mock()
            mock_dialect.drop_trigger_sql.return_value = 'DROP TRIGGER IF EXISTS test_trigger'
            mock_get_dialect.return_value = mock_dialect

            result = basic_trigger.drop()

            assert result == 'DROP TRIGGER IF EXISTS test_trigger'
            mock_dialect.drop_trigger_sql.assert_called_once_with('test_trigger', True)

    def test_drop_safe_false(self, basic_trigger):
        """Test drop method with safe=False."""
        with patch.object(basic_trigger, '_get_dialect') as mock_get_dialect:
            mock_dialect = Mock()
            mock_dialect.drop_trigger_sql.return_value = 'DROP TRIGGER test_trigger'
            mock_get_dialect.return_value = mock_dialect

            result = basic_trigger.drop(safe=False)

            assert result == 'DROP TRIGGER test_trigger'
            mock_dialect.drop_trigger_sql.assert_called_once_with('test_trigger', False)

    @pytest.mark.parametrize(
        'trigger_when,trigger_action,expected_when,expected_action',
        [
            (TriggerWhen.Before, TriggerAction.Insert, TriggerWhen.Before, TriggerAction.Insert),
            (TriggerWhen.After, TriggerAction.Update, TriggerWhen.After, TriggerAction.Update),
            (TriggerWhen.Instead, TriggerAction.Delete, TriggerWhen.Instead, TriggerAction.Delete),
        ],
    )
    def test_trigger_types_parametrized(self, trigger_when, trigger_action, expected_when, expected_action):
        """Parametrized test for different trigger types."""
        trigger = Trigger(
            trigger_name='test_trigger', trigger_type=(trigger_when, trigger_action), source_table='test_table'
        )

        assert trigger.trigger_when == expected_when
        assert trigger.trigger_action == expected_action

    @pytest.mark.parametrize(
        'safe,for_each_row,on_view',
        [
            (True, True, True),
            (True, False, False),
            (False, True, False),
            (False, False, True),
        ],
    )
    def test_trigger_boolean_flags_parametrized(self, safe, for_each_row, on_view):
        """Parametrized test for boolean flags."""
        trigger = Trigger(
            trigger_name='test_trigger',
            trigger_type=(TriggerWhen.After, TriggerAction.Insert),
            source_table='test_table',
            safe=safe,
            for_each_row=for_each_row,
            on_view=on_view,
        )

        assert trigger.safe == safe
        assert trigger.for_each_row == for_each_row
        assert trigger.on_view == on_view

    def test_trigger_chaining_methods(self, basic_trigger):
        """Test that methods return self for method chaining."""
        result = basic_trigger.add_sql('INSERT INTO test VALUES (1)').add_when('NEW.id > 0').set_database(Mock())

        assert result is basic_trigger
        assert len(basic_trigger._sql_list) == 1
        assert len(basic_trigger._when_list) == 1
        assert basic_trigger._database is not None


class DummyModel(peewee.Model):
    value = peewee.IntegerField()

    class Meta:
        database = peewee.SqliteDatabase(':memory:')
        table_name = 'dummy_table'


class TestNodeToSql:
    """Tests for Trigger._node_to_sql"""

    @pytest.fixture
    def trigger(self):
        """Trigger instance with no DB by default."""
        return Trigger(trigger_name='t1', trigger_type=(None, None), source_table='dummy')

    # -------------------------------------------------------
    # Expression with lhs, rhs, operator
    # -------------------------------------------------------

    def test_expression_simple(self, trigger):
        """Test basic Expression conversion lhs = rhs."""
        expr = DummyModel.value == 5  # peewee Expression
        sql = trigger._node_to_sql(expr)
        assert sql == '"t1"."value" = 5'

    def test_expression_nested(self, trigger):
        """Test nested expressions and recursion."""
        expr = (DummyModel.value + 1) == (DummyModel.value - 2)
        sql = trigger._node_to_sql(expr)
        assert '"t1"."value" + 1' in sql
        assert '"t1"."value" - 2' in sql
        assert ' = ' in sql

    # -------------------------------------------------------
    # Subquery handling
    # -------------------------------------------------------

    def test_expression_with_subquery_rhs(self, trigger):
        """Test wrapping subqueries in parentheses."""
        subq = DummyModel.select(DummyModel.value).where(DummyModel.value == 1)
        expr = DummyModel.value == subq
        sql = trigger._node_to_sql(expr)
        assert '"t1"."value" = (' in sql
        assert '(SELECT' in sql

    def test_expression_with_subquery_lhs(self, trigger):
        """Test wrapping subqueries in parentheses."""
        subq = DummyModel.select(DummyModel.value).where(DummyModel.value == 1)
        expr = subq == DummyModel.value
        sql = trigger._node_to_sql(expr)
        assert ') = "t1"."value"' in sql
        assert '(SELECT' in sql

    # -------------------------------------------------------
    # Context-based SQL generation (non-expression node)
    # -------------------------------------------------------

    def test_node_no_params(self, trigger):
        """Test context SQL generation when the peewee node has no params."""
        node = peewee.SQL('SOME RAW SQL')
        sql = trigger._node_to_sql(node)
        assert sql == 'SOME RAW SQL'

    def test_node_with_params(self, trigger):
        """Test interpolation of parameters into SQL."""
        # patch database context to return parameters
        mock_db = MagicMock()
        mock_ctx = MagicMock()

        mock_state = MagicMock()
        mock_state.param = '?'
        mock_ctx.state = mock_state

        mock_ctx.sql().query.return_value = ('x = ?', [123])

        mock_db.get_sql_context.return_value = mock_ctx

        trigger.set_database(mock_db)

        node = peewee.SQL('x = ?')
        sql = trigger._node_to_sql(node)
        assert sql == 'x = 123'

    # -------------------------------------------------------
    # Bool, None, string handling inside parameter interpolation
    # -------------------------------------------------------

    @pytest.mark.parametrize(
        'value,expected_fragment',
        [
            ('hello', "'hello'"),
            ("O'Hara", "'O''Hara'"),
            (None, 'NULL'),
            (True, '1'),
            (False, '0'),
            (42, '42'),
        ],
    )
    def test_param_interpolation(self, trigger, value, expected_fragment):
        """Test parameter interpolation with mixed types."""
        mock_db = MagicMock()
        mock_ctx = MagicMock()

        mock_ctx.state.param = '?'  # peewee default
        mock_ctx.sql().query.return_value = ('val = ?', [value])

        mock_db.get_sql_context.return_value = mock_ctx
        trigger.set_database(mock_db)

        node = peewee.SQL('val = ?')
        sql = trigger._node_to_sql(node)
        assert expected_fragment in sql

    @pytest.mark.parametrize(
        'value,expected_fragment',
        [
            ('hello', "'hello'"),
            ("O'Hara", "'O''Hara'"),
            (None, 'NULL'),
            (True, '1'),
            (False, '0'),
            (42, '42'),
        ],
    )
    def test_param_interpolation_with_s(self, trigger, value, expected_fragment):
        """Test parameter interpolation with mixed types."""
        mock_db = MagicMock()
        mock_ctx = MagicMock()

        mock_ctx.state.param = '%s'  # peewee default
        mock_ctx.sql().query.return_value = ('val = %s', [value])

        mock_db.get_sql_context.return_value = mock_ctx
        trigger.set_database(mock_db)

        node = peewee.SQL('val = %s')
        sql = trigger._node_to_sql(node)
        assert expected_fragment in sql

    # -------------------------------------------------------
    # DatabaseProxy handling
    # -------------------------------------------------------

    def test_database_proxy(self, trigger):
        """Ensure DatabaseProxy obj is correctly unwrapped."""
        proxy = peewee.DatabaseProxy()
        real_db = MagicMock()
        proxy.initialize(real_db)

        real_ctx = MagicMock()
        real_ctx.sql().query.return_value = ('a = ?', [7])
        real_ctx.state.param = '?'

        real_db.get_sql_context.return_value = real_ctx

        trigger.set_database(proxy)

        sql = trigger._node_to_sql(peewee.SQL('a = ?'))
        assert sql == 'a = 7'

    # -------------------------------------------------------
    # Unsupported complex object on rhs/lhs
    # -------------------------------------------------------

    def test_expression_rhs_unsupported_value(self, trigger):
        """If rhs is a non-node python value, ensure _value_to_sql() is used."""

        class X:
            def __str__(self):
                return 'XXX'

        expr = DummyModel.value == X()
        sql = trigger._node_to_sql(expr)
        assert sql.endswith('= XXX')


class TestValueToSql:
    """Tests for Trigger._value_to_sql"""

    @pytest.fixture
    def trigger(self):
        """Return a basic trigger instance for testing."""
        return Trigger(trigger_name='t1', trigger_type=(None, None), source_table='dummy')

    @pytest.mark.parametrize(
        'value,expected',
        [
            ('hello', "'hello'"),
            ("O'Hara", "'O''Hara'"),  # escaped quotes
            (42, '42'),
            (3.14, '3.14'),
            (None, 'NULL'),
            (True, '1'),
            (False, '0'),
        ],
    )
    def test_value_basic_types(self, trigger, value, expected):
        """Test correct SQL formatting for simple python values."""
        assert trigger._value_to_sql(value) == expected

    def test_value_other_object(self, trigger):
        """Test fallback to str() for unsupported types."""

        class X:
            def __str__(self):
                return 'XOBJ'

        assert trigger._value_to_sql(X()) == 'XOBJ'
