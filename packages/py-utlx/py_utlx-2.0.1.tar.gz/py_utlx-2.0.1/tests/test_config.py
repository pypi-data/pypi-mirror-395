# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: Zlib

import unittest
import sys
import types
import tempfile
import importlib
from pathlib import Path
from configparser import ConfigParser, DEFAULTSECT

import utlx
from utlx import config


class TestConfigFunctions(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for config files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.temp_path = Path(self.temp_dir.name)

    def create_config_file(self, filename: str, section: str, **entries):
        """Helper to create a config file with given section and entries."""
        parser = ConfigParser()
        parser[section] = {k: str(v) for k, v in entries.items()}
        file_path = self.temp_path / filename
        with open(file_path, "w", encoding="utf-8") as f:
            parser.write(f)
        return file_path

    def test_get_config_with_section(self):
        cfg_file = self.create_config_file("test.ini", "mysection", key1="value1")
        section = config.get_config(cfg_file, "mysection")
        self.assertEqual(section["key1"], "value1")

    def test_get_config_without_section(self):
        # DEFAULT section
        parser = ConfigParser()
        parser["DEFAULT"] = {"key2": "value2"}
        cfg_file = self.temp_path / "default.ini"
        with open(cfg_file, "w", encoding="utf-8") as f:
            parser.write(f)
        section = config.get_config(cfg_file)
        self.assertEqual(section["key2"], "value2")

    def test_get_config_missing_file(self):
        # Should return an empty section if file does not exist
        section = config.get_config(self.temp_path / "nofile.ini", "somesect")
        self.assertEqual(len(section), 0)

    def test_get_config_empty_file(self):
        cfg_file = self.temp_path / "empty.ini"
        cfg_file.write_text("", encoding="utf-8")
        # Without section -> returns DEFAULT (empty)
        section = config.get_config(cfg_file)
        self.assertEqual(len(section), 0)

    def test_get_config_missing_section_in_file(self):
        cfg_file = self.create_config_file("other.ini", "othersect", foo="bar")
        # Asking for a section that does not exist -> returns DEFAULT (empty)
        section = config.get_config(cfg_file, "nonexistent")
        self.assertEqual(len(section), 0)

    def test_make_config_sets_globals(self):
        cfg_file = self.create_config_file("conf.ini", "pkgname", foo="bar")
        # Simulate a caller module's globals
        fake_globals = {
            "__file__": str(self.temp_path / "fake_module.py"),
            "__package__": "pkgname"
        }

        # Patch sys._getframe to return our fake globals
        class FakeFrame:
            def __init__(self, f_globals):
                self.f_globals = f_globals

        original_getframe = sys._getframe
        sys._getframe = lambda depth=0: FakeFrame(fake_globals)
        try:
            config.make_config("conf.ini")
        finally:
            sys._getframe = original_getframe

        self.assertIn("config", fake_globals)
        self.assertIn("set_config", fake_globals)
        self.assertEqual(fake_globals["config"]["foo"], "bar")
        self.assertTrue(callable(fake_globals["set_config"]))

    def test_set_config_updates_and_removes(self):
        # Prepare fake package and __config__ module
        package_name = "fakepkg"
        config_mod_name = package_name + ".__config__"

        fake_config_proxy = {"a": "1", "b": "2"}
        fake_config_module = types.SimpleNamespace(config=fake_config_proxy)
        fake_package_module = types.SimpleNamespace()

        sys.modules[package_name] = fake_package_module
        sys.modules[config_mod_name] = fake_config_module
        # Add a dummy submodule to be removed
        submodule_name = package_name + ".submod"
        sys.modules[submodule_name] = types.SimpleNamespace()

        fglobals = {"__package__": package_name}

        # Patch importlib.reload to mark reload called
        reloaded = {}
        original_reload = importlib.reload
        importlib.reload = lambda mod: reloaded.setdefault("called", True) or mod
        try:
            config.set_config(fglobals, a="10", b=None, c="3")
        finally:
            importlib.reload = original_reload

        # 'a' updated, 'b' removed, 'c' added
        self.assertEqual(fake_config_proxy["a"], "10")
        self.assertNotIn("b", fake_config_proxy)
        self.assertEqual(fake_config_proxy["c"], "3")
        # Submodule should be removed
        self.assertNotIn(submodule_name, sys.modules)
        # Reload should have been called
        self.assertTrue(reloaded.get("called"))

    def test_set_config_no_changes(self):
        """Calling set_config with no changes should not break anything."""
        package_name = "fakepkg2"
        config_mod_name = package_name + ".__config__"

        fake_config_proxy = {"x": "1"}
        fake_config_module = types.SimpleNamespace(config=fake_config_proxy)
        fake_package_module = types.SimpleNamespace()

        sys.modules[package_name] = fake_package_module
        sys.modules[config_mod_name] = fake_config_module

        fglobals = {"__package__": package_name}

        original_reload = importlib.reload
        importlib.reload = lambda mod: mod
        try:
            config.set_config(fglobals)
        finally:
            importlib.reload = original_reload

        self.assertEqual(fake_config_proxy["x"], "1")  # unchanged
