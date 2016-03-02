#!/usr/env/bin python
# encoding: utf-8

import unittest
import MinVisualDistance

class TestStrVisualDistance(unittest.TestCase):
    
    def test_similarity(self):
        self.assertTrue(MinVisualDistance.calc('qq.com'))
