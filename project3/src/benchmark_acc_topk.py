#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Benchmark effect of setting a top k for graph mining on accuracy of model.
"""

from timeout import timeout
import pickle
import matplotlib.pyplot as plt

plt.style.use("ggplot")


def bmark(alg):
    accuracy = {}

    k = 1
    while k < 10_000:
        try:
            print("k: %g" % (k))
            with timeout(seconds=200):
                acc = alg("molecules.pos", "molecules.neg", 5, 300, k)
            accuracy[k] = acc
            k *= 2
        except (TimeoutError, RecursionError) as e:
            print(e)
            break

    pickle.dump(accuracy, open("../report/data/acc_topk.p", "wb"))


if __name__ == "__main__":
    import phase2 as p2
    bmark(p2.benchmark)
