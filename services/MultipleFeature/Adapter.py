#!/usr/env/bin python
# encoding: utf-8

from lib.Characterizer import Characterizer
from lib.Classifier import Classifier

def run(domain):
    vector = Characterizer.convert(domain)
    label = Classifier.classify(vector)
    return label

def run_test(domain):
    vector = [12,0,1,0,0,0.0,0,0,8,0,8,1820.0,1,1,1,2,1,75105.0,20020508,2]
    label = Classifier.classify(vector)
    return label
