# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: Zlib

import unittest
from unittest import mock
import io
import subprocess
import logging

import utlx
from utlx import _run, run


class TestRunFunction(unittest.TestCase):

    def setUp(self):
        # Capture logs for verification
        self.log_stream = logging.getLogger(_run.__name__)
        self.log_stream.setLevel(logging.DEBUG)
        self.log_buffer = io.StringIO()
        self.log_handler = logging.StreamHandler(self.log_buffer)
        self.log_stream.addHandler(self.log_handler)
        self.addCleanup(self.log_stream.removeHandler, self.log_handler)

    def test_run_basic_command(self):
        """run() should call subprocess.run with given args and return CompletedProcess."""
        fake_cp = subprocess.CompletedProcess(args=["echo", "hi"], returncode=0)
        with mock.patch("subprocess.run", return_value=fake_cp) as mock_run:
            result = run("echo", "hi")
        mock_run.assert_called_once_with(["echo", "hi"], check=True)
        self.assertIs(result, fake_cp)

    def test_run_with_check_false(self):
        """run() should pass check=False when specified."""
        fake_cp = subprocess.CompletedProcess(args=["cmd"], returncode=1)
        with mock.patch("subprocess.run", return_value=fake_cp) as mock_run:
            result = run("cmd", check=False)
        mock_run.assert_called_once_with(["cmd"], check=False)
        self.assertIs(result, fake_cp)

    def test_run_masks_safestring_in_log(self):
        """SafeString arguments should be masked in debug log output."""
        fake_cp = subprocess.CompletedProcess(args=["secret"], returncode=0)
        safe_arg = run.SafeString("secret")
        with mock.patch("subprocess.run", return_value=fake_cp):
            run("echo", safe_arg)
        # Retrieve log output
        self.log_handler.flush()
        log_output = self.log_buffer.getvalue()
        self.assertIn("*****", log_output)

    def test_run_converts_all_args_to_str(self):
        """Non-string args should be converted to strings before passing to subprocess.run."""
        fake_cp = subprocess.CompletedProcess(args=["1", "2"], returncode=0)
        with mock.patch("subprocess.run", return_value=fake_cp) as mock_run:
            run(1, 2)
        called_args, called_kwargs = mock_run.call_args
        self.assertEqual(called_args[0], ["1", "2"])

    def test_constants_and_types(self):
        """Check that run.* constants and types are correctly assigned."""
        self.assertIs(run.PIPE, subprocess.PIPE)
        self.assertIs(run.STDOUT, subprocess.STDOUT)
        self.assertIs(run.DEVNULL, subprocess.DEVNULL)
        self.assertIs(run.CompletedProcess, subprocess.CompletedProcess)
        self.assertIs(run.SubprocessError, subprocess.SubprocessError)
        self.assertIs(run.TimeoutExpired, subprocess.TimeoutExpired)
        self.assertIs(run.CalledProcessError, subprocess.CalledProcessError)
        self.assertTrue(issubclass(run.SafeString, str))


class TestSplitKwargs(unittest.TestCase):

    def test_split_kwargs_basic(self):
        """split_kwargs should separate allowed and reserved keys."""
        kwargs = {"a": 1, "b": 2, "c": 3}
        forbidden = ["b", "c"]
        allowed, reserved = run.split_kwargs(kwargs, forbidden)
        self.assertEqual(allowed, {"a": 1})
        self.assertEqual(reserved, {"b": 2, "c": 3})

    def test_split_kwargs_no_forbidden(self):
        """If no forbidden keys, all kwargs should be allowed."""
        kwargs = {"x": 10}
        allowed, reserved = run.split_kwargs(kwargs, [])
        self.assertEqual(allowed, {"x": 10})
        self.assertEqual(reserved, {})

    def test_split_kwargs_all_forbidden(self):
        """If all keys are forbidden, allowed should be empty."""
        kwargs = {"x": 1, "y": 2}
        allowed, reserved = run.split_kwargs(kwargs, ["x", "y"])
        self.assertEqual(allowed, {})
        self.assertEqual(reserved, {"x": 1, "y": 2})
