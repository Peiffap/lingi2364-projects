#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import pickle
import matplotlib.pyplot as plt
import tikzplotlib  # pip install tikzplotlib

import seaborn as sns

plt.style.use("ggplot")


def plt_acc_topk():
    accuracy = pickle.load(open("../report/data/acc_topk.p", "rb"))

    keys = list(accuracy.keys())

    test = []
    testerr = []
    train = []
    trainerr = []
    for k in keys:
        test.append(np.array(accuracy[k]['test']).mean() * 100)
        testerr.append(np.array(accuracy[k]['test']).std() * 100)

        train.append(np.array(accuracy[k]['train']).mean() * 100)
        trainerr.append(np.array(accuracy[k]['train']).std() * 100)

    clrs = sns.color_palette("husl", 2)

    plt.figure()
    plt.semilogx(keys, test, c=clrs[0])
    plt.fill_between(keys, [i - j for i, j in zip(test, testerr)],
                     [i + j for i, j in zip(test, testerr)],
                     alpha=0.3,
                     facecolor=clrs[0])

    plt.semilogx(keys, train, c=clrs[1])
    plt.fill_between(keys, [i - j for i, j in zip(train, trainerr)],
                     [i + j for i, j in zip(train, trainerr)],
                     alpha=0.3,
                     facecolor=clrs[1])

    plt.xlabel("\\(k\\)")
    plt.ylabel("Prediction accuracy (\\si{\percent})")
    plt.legend(["Test set", "Training set"])

    tikzplotlib.save("../report/plots/acc_topk.tikz", axis_width="\\linewidth")


def plt_acc_classifiers():
    accuracy = pickle.load(
        open("../report/data/classifier_performance.p", "rb"))

    names = accuracy.keys()

    values = list(range(2, 11))

    sizes = [(n - 1) * 100 / n for n in values]

    clrs = sns.color_palette("husl", 2)

    for i, name in enumerate(names):
        test = []
        testerr = []
        train = []
        trainerr = []
        for nf in values:
            test.append(np.array(accuracy[name][nf]['test']).mean() * 100)
            testerr.append(np.array(accuracy[name][nf]['test']).std() * 100)

            train.append(np.array(accuracy[name][nf]['train']).mean() * 100)
            trainerr.append(np.array(accuracy[name][nf]['train']).std() * 100)

        plt.figure()

        plt.plot(sizes, test, c=clrs[0])
        plt.fill_between(sizes, [i - j for i, j in zip(test, testerr)],
                         [i + j for i, j in zip(test, testerr)],
                         alpha=0.3,
                         facecolor=clrs[0])

        plt.plot(sizes, train, c=clrs[1])
        plt.fill_between(sizes, [i - j for i, j in zip(train, trainerr)],
                         [i + j for i, j in zip(train, trainerr)],
                         alpha=0.3,
                         facecolor=clrs[1])

        plt.xlabel("Training set size (\\si{\\percent} of total)")
        plt.legend(["Test", "Train"])
        plt.ylabel("Prediction accuracy (\\si{\percent})")

        tikzplotlib.save("../report/plots/%s_performance.tikz" % name,
                         axis_width="\\linewidth")


if __name__ == "__main__":
    #plt_acc_topk()
    plt_acc_classifiers()
