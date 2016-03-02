#!/usr/env/bin python
# encoding: utf-8

import unittest
import  Charaterizer as C

class TestNetworkFeature(unittest.TestCase):
    
    def test_convert(self):
        self.assertTrue(C.convert('google.com'))
