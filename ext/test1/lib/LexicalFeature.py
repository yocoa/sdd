#!/usr/env/bin python
# encoding: utf-8

import re
import sys

def get_feature(string):
    cleaned_string = string.strip('.')
    funcs = (
        _total_length, #整体长度
        _contains_ip_addr, #是否含有IP地址
        _dot_count, #点的个数
        _special_char_count, #特殊字符的个数
        _num_count, #数字的个数
        _num_ratio, #数字占整体的比例
        _num_freq, #连续数字块的个数
        _cap_letter_count, #大写字母的个数
        _dots_max_distance, #相邻两个点之间的最大长度
        _num_max_distance, #连续数字的最大长度
        _letter_max_distance, #连续字母的最大长度
    )
    if not cleaned_string:
        return [-1 for i in range(len(funcs))]
    return [f(cleaned_string) for f in funcs]

def _total_length(string):
    return len(string)

def _contains_ip_addr(string):
    return 1 if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', string) else 0

def _dot_count(string):
    return string.count('.')

def _special_char_count(string):
    return len(re.findall(r'\W', string))

def _num_count(string):
    return len(re.findall(r'\d', string))

def _num_ratio(string):
    return float(_num_count(string)) / float(_total_length(string))

def _num_freq(string):
    return len(re.findall(r'\d+', string))

def _cap_letter_count(string):
    return len(re.findall(r'[A-Z]+', string))

def _dots_max_distance(string):
    strs = re.split(r'\.', '.%s.' % string)
    distance = -sys.maxint - 1
    for s in strs:
        if len(s) > distance:
            distance = len(s)
    return distance

def _num_max_distance(string):
    strs = re.split(r'\D', '.%s.' % string)
    distance = -sys.maxint - 1
    for s in strs:
        if len(s) > distance:
            distance = len(s)
    return distance


def _letter_max_distance(string):
    strs = re.split(r'[^a-zA-Z]', '.%s.' % string)
    distance = -sys.maxint - 1
    for s in strs:
        if len(s) > distance:
            distance = len(s)
    return distance
