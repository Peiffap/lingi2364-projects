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


if __name__ == "__main__":
    import sumsup.PrefixSpan_sumsup_heap as ps_heap
    import sumsup.PrefixSpan_sumsup_sorted_list as ps_sl
    import sumsup.SPADE as spade
    algs = [file.main for file in [ps_heap, ps_sl, spade]]
    names = ['PrefixSpan_heap', 'PrefixSpan_sorted_list', 'SPADE']
    datasets = ['Protein', 'Reuters']
    pos_files = ['SRC1521', 'earn']
    neg_files = ['PKA_group15', 'acq']

    times = {}
    for data in datasets:
        times[data] = {}
        for alg in names:
            times[data][alg] = []

    for j, data in enumerate(datasets):
        for i in range(len(algs)):
            print()
            alg = algs[i]
            k = 1
            while True:
                try:
                    print("data: %s, alg: %s, k: %g" % (data, names[i], k))
                    with timeout(seconds=200):
                        s = time.perf_counter()
                        alg("%s/%s.txt" % (data, pos_files[j]), "%s/%s.txt" % (data, neg_files[j]), k, False)
                        e = time.perf_counter()
                    times[data][names[i]].append(e-s)
                    k *= 2
                except TimeoutError as e:
                    print(e)
                    break

    pickle.dump(times, open("../report/data/times_sumsup.p", "wb"))


    import wracc.PrefixSpan_wracc_heap as ps_heap
    import wracc.PrefixSpan_wracc_sorted_list as ps_sl
    algs = [file.main for file in [ps_heap, ps_sl]]
    names = ['PrefixSpan_heap', 'PrefixSpan_sorted_list']
    datasets = ['Protein', 'Reuters']
    pos_files = ['SRC1521', 'earn']
    neg_files = ['PKA_group15', 'acq']

    times = {}
    for data in datasets:
        times[data] = {}
        for alg in names:
            times[data][alg] = []

    for j, data in enumerate(datasets):
        for i in range(len(algs)):
            print()
            alg = algs[i]
            k = 1
            while True:
                try:
                    print("data: %s, alg: %s, k: %g" % (data, names[i], k))
                    with timeout(seconds=200):
                        s = time.perf_counter()
                        alg("%s/%s.txt" % (data, pos_files[j]), "%s/%s.txt" % (data, neg_files[j]), k, False)
                        e = time.perf_counter()
                    times[data][names[i]].append(e-s)
                    k *= 2
                except TimeoutError as e:
                    print(e)
                    break

    pickle.dump(times, open("../report/data/times_wracc.p", "wb"))


    import closed_wracc.CloSpan_wracc_heap as cs_heap
    import closed_wracc.CloSpan_wracc_sorted_list as cs_sl
    algs = [file.main for file in [cs_heap, cs_sl]]
    names = ['CloSpan_heap', 'CloSpan_sorted_list']
    datasets = ['Protein', 'Reuters']
    pos_files = ['SRC1521', 'earn']
    neg_files = ['PKA_group15', 'acq']

    times = {}
    for data in datasets:
        times[data] = {}
        for alg in names:
            times[data][alg] = []

    for j, data in enumerate(datasets):
        for i in range(len(algs)):
            print()
            alg = algs[i]
            k = 1
            while True:
                try:
                    print("data: %s, alg: %s, k: %g" % (data, names[i], k))
                    with timeout(seconds=200):
                        s = time.perf_counter()
                        alg("%s/%s.txt" % (data, pos_files[j]), "%s/%s.txt" % (data, neg_files[j]), k, False)
                        e = time.perf_counter()
                    times[data][names[i]].append(e-s)
                    k *= 2
                except TimeoutError as e:
                    print(e)
                    break

    pickle.dump(times, open("../report/data/times_closed_wracc.p", "wb"))


    import closed_abswracc.CloSpan_abswracc_heap as cs_heap
    import closed_abswracc.CloSpan_abswracc_sorted_list as cs_sl
    algs = [file.main for file in [cs_heap, cs_sl]]
    names = ['CloSpan_heap', 'CloSpan_sorted_list']
    datasets = ['Protein', 'Reuters']
    pos_files = ['SRC1521', 'earn']
    neg_files = ['PKA_group15', 'acq']

    times = {}
    for data in datasets:
        times[data] = {}
        for alg in names:
            times[data][alg] = []

    for j, data in enumerate(datasets):
        for i in range(len(algs)):
            print()
            alg = algs[i]
            k = 1
            while True:
                try:
                    print("data: %s, alg: %s, k: %g" % (data, names[i], k))
                    with timeout(seconds=200):
                        s = time.perf_counter()
                        alg("%s/%s.txt" % (data, pos_files[j]), "%s/%s.txt" % (data, neg_files[j]), k, False)
                        e = time.perf_counter()
                    times[data][names[i]].append(e-s)
                    k *= 2
                except TimeoutError as e:
                    print(e)
                    break

    pickle.dump(times, open("../report/data/times_closed_abswracc.p", "wb"))


    import closed_infogain.CloSpan_infogain_heap as cs_heap
    import closed_infogain.CloSpan_infogain_sorted_list as cs_sl
    algs = [file.main for file in [cs_heap, cs_sl]]
    names = ['CloSpan_heap', 'CloSpan_sorted_list']
    datasets = ['Protein', 'Reuters']
    pos_files = ['SRC1521', 'earn']
    neg_files = ['PKA_group15', 'acq']

    times = {}
    for data in datasets:
        times[data] = {}
        for alg in names:
            times[data][alg] = []

    for j, data in enumerate(datasets):
        for i in range(len(algs)):
            print()
            alg = algs[i]
            k = 1
            while True:
                try:
                    print("data: %s, alg: %s, k: %g" % (data, names[i], k))
                    with timeout(seconds=200):
                        s = time.perf_counter()
                        alg("%s/%s.txt" % (data, pos_files[j]), "%s/%s.txt" % (data, neg_files[j]), k, False)
                        e = time.perf_counter()
                    times[data][names[i]].append(e-s)
                    k *= 2
                except TimeoutError as e:
                    print(e)
                    break

    pickle.dump(times, open("../report/data/times_closed_infogain.p", "wb"))


