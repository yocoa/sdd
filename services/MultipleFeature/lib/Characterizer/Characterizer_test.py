#!/usr/env/bin python
# encoding: utf-8

import unittest
import Characterizer as C

class TestCharacterizer(unittest.TestCase):
    
    def test_convert(self):
        self.assertTrue(C.convert('qq.com'))
