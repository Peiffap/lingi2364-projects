#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Benchmarks for the various frequent pattern mining algorithms.
"""
from timeout import timeout
import pickle

import tracemalloc
from queue import Queue, Empty
from resource import getrusage, RUSAGE_SELF
from threading import Thread
from time import sleep

def memory_monitor(command_queue: Queue, d, poll_interval=1):
    tracemalloc.start()
    old_max = 0
    snapshot = None
    while True:
        try:
            command_queue.get(timeout=poll_interval)
            if snapshot is not None:
                snapshot = snapshot.filter_traces((
                    tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
                    tracemalloc.Filter(False, "<unknown>"),
                ))
                top_stats = snapshot.statistics('lineno')
                total = sum(stat.size for stat in top_stats)
                d.append(total / 1024) # KiB

            return
        except Empty:
            max_rss = getrusage(RUSAGE_SELF).ru_maxrss
            if max_rss > old_max:
                old_max = max_rss
                snapshot = tracemalloc.take_snapshot()

import matplotlib.pyplot as plt

plt.style.use("ggplot")

def aux(algs, names, file):

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
                    with timeout(seconds=200):
                        queue = Queue()
                        poll_interval = 0.01
                        monitor_thread = Thread(target=memory_monitor, args=(queue, sizes[data][names[i]], poll_interval))
                        monitor_thread.start()
                        try:
                            sleep(2) # Start up time.
                            alg("%s/%s.txt" % (data, pos_files[j]), "%s/%s.txt" % (data, neg_files[j]), k, False)
                            sleep(3) # Shut down time.
                        finally:
                            queue.put('stop')
                            monitor_thread.join()
                    k *= 2
                except (TimeoutError, RecursionError) as e:
                    print(e)
                    break

    pickle.dump(sizes, open("../report/data/sizes_%s.p" % (file), "wb"))

if __name__ == "__main__":
    import sumsup.PrefixSpan_sumsup_heap as ps_heap
    import sumsup.PrefixSpan_sumsup_sorted_list as ps_sl
    import sumsup.SPADE as spade
    algs = [file.main for file in [ps_heap, ps_sl, spade]]
    names = ['PrefixSpan_heap', 'PrefixSpan_sorted_list', 'SPADE']
    aux(algs, names, 'sumsup')

    import wracc.PrefixSpan_wracc_heap as ps_heap
    import wracc.PrefixSpan_wracc_sorted_list as ps_sl
    algs = [file.main for file in [ps_heap, ps_sl]]
    names = ['PrefixSpan_heap', 'PrefixSpan_sorted_list']
    aux(algs, names, 'wracc')

    import closed_wracc.CloSpan_wracc_heap as cs_heap
    import closed_wracc.CloSpan_wracc_sorted_list as cs_sl
    algs = [file.main for file in [cs_heap, cs_sl]]
    names = ['CloSpan_heap', 'CloSpan_sorted_list']
    aux(algs, names, 'closed_wracc')

    import closed_abswracc.CloSpan_abswracc_heap as cs_heap
    import closed_abswracc.CloSpan_abswracc_sorted_list as cs_sl
    algs = [file.main for file in [cs_heap, cs_sl]]
    names = ['CloSpan_heap', 'CloSpan_sorted_list']
    aux(algs, names, 'closed_abswracc')

    import closed_infogain.CloSpan_infogain_heap as cs_heap
    import closed_infogain.CloSpan_infogain_sorted_list as cs_sl
    algs = [file.main for file in [cs_heap, cs_sl]]
    names = ['CloSpan_heap', 'CloSpan_sorted_list']
    aux(algs, names, 'closed_infogain')