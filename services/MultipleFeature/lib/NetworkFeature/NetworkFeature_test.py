#!/usr/env/bin python
# encoding: utf-8

import unittest
from NetworkFeature import _NetworkFeature

class TestNetworkFeature(unittest.TestCase):
    
    def test_get_feature(self):
        n = _NetworkFeature('google.com')
        self.assertTrue(n.get_feature())
