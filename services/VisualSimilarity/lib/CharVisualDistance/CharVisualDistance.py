#!/usr/env/bin python
# encoding: utf-8

from scipy.spatial.distance import cosine
import math

import sys
sys.path.append('../CharToImage')
sys.path.append('../ImageToVector')
import CharToImage
import ImageToVector

def _cut(vector, start, limit):
    new_v = []
    width = int(math.sqrt(len(vector)))
    for i in range(width):
        for j in range(width):
            if start <= j < limit + start:
                new_v.append(vector[i * width + j])
    return new_v

def distance(char1, char2):
    im1, im2 = CharToImage.convert(char1), CharToImage.convert(char2)
    v1, v2 = ImageToVector.convert(im1), ImageToVector.convert(im2)

    min_distance = sys.maxint
    content_width = CharToImage.WIDTH * 4 / 5
    margin = CharToImage.WIDTH - content_width
    for i in range(margin):
        for j in range(margin):
            new_v1, new_v2 = _cut(v1, i, content_width), _cut(v2, j, content_width)
            d = cosine(new_v1, new_v2)
            if d < min_distance:
                min_distance = d
    return min_distance
