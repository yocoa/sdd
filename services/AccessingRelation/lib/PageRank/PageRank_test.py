#!/usr/env/bin python
# encoding: utf-8

import unittest
import PageRank as P

class TestAdapter(unittest.TestCase):
    
    def test_calc(self):
        self.assertTrue(P.get_weight())
        '''
        pr, mapper = P.get_weight()
        tmp = sorted(pr.iteritems(), key=lambda i:i[1])
        i = 1
        for name, weight in tmp:
            if name in mapper:
                print '==', i, name, mapper[name], weight
                i+=1
        '''
