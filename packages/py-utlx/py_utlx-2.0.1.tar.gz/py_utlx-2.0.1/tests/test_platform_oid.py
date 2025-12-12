# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: Zlib

import unittest
from unittest import mock
import sys

import utlx
from utlx.platform import from_oid
from utlx.platform import is_cpython


@unittest.skipUnless(is_cpython, "CPython-only tests")
class TestFromOid(unittest.TestCase):

    def test_none_oid_returns_none(self):
        self.assertIsNone(from_oid(None))

    def test_zero_oid_returns_none(self):
        self.assertIsNone(from_oid(0))

    def test_valid_oid_returns_same_object(self):

        obj = 145
        oid = id(obj)
        result = from_oid(oid)
        self.assertIs(result, obj)

        obj = "string"
        oid = id(obj)
        result = from_oid(oid)
        self.assertIs(result, obj)

        obj = ("item1", "item2")
        oid = id(obj)
        result = from_oid(oid)
        self.assertIs(result, obj)

        obj = {"item1", "item2"}
        oid = id(obj)
        result = from_oid(oid)
        self.assertIs(result, obj)

        obj = {"key": "value"}
        oid = id(obj)
        result = from_oid(oid)
        self.assertIs(result, obj)

        class Dummy:
            pass

        obj = Dummy()
        oid = id(obj)
        result = from_oid(oid)
        self.assertIs(result, obj)

    @unittest.skip("from_oid(oid) on deleted object does not work.")
    def test_deleted_object_raises_reference_error(self):
        import weakref
        import gc

        class Dummy:
            pass

        obj = Dummy()
        oid = id(obj)
        weak_ref = weakref.ref(obj)
        del obj
        gc.collect()
        self.assertIsNone(weak_ref())

        with self.assertRaises(ReferenceError):
            from_oid(oid)


class TestFromOidRaisesNotImplementedError(unittest.TestCase):

    def test_raised_non_implemented_exception(self):
        with mock.patch("platform.python_implementation", return_value="NonCPython"):
            sys.modules.pop("utlx.platform", None)
            sys.modules.pop("utlx.platform._oid", None)
            sys.modules.pop("utlx.platform._detect", None)
            from utlx.platform import from_oid
            with self.assertRaises(NotImplementedError):
                from_oid(None)
