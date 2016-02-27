#!/usr/env/bin python
# encoding: utf-8

import unittest
import CharVisualDistance

class TestCharVisualDistance(unittest.TestCase):
    
    def test_distance(self):
        d1, d2  = CharVisualDistance.distance('l', '1'), CharVisualDistance.distance('l', '0')
        self.assertTrue(d1 < d2)

        d1, d2  = CharVisualDistance.distance('l', '1'), CharVisualDistance.distance('1', 'l')
        self.assertTrue(d1 == d2)
