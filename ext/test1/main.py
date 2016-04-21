#!/usr/bin/env python
# coding: utf-8

import sys
import re
import random
import json
import os
import editdistance

from lib import DataBox
import subprocess

def load_train(path):
    train_list = []
    #filenames = ['lexical.bad', 'lexical.good', 'type.bad', 'type.good']
    filenames = ['raw.B', 'raw.W']
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
            print 'Exists'
            with open(cache_file, 'r') as f:
                self._dist = json.loads(f.read())
        with open(cache_file, 'w') as f:
            print 'Dumps'
            m = len(self._domain_list)
            #self._dist = [[self._edit_dis(self._domain_list[i], self._domain_list[j]) for j in range(m)] for i in range(m)]
            self._dist = []
            for i in range(m):
                if i % 500 == 0:
                    print "*", i
                self._dist.append([editdistance.eval(self._domain_list[i], self._domain_list[j]) for j in range(m)])
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

    """
    计算两个字符串的编辑距离
    """
    @staticmethod
    def _edit_dis(a, b):
        na = len(a)
        nb = len(b)
        f = [[0 for j in range(nb + 1)] for i in range(na + 1)]
        for i in range(na):
            f[i][-1] = i + 1
        for i in range(nb):
            f[-1][i] = i + 1
        for i in range(na):
            for j in range(nb):
                if a[i] == b[j]:
                    f[i][j] = f[i - 1][j - 1]
                else:
                    f[i][j] = min(f[i - 1][j] + 1, f[i][j - 1] + 1, f[i - 1][j - 1] + 1)
        return f[na - 1][nb - 1]


'''
if __name__ == "__main__":
    kms = KMeansSelector(["wangyb.net", "www.wangyb.net", "www.iie.ac.cn", "iie.ac.cn", "google.com", "google.com.cn", "google.com.lt"])
    # 选出3个质心，随机尝试5次
    x = kms.select(3, 5)
    x.sort()
    print x
'''

if __name__ == '__main__':
    data = load_data('data/')
    kms = KMeansSelector(data)
    
    print kms
    x = kms.select(5, 1)
    print "--"

    sys.exit(0)
    selection, number = 'default', '30'
    if len(sys.argv) > 2:
        selection, number = sys.argv[1], int(sys.argv[2])

    train = load_train('train/')
    data = load_data('data/')

    if selection == 'default':
        arff_filename = DataBox.run(train, data[:number], nolexical=True)
        arff_filename2 = DataBox.run(train, data[:number], nolexical=False)
    if selection == 'random':
        copied_data = [i for i in data]
        random.shuffle(copied_data)
        arff_filename = DataBox.run(train, copied_data[:number], nolexical=True)
        arff_filename2 = DataBox.run(train, copied_data[:number], nolexical=False)
    if selection == 'cluster':
        copied_data = get_cluster_centers(data, number)
        random.shuffle(copied_data)
        arff_filename = DataBox.run(load_train('train/'), copied_data[:number], nolexical=True)
        arff_filename2 = DataBox.run(load_train('train/'), copied_data[:number], nolexical=False)

    cmd = 'java -classpath lib/weka.jar weka.classifiers.trees.RandomForest -t %s -i' % arff_filename
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0]
    tmp = re.search(r'Weighted Avg\.(.*\..*)', output).group(1).strip()
    p, r, f1 = re.split(r'\s+', tmp)[2:5]

    cmd = 'java -classpath lib/weka.jar weka.classifiers.trees.RandomForest -t %s -i' % arff_filename2
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0]
    tmp = re.search(r'Weighted Avg\.(.*\..*)', output).group(1).strip()
    new_p, new_r, new_f1 = re.split(r'\s+', tmp)[2:5]
    print '\t'.join([selection, str(number), p, r, f1, new_p, new_r, new_f1])
