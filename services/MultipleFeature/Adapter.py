#!/usr/env/bin python
# encoding: utf-8

from lib.Characterizer import Characterizer
from lib.Classifier import Classifier

def run(domain):
    vector = Characterizer.convert(domain)
    print vector, 'Vector'
    #label = Classifier.classify(vector)
    #print label, 'Label'
    label = 1
    return label
