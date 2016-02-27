#!/usr/env/bin python
# encoding: utf-8

import unittest
import CharToImage

class TestCharToImage(unittest.TestCase):
    
    def test_convert(self):
        self.assertTrue(CharToImage.convert('a'))
