#!/usr/env/bin python
# encoding: utf-8

import lib.BgpBase as BgpBase
import os
import sys
import json

def run(domain):
    result = BgpBase.run(domain)
    return result

def run_test(domain):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    train_file = cur_dir + '/data/train'
    sys.path.append(train_file)
    with open(train_file, 'r') as f:
        for line in f:
            data = json.loads(line)
            return data
