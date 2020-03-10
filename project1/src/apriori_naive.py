#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def apriori(filepath, minFrequency, verbose=True):
    """Runs the apriori algorithm on the specified file with the given minimum frequency
       This function implements the naive version of the algorithm"""
    import itertools
    comb = itertools.combinations
    transactions_set = list()
    items = 0

    ngen = [0]
    nsupp = [0]
    nfreq = [0]

    # read data; this is heavily inspired from the provided template
    lines = filter(None, open(filepath, "r").read().splitlines())
    app = transactions_set.append
    for line in lines:
        transaction = list(map(int, line.rstrip().split(" ")))
        items = max(items, transaction[-1]) # transactions are sorted, find number of items
        app(set(transaction))
    trans = len(transactions_set)

    def frequency(itemset):
        """Returns the frequency of the given itemset for the current list of transactions"""
        # length of the list of transactions where itemset is a subset divided by total number of transactions
        # uses a bit of cpython magic to make it faster
        nsupp[0] += 1
        return len(list(filter(itemset.issubset, transactions_set)))/trans

    level = 1
    F = [[[]]] # frequent sets
    while F[level-1] != []:
        F.append([])
        Clist = [list(i) for i in comb(range(1, items + 1), level)] # list of subsets of items of size level
        for C in Clist:
            ngen[0] += 1
            subsets = [list(i) for i in comb(C, len(C) - 1)] # subsets of C with one element removed
            allIn = True # flag variable; are all subsets frequent?
            for s in subsets:
                if s not in F[level-1] and s != (): # if some subset is not frequent, C is not a candidate
                    allIn = False
                    break
            if allIn:
                freq = frequency(set(C))
                if freq >= minFrequency and C != []:
                    F[level].append(C) # append frequent itemsets
                    if verbose:
                        nfreq[0] += 1
                        print("%s  (%g)" % (C, freq)) # print frequent itemsets
        level += 1

    if verbose:
        print(ngen[0])
        print(nsupp[0])
        print(nfreq[0])

if __name__ == "__main__":
    """
    ti = 0
    for i in range(10):
        s = time.perf_counter()
        apriori("../statement/Datasets/accidents.dat", 0.9, verbose=False)
        ti += time.perf_counter() - s
    print(ti/10)
    """
    apriori('../statement/Datasets/chess.dat', 0.98, verbose=True)