#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Unit tests for regexp module.
"""

import logging

import pytest

from mafw.mafw_errors import UnknownProcessor
from mafw.tools.regexp import extract_protocol, normalize_sql_spaces, parse_processor_name


class TestExtractProtocol:
    """Test cases for extract_protocol function."""

    def test_extract_protocol_valid_urls(self):
        """Test extracting protocol from valid URLs."""
        # Common database protocols
        assert extract_protocol('postgresql://user:pass@host:5432/db') == 'postgresql'
        assert extract_protocol('mysql://user:pass@host:3306/db') == 'mysql'
        assert extract_protocol('sqlite:///path/to/database.db') == 'sqlite'
        assert extract_protocol('mongodb://user:pass@host:27017/db') == 'mongodb'

        # Web protocols
        assert extract_protocol('http://example.com') == 'http'
        assert extract_protocol('https://example.com') == 'https'
        assert extract_protocol('ftp://example.com') == 'ftp'

        # Protocols with numbers, hyphens, underscores, dots, and plus signs
        assert extract_protocol('redis+sentinel://host:port') == 'redis+sentinel'
        assert extract_protocol('mssql+pyodbc://server/database') == 'mssql+pyodbc'
        assert extract_protocol('oracle+cx_oracle://user:pass@host') == 'oracle+cx_oracle'
        assert extract_protocol('protocol_123://host') == 'protocol_123'
        assert extract_protocol('my-protocol://host') == 'my-protocol'
        assert extract_protocol('protocol.v2://host') == 'protocol.v2'

    def test_extract_protocol_edge_cases(self):
        """Test edge cases for protocol extraction."""
        # Single character protocol
        assert extract_protocol('a://host') == 'a'

        # Protocol with all allowed characters
        assert extract_protocol('abc123-_+.def://host') == 'abc123-_+.def'

        # Minimal valid URL
        assert extract_protocol('x://') == 'x'

    def test_extract_protocol_invalid_urls(self):
        """Test protocol extraction with invalid URLs."""
        # No protocol separator
        assert extract_protocol('postgresql') is None
        assert extract_protocol('example.com') is None

        # Invalid protocol characters
        assert extract_protocol('POSTGRESQL://host') is None  # uppercase
        assert extract_protocol('post@gres://host') is None  # @ symbol
        assert extract_protocol('post gres://host') is None  # space
        assert extract_protocol('post#gres://host') is None  # # symbol

        # Empty or whitespace
        assert extract_protocol('') is None
        assert extract_protocol('   ') is None

        # Only separator
        assert extract_protocol('://') is None
        assert extract_protocol('://host') is None

        # Protocol doesn't start at beginning
        assert extract_protocol('prefix postgresql://host') is None

    def test_extract_protocol_special_cases(self):
        """Test special cases and potential edge scenarios."""
        # Multiple :// in URL (should match first)
        assert extract_protocol('http://example.com://path') == 'http'

        # URL with port and complex path
        assert extract_protocol('postgresql://user:pass@localhost:5432/mydb?ssl=true') == 'postgresql'

        # Very long protocol name
        long_protocol = 'a' * 50
        assert extract_protocol(f'{long_protocol}://host') == long_protocol


class TestNormalizeSqlSpaces:
    """Test cases for normalize_sql_spaces function."""

    def test_normalize_multiple_spaces(self):
        """Test normalization of multiple consecutive spaces."""
        # Multiple spaces between words
        assert normalize_sql_spaces('SELECT  *  FROM  table') == 'SELECT * FROM table'
        assert normalize_sql_spaces('SELECT   *   FROM   table') == 'SELECT * FROM table'

        # Many consecutive spaces
        assert normalize_sql_spaces('SELECT          *          FROM          table') == 'SELECT * FROM table'

        # Mixed multiple spaces
        assert normalize_sql_spaces('SELECT  *   FROM    table  WHERE     id = 1') == 'SELECT * FROM table WHERE id = 1'

    def test_normalize_leading_trailing_spaces(self):
        """Test trimming of leading and trailing spaces."""
        # Leading spaces
        assert normalize_sql_spaces('  SELECT * FROM table') == 'SELECT * FROM table'
        assert normalize_sql_spaces('     SELECT * FROM table') == 'SELECT * FROM table'

        # Trailing spaces
        assert normalize_sql_spaces('SELECT * FROM table  ') == 'SELECT * FROM table'
        assert normalize_sql_spaces('SELECT * FROM table     ') == 'SELECT * FROM table'

        # Both leading and trailing
        assert normalize_sql_spaces('  SELECT * FROM table  ') == 'SELECT * FROM table'
        assert normalize_sql_spaces('    SELECT * FROM table    ') == 'SELECT * FROM table'

    def test_normalize_preserves_other_whitespace(self):
        """Test that other whitespace characters are preserved."""
        # Tabs should be preserved
        assert normalize_sql_spaces('SELECT\t*\tFROM\ttable') == 'SELECT\t*\tFROM\ttable'

        # Newlines should be preserved
        assert normalize_sql_spaces('SELECT *\nFROM table') == 'SELECT *\nFROM table'

        # Carriage returns should be preserved
        assert normalize_sql_spaces('SELECT *\rFROM table') == 'SELECT *\rFROM table'

        # Mixed whitespace with multiple spaces
        assert (
            normalize_sql_spaces('SELECT  *\nFROM   table\t\tWHERE  id = 1') == 'SELECT *\nFROM table\t\tWHERE id = 1'
        )

    def test_normalize_edge_cases(self):
        """Test edge cases for SQL space normalization."""
        # Empty string
        assert normalize_sql_spaces('') == ''

        # Only spaces
        assert normalize_sql_spaces('   ') == ''
        assert normalize_sql_spaces('  ') == ''

        # Single space
        assert normalize_sql_spaces(' ') == ''

        # String with no spaces
        assert normalize_sql_spaces('SELECT*FROM*table') == 'SELECT*FROM*table'

        # Single word with leading/trailing spaces
        assert normalize_sql_spaces('  word  ') == 'word'

    def test_normalize_complex_sql_examples(self):
        """Test with realistic SQL query examples."""

        # INSERT statement
        sql_input = "INSERT   INTO   users   (name,  email)   VALUES   ('John',  'john@example.com')"
        expected = "INSERT INTO users (name, email) VALUES ('John', 'john@example.com')"
        assert normalize_sql_spaces(sql_input) == expected

        # UPDATE statement
        sql_input = "UPDATE   users   SET   name  =  'Jane'   WHERE   id  =  1  "
        expected = "UPDATE users SET name = 'Jane' WHERE id = 1"
        assert normalize_sql_spaces(sql_input) == expected

    def test_normalize_single_spaces_unchanged(self):
        """Test that strings with only single spaces remain unchanged."""
        # Already normalized strings
        assert normalize_sql_spaces('SELECT * FROM table') == 'SELECT * FROM table'
        assert (
            normalize_sql_spaces("INSERT INTO users (name) VALUES ('John')")
            == "INSERT INTO users (name) VALUES ('John')"
        )
        assert normalize_sql_spaces('a b c d e') == 'a b c d e'


class TestParseProcessorName:
    """Test cases for parse_processor_name function."""

    def test_normal_case_with_replica(self):
        """Test normal case with replica identifier."""
        result = parse_processor_name('MyProcessorName#156a')
        assert result == ('MyProcessorName', '156a')

    def test_no_replica_identifier(self):
        """Test case with no replica identifier."""
        result = parse_processor_name('MyProcessorName')
        assert result == ('MyProcessorName', None)

    def test_empty_replica_identifier(self, caplog):
        """Test case with empty replica identifier after #."""
        with caplog.at_level(logging.WARNING):
            result = parse_processor_name('MyProcessorName#')
            assert result == ('MyProcessorName', None)
            assert "empty replica part after '#'" in caplog.text

    def test_only_hash_symbol(self):
        """Test case with only hash symbol."""
        with pytest.raises(UnknownProcessor, match='empty'):
            parse_processor_name('#')

    @pytest.mark.parametrize(
        'processor_name',
        [
            'Processor_Name-123#replica_456',
            'Not::Valid#12',
            'Funn$#abd',
            '',  # empty string
        ],
    )
    def test_not_valid_identifier(self, processor_name):
        """Test case with invalid identifier."""
        with pytest.raises(UnknownProcessor, match='Invalid'):
            parse_processor_name(processor_name)

    def test_multiple_hashes(self):
        """Test case with multiple hash symbols."""
        result = parse_processor_name('Name#123#extra')
        assert result == ('Name', '123#extra')

    def test_whitespace_handling(self):
        """Test handling of leading/trailing whitespace."""
        result = parse_processor_name('  MyProcessorName  ')
        assert result == ('MyProcessorName', None)

    def test_numeric_replica_id(self):
        """Test numeric replica identifier."""
        result = parse_processor_name('Processor#123')
        assert result == ('Processor', '123')

    def test_complex_replica_id(self):
        """Test complex replica identifier with various characters."""
        result = parse_processor_name('Complex#abc123XYZ-._')
        assert result == ('Complex', 'abc123XYZ-._')

    def test_edge_case_single_character_name(self):
        """Test edge case with single character name."""
        result = parse_processor_name('A#1')
        assert result == ('A', '1')

    def test_edge_case_single_character_replica(self):
        """Test edge case with single character replica."""
        result = parse_processor_name('Name#B')
        assert result == ('Name', 'B')

    def test_replica_with_leading_zeros(self):
        """Test replica identifier with leading zeros."""
        result = parse_processor_name('Processor#007')
        assert result == ('Processor', '007')

    def test_replica_with_special_chars(self):
        """Test replica identifier with special characters."""
        result = parse_processor_name('Processor#v1.0-beta')
        assert result == ('Processor', 'v1.0-beta')

    def test_replica_with_unicode(self):
        """Test replica identifier with unicode characters."""
        result = parse_processor_name('Processor#αβγ')
        assert result == ('Processor', 'αβγ')

    def test_replica_with_spaces(self):
        """Test replica identifier with spaces."""
        result = parse_processor_name('Processor#replica 1')
        assert result == ('Processor', 'replica 1')

    def test_replica_with_underscore_and_dash(self):
        """Test replica identifier with underscore and dash."""
        result = parse_processor_name('Processor#replica_1-test')
        assert result == ('Processor', 'replica_1-test')
