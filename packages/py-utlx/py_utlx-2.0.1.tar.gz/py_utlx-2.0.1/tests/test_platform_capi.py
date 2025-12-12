# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: Zlib

import unittest
from unittest import mock

import utlx
from utlx.platform import is_windows


@unittest.skipUnless(is_windows, "Windows-only tests")
class TestFDSetFunctions(unittest.TestCase):

    def setUp(self):
        """Create a fresh fd_set instance and its pointer before each test."""
        import ctypes as ct
        from utlx.platform import capi
        self.capi = capi
        self.fdset = self.capi.fd_set()
        self.fdset_p = ct.pointer(self.fdset)

    def test_fd_zero_clears_all(self):
        """FD_ZERO should reset fd_count and clear all entries."""
        # Fill with dummy data
        self.fdset.fd_count = 5
        for i in range(5):
            self.fdset.fd_array[i] = i + 100

        self.capi.FD_ZERO(self.fdset_p)

        self.assertEqual(self.fdset.fd_count, 0)
        self.assertTrue(all(v == 0 for v in self.fdset.fd_array))

    def test_fd_set_and_fd_isset(self):
        """FD_SET should add a descriptor, FD_ISSET should detect it."""
        self.capi.FD_ZERO(self.fdset_p)
        self.capi.FD_SET(42, self.fdset_p)

        self.assertEqual(self.fdset.fd_count, 1)
        self.assertEqual(self.fdset.fd_array[0], 42)
        self.assertEqual(self.capi.FD_ISSET(42, self.fdset_p), 1)
        self.assertEqual(self.capi.FD_ISSET(99, self.fdset_p), 0)

    def test_fd_set_multiple_descriptors(self):
        """FD_SET should handle multiple descriptors in insertion order."""
        self.capi.FD_ZERO(self.fdset_p)
        for fd in (10, 20, 30):
            self.capi.FD_SET(fd, self.fdset_p)

        self.assertEqual(self.fdset.fd_count, 3)
        self.assertTrue(all(self.capi.FD_ISSET(fd, self.fdset_p) for fd in (10, 20, 30)))

    def test_fd_clr_removes_descriptor(self):
        """FD_CLR should remove a descriptor and shift remaining ones."""
        self.capi.FD_ZERO(self.fdset_p)
        for fd in (10, 20, 30):
            self.capi.FD_SET(fd, self.fdset_p)

        self.capi.FD_CLR(20, self.fdset_p)

        self.assertEqual(self.fdset.fd_count, 2)
        self.assertEqual(list(self.fdset.fd_array[:2]), [10, 30])
        self.assertEqual(self.capi.FD_ISSET(20, self.fdset_p), 0)

    def test_fd_clr_nonexistent_descriptor(self):
        """FD_CLR should do nothing if descriptor is not present."""
        self.capi.FD_ZERO(self.fdset_p)
        self.capi.FD_SET(10, self.fdset_p)

        self.capi.FD_CLR(99, self.fdset_p)  # Descriptor not in set

        self.assertEqual(self.fdset.fd_count, 1)
        self.assertEqual(self.fdset.fd_array[0], 10)
