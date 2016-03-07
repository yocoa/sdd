#!/usr/env/bin python
# encoding: utf-8

from lib.PageRank import PageRank

def run(*args):
    pr, mapper = PageRank.get_weight()
    return pr, mapper

def run_test(*args):
    pr, mapper = PageRank.get_weight()
    return pr, mapper
