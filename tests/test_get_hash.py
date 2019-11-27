#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    test_get_hash.py
    ~~~~~~~~

    :author: Fufu, 2019/9/25
"""
try:
    import __init__
except ModuleNotFoundError:
    import tests.__init__

import hashlib
import unittest

from app.libs.helper import get_hash


class TestGetInt(unittest.TestCase):

    def test_text(self):
        txt = '12\n3\t\r\n4)_@#$_-?><.SD中 文。，F'
        m = hashlib.md5()
        m.update(txt.encode('utf-8'))
        md5 = m.hexdigest()
        self.assertEqual(get_hash(txt), md5)

    def test_other_data(self):
        data = [{'a': True, 'b': 11}, (1.3, 43, '33'), {3, 4, '55'}, [['中文。，']]]
        m = hashlib.md5()
        m.update(str(data).encode('utf-8'))
        md5 = m.hexdigest()
        self.assertEqual(get_hash(data), md5)
        self.assertEqual(get_hash(str(data)), md5)

    def test_salt(self):
        data = b'sdfKK32411112sdfd'
        m = hashlib.sha3_512(b'>>>kK3.2')
        m.update(data)
        md5 = m.hexdigest()
        self.assertEqual(get_hash(data, salt='>>>kK3.2', hash_name='sha3_512'), md5)
        self.assertEqual(get_hash(data, salt=b'>>>kK3.2', hash_name='sha3_512'), md5)


if __name__ == '__main__':
    unittest.main()
