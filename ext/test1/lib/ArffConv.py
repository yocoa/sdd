#!/usr/bin/env python

import sys

def convert(raw_list):
    # domain \t label \t features
    attr_length = len(raw_list[0].strip('\r\n').split('\t')[-1].split(','))

    result_list = [
        '@RELATION XXX',
        ''
    ]
    for i in range(1, attr_length + 1):
        result_list.append('@ATTRIBUTE a%d REAL' % i)
    result_list += [
        '@ATTRIBUTE class {B,W}',
        '',
        '@DATA'
    ]

    for line in raw_list:
        line = line.strip('\r\n')
        if not line:
            continue
        line = line.replace('NaN', '-1') 
        
        label = line.split('\t')[1]
        features = line.split('\t')[-1]
        result_list.append(features + ',' + label)
    return result_list
