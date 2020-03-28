#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from oddmerapp.oddmerappapp import OddmerappApp


class TestOddmerappApp(unittest.TestCase):
    """TestCase for OddmerappApp.
    """
    def setUp(self):
        self.app = OddmerappApp()

    def test_name(self):
        self.assertEqual(self.app.name, 'oddmerapp')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
