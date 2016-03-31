#!/usr/bin/env python
# coding: utf-8

import sys

from lib import DataBox
import subprocess

def load_train(path):
    train_list = []
    filenames = ['lexical.bad', 'lexical.good', 'type.bad', 'type.good']
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

if __name__ == '__main__':
    selection, number = 'default', '30'
    if len(sys.argv) > 2:
        selection, number = sys.argv[1], sys.argv[2]

    if selection == 'default':
        arff_filename = DataBox.run(load_train('train/'), load_data('data/')[:int(number)])
    print arff_filename
    cmd = 'java -classpath lib/weka.jar weka.classifiers.trees.RandomForest -t %s -i' % arff_filename
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0]
    print output



