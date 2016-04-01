#!/usr/bin/env python
# coding: utf-8

import sys
import re
import random

from lib import DataBox
import subprocess

def load_train(path):
    train_list = []
    #filenames = ['lexical.bad', 'lexical.good', 'type.bad', 'type.good']
    filenames = ['type.bad', 'type.good']
    for name in filenames:
        with open('/'.join([path, name]), 'r') as f:
            for line in f:
                domain = line.strip()
                if not domain:
                    continue

                label = 'W' if name.endswith('.good') else 'B'
                train_list.append((domain, label))
    return train_list

def load_data(path):
    data_list = []
    with open('/'.join([path, 'top-1m.txt']), 'r') as f:
        for line in f:
            domain = line.strip()
            if not domain:
                continue

            data_list.append(domain)
    return data_list

def chunks(l, n):
     chunk_size = len(l) / n
     for i in xrange(0, n):
             yield l[i*chunk_size:i*chunk_size+chunk_size]


if __name__ == '__main__':
    selection, number = 'default', '30'
    if len(sys.argv) > 2:
        selection, number = sys.argv[1], sys.argv[2]

    if selection == 'default':
        arff_filename = DataBox.run(load_train('train/'), load_data('data/')[:int(number)])
    if selection == 'random':
        copied_data = [i for i in load_data('data/')]
        random.shuffle(copied_data)
        arff_filename = DataBox.run(load_train('train/'), copied_data[:int(number)])
    if selection == 'random2':
        copied_data = [i for i in load_data('data/')]
        copied_data2 = []
        for chunk in list(chunks(copied_data, int(number))):
            copied_data2.append(random.choice(chunk))
        arff_filename = DataBox.run(load_train('train/'), copied_data2[:int(number)])
    cmd = 'java -classpath lib/weka.jar weka.classifiers.trees.RandomForest -t %s -i' % arff_filename
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0]
    tmp = re.search(r'Weighted Avg\.(.*\..*)', output).group(1).strip()
    p, r, f1 = re.split(r'\s+', tmp)[2:5]
    print '\t'.join([selection, number, p, r, f1])
