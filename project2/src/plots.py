#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pickle
import matplotlib.pyplot as plt
import tikzplotlib # pip install tikzplotlib

plt.style.use("ggplot")

def plt_time():
    def plt_time_aux(names, file):
        datasets = ['Protein', 'Reuters']

        times = pickle.load(open("../report/data/times_%s.p" % (file), "rb"))

        dataset_k = {}
        for data in datasets:
            dataset_k[data] = {}
            for alg in names:
                dataset_k[data][alg] = [2**k for k in range(len(times[data][alg]))]

        for data in datasets:
            fig, ax = plt.subplots()
            for alg in names:
                ax.semilogy(dataset_k[data][alg], times[data][alg], marker="x")
            ax.set_xlabel("\\(k\\)")
            ax.set_ylabel("Execution time [\\si{\\second}]")
            plt.legend(["\\py{%s}" % (name) for name in names])
            ax.plot()

            tikzplotlib.save("../report/plots/time_%s_%s.tikz" % (file, data), axis_width="\\linewidth")

    names_list = [['PrefixSpan_heap', 'PrefixSpan_sorted_list', 'SPADE'],
                  ['PrefixSpan_heap', 'PrefixSpan_sorted_list'],
                  ['CloSpan_heap', 'CloSpan_sorted_list'],
                  ['CloSpan_heap', 'CloSpan_sorted_list'],
                  ['CloSpan_heap', 'CloSpan_sorted_list']]

    file_list = ['sumsup', 'wracc', 'closed_wracc', 'closed_abswracc', 'closed_infogain']

    for names, file in zip(names_list, file_list):
        plt_time_aux(names, file)


def plt_size():
    def plt_size_aux(names, file):
        datasets = ['Protein', 'Reuters']

        sizes = pickle.load(open("../report/data/sizes_%s.p" % (file), "rb"))

        dataset_k = {}
        for data in datasets:
            dataset_k[data] = {}
            for alg in names:
                dataset_k[data][alg] = [2**k for k in range(len(sizes[data][alg]))]

        for data in datasets:
            fig, ax = plt.subplots()
            for alg in names:
                ax.semilogy(dataset_k[data][alg], sizes[data][alg], marker="x")
            ax.set_xlabel("\\(k\\)")
            ax.set_ylabel("Maximal memory usage [\\si{\\kibi\\byte}]")
            plt.legend(["\\py{%s}" % (name) for name in names])
            ax.plot()

            tikzplotlib.save("../report/plots/size_%s_%s.tikz" % (file, data), axis_width="\\linewidth")

    names_list = [['PrefixSpan_heap', 'PrefixSpan_sorted_list', 'SPADE'],
                  ['PrefixSpan_heap', 'PrefixSpan_sorted_list'],
                  ['CloSpan_heap', 'CloSpan_sorted_list'],
                  ['CloSpan_heap', 'CloSpan_sorted_list'],
                  ['CloSpan_heap', 'CloSpan_sorted_list']]

    file_list = ['sumsup', 'wracc', 'closed_wracc', 'closed_abswracc', 'closed_infogain']

    for names, file in zip(names_list, file_list):
        plt_size_aux(names, file)

if __name__ == "__main__":
    #plt_time()
    plt_size()
