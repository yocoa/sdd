#!/usr/env/bin python
# encoding: utf-8

import unittest
import ImageToVector

import sys
sys.path.append('../CharToImage')
import CharToImage

class TestImageToVector(unittest.TestCase):
    
    def test_convert(self):
        image = CharToImage.convert('a')
        self.assertTrue(ImageToVector.convert(image))
