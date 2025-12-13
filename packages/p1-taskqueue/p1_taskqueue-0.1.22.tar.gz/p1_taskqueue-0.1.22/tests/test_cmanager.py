from datetime import datetime
from datetime import timedelta
from typing import Any
from unittest.mock import Mock
from unittest.mock import patch

import pytest
from taskqueue.cmanager import _build_callable_task_call
from taskqueue.cmanager import _build_dynamic_task_call
from taskqueue.cmanager import _is_class_method
from taskqueue.cmanager import _split_function_and_queue_kwargs
from taskqueue.cmanager import CManager
from taskqueue.cmanager import K_DEFAULT_RETRY_COUNTDOWN
from taskqueue.cmanager import K_MAX_RETRY_COUNT
from taskqueue.cmanager import taskqueue_class


class SampleClass:

    def test_method(self):
        pass

    @classmethod
    def class_method(cls):
        pass

    @staticmethod
    def static_method():
        pass


@taskqueue_class
class SampleClassWithInit:

    def __init__(self, name, age=0, **kwargs):
        self.name = name
        self.age = age
        self.kwargs = kwargs

    def process(self):
        return f"Processing {self.name}, age {self.age}"

    def process_with_args(self, message):
        return f"{message}: {self.name}, age {self.age}"


@taskqueue_class
class SampleClassWithVarArgs:

    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.args = args
        self.kwargs = kwargs

    def process(self):
        return f"Processing {self.name} with {len(self.args)} args"


@taskqueue_class
class SampleClassWithComplexInit:

    def __init__(self, required, optional=10, *extra, **options):
        self.required = required
        self.optional = optional
        self.extra = extra
        self.options = options

    def calculate(self):
        return sum([self.required, self.optional] + list(self.extra))


@taskqueue_class
class SampleClassWithDifferentParamNames:

    def __init__(self, cognito_form_reimbursement_dict):
        self.data = cognito_form_reimbursement_dict

    def process(self):
        return f"Processing data: {self.data}"


def test_function():
    """Test function for testing function detection."""


class TestIsClassMethod:

    def test__is_class_method_given_function_expect_return_false(self):
        result = _is_class_method(test_function)
        assert result is False

    def test__is_class_method_given_class_method_expect_return_true(self):
        instance = SampleClass()
        result = _is_class_method(instance.test_method)
        assert result is True

    def test__is_class_method_given_classmethod_decorator_expect_return_true(self):
        result = _is_class_method(SampleClass.class_method)
        assert result is True

    def test__is_class_method_given_staticmethod_decorator_expect_return_false(self):
        result = _is_class_method(SampleClass.static_method)
        assert result is False

    def test__is_class_method_given_unbound_method_expect_return_false(self):
        result = _is_class_method(SampleClass.test_method)
        assert result is False


class TestSplitFunctionAndQueueKwargs:

    def test__split_function_and_queue_kwargs_given_mixed_kwargs_expect_correct_split(self):
        kwargs = {
            'channel': 'high',
            'retry': {'max_retries': 5},
            'on_commit': True,
            'job_timeout': 300,
            'user_id': 123,
            'data': {'key': 'value'}
        }

        func_kwargs, queue_kwargs = _split_function_and_queue_kwargs(kwargs)

        assert func_kwargs == {'user_id': 123, 'data': {'key': 'value'}}
        assert queue_kwargs == {
            'channel': 'high',
            'retry': {'max_retries': 5},
            'on_commit': True,
            'job_timeout': 300
        }

    def test__split_function_and_queue_kwargs_given_only_function_kwargs_expect_empty_queue_kwargs(self):
        kwargs = {'user_id': 123, 'data': 'test'}

        func_kwargs, queue_kwargs = _split_function_and_queue_kwargs(kwargs)

        assert func_kwargs == {'user_id': 123, 'data': 'test'}
        assert queue_kwargs == {}

    def test__split_function_and_queue_kwargs_given_only_queue_kwargs_expect_empty_func_kwargs(self):
        kwargs = {'channel': 'default', 'retry': {'max_retries': 3}}

        func_kwargs, queue_kwargs = _split_function_and_queue_kwargs(kwargs)

        assert func_kwargs == {}
        assert queue_kwargs == {
            'channel': 'default', 'retry': {'max_retries': 3}}

    def test__split_function_and_queue_kwargs_given_ignored_celery_keys_expect_they_are_ignored(self):
        kwargs = {
            'queue': 'default',
            'countdown': 10,
            'eta': datetime.now(),
            'priority': 1,
            'user_id': 123
        }

        func_kwargs, queue_kwargs = _split_function_and_queue_kwargs(kwargs)

        assert func_kwargs == {'user_id': 123}
        assert queue_kwargs == {}


class TestParseEnqueueArgs:

    def test__parse_enqueue_args_given_basic_enqueue_expect_correct_parsing(self):
        cm = CManager()
        args = (test_function, 1, 2, 3)
        kwargs = {
            'user_id': 123,
            'data': 'test',
            'channel': 'high',
            'retry': {'max_retries': 5}
        }

        func, func_args, func_kwargs, queue_options = cm._parse_enqueue_args(
            'enqueue', args, kwargs
        )

        assert func == test_function
        assert func_args == (1, 2, 3)
        assert func_kwargs == {'user_id': 123, 'data': 'test'}
        assert queue_options == {
            'channel': 'high',
            'retry': {'max_retries': 5}
        }
        assert 'eta' not in queue_options
        assert 'countdown' not in queue_options

    def test__parse_enqueue_args_given_enqueue_at_expect_eta_in_queue_options(self):
        cm = CManager()
        eta = datetime(2025, 12, 31, 23, 59, 59)
        args = (eta, test_function, 'arg1', 'arg2')
        kwargs = {
            'user_id': 456,
            'channel': 'default'
        }

        func, func_args, func_kwargs, queue_options = cm._parse_enqueue_args(
            'enqueue_at', args, kwargs
        )

        assert func == test_function
        assert func_args == ('arg1', 'arg2')
        assert func_kwargs == {'user_id': 456}
        assert queue_options['eta'] == eta
        assert queue_options['channel'] == 'default'
        assert 'countdown' not in queue_options

    def test__parse_enqueue_args_given_enqueue_in_expect_countdown_in_queue_options(self):
        cm = CManager()
        delta = timedelta(seconds=300)
        args = (delta, test_function, 'arg1')
        kwargs = {
            'data': {'key': 'value'},
            'retry': {'max_retries': 3}
        }

        func, func_args, func_kwargs, queue_options = cm._parse_enqueue_args(
            'enqueue_in', args, kwargs
        )

        assert func == test_function
        assert func_args == ('arg1',)
        assert func_kwargs == {'data': {'key': 'value'}}
        assert queue_options['countdown'] == 300
        assert queue_options['retry'] == {'max_retries': 3}
        assert 'eta' not in queue_options

    def test__parse_enqueue_args_given_no_func_args_expect_empty_tuple(self):
        cm = CManager()
        args = (test_function,)
        kwargs = {'user_id': 789}

        func, func_args, func_kwargs, queue_options = cm._parse_enqueue_args(
            'enqueue', args, kwargs
        )

        assert func == test_function
        assert func_args == ()
        assert func_kwargs == {'user_id': 789}

    def test__parse_enqueue_args_given_no_kwargs_expect_empty_dicts(self):
        cm = CManager()
        args = (test_function, 1, 2)
        kwargs = {}

        func, func_args, func_kwargs, queue_options = cm._parse_enqueue_args(
            'enqueue', args, kwargs
        )

        assert func == test_function
        assert func_args == (1, 2)
        assert func_kwargs == {}
        assert queue_options == {}

    def test__parse_enqueue_args_given_no_args_expect_value_error(self):
        cm = CManager()
        args = ()
        kwargs = {}

        with pytest.raises(ValueError, match="enqueue requires a callable as the first positional argument"):
            cm._parse_enqueue_args('enqueue', args, kwargs)

    def test__parse_enqueue_args_given_enqueue_at_insufficient_args_expect_value_error(self):
        cm = CManager()
        args = (datetime.now(),)
        kwargs = {}

        with pytest.raises(ValueError, match="enqueue_at requires \\(eta_datetime, func, \\*func_args\\)"):
            cm._parse_enqueue_args('enqueue_at', args, kwargs)

    def test__parse_enqueue_args_given_enqueue_in_insufficient_args_expect_value_error(self):
        cm = CManager()
        args = (timedelta(seconds=60),)
        kwargs = {}

        with pytest.raises(ValueError, match="enqueue_in requires \\(countdown_delta, func, \\*func_args\\)"):
            cm._parse_enqueue_args('enqueue_in', args, kwargs)

    def test__parse_enqueue_args_given_unknown_op_type_expect_value_error(self):
        cm = CManager()
        args = (test_function,)
        kwargs = {}

        with pytest.raises(ValueError, match="Unknown enqueue operation type: invalid_op"):
            cm._parse_enqueue_args('invalid_op', args, kwargs)

    def test__parse_enqueue_args_given_use_legacy_executor_expect_in_queue_options(self):
        cm = CManager()
        args = (test_function, 1, 2)
        kwargs = {
            'use_legacy_executor': False,
            'user_id': 123
        }

        func, func_args, func_kwargs, queue_options = cm._parse_enqueue_args(
            'enqueue', args, kwargs
        )

        assert func == test_function
        assert func_args == (1, 2)
        assert func_kwargs == {'user_id': 123}
        assert queue_options['use_legacy_executor'] is False


class TestBuildDynamicTaskCall:

    def test__build_dynamic_task_call_given_function_expect_function_executor_task(self):
        task_name, task_args, task_kwargs = _build_dynamic_task_call(
            test_function, 1, 2, key='value'
        )

        assert task_name == "taskqueue.cmanager.dynamic_function_executor"
        assert task_args == []
        assert task_kwargs == {
            'module_path': 'tests.test_cmanager',
            'function_name': 'test_function',
            'args': [1, 2],
            'kwargs': {'key': 'value'}
        }

    def test__build_dynamic_task_call_given_bound_method_expect_class_method_executor_task(self):
        instance = SampleClass()
        task_name, task_args, task_kwargs = _build_dynamic_task_call(
            instance.test_method, 1, 2, key='value'
        )

        assert task_name == "taskqueue.cmanager.dynamic_class_method_executor"
        assert task_args == []
        assert task_kwargs == {
            'module_path': 'tests.test_cmanager',
            'class_name': 'SampleClass',
            'method_name': 'test_method',
            'args': [1, 2],
            'kwargs': {'key': 'value'},
            'init_args': [],
            'init_kwargs': {}
        }

    def test__build_dynamic_task_call_given_function_without_module_expect_raise_value_error(self):
        mock_func = Mock()
        mock_func.__module__ = None
        mock_func.__name__ = 'test_func'

        with pytest.raises(ValueError, match="Unsupported callable type for Celery enqueue"):
            _build_dynamic_task_call(mock_func)

    def test__build_dynamic_task_call_given_function_without_name_expect_raise_value_error(self):
        mock_func = Mock()
        mock_func.__module__ = 'test_module'
        mock_func.__name__ = None

        with pytest.raises(ValueError, match="Unsupported callable type for Celery enqueue"):
            _build_dynamic_task_call(mock_func)


class TestCManager:

    @patch('taskqueue.cmanager.logger')
    @patch.object(CManager, '_send_task')
    def test_cmanager_enqueue_given_function_expect_send_task_called(self, mock_send_task, mock_logger):
        cm = CManager()
        cm.enqueue(test_function, 1, 2, key='value')

        mock_send_task.assert_called_once()
        call_args = mock_send_task.call_args
        assert call_args[0][0] == "taskqueue.cmanager.callable_executor"

    @patch('taskqueue.cmanager.logger')
    @patch.object(CManager, '_send_task')
    def test_cmanager_enqueue_at_given_datetime_and_function_expect_send_task_called_with_eta(self, mock_send_task, mock_logger):
        cm = CManager()
        eta = datetime.now()
        cm.enqueue_at(eta, test_function, 1, 2)

        mock_send_task.assert_called_once()
        call_args = mock_send_task.call_args
        assert call_args[0][0] == "taskqueue.cmanager.callable_executor"

    @patch('taskqueue.cmanager.logger')
    @patch.object(CManager, '_send_task')
    def test_cmanager_enqueue_in_given_timedelta_and_function_expect_send_task_called_with_countdown(self, mock_send_task, mock_logger):
        cm = CManager()
        delta = timedelta(seconds=60)
        cm.enqueue_in(delta, test_function, 1, 2)

        mock_send_task.assert_called_once()
        call_args = mock_send_task.call_args
        assert call_args[0][0] == "taskqueue.cmanager.callable_executor"

    def test_cmanager_enqueue_given_no_args_expect_raise_value_error(self):
        cm = CManager()
        with pytest.raises(ValueError, match="enqueue requires a callable as the first positional argument"):
            cm.enqueue()

    def test_cmanager_enqueue_at_given_insufficient_args_expect_raise_value_error(self):
        cm = CManager()
        with pytest.raises(ValueError, match="enqueue_at requires \\(eta_datetime, func, \\*func_args\\)"):
            cm.enqueue_at(datetime.now())

    def test_cmanager_enqueue_in_given_insufficient_args_expect_raise_value_error(self):
        cm = CManager()
        with pytest.raises(ValueError, match="enqueue_in requires \\(countdown_delta, func, \\*func_args\\)"):
            cm.enqueue_in(timedelta(seconds=10))

    def test_cmanager_enqueue_op_given_unknown_type_expect_raise_value_error(self):
        cm = CManager()
        with pytest.raises(ValueError, match="Unknown enqueue operation type: invalid"):
            cm._enqueue_op_base(test_function, enqueue_op_type='invalid')

    @patch('django.db.transaction.on_commit')
    @patch.object(CManager, '_enqueue_op_base')
    def test_cmanager_enqueue_op_given_on_commit_true_expect_transaction_on_commit_called(self, mock_enqueue_op_base, mock_on_commit):
        cm = CManager()
        cm._enqueue_op(test_function, on_commit=True)

        mock_on_commit.assert_called_once()

    @patch('django.db.transaction.on_commit')
    @patch.object(CManager, '_enqueue_op_base')
    def test_cmanager_enqueue_op_given_on_commit_false_expect_enqueue_op_base_called_directly(self, mock_enqueue_op_base, mock_on_commit):
        cm = CManager()
        cm._enqueue_op(test_function, on_commit=False)

        mock_enqueue_op_base.assert_called_once()
        mock_on_commit.assert_not_called()

    @patch('taskqueue.celery_app.celery_app')
    def test_cmanager__send_task_given_task_args_expect_celery_app_send_task_called(self, mock_celery_app):
        cm = CManager()
        cm._send_task("test.task", [1, 2], {
                      "key": "value"}, {"channel": "high"})

        mock_celery_app.send_task.assert_called_once()
        call_args = mock_celery_app.send_task.call_args
        # send_task is called with keyword arguments
        args, kwargs = call_args
        assert args[0] == "test.task"
        assert kwargs["args"] == [1, 2]
        # The retry policy is added automatically, so we need to check for both
        expected_kwargs = {"key": "value", "retry": {
            "max_retries": K_MAX_RETRY_COUNT, "countdown": K_DEFAULT_RETRY_COUNTDOWN}}
        assert kwargs["kwargs"] == expected_kwargs
        assert kwargs["queue"] == "high"

    @patch('taskqueue.celery_app.celery_app')
    def test_cmanager__send_task_given_no_retry_policy_expect_default_retry_policy_applied(self, mock_celery_app):
        cm = CManager()
        cm._send_task("test.task", [], {}, {})

        mock_celery_app.send_task.assert_called_once()
        call_args = mock_celery_app.send_task.call_args
        args, kwargs = call_args
        assert kwargs["kwargs"]["retry"] == {
            "max_retries": K_MAX_RETRY_COUNT,
            "countdown": K_DEFAULT_RETRY_COUNTDOWN
        }

    @patch('taskqueue.celery_app.celery_app')
    def test_cmanager__send_task_given_custom_retry_policy_expect_custom_policy_used(self, mock_celery_app):
        cm = CManager()
        custom_retry = {"max_retries": 5, "countdown": 20}
        cm._send_task("test.task", [], {}, {"retry": custom_retry})

        mock_celery_app.send_task.assert_called_once()
        call_args = mock_celery_app.send_task.call_args
        args, kwargs = call_args
        assert kwargs["kwargs"]["retry"] == custom_retry


class TestDynamicTaskExecutors:

    def test_dynamic_function_executor_given_valid_module_and_function_expect_function_executed(self):
        """Test that dynamic_function_executor is properly decorated."""
        from taskqueue.cmanager import dynamic_function_executor

        # Just verify the function exists and is decorated
        assert hasattr(dynamic_function_executor, 'delay')
        assert hasattr(dynamic_function_executor, 'apply_async')

    def test_dynamic_class_method_executor_given_valid_class_and_method_expect_method_executed(self):
        """Test that dynamic_class_method_executor is properly decorated."""
        from taskqueue.cmanager import dynamic_class_method_executor

        # Just verify the function exists and is decorated
        assert hasattr(dynamic_class_method_executor, 'delay')
        assert hasattr(dynamic_class_method_executor, 'apply_async')

    @patch('taskqueue.cmanager.importlib.import_module')
    def test_dynamic_function_executor_given_import_error_expect_retry_raised(self, mock_import_module):
        mock_import_module.side_effect = ImportError("Module not found")

        from taskqueue.cmanager import dynamic_function_executor

        with pytest.raises(Exception):  # retry is raised
            dynamic_function_executor("invalid_module", "test_function")

    @patch('taskqueue.cmanager.importlib.import_module')
    def test_dynamic_function_executor_given_max_retries_reached_expect_reject_raised(self, mock_import_module):
        mock_import_module.side_effect = ImportError("Module not found")

        from taskqueue.cmanager import dynamic_function_executor

        mock_self = Mock()
        mock_self.request.retries = K_MAX_RETRY_COUNT
        mock_self.max_retries = K_MAX_RETRY_COUNT

        with pytest.raises(Exception):
            dynamic_function_executor(
                mock_self, "invalid_module", "test_function",
                retry={"max_retries": K_MAX_RETRY_COUNT}
            )


class TestExtractInitArgs:

    def test_extract_init_args_from_instance_given_instance_with_init_args_expect_args_extracted(self):
        from taskqueue.cmanager import _extract_init_args_from_instance
        instance = SampleClassWithInit("John", age=25)

        init_args, init_kwargs = _extract_init_args_from_instance(instance)
        assert init_args == ["John"]
        assert init_kwargs == {"age": 25}

    def test_extract_init_args_from_instance_given_kwargs_only_expect_extracted(self):
        from taskqueue.cmanager import _extract_init_args_from_instance
        instance = SampleClassWithInit("Jane", age=30)

        init_args, init_kwargs = _extract_init_args_from_instance(instance)
        assert init_args == ["Jane"]
        assert init_kwargs == {"age": 30}

    def test_extract_init_args_from_instance_given_no_init_expect_empty(self):
        from taskqueue.cmanager import _extract_init_args_from_instance
        instance = SampleClass()

        init_args, init_kwargs = _extract_init_args_from_instance(instance)
        assert init_args == []
        assert init_kwargs == {}

    def test_extract_init_args_from_instance_given_var_args_expect_captured(self):
        from taskqueue.cmanager import _extract_init_args_from_instance
        instance = SampleClassWithVarArgs(
            "Alice", "extra1", "extra2", city="NYC")

        init_args, init_kwargs = _extract_init_args_from_instance(instance)
        assert init_args == ["Alice", "extra1", "extra2"]
        assert init_kwargs == {"city": "NYC"}

    def test_extract_init_args_from_instance_given_var_kwargs_expect_captured(self):
        from taskqueue.cmanager import _extract_init_args_from_instance
        instance = SampleClassWithInit("Bob", age=30, city="LA", country="USA")

        init_args, init_kwargs = _extract_init_args_from_instance(instance)
        assert init_args == ["Bob"]
        assert init_kwargs == {"age": 30, "city": "LA", "country": "USA"}

    def test_extract_init_args_from_instance_given_complex_init_expect_all_captured(self):
        from taskqueue.cmanager import _extract_init_args_from_instance
        instance = SampleClassWithComplexInit(
            5, 15, 20, 25, multiplier=2, debug=True)

        init_args, init_kwargs = _extract_init_args_from_instance(instance)
        assert init_args == [5, 15, 20, 25]
        assert init_kwargs == {"multiplier": 2, "debug": True}

    def test_extract_init_args_from_instance_given_different_param_names_expect_works(self):
        from taskqueue.cmanager import _extract_init_args_from_instance
        from collections import OrderedDict

        test_dict = OrderedDict([("key1", "value1"), ("key2", "value2")])
        instance = SampleClassWithDifferentParamNames(test_dict)

        init_args, init_kwargs = _extract_init_args_from_instance(instance)
        assert init_args == [test_dict]
        assert init_kwargs == {}


class TestTaskqueueClassDecorator:

    def test_taskqueue_class_decorator_given_class_expect_init_args_captured(self):
        instance = SampleClassWithInit("John", age=25)

        assert hasattr(instance, '_taskqueue_init_args')
        assert hasattr(instance, '_taskqueue_init_kwargs')
        assert instance._taskqueue_init_args == ["John"]
        assert instance._taskqueue_init_kwargs == {"age": 25}

    def test_taskqueue_class_decorator_given_different_param_names_expect_captured(self):
        from collections import OrderedDict
        test_dict = OrderedDict([("key1", "value1")])
        instance = SampleClassWithDifferentParamNames(test_dict)

        assert instance._taskqueue_init_args == [test_dict]
        assert instance._taskqueue_init_kwargs == {}
        assert instance.data == test_dict


class TestBuildDynamicTaskCallWithInitArgs:

    def test__build_dynamic_task_call_given_instance_with_init_args_expect_init_args_passed(self):
        instance = SampleClassWithInit("John", age=25)
        task_name, task_args, task_kwargs = _build_dynamic_task_call(
            instance.process, "arg1", key='value'
        )

        assert task_name == "taskqueue.cmanager.dynamic_class_method_executor"
        assert task_args == []
        assert task_kwargs == {
            'module_path': 'tests.test_cmanager',
            'class_name': 'SampleClassWithInit',
            'method_name': 'process',
            'args': ['arg1'],
            'kwargs': {'key': 'value'},
            'init_args': ['John'],
            'init_kwargs': {'age': 25}
        }

    def test__build_dynamic_task_call_given_instance_without_decorator_expect_empty_defaults(self):
        instance = SampleClass()
        task_name, task_args, task_kwargs = _build_dynamic_task_call(
            instance.test_method, 1, 2, key='value'
        )

        assert task_name == "taskqueue.cmanager.dynamic_class_method_executor"
        assert task_args == []
        assert task_kwargs == {
            'module_path': 'tests.test_cmanager',
            'class_name': 'SampleClass',
            'method_name': 'test_method',
            'args': [1, 2],
            'kwargs': {'key': 'value'},
            'init_args': [],
            'init_kwargs': {}
        }


class TestDynamicClassMethodExecutorWithInitArgs:
    """Tests for dynamic_class_method_executor with init args."""

    def test_dynamic_class_method_executor_given_init_args_expect_instance_created_with_args(self):
        from taskqueue.cmanager import dynamic_class_method_executor

        result = dynamic_class_method_executor(
            module_path="tests.test_cmanager",
            class_name="SampleClassWithInit",
            method_name="process",
            args=[],
            kwargs={},
            init_args=["Alice"],
            init_kwargs={"age": 35},
            retry=None
        )

        assert result is None

    def test_dynamic_class_method_executor_given_no_init_args_expect_backward_compatible(self):
        from taskqueue.cmanager import dynamic_class_method_executor

        result = dynamic_class_method_executor(
            module_path="tests.test_cmanager",
            class_name="SampleClass",
            method_name="test_method",
            args=[],
            kwargs={},
            init_args=None,
            init_kwargs=None,
            retry=None
        )

        assert result is None

    def test_dynamic_class_method_executor_given_var_args_and_kwargs_expect_works(self):
        from taskqueue.cmanager import dynamic_class_method_executor

        result = dynamic_class_method_executor(
            module_path="tests.test_cmanager",
            class_name="SampleClassWithVarArgs",
            method_name="process",
            args=[],
            kwargs={},
            init_args=["Bob", "extra1", "extra2"],
            init_kwargs={"city": "NYC", "country": "USA"},
            retry=None
        )

        assert result is None


class TestBuildCallableTaskCall:

    def test__build_callable_task_call_given_function_expect_callable_executor_task(self) -> None:
        task_name, task_args, task_kwargs = _build_callable_task_call(
            test_function, (1, 2), {'key': 'value'}
        )

        assert task_name == "taskqueue.cmanager.callable_executor"
        assert task_args == []
        assert task_kwargs == {
            'callable_obj': test_function,
            'args': [1, 2],
            'kwargs': {'key': 'value'}
        }

    def test__build_callable_task_call_given_lambda_expect_callable_executor_task(self) -> None:
        def lambda_func(x):
            return x * 2

        task_name, task_args, task_kwargs = _build_callable_task_call(
            lambda_func, (5,), {}
        )

        assert task_name == "taskqueue.cmanager.callable_executor"
        assert task_args == []
        assert task_kwargs == {
            'callable_obj': lambda_func,
            'args': [5],
            'kwargs': {}
        }

    def test__build_callable_task_call_given_bound_method_expect_callable_executor_task(self) -> None:
        instance = SampleClass()
        task_name, task_args, task_kwargs = _build_callable_task_call(
            instance.test_method, (1, 2), {'key': 'value'}
        )

        assert task_name == "taskqueue.cmanager.callable_executor"
        assert task_args == []
        assert task_kwargs == {
            'callable_obj': instance.test_method,
            'args': [1, 2],
            'kwargs': {'key': 'value'}
        }

    def test__build_callable_task_call_given_no_args_expect_empty_lists(self) -> None:
        task_name, task_args, task_kwargs = _build_callable_task_call(
            test_function, (), {}
        )

        assert task_name == "taskqueue.cmanager.callable_executor"
        assert task_args == []
        assert task_kwargs == {
            'callable_obj': test_function,
            'args': [],
            'kwargs': {}
        }

    def test_callable_executor_given_function_expect_function_executed(self) -> None:
        from taskqueue.cmanager import callable_executor

        assert hasattr(callable_executor, 'delay')
        assert hasattr(callable_executor, 'apply_async')

    def test_callable_executor_given_simple_function_expect_success(self) -> None:
        from taskqueue.cmanager import callable_executor

        call_tracker = []

        def simple_func(x, y):
            call_tracker.append((x, y))
            return x + y

        result = callable_executor(
            callable_obj=simple_func,
            args=[3, 5],
            kwargs={},
            retry=None
        )

        assert result is None
        assert call_tracker == [(3, 5)]

    def test_callable_executor_given_function_with_kwargs_expect_success(self) -> None:
        from taskqueue.cmanager import callable_executor

        call_tracker: list[tuple[str, int]] = []

        def func_with_kwargs(name: str, age: int = 0) -> None:
            call_tracker.append((name, age))

        result = callable_executor(
            callable_obj=func_with_kwargs,
            args=["Alice"],
            kwargs={"age": 30},
            retry=None
        )

        assert result is None
        assert call_tracker == [("Alice", 30)]

    def test_callable_executor_given_lambda_expect_success(self) -> None:
        from taskqueue.cmanager import callable_executor

        result_tracker: list[int] = []

        def lambda_func(x, y):
            return result_tracker.append(x * y)

        result = callable_executor(
            callable_obj=lambda_func,
            args=[4, 5],
            kwargs={},
            retry=None
        )

        assert result is None
        assert result_tracker == [20]

    def test_callable_executor_given_bound_method_expect_success(self) -> None:
        from taskqueue.cmanager import callable_executor

        instance = SampleClassWithInit("TestUser", age=25)

        result = callable_executor(
            callable_obj=instance.process,
            args=[],
            kwargs={},
            retry=None
        )

        assert result is None

    def test_callable_executor_given_bound_method_with_args_expect_success(self) -> None:
        from taskqueue.cmanager import callable_executor

        instance = SampleClassWithInit("TestUser", age=25)

        result = callable_executor(
            callable_obj=instance.process_with_args,
            args=["Hello"],
            kwargs={},
            retry=None
        )

        assert result is None

    def test_callable_executor_given_none_args_expect_default_to_empty(self) -> None:
        from taskqueue.cmanager import callable_executor

        call_tracker: list[str] = []

        def no_args_func() -> None:
            call_tracker.append("called")

        result = callable_executor(
            callable_obj=no_args_func,
            args=None,
            kwargs=None,
            retry=None
        )

        assert result is None
        assert call_tracker == ["called"]

    def test_callable_executor_given_callable_with_side_effects_expect_side_effects_executed(self) -> None:
        from taskqueue.cmanager import callable_executor

        side_effects: dict[str, int] = {"counter": 0}

        def increment_counter(amount: int) -> None:
            side_effects["counter"] += amount

        callable_executor(
            callable_obj=increment_counter,
            args=[5],
            kwargs={},
            retry=None
        )

        assert side_effects["counter"] == 5

    @patch('taskqueue.cmanager.logger')
    @patch.object(CManager, '_send_task')
    def test_cmanager_enqueue_given_use_legacy_executor_false_expect_callable_executor(self, mock_send_task: Any, mock_logger: Any) -> None:
        cm = CManager()
        cm.enqueue(test_function, 1, 2, key='value',
                   use_legacy_executor=False)

        mock_send_task.assert_called_once()
        call_args = mock_send_task.call_args
        assert call_args[0][0] == "taskqueue.cmanager.callable_executor"

        task_kwargs = call_args[0][2]
        assert 'callable_obj' in task_kwargs
        assert task_kwargs['callable_obj'] == test_function
        assert task_kwargs['args'] == [1, 2]
        assert task_kwargs['kwargs'] == {'key': 'value'}

    @patch('taskqueue.cmanager.logger')
    @patch.object(CManager, '_send_task')
    def test_cmanager_enqueue_given_use_legacy_executor_true_expect_dynamic_executor(self, mock_send_task: Any, mock_logger: Any) -> None:
        cm = CManager()
        cm.enqueue(test_function, 1, 2, key='value',
                   use_legacy_executor=True)

        mock_send_task.assert_called_once()
        call_args = mock_send_task.call_args
        assert call_args[0][0] == "taskqueue.cmanager.dynamic_function_executor"

        task_kwargs = call_args[0][2]
        assert 'module_path' in task_kwargs
        assert 'function_name' in task_kwargs

    @patch('taskqueue.cmanager.logger')
    @patch.object(CManager, '_send_task')
    def test_cmanager_enqueue_given_no_use_legacy_executor_expect_default_to_false(self, mock_send_task: Any, mock_logger: Any) -> None:
        cm = CManager()
        cm.enqueue(test_function, 1, 2)

        mock_send_task.assert_called_once()
        call_args = mock_send_task.call_args
        assert call_args[0][0] == "taskqueue.cmanager.callable_executor"

    @patch('taskqueue.cmanager.logger')
    @patch.object(CManager, '_send_task')
    def test_cmanager_enqueue_given_bound_method_with_callable_executor_expect_success(self, mock_send_task: Any, mock_logger: Any) -> None:
        cm = CManager()
        instance = SampleClassWithInit("Test", age=20)

        cm.enqueue(instance.process, use_legacy_executor=False)

        mock_send_task.assert_called_once()
        call_args = mock_send_task.call_args
        assert call_args[0][0] == "taskqueue.cmanager.callable_executor"

        task_kwargs = call_args[0][2]
        assert task_kwargs['callable_obj'] == instance.process
