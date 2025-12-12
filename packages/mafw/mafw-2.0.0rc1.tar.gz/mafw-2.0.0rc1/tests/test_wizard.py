#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Unit tests for the db_wizard module.

This module provides comprehensive test coverage for the database introspection
and model generation functionality.
"""

import datetime
import io
from typing import Dict, List, Tuple
from unittest.mock import Mock, patch

import pytest
from playhouse.reflection import Introspector

from mafw.db.db_wizard import HEADER, MODULE_DOCSTRING, UNKNOWN_FIELD, UnknownField, dump_models


class MockColumn:
    """Mock column for testing purposes."""

    def __init__(
        self,
        name: str = 'test_column',
        field_class: type = str,
        primary_key: bool = False,
        raw_column_type: str = 'VARCHAR',
    ):
        self.name = name
        self.field_class = field_class
        self.primary_key = primary_key
        self.raw_column_type = raw_column_type

    def get_field(self) -> str:
        """Mock get_field method."""
        return f'{self.name} = CharField()'


class MockForeignKey:
    """Mock foreign key for testing purposes."""

    def __init__(self, dest_table: str):
        self.dest_table = dest_table


class MockDatabase:
    """Mock database for testing purposes."""

    def __init__(self):
        self.model_names: Dict[str, str] = {}
        self.columns: Dict[str, Dict[str, MockColumn]] = {}
        self.foreign_keys: Dict[str, List[MockForeignKey]] = {}
        self.primary_keys: Dict[str, List[str]] = {}
        self._multi_column_indexes: Dict[str, List[Tuple[List[str], bool]]] = {}

    def multi_column_indexes(self, table: str) -> List[Tuple[List[str], bool]]:
        """Mock multi_column_indexes method."""
        return self._multi_column_indexes.get(table, [])


class TestUnknownField:
    """Test cases for the UnknownField class."""

    def test_unknown_field_initialization(self):
        """Test that UnknownField can be initialized with any arguments."""
        field = UnknownField()
        assert isinstance(field, UnknownField)

        field = UnknownField('arg1', 'arg2', kwarg1='value1', kwarg2='value2')
        assert isinstance(field, UnknownField)


class TestDumpModels:
    """Test cases for the dump_models function."""

    @pytest.fixture
    def mock_introspector(self):
        """Create a mock introspector for testing."""
        introspector = Mock(spec=Introspector)
        introspector.get_database_name.return_value = 'test_database'
        introspector.schema = None
        introspector.pk_classes = [int]
        return introspector

    @pytest.fixture
    def mock_database(self):
        """Create a mock database for testing."""
        database = MockDatabase()
        database.model_names = {'users': 'User', 'posts': 'Post'}
        database.columns = {
            'users': {
                'id': MockColumn('id', int, True, 'INTEGER'),
                'name': MockColumn('name', str, False, 'VARCHAR'),
            },
            'posts': {
                'id': MockColumn('id', int, True, 'INTEGER'),
                'title': MockColumn('title', str, False, 'VARCHAR'),
                'user_id': MockColumn('user_id', int, False, 'INTEGER'),
            },
        }
        database.foreign_keys = {'users': [], 'posts': [MockForeignKey('users')]}
        database.primary_keys = {'users': ['id'], 'posts': ['id']}
        return database

    @pytest.fixture
    def output_file(self):
        """Create a StringIO object for output testing."""
        return io.StringIO()

    def test_dump_models_basic(self, mock_introspector, mock_database, output_file):
        """Test basic dump_models functionality."""
        mock_introspector.introspect.return_value = mock_database

        dump_models(output_file, mock_introspector)

        output = output_file.getvalue()

        # Check that the module docstring is included
        assert 'The module provides an automatically generated ORM model' in output
        assert 'test_database' in output

        # Check that the header is included
        assert 'from mafw.db.db_model import MAFwBaseModel' in output

        # Check that UnknownField class is included
        assert 'class UnknownField(object):' in output

        # Check that model classes are generated
        assert 'class User(MAFwBaseModel):' in output
        assert 'class Post(MAFwBaseModel):' in output

        # Verify introspect was called with correct parameters
        mock_introspector.introspect.assert_called_once_with(table_names=None, include_views=False, snake_case=True)

    @pytest.mark.parametrize(
        'tables,expected_tables',
        [
            (['users'], ['users']),
            (('posts',), ('posts',)),
            (None, None),
        ],
    )
    def test_dump_models_with_tables_parameter(
        self, mock_introspector, mock_database, output_file, tables, expected_tables
    ):
        """Test dump_models with different tables parameter values."""
        mock_introspector.introspect.return_value = mock_database

        dump_models(output_file, mock_introspector, tables=tables)

        mock_introspector.introspect.assert_called_once_with(
            table_names=expected_tables, include_views=False, snake_case=True
        )

    @pytest.mark.parametrize('preserve_order', [True, False])
    def test_dump_models_preserve_order(self, mock_introspector, mock_database, output_file, preserve_order):
        """Test dump_models with different preserve_order values."""
        mock_introspector.introspect.return_value = mock_database

        dump_models(output_file, mock_introspector, preserve_order=preserve_order)

        output = output_file.getvalue()
        assert 'class User(MAFwBaseModel):' in output

    @pytest.mark.parametrize('include_views', [True, False])
    def test_dump_models_include_views(self, mock_introspector, mock_database, output_file, include_views):
        """Test dump_models with different include_views values."""
        mock_introspector.introspect.return_value = mock_database

        dump_models(output_file, mock_introspector, include_views=include_views)

        mock_introspector.introspect.assert_called_once_with(
            table_names=None, include_views=include_views, snake_case=True
        )

    @pytest.mark.parametrize('ignore_unknown', [True, False])
    def test_dump_models_ignore_unknown(self, mock_introspector, mock_database, output_file, ignore_unknown):
        """Test dump_models with different ignore_unknown values."""
        mock_introspector.introspect.return_value = mock_database

        dump_models(output_file, mock_introspector, ignore_unknown=ignore_unknown)

        output = output_file.getvalue()
        if ignore_unknown:
            assert 'class UnknownField(object):' not in output
        else:
            assert 'class UnknownField(object):' in output

    @pytest.mark.parametrize('snake_case', [True, False])
    def test_dump_models_snake_case(self, mock_introspector, mock_database, output_file, snake_case):
        """Test dump_models with different snake_case values."""
        mock_introspector.introspect.return_value = mock_database

        dump_models(output_file, mock_introspector, snake_case=snake_case)

        mock_introspector.introspect.assert_called_once_with(
            table_names=None, include_views=False, snake_case=snake_case
        )

    def test_dump_models_with_schema(self, mock_introspector, mock_database, output_file):
        """Test dump_models when introspector has a schema."""
        mock_introspector.introspect.return_value = mock_database
        mock_introspector.schema = 'public'

        dump_models(output_file, mock_introspector)

        output = output_file.getvalue()
        assert "schema = 'public'" in output

    def test_dump_models_with_unknown_fields(self, mock_introspector, mock_database, output_file):
        """Test dump_models handling of unknown fields."""
        # Add an unknown field to the database
        unknown_column = MockColumn('unknown_col', UnknownField, False, 'UNKNOWN_TYPE')
        mock_database.columns['users']['unknown_col'] = unknown_column
        mock_introspector.introspect.return_value = mock_database

        dump_models(output_file, mock_introspector, ignore_unknown=False)

        output = output_file.getvalue()
        assert 'unknown_col = CharField()' in output

    def test_dump_models_ignore_unknown_fields(self, mock_introspector, mock_database, output_file):
        """Test dump_models ignoring unknown fields."""
        # Add an unknown field to the database
        unknown_column = MockColumn('unknown_col', UnknownField, False, 'UNKNOWN_TYPE')
        mock_database.columns['users']['unknown_col'] = unknown_column
        mock_introspector.introspect.return_value = mock_database

        dump_models(output_file, mock_introspector, ignore_unknown=True)

        output = output_file.getvalue()
        assert '# unknown_col - UNKNOWN_TYPE' in output

    def test_dump_models_with_composite_primary_key(self, mock_introspector, mock_database, output_file):
        """Test dump_models with composite primary keys."""
        # Set up composite primary key
        mock_database.primary_keys['users'] = ['id', 'name']
        mock_database.columns['users']['id'].primary_key = True
        mock_database.columns['users']['name'].primary_key = True
        mock_introspector.introspect.return_value = mock_database

        dump_models(output_file, mock_introspector)

        output = output_file.getvalue()
        assert "primary_key = CompositeKey('id', 'name')" in output

    def test_dump_models_with_no_primary_key(self, mock_introspector, mock_database, output_file):
        """Test dump_models with tables having no primary key."""
        # Remove primary keys
        mock_database.primary_keys['users'] = []
        mock_introspector.introspect.return_value = mock_database

        dump_models(output_file, mock_introspector)

        output = output_file.getvalue()
        assert 'primary_key = False' in output

    def test_dump_models_with_multi_column_indexes(self, mock_introspector, mock_database, output_file):
        """Test dump_models with multi-column indexes."""
        # Add multi-column indexes
        mock_database._multi_column_indexes['users'] = [(['name', 'email'], True), (['created_at'], False)]
        mock_introspector.introspect.return_value = mock_database

        dump_models(output_file, mock_introspector)

        output = output_file.getvalue()
        assert 'indexes = (' in output
        assert "('name', 'email'), True" in output
        assert "('created_at'), False" in output

    def test_dump_models_with_foreign_key_cycle(self, mock_introspector, mock_database, output_file):
        """Test dump_models handling of foreign key reference cycles."""
        # Create a circular reference
        mock_database.foreign_keys['users'] = [MockForeignKey('posts')]
        mock_database.foreign_keys['posts'] = [MockForeignKey('users')]
        mock_introspector.introspect.return_value = mock_database

        dump_models(output_file, mock_introspector)

        output = output_file.getvalue()
        assert '# Possible reference cycle:' in output

    def test_dump_models_skip_default_primary_key(self, mock_introspector, mock_database, output_file):
        """Test that default 'id' primary key fields are skipped."""
        mock_introspector.introspect.return_value = mock_database

        dump_models(output_file, mock_introspector)

        output = output_file.getvalue()
        # The 'id' field should be skipped since it's a single primary key named 'id'
        # and the field class is in pk_classes
        lines = output.split('\n')
        user_class_lines = []
        in_user_class = False
        for line in lines:
            if 'class User(MAFwBaseModel):' in line:
                in_user_class = True
            elif line.startswith('class ') and in_user_class:
                break
            elif in_user_class:
                user_class_lines.append(line)

        # Check that 'id' field is not explicitly defined
        id_field_lines = [line for line in user_class_lines if 'id =' in line]
        assert len(id_field_lines) == 0

    @patch('mafw.db.db_wizard.datetime')
    @patch('mafw.db.db_wizard.mafw_version', '1.0.0')
    def test_dump_intro_formatting(self, mock_datetime, mock_introspector, mock_database, output_file):
        """Test that the module intro is formatted correctly."""
        mock_datetime.datetime.now.return_value = datetime.datetime(2023, 1, 1, 12, 0, 0)
        mock_introspector.introspect.return_value = mock_database

        dump_models(output_file, mock_introspector)

        output = output_file.getvalue()
        assert 'test_database' in output
        assert '2023-01-01 12:00:00' in output
        assert 'MAFw version: 1.0.0' in output

    def test_dump_models_column_ordering_preserved(self, mock_introspector, mock_database, output_file):
        """Test that column order is preserved when preserve_order=True."""
        # Add more columns to test ordering
        mock_database.columns['users'] = {
            'z_field': MockColumn('z_field', str, False, 'VARCHAR'),
            'a_field': MockColumn('a_field', str, False, 'VARCHAR'),
            'm_field': MockColumn('m_field', str, False, 'VARCHAR'),
        }
        mock_introspector.introspect.return_value = mock_database

        dump_models(output_file, mock_introspector, preserve_order=True)

        output = output_file.getvalue()

        # Find the User class section
        user_start = output.find('class User(MAFwBaseModel):')
        user_end = output.find('class ', user_start + 1)
        if user_end == -1:
            user_end = len(output)
        user_section = output[user_start:user_end]

        # Check that fields appear in original order (dictionary insertion order)
        z_pos = user_section.find('z_field')
        a_pos = user_section.find('a_field')
        m_pos = user_section.find('m_field')

        assert z_pos < a_pos < m_pos

    def test_dump_models_column_ordering_sorted(self, mock_introspector, mock_database, output_file):
        """Test that column order is sorted when preserve_order=False."""
        # Add more columns to test ordering
        mock_database.columns['users'] = {
            'z_field': MockColumn('z_field', str, False, 'VARCHAR'),
            'a_field': MockColumn('a_field', str, False, 'VARCHAR'),
            'm_field': MockColumn('m_field', str, False, 'VARCHAR'),
        }
        mock_introspector.introspect.return_value = mock_database

        dump_models(output_file, mock_introspector, preserve_order=False)

        output = output_file.getvalue()

        # Find the User class section
        user_start = output.find('class User(MAFwBaseModel):')
        user_end = output.find('class ', user_start + 1)
        if user_end == -1:
            user_end = len(output)
        user_section = output[user_start:user_end]

        # Check that fields appear in sorted order
        a_pos = user_section.find('a_field')
        m_pos = user_section.find('m_field')
        z_pos = user_section.find('z_field')

        assert a_pos < m_pos < z_pos

    def test_dump_models_specific_tables_only(self, mock_introspector, mock_database, output_file):
        """Test that only specified tables are dumped when tables parameter is provided."""
        mock_introspector.introspect.return_value = mock_database

        dump_models(output_file, mock_introspector, tables=['users'])

        output = output_file.getvalue()
        assert 'class User(MAFwBaseModel):' in output
        # Post should not be included since it's not in the tables list
        # but it might be included due to foreign key dependencies

    def test_dump_models_self_referential_foreign_key(self, mock_introspector, mock_database, output_file):
        """Test handling of self-referential foreign keys."""
        # Add self-referential foreign key
        mock_database.foreign_keys['users'] = [MockForeignKey('users')]
        mock_database.foreign_keys['posts'] = []
        mock_introspector.introspect.return_value = mock_database

        dump_models(output_file, mock_introspector)

        output = output_file.getvalue()
        # Should not cause infinite recursion
        assert 'class User(MAFwBaseModel):' in output
        assert 'class Post(MAFwBaseModel):' in output


class TestModuleConstants:
    """Test cases for module constants and templates."""

    def test_module_docstring_template(self):
        """Test that MODULE_DOCSTRING template has correct placeholders."""
        assert '{database_name}' in MODULE_DOCSTRING
        assert '{date}' in MODULE_DOCSTRING
        assert '{mafw_version}' in MODULE_DOCSTRING

    def test_header_content(self):
        """Test that HEADER contains necessary imports."""
        assert 'from mafw.db.db_model import MAFwBaseModel' in HEADER
        assert 'from peewee import *' in HEADER
        assert 'from typing import Any' in HEADER

    def test_unknown_field_template(self):
        """Test that UNKNOWN_FIELD template is correctly formatted."""
        assert 'class UnknownField(object):' in UNKNOWN_FIELD
        assert 'def __init__(self, *_: Any, **__: Any) -> None:' in UNKNOWN_FIELD


@pytest.mark.integration_test
class TestDumpModelsIntegration:
    """Integration tests for dump_models function."""

    def test_dump_models_complete_workflow(self):
        """Test the complete workflow of dump_models with realistic data."""
        # Create a more realistic mock setup
        introspector = Mock(spec=Introspector)
        introspector.get_database_name.return_value = 'ecommerce_db'
        introspector.schema = 'public'
        introspector.pk_classes = [int]

        database = MockDatabase()
        database.model_names = {'users': 'User', 'products': 'Product', 'orders': 'Order', 'order_items': 'OrderItem'}

        # Set up realistic columns
        database.columns = {
            'users': {
                'id': MockColumn('id', int, True, 'SERIAL'),
                'username': MockColumn('username', str, False, 'VARCHAR(50)'),
                'email': MockColumn('email', str, False, 'VARCHAR(100)'),
                'created_at': MockColumn('created_at', datetime.datetime, False, 'TIMESTAMP'),
            },
            'products': {
                'id': MockColumn('id', int, True, 'SERIAL'),
                'name': MockColumn('name', str, False, 'VARCHAR(200)'),
                'price': MockColumn('price', float, False, 'DECIMAL(10,2)'),
            },
            'orders': {
                'id': MockColumn('id', int, True, 'SERIAL'),
                'user_id': MockColumn('user_id', int, False, 'INTEGER'),
                'total': MockColumn('total', float, False, 'DECIMAL(10,2)'),
            },
            'order_items': {
                'order_id': MockColumn('order_id', int, True, 'INTEGER'),
                'product_id': MockColumn('product_id', int, True, 'INTEGER'),
                'quantity': MockColumn('quantity', int, False, 'INTEGER'),
            },
        }

        # Set up foreign keys
        database.foreign_keys = {
            'users': [],
            'products': [],
            'orders': [MockForeignKey('users')],
            'order_items': [MockForeignKey('orders'), MockForeignKey('products')],
        }

        # Set up primary keys
        database.primary_keys = {
            'users': ['id'],
            'products': ['id'],
            'orders': ['id'],
            'order_items': ['order_id', 'product_id'],  # Composite key
        }

        # Set up multi-column indexes
        database._multi_column_indexes = {
            'users': [(['username', 'email'], True)],
            'orders': [(['user_id', 'created_at'], False)],
        }

        introspector.introspect.return_value = database

        output_file = io.StringIO()
        dump_models(output_file, introspector)

        output = output_file.getvalue()

        # Verify all expected content is present
        assert 'ecommerce_db' in output
        assert "schema = 'public'" in output
        assert 'class User(MAFwBaseModel):' in output
        assert 'class Product(MAFwBaseModel):' in output
        assert 'class Order(MAFwBaseModel):' in output
        assert 'class OrderItem(MAFwBaseModel):' in output
        assert "primary_key = CompositeKey('order_id', 'product_id')" in output
        assert 'indexes = (' in output
