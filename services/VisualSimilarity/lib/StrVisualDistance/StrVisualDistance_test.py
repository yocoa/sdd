#!/usr/env/bin python
# encoding: utf-8

import unittest
import StrVisualDistance

class TestStrVisualDistance(unittest.TestCase):
    
    def test_similarity(self):
        d1 = StrVisualDistance.distance('google.com', 'g00gle.com')
        d2 = StrVisualDistance.distance('google.com', 'taobao.com')
        self.assertTrue(d1 < d2)
