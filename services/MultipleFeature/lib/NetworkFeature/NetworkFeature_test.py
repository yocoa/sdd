#!/usr/env/bin python
# encoding: utf-8

import unittest
import NetworkFeature as NF

class TestNetworkFeature(unittest.TestCase):
    
    def test_get_feature(self):
        d = 'qq.com'
        print NF.get_feature(d)
