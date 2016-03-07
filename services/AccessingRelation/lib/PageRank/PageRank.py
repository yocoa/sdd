#!/usr/env/bin python
# encoding: utf-8

import networkx as nx
import os
import re

_G = nx.Graph()
_G_FILE = os.path.dirname(os.path.abspath(__file__)) + '/../../data/train'
_PR = {}
_MAPPER = {}

def _build_graph():
    global _G
    global _G_FILE
    global _PR
    global _MAPPER

    with open(_G_FILE, 'r') as f:
        for i, line in enumerate(f):
            if i > 1000000:
                print 'Too many records!'
                break
            try:
                uid, name, domain = line.lower().strip().split(' ')
                _G.add_edge(uid, name)
                if not _MAPPER.has_key(name):
                    _MAPPER[name] = set()
                _MAPPER[name].add(domain) 
            except:
                pass
    _PR = nx.pagerank(_G)

def get_weight():
    global _PR
    global _MAPPER
    return _PR, _MAPPER

_build_graph()
