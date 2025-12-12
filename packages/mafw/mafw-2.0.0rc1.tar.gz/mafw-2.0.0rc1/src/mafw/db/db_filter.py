#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Database filter module for MAFW.

This module provides classes and utilities for creating and managing database filters
using Peewee ORM. It supports various filtering operations including simple conditions,
logical combinations, and conditional filters where one field's criteria depend on another.

The module implements a flexible filter system that can handle:
    - Simple field comparisons (equality, inequality, greater/less than, etc.)
    - Complex logical operations (AND, OR, NOT)
    - Conditional filters with dependent criteria
    - Nested logical expressions
    - Support for various data types and operations

Key components include:
    - :class:`FilterNode`: Abstract base class for filter nodes
    - :class:`ConditionNode`: Represents individual field conditions
    - :class:`LogicalNode`: Combines filter nodes with logical operators
    - :class:`ConditionalNode`: Wraps conditional filter conditions
    - :class:`ModelFilter`: Main class for building and applying filters to models
    - :class:`ProcessorFilter`: Container for multiple model filters in a processor

The module uses a hierarchical approach to build filter expressions that can be converted
into Peewee expressions for database queries. It supports both simple and complex filtering
scenarios through a combination of direct field conditions and logical expressions.

.. versionchanged:: v2.0.0
   Major overhaul introducing conditional filters and logical expression support.

Example usage::

    from mafw.db.db_filter import ModelFilter

    # Create a simple filter
    flt = ModelFilter(
        'Processor.__filter__.Model',
        field1='value1',
        field2={'op': 'IN', 'value': [1, 2, 3]},
    )

    # Bind to a model and generate query
    flt.bind(MyModel)
    query = MyModel.select().where(flt.filter())

.. seealso::

   :link:`peewee` - The underlying ORM library used for database operations

   :class:`~.mafw.enumerators.LogicalOp` - Logical operation enumerations used in filters
"""

import logging
import operator
import re
from collections import OrderedDict, UserDict
from copy import copy
from functools import reduce
from typing import TYPE_CHECKING, Any, Dict, Literal, Self, TypeAlias, Union, cast

import peewee
from peewee import Model

from mafw.db.db_model import mafw_model_register
from mafw.enumerators import LogicalOp

log = logging.getLogger(__name__)


Token = tuple[str, str]
"""Type definition for a logical expression token"""

# 1. An atom is a tuple of the literal string 'NAME' and the value
NameNode = tuple[Literal['NAME'], str]
"""An atom is a tuple of the literal string 'NAME' and the value"""

# 2. A NOT node is a tuple of 'NOT' and a recursive node
# We use a string forward reference 'ExprNode' because it is defined below
NotNode = tuple[Literal['NOT'], 'ExprNode']
"""A NOT node is a tuple of 'NOT' and a recursive node"""

# 3. AND/OR nodes are tuples of the operator and two recursive nodes
BinaryNode = tuple[Literal['AND', 'OR'], 'ExprNode', 'ExprNode']
"""AND/OR nodes are tuples of the operator and two recursive nodes"""

# 4. The main recursive type combining all options
ExprNode: TypeAlias = Union[NameNode, NotNode, BinaryNode]
"""
The main recursive type combining all options

This type represents the abstract syntax tree (AST) nodes used in logical expressions.
It can be one of:

    - :data:`NameNode`: A named element (field name or filter name)
    - :data:`NotNode`: A negation operation
    - :data:`BinaryNode`: An AND/OR operation between two nodes
"""

TOKEN_SPECIFICATION = [
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('AND', r'\bAND\b'),
    ('OR', r'\bOR\b'),
    ('NOT', r'\bNOT\b'),
    ('NAME', r'[A-Za-z_][A-Za-z0-9_\.]*(?:\:[A-Za-z_][A-Za-z0-9_]*)?'),
    ('SKIP', r'[ \t\n\r]+'),
    ('MISMATCH', r'.'),
]
"""Token specifications"""

MASTER_RE = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPECIFICATION))
"""Compiled regular expression to interpret the logical expression grammar"""


class ParseError(ValueError):
    """
    Exception raised when parsing a logical expression fails.

    This exception is raised when the parser encounters invalid syntax
    in a logical expression string.
    """

    pass


def tokenize(text: str) -> list[Token]:
    """
    Tokenize a logical expression string into a list of tokens.

    This function breaks down a logical expression string into individual
    tokens based on the defined token specifications. It skips whitespace
    and raises a :exc:`ParseError` for unexpected characters.

    :param text: The logical expression string to tokenize
    :type text: str
    :return: A list of tokens represented as (token_type, token_value) tuples
    :rtype: list[:data:`Token`]
    :raises ParseError: If an unexpected character is encountered in the text
    """
    tokens: list[Token] = []
    for mo in MASTER_RE.finditer(text):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise ParseError(f'Unexpected character {value!r}')
        else:
            if TYPE_CHECKING:
                assert kind is not None
            tokens.append((kind, value))
    return tokens


class ExprParser:
    """
    Recursive descent parser producing a simple Abstract Syntax Tree (AST).

    The parser handles logical expressions with the following grammar:

    .. code-block:: none

        expr    := or_expr
        or_expr := and_expr ("OR" and_expr)*
        and_expr:= not_expr ("AND" not_expr)*
        not_expr:= "NOT" not_expr | atom
        atom    := NAME | "(" expr ")"

    AST nodes are tuples representing different constructs:

    - ("NAME", "token"): A named element (field name or filter name)
    - ("NOT", node): A negation operation
    - ("AND", left, right): An AND operation between two nodes
    - ("OR", left, right): An OR operation between two nodes

    .. versionadded:: v2.0.0
    """

    def __init__(self, text: str) -> None:
        """
        Initialize the expression parser with a logical expression string.

        :param text: The logical expression to parse
        :type text: str
        """
        self.tokens = tokenize(text)
        self.pos = 0

    def peek(self) -> Token | None:
        """
        Peek at the next token without consuming it.

        :return: The next token if available, otherwise None
        :rtype: :data:`Token` | None
        """
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def accept(self, *kinds: str) -> Token | None:
        """
        Accept and consume the next token if it matches one of the given types.

        :param kinds: Token types to accept
        :type kinds: str
        :return: The consumed token if matched, otherwise None
        :rtype: :data:`Token`  | None
        """
        tok = self.peek()
        if tok and tok[0] in kinds:
            self.pos += 1
            return tok
        return None

    def expect(self, kind: str) -> 'Token':
        """
        Expect and consume a specific token type.

        :param kind: The expected token type
        :type kind: str
        :return: The consumed token
        :rtype: :data:`Token`
        :raises ParseError: If the expected token is not found
        """
        tok = self.accept(kind)
        if not tok:
            raise ParseError(f'Expected {kind} at position {self.pos}')
        return tok

    def parse(self) -> 'ExprNode':
        """
        Parse the entire logical expression and return the resulting AST.

        :return: The abstract syntax tree representation of the expression
        :rtype: :data:`ExprNode`
        :raises ParseError: If the expression is malformed
        """
        node = self.parse_or()
        if self.pos != len(self.tokens):
            raise ParseError('Unexpected token after end of expression')
        return node

    def parse_or(self) -> 'ExprNode':
        """
        Parse an OR expression.

        :return: The parsed OR expression AST node
        :rtype: :data:`ExprNode`
        """
        left = self.parse_and()
        while self.accept('OR'):
            right = self.parse_and()
            left = ('OR', left, right)
        return left

    def parse_and(self) -> 'ExprNode':
        """
        Parse an AND expression.

        :return: The parsed AND expression AST node
        :rtype: :data:`ExprNode`
        """
        left = self.parse_not()
        while self.accept('AND'):
            right = self.parse_not()
            left = ('AND', left, right)
        return left

    def parse_not(self) -> 'ExprNode':
        """
        Parse a NOT expression.

        :return: The parsed NOT expression AST node
        :rtype: :data:`ExprNode`
        """
        if self.accept('NOT'):
            node = self.parse_not()
            return 'NOT', node
        return self.parse_atom()

    def parse_atom(self) -> 'ExprNode':
        """
        Parse an atomic expression (NAME or parenthesised expression).

        :return: The parsed atomic expression AST node
        :rtype: :data:`ExprNode`
        :raises ParseError: If an unexpected token is encountered
        """
        tok = self.peek()
        if not tok:
            raise ParseError('Unexpected end of expression')
        if tok[0] == 'LPAREN':
            self.accept('LPAREN')
            node = self.parse_or()
            self.expect('RPAREN')
            return node
        elif tok[0] == 'NAME':
            self.accept('NAME')
            return 'NAME', tok[1]
        else:
            raise ParseError(f'Unexpected token {tok} at position {self.pos}')


class FilterNode:
    """Abstract base for nodes."""

    def to_expression(self, model: type[Model]) -> peewee.Expression | bool:
        raise NotImplementedError  # pragma: no cover


class ConditionNode(FilterNode):
    """
    Represents a single condition node in a filter expression.

    This class encapsulates a single filtering condition that can be applied
    to a model field. It supports various logical operations through the
    :class:`.LogicalOp` enumerator or string representations of operations.

    .. versionadded:: v2.0.0
    """

    def __init__(self, field: str | None, operation: LogicalOp | str, value: Any, name: str | None = None):
        """
        Initialize a condition node.

        :param field: The name of the field to apply the condition to.
        :type field: str | None
        :param operation: The logical operation to perform.
        :type operation: LogicalOp | str
        :param value: The value to compare against.
        :type value: Any
        :param name: Optional name for this condition node.
        :type name: str | None, Optional
        """
        self.field = field  # may be None for some special nodes
        if isinstance(operation, str):
            try:
                self.operation = LogicalOp(operation)
            except ValueError:
                raise ValueError(f'Unsupported operation: {operation}')
        else:
            self.operation = operation
        self.value = value
        self.name = name

    def to_expression(self, model: type[Model]) -> peewee.Expression:
        """
        Convert this condition node to a Peewee expression.

        This method translates the condition represented by this node into
        a Peewee expression that can be used in database queries.

        :param model: The model class containing the field to filter.
        :type model: type[Model]
        :return: A Peewee expression representing this condition.
        :rtype: peewee.Expression
        :raises RuntimeError: If the node has no field to evaluate.
        :raises ValueError: If an unsupported operation is specified.
        :raises TypeError: If operation requirements are not met (e.g., IN operation requires list/tuple).
        """
        if self.field is None:
            # Should not happen for standard ConditionNode
            raise RuntimeError('ConditionNode has no field to evaluate')
        model_field = getattr(model, self.field)
        op = self.operation
        val = self.value
        # the code is full of cast and redundant checks to make mypy happy.
        # I do not know to which extent they make the code safer, but for sure they make it less readable.
        if op == LogicalOp.EQ:
            return cast(peewee.Expression, cast(object, model_field == val))
        elif op == LogicalOp.NE:
            return cast(peewee.Expression, cast(object, model_field != val))
        elif op == LogicalOp.LT:
            return cast(peewee.Expression, cast(object, model_field < val))
        elif op == LogicalOp.LE:
            return cast(peewee.Expression, cast(object, model_field <= val))
        elif op == LogicalOp.GT:
            return cast(peewee.Expression, cast(object, model_field > val))
        elif op == LogicalOp.GE:
            return cast(peewee.Expression, cast(object, model_field >= val))
        elif op == LogicalOp.GLOB:
            return cast(peewee.Expression, model_field % val)
        elif op == LogicalOp.LIKE:
            return cast(peewee.Expression, model_field**val)
        elif op == LogicalOp.REGEXP:
            if hasattr(model_field, 'regexp') and callable(getattr(model_field, 'regexp')):
                return cast(peewee.Expression, getattr(model_field, 'regexp')(val))
            else:
                raise ValueError(f'REGEXP operation not supported for field type {type(model_field)}')
        elif op == LogicalOp.IN:
            if not isinstance(val, (list, tuple)):
                raise TypeError(f'IN operation requires list/tuple, got {type(val)}')
            if hasattr(model_field, 'in_') and callable(getattr(model_field, 'in_')):
                return cast(peewee.Expression, getattr(model_field, 'in_')(val))
            else:
                raise ValueError(f'IN operation not supported for field type {type(model_field)}')
        elif op == LogicalOp.NOT_IN:
            if not isinstance(val, (list, tuple)):
                raise TypeError(f'NOT_IN operation requires list/tuple, got {type(val)}')
            if hasattr(model_field, 'not_in') and callable(getattr(model_field, 'not_in')):
                return cast(peewee.Expression, getattr(model_field, 'not_in')(val))
            else:
                raise ValueError(f'NOT_IN operation not supported for field type {type(model_field)}')
        elif op == LogicalOp.BETWEEN:
            if not isinstance(val, (list, tuple)) or len(val) != 2:
                raise TypeError(f'BETWEEN operation requires list/tuple of 2 elements, got {val}')
            if hasattr(model_field, 'between') and callable(getattr(model_field, 'between')):
                return cast(peewee.Expression, getattr(model_field, 'between')(val[0], val[1]))
            else:
                raise ValueError(f'BETWEEN operation not supported for field type {type(model_field)}')
        elif op == LogicalOp.BIT_AND:
            if hasattr(model_field, 'bin_and') and callable(getattr(model_field, 'bin_and')):
                return cast(peewee.Expression, cast(object, getattr(model_field, 'bin_and')(val) != 0))
            else:
                raise ValueError(f'BIT_AND operation not supported for field type {type(model_field)}')
        elif op == LogicalOp.BIT_OR:
            if hasattr(model_field, 'bin_or') and callable(getattr(model_field, 'bin_or')):
                return cast(peewee.Expression, cast(object, getattr(model_field, 'bin_or')(val) != 0))
            else:
                raise ValueError(f'BIT_OR operation not supported for field type {type(model_field)}')
        elif op == LogicalOp.IS_NULL:
            return cast(peewee.Expression, model_field.is_null())
        elif op == LogicalOp.IS_NOT_NULL:
            return cast(peewee.Expression, model_field.is_null(False))
        else:
            raise ValueError(f'Unsupported operation: {op}')


class ConditionalNode(FilterNode):
    """
    Wraps :class:`ConditionalFilterCondition` behaviour as a :class:`FilterNode`.

    This class serves as an adapter to integrate conditional filter conditions
    into the filter node hierarchy, allowing them to be treated uniformly with
    other filter nodes during expression evaluation.

    .. versionadded:: v2.0.0
    """

    def __init__(self, conditional: 'ConditionalFilterCondition', name: str | None = None):
        """
        Initialize a conditional node.

        :param conditional: The conditional filter condition to wrap
        :type conditional: ConditionalFilterCondition
        :param name: Optional name for this conditional node
        :type name: str | None, Optional
        """
        self.conditional = conditional
        self.name = name

    def to_expression(self, model: type[Model]) -> peewee.Expression:
        """
        Convert this conditional node to a Peewee expression.

        This method delegates the conversion to the wrapped conditional filter
        condition's :meth:`to_expression` method.

        :param model: The model class to generate the expression for
        :type model: type[Model]
        :return: A Peewee expression representing this conditional node
        :rtype: peewee.Expression
        """
        return self.conditional.to_expression(model)


class LogicalNode(FilterNode):
    """
    Logical combination of child nodes.

    This class represents logical operations (AND, OR, NOT) applied to filter nodes.
    It enables building complex filter expressions by combining simpler filter nodes
    with logical operators.

    .. versionadded:: v2.0.0
    """

    def __init__(self, op: str, *children: FilterNode):
        """
        Initialize a logical node.

        :param op: The logical operation ('AND', 'OR', 'NOT')
        :type op: str
        :param children: Child filter nodes to combine with the logical operation
        :type children: FilterNode
        """
        self.op = op  # 'AND', 'OR', 'NOT'
        self.children = list(children)

    def to_expression(self, model: type[Model]) -> peewee.Expression | bool:
        """
        Convert this logical node to a Peewee expression.

        This method evaluates the logical operation on the child nodes and returns
        the corresponding Peewee expression.

        :param model: The model class to generate the expression for
        :type model: type[Model]
        :return: A Peewee expression representing this logical node
        :rtype: peewee.Expression | bool
        :raises ValueError: If an unknown logical operation is specified
        """
        if self.op == 'NOT':
            assert len(self.children) == 1
            inner = self.children[0].to_expression(model)
            return cast(peewee.Expression, ~inner)
        elif self.op == 'AND':
            expressions = [c.to_expression(model) for c in self.children]
            return cast(peewee.Expression, reduce(operator.and_, expressions))
        elif self.op == 'OR':
            expressions = [c.to_expression(model) for c in self.children]
            return cast(peewee.Expression, reduce(operator.or_, expressions))
        else:
            raise ValueError(f'Unknown logical op: {self.op}')


class ConditionalFilterCondition:
    """
    Represents a conditional filter where one field's criteria depends on another.

    This allows expressing logic like:
    "IF field_a IN [x, y] THEN field_b IN [1, 2] ELSE no constraint on field_b"

    Example usage:

    .. code-block:: python

        # Filter: sample_id in [1,2] if composite_image_id in [100,101]
        condition = ConditionalFilterCondition(
            condition_field='composite_image_id',
            condition_op='IN',
            condition_value=[100, 101],
            then_field='sample_id',
            then_op='IN',
            then_value=[1, 2],
        )

        # This generates:
        # WHERE (composite_image_id IN (100, 101) AND sample_id IN (1, 2))
        #    OR (composite_image_id NOT IN (100, 101))
    """

    def __init__(
        self,
        condition_field: str,
        condition_op: str | LogicalOp,
        condition_value: Any,
        then_field: str,
        then_op: str | LogicalOp,
        then_value: Any,
        else_field: str | None = None,
        else_op: str | LogicalOp | None = None,
        else_value: Any | None = None,
        name: str | None = None,
    ) -> None:
        """
        Initialise a conditional filter condition.

        :param condition_field: The field to check for the condition
        :type condition_field: str
        :param condition_op: The operation for the condition (e.g., 'IN', '==')
        :type condition_op: str | LogicalOp
        :param condition_value: The value(s) for the condition
        :type condition_value: Any
        :param then_field: The field to filter when condition is true
        :type then_field: str
        :param then_op: The operation to apply when condition is true
        :type then_op: str | LogicalOp
        :param then_value: The value(s) for the then clause
        :type then_value: Any
        :param else_field: Optional field to filter when condition is false
        :type else_field: str | None
        :param else_op: Optional operation when condition is false
        :type else_op: str | LogicalOp | None
        :param else_value: Optional value(s) for the else clause
        :type else_value: Any | None
        :param name: The name of this condition. Avoid name clashing with model fields. Defaults to None
        :type name: str | None, Optional
        """
        self.condition_field = condition_field
        self.condition_op = condition_op
        self.condition_value = condition_value
        self.then_field = then_field
        self.then_op = then_op
        self.then_value = then_value
        self.else_field = else_field
        self.else_op = else_op
        self.else_value = else_value
        self.name = name

    def to_expression(self, model: type[Model]) -> peewee.Expression:
        """
        Convert this conditional filter to a Peewee expression.

        The resulting expression is:
        (condition AND then_constraint) OR (NOT condition AND else_constraint)

        Which logically means:

        - When condition is true, apply then_constraint
        - When condition is false, apply else_constraint (or no constraint)

        :param model: The model class containing the fields
        :type model: type[Model]
        :return: A Peewee expression
        :rtype: peewee.Expression
        """
        # Build the condition expression
        condition_expr = ConditionNode(self.condition_field, self.condition_op, self.condition_value).to_expression(
            model
        )

        # Build the then expression
        then_expr = ConditionNode(self.then_field, self.then_op, self.then_value).to_expression(model)

        # Build the else expression
        if self.else_field is not None and self.else_op is not None:
            else_expr = ConditionNode(self.else_field, self.else_op, self.else_value).to_expression(model)
        else:
            # No constraint in else clause - always true
            # the nested cast is needed to make mypy happy.
            else_expr = cast(peewee.Expression, cast(object, True))

        # Combine: (condition AND then) OR (NOT condition AND else)
        return cast(peewee.Expression, (condition_expr & then_expr) | (~condition_expr & else_expr))

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ConditionalFilterCondition):
            return False

        return vars(self) == vars(other)


class ModelFilter:
    r"""
    Class to filter rows from a model.

    The filter object can be used to generate a where clause to be applied to Model.select().

    The construction of a ModelFilter is normally done via a configuration file using the :meth:`from_conf` class method.
    The name of the filter is playing a key role in this. If it follows a dot structure like:

        *ProcessorName.__filter__.ModelName*

    then the corresponding table from the TOML configuration object will be used.

    For each processor, there might be many Filters, up to one for each Model used to get the input list. If a
    processor is joining together three Models when performing the input select, there will be up to three Filters
    collaborating on making the selection.

    The filter configuration can contain the following key, value pair:

        - key / string pairs, where the key is the name of a field in the corresponding Model

        - key / numeric pairs

        - key / arrays

        - key / dict pairs with 'op' and 'value' keys for explicit operation specification

    All fields from the configuration file will be added to the instance namespace, thus accessible with the dot
    notation. Moreover, the field names and their filter value will be added to a private dictionary to simplify the
    generation of the filter SQL code.

    The user can use the filter object to store selection criteria. He can construct queries using the filter
    contents in the same way as he could use processor parameters.

    If he wants to automatically generate valid filtering expression, he can use the :meth:`filter` method. In order
    for this to work, the ModelFilter object be :meth:`bound <bind>` to a Model. Without this binding the ModelFilter will not
    be able to automatically generate expressions.

    For each field in the filter, one condition will be generated according to the following scheme:

    =================   =================   ==================
    Filter field type   Logical operation      Example
    =================   =================   ==================
    Numeric, boolean        ==               Field == 3.14
    String                 GLOB             Field GLOB '\*ree'
    List                   IN               Field IN [1, 2, 3]
    Dict (explicit)     op from dict         Field BIT_AND 5
    =================   =================   ==================

    All conditions will be joined with a AND logic by default, but this can be changed.

    The ModelFilter also supports logical expressions to combine multiple filter conditions using AND, OR, and NOT
    operators. These expressions can reference named filter conditions within the same filter or even combine
    conditions from different filters when used with :class:`ProcessorFilter`.

    Conditional filters allow expressing logic like:
    "IF field_a IN [x, y] THEN field_b IN [1, 2] ELSE no constraint on field_b"

    Consider the following example:

    .. code-block:: python
        :linenos:

        class MeasModel(MAFwBaseModel):
            meas_id = AutoField(primary_key=True)
            sample_name = TextField()
            successful = BooleanField()
            flags = IntegerField()
            composite_image_id = IntegerField()
            sample_id = IntegerField()


        # Traditional simplified usage
        flt = ModelFilter(
            'MyProcessor.__filter__.MyModel',
            sample_name='sample_00*',
            meas_id=[1, 2, 3],
            successful=True,
        )

        # New explicit operation usage
        flt = ModelFilter(
            'MyProcessor.__filter__.MyModel',
            sample_name={'op': 'LIKE', 'value': 'sample_00%'},
            flags={'op': 'BIT_AND', 'value': 5},
            meas_id={'op': 'IN', 'value': [1, 2, 3]},
        )

        # Logical expression usage
        flt = ModelFilter(
            'MyProcessor.__filter__.MyModel',
            sample_name={'op': 'LIKE', 'value': 'sample_00%'},
            flags={'op': 'BIT_AND', 'value': 5},
            meas_id={'op': 'IN', 'value': [1, 2, 3]},
            __logic__='sample_name AND (flags OR meas_id)',
        )

        # Conditional filter usage
        flt = ModelFilter(
            'MyProcessor.__filter__.MyModel',
            sample_name='sample_00*',
            composite_image_id=[100, 101],
            sample_id=[1, 2],
            __conditional__=[
                {
                    'condition_field': 'composite_image_id',
                    'condition_op': 'IN',
                    'condition_value': [100, 101],
                    'then_field': 'sample_id',
                    'then_op': 'IN',
                    'then_value': [1, 2],
                }
            ],
        )

        flt.bind(MeasModel)
        filtered_query = MeasModel.select().where(flt.filter())

    The explicit operation format allows for bitwise operations and other advanced filtering.

    TOML Configuration Examples:

    .. code-block:: toml

        [MyProcessor.__filter__.MyModel]
        sample_name = "sample_00*"  # Traditional GLOB
        successful = true           # Traditional equality

        # Explicit operations
        flags = { op = "BIT_AND", value = 5 }
        score = { op = ">=", value = 75.0 }
        category = { op = "IN", value = ["A", "B", "C"] }
        date_range = { op = "BETWEEN", value = ["2024-01-01", "2024-12-31"] }

        # Logical expression for combining conditions
        __logic__ = "sample_name AND (successful OR flags)"

        # Conditional filters
        [[MyProcessor.__filter__.MyModel.__conditional__]]
        condition_field = "composite_image_id"
        condition_op = "IN"
        condition_value = [100, 101]
        then_field = "sample_id"
        then_op = "IN"
        then_value = [1, 2]

        # Nested conditions with logical expressions
        [MyProcessor.__filter__.MyModel.nested_conditions]
        __logic__ = "a OR b"
        a = { op = "LIKE", value = "test%" }
        b = { op = "IN", value = [1, 2, 3] }

    .. seealso::

       - :class:`mafw.db.db_filter.ProcessorFilter` - For combining multiple ModelFilters with logical expressions
       - :class:`mafw.db.db_filter.ConditionalFilterCondition` - For conditional filtering logic
       - :class:`mafw.db.db_filter.ExprParser` - For parsing logical expressions
    """

    logic_name = '__logic__'
    """
    The logic keyword identifier.
    
    This value cannot be used as field name in the filter bound model.
    """
    conditional_name = '__conditional__'
    """
    The conditional keyword identifier.
    
    This value cannot be used as field name in the filter bound model.
    """

    def __init__(self, name_: str, **kwargs: Any) -> None:
        """
        Constructor parameters:

        :param `name_`: The name of the filter. It should be in dotted format to facilitate the configuration via the
            steering file. The _ is used to allow the user to have a keyword argument named name.
        :type `name_`: str
        :param kwargs: Keyword parameters corresponding to fields and filter values.

        .. versionchanged:: v1.2.0
           The parameter *name* has been renamed as *name_*.

        .. versionchanged:: v1.3.0
           Implementation of explicit operation.

        .. versionchanged:: v2.0.0
           Introduction of conditional filters, logical expression and hierarchical structure.
           Introduction of autobinding for MAFwBaseModels

        """
        self.name = name_
        self.model_name = name_.split('.')[-1]
        self.model: type[Model] | None = None
        self._model_bound = False

        # attempt to autobind
        self._auto_bind()

        # mapping name -> FilterNode
        self._nodes: 'OrderedDict[str, FilterNode]' = OrderedDict()
        # conditional nodes mapping (named)
        self._cond_nodes: 'OrderedDict[str, ConditionalNode]' = OrderedDict()
        # logic expression for this filter (combining top-level node names)
        self._logic_expr: str | None = None

        # Extract conditional filters if present
        if self.conditional_name in kwargs:
            conditionals = kwargs.pop(self.conditional_name)
            if not isinstance(conditionals, list):
                conditionals = [conditionals]

            for cond_dict in conditionals:
                self.add_conditional_from_dict(cond_dict)

        # Extract logic for internal conditions, if provided
        if self.logic_name in kwargs:
            self._logic_expr = kwargs.pop(self.logic_name)

        # now process remaining kwargs as either:
        # - simple/extended condition for a field
        # - or a nested mapping describing subconditions for field (field-level logic)
        for k, v in kwargs.items():
            # simple types map to ConditionNode
            if isinstance(v, dict) and ('op' in v and 'value' in v):
                # explicit op/value for field k
                # extended operation condition
                node = ConditionNode(k, v['op'], v['value'], name=k)
                self._nodes[k] = node
            elif isinstance(v, dict) and any(
                isinstance(x, dict) or x == self.logic_name or x not in ['op', 'value']
                for x in v.keys()
                if isinstance(v, dict)
            ):
                # nested mapping: create sub-nodes for this field
                # v expected like {'__logic__': 'a OR b', 'a': {'op':..., 'value':...}, 'b': ...}
                subnodes: 'OrderedDict[str, FilterNode]' = OrderedDict()
                sub_logic = v.get(self.logic_name, None)
                for subk, subv in v.items():
                    if subk == self.logic_name:
                        continue
                    if isinstance(subv, dict) and ('op' in subv and 'value' in subv):
                        subnode = ConditionNode(k, subv['op'], subv['value'], name=subk)
                        subnodes[subk] = subnode
                    else:
                        subnodes[subk] = self._create_condition_node_from_value(subv, k, subk)
                # combine subnodes using sub_logic or AND by default
                if sub_logic:
                    ast = ExprParser(sub_logic).parse()
                    ln = self._build_logical_node_from_ast(ast, subnodes, model_name_placeholder=k)
                else:
                    # AND all subnodes
                    ln = LogicalNode('AND', *subnodes.values())
                self._nodes[k] = ln
            else:
                self._nodes[k] = self._create_condition_node_from_value(v, k, k)

    def _auto_bind(self) -> None:
        try:
            model = mafw_model_register.get_model(self.model_name)
            self.bind(model)  # type: ignore[arg-type]
        except KeyError:
            log.warning(f'Impossible to perform auto-binding for model {self.model_name}')

    def _build_logical_node_from_ast(
        self, ast: ExprNode, name_to_nodes: Dict[str, FilterNode], model_name_placeholder: str | None = None
    ) -> FilterNode:
        """Recursively build LogicalNode from AST using a mapping name->FilterNode."""
        t = ast[0]
        if t == 'NAME':
            named_ast = cast(NameNode, ast)
            nm = named_ast[1]
            if nm not in name_to_nodes:
                raise KeyError(f'Unknown name {nm} in nested logic for field {model_name_placeholder}')
            return name_to_nodes[nm]
        elif t == 'NOT':
            not_ast = cast(NotNode, ast)
            child = self._build_logical_node_from_ast(not_ast[1], name_to_nodes, model_name_placeholder)
            return LogicalNode('NOT', child)
        elif t in ('AND', 'OR'):
            bin_ast = cast(BinaryNode, ast)
            left = self._build_logical_node_from_ast(bin_ast[1], name_to_nodes, model_name_placeholder)
            right = self._build_logical_node_from_ast(bin_ast[2], name_to_nodes, model_name_placeholder)
            return LogicalNode(t, left, right)
        else:
            raise ValueError(f'Unsupported AST node {t}')

    @staticmethod
    def _create_condition_node_from_value(value: Any, field_name: str, node_name: str | None = None) -> ConditionNode:
        """
        Create a FilterCondition based on value type (backward compatibility).

        :param value: The filter value
        :param field_name: The field name
        :return: A FilterCondition
        """
        if isinstance(value, (int, float, bool)):
            return ConditionNode(field_name, LogicalOp.EQ, value, node_name)
        elif isinstance(value, str):
            return ConditionNode(field_name, LogicalOp.GLOB, value, node_name)
        elif isinstance(value, list):
            return ConditionNode(field_name, LogicalOp.IN, value, node_name)
        else:
            raise TypeError(f'ModelFilter value of unsupported type {type(value)} for field {field_name}.')

    def bind(self, model: type[Model]) -> None:
        """
        Connects a filter to a Model class.

        :param model: Model to be bound.
        :type model: Model
        """

        self.model = model
        self._model_bound = True

        if hasattr(self.model, self.logic_name) and self._model_bound:
            if TYPE_CHECKING:
                assert self.model is not None

            log.warning(
                f'Model {self.model.__name__} has a field named {self.logic_name}. This is '
                f'preventing the logic expression to work.'
            )
            log.warning('Modify your model. Logic expression disabled.')
            self._logic_expr = None

    @property
    def is_bound(self) -> bool:
        """Returns true if the ModelFilter has been bound to a Model"""
        return self._model_bound

    def add_conditional(self, conditional: ConditionalFilterCondition) -> None:
        """
        Add a conditional filter.

        .. versionadded:: v2.0.0

        :param conditional: The conditional filter condition
        :type conditional: ConditionalFilterCondition
        """
        condition_name = conditional.name
        if condition_name is None:
            # it means that the user did not specify any name for this condition.
            # we will then assign one
            increment = 0
            while True:
                condition_name = f'__cond{increment + len(self._cond_nodes)}__'
                if condition_name not in self._cond_nodes:
                    break
                else:
                    increment += 1
        else:
            # the user specified a name for this condition. we will use it but first we check if it is not yet used
            if condition_name in self._cond_nodes:
                raise KeyError(
                    f'A conditional filter named {condition_name} already exists. Please review your steering file.'
                )

        node = ConditionalNode(conditional, name=condition_name)
        self._cond_nodes[condition_name] = node
        self._nodes[condition_name] = node

    def add_conditional_from_dict(self, config: dict[str, Any]) -> None:
        """
        Add a conditional filter from a configuration dictionary.

        .. versionadded:: v2.0.0

        :param config: Dictionary with conditional filter configuration
        :type config: dict[str, Any]
        """
        conditional = ConditionalFilterCondition(
            condition_field=config['condition_field'],
            condition_op=config['condition_op'],
            condition_value=config['condition_value'],
            then_field=config['then_field'],
            then_op=config['then_op'],
            then_value=config['then_value'],
            else_field=config.get('else_field'),
            else_op=config.get('else_op'),
            else_value=config.get('else_value'),
            name=config.get('name'),
        )
        self.add_conditional(conditional)

    @classmethod
    def from_conf(cls, name: str, conf: dict[str, Any]) -> Self:
        """
        Builds a Filter object from a steering file dictionary.

        If the name is in dotted notation, then this should be corresponding to the table in the configuration file.
        If a default configuration is provided, this will be used as a starting point for the filter, and it will be
        updated by the actual configuration in ``conf``.

        In normal use, you would provide the specific configuration via the conf parameter.

        See details in the :class:`class documentation <ModelFilter>`

        :param name: The name of the filter in dotted notation.
        :type name: str
        :param conf: The configuration dictionary.
        :type conf: dict
        :return: A Filter object
        :rtype: ModelFilter
        """
        param = {}

        # split the name from dotted notation
        # ProcessorName#123.ModelName.Filter
        # the processor name is actually the processor replica name
        names = name.split('.')
        if len(names) == 3 and names[1] == '__filter__':
            proc_name, _, model_name = names
            if proc_name in conf and '__filter__' in conf[proc_name] and model_name in conf[proc_name]['__filter__']:
                param.update(copy(conf[proc_name]['__filter__'][model_name]))

        # if the name is not in the expected dotted notation, the use an empty filter.
        return cls(name, **param)

    def _evaluate_logic_ast(self, ast: ExprNode) -> peewee.Expression | bool:
        """
        Evaluate an abstract syntax tree (AST) representing a logical expression.

        This method recursively evaluates the AST nodes to produce a Peewee expression
        or boolean value representing the logical combination of filter conditions.

        :param ast: The abstract syntax tree node to evaluate
        :type ast: Any
        :return: A Peewee expression for logical operations or boolean True/False
        :rtype: peewee.Expression | bool
        :raises KeyError: If a referenced condition name is not found in the filter
        :raises ValueError: If an unsupported AST node type is encountered
        """
        t = ast[0]
        if t == 'NAME':
            named_ast = cast(NameNode, ast)
            nm = named_ast[1]
            if nm not in self._nodes:
                raise KeyError(f"Unknown node '{nm}' in logic for filter {self.name}")
            node = self._nodes[nm]

            if TYPE_CHECKING:
                assert self.model is not None
            return node.to_expression(self.model)
        elif t == 'NOT':
            not_ast = cast(NotNode, ast)
            val = self._evaluate_logic_ast(not_ast[1])
            return cast(peewee.Expression, ~val)
        elif t == 'AND':
            bin_ast = cast(BinaryNode, ast)
            left = self._evaluate_logic_ast(bin_ast[1])
            right = self._evaluate_logic_ast(bin_ast[2])
            return cast(peewee.Expression, cast(object, left & right))
        elif t == 'OR':
            bin_ast = cast(BinaryNode, ast)
            left = self._evaluate_logic_ast(bin_ast[1])
            right = self._evaluate_logic_ast(bin_ast[2])
            return cast(peewee.Expression, cast(object, left | right))
        else:
            raise ValueError(f'Unsupported AST node {t}')

    def filter(self, join_with: Literal['AND', 'OR'] = 'AND') -> peewee.Expression | bool:
        """
        Generates a filtering expression joining all filtering fields.

        See details in the :class:`class documentation <ModelFilter>`

        .. versionchanged:: v1.3.0
           Add the possibility to specify a `join_with` function

        .. versionchanged:: v2.0.0
           Add support for conditional filters and for logical expression

        :param join_with: How to join conditions ('AND' or 'OR'). Defaults to 'AND'.
        :type join_with: Literal['AND', 'OR'], default 'AND'
        :return: The filtering expression.
        :rtype: peewee.Expression | bool
        :raises TypeError: when the field value type is not supported.
        :raises ValueError: when join_with is not 'AND' or 'OR'.
        """
        if not self.is_bound:
            log.warning('Unable to generate the filter. Did you bind the filter to the model?')
            return True

        if TYPE_CHECKING:
            # if we get here, it means that we have a valid model
            assert self.model is not None

        # if logic provided for this filter, use it
        if self._logic_expr:
            try:
                ast = ExprParser(self._logic_expr).parse()
            except ParseError as e:
                raise ValueError(f'Error parsing logic for filter {self.name}: {e}')
            try:
                return self._evaluate_logic_ast(ast)
            except KeyError as e:
                raise ValueError(f'Error evaluating logic for filter {self.name}: {e}')

        # otherwise combine all top-level nodes (AND by default)
        exprs = [n.to_expression(self.model) for n in self._nodes.values()]
        if not exprs:
            return True
        if join_with not in ('AND', 'OR'):
            raise ValueError("join_with must be 'AND' or 'OR'")
        if join_with == 'AND':
            return cast(peewee.Expression, reduce(operator.and_, exprs))
        return cast(peewee.Expression, reduce(operator.or_, exprs))


class ProcessorFilter(UserDict[str, ModelFilter]):
    """
    A special dictionary to store all :class:`Filters <mafw.db.db_filter.ModelFilter>` in a processors.

    It contains a publicly accessible dictionary with the configuration of each ModelFilter using the Model name as
    keyword.

    It contains a private dictionary with the global filter configuration as well.
    The global filter is not directly accessible, but only some of its members will be exposed via properties.
    In particular, the new_only flag that is relevant only at the Processor level can be accessed directly using the
    :attr:`new_only`. If not specified in the configuration file, the new_only is by default True.

    It is possible to assign a logic operation string to the register that is used to join all the filters together
    when performing the :meth:`filter_all`. If no logic operation string is provided, the register will provide a join
    condition using either AND (default) or OR.
    """

    def __init__(self, data: dict[str, ModelFilter] | None = None, /, **kwargs: Any) -> None:
        """
        Constructor parameters:

        :param data: Initial data
        :type data: dict
        :param kwargs: Keywords arguments
        """
        self._global_filter: dict[str, Any] = {}
        self._logic: str | None = None
        super().__init__(data, **kwargs)

    @property
    def new_only(self) -> bool:
        """
        The new only flag.

        :return: True, if only new items, not already in the output database table must be processed.
        :rtype: bool
        """
        return cast(bool, self._global_filter.get('new_only', True))

    @new_only.setter
    def new_only(self, v: bool) -> None:
        self._global_filter['new_only'] = v

    def __setitem__(self, key: str, value: ModelFilter) -> None:
        """
        Set a new value at key.

        If value is not a Filter, then it will be automatically and silently discarded.

        :param key: Dictionary key. Normally the name of the model linked to the filter.
        :type key: str
        :param value: The Filter.
        :type value: ModelFilter
        """
        if not isinstance(value, ModelFilter):
            return
        super().__setitem__(key, value)

    def bind_all(self, models: list[type[Model]] | dict[str, type[Model]]) -> None:
        """
        Binds all filters to their models.

        The ``models`` list or dictionary should contain a valid model for all the ModelFilters in the registry.
        In the case of a dictionary, the key value should be the model name.

        :param models: List or dictionary of a databank of Models from which the ModelFilter can be bound.
        :type models:  list[type(Model)] | dict[str,type(Model)]
        """
        if isinstance(models, list):
            models = {m.__name__: m for m in models}

        # check, if we have a filter for each listed models, if not create one using the default configuration.
        for model_name in models.keys():
            if model_name not in self.data:
                self.data[model_name] = ModelFilter.from_conf(f'{model_name}', conf={})

        for k, v in self.data.items():
            if k in self.data and k in models and not v.is_bound:
                v.bind(models[k])

    def filter_all(self, join_with: Literal['AND', 'OR'] = 'AND') -> peewee.Expression | bool:
        """
        Generates a where clause joining all filters.

        If a logic expression is present, it will be used to combine named filters.
        Otherwise, fall back to the legacy behaviour using join_with.

        :raise ValueError: If the parsing of the logical expression fails
        :param join_with: Logical function to join the filters if no logic expression is provided.
        :type join_with: Literal['AND', 'OR'], default: 'AND'
        :return: ModelFilter expression
        :rtype: peewee.Expression
        """
        # If a logic expression is present at the global level, use it to combine filters
        if self._logic:
            try:
                ast = ExprParser(self._logic).parse()
            except ParseError as e:
                raise ValueError(f'Error parsing global logic for ProcessorFilter: {e}')

            def eval_ast(node: ExprNode) -> peewee.Expression | bool:
                t = node[0]
                if t == 'NAME':
                    named_node = cast(NameNode, node)
                    nm = named_node[1]
                    if nm not in self.data:
                        raise KeyError(f"Unknown filter name '{nm}' in processor logic")
                    flt = self.data[nm]
                    if not flt.is_bound:
                        log.warning(f"ModelFilter '{nm}' is not bound; using True for its expression")
                        return True
                    return flt.filter()
                elif t == 'NOT':
                    not_node = cast(NotNode, node)
                    return cast(peewee.Expression, ~eval_ast(not_node[1]))
                elif t == 'AND':
                    bin_node = cast(BinaryNode, node)
                    return cast(peewee.Expression, cast(object, eval_ast(bin_node[1]) & eval_ast(bin_node[2])))
                elif t == 'OR':
                    bin_node = cast(BinaryNode, node)
                    return cast(peewee.Expression, cast(object, eval_ast(bin_node[1]) | eval_ast(bin_node[2])))
                else:
                    raise ValueError(f'Unsupported AST node {t}')

            try:
                return eval_ast(ast)
            except KeyError as e:
                raise ValueError(f'Error evaluating processor logic: {e}')

        # Legacy behaviour: combine all filters with join_with (AND/OR)
        filter_list = [flt.filter() for flt in self.data.values() if flt.is_bound]
        if join_with == 'AND':
            return cast(peewee.Expression, cast(object, reduce(operator.and_, filter_list, True)))
        else:
            return cast(peewee.Expression, cast(object, reduce(operator.or_, filter_list, True)))
