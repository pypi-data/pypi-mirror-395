# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: Zlib

import unittest
import warnings

import utlx
from utlx import deprecated


class TestDeprecatedDecorator(unittest.TestCase):

    def test_deprecated_emits_warning(self):
        @deprecated
        def old_function():
            return "ok"

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = old_function()
            self.assertEqual(result, "ok")
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))
            self.assertIn("Call to deprecated function 'old_function'", str(w[0].message))

    def test_deprecated_preserves_function_metadata(self):
        @deprecated
        def sample():
            """This is a sample function"""
            return 123

        self.assertEqual(sample.__name__, "sample")
        self.assertEqual(sample.__doc__, "This is a sample function")

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = sample()
            self.assertEqual(result, 123)
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))
            self.assertIn("Call to deprecated function 'sample'", str(w[0].message))

    def test_deprecated_with_arguments(self):
        @deprecated
        def add(a, b):
            return a + b

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = add(2, 3)
            self.assertEqual(result, 5)
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))
            self.assertIn("Call to deprecated function 'add'", str(w[0].message))
