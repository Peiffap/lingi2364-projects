#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Benchmarks for the various frequent pattern mining algorithms.
"""

import time

import apriori_singleton_member as asm
import apriori_list_prefix as alp
import apriori_dict as ad

if __name__ == "__main__":
    times = []
    algs = [asm.apriori, alp.apriori, ad.apriori]
    names = ['asm', 'alp', 'ad']
    for alg in algs:
        s = time.perf_counter()
        alg("../statement/Datasets/retail.dat", 0.01)
        e = time.perf_counter()
        print()
        print()
        times.append(e-s)
    for i in range(len(times)):
        print('Time elapsed for %s: %g s' % (names[i], times[i]))
        print()

