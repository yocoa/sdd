#!/usr/bin/env python
# coding: utf-8

import sys
import re
import random
import json
import os
import time
import editdistance

from lib import DataBox
import subprocess

def load_train(path, train_selection):
    train_list = []

    assert train_selection in ['small', 'large']
    filenames = [train_selection + '.B', train_selection + '.W']

    for name in filenames:
        with open('/'.join([path, name]), 'r') as f:
            for line in f:
                domain = line.strip()
                if not domain:
                    continue

                label = 'W' if name.endswith('.W') else 'B'
                train_list.append((domain, label))
    return train_list

def load_data(path):
    data_list = []
    with open('/'.join([path, 'top-1w.txt']), 'r') as f:
        for line in f:
            domain = line.strip()
            if not domain:
                continue

            data_list.append(domain)
    return data_list

class KMeansSelector(object):

    def __init__(self, domain_list):
        self._domain_list = [d for d in domain_list]
        cache_file = 'cache.json'

        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                self._dist = json.loads(f.read())
        else:
            print 'Generating caceh...'
            with open(cache_file, 'w') as f:
                m = len(self._domain_list)
                self._dist = [[editdistance.eval(self._domain_list[i], self._domain_list[j]) for j in range(m)] for i in range(m)]
                f.write(json.dumps(self._dist))


    """
    n: 聚类的簇的数量
    times: 聚类尝试的次数

    返回n个簇的质心域名的列表
    """
    def select(self, n, times=1):
        res, cost = self._select(n)
        while times > 1:
            r, c = self._select(n)
            if c < cost:
                res, cost = r, c
            times -= 1
        return res

    """
    n: 聚类的簇的数量

    返回n个簇的质心域名的列表，以及最优的代价
    """
    def _select(self, n):
        m = len(self._domain_list)
        assert m >= n, "The parameter 'n' cannot be larger than the number of domains"
        centers = random.sample(range(m), n)
        # print "centers", centers
        updated, cost = True, None
        while updated:
            # print("=========")
            # 计算每个点属于哪个簇
            points = [[] for i in range(n)]
            for i in range(m):
                d, g = None, None
                for j in range(n):
                    t = self._dist[i][centers[j]]
                    if d is None or t < d:
                        d, g = t, j
                points[g].append(i)
            # print("points", points)
            new_centers, new_cost = [], 0
            # 计算每个簇的质心
            for i in range(n):
                ms, id = None, None
                p = points[i]
                sz = len(p)
                for j in range(sz):
                    s = 0
                    for k in range(sz):
                        s += self._dist[p[j]][p[k]]
                    if ms is None or s < ms:
                        ms, id = s, p[j]
                new_centers.append(id)
                new_cost += ms
            # print "new_centers", new_centers, "new_cost", new_cost
            updated = new_cost != cost
            centers, cost = new_centers, new_cost
        return [self._domain_list[i] for i in centers], cost

class HierarchicalSelector(object):

    def __init__(self, domain_list, strategy=None):
        print 'init!'

        self._domain_list = [d for d in domain_list]
        cache_file = 'cache.json'

        if strategy is None:
            strategy = "single"
        self._strategy = self._single_strategy

        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                self._dist = json.loads(f.read())
        else:
            print 'Generating caceh...'
            with open(cache_file, 'w') as f:
                m = len(self._domain_list)
                self._dist = []
                for i in range(m):
                    self._dist.append([editdistance.eval(self._domain_list[i], self._domain_list[j]) for j in range(m)])
                f.write(json.dumps(self._dist))

    """
    n: 聚类的簇的数量

    返回n个簇的质心域名的列表，以及最优的代价
    """
    def select(self, n):
        print 'select'
        m = len(self._domain_list)
        assert m >= n, "The parameter 'n' cannot be larger than the number of domains"
        cluster = [[i] for i in range(m)]
        
        count = 0
        while m > n:
            print count
            count+=1

            cost, pi, pj = None, None, None
            for i in range(m - 1):
                for j in range(i + 1, m):
                    c = self._strategy(cluster[i], cluster[j])
                    if cost is None or c < cost:
                        cost, pi, pj = c, i, j
            for x in cluster[pj]:
                cluster[pi].append(x)
            cluster.pop(pj)
            m -= 1
        # print cluster
        res = []
        for i in range(m):
            min_s, id = None, None
            for j in cluster[i]:
                s = 0
                for k in cluster[i]:
                    s += self._dist[j][k]
                if min_s is None or s < min_s:
                    min_s, id = s, j
            res.append(self._domain_list[id])
        return res

    def _single_strategy(self, v1, v2):
        res = None
        for i in v1:
            for j in v2:
                d = self._dist[i][j]
                if res is None or d < res:
                    res = d
        return res

    """
    计算两个字符串的编辑距离
    """
    @staticmethod
    def _edit_dis(s, t):
        if s == t:
            return 0
        if len(s) == 0:
            return len(t)
        elif len(t) == 0:
            return len(s)
        v0 = [None] * (len(t) + 1)
        v1 = [None] * (len(t) + 1)
        for i in range(len(v0)):
            v0[i] = i
        for i in range(len(s)):
            v1[0] = i + 1
            for j in range(len(t)):
                cost = 0 if s[i] == t[j] else 1
                v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
            for j in range(len(v0)):
                v0[j] = v1[j]
        return v1[len(t)]

if __name__ == '__main__':
    train_selection, selection, number = 'small', 'lexical', '30'
    if len(sys.argv) > 3:
        train_selection, selection, number = sys.argv[1], sys.argv[2], int(sys.argv[3])

    train = load_train('train/', train_selection)
    data = load_data('data/')

    if selection == 'lexical':
        start_time = time.time()
        arff_filename = DataBox.run(train, data[:number], selection)
        delta = time.time() - start_time

    if selection == 'topk':
        start_time = time.time()
        arff_filename = DataBox.run(train, data[:number], selection)
        delta = time.time() - start_time

    if selection == 'kmeans':
        kms = KMeansSelector(data)
        x = kms.select(number, 10)
        start_time = time.time()
        arff_filename = DataBox.run(load_train('train/'), x, selection)
        delta = time.time() - start_time

    if selection == 'topk2':
        start_time = time.time()
        arff_filename = DataBox.run(train, data[:number], selection)
        delta = time.time() - start_time

    if selection == 'kmeans2':
        kms = KMeansSelector(data)
        x = kms.select(number, 10)
        start_time = time.time()
        arff_filename = DataBox.run(load_train('train/'), x, selection)
        delta = time.time() - start_time

    cmd = 'java -classpath lib/weka.jar weka.classifiers.trees.RandomForest -t %s -i' % arff_filename
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0]
    tmp = re.search(r'Weighted Avg\.(.*\..*)', output).group(1).strip()
    p, r, f1 = re.split(r'\s+', tmp)[2:5]
    print '\t'.join([selection, str(number), p, r, f1, str(delta)])
