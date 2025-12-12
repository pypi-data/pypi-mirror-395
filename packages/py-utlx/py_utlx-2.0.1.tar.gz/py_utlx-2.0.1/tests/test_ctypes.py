# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: Zlib

import unittest
import doctest
import ctypes as ct

from utlx import ctypes as ctx


class TestUtlxCtypes(unittest.TestCase):

    def test_utlx_ctypes_c_ptr(self):
        from utlx.ctypes import _c_ptr
        result = doctest.testmod(_c_ptr)
        if result.failed:  # pragma: no cover
            doctest.testmod(_c_ptr, raise_on_error=True)

    def test_invalid_c_ptr_parameters(self):
        obj = ct.c_char_p(b"ABCD")
        with self.assertRaisesRegex(TypeError, "Can only "):
            _ = ctx.c_ptr_add(obj,  "invalid because string")
        with self.assertRaisesRegex(TypeError, "Can only "):
            _ = ctx.c_ptr_sub(obj,  "invalid because string")
        with self.assertRaisesRegex(TypeError, "Both pointers must "):
            _ = ctx.c_ptr_sub(obj,  ct.c_void_p(345))
        with self.assertRaisesRegex(TypeError, "Can only "):
            ctx.c_ptr_iadd(obj, "invalid because string")
        with self.assertRaisesRegex(TypeError, "Can only "):
            ctx.c_ptr_isub(obj, "invalid because string")


if __name__ == "__main__":
    unittest.main()
