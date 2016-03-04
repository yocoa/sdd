#!/usr/env/bin python
# encoding: utf-8

import os

def convert(domain):
    tmp = '.domain.tmp'
    current_file_path = os.path.dirname(os.path.abspath(__file__))
    jar_file = os.path.join(current_file_path, 'MalDomainFeature.jar')
    with open(tmp, 'w') as f:
        f.write('%s\tX' % (domain))
    output = os.popen('java -jar %s %s' % (jar_file, tmp)).read()
    vector_str = output.split('\n')[0].split('\t')[-1]
    vector = vector_str.split(',')
    return vector
