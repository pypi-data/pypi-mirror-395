# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: Zlib

import unittest

import utlx
from utlx import cached, cached_property


class TestCachedDecorators(unittest.TestCase):

    def test_cached_method_caches_result(self):
        class Example:
            def __init__(self):
                self.counter = 0

            @cached
            def compute(self):
                self.counter += 1
                return self.counter

        obj = Example()
        result1 = obj.compute()
        result2 = obj.compute()
        self.assertEqual(result1, result2)
        self.assertEqual(obj.counter, 1)

    def test_cached_method_initializes_cache(self):
        class Example:
            @cached
            def value(self):
                return 42

        obj = Example()
        self.assertFalse(hasattr(obj, '__cache__'))
        val = obj.value()
        self.assertTrue(hasattr(obj, '__cache__'))
        self.assertEqual(val, 42)

    def test_cached_property_basic_usage(self):
        class Example:
            def __init__(self):
                self.counter = 0

            @cached_property
            def prop(self):
                self.counter += 1
                return self.counter

        obj = Example()
        val1 = obj.prop
        val2 = obj.prop
        self.assertEqual(val1, val2)
        self.assertEqual(obj.counter, 1)

    def test_cached_property_with_setter_and_deleter(self):
        class Example:
            def __init__(self):
                self._value = 10

            def get(self):
                return self._value

            def set(self, val):
                self._value = val

            def delete(self):
                self._value = None

            prop = cached_property(get, set, delete, doc="cached prop")

        obj = Example()
        self.assertEqual(obj.prop, 10)
        obj.prop = 20
        self.assertEqual(obj.prop, 20)
        del obj.prop
        self.assertIsNone(obj._value)

    def test_cached_property_with_setter_and_deleter_first_set(self):
        class Example:
            def __init__(self):
                self._value = 10

            def get(self):
                return self._value

            def set(self, val):
                self._value = val

            def delete(self):
                self._value = None

            prop = cached_property(get, set, delete, doc="cached prop")

        obj = Example()
        obj.prop = 20
        self.assertEqual(obj.prop, 20)
        del obj.prop
        self.assertIsNone(obj._value)

    def test_cached_property_with_setter_and_deleter_first_delete(self):
        class Example:
            def __init__(self):
                self._value = 10

            def get(self):
                return self._value

            def set(self, val):
                self._value = val

            def delete(self):
                self._value = None

            prop = cached_property(get, set, delete, doc="cached prop")

        obj = Example()
        del obj.prop
        self.assertIsNone(obj._value)
        obj.prop = 20
        self.assertEqual(obj.prop, 20)

    def test_cached_property_without_getter(self):
        class Example:
            def __init__(self):
                self._value = 10

            def set(self, val):
                self._value = val

            def delete(self):
                self._value = None

            prop = cached_property(None, set, delete, doc="cached prop")

        obj = Example()
        self.assertEqual(obj._value, 10)
        obj.prop = 20
        self.assertEqual(obj._value, 20)
        del obj.prop
        self.assertIsNone(obj._value)

    def test_cached_property_docstring(self):
        class Example:
            @cached_property
            def prop(self):
                """Returns something"""
                return 1

        self.assertEqual(Example.__dict__['prop'].__doc__, "Returns something")
        self.assertEqual(Example().prop, 1)  # for full coverage
