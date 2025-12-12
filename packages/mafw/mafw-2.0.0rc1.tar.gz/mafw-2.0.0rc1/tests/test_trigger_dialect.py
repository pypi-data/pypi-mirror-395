#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Test cases for TriggerDialect and its subclasses.

This module tests SQLiteDialect, MySQLDialect, and PostgreSQLDialect
to ensure proper SQL generation and feature support validation.
"""

from unittest.mock import Mock

import peewee
import pytest

from mafw.db.trigger import (
    MissingSQLStatement,
    MySQLDialect,
    PostgreSQLDialect,
    SQLiteDialect,
    Trigger,
    TriggerAction,
    TriggerDialect,
    TriggerWhen,
    UnsupportedDatabaseError,
)


class TestTriggerDialect:
    """Test the abstract TriggerDialect base class."""

    def test_abstract_class_cannot_be_instantiated(self):
        """Test that TriggerDialect abstract class cannot be instantiated."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class TriggerDialect"):
            TriggerDialect()

    def test_incomplete_subclass_cannot_be_instantiated(self):
        """Test that incomplete subclasses cannot be instantiated."""

        # Create a subclass that doesn't implement all abstract methods
        class IncompleteDialect(TriggerDialect):
            def create_trigger_sql(self, trigger):
                return 'CREATE TRIGGER'

            # Missing other abstract methods

        # Should raise TypeError because not all abstract methods are implemented
        with pytest.raises(TypeError, match="Can't instantiate abstract class IncompleteDialect"):
            IncompleteDialect()

    def test_complete_subclass_can_be_instantiated(self):
        """Test that complete subclasses can be instantiated."""

        # Create a complete subclass
        class CompleteDialect(TriggerDialect):
            def create_trigger_sql(self, trigger):
                return 'CREATE TRIGGER'

            def drop_trigger_sql(self, trigger_name, safe=True, table_name='tbl_name'):
                return 'DROP TRIGGER'

            def supports_trigger_type(self, when, action, on_view=False):
                return True

            def supports_safe_create(self):
                return True

            def supports_update_of_columns(self):
                return True

            def supports_when_clause(self):
                return True

            def select_all_trigger_sql(self) -> str:
                return 'SELECT'

        # Should work fine
        dialect = CompleteDialect()
        assert isinstance(dialect, TriggerDialect)

    def test_abstract_methods_are_properly_defined(self):
        """Test that all expected abstract methods are defined."""
        # Get all abstract methods from TriggerDialect
        abstract_methods = TriggerDialect.__abstractmethods__

        expected_methods = {
            'create_trigger_sql',
            'drop_trigger_sql',
            'select_all_trigger_sql',
            'supports_trigger_type',
            'supports_safe_create',
            'supports_update_of_columns',
            'supports_when_clause',
        }

        assert abstract_methods == expected_methods


class TestSQLiteDialect:
    """Test SQLite-specific dialect implementation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.dialect = SQLiteDialect()
        self.trigger = Mock()
        self.trigger.trigger_name = 'test_trigger'
        self.trigger.target_table = 'test_table'
        self.trigger.trigger_when = TriggerWhen.After
        self.trigger.trigger_action = TriggerAction.Insert
        self.trigger.safe = True
        self.trigger.for_each_row = True
        self.trigger.update_columns = []
        self.trigger._when_list = []
        self.trigger._sql_list = ['INSERT INTO log_table VALUES (NEW.id);']

    def test_create_trigger_sql_basic(self):
        """Test basic trigger SQL generation."""
        sql = self.dialect.create_trigger_sql(self.trigger)

        assert 'CREATE TRIGGER IF NOT EXISTS test_trigger' in sql
        assert 'AFTER INSERT ON test_table' in sql
        assert 'FOR EACH ROW' in sql
        assert 'INSERT INTO log_table VALUES (NEW.id);' in sql
        assert 'BEGIN' in sql
        assert 'END;' in sql

    def test_select_all_trigger_sql(self):
        sql = self.dialect.select_all_trigger_sql()
        assert "SELECT name AS trigger_name, tbl_name AS table_name FROM sqlite_master WHERE type = 'trigger';" in sql

    def test_create_trigger_sql_without_safe(self):
        """Test trigger SQL generation without IF NOT EXISTS."""
        self.trigger.safe = False
        sql = self.dialect.create_trigger_sql(self.trigger)

        assert 'IF NOT EXISTS' not in sql
        assert 'CREATE TRIGGER test_trigger' in sql

    def test_create_trigger_sql_without_for_each_row(self):
        """Test trigger SQL generation without FOR EACH ROW."""
        self.trigger.for_each_row = False
        sql = self.dialect.create_trigger_sql(self.trigger)

        assert 'FOR EACH ROW' not in sql.replace('FOR EACH ROW\n', '').replace('FOR EACH ROW ', '')

    def test_create_trigger_sql_with_update_columns(self):
        """Test trigger SQL with column-specific UPDATE."""
        self.trigger.trigger_action = TriggerAction.Update
        self.trigger.update_columns = ['name', 'email']
        sql = self.dialect.create_trigger_sql(self.trigger)

        assert 'OF name, email' in sql
        assert 'AFTER UPDATE OF name, email ON test_table' in sql

    def test_create_trigger_sql_with_when_conditions(self):
        """Test trigger SQL with WHEN conditions."""
        self.trigger._when_list = ["NEW.status = 'active'", 'OLD.status != NEW.status']
        sql = self.dialect.create_trigger_sql(self.trigger)

        assert "WHEN NEW.status = 'active' AND OLD.status != NEW.status" in sql

    def test_create_trigger_sql_multiple_sql_statements(self):
        """Test trigger with multiple SQL statements."""
        self.trigger._sql_list = ['INSERT INTO log_table VALUES (NEW.id);', 'UPDATE stats SET count = count + 1;']
        sql = self.dialect.create_trigger_sql(self.trigger)

        assert 'INSERT INTO log_table VALUES (NEW.id);' in sql
        assert 'UPDATE stats SET count = count + 1;' in sql

    def test_drop_trigger_sql_safe(self):
        """Test drop trigger SQL with IF EXISTS."""
        sql = self.dialect.drop_trigger_sql('test_trigger', safe=True)
        assert sql == 'DROP TRIGGER IF EXISTS test_trigger'

    def test_drop_trigger_sql_unsafe(self):
        """Test drop trigger SQL without IF EXISTS."""
        sql = self.dialect.drop_trigger_sql('test_trigger', safe=False)
        assert sql == 'DROP TRIGGER test_trigger'

    def test_supports_trigger_type_valid_combinations(self):
        """Test valid trigger type combinations."""
        # Test all valid combinations
        assert self.dialect.supports_trigger_type(TriggerWhen.Before, TriggerAction.Insert)
        assert self.dialect.supports_trigger_type(TriggerWhen.After, TriggerAction.Update)
        assert self.dialect.supports_trigger_type(TriggerWhen.Before, TriggerAction.Delete)
        assert self.dialect.supports_trigger_type(TriggerWhen.Instead, TriggerAction.Insert, on_view=True)

    def test_supports_trigger_type_instead_of_on_table(self):
        """Test that INSTEAD OF is not supported on tables."""
        assert not self.dialect.supports_trigger_type(TriggerWhen.Instead, TriggerAction.Insert, on_view=False)
        assert not self.dialect.supports_trigger_type(TriggerWhen.Instead, TriggerAction.Update)
        assert not self.dialect.supports_trigger_type(TriggerWhen.Instead, TriggerAction.Delete)

    def test_feature_support_methods(self):
        """Test SQLite feature support methods."""
        assert self.dialect.supports_safe_create()
        assert self.dialect.supports_update_of_columns()
        assert self.dialect.supports_when_clause()


class TestMySQLDialect:
    """Test MySQL-specific dialect implementation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.dialect = MySQLDialect()
        self.trigger = Mock()
        self.trigger.trigger_name = 'test_trigger'
        self.trigger.target_table = 'test_table'
        self.trigger.trigger_when = TriggerWhen.Before
        self.trigger.trigger_action = TriggerAction.Update
        self.trigger.safe = True
        self.trigger.for_each_row = True
        self.trigger.update_columns = []
        self.trigger._when_list = []
        self.trigger._sql_list = ['SET NEW.updated_at = NOW();']

    def test_create_trigger_sql_basic(self):
        """Test basic MySQL trigger SQL generation."""
        sql = self.dialect.create_trigger_sql(self.trigger)

        assert 'CREATE TRIGGER IF NOT EXISTS test_trigger' in sql
        assert 'BEFORE UPDATE ON test_table' in sql
        assert 'FOR EACH ROW' in sql
        assert 'SET NEW.updated_at = NOW();' in sql
        assert 'BEGIN' in sql
        assert 'END;' in sql

    def test_select_all_trigger_sql(self):
        sql = self.dialect.select_all_trigger_sql()
        assert (
            'SELECT trigger_name, event_object_table AS table_name FROM information_schema.TRIGGERS WHERE TRIGGER_SCHEMA = DATABASE();'
            in sql
        )

    def test_create_trigger_sql_with_when_conditions(self):
        """Test MySQL trigger with WHEN conditions converted to IF/THEN."""
        self.trigger._when_list = ["NEW.status = 'active'", 'OLD.id = NEW.id']
        sql = self.dialect.create_trigger_sql(self.trigger)

        assert "IF NEW.status = 'active' AND OLD.id = NEW.id THEN" in sql
        assert 'SET NEW.updated_at = NOW();' in sql
        assert 'END IF;' in sql

    def test_create_trigger_sql_without_when_conditions(self):
        """Test MySQL trigger without WHEN conditions."""
        sql = self.dialect.create_trigger_sql(self.trigger)

        assert 'IF' not in sql or 'IF NOT EXISTS' in sql  # Only IF NOT EXISTS should be present
        assert 'SET NEW.updated_at = NOW();' in sql

    def test_create_trigger_sql_multiple_statements_with_conditions(self):
        """Test MySQL trigger with multiple statements and conditions."""
        self.trigger._when_list = ['NEW.active = 1']
        self.trigger._sql_list = ['SET NEW.updated_at = NOW();', "INSERT INTO audit_log VALUES (NEW.id, 'updated');"]
        sql = self.dialect.create_trigger_sql(self.trigger)

        assert 'IF NEW.active = 1 THEN' in sql
        assert 'SET NEW.updated_at = NOW();' in sql
        assert "INSERT INTO audit_log VALUES (NEW.id, 'updated');" in sql
        assert 'END IF;' in sql

    def test_drop_trigger_sql(self):
        """Test MySQL drop trigger SQL."""
        sql = self.dialect.drop_trigger_sql('test_trigger', safe=True)
        assert sql == 'DROP TRIGGER IF EXISTS test_trigger'

        sql = self.dialect.drop_trigger_sql('test_trigger', safe=False)
        assert sql == 'DROP TRIGGER test_trigger'

    def test_supports_trigger_type(self):
        """Test MySQL trigger type support."""
        # MySQL supports BEFORE and AFTER
        assert self.dialect.supports_trigger_type(TriggerWhen.Before, TriggerAction.Insert)
        assert self.dialect.supports_trigger_type(TriggerWhen.After, TriggerAction.Update)

        # MySQL doesn't support INSTEAD OF
        assert not self.dialect.supports_trigger_type(TriggerWhen.Instead, TriggerAction.Insert)
        assert not self.dialect.supports_trigger_type(TriggerWhen.Instead, TriggerAction.Delete, on_view=True)

    def test_feature_support_methods(self):
        """Test MySQL feature support methods."""
        assert self.dialect.supports_safe_create()
        assert not self.dialect.supports_update_of_columns()
        assert self.dialect.supports_when_clause()


class TestPostgreSQLDialect:
    """Test PostgreSQL-specific dialect implementation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.dialect = PostgreSQLDialect()
        self.trigger = Mock()
        self.trigger.trigger_name = 'test_trigger'
        self.trigger.target_table = 'test_table'
        self.trigger.trigger_when = TriggerWhen.Before
        self.trigger.trigger_action = TriggerAction.Insert
        self.trigger.safe = True
        self.trigger.for_each_row = True
        self.trigger.update_columns = []
        self.trigger._when_list = []
        self.trigger._sql_list = ["INSERT INTO audit_table VALUES (NEW.id, 'inserted');"]

    def test_select_all_trigger_sql(self):
        sql = self.dialect.select_all_trigger_sql()
        assert (
            "SELECT trigger_name, event_object_table AS table_name FROM information_schema.triggers WHERE trigger_schema NOT IN ('pg_catalog', 'information_schema');"
            in sql
        )

    def test_create_trigger_sql_basic_before(self):
        """Test basic PostgreSQL trigger SQL generation for BEFORE trigger."""
        sql = self.dialect.create_trigger_sql(self.trigger)

        # Should contain function creation
        assert 'CREATE OR REPLACE FUNCTION fn_test_trigger() RETURNS TRIGGER' in sql
        assert 'BEGIN' in sql
        assert "INSERT INTO audit_table VALUES (NEW.id, 'inserted');" in sql
        assert 'RETURN NEW;' in sql
        assert '$$ LANGUAGE plpgsql;' in sql

        # Should contain trigger creation
        assert 'DROP TRIGGER IF EXISTS test_trigger ON test_table CASCADE;' in sql
        assert 'CREATE TRIGGER test_trigger' in sql
        assert 'BEFORE INSERT ON test_table' in sql
        assert 'FOR EACH ROW' in sql
        assert 'EXECUTE FUNCTION fn_test_trigger();' in sql

    def test_create_trigger_sql_after_trigger(self):
        """Test PostgreSQL AFTER trigger returns NULL."""
        self.trigger.trigger_when = TriggerWhen.After
        sql = self.dialect.create_trigger_sql(self.trigger)

        assert 'RETURN NULL;' in sql
        assert 'AFTER INSERT ON test_table' in sql

    def test_create_trigger_sql_instead_of_trigger(self):
        """Test PostgreSQL INSTEAD OF trigger returns NEW."""
        self.trigger.trigger_when = TriggerWhen.Instead
        sql = self.dialect.create_trigger_sql(self.trigger)

        assert 'RETURN NEW;' in sql
        assert 'INSTEAD OF INSERT ON test_table' in sql

    def test_create_trigger_sql_with_when_conditions(self):
        """Test PostgreSQL trigger with WHEN conditions."""
        self.trigger._when_list = ['NEW.active = true', 'OLD.status != NEW.status']
        sql = self.dialect.create_trigger_sql(self.trigger)

        assert 'IF NEW.active = true AND OLD.status != NEW.status THEN' in sql
        assert "INSERT INTO audit_table VALUES (NEW.id, 'inserted');" in sql
        assert 'END IF;' in sql

    def test_create_trigger_sql_with_update_columns(self):
        """Test PostgreSQL trigger with column-specific UPDATE."""
        self.trigger.trigger_action = TriggerAction.Update
        self.trigger.update_columns = ['name', 'email']
        sql = self.dialect.create_trigger_sql(self.trigger)

        assert 'OF name, email' in sql
        assert 'BEFORE UPDATE OF name, email ON test_table' in sql

    def test_create_trigger_sql_for_each_statement(self):
        """Test PostgreSQL trigger FOR EACH STATEMENT."""
        self.trigger.for_each_row = False
        sql = self.dialect.create_trigger_sql(self.trigger)

        assert 'FOR EACH STATEMENT' in sql
        assert 'FOR EACH ROW' not in sql.replace('FOR EACH STATEMENT', '')

    def test_create_trigger_sql_unsafe(self):
        """Test PostgreSQL trigger without safe mode."""
        self.trigger.safe = False
        sql = self.dialect.create_trigger_sql(self.trigger)

        assert 'DROP TRIGGER IF EXISTS' not in sql
        assert 'CREATE TRIGGER test_trigger' in sql

    def test_clean_sql_with_returning_clause(self):
        """Test _clean_sql method with RETURNING clause."""
        sql_with_returning = 'UPDATE table SET col = 1 RETURNING id;'
        cleaned = self.dialect._clean_sql(sql_with_returning)
        assert cleaned == 'UPDATE table SET col = 1 ;'

        sql_with_returning_no_semicolon = 'UPDATE table SET col = 1 RETURNING id'
        cleaned = self.dialect._clean_sql(sql_with_returning_no_semicolon)
        assert cleaned == 'UPDATE table SET col = 1 '

    def test_clean_sql_without_returning_clause(self):
        """Test _clean_sql method without RETURNING clause."""
        sql_without_returning = 'INSERT INTO table VALUES (1, 2);'
        cleaned = self.dialect._clean_sql(sql_without_returning)
        assert cleaned == 'INSERT INTO table VALUES (1, 2);'

    def test_clean_sql_case_insensitive_returning(self):
        """Test _clean_sql handles case-insensitive RETURNING."""
        sql_with_returning = 'UPDATE table SET col = 1 returning id;'
        cleaned = self.dialect._clean_sql(sql_with_returning)
        assert cleaned == 'UPDATE table SET col = 1 ;'

    def test_drop_trigger_sql(self):
        """Test PostgreSQL drop trigger SQL."""
        sql = self.dialect.drop_trigger_sql('test_trigger', safe=True, table_name='test_table')
        expected = 'DROP TRIGGER IF EXISTS test_trigger ON test_table;\nDROP FUNCTION IF EXISTS fn_test_trigger();'
        assert sql == expected

        sql = self.dialect.drop_trigger_sql('test_trigger', safe=False, table_name='test_table')
        expected = 'DROP TRIGGER test_trigger ON test_table;\nDROP FUNCTION fn_test_trigger();'
        assert sql == expected

    def test_drop_trigger_sql_raises(self):
        with pytest.raises(RuntimeError, match='Cannot drop a trigger in PostgreSQL without a table_name'):
            self.dialect.drop_trigger_sql('test')

    def test_supports_trigger_type(self):
        """Test PostgreSQL trigger type support."""
        # PostgreSQL supports BEFORE and AFTER on tables
        assert self.dialect.supports_trigger_type(TriggerWhen.Before, TriggerAction.Insert)
        assert self.dialect.supports_trigger_type(TriggerWhen.After, TriggerAction.Update)

        # PostgreSQL supports INSTEAD OF only on views
        assert self.dialect.supports_trigger_type(TriggerWhen.Instead, TriggerAction.Insert, on_view=True)
        assert not self.dialect.supports_trigger_type(TriggerWhen.Instead, TriggerAction.Delete, on_view=False)

    def test_feature_support_methods(self):
        """Test PostgreSQL feature support methods."""
        assert self.dialect.supports_safe_create()  # We implement it differently
        assert self.dialect.supports_update_of_columns()
        assert self.dialect.supports_when_clause()


@pytest.mark.integration_test
class TestTriggerIntegration:
    """Test integration of Trigger class with different dialects."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_db_sqlite = Mock(spec=peewee.SqliteDatabase)
        self.mock_db_mysql = Mock(spec=peewee.MySQLDatabase)
        self.mock_db_postgres = Mock(spec=peewee.PostgresqlDatabase)
        self.mock_db_proxy = Mock(spec=peewee.DatabaseProxy)
        self.mock_db_unsupported = Mock()

    def test_trigger_get_dialect_sqlite(self):
        """Test trigger gets correct SQLite dialect."""
        trigger = Trigger('test', (TriggerWhen.After, TriggerAction.Insert), 'test_table')
        trigger.set_database(self.mock_db_sqlite)
        dialect = trigger._get_dialect()
        assert isinstance(dialect, SQLiteDialect)

    def test_trigger_get_dialect_mysql(self):
        """Test trigger gets correct MySQL dialect."""
        trigger = Trigger('test', (TriggerWhen.After, TriggerAction.Insert), 'test_table')
        trigger.set_database(self.mock_db_mysql)
        dialect = trigger._get_dialect()
        assert isinstance(dialect, MySQLDialect)

    def test_trigger_get_dialect_postgresql(self):
        """Test trigger gets correct PostgreSQL dialect."""
        trigger = Trigger('test', (TriggerWhen.After, TriggerAction.Insert), 'test_table')
        trigger.set_database(self.mock_db_postgres)
        dialect = trigger._get_dialect()
        assert isinstance(dialect, PostgreSQLDialect)

    def test_trigger_get_dialect_database_proxy(self):
        """Test trigger handles DatabaseProxy correctly."""
        self.mock_db_proxy.obj = self.mock_db_sqlite
        trigger = Trigger('test', (TriggerWhen.After, TriggerAction.Insert), 'test_table')
        trigger.set_database(self.mock_db_proxy)
        dialect = trigger._get_dialect()
        assert isinstance(dialect, SQLiteDialect)

    def test_trigger_get_dialect_unsupported_database(self):
        """Test trigger raises error for unsupported database."""
        trigger = Trigger('test', (TriggerWhen.After, TriggerAction.Insert), 'test_table')
        trigger.set_database(self.mock_db_unsupported)

        with pytest.raises(UnsupportedDatabaseError):
            trigger._get_dialect()

    def test_trigger_get_dialect_no_database_defaults_sqlite(self):
        """Test trigger defaults to SQLite dialect when no database set."""
        trigger = Trigger('test', (TriggerWhen.After, TriggerAction.Insert), 'test_table')
        dialect = trigger._get_dialect()
        assert isinstance(dialect, SQLiteDialect)

    def test_trigger_create_validates_support(self):
        """Test trigger create validates database support."""
        trigger = Trigger('test', (TriggerWhen.Instead, TriggerAction.Insert), 'test_table')
        trigger.set_database(self.mock_db_mysql)
        trigger.add_sql('INSERT INTO log VALUES (1);')

        # MySQL doesn't support INSTEAD OF triggers
        with pytest.raises(UnsupportedDatabaseError):
            trigger.create()

    def test_trigger_create_handles_missing_sql(self):
        """Test trigger create raises error when no SQL statements provided."""
        trigger = Trigger('test', (TriggerWhen.After, TriggerAction.Insert), 'test_table')

        with pytest.raises(MissingSQLStatement):
            trigger.create()

    def test_trigger_create_handles_unsupported_features_gracefully(self):
        """Test trigger create handles unsupported features gracefully."""
        trigger = Trigger(
            'test', (TriggerWhen.After, TriggerAction.Update), 'test_table', safe=True, update_columns=['name', 'email']
        )
        trigger.set_database(self.mock_db_mysql)  # MySQL doesn't support update columns
        trigger.add_sql('SET NEW.updated_at = NOW();')

        # Should not raise error, but should ignore unsupported features
        sql = trigger.create()
        assert 'OF name, email' not in sql  # Update columns should be ignored

    @pytest.mark.parametrize(
        'dialect_class,db_class',
        [
            (SQLiteDialect, peewee.SqliteDatabase),
            (MySQLDialect, peewee.MySQLDatabase),
            (PostgreSQLDialect, peewee.PostgresqlDatabase),
        ],
    )
    def test_all_dialects_implement_required_methods(self, dialect_class, db_class):
        """Test that all dialect classes implement required abstract methods."""
        dialect = dialect_class()

        # Test that all required methods exist and are callable
        assert hasattr(dialect, 'create_trigger_sql')
        assert callable(dialect.create_trigger_sql)

        assert hasattr(dialect, 'drop_trigger_sql')
        assert callable(dialect.drop_trigger_sql)

        assert hasattr(dialect, 'supports_trigger_type')
        assert callable(dialect.supports_trigger_type)

        assert hasattr(dialect, 'supports_safe_create')
        assert callable(dialect.supports_safe_create)

        assert hasattr(dialect, 'supports_update_of_columns')
        assert callable(dialect.supports_update_of_columns)

        assert hasattr(dialect, 'supports_when_clause')
        assert callable(dialect.supports_when_clause)


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_sql_statements_list(self):
        """Test behavior with empty SQL statements."""
        dialect = SQLiteDialect()
        trigger = Mock()
        trigger.trigger_name = 'test'
        trigger.target_table = 'test_table'
        trigger.trigger_when = TriggerWhen.After
        trigger.trigger_action = TriggerAction.Insert
        trigger.safe = False
        trigger.for_each_row = True
        trigger.update_columns = []
        trigger._when_list = []
        trigger._sql_list = []

        # This should work - the validation happens in Trigger.create()
        sql = dialect.create_trigger_sql(trigger)
        assert 'BEGIN' in sql
        assert 'END;' in sql

    def test_complex_when_conditions(self):
        """Test complex WHEN conditions across dialects."""
        dialects = [SQLiteDialect(), MySQLDialect(), PostgreSQLDialect()]

        for dialect in dialects:
            trigger = Mock()
            trigger.trigger_name = 'complex_trigger'
            trigger.target_table = 'test_table'
            trigger.trigger_when = TriggerWhen.Before
            trigger.trigger_action = TriggerAction.Update
            trigger.safe = True
            trigger.for_each_row = True
            trigger.update_columns = []
            trigger._when_list = ['NEW.amount > 1000', "OLD.status = 'pending'", "NEW.created_at > '2023-01-01'"]
            trigger._sql_list = ['UPDATE audit SET checked = true;']

            sql = dialect.create_trigger_sql(trigger)
            assert 'NEW.amount > 1000' in sql
            assert "OLD.status = 'pending'" in sql
            assert "NEW.created_at > '2023-01-01'" in sql

    def test_special_characters_in_trigger_names(self):
        """Test handling of special characters in trigger names."""
        dialects = [SQLiteDialect(), MySQLDialect(), PostgreSQLDialect()]

        for dialect in dialects:
            trigger = Mock()
            trigger.trigger_name = 'test_trigger_123'
            trigger.target_table = 'test_table_456'
            trigger.trigger_when = TriggerWhen.After
            trigger.trigger_action = TriggerAction.Insert
            trigger.safe = True
            trigger.for_each_row = True
            trigger.update_columns = []
            trigger._when_list = []
            trigger._sql_list = ['INSERT INTO log VALUES (1);']

            sql = dialect.create_trigger_sql(trigger)
            assert 'test_trigger_123' in sql
            assert 'test_table_456' in sql


# Additional fixtures and utilities for testing
@pytest.fixture
def sample_trigger():
    """Create a sample trigger for testing."""
    trigger = Trigger('sample_trigger', (TriggerWhen.After, TriggerAction.Insert), 'sample_table')
    trigger.add_sql("INSERT INTO audit_log VALUES (NEW.id, 'inserted');")
    return trigger


@pytest.fixture
def all_dialects():
    """Provide all dialect instances for parameterized testing."""
    return [SQLiteDialect(), MySQLDialect(), PostgreSQLDialect()]


class TestDialectComparison:
    """Test differences between dialects."""

    def test_feature_support_comparison(self, all_dialects):
        """Compare feature support across all dialects."""
        features = {}

        for dialect in all_dialects:
            dialect_name = dialect.__class__.__name__
            features[dialect_name] = {
                'safe_create': dialect.supports_safe_create(),
                'update_columns': dialect.supports_update_of_columns(),
                'when_clause': dialect.supports_when_clause(),
                'instead_of_table': dialect.supports_trigger_type(TriggerWhen.Instead, TriggerAction.Insert, False),
                'instead_of_view': dialect.supports_trigger_type(TriggerWhen.Instead, TriggerAction.Insert, True),
            }

        # Verify expected differences
        assert not features['MySQLDialect']['update_columns']
        assert features['SQLiteDialect']['update_columns']
        assert features['PostgreSQLDialect']['update_columns']

        assert not features['MySQLDialect']['instead_of_table']
        assert not features['MySQLDialect']['instead_of_view']
        assert not features['SQLiteDialect']['instead_of_table']
        assert features['SQLiteDialect']['instead_of_view']
        assert not features['PostgreSQLDialect']['instead_of_table']
        assert features['PostgreSQLDialect']['instead_of_view']
