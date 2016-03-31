#!/usr/bin/env python
# coding: utf-8

import LexicalFeature as LF
import editdistance
import ArffConv

def get_distances(domain, domain_list):
    distances = []
    for d in domain_list:
        distances.append(editdistance.eval(domain, d))
    return distances

def run(train_list, data_list):
    line_list = []
    for domain, label in train_list:
        v = LF.get_feature(domain)
        distances = get_distances(domain, data_list)
        v += distances #long vector(lexical + distances)
        line = '%s\t%s\t%s' % (domain, label, ','.join(map(lambda x:str(x), v)))
        line_list.append(line)
    arff_content = '\n'.join(ArffConv.convert(line_list))

    arff_filename = '.tmp.arff'
    with open(arff_filename, 'w') as f:
        f.write(arff_content)
    return arff_filename
