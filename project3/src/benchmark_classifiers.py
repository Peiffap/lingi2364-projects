#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Benchmark classifier performance.
"""

import pickle
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn import svm
from sklearn import neighbors
from sklearn import neural_network

plt.style.use("ggplot")


def bmark(cl, names):
    values = list(range(2, 11))

    accuracy = {name: {i: {} for i in values} for name in names}

    accuracy['seqcover'] = {i: {} for i in values}

    k = 64
    minsup = 1000

    for nfolds in values:
        acc = p4.benchmark("molecules.pos", "molecules.neg", nfolds, minsup, k,
                           cl)
        for i, name in enumerate(names):
            accuracy[name][nfolds]['test'] = [
                acc['test'][j][i] for j in range(nfolds)
            ]
            accuracy[name][nfolds]['train'] = [
                acc['train'][j][i] for j in range(nfolds)
            ]

        acc = p3.benchmark("molecules.pos", "molecules.neg", nfolds, minsup, k)
        accuracy['seqcover'][nfolds]['test'] = acc['test']
        accuracy['seqcover'][nfolds]['train'] = acc['train']

    pickle.dump(accuracy, open("../report/data/classifier_performance.p",
                               "wb"))


if __name__ == "__main__":
    import phase4 as p4
    import phase3 as p3

    cl = [
        tree.DecisionTreeClassifier(),
        svm.LinearSVC(),
        neighbors.KNeighborsClassifier(),
        neural_network.MLPClassifier()
    ]

    names = ["dt", "svm", "knn", "mlp"]

    bmark(cl, names)
