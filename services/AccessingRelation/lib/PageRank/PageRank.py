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
        for line in f:
            try:
                uid, domain = line.strip().split(' ')
                _G.add_edge(uid, domain.lower())
            except:
                pass
    _PR = nx.pagerank(_G)

def get_weight():
    global _PR
    tmp = sorted(_PR.iteritems(), key=lambda i:i[1])
    for i,j in tmp:
        if not re.match(r'\d+$', i):
            print i, j
    return _PR

_build_graph()
