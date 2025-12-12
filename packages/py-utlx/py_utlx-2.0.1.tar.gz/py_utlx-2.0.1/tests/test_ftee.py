# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: Zlib

import unittest
import sys
import tempfile
from pathlib import Path
from io import StringIO

import utlx
from utlx import ftee
from utlx._ftee import _Tee


class TestTee(unittest.TestCase):

    def test_write_writes_to_all_files(self):
        buf1 = StringIO()
        buf2 = StringIO()
        tee = _Tee(buf1, buf2)
        tee.write("hello")
        self.assertEqual(buf1.getvalue(), "hello")
        self.assertEqual(buf2.getvalue(), "hello")

    def test_flush_flushes_all_files(self):
        buf1 = StringIO()
        buf2 = StringIO()
        tee = _Tee(buf1, buf2)
        tee.write("data")
        # StringIO flush doesn't change content, but we can call without error
        tee.flush()  # Should not raise

    def test_writable_returns_true_when_open(self):
        buf = StringIO()
        tee = _Tee(buf)
        self.assertTrue(tee.writable())

    def test_writable_raises_when_closed(self):
        buf = StringIO()
        tee = _Tee(buf)
        tee.close()
        with self.assertRaises(ValueError):
            tee.writable()

    def test_close_closes_secondary_files(self):
        buf1 = StringIO()
        buf2 = StringIO()
        tee = _Tee(buf1, buf2)
        tee.close()
        # buf2 should be closed
        with self.assertRaises(ValueError):
            buf2.write("x")


class TestFtee(unittest.TestCase):

    def test_ftee_redirects_stdout_and_writes_to_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "out.txt"
            # Capture original stdout
            original_stdout = sys.stdout
            try:
                with ftee(file_path) as tee_stdout:
                    print("Hello Tee", end="")
                # After context, sys.stdout restored
                self.assertIs(sys.stdout, original_stdout)
                # File should contain the printed text
                content = file_path.read_text()
                self.assertIn("Hello Tee", content)
            finally:
                sys.stdout = original_stdout

    def test_ftee_writes_to_multiple_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file1 = Path(tmpdir) / "out1.txt"
            file2 = Path(tmpdir) / "out2.txt"
            with ftee(file1, file2):
                print("Multi", end="")
            self.assertEqual(file1.read_text(), "Multi")
            self.assertEqual(file2.read_text(), "Multi")


class TestFteeExceptionSafety(unittest.TestCase):

    def test_ftee_restores_stdout_on_exception(self):
        original_stdout = sys.stdout
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "out.txt"
            try:
                with ftee(file_path):
                    print("Before crash", end="")
                    raise RuntimeError("Simulated error")
            except RuntimeError:
                pass
