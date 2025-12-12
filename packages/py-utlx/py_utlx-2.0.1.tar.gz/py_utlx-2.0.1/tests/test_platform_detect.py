# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: Zlib

import unittest
from unittest import mock
import sys
import os
import platform
import importlib

import utlx


class TestPlatformDetect(unittest.TestCase):

    def reload_platform(self, platform_attrs=None, sys_attrs=None, os_attrs=None):
        """Helper function for reloading the module with mocked values."""
        patches = []
        if platform_attrs:
            for name, value in platform_attrs.items():
                patches.append(mock.patch.object(platform, name, value, create=True))
        else: pass  # pragma: no cover
        if sys_attrs:
            for name, value in sys_attrs.items():
                patches.append(mock.patch.object(sys, name, value, create=True))
        else: pass  # pragma: no cover
        if os_attrs:
            for name, value in os_attrs.items():
                patches.append(mock.patch.object(os, name, value, create=True))
        else: pass  # pragma: no cover

        for p in patches:
            p.start()

        # Force a fresh import
        sys.modules.pop("utlx.platform._detect", None)
        import utlx.platform._detect as _detect
        _detect = importlib.reload(_detect)

        for p in reversed(patches):
            p.stop()

        return _detect

    def test_is_windows_true_for_win32(self):
        utlx_platform = self.reload_platform(sys_attrs={"platform": "win32"},
                                             platform_attrs={"win32_ver": lambda: ("10",)})
        self.assertTrue(utlx_platform.is_windows)

    def test_is_linux_true(self):
        utlx_platform = self.reload_platform(sys_attrs={"platform": "linux"},
                                             platform_attrs={"win32_ver": lambda: ("",)})
        self.assertTrue(utlx_platform.is_linux)

    def test_is_macos_true(self):
        utlx_platform = self.reload_platform(sys_attrs={"platform": "darwin"},
                                             platform_attrs={"win32_ver": lambda: ("",)})
        self.assertTrue(utlx_platform.is_macos)

    def test_is_bsd_true(self):
        utlx_platform = self.reload_platform(sys_attrs={"platform": "freebsd"},
                                             platform_attrs={"win32_ver": lambda: ("",)})
        self.assertTrue(utlx_platform.is_bsd)

    def test_is_sunos_true(self):
        utlx_platform = self.reload_platform(sys_attrs={"platform": "sunos"},
                                             platform_attrs={"win32_ver": lambda: ("",)})
        self.assertTrue(utlx_platform.is_sunos)

    def test_is_aix_true(self):
        utlx_platform = self.reload_platform(sys_attrs={"platform": "aix"},
                                             platform_attrs={"win32_ver": lambda: ("",)})
        self.assertTrue(utlx_platform.is_aix)

    def test_is_android_true(self):
        utlx_platform = self.reload_platform(sys_attrs={"getandroidapilevel": lambda: 33},
                                             platform_attrs={"win32_ver": lambda: ("",)})
        self.assertTrue(utlx_platform.is_android)

    def test_is_posix_true(self):
        utlx_platform = self.reload_platform(os_attrs={"name": "posix"},
                                             platform_attrs={"win32_ver": lambda: ("",)})
        self.assertTrue(utlx_platform.is_posix)

    def test_is_32bits_true(self):
        utlx_platform = self.reload_platform(sys_attrs={"maxsize": 2**32},
                                             platform_attrs={"win32_ver": lambda: ("",)})
        self.assertTrue(utlx_platform.is_32bits)

    def test_is_ucs2_true(self):
        utlx_platform = self.reload_platform(sys_attrs={"maxunicode": 0xFFFF},
                                             platform_attrs={"win32_ver": lambda: ("",)})
        self.assertTrue(utlx_platform.is_ucs2)

    def test_is_cpython_true(self):
        utlx_platform = self.reload_platform(platform_attrs={"python_implementation": lambda: "CPython",
                                                             "win32_ver": lambda: ("",)})
        self.assertTrue(utlx_platform.is_cpython)

    def test_is_pypy_true(self):
        utlx_platform = self.reload_platform(platform_attrs={"python_implementation": lambda: "PyPy",
                                                             "win32_ver": lambda: ("",)})
        self.assertTrue(utlx_platform.is_pypy)

    def test_is_ironpython_true(self):
        utlx_platform = self.reload_platform(platform_attrs={"python_implementation": lambda: "IronPython",
                                                             "system": lambda: "CLI",
                                                             "win32_ver": lambda: ("",)},
                                             sys_attrs={"platform": "cli"})
        self.assertTrue(utlx_platform.is_ironpython)

    def test_is_wsl_true(self):
        Uname = type("Uname", (), {"system": platform.system(),
                                   "release": "5.15.0-microsoft-standard"})
        utlx_platform = self.reload_platform(platform_attrs={"uname": lambda: Uname(),
                                                             "win32_ver": lambda: ("",)})
        self.assertTrue(utlx_platform.is_wsl)

    def test_is_cygwin_true(self):
        utlx_platform = self.reload_platform(sys_attrs={"platform": "cygwin"},
                                             platform_attrs={"win32_ver": lambda: ("",)})
        self.assertTrue(utlx_platform.is_cygwin)

    def test_is_msys_true(self):
        utlx_platform = self.reload_platform(sys_attrs={"platform": "msys"},
                                             platform_attrs={"win32_ver": lambda: ("",)})
        self.assertTrue(utlx_platform.is_msys)
