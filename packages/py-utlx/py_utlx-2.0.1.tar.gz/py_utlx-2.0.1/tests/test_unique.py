# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: Zlib

import unittest

import utlx
from utlx import unique, iter_unique


class TestUniqueFunctions(unittest.TestCase):

    def test_unique_with_integers(self):
        self.assertEqual(unique([1, 2, 2, 3, 1]), [1, 2, 3])

    def test_unique_with_strings(self):
        self.assertEqual(unique("banana"), ['b', 'a', 'n'])

    def test_unique_with_empty_iterable(self):
        self.assertEqual(unique([]), [])

    def test_unique_with_mixed_types(self):
        self.assertEqual(unique([1, "1", 1.0]), [1, "1"])

    def test_iter_unique_basic(self):
        result = list(iter_unique("AAAABBBCCDAABBB"))
        self.assertEqual(result, ['A', 'B', 'C', 'D'])

    def test_iter_unique_with_key(self):
        result = list(iter_unique("ABBCcAD", key=str.lower))
        self.assertEqual(result, ['A', 'B', 'C', 'D'])

    def test_iter_unique_empty(self):
        result = list(iter_unique([], key=str.lower))
        self.assertEqual(result, [])

    def test_iter_unique_custom_key(self):
        data = ["apple", "Apple", "banana", "Banana"]
        result = list(iter_unique(data, key=str.lower))
        self.assertEqual(result, ["apple", "banana"])

    def test_iter_unique_with_numbers_and_key(self):
        data = [1, 2, -1, -2, 3]
        result = list(iter_unique(data, key=abs))
        self.assertEqual(result, [1, 2, 3])

    def test_iter_unique_generator_behavior(self):
        gen = iter_unique([1, 2, 2, 3])
        self.assertTrue(hasattr(gen, '__iter__'))
        self.assertTrue(hasattr(gen, '__next__'))
        self.assertEqual(next(gen), 1)
        self.assertEqual(next(gen), 2)
        self.assertEqual(next(gen), 3)
        with self.assertRaises(StopIteration):
            next(gen)
