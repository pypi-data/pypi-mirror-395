# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: Zlib

import unittest
import doctest

import utlx
from utlx import getproperty, setproperty, delproperty


class TestRWProperty(unittest.TestCase):
    """Unit tests for the custom read/write/delete property decorators."""

    def test_doctests(self):
        result = doctest.testfile("_rwproperty_utlx.txt", package=utlx)
        if result.failed:  # pragma: no cover
            doctest.testfile("_rwproperty_utlx.txt", package=utlx,
                             raise_on_error=True)

    def test_get_and_set_property(self):
        """Getter defined first, then setter."""
        class JamesBrown:
            @getproperty
            def feel(self):
                return self._feel

            @setproperty
            def feel(self, feel):
                self._feel = feel

        obj = JamesBrown()
        # Reading before setting should raise AttributeError
        with self.assertRaises(AttributeError):
            _ = obj.feel
        # Setting and reading should work
        obj.feel = "good"
        self.assertEqual(obj.feel, "good")

    def test_set_then_get_property(self):
        """Setter defined first, then getter."""
        class JamesBrown:
            @setproperty
            def feel(self, feel):
                self._feel = feel

            @getproperty
            def feel(self):
                return self._feel

        obj = JamesBrown()
        obj.feel = "good"
        self.assertEqual(obj.feel, "good")

    def test_with_deleter(self):
        """Property with getter, setter, and deleter."""
        class JamesBrown:
            @setproperty
            def feel(self, feel):
                self._feel = feel

            @getproperty
            def feel(self):
                return self._feel

            @delproperty
            def feel(self):
                del self._feel

        obj = JamesBrown()
        obj.feel = "good"
        self.assertEqual(obj.feel, "good")
        del obj.feel
        with self.assertRaises(AttributeError):
            _ = obj.feel

    def test_with_deleter_as_first(self):
        """Property with getter, setter, and deleter."""
        class JamesBrown:
            @delproperty
            def feel(self):
                del self._feel

            @setproperty
            def feel(self, feel):
                self._feel = feel

            @getproperty
            def feel(self):
                return self._feel

        obj = JamesBrown()
        obj.feel = "good"
        self.assertEqual(obj.feel, "good")
        del obj.feel
        with self.assertRaises(AttributeError):
            _ = obj.feel

    def test_edge_case_non_property_attribute(self):
        """Defining a property on top of a non-property attribute should fail."""
        with self.assertRaises(TypeError):
            class JamesBrown:
                feel = "good"

                @getproperty
                def feel(self):
                    return "so good"  # pragma: no cover

    def test_enhance_property_getter(self):
        """Enhancing an existing property with a getter should only replace fget."""
        class Foo:
            @getproperty
            def x(self):
                return 1

            @setproperty
            def x(self, value):
                self._x = value

        obj = Foo()
        obj.x = 42
        self.assertEqual(obj._x, 42)
        self.assertEqual(obj.x, 1)

    def test_enhance_property_setter(self):
        """Enhancing an existing property with a setter should only replace fset."""
        class Foo:
            @setproperty
            def x(self, value):
                self._x = value

            @getproperty
            def x(self):
                return getattr(self, "_x", None)

        obj = Foo()
        obj.x = 99
        self.assertEqual(obj.x, 99)

    def test_enhance_property_deleter(self):
        """Enhancing an existing property with a deleter should only replace fdel."""
        class Foo:
            @setproperty
            def x(self, value):
                self._x = value

            @getproperty
            def x(self):
                return self._x

            @delproperty
            def x(self):
                self._x = "deleted"

        obj = Foo()
        obj.x = 5
        self.assertEqual(obj.x, 5)
        del obj.x
        self.assertEqual(obj._x, "deleted")
