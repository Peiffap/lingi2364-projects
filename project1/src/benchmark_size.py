#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Benchmarks for the various frequent pattern mining algorithms.
"""
from timeout import timeout
import pickle

from apriori_prefix import apriori as apriori_prefix
from apriori_prefix_vdb import apriori as apriori_prefix_vdb
from apriori_dict import apriori as apriori_dict
from dfs1 import dfs as dfs1
from dfs2 import dfs as dfs2

import tracemalloc

import matplotlib.pyplot as plt

plt.style.use("ggplot")

if __name__ == "__main__":
    algs = [apriori_prefix, apriori_prefix_vdb, apriori_dict, dfs1, dfs2]
    names = ['apriori_prefix', 'apriori_prefix_vdb', 'apriori_dict', 'dfs1', 'dfs2']
    datasets = ['retail', 'accidents', 'chess', 'pumsb', 'pumsb_star', 'connect', 'mushroom']

    dataset_freqs = {}
    dataset_freqs['retail'] = [0.1, 0.05, 0.01, 0.005, 0.004, 0.003, 0.002, 0.001, 0.0005, 0.00001]
    dataset_freqs['accidents'] = [0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.55, 0.5]
    dataset_freqs['chess'] = [0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.55, 0.5, 0.45]
    dataset_freqs['pumsb'] = [0.99, 0.98, 0.97, 0.96, 0.95, 0.94, 0.93, 0.92, 0.91, 0.9, 0.89, 0.88, 0.87, 0.86, 0.85]
    dataset_freqs['pumsb_star'] = [0.75, 0.7, 0.65, 0.6, 0.55, 0.5, 0.45, 0.4, 0.35, 0.3]
    dataset_freqs['connect'] = [0.99, 0.98, 0.97, 0.96, 0.95, 0.94, 0.93, 0.92, 0.91, 0.9]
    dataset_freqs['mushroom'] = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.05]

    sizes = {}
    for data in datasets:
        sizes[data] = {}
        for alg in names:
            sizes[data][alg] = []

    for data in datasets:
        for i in range(len(algs)):
            print()
            alg = algs[i]
            for freq in dataset_freqs[data]:
                try:
                    tracemalloc.start()
                    print("data: %s, alg: %s, freq: %g" % (data, names[i], freq))
                    before = tracemalloc.take_snapshot()
                    with timeout(seconds=200):
                        alg("../statement/Datasets/%s.dat" % (data), freq, verbose=False)
                    after = tracemalloc.take_snapshot()
                    nkib = sum([x.size_diff for x in after.compare_to(before, 'lineno')]) / 1024
                    sizes[data][names[i]].append(nkib)
                    tracemalloc.stop()
                except:
                    tracemalloc.stop()
                    print("Timeout")
                    break

    pickle.dump(sizes, open("../report/data/sizes.p", "wb"))