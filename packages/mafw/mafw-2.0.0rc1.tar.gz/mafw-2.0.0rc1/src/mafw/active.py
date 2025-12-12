#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
"""
Module implements active variable for classes.
"""

from __future__ import annotations

from typing import Generic, Type, TypeVar, cast

ActiveType = TypeVar('ActiveType')
"""A type for templating the Active class."""

ActivableType = TypeVar('ActivableType')
"""A type for  all classes that can include an Active."""


class Active(Generic[ActiveType]):
    """
    A descriptor class to make class variable **active**.

    When assigned to a class variable, any change of this value will trigger a call back to a specific function.

    Here is a clarifying example.

    .. code-block:: python

        class Person:
            age = Active()

            def __init__(self, age):
                self.age = age

            def on_age_change(self, old_value, new_value):
                # callback invoked every time the value of age is changed
                # do something with the old and the new age
                pass

            def on_age_set(self, value):
                # callback invoked every time the value on age is set to the same
                # value as before.
                pass

            def on_age_get(self, value):
                # callback invoked every time the value of age is asked.
                # not really useful, but...
                pass


    Once you have assigned an Active to a class member, you need to implement the callback in your class.
    If you do not implement them, the code will run without problems.

    The three callbacks have the signature described in the example.

        * on_[var_name]_change(self, old, new)
        * on_[var_name]_set(self, value)
        * on_[var_name]_get(self, value)
    """

    def __init__(self, default: ActiveType | None = None) -> None:
        """
        Constructor parameter:

        :param default: Initial value of the Active value. Defaults to None.
        :type default: ActiveType
        """
        self.default = default

        # the name of the three callbacks.
        # they will be assigned after we know the name of the variable.
        self._change_call_back_name: str
        self._set_callback_name: str
        self._get_callback_name: str

    def __set_name__(self, obj: Type[ActivableType], name: str) -> None:
        # this is the public name of the class variable
        self.public_name = name
        # this is the name where we will be storing the value in the owner class
        self.private_name = 'active_' + name

        # check if the owner does not have an attribute named after private name
        # if so create it and assign it the default value
        if not hasattr(obj, self.private_name):
            setattr(obj, self.private_name, self.default)

        # now you can prepare the name for the callbacks
        self._init_callbacks()

    def _init_callbacks(self) -> None:
        # now we know the name of the variable, so we can create the callback names as well
        self._change_callback_name = f'on_{self.public_name}_change'
        self._set_callback_name = f'on_{self.public_name}_set'
        self._get_callback_name = f'on_{self.public_name}_get'

    def __get__(self, obj: ActivableType, obj_type: Type[ActivableType]) -> Active[ActiveType] | ActiveType:
        if obj is None:
            # obj is None means that we are invoking the descriptor via the class and not the instance
            # in this case we cannot return the private value and we return the descriptor itself.
            return self

        # if the object does not have an attribute named with our private_name, it means this is the first use.
        # we need to initialize the descriptor
        if not hasattr(obj, self.private_name):
            setattr(obj, self.private_name, self.default)

        # the value is stored in the private_name attribute.
        value = getattr(obj, self.private_name)

        # check if there is a get callback and if yes call it
        if hasattr(obj, self._get_callback_name):
            getattr(obj, self._get_callback_name)(value)

        return cast(ActiveType, value)

    def __set__(self, obj: ActivableType, value: ActiveType) -> None:
        # this is the current value
        current_value = getattr(obj, self.private_name)
        # now set the new value
        setattr(obj, self.private_name, value)

        if current_value != value:
            # the value really changed, call the change callback if it exists:
            if hasattr(obj, self._change_callback_name):
                getattr(obj, self._change_callback_name)(current_value, value)
        else:
            # the value did not change, but it was set anyhow. call the set callback if it exists
            if hasattr(obj, self._set_callback_name):
                getattr(obj, self._set_callback_name)(value)
