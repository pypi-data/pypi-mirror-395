#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""Unit tests for the db_filter module."""

import logging
from collections import UserDict
from unittest.mock import MagicMock, Mock, patch

import peewee
import pytest

import mafw.db.db_filter
from mafw.db.db_filter import (
    ConditionalFilterCondition,
    ConditionalNode,
    ConditionNode,
    ExprParser,
    FilterNode,
    LogicalNode,
    ModelFilter,
    ParseError,
    ProcessorFilter,
    tokenize,
)
from mafw.enumerators import LogicalOp


class TestTokenize:
    """Tests for the tokenize function."""

    def test_tokenize_simple_expression(self):
        """Test tokenizing a simple AND expression."""
        tokens = tokenize('field1 AND field2')
        assert tokens == [('NAME', 'field1'), ('AND', 'AND'), ('NAME', 'field2')]

    def test_tokenize_with_parentheses(self):
        """Test tokenizing expression with parentheses."""
        tokens = tokenize('(field1 OR field2)')
        assert tokens == [('LPAREN', '('), ('NAME', 'field1'), ('OR', 'OR'), ('NAME', 'field2'), ('RPAREN', ')')]

    def test_tokenize_with_not(self):
        """Test tokenizing expression with NOT operator."""
        tokens = tokenize('NOT field1')
        assert tokens == [('NOT', 'NOT'), ('NAME', 'field1')]

    def test_tokenize_with_dots_and_colons(self):
        """Test tokenizing names with dots and colons."""
        tokens = tokenize('Model.field:subfield')
        assert tokens == [('NAME', 'Model.field:subfield')]

    def test_tokenize_skips_whitespace(self):
        """Test that whitespace is properly skipped."""
        tokens = tokenize('  field1   AND   field2  ')
        assert tokens == [('NAME', 'field1'), ('AND', 'AND'), ('NAME', 'field2')]

    def test_tokenize_raises_on_invalid_character(self):
        """Test that invalid characters raise ParseError."""
        with pytest.raises(ParseError, match='Unexpected character'):
            tokenize('field1 & field2')


class TestExprParser:
    """Tests for the ExprParser class."""

    @pytest.mark.parametrize(
        'input_,output_',
        [
            ('field1', ('NAME', 'field1')),
            ('field1 AND field2', ('AND', ('NAME', 'field1'), ('NAME', 'field2'))),
            ('field1 OR field2', ('OR', ('NAME', 'field1'), ('NAME', 'field2'))),
            ('NOT field1', ('NOT', ('NAME', 'field1'))),
            (
                '(field1 AND field2) OR field3',
                ('OR', ('AND', ('NAME', 'field1'), ('NAME', 'field2')), ('NAME', 'field3')),
            ),
            (
                'field1 AND (field2 OR NOT field3)',
                (('AND', ('NAME', 'field1'), ('OR', ('NAME', 'field2'), ('NOT', ('NAME', 'field3'))))),
            ),
        ],
    )
    def test_parse_parametric(self, input_, output_):
        parser = ExprParser(input_)
        result = parser.parse()
        assert result == output_

    def test_parse_raises_on_unexpected_token(self):
        """Test that unexpected tokens raise ParseError."""
        parser = ExprParser('field1 AND')
        with pytest.raises(ParseError, match='Unexpected end of expression'):
            parser.parse()

    def test_parse_raises_on_extra_tokens(self):
        """Test that extra tokens after expression raise ParseError."""
        parser = ExprParser('field1 field2')
        with pytest.raises(ParseError, match='Unexpected token after end'):
            parser.parse()

    def test_parse_raises_on_extra_tokens_at_beginning(self):
        """Test that extra tokens after expression raise ParseError."""
        parser = ExprParser('AND field1 field2')
        with pytest.raises(ParseError, match='Unexpected token'):
            parser.parse()

    def test_expect_raises_on_wrong_token(self):
        """Test that expect raises ParseError on wrong token type."""
        parser = ExprParser('field1')
        parser.pos = 0
        with pytest.raises(ParseError, match='Expected LPAREN'):
            parser.expect('LPAREN')


class TestConditionNode:
    """Tests for the ConditionNode class."""

    def test_condition_node_init_with_string_op(self):
        """Test initializing ConditionNode with string operation."""
        node = ConditionNode('field1', '==', 'value1')
        assert node.field == 'field1'
        assert node.operation == LogicalOp.EQ
        assert node.value == 'value1'

    def test_condition_node_init_with_logical_op(self):
        """Test initializing ConditionNode with LogicalOp enum."""
        node = ConditionNode('field1', LogicalOp.GT, 10)
        assert node.operation == LogicalOp.GT

    def test_condition_node_invalid_operation(self):
        """Test that invalid operation string raises ValueError."""
        with pytest.raises(ValueError, match='Unsupported operation'):
            ConditionNode('field1', 'INVALID_OP', 'value1')

    def test_condition_node_like_operation(self):
        """Test LIKE operation."""
        mock_model = Mock()
        mock_field = MagicMock()
        mock_model.field1 = mock_field

        node = ConditionNode('field1', LogicalOp.LIKE, '%pattern%')
        node.to_expression(mock_model)

        # Verify pow operator is used for LIKE
        mock_field.__pow__.assert_called_once_with('%pattern%')

    def test_condition_node_in_operation(self):
        """Test IN operation."""
        mock_model = Mock()
        mock_field = MagicMock()
        mock_field.in_ = Mock(return_value=MagicMock())
        mock_model.field1 = mock_field

        node = ConditionNode('field1', LogicalOp.IN, [1, 2, 3])
        node.to_expression(mock_model)

        mock_field.in_.assert_called_once_with([1, 2, 3])

    def test_condition_node_in_operation_invalid_type(self):
        """Test IN operation with invalid value type."""
        mock_model = Mock()
        mock_field = MagicMock()
        mock_model.field1 = mock_field

        node = ConditionNode('field1', LogicalOp.IN, 'not_a_list')
        with pytest.raises(TypeError, match='IN operation requires list/tuple'):
            node.to_expression(mock_model)

    def test_condition_node_not_in_operation(self):
        """Test NOT_IN operation."""
        mock_model = Mock()
        mock_field = MagicMock()
        mock_field.not_in = Mock(return_value=MagicMock())
        mock_model.field1 = mock_field

        node = ConditionNode('field1', LogicalOp.NOT_IN, [1, 2, 3])
        node.to_expression(mock_model)

        mock_field.not_in.assert_called_once_with([1, 2, 3])

    def test_condition_node_between_operation(self):
        """Test BETWEEN operation."""
        mock_model = Mock()
        mock_field = MagicMock()
        mock_field.between = Mock(return_value=MagicMock())
        mock_model.field1 = mock_field

        node = ConditionNode('field1', LogicalOp.BETWEEN, [1, 10])
        node.to_expression(mock_model)

        mock_field.between.assert_called_once_with(1, 10)

    def test_condition_node_between_operation_invalid_value(self):
        """Test BETWEEN operation with invalid value."""
        mock_model = Mock()
        mock_field = MagicMock()
        mock_model.field1 = mock_field

        node = ConditionNode('field1', LogicalOp.BETWEEN, [1, 2, 3])
        with pytest.raises(TypeError, match='BETWEEN operation requires list/tuple of 2 elements'):
            node.to_expression(mock_model)

    def test_condition_node_bit_and_operation(self):
        """Test BIT_AND operation."""
        mock_model = Mock()
        mock_field = MagicMock()
        mock_field.bin_and = Mock(return_value=MagicMock())
        mock_model.field1 = mock_field

        node = ConditionNode('field1', LogicalOp.BIT_AND, 5)
        node.to_expression(mock_model)

        mock_field.bin_and.assert_called_once_with(5)

    def test_condition_node_bit_or_operation(self):
        """Test BIT_OR operation."""
        mock_model = Mock()
        mock_field = MagicMock()
        mock_field.bin_or = Mock(return_value=MagicMock())
        mock_model.field1 = mock_field

        node = ConditionNode('field1', LogicalOp.BIT_OR, 5)
        node.to_expression(mock_model)

        mock_field.bin_or.assert_called_once_with(5)

    def test_condition_node_is_null_operation(self):
        """Test IS_NULL operation."""
        mock_model = Mock()
        mock_field = MagicMock()
        mock_field.is_null = Mock(return_value=MagicMock())
        mock_model.field1 = mock_field

        node = ConditionNode('field1', LogicalOp.IS_NULL, None)
        node.to_expression(mock_model)

        mock_field.is_null.assert_called_once_with()

    def test_condition_node_is_not_null_operation(self):
        """Test IS_NOT_NULL operation."""
        mock_model = Mock()
        mock_field = MagicMock()
        mock_field.is_null = Mock(return_value=MagicMock())
        mock_model.field1 = mock_field

        node = ConditionNode('field1', LogicalOp.IS_NOT_NULL, None)
        node.to_expression(mock_model)

        mock_field.is_null.assert_called_once_with(False)

    def test_condition_node_regexp_operation(self):
        """Test REGEXP operation."""
        mock_model = Mock()
        mock_field = MagicMock()
        mock_field.regexp = Mock(return_value=MagicMock())
        mock_model.field1 = mock_field

        node = ConditionNode('field1', LogicalOp.REGEXP, r'\d+')
        node.to_expression(mock_model)

        mock_field.regexp.assert_called_once_with(r'\d+')

    def test_condition_node_regexp_not_supported(self):
        """Test REGEXP operation when not supported by field."""
        mock_model = Mock()
        mock_field = MagicMock(spec=[])  # No regexp method
        mock_model.field1 = mock_field

        node = ConditionNode('field1', LogicalOp.REGEXP, r'\d+')
        with pytest.raises(ValueError, match='REGEXP operation not supported'):
            node.to_expression(mock_model)

    def test_condition_node_no_field_raises_error(self):
        """Test that ConditionNode without field raises RuntimeError."""
        node = ConditionNode(None, LogicalOp.EQ, 'value')
        mock_model = Mock()

        with pytest.raises(RuntimeError, match='ConditionNode has no field to evaluate'):
            node.to_expression(mock_model)

    def test_to_expression_eq(self):
        """Test EQ operation in to_expression."""
        mock_model = Mock()
        mock_field = Mock()
        mock_model.field1 = mock_field
        mock_field.__eq__ = Mock(return_value='field1 == value1')

        node = ConditionNode('field1', LogicalOp.EQ, 'value1')
        result = node.to_expression(mock_model)
        assert result == 'field1 == value1'

    def test_to_expression_ne(self):
        """Test NE operation in to_expression."""
        mock_model = Mock()
        mock_field = Mock()
        mock_model.field1 = mock_field
        mock_field.__ne__ = Mock(return_value='field1 != value1')

        node = ConditionNode('field1', LogicalOp.NE, 'value1')
        result = node.to_expression(mock_model)
        assert result == 'field1 != value1'

    def test_to_expression_lt(self):
        """Test LT operation in to_expression."""
        mock_model = Mock()
        mock_field = Mock()
        mock_model.field1 = mock_field
        mock_field.__lt__ = Mock(return_value='field1 < value1')

        node = ConditionNode('field1', LogicalOp.LT, 'value1')
        result = node.to_expression(mock_model)
        assert result == 'field1 < value1'

    def test_to_expression_le(self):
        """Test LE operation in to_expression."""
        mock_model = Mock()
        mock_field = Mock()
        mock_model.field1 = mock_field
        mock_field.__le__ = Mock(return_value='field1 <= value1')

        node = ConditionNode('field1', LogicalOp.LE, 'value1')
        result = node.to_expression(mock_model)
        assert result == 'field1 <= value1'

    def test_to_expression_gt(self):
        """Test GT operation in to_expression."""
        mock_model = Mock()
        mock_field = Mock()
        mock_model.field1 = mock_field
        mock_field.__gt__ = Mock(return_value='field1 > value1')

        node = ConditionNode('field1', LogicalOp.GT, 'value1')
        result = node.to_expression(mock_model)
        assert result == 'field1 > value1'

    def test_to_expression_ge(self):
        """Test GE operation in to_expression."""
        mock_model = Mock()
        mock_field = Mock()
        mock_model.field1 = mock_field
        mock_field.__ge__ = Mock(return_value='field1 >= value1')

        node = ConditionNode('field1', LogicalOp.GE, 'value1')
        result = node.to_expression(mock_model)
        assert result == 'field1 >= value1'

    def test_to_expression_glob(self):
        """Test GLOB operation in to_expression."""
        mock_model = Mock()
        mock_field = Mock()
        mock_model.field1 = mock_field
        mock_field.__mod__ = Mock(return_value='field1 % value1')

        node = ConditionNode('field1', LogicalOp.GLOB, 'value1')
        result = node.to_expression(mock_model)
        assert result == 'field1 % value1'

    def test_to_expression_like(self):
        """Test LIKE operation in to_expression."""
        mock_model = Mock()
        mock_field = Mock()
        mock_model.field1 = mock_field
        mock_field.__pow__ = Mock(return_value='field1 ** value1')

        node = ConditionNode('field1', LogicalOp.LIKE, 'value1')
        result = node.to_expression(mock_model)
        assert result == 'field1 ** value1'

    def test_to_expression_regexp(self):
        """Test REGEXP operation in to_expression."""
        mock_model = Mock()
        mock_field = Mock()
        mock_model.field1 = mock_field
        mock_field.regexp = Mock(return_value='field1 regexp value1')

        node = ConditionNode('field1', LogicalOp.REGEXP, 'value1')
        result = node.to_expression(mock_model)
        assert result == 'field1 regexp value1'

    def test_to_expression_regexp_not_supported(self):
        """Test REGEXP operation when not supported."""
        mock_model = Mock()
        mock_field = Mock()
        mock_model.field1 = mock_field
        delattr(mock_field, 'regexp')

        node = ConditionNode('field1', LogicalOp.REGEXP, 'value1')
        with pytest.raises(ValueError, match='REGEXP operation not supported for field type'):
            node.to_expression(mock_model)

    def test_to_expression_in(self):
        """Test IN operation in to_expression."""
        mock_model = Mock()
        mock_field = Mock()
        mock_model.field1 = mock_field
        mock_field.in_ = Mock(return_value='field1 in_ value1')

        node = ConditionNode('field1', LogicalOp.IN, [1, 2, 3])
        result = node.to_expression(mock_model)
        assert result == 'field1 in_ value1'

    def test_to_expression_in_invalid_type(self):
        """Test IN operation with invalid value type."""
        node = ConditionNode('field1', LogicalOp.IN, 'invalid')
        with pytest.raises(TypeError, match='IN operation requires list/tuple'):
            node.to_expression(Mock())

    def test_to_expression_in_not_supported(self):
        """Test IN operation when not supported."""
        mock_model = Mock()
        mock_field = Mock()
        mock_model.field1 = mock_field
        delattr(mock_field, 'in_')

        node = ConditionNode('field1', LogicalOp.IN, [1, 2, 3])
        with pytest.raises(ValueError, match='IN operation not supported for field type'):
            node.to_expression(mock_model)

    def test_to_expression_not_in(self):
        """Test NOT_IN operation in to_expression."""
        mock_model = Mock()
        mock_field = Mock()
        mock_model.field1 = mock_field
        mock_field.not_in = Mock(return_value='field1 not_in value1')

        node = ConditionNode('field1', LogicalOp.NOT_IN, [1, 2, 3])
        result = node.to_expression(mock_model)
        assert result == 'field1 not_in value1'

    def test_to_expression_not_in_invalid_type(self):
        """Test NOT_IN operation with invalid value type."""
        node = ConditionNode('field1', LogicalOp.NOT_IN, 'invalid')
        with pytest.raises(TypeError, match='NOT_IN operation requires list/tuple'):
            node.to_expression(Mock())

    def test_to_expression_not_in_not_supported(self):
        """Test NOT_IN operation when not supported."""
        mock_model = Mock()
        mock_field = Mock()
        mock_model.field1 = mock_field
        delattr(mock_field, 'not_in')

        node = ConditionNode('field1', LogicalOp.NOT_IN, [1, 2, 3])
        with pytest.raises(ValueError, match='NOT_IN operation not supported for field type'):
            node.to_expression(mock_model)

    def test_to_expression_between(self):
        """Test BETWEEN operation in to_expression."""
        mock_model = Mock()
        mock_field = Mock()
        mock_model.field1 = mock_field
        mock_field.between = Mock(return_value='field1 between value1')

        node = ConditionNode('field1', LogicalOp.BETWEEN, [1, 2])
        result = node.to_expression(mock_model)
        assert result == 'field1 between value1'

    def test_to_expression_between_invalid_type(self):
        """Test BETWEEN operation with invalid value type."""
        node = ConditionNode('field1', LogicalOp.BETWEEN, 'invalid')
        with pytest.raises(TypeError, match='BETWEEN operation requires list/tuple of 2 elements'):
            node.to_expression(Mock())

    def test_to_expression_between_invalid_length(self):
        """Test BETWEEN operation with wrong length."""
        node = ConditionNode('field1', LogicalOp.BETWEEN, [1, 2, 3])
        with pytest.raises(TypeError, match='BETWEEN operation requires list/tuple of 2 elements'):
            node.to_expression(Mock())

    def test_to_expression_between_not_supported(self):
        """Test BETWEEN operation when not supported."""
        mock_model = Mock()
        mock_field = Mock()
        mock_model.field1 = mock_field
        delattr(mock_field, 'between')

        node = ConditionNode('field1', LogicalOp.BETWEEN, [1, 2])
        with pytest.raises(ValueError, match='BETWEEN operation not supported for field type'):
            node.to_expression(mock_model)

    def test_to_expression_bit_and(self):
        """Test BIT_AND operation in to_expression."""
        mock_model = Mock()
        mock_field = Mock()
        mock_model.field1 = mock_field
        mock_field.bin_and = Mock(return_value='field1 bin_and value1')

        node = ConditionNode('field1', LogicalOp.BIT_AND, 5)
        result = node.to_expression(mock_model)
        assert result

    def test_to_expression_bit_and_not_supported(self):
        """Test BIT_AND operation when not supported."""
        mock_model = Mock()
        mock_field = Mock()
        mock_model.field1 = mock_field
        delattr(mock_field, 'bin_and')

        node = ConditionNode('field1', LogicalOp.BIT_AND, 5)
        with pytest.raises(ValueError, match='BIT_AND operation not supported for field type'):
            node.to_expression(mock_model)

    def test_to_expression_bit_or(self):
        """Test BIT_OR operation in to_expression."""
        mock_model = Mock()
        mock_field = Mock()
        mock_model.field1 = mock_field
        mock_field.bin_or = Mock(return_value='field1 bin_or value1')

        node = ConditionNode('field1', LogicalOp.BIT_OR, 5)
        result = node.to_expression(mock_model)
        assert result

    def test_to_expression_bit_or_not_supported(self):
        """Test BIT_OR operation when not supported."""
        mock_model = Mock()
        mock_field = Mock()
        mock_model.field1 = mock_field
        delattr(mock_field, 'bin_or')

        node = ConditionNode('field1', LogicalOp.BIT_OR, 5)
        with pytest.raises(ValueError, match='BIT_OR operation not supported for field type'):
            node.to_expression(mock_model)

    def test_to_expression_is_null(self):
        """Test IS_NULL operation in to_expression."""
        mock_model = Mock()
        mock_field = Mock()
        mock_model.field1 = mock_field
        mock_field.is_null = Mock(return_value='field1 is_null()')

        node = ConditionNode('field1', LogicalOp.IS_NULL, None)
        result = node.to_expression(mock_model)
        assert result == 'field1 is_null()'

    def test_to_expression_is_not_null(self):
        """Test IS_NOT_NULL operation in to_expression."""
        mock_model = Mock()
        mock_field = Mock()
        mock_model.field1 = mock_field
        mock_field.is_null = Mock(return_value='field1 is_null(False)')

        node = ConditionNode('field1', LogicalOp.IS_NOT_NULL, None)
        result = node.to_expression(mock_model)
        assert result == 'field1 is_null(False)'

    def test_to_expression_unsupported_operation(self):
        """Test unsupported operation raises ValueError."""

        mock_model = Mock()
        mock_field = Mock()
        mock_model.field1 = mock_field
        mock_field.is_null = Mock(return_value='field1 is_null(False)')
        # the constructor is not complaining
        node = ConditionNode('field1', LogicalOp.IS_NOT_NULL, None)
        node.operation = 'UNSUPPORTED'
        with pytest.raises(ValueError, match='Unsupported operation: UNSUPPORTED'):
            node.to_expression(mock_model)


class TestLogicalNode:
    """Tests for the LogicalNode class."""

    def test_logical_node_and(self):
        """Test AND logical operation."""
        mock_model = Mock()
        child1 = Mock(spec=FilterNode)
        child1.to_expression = Mock(return_value=MagicMock())
        child2 = Mock(spec=FilterNode)
        child2.to_expression = Mock(return_value=MagicMock())

        node = LogicalNode('AND', child1, child2)
        node.to_expression(mock_model)

        child1.to_expression.assert_called_once_with(mock_model)
        child2.to_expression.assert_called_once_with(mock_model)

    def test_logical_node_or(self):
        """Test OR logical operation."""
        mock_model = Mock()
        child1 = Mock(spec=FilterNode)
        child1.to_expression = Mock(return_value=MagicMock())
        child2 = Mock(spec=FilterNode)
        child2.to_expression = Mock(return_value=MagicMock())

        node = LogicalNode('OR', child1, child2)
        node.to_expression(mock_model)

        child1.to_expression.assert_called_once_with(mock_model)
        child2.to_expression.assert_called_once_with(mock_model)

    def test_logical_node_not(self):
        """Test NOT logical operation."""
        mock_model = Mock()
        child = Mock(spec=FilterNode)
        child.to_expression = Mock(return_value=MagicMock())

        node = LogicalNode('NOT', child)
        node.to_expression(mock_model)

        child.to_expression.assert_called_once_with(mock_model)

    def test_logical_node_unknown_op(self):
        """Test that unknown logical operation raises ValueError."""
        mock_model = Mock()
        child = Mock(spec=FilterNode)

        node = LogicalNode('UNKNOWN', child)
        with pytest.raises(ValueError, match='Unknown logical op'):
            node.to_expression(mock_model)


class TestConditionalFilterCondition:
    """Tests for the ConditionalFilterCondition class."""

    def test_init(self):
        """Test ConditionalFilterCondition initialization."""
        condition = ConditionalFilterCondition(
            condition_field='field1',
            condition_op='IN',
            condition_value=[1, 2],
            then_field='field2',
            then_op='EQ',
            then_value=3,
        )
        assert condition.condition_field == 'field1'
        assert condition.condition_op == 'IN'
        assert condition.condition_value == [1, 2]
        assert condition.then_field == 'field2'
        assert condition.then_op == 'EQ'
        assert condition.then_value == 3

    def test_to_expression_simple_case(self):
        """Test simple conditional expression generation."""
        mock_model = Mock()
        mock_condition_field = Mock()
        mock_then_field = Mock()
        mock_model.field1 = mock_condition_field
        mock_model.field2 = mock_then_field

        condition_expr = 1
        then_expr = 2

        # Mock the condition expression
        mock_condition_field.in_ = Mock(return_value=condition_expr)
        mock_then_field.__eq__ = Mock(return_value=then_expr)

        condition = ConditionalFilterCondition(
            condition_field='field1',
            condition_op='IN',
            condition_value=[1, 2],
            then_field='field2',
            then_op='==',
            then_value=3,
        )

        result = condition.to_expression(mock_model)
        # Should return (condition_expr & then_expr) | (~condition_expr & True)
        assert result == (condition_expr & then_expr) | (~condition_expr & True)

    def test_to_expression_with_else(self):
        """Test conditional expression with else clause."""
        mock_model = Mock()
        mock_condition_field = Mock()
        mock_then_field = Mock()
        mock_else_field = Mock()
        mock_model.field1 = mock_condition_field
        mock_model.field2 = mock_then_field
        mock_model.field3 = mock_else_field

        condition_expr = 1
        then_expr = 2
        else_expr = 3

        # Mock the expressions
        mock_condition_field.in_ = Mock(return_value=condition_expr)
        mock_then_field.__eq__ = Mock(return_value=then_expr)
        mock_else_field.__eq__ = Mock(return_value=else_expr)

        condition = ConditionalFilterCondition(
            condition_field='field1',
            condition_op='IN',
            condition_value=[1, 2],
            then_field='field2',
            then_op='==',
            then_value=3,
            else_field='field3',
            else_op='==',
            else_value=4,
        )

        result = condition.to_expression(mock_model)
        # Should return (condition_expr & then_expr) | (~condition_expr & else_expr)
        assert result == (condition_expr & then_expr) | (~condition_expr & else_expr)

    def test_conditional_filter_condition_equality(self):
        """Test equality comparison of ConditionalFilterCondition."""
        cond1 = ConditionalFilterCondition(
            condition_field='field1',
            condition_op=LogicalOp.EQ,
            condition_value='value1',
            then_field='field2',
            then_op=LogicalOp.GT,
            then_value=10,
        )

        cond2 = ConditionalFilterCondition(
            condition_field='field1',
            condition_op=LogicalOp.EQ,
            condition_value='value1',
            then_field='field2',
            then_op=LogicalOp.GT,
            then_value=10,
        )

        assert cond1 == cond2

    def test_conditional_filter_condition_inequality(self):
        """Test inequality comparison of ConditionalFilterCondition."""
        cond1 = ConditionalFilterCondition(
            condition_field='field1',
            condition_op=LogicalOp.EQ,
            condition_value='value1',
            then_field='field2',
            then_op=LogicalOp.GT,
            then_value=10,
        )

        cond2 = ConditionalFilterCondition(
            condition_field='field1',
            condition_op=LogicalOp.EQ,
            condition_value='value2',
            then_field='field2',
            then_op=LogicalOp.GT,
            then_value=10,
        )

        assert cond1 != cond2

    def test_conditional_filter_condition_not_equal_to_other_type(self):
        """Test that ConditionalFilterCondition is not equal to other types."""
        cond = ConditionalFilterCondition(
            condition_field='field1',
            condition_op=LogicalOp.EQ,
            condition_value='value1',
            then_field='field2',
            then_op=LogicalOp.GT,
            then_value=10,
        )

        assert cond != 'not a conditional'
        assert cond != 42


class TestConditionalNode:
    """Tests for the ConditionalNode class."""

    def test_conditional_node_init(self):
        """Test initializing ConditionalNode."""
        cond = ConditionalFilterCondition(
            condition_field='field1',
            condition_op=LogicalOp.EQ,
            condition_value='value1',
            then_field='field2',
            then_op=LogicalOp.GT,
            then_value=10,
        )

        node = ConditionalNode(cond, name='test_cond')
        assert node.conditional == cond
        assert node.name == 'test_cond'

    def test_conditional_node_to_expression(self):
        """Test converting ConditionalNode to expression."""
        mock_model = Mock()
        mock_field1 = peewee.IntegerField()
        mock_field2 = peewee.IntegerField()
        mock_model.field1 = mock_field1
        mock_model.field2 = mock_field2

        cond = ConditionalFilterCondition(
            condition_field='field1',
            condition_op=LogicalOp.EQ,
            condition_value='value1',
            then_field='field2',
            then_op=LogicalOp.GT,
            then_value=10,
        )

        node = ConditionalNode(cond)
        result = node.to_expression(mock_model)
        assert result is not None


class TestModelFilter:
    """Tests for the ModelFilter class."""

    def test_model_filter_init_simple(self):
        """Test initializing ModelFilter with simple parameters."""
        flt = ModelFilter('Processor.__filter__.Model', field1='value1', field2=10)

        assert flt.name == 'Processor.__filter__.Model'
        assert flt.model_name == 'Model'
        assert len(flt._nodes) == 2

    def test_model_filter_init_with_dict_op(self):
        """Test initializing ModelFilter with dict operation."""
        flt = ModelFilter('Processor.__filter__.Model', field1={'op': '==', 'value': 'value1'})

        assert len(flt._nodes) == 1
        node = flt._nodes['field1']
        assert isinstance(node, ConditionNode)
        assert node.operation == LogicalOp.EQ

    def test_model_filter_init_with_nested_dict(self):
        """Test initializing ModelFilter with nested dict."""
        flt = ModelFilter(
            'Processor.__filter__.Model',
            field1={
                'sub1': {'op': '==', 'value': 'v1'},
                'sub2': {'op': '>', 'value': 10},
                '__logic__': 'sub1 AND sub2',
            },
        )

        assert len(flt._nodes) == 1
        node = flt._nodes['field1']
        assert isinstance(node, LogicalNode)

    def test_model_filter_init_with_nested_dict_and_value(self):
        """Test initializing ModelFilter with nested dict."""
        flt = ModelFilter(
            'Processor.__filter__.Model',
            field1={'sub1': {'op': '==', 'value': 'v1'}, 'sub2': 5, '__logic__': 'sub1 AND sub2'},
        )

        assert len(flt._nodes) == 1
        node = flt._nodes['field1']
        assert isinstance(node, LogicalNode)

    def test_model_filter_init_with_nested_dict_and_value_default_and(self):
        """Test initializing ModelFilter with nested dict."""
        flt = ModelFilter(
            'Processor.__filter__.Model',
            field1={
                'sub1': {'op': '==', 'value': 'v1'},
                'sub2': 5,
            },
        )

        assert len(flt._nodes) == 1
        node = flt._nodes['field1']
        assert isinstance(node, LogicalNode)

    def test_model_filter_init_with_logic_expression(self):
        """Test initializing ModelFilter with logic expression."""
        flt = ModelFilter('Processor.__filter__.Model', field1='value1', field2=10, __logic__='field1 OR field2')

        assert flt._logic_expr == 'field1 OR field2'

    def test_model_filter_init_with_conditionals(self):
        """Test initializing ModelFilter with conditional filters."""
        conditional_dict = {
            'condition_field': 'field1',
            'condition_op': '==',
            'condition_value': 'value1',
            'then_field': 'field2',
            'then_op': '>',
            'then_value': 10,
        }

        flt = ModelFilter('Processor.__filter__.Model', __conditional__=[conditional_dict])

        assert len(flt._cond_nodes) == 1

    def test_model_filter_init_with_conditional_no_list(self):
        """Test initializing ModelFilter with conditional filters."""
        conditional_dict = {
            'condition_field': 'field1',
            'condition_op': '==',
            'condition_value': 'value1',
            'then_field': 'field2',
            'then_op': '>',
            'then_value': 10,
        }

        flt = ModelFilter('Processor.__filter__.Model', __conditional__=conditional_dict)

        assert len(flt._cond_nodes) == 1

    def test_model_filter_bind_with_model(self):
        """Test binding ModelFilter to a model."""
        mock_model = Mock()
        mock_model.__name__ = 'TestModel'

        flt = ModelFilter('Processor.__filter__.TestModel', field1='value1')
        flt.bind(mock_model)

        assert flt.model == mock_model
        assert flt.is_bound is True

    def test_model_filter_bind_warns_on_logic_field_conflict(self):
        """Test that binding warns when model has __logic__ field."""
        mock_model = Mock()
        mock_model.__name__ = 'TestModel'
        mock_model.__logic__ = 'some_field'

        flt = ModelFilter('Processor.__filter__.TestModel', field1='value1', __logic__='field1')

        with patch('mafw.db.db_filter.log.warning') as mock_warning:
            flt.bind(mock_model)
            assert mock_warning.call_count == 2
            assert flt._logic_expr is None

    def test_model_filter_add_conditional(self):
        """Test adding conditional to ModelFilter."""
        flt = ModelFilter('Processor.__filter__.Model')

        cond = ConditionalFilterCondition(
            condition_field='field1',
            condition_op=LogicalOp.EQ,
            condition_value='value1',
            then_field='field2',
            then_op=LogicalOp.GT,
            then_value=10,
            name='test_cond',
        )

        flt.add_conditional(cond)
        assert 'test_cond' in flt._cond_nodes
        assert 'test_cond' in flt._nodes

    def test_model_filter_add_conditional_auto_name(self):
        """Test adding conditional without name generates auto name."""
        flt = ModelFilter('Processor.__filter__.Model')

        cond = ConditionalFilterCondition(
            condition_field='field1',
            condition_op=LogicalOp.EQ,
            condition_value='value1',
            then_field='field2',
            then_op=LogicalOp.GT,
            then_value=10,
        )

        flt.add_conditional(cond)
        assert len(flt._cond_nodes) == 1
        assert '__cond0__' in flt._cond_nodes

    def test_model_filter_add_conditional_duplicate_name_raises(self):
        """Test that duplicate conditional name raises KeyError."""
        flt = ModelFilter('Processor.__filter__.Model')

        cond1 = ConditionalFilterCondition(
            condition_field='field1',
            condition_op=LogicalOp.EQ,
            condition_value='value1',
            then_field='field2',
            then_op=LogicalOp.GT,
            then_value=10,
            name='test_cond',
        )

        cond2 = ConditionalFilterCondition(
            condition_field='field3',
            condition_op=LogicalOp.EQ,
            condition_value='value3',
            then_field='field4',
            then_op=LogicalOp.GT,
            then_value=20,
            name='test_cond',
        )

        flt.add_conditional(cond1)
        with pytest.raises(KeyError, match='already exists'):
            flt.add_conditional(cond2)

    def test_model_filter_add_conditional_from_dict(self):
        """Test adding conditional from dictionary."""
        flt = ModelFilter('Processor.__filter__.Model')

        config = {
            'condition_field': 'field1',
            'condition_op': 'EQ',
            'condition_value': 'value1',
            'then_field': 'field2',
            'then_op': 'GT',
            'then_value': 10,
            'name': 'test_cond',
        }

        flt.add_conditional_from_dict(config)
        assert 'test_cond' in flt._cond_nodes

    def test_model_filter_create_condition_node_from_int(self):
        """Test creating ConditionNode from int value."""
        node = ModelFilter._create_condition_node_from_value(10, 'field1')
        assert isinstance(node, ConditionNode)
        assert node.operation == LogicalOp.EQ
        assert node.value == 10

    def test_model_filter_create_condition_node_from_float(self):
        """Test creating ConditionNode from float value."""
        node = ModelFilter._create_condition_node_from_value(10.5, 'field1')
        assert node.operation == LogicalOp.EQ
        assert node.value == 10.5

    def test_model_filter_create_condition_node_from_bool(self):
        """Test creating ConditionNode from bool value."""
        node = ModelFilter._create_condition_node_from_value(True, 'field1')
        assert node.operation == LogicalOp.EQ
        assert node.value is True

    def test_model_filter_create_condition_node_from_string(self):
        """Test creating ConditionNode from string value."""
        node = ModelFilter._create_condition_node_from_value('*.txt', 'field1')
        assert node.operation == LogicalOp.GLOB
        assert node.value == '*.txt'

    def test_model_filter_create_condition_node_from_list(self):
        """Test creating ConditionNode from list value."""
        node = ModelFilter._create_condition_node_from_value([1, 2, 3], 'field1')
        assert node.operation == LogicalOp.IN
        assert node.value == [1, 2, 3]

    def test_model_filter_create_condition_node_invalid_type(self):
        """Test creating ConditionNode from unsupported type raises TypeError."""
        with pytest.raises(TypeError, match='unsupported type'):
            ModelFilter._create_condition_node_from_value({'key': 'value'}, 'field1')

    def test_model_filter_from_conf(self):
        """Test creating ModelFilter from configuration."""
        conf = {'TestProc': {'__filter__': {'TestModel': {'field1': 'value1', 'field2': 10}}}}

        flt = ModelFilter.from_conf('TestProc.__filter__.TestModel', conf)
        assert flt.name == 'TestProc.__filter__.TestModel'
        assert len(flt._nodes) == 2

    def test_bind_success(self):
        """Test successful model binding."""
        mock_model = Mock()
        filter_obj = ModelFilter('TestProcessor.__filter__.TestModel')
        filter_obj.bind(mock_model)
        assert filter_obj.is_bound
        assert filter_obj.model == mock_model

    def test_add_conditional(self):
        """Test adding conditional filter."""
        filter_obj = ModelFilter('TestProcessor.__filter__.TestModel')
        condition = ConditionalFilterCondition(
            condition_field='field1',
            condition_op='IN',
            condition_value=[1, 2],
            then_field='field2',
            then_op='EQ',
            then_value=3,
        )
        filter_obj.add_conditional(condition)
        assert len(filter_obj._cond_nodes) == 1
        assert len(filter_obj._nodes) == 1

    def test_add_conditional_named(self):
        """Test adding conditional filter with name."""
        filter_obj = ModelFilter('TestProcessor.__filter__.TestModel')
        condition = ConditionalFilterCondition(
            condition_field='field1',
            condition_op='IN',
            condition_value=[1, 2],
            then_field='field2',
            then_op='EQ',
            then_value=3,
            name='test_condition',
        )
        filter_obj.add_conditional(condition)
        assert 'test_condition' in filter_obj._cond_nodes
        assert 'test_condition' in filter_obj._nodes

    def test_add_conditional_named_increment(self):
        """Test adding conditional filter with name."""
        filter_obj = ModelFilter('TestProcessor.__filter__.TestModel')
        condition1 = ConditionalFilterCondition(
            condition_field='field1',
            condition_op='IN',
            condition_value=[1, 2],
            then_field='field2',
            then_op='EQ',
            then_value=3,
            name='__cond1__',
        )
        condition2 = ConditionalFilterCondition(
            condition_field='field1',
            condition_op='IN',
            condition_value=[1, 2],
            then_field='field2',
            then_op='EQ',
            then_value=3,
        )
        filter_obj.add_conditional(condition1)
        filter_obj.add_conditional(condition2)

        for name in ['__cond1__', '__cond2__']:
            assert name in filter_obj._cond_nodes
            assert name in filter_obj._nodes

    def test_filter_with_not_dotted_name(self):
        flt = ModelFilter('OneFileter')
        assert flt.name == 'OneFileter'
        assert flt.model_name == 'OneFileter'

    def test_filter_not_filter_in_name(self):
        flt = ModelFilter('Processor.FLT.TestModel')
        assert flt.name == 'Processor.FLT.TestModel'
        assert flt.model_name == 'TestModel'

    def test_filter_not_filter_in_name_from_conf(self):
        conf = {'Processor': {'FLT': {'TestModel': {'field1': 'value1'}}}}
        flt = ModelFilter.from_conf('Processor.FLT.TestModel', conf)
        assert flt.name == 'Processor.FLT.TestModel'
        assert flt.model_name == 'TestModel'

    def test_filter_not_filter_in_name_from_conf2(self):
        conf = {'NotProcessor': {'FLT': {'TestModel': {'field1': 'value1'}}}}
        flt = ModelFilter.from_conf('Processor.__filter__.TestModel', conf)
        assert flt.name == 'Processor.__filter__.TestModel'
        assert flt.model_name == 'TestModel'

    def test_model_filter_filter_with_invalid_logic_raises(self):
        """Test that invalid logic expression raises ValueError."""
        mock_model = Mock()
        flt = ModelFilter('Processor.__filter__.Model', field1='value1', __logic__='INVALID SYNTAX &&&')
        flt.bind(mock_model)

        with pytest.raises(ValueError, match='Error parsing logic'):
            flt.filter()

    def test_model_filter_subfilter_with_valid_logic(self):
        mock_model = Mock()
        flt = ModelFilter(
            'Processor.__filter__.Model',
            field1={
                '__logic__': 'a AND b OR NOT c',
                'a': 5,
                'b': 10,
                'c': True,
            },
        )
        flt.bind(mock_model)
        assert len(flt._nodes) == 1
        assert 'field1' in flt._nodes

    def test_model_filter_filter_with_unknown_name_in_logic_raises(self):
        """Test that unknown name in logic raises ValueError."""
        mock_model = Mock()
        mock_field1 = MagicMock()
        mock_model.field1 = mock_field1

        flt = ModelFilter('Processor.__filter__.Model', field1='value1', __logic__='field1 AND unknown_field')
        flt.bind(mock_model)

        with pytest.raises(ValueError, match='Error evaluating logic'):
            flt.filter()

    def test_model_filter_with_nested_missing_name(self):
        with pytest.raises(KeyError, match='Unknown name unknown_field in nested logic for field field1'):
            ModelFilter('Processor.__filter__.Model', field1={'__logic__': 'a AND unknown_field', 'a': 5, 'b': 10})

    def test_model_filter_with_nested_unexpected_keyword(self):
        with patch.object(mafw.db.db_filter.ExprParser, 'parse', return_value=('NAND', ('a', 'b'))):
            with pytest.raises(ValueError, match='Unsupported AST node'):
                ModelFilter('Processor.__filter__.Model', field1={'__logic__': 'a AND unknown_field', 'a': 5, 'b': 10})

    def test_model_filter_with_unexpected_keyword(self):
        filter_obj = ModelFilter('Processor.__filter__.Model', __logic__='field1 AND field2', field1=5, field2=10)

        mock_model = Mock()
        filter_obj.bind(mock_model)

        # Mock the node expressions
        mock_node1 = Mock()
        mock_node2 = Mock()
        mock_node1.to_expression.return_value = 1
        mock_node2.to_expression.return_value = 1
        filter_obj._nodes['field1'] = mock_node1
        filter_obj._nodes['field2'] = mock_node2

        with patch.object(mafw.db.db_filter.ExprParser, 'parse', return_value=('NAND', ('a', 'b'))):
            with pytest.raises(ValueError, match='Unsupported AST node'):
                filter_obj.filter()

    def test_filter_not_bound(self, caplog):
        """Test filter generation with logic expression."""
        filter_obj = ModelFilter(
            'TestProcessor.Filter.TestModelXYZ',
            field1='value1',
            field2='value2',
            field3='value3',
        )
        with caplog.at_level(logging.WARNING):
            result = filter_obj.filter()

        assert result
        assert 'Unable to generate the filter. Did you bind the filter to the model?' in caplog.text

    @patch('mafw.db.db_filter.mafw_model_register')
    def test_filter_with_autobind(self, mock_register, caplog):
        """Test filter generation with logic expression."""
        MockModel = MagicMock(spec=peewee.Model)
        mock_register.get_model = Mock(return_value=MockModel)

        filter_obj = ModelFilter(
            'TestProcessor.Filter.TestModel123',
            field1='value1',
            field2='value2',
            field3='value3',
        )
        assert filter_obj.is_bound

    def test_filter_without_logic_expression_with_and(self):
        """Test filter generation with logic expression."""
        filter_obj = ModelFilter(
            'TestProcessor.Filter.TestModel',
            field1='value1',
            field2='value2',
            field3='value3',
        )
        mock_model = Mock()
        filter_obj.bind(mock_model)

        # Mock the node expressions
        mock_node1 = Mock()
        mock_node2 = Mock()
        mock_node3 = Mock()
        mock_node1.to_expression.return_value = 1
        mock_node2.to_expression.return_value = 1
        mock_node3.to_expression.return_value = 0
        filter_obj._nodes['field1'] = mock_node1
        filter_obj._nodes['field2'] = mock_node2
        filter_obj._nodes['field3'] = mock_node3

        result = filter_obj.filter()
        assert not result

    def test_filter_without_logic_expression_with_or(self):
        """Test filter generation with logic expression."""
        filter_obj = ModelFilter(
            'TestProcessor.Filter.TestModel',
            field1='value1',
            field2='value2',
            field3='value3',
        )
        mock_model = Mock()
        filter_obj.bind(mock_model)

        # Mock the node expressions
        mock_node1 = Mock()
        mock_node2 = Mock()
        mock_node3 = Mock()
        mock_node1.to_expression.return_value = 0
        mock_node2.to_expression.return_value = 0
        mock_node3.to_expression.return_value = 1
        filter_obj._nodes['field1'] = mock_node1
        filter_obj._nodes['field2'] = mock_node2
        filter_obj._nodes['field3'] = mock_node3

        result = filter_obj.filter(join_with='OR')
        assert result

    def test_filter_without_logic_expression_with_not_implemented(self):
        """Test filter generation with logic expression."""
        filter_obj = ModelFilter(
            'TestProcessor.Filter.TestModel',
            field1='value1',
            field2='value2',
            field3='value3',
        )
        mock_model = Mock()
        filter_obj.bind(mock_model)

        # Mock the node expressions
        mock_node1 = Mock()
        mock_node2 = Mock()
        mock_node3 = Mock()
        mock_node1.to_expression.return_value = 0
        mock_node2.to_expression.return_value = 0
        mock_node3.to_expression.return_value = 1
        filter_obj._nodes['field1'] = mock_node1
        filter_obj._nodes['field2'] = mock_node2
        filter_obj._nodes['field3'] = mock_node3

        with pytest.raises(ValueError, match="join_with must be 'AND' or 'OR'"):
            filter_obj.filter(join_with='XOR')

    def test_filter_without_logic_expression_with_no_expressions(self):
        """Test filter generation with logic expression."""
        filter_obj = ModelFilter('TestProcessor.Filter.TestModel')
        mock_model = Mock()
        filter_obj.bind(mock_model)

        assert filter_obj.filter()

    def test_filter_with_logic_expression(self):
        """Test filter generation with logic expression."""
        filter_obj = ModelFilter(
            'TestProcessor.Filter.TestModel',
            field1='value1',
            field2='value2',
            field3='value3',
            __logic__='field1 AND field2 OR NOT field3',
        )
        mock_model = Mock()
        filter_obj.bind(mock_model)

        # Mock the node expressions
        mock_node1 = Mock()
        mock_node2 = Mock()
        mock_node3 = Mock()
        mock_node1.to_expression.return_value = 1
        mock_node2.to_expression.return_value = 1
        mock_node3.to_expression.return_value = 1
        filter_obj._nodes['field1'] = mock_node1
        filter_obj._nodes['field2'] = mock_node2
        filter_obj._nodes['field3'] = mock_node3

        result = filter_obj.filter()
        assert result


class TestProcessorFilter:
    """Test ProcessorFilter functionality."""

    def test_init(self):
        """Test ProcessorFilter initialization."""
        pf = ProcessorFilter()
        assert isinstance(pf, UserDict)
        assert pf._global_filter == {}

    def test_new_only_property(self):
        """Test new_only property."""
        pf = ProcessorFilter()
        assert pf.new_only is True
        pf.new_only = False
        assert pf.new_only is False

    def test_setitem_filter_validation(self):
        """Test setitem with non-Filter value."""
        pf = ProcessorFilter()
        pf['test'] = 'not_a_filter'
        assert 'test' not in pf

    def test_bind_all_with_list(self):
        """Test bind_all with list of models."""

        class Model1(peewee.Model):
            pass

        class Model2(peewee.Model):
            pass

        models = [Model1, Model2]
        pf = ProcessorFilter()
        pf['Model1'] = ModelFilter('TestProcessor.Filter.Model1')
        pf['Model2'] = ModelFilter('TestProcessor.Filter.Model2')

        pf.bind_all(models)
        assert pf['Model1'].is_bound
        assert pf['Model2'].is_bound

    def test_bind_all_with_dict(self):
        """Test bind_all with dictionary of models."""

        class Model1(peewee.Model):
            pass

        class Model2(peewee.Model):
            pass

        models = {'Model1': Model1, 'Model2': Model2}
        pf = ProcessorFilter()
        pf['Model1'] = ModelFilter('TestProcessor.Filter.Model1')
        pf['Model2'] = ModelFilter('TestProcessor.Filter.Model2')

        pf.bind_all(models)
        assert pf['Model1'].is_bound
        assert pf['Model2'].is_bound

    def test_bind_all_missing_filter(self):
        """Test bind_all creates missing filter with default."""

        class Model1(peewee.Model):
            pass

        class Model2(peewee.Model):
            pass

        models = {'Model1': Model1, 'Model2': Model2}
        pf = ProcessorFilter()
        pf._global_filter = {'new_only': False}
        pf['Model1'] = ModelFilter('TestProcessor.Filter.Model1')

        pf.bind_all(models)
        assert 'Model2' in pf
        assert pf['Model2'].is_bound
        assert pf.new_only is False

    def test_filter_all_with_logic(self):
        """Test filter_all with logic expression."""
        pf = ProcessorFilter()
        pf._logic = 'filter1 AND filter2 OR NOT filter3'
        filter1 = MagicMock(spec=ModelFilter)
        filter2 = MagicMock(spec=ModelFilter)
        filter3 = MagicMock(spec=ModelFilter)
        filter1.filter.return_value = 1
        filter2.filter.return_value = 1
        filter3.filter.return_value = 0
        pf['filter1'] = filter1
        pf['filter2'] = filter2
        pf['filter3'] = filter3

        result = pf.filter_all()
        assert result

    def test_filter_all_with_logic_and_unknown_field(self):
        """Test filter_all with logic expression."""
        pf = ProcessorFilter()
        pf._logic = 'filterAAA AND filter2 OR NOT filter3'
        filter1 = MagicMock(spec=ModelFilter)
        filter2 = MagicMock(spec=ModelFilter)
        filter3 = MagicMock(spec=ModelFilter)
        filter1.filter.return_value = 1
        filter2.filter.return_value = 1
        filter3.filter.return_value = 0
        pf['filter1'] = filter1
        pf['filter2'] = filter2
        pf['filter3'] = filter3

        with pytest.raises(
            ValueError, match='Error evaluating processor logic: "Unknown filter name \'filterAAA\' in processor logic"'
        ):
            pf.filter_all()

    def test_filter_all_with_logic_and_unbound_filter(self, caplog):
        """Test filter_all with logic expression."""
        pf = ProcessorFilter()
        pf._logic = 'filter1 AND filter2 OR NOT filter3'
        filter1 = MagicMock(spec=ModelFilter)
        filter1.is_bound = False
        filter2 = MagicMock(spec=ModelFilter)
        filter3 = MagicMock(spec=ModelFilter)
        filter1.filter.return_value = 0
        filter2.filter.return_value = 1
        filter3.filter.return_value = 0
        pf['filter1'] = filter1
        pf['filter2'] = filter2
        pf['filter3'] = filter3

        with caplog.at_level(logging.WARNING):
            result = pf.filter_all()

        assert result
        assert 'is not bound; using True for its expression' in caplog.text

    def test_filter_all_legacy_behavior(self):
        """Test filter_all with legacy behavior."""
        pf = ProcessorFilter()
        filter1 = MagicMock(spec=ModelFilter)
        filter2 = MagicMock(spec=ModelFilter)
        filter1.filter.return_value = 1
        filter2.filter.return_value = 0
        pf['filter1'] = filter1
        pf['filter2'] = filter2

        result = pf.filter_all(join_with='AND')
        assert not result

    def test_filter_all_legacy_behavior_with_or(self):
        """Test filter_all with legacy behavior."""
        pf = ProcessorFilter()
        filter1 = MagicMock(spec=ModelFilter)
        filter2 = MagicMock(spec=ModelFilter)
        filter1.filter.return_value = 1
        filter2.filter.return_value = 0
        pf['filter1'] = filter1
        pf['filter2'] = filter2

        result = pf.filter_all(join_with='OR')
        assert result

    def test_filter_all_with_false_logic(self):
        """Test filter_all with logic expression."""
        pf = ProcessorFilter()
        pf._logic = 'filter NAND filter2 OR NOT filter3'
        filter1 = MagicMock(spec=ModelFilter)
        filter2 = MagicMock(spec=ModelFilter)
        filter3 = MagicMock(spec=ModelFilter)
        filter1.filter.return_value = 1
        filter2.filter.return_value = 1
        filter3.filter.return_value = 0
        pf['filter1'] = filter1
        pf['filter2'] = filter2
        pf['filter3'] = filter3

        with pytest.raises(ValueError, match='Error parsing global logic for ProcessorFilter'):
            pf.filter_all()

    def test_filter_all_with_false_logic2(self):
        """Test filter_all with logic expression."""
        pf = ProcessorFilter()
        pf._logic = 'filter AND filter2 OR NOT filter3'
        filter1 = MagicMock(spec=ModelFilter)
        filter2 = MagicMock(spec=ModelFilter)
        filter3 = MagicMock(spec=ModelFilter)
        filter1.filter.return_value = 1
        filter2.filter.return_value = 1
        filter3.filter.return_value = 0
        pf['filter1'] = filter1
        pf['filter2'] = filter2
        pf['filter3'] = filter3

        with (
            patch.object(mafw.db.db_filter.ExprParser, 'parse', return_value=('NAND', ('a', 'b'))),
            pytest.raises(ValueError, match='Unsupported AST node NAND'),
        ):
            pf.filter_all()
