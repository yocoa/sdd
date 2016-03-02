#!/usr/bin/env python
# encoding: utf-8

import os
import json

from simhash import Simhash, SimhashIndex 
import sys
sys.path.append('../StrVisualDistance')
import StrVisualDistance

BETA = 0.0356
_TRAIN_FILE = os.path.dirname(os.path.abspath(__file__)) + '/../../data/train'
with open(_TRAIN_FILE, 'r') as f:
    _TRAIN = json.load(f)

_INDEX = None

def _build_index():
    global _INDEX
    index_list = []
    for domain in _TRAIN.keys():
        sim = Simhash(domain)
        index_list.append((domain, sim))
    _INDEX = SimhashIndex(index_list, k=100)

def _pop_node(all_nodes, sim_list):
    if sim_list:
        d = sim_list[0]
        if d in sim_list:
            sim_list.remove(d)
        if d in all_nodes:
            all_nodes.remove(d)
        return d
    return ''


def calc(domain):
    global _TRAIN
    global _INDEX
    all_nodes = set(_TRAIN.keys())
    tmp_sim_list = _INDEX.get_near_dups(Simhash(domain))
    sim_list = tmp_sim_list + list(all_nodes - set(tmp_sim_list))

    min_distance = sys.maxint
    min_node = ''

    while all_nodes:
        board_node = _pop_node(all_nodes, sim_list)
        d = StrVisualDistance.distance(board_node, domain)
        if d < min_distance:
            min_distance = d
            min_node = board_node
        tmp = list(all_nodes)
        for n in tmp:
            _d = StrVisualDistance.distance(n, domain)
            if _d >= 2 * d:
                all_nodes.remove(n)
    return min_node, min_distance, 'B' if min_distance < BETA else 'W'

_build_index()
