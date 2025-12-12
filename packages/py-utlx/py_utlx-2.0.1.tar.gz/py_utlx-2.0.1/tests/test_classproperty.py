# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: Zlib

import unittest

import utlx
from utlx import classproperty


class TestClassProperty(unittest.TestCase):

    def test_basic_classproperty_access(self):
        class MyClass:
            @classproperty
            def name(cls):
                return cls.__name__

        self.assertEqual(MyClass.name, "MyClass")

    def test_classproperty_access_from_instance(self):
        class MyClass:
            @classproperty
            def info(cls):
                return "class-level"

        instance = MyClass()
        self.assertEqual(instance.info, "class-level")

    def test_classproperty_with_docstring(self):
        class MyClass:
            @classproperty
            def value(cls):
                """Returns a fixed value"""
                return 42

        self.assertEqual(MyClass.value, 42)
        self.assertEqual(MyClass.__dict__['value'].__doc__, "Returns a fixed value")

    def test_classproperty_without_fget_raises(self):
        cp = classproperty()
        with self.assertRaises(AttributeError):
            cp.__get__(None, None)

    def test_classproperty_with_non_callable_fget_raises(self):
        cp = classproperty(fget=123)
        with self.assertRaises(TypeError):
            cp.__get__(None, None)

    def test_classproperty_rejects_fset_and_fdel(self):
        with self.assertRaises(ValueError):
            classproperty(lambda cls: 1, fset=lambda cls, val: None)

        with self.assertRaises(ValueError):
            classproperty(lambda cls: 1, fdel=lambda cls: None)

    def test_classproperty_getter_method(self):
        def get_value(cls):
            return "OK"

        cp = classproperty().getter(get_value)
        class Dummy:
            prop = cp

        self.assertEqual(Dummy.prop, "OK")

    def test_classproperty_doc_inferred(self):
        def get(cls):
            """Auto-doc"""
            return "doc"  # pragma: no cover

        cp = classproperty(get)
        self.assertEqual(cp.__doc__, "Auto-doc")

    def test_classproperty_fget_property(self):
        def get(cls):
            return "value"  # pragma: no cover

        cp = classproperty(get)
        self.assertEqual(cp.fget, get)
