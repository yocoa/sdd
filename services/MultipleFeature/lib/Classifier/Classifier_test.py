#!/usr/env/bin python
# encoding: utf-8

import unittest
import Classifier as C

class TestClassifier(unittest.TestCase):
    
    def test_classify(self):
        vector = [11,0,2,0,0,0.0,0,0,4,0,4,-1,0,0,0,2,2,23417.5,-1,0]
        self.assertTrue(C.classify(vector))
