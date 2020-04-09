#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 11:56:32 2020

@author: admin
"""

import time

from itertools import groupby
from collections import Counter

n = 100000

a = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
s = time.perf_counter()
for i in range(n):
    [sum(1 for _ in group) for key, group in groupby(a)]
print(time.perf_counter() - s)

s = time.perf_counter()
for i in range(n):
    [len(list(group)) for key, group in groupby(a)]
print(time.perf_counter() - s)

s = time.perf_counter()
for i in range(n):
    ctr= Counter(a).values()
print(time.perf_counter() - s)

s = time.perf_counter()
for i in range(n):
    {x: a.count(x) for x in set(a)}.values()
print(time.perf_counter() - s)

s = time.perf_counter()
for i in range(n):
    {x: a.count(x) for x in a}.values()
print(time.perf_counter() - s)

