#!/usr/env/bin python
# encoding: utf-8

import networkx as nx
import os
import re

_G = nx.Graph()
_G_FILE = os.path.dirname(os.path.abspath(__file__)) + '/../../data/train'
_PR = {}

def _build_graph():
    global _G
    global _G_FILE
    global _PR

    with open(_G_FILE, 'r') as f:
        for i, line in enumerate(f):
            if i > 1000000:
                print 'Too many records!'
                break
            try:
                uid, domain = line.strip().split(' ')
                _G.add_edge(uid, domain.lower())
            except:
                pass
    _PR = nx.pagerank(_G)

def get_weight():
    global _PR
    return _PR

_build_graph()
