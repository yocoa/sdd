#!/usr/env/bin python
# encoding: utf-8

import lib.BgpBase as BgpBase
import os
import sys
import json
import re

def run(domain):
    result = BgpBase.run(domain)
    result['dns'] = re.sub(r'\n\s+', '\n', result['dns']) 
    return result

def run_test(domain):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    train_file = cur_dir + '/data/train'
    sys.path.append(train_file)
    with open(train_file, 'r') as f:
        for line in f:
            data = json.loads(line)
            data['dns'] = re.sub(r'\n\s+', '\n', data['dns']) 
            return data
