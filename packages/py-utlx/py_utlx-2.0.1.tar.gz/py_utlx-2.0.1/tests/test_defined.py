# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: Zlib

import unittest

import utlx
from utlx import defined


class TestDefinedFunction(unittest.TestCase):

    def test_defined_local_variable(self):
        def func():
            local_var = 123
            return defined("local_var")
        self.assertTrue(func())

    def test_defined_global_variable(self):
        global_var = "hello"
        self.assertTrue(defined("global_var"))

    def test_defined_missing_variable(self):
        self.assertFalse(defined("nonexistent_var"))

    def test_defined_shadowed_variable(self):
        # The variable exists only locally, not globally
        def func():
            shadow = "local"
            return defined("shadow")
        self.assertTrue(func())
        self.assertFalse("shadow" in globals())

    def test_defined_with_builtin(self):
        # Built-in functions are not treated as local or global
        self.assertFalse(defined("print"))  # print is in builtins, not in globals
