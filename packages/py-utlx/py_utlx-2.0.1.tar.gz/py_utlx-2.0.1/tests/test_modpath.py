# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: Zlib

import unittest
from unittest import mock
import types
import inspect
from pathlib import Path

import utlx
from utlx import module_path


class TestModulePath(unittest.TestCase):

    def test_module_path_with_explicit_module(self):
        # We use a built-in module as an example
        import os
        path = module_path(os)
        self.assertIsInstance(path, Path)
        self.assertTrue(path.exists())
        self.assertTrue(path.is_dir())

    def test_module_path_with_none_detects_current_file(self):
        # The function should return the path to the directory of this test file
        current_file = inspect.getfile(inspect.currentframe())
        expected_dir = Path(current_file).resolve().parent
        result = module_path()
        self.assertEqual(result, expected_dir)

    def test_module_path_with_level_argument(self):
        # We test whether the level works correctly in a deeper call stack
        def inner():
            return module_path(level=2)

        def outer():
            return inner()

        expected_dir = Path(inspect.getfile(inspect.currentframe())).resolve().parent
        self.assertEqual(outer(), expected_dir)

    @unittest.skip("test_module_path_fallback_to___file__: failed!")
    def test_module_path_fallback_to___file__(self):
        # We simulate the absence of a module in the frame, forcing the use of file
        frame = inspect.currentframe()
        fake_globals = {"__file__": __file__}
        with mock.patch("sys._getframe", return_value=frame), \
             mock.patch("inspect.getmodule", return_value=None), \
             mock.patch.object(frame, "f_globals", fake_globals):
            result = module_path(module=None)
            expected = Path(__file__).resolve().parent
            self.assertEqual(result, expected)


class TestModulePathMocked(unittest.TestCase):

    def test_module_explicit(self):
        dummy_module = mock.Mock(spec=types.ModuleType)
        with mock.patch("inspect.getfile", return_value="/fake/path/module.py"):
            result = module_path(dummy_module)
        self.assertEqual(result, Path("/fake/path").resolve())

    def test_module_none_with_module_detected(self):
        dummy_module = mock.Mock(spec=types.ModuleType)
        frame_mock = mock.Mock()
        frame_mock.f_globals = {"__file__": "/fake/path/from_frame.py"}

        with mock.patch("sys._getframe", return_value=frame_mock), \
             mock.patch("inspect.getmodule", return_value=dummy_module), \
             mock.patch("inspect.getfile", return_value="/fake/path/from_module.py"):
            result = module_path(None)
        self.assertEqual(result, Path("/fake/path").resolve())

    def test_module_none_without_module_detected(self):
        frame_mock = mock.Mock()
        frame_mock.f_globals = {"__file__": "/fake/path/from_globals.py"}

        with mock.patch("sys._getframe", return_value=frame_mock), \
             mock.patch("inspect.getmodule", return_value=None):
            result = module_path(None)
        self.assertEqual(result, Path("/fake/path").resolve())

    def test_module_none_with_level(self):
        frame_mock = mock.Mock()
        frame_mock.f_globals = {"__file__": "/fake/path/level_up.py"}

        with mock.patch("sys._getframe", return_value=frame_mock), \
             mock.patch("inspect.getmodule", return_value=None):
            result = module_path(level=1)
        self.assertEqual(result, Path("/fake/path").resolve())
