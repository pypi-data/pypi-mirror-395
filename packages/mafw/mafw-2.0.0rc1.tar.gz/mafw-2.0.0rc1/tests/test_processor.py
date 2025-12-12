#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
from contextlib import nullcontext as does_not_raise
from copy import deepcopy
from typing import Any, Collection
from unittest.mock import MagicMock, Mock, call, patch

import peewee
import pytest

from mafw.db.std_tables import StandardTable
from mafw.decorators import database_required, single_loop
from mafw.enumerators import LoopingStatus, LoopType, ProcessorExitStatus, ProcessorStatus
from mafw.mafw_errors import AbortProcessorException, MissingDatabase
from mafw.processor import (
    ActiveParameter,
    PassiveParameter,
    Processor,
    ProcessorList,
    ProcessorMeta,
    ProcessorParameterError,
    ensure_parameter_registration,
    validate_database_conf,
)
from mafw.timer import Timer
from mafw.ui.abstract_user_interface import UserInterfaceBase
from mafw.ui.console_user_interface import ConsoleInterface

# -------------------
# Tests for validate_database_conf
# -------------------


class TestValidateDatabaseConf:
    @pytest.mark.parametrize(
        'input_conf,expected',
        [
            (None, None),
            ({}, None),
            ({'DBConfiguration': {'URL': 'sqlite://'}}, {'DBConfiguration': {'URL': 'sqlite://'}}),
            ({'DBConfiguration': {}}, None),
            ({'URL': 'sqlite://'}, {'URL': 'sqlite://'}),
        ],
    )
    def test_validate_database_conf(self, input_conf, expected):
        assert validate_database_conf(input_conf) == expected


# -------------------
# Tests for ensure_parameter_registration
# -------------------


class TestEnsureParameterRegistration:
    @pytest.fixture
    def processor_mock(self):
        @single_loop
        class DummyProcessor(Processor):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self._parameter_registered = False
                self._register_parameters_called = False

            def _register_parameters(self):
                self._parameter_registered = True
                self._register_parameters_called = True

            dummy_param = ActiveParameter('dummy_param', default='default')

        return DummyProcessor()

    def test_register_called_before_decorated_func(self, processor_mock):
        @ensure_parameter_registration
        def dummy_method(self):
            return self._parameter_registered

        result = dummy_method(processor_mock)
        assert result is True
        assert processor_mock._register_parameters_called is True

    def test_decorator_with_invalid_self(self):
        @ensure_parameter_registration
        def bad_func():
            return True

        with pytest.raises(ProcessorParameterError):
            bad_func()

    def test_decorator_with_not_processor(self):
        @ensure_parameter_registration
        def some_function(value: int):
            return value

        with pytest.raises(ProcessorParameterError):
            some_function(15)

    def test_decorator_without_param_registration(self):
        @single_loop
        class MyProcessor(Processor):
            dummy_param = ActiveParameter('dummy_param', default='default')

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                # self._parameter_registered = False
                # self._register_parameters_called = False
                self._something_done = False
                self.do_something()

            @ensure_parameter_registration
            def do_something(self):
                self._something_done = True

        my = MyProcessor()
        assert my._parameter_registered
        assert my._something_done


# -------------------
# Tests for PassiveParameter
# -------------------


class TestPassiveParameter:
    def test_valid_value_and_name(self):
        param = PassiveParameter('param1', value=42)
        assert param.name == 'param1'
        assert param.value == 42
        assert param.is_set is True
        assert param.is_optional is False

    def test_default_only(self):
        param = PassiveParameter('param2', default=3.14)
        assert param.value == 3.14
        assert param.is_set is False
        assert param.is_optional is True

    def test_value_setter(self):
        param = PassiveParameter('param3', default=1)
        param.value = 2
        assert param.value == 2
        assert param.is_set is True

    def test_invalid_name_raises(self):
        with pytest.raises(ProcessorParameterError):
            PassiveParameter('not valid', value=5)

    def test_both_none_raises(self):
        with pytest.raises(ProcessorParameterError):
            PassiveParameter('param4')

    def test_rich_repr_output(self):
        param = PassiveParameter('param_rich', value=10, help_doc='some help')
        rich_output = list(param.__rich_repr__())
        expected_keys = {'name', 'value', 'help_doc'}
        result_keys = {key for key, *_ in rich_output}
        assert expected_keys == result_keys

    def test_repr_output(self):
        param = PassiveParameter('param_repr', value='xyz', help_doc='desc')
        repr_str = repr(param)
        assert 'PassiveParameter(' in repr_str
        assert 'param_repr' in repr_str
        assert 'xyz' in repr_str


# -------------------
# Tests for ActiveParameter
# -------------------


class TestActiveParameter:
    def test_descriptor_behavior(self):
        @single_loop
        class DummyProcessor(Processor):
            test_param = ActiveParameter('test_param', default='abc')

        proc = DummyProcessor()
        assert proc.test_param == 'abc'

        proc.test_param = 'xyz'
        assert proc.test_param == 'xyz'

    def test_passive_parameter_linked(self):
        @single_loop
        class DummyProcessor(Processor):
            p = ActiveParameter('p', default=1)

        proc = DummyProcessor()
        passive = proc.get_parameter('p')
        assert isinstance(passive, PassiveParameter)
        assert passive.value == 1
        assert passive.name == 'p'

    def test_get_returns_descriptor_when_obj_is_none(self):
        """
        Covers the branch where obj is None in __get__, returning the descriptor itself.
        """
        param = ActiveParameter('some_param', default=42)

        result = param.__get__(None, Processor)  # Emulates access via class: MyProcessor.some_param
        assert result is param

    @pytest.mark.parametrize(
        'name, catch',
        [
            ('__logic__', pytest.raises(ProcessorParameterError, match='__logic__')),
            ('__filter__', pytest.raises(ProcessorParameterError, match='__filter')),
            ('__new_only__', pytest.raises(ProcessorParameterError, match='__new_only__')),
            ('__inheritance__', pytest.raises(ProcessorParameterError, match='__inheritance__')),
            ('anything_else', does_not_raise()),
        ],
    )
    def test_name_validation(self, name, catch):
        with catch:
            ActiveParameter(name, default=1)

    def test_reserved_names(self):
        for name in ActiveParameter.reserved_names:
            with pytest.raises(ProcessorParameterError, match=name):
                ActiveParameter(name, default=1)


class TestProcessorMeta:
    """Test cases for ProcessorMeta metaclass."""

    def test_processor_meta_call_creates_instance_with_post_init(self):
        """Test that ProcessorMeta.__call__ creates instance and calls __post_init__."""

        # Create a test class using ProcessorMeta
        class TestProcessor(metaclass=ProcessorMeta):
            def __init__(self):
                self.init_called = True
                self.post_init_called = False

            def __post_init__(self):
                self.post_init_called = True

        # Create instance
        instance = TestProcessor()

        # Verify both init and post_init were called
        assert instance.init_called is True
        assert instance.post_init_called is True
        assert isinstance(instance, TestProcessor)

    def test_processor_meta_call_with_args_kwargs(self):
        """Test ProcessorMeta.__call__ passes args and kwargs correctly."""

        class TestProcessor(metaclass=ProcessorMeta):
            def __init__(self, arg1, arg2, kwarg1=None):
                self.arg1 = arg1
                self.arg2 = arg2
                self.kwarg1 = kwarg1
                self.post_init_called = False

            def __post_init__(self):
                self.post_init_called = True

        instance = TestProcessor('test1', 'test2', kwarg1='test3')

        assert instance.arg1 == 'test1'
        assert instance.arg2 == 'test2'
        assert instance.kwarg1 == 'test3'
        assert instance.post_init_called is True


class TestProcessorInit:
    """Test cases for Processor initialization."""

    @pytest.mark.filterwarnings('ignore:get_items')
    def test_processor_init_defaults(self):
        """Test Processor initialization with default parameters."""
        processor = Processor()

        assert processor.name == 'Processor'
        assert processor.description == 'Processor'
        assert processor.item is None
        assert processor.processor_exit_status == ProcessorExitStatus.Successful
        assert processor.loop_type == LoopType.ForLoop
        assert processor.remove_orphan_files is True
        assert processor._config == {}
        assert processor._kwargs == {}
        assert processor.replica_id is None

    @pytest.mark.parametrize(
        'name,expected_name,expected_desc',
        [
            (None, 'Processor', 'Processor'),
            ('TestProcessor', 'TestProcessor', 'TestProcessor'),
            ('CustomProcessor', 'CustomProcessor', 'CustomProcessor'),
        ],
    )
    @pytest.mark.filterwarnings('ignore:get_items')
    def test_processor_init_name_and_description(self, name, expected_name, expected_desc):
        """Test processor name and description initialization."""
        processor = Processor(name=name)
        assert processor.name == expected_name
        assert processor.description == expected_desc
        assert processor.replica_name == expected_name

    @pytest.mark.parametrize(
        'name,replica, expected_name,expected_desc',
        [
            (None, None, 'Processor', 'Processor'),
            ('TestProcessor', '123', 'TestProcessor', 'TestProcessor'),
            ('CustomProcessor', '#145', 'CustomProcessor', 'CustomProcessor'),
        ],
    )
    @pytest.mark.filterwarnings('ignore:get_items')
    def test_processor_init_name_description_and_replica(self, name, replica, expected_name, expected_desc):
        """Test processor name and description initialization."""
        processor = Processor(name=name, replica_id=replica)
        assert processor.name == expected_name
        assert processor.description == expected_desc
        assert processor.replica_name == processor.name + '#' + replica if replica else processor.name

    @pytest.mark.filterwarnings('ignore:get_items')
    def test_processor_init_custom_description(self):
        """Test processor with custom description."""
        processor = Processor(name='Test', description='Custom Description')
        assert processor.name == 'Test'
        assert processor.description == 'Custom Description'

    @pytest.mark.parametrize(
        'loop_type',
        [
            LoopType.ForLoop,
            LoopType.WhileLoop,
            LoopType.SingleLoop,
            'for_loop',  # Test string conversion
            'while_loop',
            'single',
        ],
    )
    @pytest.mark.filterwarnings('ignore:get_items')
    @pytest.mark.filterwarnings('ignore:while_condition')
    def test_processor_init_loop_type(self, loop_type):
        """Test processor initialization with different loop types."""
        processor = Processor(looper=loop_type)
        expected = LoopType(loop_type) if isinstance(loop_type, str) else loop_type
        assert processor.loop_type == expected

    @pytest.mark.filterwarnings('ignore:get_items')
    def test_processor_init_with_config(self):
        """Test processor initialization with configuration."""
        config = {'param1': 'value1', 'param2': 'value2'}
        processor = Processor(config=config)
        assert processor._config == config

    @pytest.mark.filterwarnings('ignore:get_items')
    def test_processor_init_with_kwargs(self):
        """Test processor initialization with keyword arguments."""
        kwargs = {'param1': 'value1', 'param2': 'value2'}
        processor = Processor(**kwargs)
        assert processor._kwargs == kwargs

    @pytest.mark.filterwarnings('ignore:get_items')
    def test_processor_init_unique_ids(self):
        """Test that each processor gets a unique ID."""
        processor1 = Processor()
        processor2 = Processor()
        processor3 = Processor()

        assert processor1.unique_id != processor2.unique_id
        assert processor2.unique_id != processor3.unique_id
        assert processor1.unique_id != processor3.unique_id


class TestProcessorPostInit:
    """Test cases for Processor.__post_init__ method."""

    @pytest.fixture
    def processor_mock_setup(self):
        """Setup mocks for processor post_init testing."""
        calls = []

        def record(name):
            def wrapper(*args, **kwargs):
                calls.append(name)

            return wrapper

        with (
            patch.object(Processor, '_register_parameters', side_effect=record('register')) as mock_register,
            patch.object(
                Processor, '_override_defaults', side_effect=record('override_defaults')
            ) as mock_override_defaults,
            patch.object(Processor, '_load_parameter_configuration', side_effect=record('load')) as mock_load,
            patch.object(Processor, '_overrule_kws_parameters', side_effect=record('overrule')) as mock_overrule,
            patch.object(
                Processor, '_check_method_overload', side_effect=record('check_overload')
            ) as mock_check_overload,
            patch.object(Processor, '_check_method_super', side_effect=record('check_super')) as mock_check_super,
            patch('mafw.processor.ConsoleInterface'),
            patch('mafw.processor.validate_database_conf'),
            patch('mafw.db.db_filter.ProcessorFilter'),
        ):
            yield {
                'calls': calls,
                'mocks': {
                    'register': mock_register,
                    'defaults': mock_override_defaults,
                    'load': mock_load,
                    'overrule': mock_overrule,
                    'check_overload': mock_check_overload,
                    'check_super': mock_check_super,
                },
            }

    def test_post_init_method_call_order(self, processor_mock_setup):
        """Test that __post_init__ methods are called in correct order."""
        calls = processor_mock_setup['calls']

        # Instantiate Processor (triggers __post_init__)
        p = Processor()

        # Expected call order
        expected_call_order = ['register', 'override_defaults', 'load', 'overrule', 'check_overload', 'check_super']

        assert calls == expected_call_order, f'Expected {expected_call_order}, but got {calls}'
        assert p.processor_status == ProcessorStatus.Init


class TestProcessorParameters:
    """Test cases for Processor parameter management."""

    @pytest.fixture
    def processor_with_parameters(self):
        """Create a processor with test parameters."""
        with (
            patch('mafw.processor.ConsoleInterface'),
            patch('mafw.processor.validate_database_conf'),
            patch('mafw.db.db_filter.ProcessorFilter'),
        ):

            @single_loop
            class TestProcessor(Processor):
                test_param1 = ActiveParameter('test_param1', 'default1')
                test_param2 = ActiveParameter('test_param2', 42)

            return TestProcessor()

    def test_register_parameters(self, processor_with_parameters):
        """Test parameter registration."""
        processor = processor_with_parameters

        assert 'test_param1' in processor._processor_parameters
        assert 'test_param2' in processor._processor_parameters
        assert processor._parameter_registered is True

    def test_register_parameters_second_time(self, processor_with_parameters):
        processor = processor_with_parameters
        assert processor._parameter_registered  # parameter should be automatically registered
        processor._register_parameters()  # calling register a second time does not hurt
        assert 'test_param1' in processor._processor_parameters
        assert 'test_param2' in processor._processor_parameters
        assert processor._parameter_registered is True

    def test_default_value_override(self):
        @single_loop
        class BaseProcessor(Processor):
            param = ActiveParameter('test_param1', default='base_default')

        class DerivProcessor(BaseProcessor):
            new_defaults = {'test_param1': 'deriv_default', 'missing_param': 'nothing_happens'}

        base = BaseProcessor()
        deriv = DerivProcessor()

        assert 'test_param1' in base._processor_parameters
        assert base.param == 'base_default'
        assert 'test_param1' in deriv._processor_parameters
        assert deriv.param == 'deriv_default'
        assert 'missing_param' not in deriv._processor_parameters

    def test_register_parameters_duplicate_name_raises_error(self):
        """Test that duplicate parameter names raise an error."""
        with (
            patch('mafw.processor.ConsoleInterface'),
            patch('mafw.processor.validate_database_conf'),
            patch('mafw.db.db_filter.ProcessorFilter'),
        ):

            @single_loop
            class TestProcessor(Processor):
                param1 = ActiveParameter('duplicate_name', 'value1')
                param2 = ActiveParameter('duplicate_name', 'value2')

            with pytest.raises(ProcessorParameterError, match='Duplicated parameter name'):
                TestProcessor()

    def test_get_parameter_success(self, processor_with_parameters):
        """Test successful parameter retrieval."""
        processor = processor_with_parameters
        param = processor.get_parameter('test_param1')

        assert isinstance(param, PassiveParameter)
        assert param.name == 'test_param1'
        assert param.value == 'default1'

    def test_get_parameter_not_found(self, processor_with_parameters):
        """Test parameter retrieval with non-existent parameter."""
        processor = processor_with_parameters

        with pytest.raises(ProcessorParameterError, match='No parameter \\(nonexistent\\) found'):
            processor.get_parameter('nonexistent')

    def test_get_parameters_returns_all(self, processor_with_parameters):
        """Test that get_parameters returns all registered parameters."""
        processor = processor_with_parameters
        params = processor.get_parameters()

        assert len(params) == 2
        assert 'test_param1' in params
        assert 'test_param2' in params

    def test_set_parameter_value_success(self, processor_with_parameters):
        """Test successful parameter value setting."""
        processor = processor_with_parameters
        processor.set_parameter_value('test_param1', 'new_value')

        param = processor.get_parameter('test_param1')
        assert param.value == 'new_value'

    def test_set_parameter_value_not_found(self, processor_with_parameters):
        """Test parameter value setting with non-existent parameter."""
        processor = processor_with_parameters

        with pytest.raises(ProcessorParameterError, match='No parameter \\(nonexistent\\) found'):
            processor.set_parameter_value('nonexistent', 'value')

    def test_delete_parameter_success(self, processor_with_parameters):
        """Test successful parameter deletion."""
        processor = processor_with_parameters
        processor.delete_parameter('test_param1')

        assert 'test_param1' not in processor._processor_parameters
        assert 'test_param2' in processor._processor_parameters

    def test_delete_parameter_not_found(self, processor_with_parameters):
        """Test parameter deletion with non-existent parameter."""
        processor = processor_with_parameters

        with pytest.raises(ProcessorParameterError, match='No parameter \\(nonexistent\\) found'):
            processor.delete_parameter('nonexistent')

    def test_reset_parameters(self, processor_with_parameters):
        """Test parameter reset functionality."""
        processor = processor_with_parameters

        # Modify parameters
        processor.delete_parameter('test_param1')
        assert 'test_param1' not in processor._processor_parameters

        # Reset parameters
        processor._reset_parameters()

        # Verify parameters are restored
        assert 'test_param1' in processor._processor_parameters
        assert 'test_param2' in processor._processor_parameters

    @pytest.mark.parametrize(
        'option,expected_structure',
        [
            (1, lambda name, params: {name: params}),
            (2, lambda name, params: params),
            (3, lambda name, params: params),  # Unknown option defaults to 2
        ],
    )
    def test_dump_parameter_configuration(self, processor_with_parameters, option, expected_structure):
        """Test parameter configuration dumping with different options."""
        processor = processor_with_parameters

        with patch('mafw.processor.log') as mock_log:
            config = processor.dump_parameter_configuration(option)

            expected_params = {'test_param1': 'default1', 'test_param2': 42}
            expected_config = expected_structure(processor.replica_name, expected_params)

            assert config == expected_config

            if option not in [1, 2]:
                mock_log.warning.assert_called_once_with('Unknown option %s. Using option 2' % option)

    @pytest.mark.parametrize(
        'option,replica,expected_structure',
        [
            (1, None, lambda replica_name, params: {replica_name: params}),
            (1, '123', lambda replica_name, params: {replica_name: params}),
            (2, None, lambda replica_name, params: params),
            (2, '123', lambda replica_name, params: params),
            (3, None, lambda replica_name, params: params),
            (3, '123', lambda replica_name, params: params),
        ],
    )
    def test_dump_parameter_configuration_and_replica(
        self, processor_with_parameters, option, replica, expected_structure
    ):
        """Test parameter configuration dumping with different options."""
        processor = processor_with_parameters
        processor.replica_id = replica

        with patch('mafw.processor.log') as mock_log:
            config = processor.dump_parameter_configuration(option)

            expected_params = {'test_param1': 'default1', 'test_param2': 42}
            expected_config = expected_structure(processor.replica_name, expected_params)

            assert config == expected_config

            if option not in [1, 2]:
                mock_log.warning.assert_called_once_with('Unknown option %s. Using option 2' % option)


class TestProcessorProperties:
    """Test cases for Processor properties."""

    @pytest.fixture
    def processor(self):
        """Create a basic processor for testing."""
        with (
            patch('mafw.processor.ConsoleInterface'),
            patch('mafw.processor.validate_database_conf'),
            patch('mafw.db.db_filter.ProcessorFilter'),
        ):
            return Processor(looper=LoopType.SingleLoop)

    def test_i_item_property(self, processor):
        """Test i_item property getter and setter."""
        assert processor.i_item == -1

        processor.i_item = 5
        assert processor.i_item == 5
        assert processor._i_item == 5

    def test_n_item_property(self, processor):
        """Test n_item property getter and setter."""
        assert processor.n_item == -1

        processor.n_item = 10
        assert processor.n_item == 10
        assert processor._n_item == 10

        processor.n_item = None
        assert processor.n_item is None

    def test_unique_name_property(self, processor):
        """Test unique_name property."""
        expected_name = f'{processor.name}_{processor.unique_id}'
        assert processor.unique_name == expected_name

    def test_local_resource_acquisition_property(self, processor):
        """Test local_resource_acquisition property."""
        assert processor.local_resource_acquisition is True

        processor.local_resource_acquisition = False
        assert processor.local_resource_acquisition is False
        assert processor._resource_acquisition is False

    def test_database_property_success(self, processor):
        """Test database property when database is available."""
        mock_db = Mock()
        processor._database = mock_db

        assert processor.database == mock_db

    def test_database_property_missing_database(self, processor):
        """Test database property when database is None."""
        processor._database = None

        with pytest.raises(MissingDatabase, match='Database connection not initialized'):
            _ = processor.database


class TestProcessorExecution:
    """Test cases for Processor execution methods."""

    @pytest.fixture
    def processor_with_mocks(self):
        """Create processor with execution methods mocked."""
        with (
            patch('mafw.processor.ConsoleInterface'),
            patch('mafw.processor.validate_database_conf'),
            patch('mafw.db.db_filter.ProcessorFilter'),
        ):
            processor = Processor()

            # Mock execution methods
            processor._execute_single = Mock()
            processor._execute_for_loop = Mock()
            processor._execute_while_loop = Mock()

            return processor

    @pytest.mark.parametrize(
        'loop_type,expected_method',
        [
            (LoopType.SingleLoop, '_execute_single'),
            (LoopType.ForLoop, '_execute_for_loop'),
            (LoopType.WhileLoop, '_execute_while_loop'),
        ],
    )
    @pytest.mark.filterwarnings('ignore:get_items')
    @pytest.mark.filterwarnings('ignore:while_condition')
    def test_execute_dispatcher(self, processor_with_mocks, loop_type, expected_method):
        """Test that execute method dispatches to correct implementation."""
        processor = processor_with_mocks
        processor.loop_type = loop_type

        processor.execute()

        expected_mock = getattr(processor, expected_method)
        expected_mock.assert_called_once()

        # Verify other methods weren't called
        other_methods = ['_execute_single', '_execute_for_loop', '_execute_while_loop']
        other_methods.remove(expected_method)
        for method_name in other_methods:
            method_mock = getattr(processor, method_name)
            method_mock.assert_not_called()

    @pytest.mark.filterwarnings('ignore:get_items')
    def test_execute_single(self):
        """Test single execution implementation."""
        with (
            patch('mafw.processor.ConsoleInterface'),
            patch('mafw.processor.validate_database_conf'),
            patch('mafw.db.db_filter.ProcessorFilter'),
            patch('contextlib.ExitStack') as mock_exit_stack,
        ):
            processor = Processor()
            processor.acquire_resources = Mock()
            processor.start = Mock()
            processor.process = Mock()
            processor.finish = Mock()

            mock_stack = Mock()
            mock_exit_stack.return_value.__enter__.return_value = mock_stack

            processor._execute_single()

            processor.acquire_resources.assert_called_once()
            processor.start.assert_called_once()
            processor.process.assert_called_once()
            processor.finish.assert_called_once()
            assert processor.processor_status == ProcessorStatus.Run

    @pytest.mark.filterwarnings('ignore:get_items')
    def test_execute_for_loop(self):
        """Test for loop execution implementation."""
        with (
            patch('mafw.processor.ConsoleInterface') as mock_console,
            patch('mafw.processor.validate_database_conf'),
            patch('mafw.db.db_filter.ProcessorFilter'),
            patch('contextlib.ExitStack') as mock_exit_stack,
            patch('mafw.processor.Timer') as mock_timer,
        ):
            # Setup mocks
            mock_ui = Mock()
            mock_console.return_value = mock_ui
            mock_stack = Mock()
            mock_exit_stack.return_value.__enter__.return_value = mock_stack

            # Setup timer mock
            timer_instance = Mock()
            timer_instance.duration = 0.5
            mock_timer.return_value.__enter__.return_value = timer_instance

            processor = Processor()
            processor._user_interface = mock_ui
            processor.acquire_resources = Mock()
            processor.start = Mock()
            processor.finish = Mock()
            processor.process = Mock()
            processor.accept_item = Mock()
            processor.format_progress_message = Mock()

            # Mock get_items to return test data
            test_items = ['item1', 'item2', 'item3']
            processor.get_items = Mock(return_value=test_items)

            processor._execute_for_loop()

            # Verify setup calls
            processor.acquire_resources.assert_called_once()
            processor.start.assert_called_once()
            processor.get_items.assert_called_once()

            # Verify UI calls
            mock_ui.create_task.assert_called_once()
            assert mock_ui.update_task.call_count >= 1

            # Verify processing calls
            assert processor.process.call_count == len(test_items)
            assert processor.accept_item.call_count == len(test_items)

            processor.finish.assert_called_once()
            assert processor.n_item == len(test_items)

    def test_execute_for_loop_accept_skip_quit(self):
        class TestProcessor(Processor):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.skip = 0
                self.accept = 0

            def get_items(self) -> Collection[Any]:
                return [LoopingStatus.Continue, LoopingStatus.Skip, LoopingStatus.Quit]

            def process(self) -> None:
                self.looping_status = self.item

            def accept_item(self) -> None:
                self.accept = self.i_item

            def skip_item(self) -> None:
                self.skip = self.i_item

        tp = TestProcessor()
        tp.execute()

        assert tp.accept == 0
        assert tp.skip == 1
        assert tp.processor_exit_status == ProcessorExitStatus.Successful

    def test_execute_for_loop_accept_skip_abort(self):
        class TestProcessor(Processor):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.skip = 0
                self.accept = 0

            def get_items(self) -> Collection[Any]:
                return [LoopingStatus.Continue, LoopingStatus.Skip, LoopingStatus.Abort]

            def process(self) -> None:
                self.looping_status = self.item

            def accept_item(self) -> None:
                self.accept = self.i_item

            def skip_item(self) -> None:
                self.skip = self.i_item

        tp = TestProcessor()
        tp.execute()

        assert tp.accept == 0
        assert tp.skip == 1
        assert tp.processor_exit_status == ProcessorExitStatus.Aborted

    @pytest.mark.filterwarnings('ignore:get_items')
    def test_execute_while_loop(self):
        """Test while loop execution implementation."""
        with (
            patch('mafw.processor.ConsoleInterface') as mock_console,
            patch('mafw.processor.validate_database_conf'),
            patch('mafw.db.db_filter.ProcessorFilter'),
            patch('contextlib.ExitStack') as mock_exit_stack,
            patch('mafw.processor.Timer') as mock_timer,
        ):
            # Setup mocks
            mock_ui = Mock()
            mock_console.return_value = mock_ui
            mock_stack = Mock()
            mock_exit_stack.return_value.__enter__.return_value = mock_stack

            # Setup timer mock
            timer_instance = Mock()
            timer_instance.duration = 0.5
            mock_timer.return_value.__enter__.return_value = timer_instance

            processor = Processor()
            processor._user_interface = mock_ui
            processor.acquire_resources = Mock()
            processor.start = Mock()
            processor.finish = Mock()
            processor.process = Mock()
            processor.accept_item = Mock()
            processor.format_progress_message = Mock()

            # Setup while condition to run 3 times then stop
            call_count = 0

            def mock_while_condition():
                nonlocal call_count
                call_count += 1
                return call_count <= 3

            processor.while_condition = Mock(side_effect=mock_while_condition)

            processor._execute_while_loop()

            # Verify setup calls
            processor.acquire_resources.assert_called_once()
            processor.start.assert_called_once()

            # Verify UI calls
            mock_ui.create_task.assert_called_once()
            assert mock_ui.update_task.call_count >= 1

            # Verify processing calls (should run 3 times)
            assert processor.process.call_count == 3
            assert processor.accept_item.call_count == 3

            processor.finish.assert_called_once()

    def test_execute_while_loop_accept_skip_quit(self):
        class TestProcessor(Processor):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, looper='while_loop', **kwargs)
                self.skip = 0
                self.accept = 0
                self.list = [LoopingStatus.Continue, LoopingStatus.Skip, LoopingStatus.Quit]

            def while_condition(self) -> bool:
                return self.i_item < len(self.list)

            def process(self) -> None:
                self.item = self.list[self.i_item]
                self.looping_status = self.item

            def accept_item(self) -> None:
                self.accept = self.i_item
                self.i_item += 1

            def skip_item(self) -> None:
                self.skip = self.i_item
                self.i_item += 1

        tp = TestProcessor()
        tp.execute()

        assert tp.accept == 0
        assert tp.skip == 1
        assert tp.processor_exit_status == ProcessorExitStatus.Successful

    def test_execute_while_loop_accept_skip_abort(self):
        class TestProcessor(Processor):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, looper='while_loop', **kwargs)
                self.skip = 0
                self.accept = 0
                self.list = [LoopingStatus.Continue, LoopingStatus.Skip, LoopingStatus.Abort]

            def while_condition(self) -> bool:
                return self.i_item < len(self.list)

            def process(self) -> None:
                self.item = self.list[self.i_item]
                self.looping_status = self.item

            def accept_item(self) -> None:
                self.n_item = 12  # kind of fake, because this is a fake while
                self.accept = self.i_item
                self.i_item += 1

            def skip_item(self) -> None:
                self.skip = self.i_item
                self.i_item += 1

        tp = TestProcessor()
        tp.execute()

        assert tp.accept == 0
        assert tp.skip == 1
        assert tp.n_item == 12
        assert tp.processor_exit_status == ProcessorExitStatus.Aborted


class TestProcessorCallbacks:
    """Test cases for Processor callback methods."""

    @pytest.fixture
    def processor(self):
        """Create processor with mocked UI."""
        with (
            patch('mafw.processor.ConsoleInterface') as mock_console,
            patch('mafw.processor.validate_database_conf'),
            patch('mafw.db.db_filter.ProcessorFilter'),
        ):
            mock_ui = Mock()
            mock_console.return_value = mock_ui
            processor = Processor()
            processor._user_interface = mock_ui
            return processor

    @pytest.mark.filterwarnings('ignore:get_items')
    def test_on_processor_status_change(self, processor):
        """Test processor status change callback."""
        old_status = ProcessorStatus.Init
        new_status = ProcessorStatus.Run

        processor.on_processor_status_change(old_status, new_status)

        processor._user_interface.change_of_processor_status.assert_has_calls(
            [call(processor.name, ProcessorStatus.Unknown, old_status), call(processor.name, old_status, new_status)],
            any_order=False,
        )

    @pytest.mark.parametrize(
        'status,expected_log_level',
        [
            (LoopingStatus.Skip, 'warning'),
            (LoopingStatus.Abort, 'error'),
            (LoopingStatus.Quit, 'warning'),
            (LoopingStatus.Continue, None),  # No logging expected
        ],
    )
    @pytest.mark.filterwarnings('ignore:get_items')
    def test_on_looping_status_set(self, processor, status, expected_log_level):
        """Test looping status set callback."""
        with patch('mafw.processor.log') as mock_log:
            processor.i_item = 5
            processor.on_looping_status_set(status)

            if expected_log_level:
                log_method = getattr(mock_log, expected_log_level)
                log_method.assert_called_once()
            else:
                mock_log.warning.assert_not_called()
                mock_log.error.assert_not_called()


class TestProcessorMethodChecking:
    """Test cases for Processor method overload and super call checking."""

    def test_check_method_overload_for_loop(self):
        """Test method overload checking for ForLoop type."""
        with (
            patch('mafw.processor.ConsoleInterface'),
            patch('mafw.processor.validate_database_conf'),
            patch('mafw.db.db_filter.ProcessorFilter'),
            patch('mafw.processor.warnings') as mock_warnings,
        ):

            class TestProcessor(Processor):
                def __init__(self):
                    super().__init__(looper=LoopType.ForLoop)

                # get_items is not overloaded

            _ = TestProcessor()

            # Should emit warning for missing get_items overload
            mock_warnings.warn.assert_called()
            warning_args = mock_warnings.warn.call_args[0]
            assert 'get_items' in str(warning_args[0])

    def test_check_method_overload_while_loop(self):
        """Test method overload checking for WhileLoop type."""
        with (
            patch('mafw.processor.ConsoleInterface'),
            patch('mafw.processor.validate_database_conf'),
            patch('mafw.db.db_filter.ProcessorFilter'),
            patch('mafw.processor.warnings') as mock_warnings,
        ):

            class TestProcessor(Processor):
                def __init__(self):
                    super().__init__(looper=LoopType.WhileLoop)

                # while_condition is not overloaded

            _ = TestProcessor()

            # Should emit warning for missing while_condition overload
            mock_warnings.warn.assert_called()
            warning_args = mock_warnings.warn.call_args[0]
            assert 'while_condition' in str(warning_args[0])

    def test_check_method_overload_ok(self):
        with (
            patch('mafw.processor.ConsoleInterface'),
            patch('mafw.processor.validate_database_conf'),
            patch('mafw.db.db_filter.ProcessorFilter'),
            patch('mafw.processor.warnings') as mock_warnings,
        ):

            class TestProcessor(Processor):
                def __init__(self):
                    super().__init__(looper=LoopType.WhileLoop)

                def while_condition(self) -> bool:
                    print('check condition')
                    return True

            TestProcessor()

            # Should not emit warning for missing while_condition overload
            mock_warnings.warn.assert_not_called()

    def test_check_method_super_missing_super_call(self):
        """Test super call checking when super is missing."""
        with (
            patch('mafw.processor.ConsoleInterface'),
            patch('mafw.processor.validate_database_conf'),
            patch('mafw.db.db_filter.ProcessorFilter'),
            patch('mafw.processor.warnings') as mock_warnings,
        ):

            class TestProcessor(Processor):
                def start(self):
                    print('Custom start without super')

                def finish(self) -> None:
                    print('Custom finish without super')

            TestProcessor()

            # Should emit warning for missing super call
            mock_warnings.warn.assert_called()

    def test_check_method_super_with_super_call(self):
        """Test super call checking when super is present."""
        with (
            patch('mafw.processor.ConsoleInterface'),
            patch('mafw.processor.validate_database_conf'),
            patch('mafw.db.db_filter.ProcessorFilter'),
            patch('mafw.processor.warnings') as mock_warnings,
        ):

            class TestProcessor(Processor):
                def start(self):
                    super().start()
                    print('Custom start with super')

                def finish(self) -> None:
                    super().finish()
                    print('Custom finish with super')

            TestProcessor()

            # Should not emit warning
            # Check if any warning about missing super was called
            warning_calls = mock_warnings.warn.call_args_list
            super_warnings = [call for call in warning_calls if call and 'super method' in str(call[0][0])]
            assert len(super_warnings) == 0

    def test_check_method_super_with_decorated_super_call(self):
        """Test super call checking when super is present."""
        with (
            patch('mafw.processor.ConsoleInterface'),
            patch('mafw.processor.validate_database_conf'),
            patch('mafw.db.db_filter.ProcessorFilter'),
            patch('mafw.processor.warnings') as mock_warnings,
        ):

            @database_required
            class TestProcessor(Processor):
                def finish(self) -> None:
                    super().finish()
                    print('Custom finish with super')

            TestProcessor()

            # Should not emit warning
            # Check if any warning about missing super was called
            warning_calls = mock_warnings.warn.call_args_list
            super_warnings = [call for call in warning_calls if call and 'super method' in str(call[0][0])]
            assert len(super_warnings) == 0


class TestProcessorVirtualMethods:
    """Test cases for Processor virtual methods that should be overloaded."""

    @pytest.fixture
    def processor(self):
        """Create basic processor."""
        with (
            patch('mafw.processor.ConsoleInterface'),
            patch('mafw.processor.validate_database_conf'),
            patch('mafw.db.db_filter.ProcessorFilter'),
        ):
            return Processor(looper=LoopType.SingleLoop)

    def test_get_items_default_implementation(self, processor):
        """Test that get_items returns empty collection by default."""
        items = processor.get_items()
        assert isinstance(items, Collection)
        assert len(items) == 0

    def test_while_condition_default_implementation(self, processor):
        """Test that while_condition returns False by default."""
        result = processor.while_condition()
        assert result is False

    def test_process_default_implementation(self, processor):
        """Test that process method does nothing by default."""
        # Should not raise any exception
        processor.process()

    def test_accept_item_default_implementation(self, processor):
        """Test that accept_item method does nothing by default."""
        # Should not raise any exception
        processor.accept_item()

    def test_skip_item_default_implementation(self, processor):
        """Test that skip_item method does nothing by default."""
        # Should not raise any exception
        processor.skip_item()

    def test_format_progress_message_default_implementation(self, processor):
        """Test that format_progress_message method does nothing by default."""
        # Should not raise any exception
        processor.format_progress_message()


class TestProcessorConfiguration:
    """Test configuration loading and parameter management."""

    @pytest.mark.filterwarnings('ignore:get_items')
    def test_load_parameter_configuration_with_processor_name_key(self):
        """Test config loading when processor name is a key in config."""
        processor = Processor(
            name='TestProcessor', config={'TestProcessor': {'param1': 'value1'}, 'other_key': 'other_value'}
        )
        # Mock a parameter to test
        mock_param = Mock()
        mock_param.value = 'default'
        processor._processor_parameters = {'param1': mock_param}

        processor._load_parameter_configuration()

        # Should have used the nested config
        assert processor._config == {'param1': 'value1'}

    @pytest.mark.filterwarnings('ignore:get_items')
    def test_load_parameter_configuration_with_processor_name_key_and_right_replica(self):
        """Test config loading when processor name is a key in config."""
        processor = Processor(
            name='TestProcessor',
            config={
                'TestProcessor': {'param1': 'value1'},
                'TestProcessor#WRONGREPLICA': {'param1': 'WRONG'},
                'TestProcessor#123': {'param1': '123'},
                'other_key': 'other_value',
            },
            replica_id='123',
        )

        # Should have used the nested config
        assert processor._config == {'param1': '123'}

    @pytest.mark.filterwarnings('ignore:get_items')
    def test_load_parameter_configuration_with_processor_replica(self):
        """Test config loading when processor name is a key in config."""
        processor = Processor(
            name='TestProcessor',
            config={
                'AnotherTestProcessor': {'param1': 'value1'},
                'TestProcessor#WRONGREPLICA': {'param1': 'WRONG'},
                'TestProcessor#123': {'param1': '123'},
                'other_key': 'other_value',
            },
            replica_id='123',
        )

        # Should have used the nested config
        assert processor._config == {'param1': '123'}

    @pytest.mark.filterwarnings('ignore:get_items')
    def test_load_parameter_configuration_with_processor_name_key_and_wrong_replica(self):
        """Test config loading when processor name is a key in config."""
        processor = Processor(
            name='TestProcessor',
            config={
                'TestProcessor': {'param1': 'value1'},
                'TestProcessor#WRONGREPLICA': {'param1': 'WRONG'},
                'other_key': 'other_value',
            },
        )

        # Should have used the nested config
        assert processor._config == {'param1': 'value1'}

    @pytest.mark.filterwarnings('ignore:get_items')
    def test_load_parameter_configuration_without_processor_name_key(self):
        """Test config loading when processor name is not a key in config."""
        config = {'param1': 'value1', 'param2': 'value2'}
        processor = Processor(config=config)

        # Should use the config as-is
        assert processor._config == config

    @pytest.mark.filterwarnings('ignore:get_items')
    def test_load_parameter_configuration_without_processor_name_key_but_replica(self):
        """Test config loading when processor name is not a key in config."""
        config = {'param1': 'value1', 'param2': 'value2'}
        processor = Processor(config=config, replica_id='123')

        # Should use the config as-is
        assert processor._config == config

    @pytest.mark.filterwarnings('ignore:get_items')
    @patch('mafw.db.db_filter.ModelFilter.from_conf')
    def test_load_parameter_configuration_with_filter_only(self, mock_from_conf):
        """Test config loading with ModelFilter but no GlobalFilter."""
        config = {'TestProcessor': {'__filter__': {'Model1': {'filter_param': 'filter_value'}}}}
        Processor(name='TestProcessor', config=config)

        mock_from_conf.assert_called_once_with(
            'TestProcessor.__filter__.Model1',
            config,
        )

    @pytest.mark.filterwarnings('ignore:get_items')
    @patch('mafw.db.db_filter.ModelFilter.from_conf')
    def test_load_parameter_configuration_with_filter_only_processor_replica_base_conf(self, mock_from_conf):
        """Test config loading with ModelFilter but no GlobalFilter."""
        config = {'TestProcessor': {'__filter__': {'Model1': {'filter_param': 'filter_value'}}}}
        p = Processor(name='TestProcessor', config=config, replica_id='123')

        # during the parameter loading we create an additional entry in the original configuration with
        # the updated value for the replica
        config[p.replica_name] = {'__filter__': {'Model1': {'filter_param': 'filter_value'}}}

        mock_from_conf.assert_called_once_with(
            'TestProcessor#123.__filter__.Model1',
            config,
        )

    @pytest.mark.filterwarnings('ignore:get_items')
    @patch('mafw.db.db_filter.ModelFilter.from_conf')
    def test_load_parameter_configuration_with_filter_only_processor_replica_base_logic(self, mock_from_conf):
        """Test config loading with ModelFilter but no GlobalFilter."""
        config = {
            'TestProcessor': {'__filter__': {'Model1': {'filter_param': 'filter_value'}}, '__logic__': 'NOT Model1'}
        }
        p = Processor(name='TestProcessor', config=config, replica_id='123')

        # during the parameter loading we create an additional entry in the original configuration with
        # the updated value for the replica
        update_config = deepcopy(config)
        update_config[p.replica_name] = p._config

        assert p.filter_register._logic == 'NOT Model1'

        mock_from_conf.assert_called_once_with(
            'TestProcessor#123.__filter__.Model1',
            update_config,
        )

    @pytest.mark.filterwarnings('ignore:get_items')
    @patch('mafw.db.db_filter.ModelFilter.from_conf')
    def test_load_parameter_configuration_with_one_model_processor_replica(self, mock_from_conf):
        """Test config loading with ModelFilter but no GlobalFilter."""
        config = {
            'TestProcessor': {'param': 1, '__filter__': {'Model1': {'filter_param': 'filter_value'}}},
            'TestProcessor#123': {'__filter__': {'Model1': {'filter_param': 'filter_value123'}}},
            'TestProcessor#124': {'__filter__': {'Model1': {'filter_param': 'filter_value124'}}},
        }
        p = Processor(name='TestProcessor', config=config, replica_id='123')

        update_config = deepcopy(config)
        update_config[p.replica_name] = p._config

        mock_from_conf.assert_called_once_with(
            'TestProcessor#123.__filter__.Model1',
            update_config,
        )

    @pytest.mark.filterwarnings('ignore:get_items')
    @patch('mafw.db.db_filter.ModelFilter.from_conf')
    def test_load_parameter_configuration_with_one_model_processor_replica_no_inheritance(self, mock_from_conf):
        """Test config loading with ModelFilter but no GlobalFilter."""
        config = {
            'TestProcessor': {'param': 1, '__filter__': {'Model1': {'filter_param': 'filter_value'}}},
            'TestProcessor#123': {'__filter__': {'Model1': {'filter_param': 'filter_value123'}}},
            'TestProcessor#124': {
                '__inheritance__': False,
                '__filter__': {'Model1': {'filter_param': 'filter_value124'}},
            },
        }
        p = Processor(name='TestProcessor', config=config, replica_id='124')

        #        update_config = deepcopy(config)
        #        update_config[p.replica_name] = p._config

        mock_from_conf.assert_called_once_with(
            'TestProcessor#124.__filter__.Model1',
            config,
        )

        assert p._config == config['TestProcessor#124']

    @pytest.mark.filterwarnings('ignore:get_items')
    @patch('mafw.db.db_filter.ModelFilter.from_conf')
    def test_load_parameter_configuration_with_filter_only_processor_replica_with_update(self, mock_from_conf):
        """Test config loading with ModelFilter but no GlobalFilter."""
        config = {
            'TestProcessor': {
                '__filter__': {'Model1': {'filter_param': 'filter_value'}, 'Model2': {'filter_param': 'base_value'}}
            },
            'TestProcessor#123': {'__filter__': {'Model1': {'filter_param': 'filter_value123'}}},
            'TestProcessor#124': {'__filter__': {'Model1': {'filter_param': 'filter_value124'}}},
        }
        p = Processor(name='TestProcessor', config=config, replica_id='123')

        updated_config = deepcopy(config)
        updated_config[p.replica_name] = p._config
        assert p._orig_config == config

        # Verify that mock_from_conf was called exactly twice
        assert mock_from_conf.call_count == 2

        # Get all call arguments
        call_args_list = mock_from_conf.call_args_list

        # Verify first call
        expected_call_1 = call('TestProcessor#123.__filter__.Model1', updated_config)
        assert call_args_list[0] == expected_call_1

        # Verify second call
        expected_call_2 = call('TestProcessor#123.__filter__.Model2', updated_config)
        assert call_args_list[1] == expected_call_2

    @pytest.mark.filterwarnings('ignore:get_items')
    @patch('mafw.db.db_filter.ModelFilter.from_conf')
    def test_preservation_of_original_config(self, mock_from_conf):
        """Test config loading with ModelFilter but no GlobalFilter."""
        config = {
            'TestProcessor': {'__filter__': {'Model2': {'filter_param': 'base_value'}}},
            'TestProcessor#123': {'__filter__': {'Model1': {'filter_param': 'filter_value123'}}, '__new_only__': False},
            'TestProcessor#124': {'__filter__': {'Model2': {'filter_param': 'filter_value124'}}},
        }
        p1 = Processor(name='TestProcessor', config=config, replica_id=None)
        p2 = Processor(name='TestProcessor', config=config, replica_id='123')
        p3 = Processor(name='TestProcessor', config=config, replica_id='124')

        assert p1.filter_register.new_only
        assert not p2.filter_register.new_only
        assert p3.filter_register.new_only

        assert p1._orig_config == config
        assert p2._orig_config == config
        assert p3._orig_config == config

        p1_updated = deepcopy(config)
        p1_updated[p1.replica_name] = p1._config

        p2_updated = deepcopy(config)
        p2_updated[p2.replica_name] = p2._config

        p3_updated = deepcopy(config)
        p3_updated[p3.replica_name] = p3._config

        # Verify that mock_from_conf was called exactly four times
        # - 1x for TestProcessor
        # - 2x for TestProcessor123
        # - 1x for TestProcessor124
        assert mock_from_conf.call_count == 4

        # Get all call arguments
        call_args_list = mock_from_conf.call_args_list

        assert call_args_list == [
            call('TestProcessor.__filter__.Model2', p1_updated),
            call('TestProcessor#123.__filter__.Model2', p2_updated),
            call('TestProcessor#123.__filter__.Model1', p2_updated),
            call('TestProcessor#124.__filter__.Model2', p3_updated),
        ]

    @pytest.mark.filterwarnings('ignore:get_items')
    def test_overrule_kws_parameters(self):
        """Test that kwargs override parameter values."""
        mock_param = Mock()
        mock_param.value = 'original'

        processor = Processor(param1='overridden')
        processor._processor_parameters = {'param1': mock_param}

        with patch.object(processor, 'get_parameter', return_value=mock_param):
            with patch.object(processor, 'set_parameter_value') as mock_set:
                processor._overrule_kws_parameters()
                mock_set.assert_called_once_with('param1', str('overridden'))


class TestProcessorFilterManagement:
    """Test filter-related functionality."""

    @pytest.mark.filterwarnings('ignore:get_items')
    def test_get_filter_success(self):
        """Test successful filter retrieval."""
        processor = Processor()
        mock_filter = Mock()
        processor.filter_register = {'Model1': mock_filter}

        result = processor.get_filter('Model1')

        assert result == mock_filter

    @pytest.mark.filterwarnings('ignore:get_items')
    def test_get_filter_not_found(self):
        """Test filter retrieval when filter doesn't exist."""
        processor = Processor()
        processor.filter_register = {}

        with pytest.raises(KeyError):
            processor.get_filter('NonExistentModel')


class TestProcessorResourceAcquisition:
    """Test resource acquisition and management."""

    @patch('mafw.processor.connect')
    @patch('mafw.processor.extract_protocol')
    @patch('mafw.processor.database_proxy')
    @patch('mafw.processor.mafw_model_register')
    def test_acquire_resources_with_database_config_sqlite(
        self, mock_db_register, mock_db_proxy, mock_extract, mock_connect
    ):
        """Test resource acquisition with SQLite database configuration."""
        mock_extract.return_value = 'sqlite'
        mock_db = Mock()
        mock_connect.return_value = mock_db

        mock_std_table = MagicMock(spec=StandardTable)

        mock_db_register.get_standard_tables = Mock(return_value=[mock_std_table])

        processor = Processor(
            database_conf={
                'DBConfiguration': {'URL': 'sqlite:///test.db', 'pragmas': {'foreign_keys': 1}, 'other_param': 'value'}
            },
            looper='single',
        )

        # Create a proper ExitStack mock
        processor._resource_stack = Mock()
        processor._resource_stack.callback = Mock()
        processor._resource_stack.enter_context = Mock()
        processor._resource_acquisition = True

        processor.acquire_resources()

        # Verify the database connection was set up correctly
        mock_connect.assert_called_once_with('sqlite:///test.db', pragmas={'foreign_keys': 1}, other_param='value')
        mock_db.connect.assert_called_once()
        mock_db_proxy.initialize.assert_called_once_with(mock_db)

        # Verify database was added to resource stack for cleanup
        processor._resource_stack.callback.assert_called_once_with(mock_db.close)

        # Verify table creation and initialization
        mock_db.create_tables.assert_called_once_with([mock_std_table])
        mock_std_table.init.assert_called_once()

    @patch('mafw.processor.connect')
    @patch('mafw.processor.extract_protocol')
    @patch('mafw.processor.database_proxy')
    @patch('mafw.processor.mafw_model_register')
    def test_acquire_resources_with_database_config_sqlite_no_std_table(
        self, mock_db_register, mock_db_proxy, mock_extract, mock_connect
    ):
        """Test resource acquisition with SQLite database configuration."""
        mock_extract.return_value = 'sqlite'
        mock_db = Mock()
        mock_connect.return_value = mock_db

        mock_std_table = MagicMock(spec=StandardTable)

        mock_db_register.get_standard_tables = Mock(return_value=[mock_std_table])

        processor = Processor(
            database_conf={
                'DBConfiguration': {'URL': 'sqlite:///test.db', 'pragmas': {'foreign_keys': 1}, 'other_param': 'value'}
            },
            looper='single',
            create_standard_tables=False,
        )

        # Create a proper ExitStack mock
        processor._resource_stack = Mock()
        processor._resource_stack.callback = Mock()
        processor._resource_stack.enter_context = Mock()
        processor._resource_acquisition = True

        processor.acquire_resources()

        # Verify the database connection was set up correctly
        mock_connect.assert_called_once_with('sqlite:///test.db', pragmas={'foreign_keys': 1}, other_param='value')
        mock_db.connect.assert_called_once()
        mock_db_proxy.initialize.assert_called_once_with(mock_db)

        # Verify database was added to resource stack for cleanup
        processor._resource_stack.callback.assert_called_once_with(mock_db.close)

        # Verify table creation and initialization
        mock_db.create_tables.assert_not_called()
        mock_std_table.init.assert_not_called()

    @patch('mafw.processor.connect')
    @patch('mafw.processor.extract_protocol')
    @patch('mafw.processor.database_proxy')
    @patch('mafw.processor.mafw_model_register')
    def test_acquire_resources_with_database_config_non_sqlite(
        self, mock_db_register, mock_db_proxy, mock_extract, mock_connect
    ):
        """Test resource acquisition with non-SQLite database configuration."""
        mock_extract.return_value = 'postgresql'
        mock_db = Mock()
        mock_connect.return_value = mock_db

        # Mock the standard_tables to avoid table creation issues
        mock_table = Mock()
        mock_table.init = Mock()
        mock_db_register.get_standard_tables = Mock(return_value=[mock_table])

        processor = Processor(
            database_conf={'URL': 'postgresql://user:pass@localhost/db', 'param1': 'value1'}, looper='single'
        )
        processor._resource_stack = Mock()

        processor.acquire_resources()

        mock_connect.assert_called_once_with('postgresql://user:pass@localhost/db', param1='value1')

        mock_db.connect.assert_called_once()
        mock_db_proxy.initialize.assert_called_once_with(mock_db)

        # Verify database was added to resource stack for cleanup
        processor._resource_stack.callback.assert_called_once_with(mock_db.close)

        # Verify table creation and initialization
        mock_db.create_tables.assert_called_once_with([mock_table])
        mock_table.init.assert_called_once()

    @patch('mafw.processor.connect')
    @patch('mafw.processor.log')
    def test_acquire_resources_database_connection_error(self, mock_log, mock_connect):
        """Test handling of database connection errors."""
        mock_db = Mock()
        mock_db.connect.side_effect = peewee.OperationalError('Connection failed')
        mock_connect.return_value = mock_db

        processor = Processor(database_conf={'URL': 'sqlite:///test.db'}, looper='single')
        processor._resource_stack = Mock()

        with pytest.raises(peewee.OperationalError):
            processor.acquire_resources()

        mock_log.critical.assert_called_once()

    def test_acquire_resources_existing_database(self):
        """Test resource acquisition when database already exists."""
        mock_db = Mock()
        processor = Processor(database=mock_db, looper='single')
        processor._resource_stack = Mock()

        # Should not raise any exceptions
        processor.acquire_resources()

        # Database should not be added to exit stack
        assert processor._database == mock_db

    def test_acquire_resources_no_local_acquisition(self):
        """Test resource acquisition when local acquisition is disabled."""
        processor = Processor(timer=Mock(), user_interface=Mock(), looper='single')
        processor._resource_acquisition = False
        processor._resource_stack = Mock()

        processor.acquire_resources()

        # Timer and UI should not be added to exit stack
        processor._resource_stack.enter_context.assert_not_called()


class TestProcessorDatabaseProperty:
    """Test database property behavior."""

    def test_database_property_success(self):
        """Test successful database property access."""
        mock_db = Mock()
        processor = Processor(database=mock_db, looper='single')

        result = processor.database

        assert result == mock_db

    def test_database_property_missing_database(self):
        """Test database property when database is None."""
        processor = Processor(looper='single')

        with pytest.raises(MissingDatabase, match='Database connection not initialized'):
            _ = processor.database


class TestProcessorOrphanFileRemoval:
    """Test orphan file removal functionality."""

    @patch('mafw.processor.mafw_model_register')
    def test_remove_orphan_files_no_database(self, mock_register):
        """Test orphan file removal when no database is available."""
        processor = Processor(looper='single')
        processor._database = None

        processor._remove_orphan_files()

        # Should return early, no database operations
        mock_register.__getitem__.assert_not_called()

    @patch('mafw.processor.mafw_model_register')
    def test_remove_orphan_files_disabled(self, mock_register):
        """Test orphan file removal when disabled."""
        processor = Processor(remove_orphan_files=False, looper='single')
        processor._database = Mock()

        processor._remove_orphan_files()

        # Should return early
        mock_register.__getitem__.assert_not_called()

    @patch('mafw.processor.mafw_model_register')
    @patch('mafw.processor.log')
    def test_remove_orphan_files_table_not_found(self, mock_log, mock_register):
        """Test orphan file removal when OrphanFile table doesn't exist."""
        mock_db = Mock()

        mock_register.get_model = Mock(side_effect=KeyError)

        processor = Processor(looper='single', database=mock_db)

        processor._remove_orphan_files()

        mock_log.warning.assert_called_once_with('OrphanFile table not found in DB. Please verify database integrity')

    @patch('mafw.processor.mafw_model_register')
    @patch('mafw.processor.log')
    def test_remove_orphan_files_success(self, mock_log, mock_register):
        """Test successful orphan file removal."""
        mock_db = Mock()

        mock_file1 = Mock()
        mock_file2 = Mock()

        mock_orphan = MagicMock()
        mock_orphan.filenames = [mock_file1, mock_file2]

        mock_orphan_model = Mock()
        mock_orphan_model.select.return_value.execute.return_value = [mock_orphan]
        mock_register.get_model.return_value = mock_orphan_model

        processor = Processor(database=mock_db, looper='single')

        processor._remove_orphan_files()

        # Verify files were unlinked
        mock_file1.unlink.assert_called_once_with(missing_ok=True)
        mock_file2.unlink.assert_called_once_with(missing_ok=True)

        # Verify database cleanup
        mock_orphan_model.delete.return_value.execute.assert_called_once()

        # Verify log message
        mock_log.info.assert_called_once()
        assert 'Pruning orphan files' in mock_log.info.call_args[0][0]

    @patch('mafw.processor.mafw_model_register')
    def test_remove_orphan_files_no_orphans(self, mock_register):
        """Test orphan file removal when no orphan files exist."""
        mock_db = Mock()

        mock_orphan_model = Mock()
        mock_orphan_model.select.return_value.execute.return_value = []  # No orphans

        mock_register.get_model.return_value = mock_orphan_model

        processor = Processor(database=mock_db, looper='single')

        processor._remove_orphan_files()

        # Should not call delete if no orphans
        mock_orphan_model.delete.assert_not_called()


class TestProcessorStatistics:
    """Test process statistics functionality."""

    @patch('mafw.processor.log')
    @patch('mafw.processor.pretty_format_duration')
    def test_print_process_statistics_with_durations(self, mock_format, mock_log):
        """Test printing statistics when process durations exist."""
        mock_format.side_effect = lambda x, **kwargs: f'{x:.3f}s'

        processor = Processor(looper='single')
        processor._process_durations = [1.0, 2.0, 3.0, 0.5, 1.5]

        processor.print_process_statistics()

        # Verify all log calls
        expected_calls = [
            call('[cyan] Processed %s items.' % 5),
            call('[cyan] Fastest item process duration: %s ' % '0.500s'),
            call('[cyan] Slowest item process duration: %s ' % '3.000s'),
            call('[cyan] Average item process duration: %s ' % '1.600s'),
            call('[cyan] Total process duration: %s' % '8.000s'),
        ]

        mock_log.info.assert_has_calls(expected_calls)

    @patch('mafw.processor.log')
    def test_print_process_statistics_no_durations(self, mock_log):
        """Test printing statistics when no process durations exist."""
        processor = Processor(looper='single')
        processor._process_durations = []

        processor.print_process_statistics()

        # Should not log anything
        mock_log.info.assert_not_called()


class TestProcessorListInitialization:
    """Test ProcessorList initialization and constructor parameters."""

    def test_init_empty_list(self):
        """Test initialization with no processors."""
        processor_list = ProcessorList()

        assert len(processor_list) == 0
        assert processor_list.name == 'ProcessorList'
        assert processor_list.description == 'ProcessorList'
        assert processor_list.timer is None
        assert processor_list.timer_params == {}
        assert isinstance(processor_list._user_interface, ConsoleInterface)
        assert processor_list._database is None
        assert processor_list._database_conf is None
        assert processor_list.processor_exit_status == ProcessorExitStatus.Successful

    def test_init_with_processors(self):
        """Test initialization with processors."""
        mock_processor1 = Mock(spec=Processor)
        mock_processor2 = Mock(spec=Processor)

        processor_list = ProcessorList(mock_processor1, mock_processor2)

        assert len(processor_list) == 2
        assert processor_list[0] == mock_processor1
        assert processor_list[1] == mock_processor2

    def test_init_with_custom_parameters(self):
        """Test initialization with custom parameters."""
        mock_timer = Mock(spec=Timer)
        mock_ui = Mock(spec=UserInterfaceBase)
        mock_db = Mock(spec=peewee.Database)
        timer_params = {'param1': 'value1'}
        db_conf = {'URL': 'sqlite:///test.db'}

        processor_list = ProcessorList(
            name='TestList',
            description='Test Description',
            timer=mock_timer,
            timer_params=timer_params,
            user_interface=mock_ui,
            database=mock_db,
            database_conf=db_conf,
        )

        assert processor_list.name == 'TestList'
        assert processor_list.description == 'Test Description'
        assert processor_list.timer == mock_timer
        assert processor_list.timer_params == timer_params
        assert processor_list._user_interface == mock_ui
        assert processor_list._database == mock_db
        assert processor_list._database_conf == db_conf

    def test_init_with_processor_list(self):
        """Test initialization with nested ProcessorList."""
        mock_processor = Mock(spec=Processor)
        nested_list = ProcessorList(mock_processor)

        processor_list = ProcessorList(nested_list)

        assert len(processor_list) == 1
        assert processor_list[0] == nested_list


class TestProcessorListValidation:
    """Test validation methods for ProcessorList."""

    def test_validate_item_processor(self):
        """Test validate_item with a valid Processor."""
        mock_processor = Mock(spec=Processor)

        result = ProcessorList.validate_item(mock_processor)

        assert result == mock_processor
        assert mock_processor.local_resource_acquisition is False

    def test_validate_item_processor_list(self):
        """Test validate_item with a valid ProcessorList."""
        processor_list = ProcessorList()

        result = ProcessorList.validate_item(processor_list)

        assert result == processor_list
        assert processor_list.timer_params == {'suppress_message': True}

    def test_validate_item_invalid_type(self):
        """Test validate_item with invalid type."""
        with pytest.raises(TypeError, match='Expected Processor or ProcessorList, got str'):
            ProcessorList.validate_item('invalid')

    def test_validate_items_empty(self):
        """Test validate_items with empty tuple."""
        result = ProcessorList.validate_items()
        assert result == tuple()

    def test_validate_items_with_none(self):
        """Test validate_items filtering out None values."""
        mock_processor = Mock(spec=Processor)

        result = ProcessorList.validate_items((mock_processor, None))

        assert len(result) == 1
        assert result[0] == mock_processor

    def test_validate_items_multiple(self):
        """Test validate_items with multiple items."""
        mock_processor1 = Mock(spec=Processor)
        mock_processor2 = Mock(spec=Processor)

        result = ProcessorList.validate_items((mock_processor1, mock_processor2))

        assert len(result) == 2
        assert result[0] == mock_processor1
        assert result[1] == mock_processor2


class TestProcessorListListOperations:
    """Test list operations (append, insert, extend, setitem)."""

    def test_setitem_valid_processor(self):
        """Test __setitem__ with valid processor."""
        mock_processor1 = Mock(spec=Processor)
        mock_processor2 = Mock(spec=Processor)

        processor_list = ProcessorList(mock_processor1)
        processor_list[0] = mock_processor2

        assert processor_list[0] == mock_processor2
        assert mock_processor2.local_resource_acquisition is False

    def test_setitem_invalid_type(self):
        """Test __setitem__ with invalid type."""
        mock_processor = Mock(spec=Processor)
        processor_list = ProcessorList(mock_processor)

        with pytest.raises(TypeError):
            processor_list[0] = 'invalid'

    def test_insert_valid_processor(self):
        """Test insert with valid processor."""
        mock_processor1 = Mock(spec=Processor)
        mock_processor2 = Mock(spec=Processor)

        processor_list = ProcessorList(mock_processor1)
        processor_list.insert(0, mock_processor2)

        assert len(processor_list) == 2
        assert processor_list[0] == mock_processor2
        assert processor_list[1] == mock_processor1

    def test_insert_invalid_type(self):
        """Test insert with invalid type."""
        processor_list = ProcessorList()

        with pytest.raises(TypeError):
            processor_list.insert(0, 'invalid')

    def test_append_valid_processor(self):
        """Test append with valid processor."""
        mock_processor1 = Mock(spec=Processor)
        mock_processor2 = Mock(spec=Processor)

        processor_list = ProcessorList(mock_processor1)
        processor_list.append(mock_processor2)

        assert len(processor_list) == 2
        assert processor_list[1] == mock_processor2

    def test_append_invalid_type(self):
        """Test append with invalid type."""
        processor_list = ProcessorList()

        with pytest.raises(TypeError):
            processor_list.append('invalid')

    def test_extend_with_processor_list(self):
        """Test extend with another ProcessorList."""
        mock_processor1 = Mock(spec=Processor)
        mock_processor2 = Mock(spec=Processor)

        processor_list1 = ProcessorList(mock_processor1)
        processor_list2 = ProcessorList(mock_processor2)

        processor_list1.extend(processor_list2)

        assert len(processor_list1) == 2
        assert processor_list1[0] == mock_processor1
        assert processor_list1[1] == mock_processor2

    def test_extend_with_iterable(self):
        """Test extend with regular iterable."""
        mock_processor1 = Mock(spec=Processor)
        mock_processor2 = Mock(spec=Processor)
        mock_processor3 = Mock(spec=Processor)

        processor_list = ProcessorList(mock_processor1)
        processor_list.extend([mock_processor2, mock_processor3])

        assert len(processor_list) == 3
        assert processor_list[0] == mock_processor1
        assert processor_list[1] == mock_processor2
        assert processor_list[2] == mock_processor3

    def test_extend_with_invalid_items(self):
        """Test extend with iterable containing invalid items."""
        mock_processor = Mock(spec=Processor)
        processor_list = ProcessorList()

        with pytest.raises(TypeError):
            processor_list.extend([mock_processor, 'invalid'])


class TestProcessorListProperties:
    """Test ProcessorList properties."""

    def test_name_property_getter(self):
        """Test name property getter."""
        processor_list = ProcessorList(name='TestName')
        assert processor_list.name == 'TestName'

    def test_name_property_setter(self):
        """Test name property setter."""
        processor_list = ProcessorList()
        processor_list.name = 'NewName'
        assert processor_list.name == 'NewName'

    def test_processor_exit_status_getter(self):
        """Test processor_exit_status property getter."""
        processor_list = ProcessorList()
        assert processor_list.processor_exit_status == ProcessorExitStatus.Successful

    def test_processor_exit_status_setter(self):
        """Test processor_exit_status property setter."""
        processor_list = ProcessorList()
        processor_list.processor_exit_status = ProcessorExitStatus.Aborted
        assert processor_list.processor_exit_status == ProcessorExitStatus.Aborted

    def test_database_property_with_database(self):
        """Test database property when database is set."""
        mock_db = Mock(spec=peewee.Database)
        processor_list = ProcessorList(database=mock_db)
        assert processor_list.database == mock_db

    def test_database_property_without_database(self):
        """Test database property when database is None."""
        processor_list = ProcessorList()
        with pytest.raises(MissingDatabase, match='Database connection not initialized'):
            _ = processor_list.database


class TestProcessorListResourceAcquisition:
    """Test resource acquisition methods."""

    @patch('mafw.processor.Timer')
    @patch('mafw.processor.extract_protocol')
    @patch('mafw.processor.connect')
    @patch('mafw.processor.mafw_model_register')
    def test_acquire_resources_no_existing_resources(
        self, mock_db_register, mock_connect, mock_extract_protocol, mock_timer_class
    ):
        """Test acquire_resources when no resources exist."""
        # Setup mocks
        mock_timer = Mock(spec=Timer)
        mock_timer_class.return_value = mock_timer
        mock_db = Mock(spec=peewee.Database)
        mock_connect.return_value = mock_db
        mock_extract_protocol.return_value = 'sqlite'

        mock_std_table = MagicMock(spec=StandardTable)
        mock_db_register.get_standard_tables = Mock(return_value=[mock_std_table])

        # Setup processor list with database config
        db_conf = {'DBConfiguration': {'URL': 'sqlite:///test1.db', 'pragmas': {'foreign_keys': 1}}}
        processor_list = ProcessorList(database_conf=db_conf)

        # Mock the ExitStack
        with patch('contextlib.ExitStack') as mock_exit_stack:
            mock_stack = Mock()
            mock_exit_stack.return_value.__enter__.return_value = mock_stack
            processor_list._resource_stack = mock_stack

            processor_list.acquire_resources()

            # Verify timer creation
            mock_timer_class.assert_called_once_with()
            mock_stack.enter_context.assert_any_call(mock_timer)

            # Verify database connection
            mock_connect.assert_called_once()
            mock_db.connect.assert_called_once()
            mock_stack.callback.assert_called_with(mock_db.close)

            mock_db.create_tables.assert_called_once_with([mock_std_table])
            mock_stack.callback.assert_called_once()

    def test_acquire_resources_with_existing_timer(self):
        """Test acquire_resources when timer already exists."""
        mock_timer = Mock(spec=Timer)
        processor_list = ProcessorList(timer=mock_timer)

        with patch('contextlib.ExitStack') as mock_exit_stack:
            mock_stack = Mock()
            mock_exit_stack.return_value.__enter__.return_value = mock_stack
            processor_list._resource_stack = mock_stack

            processor_list.acquire_resources()

            # Timer should not be created since it already exists
            assert processor_list.timer == mock_timer

    @patch('mafw.processor.connect')
    @patch('mafw.processor.extract_protocol')
    def test_acquire_resources_database_connection_error(self, mock_extract_protocol, mock_connect):
        """Test acquire_resources when database connection fails."""
        mock_extract_protocol.return_value = 'sqlite'
        mock_db = Mock(spec=peewee.Database)
        mock_db.connect.side_effect = peewee.OperationalError('Connection failed')
        mock_connect.return_value = mock_db

        db_conf = {'URL': 'sqlite:///test.db'}
        processor_list = ProcessorList(database_conf=db_conf)

        with patch('contextlib.ExitStack') as mock_exit_stack:
            mock_stack = Mock()
            mock_exit_stack.return_value.__enter__.return_value = mock_stack
            processor_list._resource_stack = mock_stack

            with pytest.raises(peewee.OperationalError):
                processor_list.acquire_resources()

    def test_acquire_resources_with_existing_database(self):
        """Test acquire_resources when database already exists."""
        mock_db = Mock(spec=peewee.Database)
        processor_list = ProcessorList(database=mock_db)

        with patch('contextlib.ExitStack') as mock_exit_stack:
            mock_stack = Mock()
            mock_exit_stack.return_value.__enter__.return_value = mock_stack
            processor_list._resource_stack = mock_stack

            processor_list.acquire_resources()

            # Database should remain unchanged
            assert processor_list._database == mock_db

    @patch('mafw.processor.connect')
    @patch('mafw.processor.extract_protocol')
    @patch('mafw.processor.database_proxy')
    @patch('mafw.processor.mafw_model_register')
    def test_acquire_resources_with_existing_database_no_std_tables(
        self, mock_db_register, mock_db_proxy, mock_extract, mock_connect
    ):
        mock_extract.return_value = 'sqlite'
        mock_db = Mock()
        mock_connect.return_value = mock_db

        mock_std_table = MagicMock(spec=StandardTable)
        mock_db_register.get_standard_tables = Mock(return_value=[mock_std_table])

        """Test acquire_resources when database already exists."""
        db_conf = {'DBConfiguration': {'URL': 'sqlite:///test.db', 'pragmas': {'foreign_keys': 1}}}
        processor_list = ProcessorList(database_conf=db_conf, create_standard_tables=False)

        with patch('contextlib.ExitStack') as mock_exit_stack:
            mock_stack = Mock()
            mock_exit_stack.return_value.__enter__.return_value = mock_stack
            processor_list._resource_stack = mock_stack

            processor_list.acquire_resources()

            mock_connect.assert_called_once_with('sqlite:///test.db', pragmas={'foreign_keys': 1})
            mock_db.connect.assert_called_once()
            mock_db_proxy.initialize.assert_called_once_with(mock_db)

            # Verify database was added to resource stack for cleanup
            processor_list._resource_stack.callback.assert_called_once_with(mock_db.close)

            # Verify table creation and initialization
            mock_db.create_tables.assert_not_called()
            mock_std_table.init.assert_not_called()

    def test_distribute_resources(self):
        """Test distribute_resources method."""
        mock_timer = Mock(spec=Timer)
        mock_ui = Mock(spec=UserInterfaceBase)
        mock_db = Mock(spec=peewee.Database)
        mock_processor = Mock(spec=Processor)

        processor_list = ProcessorList(
            timer=mock_timer, user_interface=mock_ui, database=mock_db, create_standard_tables=False
        )

        processor_list.distribute_resources(mock_processor)

        assert mock_processor.timer == mock_timer
        assert mock_processor._user_interface == mock_ui
        assert mock_processor._database == mock_db


class TestProcessorListExecution:
    """Test ProcessorList execution."""

    @patch('mafw.processor.log')
    def test_execute_successful(self, mock_log):
        """Test successful execution of processor list."""
        # Setup mocks
        mock_processor1 = Mock(spec=Processor)
        mock_processor1.name = 'Processor1'
        mock_processor1.execute.return_value = None
        mock_processor1.processor_exit_status = ProcessorExitStatus.Successful

        mock_processor2 = Mock(spec=Processor)
        mock_processor2.name = 'Processor2'
        mock_processor2.execute.return_value = None
        mock_processor2.processor_exit_status = ProcessorExitStatus.Successful

        mock_ui = Mock(spec=UserInterfaceBase)

        processor_list = ProcessorList(
            mock_processor1, mock_processor2, name='TestList', description='Test Description', user_interface=mock_ui
        )

        # Mock acquire_resources and distribute_resources
        with (
            patch.object(processor_list, 'acquire_resources'),
            patch.object(processor_list, 'distribute_resources') as mock_distribute,
        ):
            result = processor_list.execute()

            # Verify execution
            assert result == ProcessorExitStatus.Successful
            mock_processor1.execute.assert_called_once()
            mock_processor2.execute.assert_called_once()

            # Verify UI calls
            mock_ui.create_task.assert_called_once_with(
                'TestList', 'Test Description', completed=0, increment=0, total=2
            )
            assert mock_ui.update_task.call_count == 3  # 2 during execution + 1 final

            # Verify resource distribution
            assert mock_distribute.call_count == 2
            mock_distribute.assert_any_call(mock_processor1)
            mock_distribute.assert_any_call(mock_processor2)

            # Verify logging
            assert mock_log.info.call_count == 2

    @patch('mafw.processor.log')
    def test_execute_with_processor_list(self, mock_log):
        """Test execution with nested ProcessorList."""
        mock_nested_list = Mock(spec=ProcessorList)
        mock_nested_list.name = 'NestedList'
        mock_nested_list.execute.return_value = None
        mock_nested_list.processor_exit_status = ProcessorExitStatus.Successful

        mock_ui = Mock(spec=UserInterfaceBase)

        processor_list = ProcessorList(mock_nested_list, name='MainList', user_interface=mock_ui)

        with patch.object(processor_list, 'acquire_resources'), patch.object(processor_list, 'distribute_resources'):
            result = processor_list.execute()

            assert result == ProcessorExitStatus.Successful
            mock_nested_list.execute.assert_called_once()
            mock_log.info.assert_called_with('Executing [red]%s[/red] processor list' % 'NestedList')

    @patch('mafw.processor.log')
    def test_execute_processor_abort(self, mock_log):
        """Test execution when a processor aborts."""
        mock_processor1 = Mock(spec=Processor)
        mock_processor1.name = 'Processor1'
        mock_processor1.execute.return_value = None
        mock_processor1.processor_exit_status = ProcessorExitStatus.Successful

        mock_processor2 = Mock(spec=Processor)
        mock_processor2.name = 'Processor2'
        mock_processor2.execute.return_value = None
        mock_processor2.processor_exit_status = ProcessorExitStatus.Aborted

        mock_ui = Mock(spec=UserInterfaceBase)

        processor_list = ProcessorList(mock_processor1, mock_processor2, user_interface=mock_ui)

        with patch.object(processor_list, 'acquire_resources'), patch.object(processor_list, 'distribute_resources'):
            with pytest.raises(
                AbortProcessorException, match='Processor Processor2 caused the processor list to abort'
            ):
                processor_list.execute()

            # Verify both processors were executed
            mock_processor1.execute.assert_called_once()
            mock_processor2.execute.assert_called_once()

            # Verify error logging
            mock_log.error.assert_called_once()

    def test_execute_empty_list(self):
        """Test execution of empty processor list."""
        mock_ui = Mock(spec=UserInterfaceBase)
        processor_list = ProcessorList(user_interface=mock_ui)

        with patch.object(processor_list, 'acquire_resources'):
            result = processor_list.execute()

            assert result == ProcessorExitStatus.Successful
            mock_ui.create_task.assert_called_once_with(
                'ProcessorList', 'ProcessorList', completed=0, increment=0, total=0
            )
            mock_ui.update_task.assert_called_with('ProcessorList', completed=0, total=0)


class TestProcessorListEdgeCases:
    """Test edge cases and error conditions."""

    def test_init_with_none_values(self):
        """Test initialization filters out None values."""
        mock_processor = Mock(spec=Processor)
        processor_list = ProcessorList(mock_processor, None, None)

        assert len(processor_list) == 1
        assert processor_list[0] == mock_processor

    @pytest.mark.parametrize(
        'protocol,expected_params',
        [
            ('sqlite', {'pragmas': {'foreign_keys': 1}, 'timeout': 20}),
            ('postgresql', {'timeout': 20}),
            ('mysql', {'timeout': 20}),
        ],
    )
    @patch('mafw.processor.connect')
    @patch('mafw.processor.extract_protocol')
    @patch('mafw.processor.mafw_model_register')
    def test_acquire_resources_different_protocols(
        self, mock_register, mock_extract_protocol, mock_connect, protocol, expected_params
    ):
        """Test acquire_resources with different database protocols."""
        mock_extract_protocol.return_value = protocol
        mock_db = Mock(spec=peewee.Database)
        mock_connect.return_value = mock_db
        mock_table = Mock()
        mock_table.init = Mock()
        mock_register.get_model.return_value = [mock_table]

        db_conf = {'URL': f'{protocol}://test.db', 'timeout': 20, 'pragmas': {'foreign_keys': 1}}

        processor_list = ProcessorList(database_conf=db_conf)

        with patch('contextlib.ExitStack') as mock_exit_stack:
            mock_stack = Mock()
            mock_exit_stack.return_value.__enter__.return_value = mock_stack
            processor_list._resource_stack = mock_stack

            processor_list.acquire_resources()

            if protocol == 'sqlite':
                mock_connect.assert_called_once_with(f'{protocol}://test.db', **expected_params)
            else:
                mock_connect.assert_called_once_with(f'{protocol}://test.db', timeout=20)

    def test_database_conf_type1_vs_type2(self):
        """Test different database configuration formats."""
        # Type 1: wrapped in DBConfiguration
        db_conf_type1 = {'DBConfiguration': {'URL': 'sqlite:///test.db', 'timeout': 30}}

        # Type 2: direct configuration
        db_conf_type2 = {'URL': 'sqlite:///test.db', 'timeout': 30}

        processor_list1 = ProcessorList(database_conf=db_conf_type1)
        processor_list2 = ProcessorList(database_conf=db_conf_type2)

        # Both should be handled correctly
        assert processor_list1._database_conf == db_conf_type1
        assert processor_list2._database_conf == db_conf_type2


# Fixtures for common test objects
@pytest.fixture
def mock_processor():
    """Fixture for a mock processor."""
    processor = Mock(spec=Processor)
    processor.name = 'TestProcessor'
    processor.execute.return_value = None
    processor.processor_exit_status = ProcessorExitStatus.Successful
    return processor


@pytest.fixture
def mock_ui():
    """Fixture for a mock user interface."""
    return Mock(spec=UserInterfaceBase)


@pytest.fixture
def mock_timer():
    """Fixture for a mock timer."""
    return Mock(spec=Timer)


@pytest.fixture
def mock_database():
    """Fixture for a mock database."""
    return Mock(spec=peewee.Database)


@pytest.mark.integration_test
class TestProcessorListIntegration:
    """Integration tests for ProcessorList."""

    def test_full_lifecycle(self, mock_processor, mock_ui, mock_timer, mock_database):
        """Test the full lifecycle of a ProcessorList."""
        processor_list = ProcessorList(
            mock_processor,
            name='IntegrationTest',
            description='Integration test description',
            timer=mock_timer,
            user_interface=mock_ui,
            database=mock_database,
        )

        # Test all major operations
        assert len(processor_list) == 1
        assert processor_list.name == 'IntegrationTest'
        assert processor_list.database == mock_database

        # Add another processor
        mock_processor2 = Mock(spec=Processor)
        mock_processor2.name = 'Processor2'
        mock_processor2.processor_exit_status = ProcessorExitStatus.Successful
        processor_list.append(mock_processor2)

        assert len(processor_list) == 2

        # Test execution
        with patch.object(processor_list, 'acquire_resources'), patch.object(processor_list, 'distribute_resources'):
            result = processor_list.execute()

            assert result == ProcessorExitStatus.Successful
            mock_processor.execute.assert_called_once()
            mock_processor2.execute.assert_called_once()
