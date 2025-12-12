#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
import pytest

from mafw.active import Active


class TestActive:
    def setup_method(self):
        class TestClass:
            variable = Active(default=0)

            def on_variable_change(self, old_value, new_value):
                self.change_called = True
                self.old_value = old_value
                self.new_value = new_value

            def on_variable_set(self, value):
                self.set_called = True
                self.set_value = value

            def on_variable_get(self, value):
                self.get_called = True
                self.get_value = value

        self.test_obj = TestClass()

    @pytest.mark.parametrize(
        'initial, new, expected_change_call',
        [
            (0, 1, True),
            (1, 1, False),
            (5, 10, True),
        ],
    )
    def test_change_callback(self, initial, new, expected_change_call):
        self.test_obj.variable = initial
        self.test_obj.change_called = False
        self.test_obj.variable = new
        assert self.test_obj.change_called == expected_change_call

    @pytest.mark.parametrize(
        'initial, new, expected_set_call',
        [
            (0, 1, False),
            (1, 1, True),
            (5, 5, True),
        ],
    )
    def test_set_callback(self, initial, new, expected_set_call):
        self.test_obj.variable = initial
        self.test_obj.set_called = False
        self.test_obj.variable = new
        assert self.test_obj.set_called == expected_set_call

    @pytest.mark.parametrize('initial', [0, 1, 10])
    def test_get_callback(self, initial):
        self.test_obj.variable = initial
        self.test_obj.get_called = False
        _ = self.test_obj.variable
        assert self.test_obj.get_called

    def test_default_value(self):
        assert self.test_obj.variable == 0
