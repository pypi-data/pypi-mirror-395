# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: Zlib

import unittest
import gc

import utlx
from utlx import const, weakconst


class TestConstDescriptors(unittest.TestCase):

    def test_const_returns_value(self):
        class Example:
            value = const(42)

        obj = Example()
        self.assertEqual(obj.value, 42)
        self.assertEqual(Example.value, 42)

    def test_const_is_readonly(self):
        class Example:
            value = const(100)

        obj = Example()
        with self.assertRaises(TypeError):
            obj.value = 200
        with self.assertRaises(TypeError):
            del obj.value

    def test_const_docstring(self):
        class Example:
            value = const(1, doc="This is a constant")

        self.assertEqual(Example.__dict__['value'].__doc__, "This is a constant")

    def test_weakconst_returns_value(self):
        class Ref:
            pass

        ref = Ref()

        class Example:
            value = weakconst(ref)

        obj = Example()
        self.assertIs(obj.value, ref)
        self.assertIs(Example.value, ref)

    def test_weakconst_is_readonly(self):
        class Ref:
            pass

        ref = Ref()

        class Example:
            value = weakconst(ref)

        obj = Example()
        with self.assertRaises(TypeError):
            obj.value = "new"
        with self.assertRaises(TypeError):
            del obj.value

    def test_weakconst_returns_none_after_gc(self):
        class Ref:
            pass

        ref = Ref()

        class Example:
            value = weakconst(ref)

        del ref
        gc.collect()

        obj = Example()
        self.assertIsNone(obj.value)

    def test_weakconst_docstring(self):
        class Ref:
            pass

        ref = Ref()

        class Example:
            value = weakconst(ref, doc="Weak reference")

        self.assertEqual(Example.__dict__['value'].__doc__, "Weak reference")
