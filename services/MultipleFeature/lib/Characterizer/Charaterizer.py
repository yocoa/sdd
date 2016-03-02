#!/usr/env/bin python
# encoding: utf-8

import os

def convert(domain):
    tmp = '.domain.tmp'
    with open(tmp, 'w') as f:
        f.write('%s\tX' % (domain))
    output = os.popen('java -jar MalDomainFeature.jar %s' % tmp).read()
    vector = output.split('\n')[0].split('\t')[-1]
    return vector
