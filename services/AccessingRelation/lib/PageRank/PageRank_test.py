#!/usr/env/bin python
# encoding: utf-8

import unittest
import PageRank as P

class TestAdapter(unittest.TestCase):
    
    def test_calc(self):
        self.assertTrue(P.get_weight())
