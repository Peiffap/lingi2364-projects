#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Benchmarks for the various frequent pattern mining algorithms.
"""
from timeout import timeout
import pickle

import resource
import time

from stoppable_thread import StoppableThread


class MyLibrarySniffingClass(StoppableThread):
    def __init__(self, target_lib_call, pf, nf, k, verbose):
        super(MyLibrarySniffingClass, self).__init__()
        self.target_function = target_lib_call
        self.pf = pf
        self.nf = nf
        self.k = k
        self.verbose = verbose

    def startup(self):
        pass

    def cleanup(self):
        # Overload the cleanup function
        pass

    def mainloop(self):
        # Start the library Call
        self.target_function(self.pf, self.nf, self.k, self.verbose)

        # Kill the thread when complete
        self.stop()

import matplotlib.pyplot as plt

plt.style.use("ggplot")

if __name__ == "__main__":

    memory_usage_refresh = .005 # Seconds

    import sumsup.PrefixSpan_sumsup_heap as ps_heap
    import sumsup.PrefixSpan_sumsup_sorted_list as ps_sl
    import sumsup.SPADE as spade
    algs = [file.main for file in [ps_heap, ps_sl, spade]]
    names = ['PrefixSpan_heap', 'PrefixSpan_sorted_list', 'SPADE']
    datasets = ['Protein', 'Reuters']
    pos_files = ['SRC1521', 'earn']
    neg_files = ['PKA_group15', 'acq']

    sizes = {}
    for data in datasets:
        sizes[data] = {}
        for alg in names:
            sizes[data][alg] = []

    for j, data in enumerate(datasets):
        for i in range(len(algs)):
            print()
            alg = algs[i]
            k = 1
            while True:
                try:
                    print("data: %s, alg: %s, k: %g" % (data, names[i], k))
                    max_memory = 0
                    with timeout(seconds=200):
                        # Lib Testing Code
                        mythread = MyLibrarySniffingClass(alg, "%s/%s.txt" % (data, pos_files[j]), "%s/%s.txt" % (data, neg_files[j]), k, False)
                        mythread.start()

                        start_mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                        delta_mem = 0

                        while(1):
                            time.sleep(memory_usage_refresh)
                            delta_mem = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) - start_mem
                            if delta_mem > max_memory:
                                max_memory = delta_mem

                            # Check to see if the library call is complete
                            if mythread.isShutdown():
                                break
                    sizes[data][names[i]].append(max_memory)
                    k *= 2
                except TimeoutError as e:
                    print(e)
                    break

    pickle.dump(sizes, open("../report/data/sizes_sumsup.p", "wb"))


    import wracc.PrefixSpan_wracc_heap as ps_heap
    import wracc.PrefixSpan_wracc_sorted_list as ps_sl
    algs = [file.main for file in [ps_heap, ps_sl]]
    names = ['PrefixSpan_heap', 'PrefixSpan_sorted_list']
    datasets = ['Protein', 'Reuters']
    pos_files = ['SRC1521', 'earn']
    neg_files = ['PKA_group15', 'acq']

    sizes = {}
    for data in datasets:
        sizes[data] = {}
        for alg in names:
            sizes[data][alg] = []

    for j, data in enumerate(datasets):
        for i in range(len(algs)):
            print()
            alg = algs[i]
            k = 1
            while True:
                try:
                    print("data: %s, alg: %s, k: %g" % (data, names[i], k))
                    max_memory = 0
                    with timeout(seconds=200):
                        # Lib Testing Code
                        mythread = MyLibrarySniffingClass(alg, "%s/%s.txt" % (data, pos_files[j]), "%s/%s.txt" % (data, neg_files[j]), k, False)
                        mythread.start()

                        start_mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                        delta_mem = 0

                        while(1):
                            time.sleep(memory_usage_refresh)
                            delta_mem = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) - start_mem
                            if delta_mem > max_memory:
                                max_memory = delta_mem

                            # Check to see if the library call is complete
                            if mythread.isShutdown():
                                break
                    sizes[data][names[i]].append(max_memory)
                    k *= 2
                except TimeoutError as e:
                    print(e)
                    break

    pickle.dump(sizes, open("../report/data/sizes_wracc.p", "wb"))


    import closed_wracc.CloSpan_wracc_heap as cs_heap
    import closed_wracc.CloSpan_wracc_sorted_list as cs_sl
    algs = [file.main for file in [cs_heap, cs_sl]]
    names = ['CloSpan_heap', 'CloSpan_sorted_list']
    datasets = ['Protein', 'Reuters']
    pos_files = ['SRC1521', 'earn']
    neg_files = ['PKA_group15', 'acq']

    sizes = {}
    for data in datasets:
        sizes[data] = {}
        for alg in names:
            sizes[data][alg] = []

    for j, data in enumerate(datasets):
        for i in range(len(algs)):
            print()
            alg = algs[i]
            k = 1
            while True:
                try:
                    print("data: %s, alg: %s, k: %g" % (data, names[i], k))
                    max_memory = 0
                    with timeout(seconds=200):
                        # Lib Testing Code
                        mythread = MyLibrarySniffingClass(alg, "%s/%s.txt" % (data, pos_files[j]), "%s/%s.txt" % (data, neg_files[j]), k, False)
                        mythread.start()

                        start_mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                        delta_mem = 0

                        while(1):
                            time.sleep(memory_usage_refresh)
                            delta_mem = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) - start_mem
                            if delta_mem > max_memory:
                                max_memory = delta_mem

                            # Check to see if the library call is complete
                            if mythread.isShutdown():
                                break
                    sizes[data][names[i]].append(max_memory)
                    k *= 2
                except TimeoutError as e:
                    print(e)
                    break

    pickle.dump(sizes, open("../report/data/sizes_closed_wracc.p", "wb"))


    import closed_abswracc.CloSpan_abswracc_heap as cs_heap
    import closed_abswracc.CloSpan_abswracc_sorted_list as cs_sl
    algs = [file.main for file in [cs_heap, cs_sl]]
    names = ['CloSpan_heap', 'CloSpan_sorted_list']
    datasets = ['Protein', 'Reuters']
    pos_files = ['SRC1521', 'earn']
    neg_files = ['PKA_group15', 'acq']

    sizes = {}
    for data in datasets:
        sizes[data] = {}
        for alg in names:
            sizes[data][alg] = []

    for j, data in enumerate(datasets):
        for i in range(len(algs)):
            print()
            alg = algs[i]
            k = 1
            while True:
                try:
                    print("data: %s, alg: %s, k: %g" % (data, names[i], k))
                    max_memory = 0
                    with timeout(seconds=200):
                        # Lib Testing Code
                        mythread = MyLibrarySniffingClass(alg, "%s/%s.txt" % (data, pos_files[j]), "%s/%s.txt" % (data, neg_files[j]), k, False)
                        mythread.start()

                        start_mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                        delta_mem = 0

                        while(1):
                            time.sleep(memory_usage_refresh)
                            delta_mem = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) - start_mem
                            if delta_mem > max_memory:
                                max_memory = delta_mem

                            # Check to see if the library call is complete
                            if mythread.isShutdown():
                                break
                    sizes[data][names[i]].append(max_memory)
                    k *= 2
                except TimeoutError as e:
                    print(e)
                    break

    pickle.dump(sizes, open("../report/data/sizes_closed_abswracc.p", "wb"))


    import closed_infogain.CloSpan_infogain_heap as cs_heap
    import closed_infogain.CloSpan_infogain_sorted_list as cs_sl
    algs = [file.main for file in [cs_heap, cs_sl]]
    names = ['CloSpan_heap', 'CloSpan_sorted_list']
    datasets = ['Protein', 'Reuters']
    pos_files = ['SRC1521', 'earn']
    neg_files = ['PKA_group15', 'acq']

    sizes = {}
    for data in datasets:
        sizes[data] = {}
        for alg in names:
            sizes[data][alg] = []

    for j, data in enumerate(datasets):
        for i in range(len(algs)):
            print()
            alg = algs[i]
            k = 1
            while True:
                try:
                    print("data: %s, alg: %s, k: %g" % (data, names[i], k))
                    max_memory = 0
                    with timeout(seconds=200):
                        # Lib Testing Code
                        mythread = MyLibrarySniffingClass(alg, "%s/%s.txt" % (data, pos_files[j]), "%s/%s.txt" % (data, neg_files[j]), k, False)
                        mythread.start()

                        start_mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                        delta_mem = 0

                        while(1):
                            time.sleep(memory_usage_refresh)
                            delta_mem = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) - start_mem
                            if delta_mem > max_memory:
                                max_memory = delta_mem

                            # Check to see if the library call is complete
                            if mythread.isShutdown():
                                break
                    sizes[data][names[i]].append(max_memory)
                    k *= 2
                except TimeoutError as e:
                    print(e)
                    break

    pickle.dump(sizes, open("../report/data/sizes_closed_infogain.p", "wb"))