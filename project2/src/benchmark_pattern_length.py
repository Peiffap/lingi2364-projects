#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Benchmarks for the various top-k sequence mining algorithms.
"""

import time
from timeout import timeout
import pickle
import matplotlib.pyplot as plt


plt.style.use("ggplot")

def mean(x):
    return sum(x)/len(x)

def aux(algs, names):
    datasets = ['Protein', 'Reuters']
    pos_files = ['SRC1521', 'earn']
    neg_files = ['PKA_group15', 'acq']

    lengths = {}
    for data in datasets:
        lengths[data] = {}
        for alg in names:
            lengths[data][alg] = []

    for j, data in enumerate(datasets):
        for i in range(len(algs)):
            print()
            alg = algs[i]
            k = 1
            while True:
                try:
                    print("data: %s, alg: %s, k: %g" % (data, names[i], k))
                    res = []
                    with timeout(seconds=100):
                        res = alg("%s/%s.txt" % (data, pos_files[j]), "%s/%s.txt" % (data, neg_files[j]), k, False, True)
                    lengths[data][names[i]].append(mean([len(x) for x in res]))
                    k *= 2
                except (TimeoutError, RecursionError) as e:
                    print(e)
                    break

    pickle.dump(lengths, open("../report/data/lengths.p", "wb"))

if __name__ == "__main__":
    import sumsup.PrefixSpan_sumsup_heap as ps_sup
    import wracc.PrefixSpan_wracc_heap as ps_wracc
    import closed_wracc.CloSpan_wracc_heap as cs_wracc
    import closed_abswracc.CloSpan_abswracc_heap as cs_abswracc
    import closed_infogain.CloSpan_infogain_heap as cs_infogain
    algs = [file.main for file in [ps_sup, ps_wracc, cs_wracc, cs_abswracc, cs_infogain]]
    names = ['Sumsup', 'WRAcc', 'Closed WRAcc', 'Closed AbsWRAcc', 'Closed IG']

    aux(algs, names)
