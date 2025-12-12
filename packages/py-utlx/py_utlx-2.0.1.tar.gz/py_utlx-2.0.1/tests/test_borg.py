# Copyright (c) 2004 Adam Karpierz
# SPDX-License-Identifier: Zlib

import unittest

import utlx
from utlx import Borg


class TestBorgPattern(unittest.TestCase):

    def test_shared_state_across_instances(self):
        a = Borg()
        b = Borg()
        a.x = 42
        self.assertEqual(b.x, 42)
        b.y = "hello"
        self.assertEqual(a.y, "hello")

    def test_dict_identity(self):
        a = Borg()
        b = Borg()
        self.assertIs(a.__dict__, b.__dict__)

    def test_modifying_state_affects_all_instances(self):
        a = Borg()
        b = Borg()
        a.data = [1, 2, 3]
        b.data.append(4)
        self.assertEqual(a.data, [1, 2, 3, 4])

    def test_new_instance_has_existing_state(self):
        Borg().shared = "yes"
        new_instance = Borg()
        self.assertEqual(new_instance.shared, "yes")

    def test_state_persistence_after_deletion(self):
        a = Borg()
        a.temp = "value"
        del a
        b = Borg()
        self.assertEqual(b.temp, "value")

    def test_independent_instances_same_state(self):
        class SubBorg(Borg):
            pass

        a = Borg()
        b = SubBorg()
        a.flag = True
        self.assertTrue(b.flag)
        self.assertIs(a.__dict__, b.__dict__)
