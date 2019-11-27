#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    test_basic_demo.py
    ~~~~~~~~

    :author: Fufu, 2019/9/12
"""
try:
    import __init__
except ModuleNotFoundError:
    import tests.__init__

import unittest

from app.libs.helper import get_int


class TestGetInt(unittest.TestCase):

    def test_default(self):
        self.assertEqual(get_int('1a', 9), 9)
        self.assertEqual(get_int('1a'), None)
        self.assertEqual(get_int(' 123    '), 123)
        self.assertEqual(get_int(' -123    '), -123)
        self.assertEqual(get_int(123), 123)
        self.assertEqual(get_int('0'), 0)
        self.assertEqual(get_int(0b10), 2)

    def test_int_list(self):
        self.assertEqual(get_int('123, 456,, 7,, ,', default=9, sep=','), [123, 456, 7])
        self.assertEqual(get_int('123, 456,, 7,, ,', sep=','), [123, 456, 7])

    def test_error(self):
        self.assertEqual(get_int('a123, 4.56,, x,, ,', sep=','), [])

    def test_other(self):
        self.assertEqual(get_int(None, sep=','), [])
        self.assertEqual(get_int(None, 0), 0)

if __name__ == '__main__':
    unittest.main()
