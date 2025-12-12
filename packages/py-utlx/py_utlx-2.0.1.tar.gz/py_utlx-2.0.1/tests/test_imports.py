# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: Zlib

import unittest
import sys
import platform
import types
import tempfile
import shutil
from pathlib import Path

import utlx
from utlx.imports import import_static, import_file
from utlx.platform import is_pypy


class TestImportStatic(unittest.TestCase):

    def test_import_builtin_module(self):
        mod = import_static("math")
        self.assertIsInstance(mod, types.ModuleType)
        self.assertEqual(mod.__name__, "math")

    def test_import_with_reload(self):
        mod1 = import_static("enum")
        mod2 = import_static("enum", reload=True)
        self.assertIsInstance(mod2, types.ModuleType)
        self.assertEqual(mod2.__name__, "enum")
        self.assertIsNot(mod1, mod2)

    def test_import_nonexistent_module(self):
        with self.assertRaises(ImportError):
            import_static("nonexistent_module_abcxyz")


class TestImportFile(unittest.TestCase):

    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.module_path = self.temp_dir/"testmod.py"
        self.module_path.write_text("x = 42\ny = 'hello'\n")

        # Package: directory with __init__.py
        self.pkg_dir = self.temp_dir/"mypkg"
        self.pkg_dir.mkdir()
        (self.pkg_dir/"__init__.py").write_text("a = 'package'\nb = 123\n")

        # Ensure temp_dir is in sys.path for strict_sys_path=True
        sys.path.insert(0, str(self.temp_dir))

    def tearDown(self):
        sys.path.remove(str(self.temp_dir))
        shutil.rmtree(self.temp_dir)

    def test_import_file_basic(self):
        mod = import_file(self.module_path)
        self.assertIsInstance(mod, types.ModuleType)
        self.assertEqual(mod.x, 42)
        self.assertEqual(mod.y, "hello")

    def test_import_file_with_custom_name(self):
        mod = import_file(self.module_path, name="custom_name")
        self.assertEqual(mod.__name__, "custom_name")

    def test_import_file_improper(self):
        module_path = self.temp_dir/"testmod.txt"
        module_path.write_text("\n")
        with self.assertRaises(ImportError):
            import_file(module_path)

    def test_import_file_reload(self):
        mod1 = import_file(self.module_path)
        mod2 = import_file(self.module_path, reload=True)
        self.assertIsNot(mod1, mod2)

    def test_import_file_strict_sys_path_violation(self):
        outside_path = Path(tempfile.gettempdir())/"outside.py"
        outside_path.write_text("z = 99\n")
        try:
            with self.assertRaises(ImportError):
                import_file(outside_path, strict_sys_path=True)
            # Default: strict_sys_path == True
            with self.assertRaises(ImportError):
                import_file(outside_path)
            import_file(outside_path, strict_sys_path=False)
        finally:
            outside_path.unlink()

    def test_import_file_nonexistent(self):
        with self.assertRaises(ImportError):
            import_file(self.temp_dir/"missing.py")

    def test_import_package_directory(self):
        mod = import_file(self.pkg_dir)
        self.assertIsInstance(mod, types.ModuleType)
        self.assertEqual(mod.a, "package")
        self.assertEqual(mod.b, 123)
        self.assertEqual(mod.__name__, "mypkg")

    def test_import_package_with_custom_name(self):
        mod = import_file(self.pkg_dir, name="custompkg")
        self.assertEqual(mod.__name__, "custompkg")

    def test_import_package_reload(self):
        mod1 = import_file(self.pkg_dir)
        mod2 = import_file(self.pkg_dir, reload=True)
        self.assertIsNot(mod1, mod2)
