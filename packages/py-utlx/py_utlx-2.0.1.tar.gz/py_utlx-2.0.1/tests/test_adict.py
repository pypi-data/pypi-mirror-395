# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: Zlib

import unittest
import copy

import utlx
from utlx import adict, defaultadict


class TestAdict(unittest.TestCase):

    def test_item_assignment(self):
        d = adict()
        self.assertNotIn("x", d)
        d["x"] = 10
        self.assertEqual(d.x, 10)
        self.assertEqual(d["x"], 10)

    def test_attribute_assignment(self):
        d = adict()
        self.assertNotIn("x", d)
        d.x = 20
        self.assertEqual(d["x"], 20)
        self.assertEqual(d.x, 20)

    def test_missing_item_raises(self):
        d = adict()
        with self.assertRaises(KeyError):
            _ = d["missing"]
        with self.assertRaises(AttributeError):
            _ = d["missing"]

    def test_missing_attribute_raises(self):
        d = adict()
        with self.assertRaises(KeyError):
            _ = d.missing
        with self.assertRaises(AttributeError):
            _ = d.missing

    def test_item_deletion(self):
        d = adict(x=5)
        self.assertIn("x", d)
        del d["x"]
        self.assertNotIn("x", d)

    def test_attribute_deletion(self):
        d = adict(x=5)
        self.assertIn("x", d)
        del d.x
        self.assertNotIn("x", d)

    def test_missing_item_deletion_raises(self):
        d = adict()
        with self.assertRaises(KeyError):
            del d["missing"]
        with self.assertRaises(AttributeError):
            del d["missing"]

    def test_missing_attribute_deletion_raises(self):
        d = adict()
        with self.assertRaises(KeyError):
            del d.missing
        with self.assertRaises(AttributeError):
            del d.missing

    def test_self_copy_returns_new_instance(self):
        d1 = adict(a=1, b=2)
        d2 = d1.copy()
        self.assertIsInstance(d1, adict)
        self.assertIsInstance(d2, adict)
        self.assertEqual(d2, d1)
        self.assertIsNot(d1, d2)

    def test_copy_returns_new_instance(self):
        d1 = adict(a=1, b=2)
        d2 = copy.copy(d1)
        self.assertIsInstance(d1, adict)
        self.assertIsInstance(d2, adict)
        self.assertEqual(d2, d1)
        self.assertIsNot(d1, d2)

    def test_fromkeys_creates_instance(self):
        d = adict.fromkeys(["a", "b"], 0)
        self.assertIsInstance(d, adict)
        self.assertEqual(d["a"], 0)
        self.assertEqual(d.a, 0)
        self.assertEqual(d["b"], 0)
        self.assertEqual(d.b, 0)


class TestDefaultAdict(unittest.TestCase):

    def test_default_factory_behavior(self):
        d = defaultadict(lambda: "default")
        self.assertEqual(d["missing"], "default")

    def test_item_access_and_assignment(self):
        d = defaultadict(lambda: 0)
        self.assertNotIn("x", d)
        d["x"] = 100
        self.assertEqual(d["x"], 100)
        self.assertEqual(d.x, 100)

    def test_attribute_access_and_assignment(self):
        d = defaultadict(lambda: 0)
        self.assertNotIn("x", d)
        d.x = 100
        self.assertEqual(d["x"], 100)
        self.assertEqual(d.x, 100)

    def test_item_deletion(self):
        d = defaultadict(lambda: None, x=1)
        self.assertIn("x", d)
        del d["x"]
        self.assertNotIn("x", d)

    def test_attribute_deletion(self):
        d = defaultadict(lambda: None, x=1)
        self.assertIn("x", d)
        del d.x
        self.assertNotIn("x", d)

    def test_self_copy_returns_new_instance(self):
        d1 = defaultadict(None, a=1, b=2)
        d2 = d1.copy()
        self.assertIsInstance(d1, defaultadict)
        self.assertIsInstance(d2, defaultadict)
        self.assertEqual(d2, d1)
        self.assertIsNot(d1, d2)

    def test_copy_returns_new_instance(self):
        d1 = defaultadict(None, a=1, b=2)
        d2 = copy.copy(d1)
        self.assertIsInstance(d1, defaultadict)
        self.assertIsInstance(d2, defaultadict)
        self.assertEqual(d2, d1)
        self.assertIsNot(d1, d2)

    def test_self_copy_preserves_factory(self):
        d1 = defaultadict(lambda: 42, a=1)
        d2 = d1.copy()
        self.assertIsInstance(d1, defaultadict)
        self.assertIsInstance(d2, defaultadict)
        self.assertEqual(d2, d1)
        self.assertIsNot(d1, d2)
        self.assertEqual(d2["a"], 1)
        self.assertEqual(d2.a, 1)
        self.assertEqual(d2["missing"], 42)

    def test_copy_preserves_factory(self):
        d1 = defaultadict(lambda: 42, a=1)
        d2 = copy.copy(d1)
        self.assertIsInstance(d1, defaultadict)
        self.assertIsInstance(d2, defaultadict)
        self.assertEqual(d2, d1)
        self.assertIsNot(d1, d2)
        self.assertEqual(d2["a"], 1)
        self.assertEqual(d2.a, 1)
        self.assertEqual(d2["missing"], 42)

    def test_fromkeys_creates_instance(self):
        d = defaultadict.fromkeys(["a", "b"], "Y")
        # d.default_factory = lambda: "X"
        self.assertIsInstance(d, defaultadict)
        self.assertEqual(d["a"], "Y")
        self.assertEqual(d.a, "Y")
        self.assertEqual(d["b"], "Y")
        self.assertEqual(d.b, "Y")
        # self.assertEqual(d.missing, "X")
        # self.assertEqual(d["missing"], "X")

    def test_missing_attribute_raises(self):
        d = defaultadict(lambda: None)
        self.assertNotIn("nonexistent", d)
        item = d["nonexistent"]
        self.assertIsNone(item)
        item = d.nonexistent
        self.assertIsNone(item)
        item = d.__getitem__("nonexistent")
        self.assertIsNone(item)
        item = d.__getattr__("nonexistent")
        self.assertIsNone(item)
