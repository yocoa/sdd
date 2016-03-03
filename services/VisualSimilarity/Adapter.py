#!/usr/env/bin python
# encoding: utf-8

from lib.MinVisualDistance import MinVisualDistance

def run(domain):
    result = MinVisualDistance.calc(domain)
    return result

def run_test(domain):
    return 'google.com', 0.7150659255665122, 'W'
