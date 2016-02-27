#!/usr/env/bin python
# encoding: utf-8

import numpy as np

def convert(image):
    vector = []
    for x in np.array(image).flatten():
        vector.append(float(x))
    return vector
