#!/usr/env/bin python
# encoding: utf-8

import unittest
import CharVisualDistanceCache

class TestCharVisualDistanceCache(unittest.TestCase):

    def test_get_cache(self):
        CharVisualDistanceCache._reset_chars_only_for_unittest(['a', 'b', 'c'])
        cache = CharVisualDistanceCache.get_cache()
        self.assertTrue(cache)
        self.assertTrue(cache['a']['b'] == cache['b']['a'])
