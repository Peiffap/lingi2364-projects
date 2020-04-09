#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 11:56:32 2020

@author: admin
"""

def contains(patt1, patt2):
    k = -1
    for i in range(len(patt1)):
        for j in range(k+1, len(patt2) + 1):
            if j == len(patt2):
                return False
            if patt1[j] == patt2[i]:
                k = j
                break
    return True

print(contains([1, 2, 3, 1], [1, 1, 2]))