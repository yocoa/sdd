#!/usr/env/bin python
# encoding: utf-8

import os

from weka.classifiers import RandomForest 

_TRAIN_ARFF = os.path.dirname(os.path.abspath(__file__)) + '/../../data/train.arff'
_QUERY_ARFF = os.path.dirname(os.path.abspath(__file__)) + '/.query.arff'

def _vector_to_arff(vector):
    global _QUERY_ARFF
    with open(_QUERY_ARFF, 'w') as f:
        text = '''@RELATION query
@ATTRIBUTE a1 real
@ATTRIBUTE a2 real
@ATTRIBUTE a3 real
@ATTRIBUTE a4 real
@ATTRIBUTE a5 real
@ATTRIBUTE a6 real
@ATTRIBUTE a7 real
@ATTRIBUTE a8 real
@ATTRIBUTE a9 real
@ATTRIBUTE a10 real
@ATTRIBUTE a11 real
@ATTRIBUTE a12 real
@ATTRIBUTE a13 real
@ATTRIBUTE a14 real
@ATTRIBUTE a15 real
@ATTRIBUTE a16 real
@ATTRIBUTE a17 real
@ATTRIBUTE a18 real
@ATTRIBUTE a19 real
@ATTRIBUTE a20 real
@ATTRIBUTE class {B,W}

@DATA
%s
''' % ','.join([str(i) for i in vector] + ['W'])
        f.write(text)

def classify(vector):
    global _TRAIN_ARFF
    _vector_to_arff(vector)

    c = RandomForest()
    c.train(_TRAIN_ARFF)
    predictions = c.predict(_QUERY_ARFF)
    result = [(i.predicted, i.probability) for i in predictions]
    return result
