#!/usr/env/bin python
# encoding: utf-8

import unittest
import BgpBase

class TestBgpBase(unittest.TestCase):
    
    def test_run(self):
        self.assertTrue(BgpBase.run('qq.com'))
