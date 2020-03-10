#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pickle
import matplotlib.pyplot as plt
import tikzplotlib # pip install tikzplotlib

plt.style.use("ggplot")

def plt_time():
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

    trans = {}
    dataset_supports = {}
    for data in datasets:
        lines = list(filter(None, open("../statement/Datasets/%s.dat" % (data), "r").read().splitlines()))
        trans[data] = len(lines)
        dataset_supports[data] = [0 for freq in dataset_freqs[data]]
        for i in range(len(dataset_freqs[data])):
            dataset_supports[data][i] = dataset_freqs[data][i] * trans[data]

    times = pickle.load(open("../report/data/times.p", "rb"))

    for data in datasets:
        fig, ax = plt.subplots()
        secax = ax.twiny()
        secax.set_xlabel('Minimum frequency threshold')
        for alg in names:
            secax.semilogy(dataset_freqs[data][:len(times[data][alg])], times[data][alg], marker="x")
        ax.set_xlim(min(ax.get_xlim()) * trans[data], max(ax.get_xlim()) * trans[data])
        secax.invert_xaxis()
        ax.set_xlabel("Minimum support threshold")
        ax.set_ylabel("Execution time [\\si{\\second}]")
        ax.invert_xaxis()
        plt.legend(["\\py{%s}" % (name) for name in names])
        ax.plot()

        tikzplotlib.save("../report/plots/time_%s.tikz" % (data), axis_width="\\linewidth")

def plt_size():
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

    trans = {}
    dataset_supports = {}
    for data in datasets:
        lines = list(filter(None, open("../statement/Datasets/%s.dat" % (data), "r").read().splitlines()))
        trans[data] = len(lines)
        dataset_supports[data] = [0 for freq in dataset_freqs[data]]
        for i in range(len(dataset_freqs[data])):
            dataset_supports[data][i] = dataset_freqs[data][i] * trans[data]

    sizes = pickle.load(open("../report/data/sizes.p", "rb"))

    for data in datasets:
        fig, ax = plt.subplots()
        secax = ax.twiny()
        secax.set_xlabel('Minimum frequency threshold')
        for alg in names:
            freqs = []
            s = []
            for i in range(len(sizes[data][alg])):
                if sizes[data][alg][i] > 0:
                    freqs.append(dataset_freqs[data][:len(sizes[data][alg])][i])
                    s.append(sizes[data][alg][i])
            secax.semilogy(freqs, s, marker="x")
        ax.set_xlim(min(ax.get_xlim()) * trans[data], max(ax.get_xlim()) * trans[data])
        secax.invert_xaxis()
        ax.set_xlabel("Minimum support threshold")
        ax.set_ylabel("Memory consumption [\\si{\\kibi\\byte}]")
        ax.invert_xaxis()
        plt.legend(["\\py{%s}" % (name) for name in names])
        ax.plot()

        tikzplotlib.save("../report/plots/size_%s.tikz" % (data), axis_width="\\linewidth")

if __name__ == "__main__":
    #plt_time()
    plt_size()
