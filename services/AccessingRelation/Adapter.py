#!/usr/env/bin python
# encoding: utf-8

from lib.PageRank import PageRank

def run(*args):
    pr = PageRank.get_weight()
    return pr

def run_test(*args):
    pr = PageRank.get_weight()
    return pr
