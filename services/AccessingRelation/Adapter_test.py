#!/usr/env/bin python
# encoding: utf-8

import unittest
import Adapter as A

class TestAdapter(unittest.TestCase):
    
    def test_run(self):
        self.assertTrue(A.run())
