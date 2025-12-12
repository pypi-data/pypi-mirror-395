#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
import pytest

from mafw.enumerators import LogicalOp, LoopingStatus, LoopType, ProcessorExitStatus, ProcessorStatus


class TestProcessorExitStatus:
    @pytest.mark.parametrize(
        'status, expected',
        [
            (ProcessorExitStatus.Successful, 'Successful'),
            (ProcessorExitStatus.Failed, 'Failed'),
            (ProcessorExitStatus.Aborted, 'Aborted'),
        ],
    )
    def test_exit_status(self, status, expected):
        assert status.name == expected


class TestProcessorStatus:
    @pytest.mark.parametrize(
        'status, expected',
        [
            (ProcessorStatus.Unknown, 'unknown'),
            (ProcessorStatus.Init, 'initializing'),
            (ProcessorStatus.Start, 'starting'),
            (ProcessorStatus.Run, 'processing'),
            (ProcessorStatus.Finish, 'finishing'),
        ],
    )
    def test_processor_status(self, status, expected):
        assert status.value == expected


class TestLoopingStatus:
    @pytest.mark.parametrize(
        'status, expected',
        [
            (LoopingStatus.Continue, 'Continue'),
            (LoopingStatus.Skip, 'Skip'),
            (LoopingStatus.Abort, 'Abort'),
            (LoopingStatus.Quit, 'Quit'),
        ],
    )
    def test_looping_status(self, status, expected):
        assert status.name == expected


class TestLoopType:
    @pytest.mark.parametrize(
        'loop_type, expected',
        [
            (LoopType.SingleLoop, 'single'),
            (LoopType.ForLoop, 'for_loop'),
            (LoopType.WhileLoop, 'while_loop'),
        ],
    )
    def test_loop_type(self, loop_type, expected):
        assert loop_type.value == expected


class TestLogicalOp:
    """Test cases for the LogicalOp enum."""

    def test_logical_op_values(self):
        """Test LogicalOp enum values."""
        assert LogicalOp.EQ.value == '=='
        assert LogicalOp.NE.value == '!='
        assert LogicalOp.LT.value == '<'
        assert LogicalOp.LE.value == '<='
        assert LogicalOp.GT.value == '>'
        assert LogicalOp.GE.value == '>='
        assert LogicalOp.GLOB.value == 'GLOB'
        assert LogicalOp.LIKE.value == 'LIKE'
        assert LogicalOp.REGEXP.value == 'REGEXP'
        assert LogicalOp.IN.value == 'IN'
        assert LogicalOp.NOT_IN.value == 'NOT_IN'
        assert LogicalOp.BETWEEN.value == 'BETWEEN'
        assert LogicalOp.BIT_AND.value == 'BIT_AND'
        assert LogicalOp.BIT_OR.value == 'BIT_OR'
        assert LogicalOp.IS_NULL.value == 'IS_NULL'
        assert LogicalOp.IS_NOT_NULL.value == 'IS_NOT_NULL'
