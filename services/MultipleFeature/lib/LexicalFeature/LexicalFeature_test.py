#!/usr/env/bin python
# encoding: utf-8

import unittest
import LexicalFeature as LF

class TestLexicalFeature(unittest.TestCase):
    
    def test_get_feature(self):
        s = 'google-123.123Abc.com'
        self.assertEquals(LF._total_length(s), 21)
        self.assertEquals(LF._contains_ip_addr(s), 0)
        self.assertEquals(LF._dot_count(s), 2)
        self.assertEquals(LF._special_char_count(s), 3)
        self.assertEquals(LF._num_count(s), 6)
        self.assertEquals(LF._num_ratio(s), 6 / 21.0)
        self.assertEquals(LF._num_freq(s), 2)
        self.assertEquals(LF._cap_letter_count(s), 1)
        self.assertEquals(LF._dots_max_distance(s), 10)
        self.assertEquals(LF._num_max_distance(s), 3)
        self.assertEquals(LF._letter_max_distance(s), 6)
