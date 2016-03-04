#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import json

_DATA = {}

def run(domain):
    global _DATA
    return _DATA[domain] if domain in _DATA else None

def _load_data():
    global _DATA

    cur_dir = os.path.dirname(os.path.abspath(__file__))
    train_file = cur_dir + '/../data/train'
    sys.path.append(train_file)
    with open(train_file, 'r') as f:
        for line in f:
            data = json.loads(line)
            _DATA[data['url']] = data

_load_data()
