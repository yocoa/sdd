#!/usr/bin/env python
# encoding: utf-8

import sys
sys.path.append('../CharVisualDistanceCache')
import CharVisualDistanceCache

ALPHA = 0.9
C = CharVisualDistanceCache.get_cache()

def set_alpha(alpha):
    global ALPHA
    ALPHA = alpha

def distance(str1, str2):
    len1 = len(str1)
    len2 = len(str2)
    dp = [
        [0 for j in range(len2 + 1)]
        for i in range(len1 + 1)
    ]
    for i in range(len1 + 1):
        dp[i][0] = i
    for j in range(len2 + 1):
        dp[0][j] = j
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                weight = ALPHA**min(i, j) * C[str1[i - 1]][str2[j - 1]]
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + weight
    return dp[len1][len2]
