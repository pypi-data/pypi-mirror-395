# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: Zlib

import unittest
from unittest import mock
import sys
import io

import utlx
from utlx import issubtype, isiterable, issequence, remove_all, print_refinfo


class TestUtilityFunctions(unittest.TestCase):

    # --- issubtype ---
    def test_issubtype_with_valid_subclass(self):
        self.assertTrue(issubtype(int, object))

    def test_issubtype_with_non_type(self):
        self.assertFalse(issubtype(123, object))

    def test_issubtype_with_unrelated_types(self):
        self.assertFalse(issubtype(str, int))

    # --- isiterable ---
    def test_isiterable_with_list(self):
        self.assertTrue(isiterable([1, 2, 3]))

    def test_isiterable_with_tuple(self):
        self.assertTrue(isiterable((1, 2)))

    def test_isiterable_with_generator(self):
        self.assertTrue(isiterable((x for x in range(3))))

    def test_isiterable_with_string(self):
        self.assertFalse(isiterable("abc"))

    def test_isiterable_with_bytes(self):
        self.assertFalse(isiterable(b"abc"))

    def test_isiterable_with_custom_iterable(self):
        class Custom:
            def __iter__(self):
                return iter([1])
        seq = Custom()
        self.assertTrue(isiterable(seq))
        for item in seq:               # for full coverage
            self.assertEqual(item, 1)  #       -||-

    # --- issequence ---
    def test_issequence_with_list(self):
        self.assertTrue(issequence([1, 2]))

    def test_issequence_with_tuple(self):
        self.assertTrue(issequence((1, 2)))

    def test_issequence_with_string(self):
        self.assertFalse(issequence("text"))

    def test_issequence_with_bytes(self):
        self.assertFalse(issequence(b"data"))

    def test_issequence_with_custom_sequence(self):
        from collections.abc import Sequence
        class Custom(Sequence):
            def __getitem__(self, index):
                return index
            def __len__(self):
                return 12
        seq = Custom()
        self.assertTrue(issequence(seq))
        self.assertEqual(seq[7], 7)     # for full coverage
        self.assertEqual(len(seq), 12)  #       -||-

    # --- remove_all ---
    def test_remove_all_removes_all_occurrences(self):
        data = [1, 2, 3, 2, 4]
        remove_all(data, 2)
        self.assertEqual(data, [1, 3, 4])

    def test_remove_all_with_no_match(self):
        data = [1, 2, 3]
        remove_all(data, 99)
        self.assertEqual(data, [1, 2, 3])

    def test_remove_all_with_empty_list(self):
        data = []
        remove_all(data, 1)
        self.assertEqual(data, [])

    def test_remove_all_removes_everything(self):
        data = [5, 5, 5]
        remove_all(data, 5)
        self.assertEqual(data, [])


class TestPrintRefInfo(unittest.TestCase):

    def test_print_refinfo_outputs_expected_lines(self):
        obj = [1, 2, 3]
        captured = io.StringIO()
        sys.stderr = captured
        print_refinfo(obj)
        sys.stderr = sys.__stderr__
        output = captured.getvalue()
        self.assertIn("Object info report", output)
        self.assertIn("obj type:", output)
        self.assertIn("obj id:", output)

    def test_normal_object_with_refcount(self):
        obj = "hello"
        with mock.patch.object(sys, 'getrefcount', return_value=10, create=True), \
             mock.patch('sys.stderr', new_callable=io.StringIO) as fake_stderr:
            print_refinfo(obj)
            output = fake_stderr.getvalue()
            self.assertIn("Object info report", output)
            self.assertIn("obj type:", output)
            self.assertIn("obj id:", output)
            self.assertIn("ref count: 8", output)  # 10 - 2

    def test_object_without_getrefcount(self):
        obj = 123
        with mock.patch.object(sys, 'getrefcount', side_effect=AttributeError, create=True), \
             mock.patch('sys.stderr', new_callable=io.StringIO) as fake_stderr, \
             mock.patch('sys.hasattr', return_value=False):
            # We simulate the absence of getrefcount by manipulating hasattr
            original_hasattr = hasattr
            def fake_hasattr(obj, name):
                if obj is sys and name == "getrefcount":
                    return False
                return original_hasattr(obj, name)

            with mock.patch('builtins.hasattr', side_effect=fake_hasattr):
                hasattr(obj, "__doc__")  # for full coverage
                print_refinfo(obj)
                output = fake_stderr.getvalue()
                self.assertIn("Object info report", output)
                self.assertIn("obj type:", output)
                self.assertIn("obj id:", output)
                self.assertNotIn("ref count:", output)

    def test_object_with_missing_class_name(self):
        class Weird:
            def __getattribute__(self, name):
                if name in ['__class__']:
                    raise AttributeError("no __class__")
                return super().__getattribute__(name)

        obj = Weird()
        obj.__doc__  # for full coverage
        with mock.patch.object(sys, 'getrefcount', return_value=5, create=True), \
             mock.patch('sys.stderr', new_callable=io.StringIO) as fake_stderr:
            print_refinfo(obj)
            output = fake_stderr.getvalue()
            self.assertIn("Object info report", output)
            self.assertIn("obj type:", output)
            self.assertIn("ref count: 3", output)  # 5 - 2

    def test_object_with_missing_type_and_class_name(self):
        class Nameless:
            def __getattribute__(self, name):
                if name in ('__class__', '__name__'):
                    raise AttributeError("nope")
                return super().__getattribute__(name)

        obj = Nameless()
        obj.__doc__  # for full coverage
        with mock.patch.object(sys, 'getrefcount', return_value=7, create=True), \
             mock.patch('sys.stderr', new_callable=io.StringIO) as fake_stderr:
            print_refinfo(obj)
            output = fake_stderr.getvalue()
            self.assertIn("Object info report", output)
            self.assertIn("obj type:", output)
            self.assertIn("ref count: 5", output)
