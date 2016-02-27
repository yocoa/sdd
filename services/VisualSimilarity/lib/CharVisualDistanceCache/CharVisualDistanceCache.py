#!/usr/env/bin python
# encoding: utf-8

import os
import json

import sys
sys.path.append('../CharVisualDistance')
import CharVisualDistance

_CHARS = [''] + [chr(i) for i in range(97, 97 + 26)] + [str(i) for i in range(0, 10)] + ['.', '-']
_CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
_CACHE_FILE = os.path.join(_CURRENT_FILE_PATH, 'cache')

def _reset_chars_only_for_unittest(chars):
    global _CHARS
    _CHARS = chars

def get_cache():
    cache = None
    if os.path.exists(_CACHE_FILE):
        with open(_CACHE_FILE, 'r') as f:
            cache = json.load(f)
    else:
        temp_cache = _build_cache()
        cache = _normal_cache(temp_cache)
        with open(_CACHE_FILE, 'w') as f:
            json.dump(cache, f)
    return cache

def _build_cache():
    cache = {}
    for c1 in _CHARS:
        for c2 in _CHARS:
            if not cache.has_key(c1):
                cache[c1] = {}

            if cache.has_key(c2) and cache[c2].has_key(c1):
                cache[c1][c2] = cache[c2][c1]
            else:
                cache[c1][c2] = CharVisualDistance.distance(c1, c2)
    return cache

def _normal_cache(temp_cache):
    max_distance = -sys.maxint - 1
    for c1 in _CHARS:
        for c2 in _CHARS:
            if temp_cache[c1][c2] > max_distance:
                max_distance = temp_cache[c1][c2]

    cache = {}
    for c1 in _CHARS:
        for c2 in _CHARS:
            if not cache.has_key(c1):
                cache[c1] = {}

            if cache.has_key(c2) and cache[c2].has_key(c1):
                cache[c1][c2] = cache[c2][c1]
            else:
                cache[c1][c2] = temp_cache[c1][c2] / max_distance
    return cache
