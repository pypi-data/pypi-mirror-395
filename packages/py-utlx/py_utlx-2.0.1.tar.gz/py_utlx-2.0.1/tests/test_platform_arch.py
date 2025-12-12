# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: Zlib

import unittest
from unittest import mock
import platform
import sys

import utlx
from utlx import module_path
from utlx.imports import import_file


class TestWindowsArchDetection(unittest.TestCase):

    def run_arch_test(self, machine_value, is_32bits, expected):
        with mock.patch("platform.machine", return_value=machine_value), \
             mock.patch("sys.maxsize", 2**32 if is_32bits else 2**64):
            import utlx.platform
            _arch = import_file(module_path(utlx.platform)/"windows/_arch.py", reload=True)
            result = _arch.get_python_arch()
            self.assertEqual(result, expected)

    def test_x86_64_variants(self):
        self.run_arch_test("x86_64", False, "x86_64")
        self.run_arch_test("x86_64", True, "x86")
        self.run_arch_test("amd64", False, "x86_64")
        self.run_arch_test("amd64", True, "x86")

    def test_x86_aliases(self):
        for variant in ["x86", "i386", "i686", "ia32"]:
            self.run_arch_test(variant, True, "x86")

    def test_arm_variants(self):
        self.run_arch_test("arm64", False, "arm64")
        self.run_arch_test("arm64", True, "arm")
        self.run_arch_test("armv7l", True, "arm")
        self.run_arch_test("aarch64", False, "arm64")
        self.run_arch_test("aarch64", True, "arm")

    def test_unknown_arch(self):
        self.run_arch_test("unknown", False, None)
        self.run_arch_test("weirdarch", True, None)


class TestLinuxArchDetection(unittest.TestCase):

    def run_arch_test(self, machine_value, is_32bits, expected,
                      fpu_present=None, byteorder="little"):
        with mock.patch("platform.machine", return_value=machine_value), \
             mock.patch("sys.maxsize", 2**32 if is_32bits else 2**64), \
             mock.patch("sys.byteorder", byteorder):
            import utlx.platform
            # optional mock of has_fpu()
            _arch = import_file(module_path(utlx.platform)/"linux/_arch.py", reload=True)
            if fpu_present is not None:
                has_fpu_saved, _arch.has_fpu = _arch.has_fpu, lambda: fpu_present
            try:
                result = _arch.get_python_arch()
            finally:
                if fpu_present is not None:
                    _arch.has_fpu = has_fpu_saved
            self.assertEqual(result, expected)

    def test_x86_variants(self):
        self.run_arch_test("x86_64", False, "x86_64")
        self.run_arch_test("x86_64", True, "x86")
        self.run_arch_test("amd64", False, "x86_64")
        self.run_arch_test("amd64", True, "x86")
        for variant in ["i386", "i686", "x86", "ia32"]:
            self.run_arch_test(variant, True, "x86")

    def test_arm64_variants(self):
        self.run_arch_test("aarch64", False, "aarch64")
        self.run_arch_test("arm64", False, "aarch64")
        self.run_arch_test("aarch64_be", False, "aarch64be", byteorder="big")
        # 32-bit mode on ARMv8 -> armhf/armle
        self.run_arch_test("aarch64", True, "armhf", fpu_present=True)
        self.run_arch_test("aarch64", True, "armle", fpu_present=False)

    def test_arm32_variants(self):
        # soft-float group
        for variant in ["armv6l", "armv5tel", "armv4tl", "armv4l", "arml", "armel"]:
            self.run_arch_test(variant, True, "armle")
        # hard-float group
        self.run_arch_test("armv7l", True, "armhf", fpu_present=True)
        self.run_arch_test("armv7l", True, "armle", fpu_present=False)
        self.run_arch_test("armv8l", True, "armhf", fpu_present=True)
        self.run_arch_test("armv8l", True, "armle", fpu_present=False)

    def test_arm_big_endian(self):
        self.run_arch_test("armv7b", True, None)
        self.run_arch_test("aarch64_be", True, None)

    def test_ppc_variants(self):
        # ppc64 big-endian
        self.run_arch_test("ppc64", False, "ppc64", byteorder="big")
        self.run_arch_test("powerpc64", False, "ppc64", byteorder="big")
        # ppc64 little-endian
        self.run_arch_test("ppc64le", False, "ppc64le", byteorder="little")
        self.run_arch_test("powerpc64le", False, "ppc64le", byteorder="little")
        # ppc64 32bit-mode,big-endian
        self.run_arch_test("ppc64", True, "ppc", byteorder="big")
        self.run_arch_test("powerpc64", True, "ppc", byteorder="big")
        # ppc64 32bit-mode,little-endian
        self.run_arch_test("ppc64le", True, "ppcle", byteorder="little")
        self.run_arch_test("powerpc64le", True, "ppcle", byteorder="little")
        # ppc32 big-endian
        self.run_arch_test("ppc", True, "ppc", byteorder="big")
        self.run_arch_test("powerpc", True, "ppc", byteorder="big")
        # ppc32 little-endian
        self.run_arch_test("ppcle", True, "ppcle", byteorder="little")
        self.run_arch_test("powerpcle", True, "ppcle", byteorder="little")

    def test_mips_variants(self):
        # MIPS64 big-endian
        self.run_arch_test("mips64", False, "mips64", byteorder="big")
        self.run_arch_test("mips64eb", False, "mips64", byteorder="big")
        # MIPS64 little-endian
        self.run_arch_test("mips64el", False, "mips64le", byteorder="little")
        self.run_arch_test("mips64le", False, "mips64le", byteorder="little")
        # MIPS64 32bit-mode,big-endian
        self.run_arch_test("mips64", True, "mips", byteorder="big")
        self.run_arch_test("mips64eb", True, "mips", byteorder="big")
        # MIPS64 32bit-mode,little-endian
        self.run_arch_test("mips64el", True, "mipsle", byteorder="little")
        self.run_arch_test("mips64le", True, "mipsle", byteorder="little")
        # MIPS32 big-endian
        self.run_arch_test("mips", True, "mips", byteorder="big")
        self.run_arch_test("mipseb", True, "mips", byteorder="big")
        # MIPS32 little-endian
        self.run_arch_test("mipsel", True, "mipsle", byteorder="little")
        self.run_arch_test("mipsle", True, "mipsle", byteorder="little")

    def test_other_architectures(self):
        self.run_arch_test("riscv64", False, "riscv64")
        self.run_arch_test("s390x", False, "s390x")

    def test_unknown_arch(self):
        self.run_arch_test("unknown", False, None)
        self.run_arch_test("weirdarch", True, None)


class TestMacOSArchDetection(unittest.TestCase):

    def run_arch_test(self, machine_value, is_32bits, expected):
        with mock.patch("platform.machine", return_value=machine_value), \
             mock.patch("sys.maxsize", 2**32 if is_32bits else 2**64):
            import utlx.platform
            _arch = import_file(module_path(utlx.platform)/"macos/_arch.py", reload=True)
            result = _arch.get_python_arch()
            self.assertEqual(result, expected)

    def test_x86_variants(self):
        self.run_arch_test("x86_64", False, "x86_64")
        self.run_arch_test("x86_64", True, "x86")
        self.run_arch_test("amd64", False, "x86_64")
        self.run_arch_test("amd64", True, "x86")
        for variant in ["i386", "i686", "x86", "ia32"]:
            self.run_arch_test(variant, True, "x86")

    def test_arm64_variants(self):
        self.run_arch_test("arm64", False, "arm64")
        self.run_arch_test("arm64", True, "arm")

    def test_unknown_arch(self):
        self.run_arch_test("unknown", False, None)
        self.run_arch_test("weirdarch", True, None)
