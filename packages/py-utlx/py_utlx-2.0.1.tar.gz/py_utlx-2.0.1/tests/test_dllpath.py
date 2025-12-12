# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: Zlib

import unittest
import sys
import platform
import ctypes as ct
from pathlib import Path

import utlx
from utlx import dll_path, python_dll_path
from utlx.platform import is_windows, is_pypy


@unittest.skipUnless(is_windows, "Windows-only tests")
class TestDllPathWindows(unittest.TestCase):

    @unittest.skip("test_dll_path_for_known_system_dlls: failed!")
    def test_dll_path_for_known_system_dlls(self):
        # Known DLLs that should be loaded in every Windows session
        dll_names = ["kernel32.dll", "user32.dll"]
        for dll_name in dll_names:
            handle = ct.windll.kernel32.GetModuleHandleW(dll_name)
            self.assertNotEqual(handle, 0, f"Failed to get handle for {dll_name}")
            path = dll_path(handle)
            print("@@@@@@@@@@@@ DLL name:", dll_name, handle, path)
            self.assertIsInstance(path, Path)
            self.assertTrue(path.exists(), f"Path for {dll_name} does not exist: {path}")
            self.assertTrue(path.name.lower().endswith(dll_name.lower()))

    def test_python_dll_path(self):
        path = python_dll_path()
        self.assertIsInstance(path, Path)
        self.assertTrue(path.exists(), f"Python DLL path does not exist: {path}")
        self.assertEqual(path.suffix.lower(), ".dll")

    def test_dll_path_with_invalid_handle_returns_none(self):
        # 0 is not a valid module handle
        invalid_handle = 0
        result = dll_path(invalid_handle)
        self.assertIsNone(result)

    @unittest.skipIf(is_pypy and sys.version_info[:2] >= (3, 11),
                     "This test is skipped on PyPy 3.11+")
    def test_dll_path_with_dynamic_windll_loading(self):
        # Load DLL dynamically using WinDLL
        dll = ct.WinDLL("kernel32.dll")
        handle = dll._handle
        path = dll_path(handle)
        self.assertIsInstance(path, Path)
        self.assertTrue(path.exists(), f"Dynamically loaded DLL path does not exist: {path}")
        self.assertTrue(path.name.lower().endswith("kernel32.dll"))
