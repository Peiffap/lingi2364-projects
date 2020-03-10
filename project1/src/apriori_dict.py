#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import defaultdict
import cProfile
import time

def apriori(filepath, minFrequency, verbose=True):
    """Runs the apriori algorithm on the specified file with the given minimum frequency.

        This version has:
            - intelligent candidate generation using prefixes (implemented using lists);
            - frequency computation using a dictionary;
            - no additional anti-monotonicity pruning."""

    ngen = 0
    nsupp = 0
    nfreq = 0

    # read data; this is heavily inspired from the provided template
    lines = list(filter(None, open(filepath, "r").read().splitlines()))
    trans = len(lines) # number of transactions
    singleton_projection = defaultdict(set)
    for l in range(trans):
        transaction = list(map(int, lines[l].rstrip().split(" ")))
        for i in transaction:
            singleton_projection[i].add(l) # store the transactions l in which item i appears

    items = max(singleton_projection) # number of items is maximum dict index

    member = defaultdict(set)

    minSupport = trans * minFrequency
    if not minSupport == int(minSupport):
        minSupport = int(minSupport) + 1

    def support(itemset):
        """Returns the support of the given itemset for the current list of transactions"""
        # compute the intersection of the prefix' support and the last item's
        if len(itemset) == 2: # if length is two, need to use singleton_projection
            tmp = singleton_projection[itemset[0]] & singleton_projection[itemset[1]]
            l = len(tmp)
            if l >= minSupport: # only frequent itemsets will be used as prefixes
                member[tuple(itemset)] = tmp
                return l
            return 0
        else:
            tmp = member[tuple(itemset[:-1])] & singleton_projection[itemset[-1]]
            l = len(tmp)
            if l >= minSupport:
                member[tuple(itemset)] = tmp
                return l
            return 0

    F = [] # frequent sets
    for i in range(items):
        supp = len(singleton_projection[i + 1])
        nsupp += 1
        ngen += 1
        if supp >= minSupport:
            F += [[i+1]]
            if verbose:
                nfreq += 1
                print("[%i]  (%g)" % (i+1, supp/trans)) # print frequent singleton sets
    while F != []:
        # list of subsets of items of size level
        l = F[:] # deep copy the list
        F = []
        cnt = 1
        for l1 in l[:-1]:
            l11 = l1[:-1] # take prefix
            for l2 in l[cnt:]:
                if l11 == l2[:-1]: # if the sets share a common prefix
                    newl = l1 + [l2[-1]] # new candidate based on sets sharing prefixes
                    supp = support(newl)
                    ngen += 1
                    nsupp += 1
                    if supp >= minSupport:
                        F += [newl]
                        if verbose:
                            nfreq += 1
                            print("%s  (%g)" % (newl, supp/trans)) # print frequent sets
                else: # prefix will never be the same again, we can skip
                    break
            cnt += 1

    if verbose:
        print(ngen)
        print(nsupp)
        print(nfreq)

if __name__ == "__main__":
    """
    ti = 0
    for i in range(10):
        s = time.perf_counter()
        apriori("../statement/Datasets/accidents.dat", 0.9, verbose=False)
        ti += time.perf_counter() - s
    print(ti/10)
    """
    apriori('../statement/Datasets/mushroom.dat', 0.2, verbose=True)