#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def apriori(filepath, minFrequency, verbose=True):
    """Runs the apriori algorithm on the specified file with the given minimum frequency.

        This version has:
            - intelligent candidate generation using prefixes (implemented using lists);
            - frequency computation using union of singleton database projections,
              with break if minsup cannot be reached;
            - no additional anti-monotonicity pruning."""

    ngen = 0
    nsupp = 0
    nfreq = 0

    # read data; this is heavily inspired from the provided template
    transactions_set = list()
    lines = filter(None, open(filepath, "r").read().splitlines())
    app = transactions_set.append
    items = 0
    for line in lines:
        transaction = list(map(int, line.rstrip().split(" ")))
        items = max(items, transaction[-1]) # transactions are sorted, find number of items
        app(set(transaction))
    trans = len(transactions_set) # number of transactions

    member = [set() for i in range(items+1)]
    for t in range(len(transactions_set)):
        for i in transactions_set[t]:
            member[i].add(t) # store the transactions t in which item i appears


    minSupport = trans * minFrequency
    if not minSupport == int(minSupport):
        minSupport = int(minSupport) + 1
    def frequency(itemset):
        """Returns the frequency of the given itemset for the current list of transactions"""
        # compute the intersection of all member[i] where i in itemset
        # this intersection contains all the transactions covered by itemset
        s = member[itemset[0]]
        if len(itemset) > 1:
            for i in itemset[1:]:
                s = s & member[i]
                if len(s) < minSupport:
                    return 0
        return len(s)/trans

    F = [] # frequent sets
    for i in range(items):
        nsupp += 1
        ngen += 1
        freq = frequency([i + 1])
        if freq >= minFrequency:
            F += [[i+1]]
            if verbose:
                nfreq += 1
                print("%s  (%g)" % ([i+1], freq)) # print frequent singleton sets
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
                    freq = frequency(newl)
                    nsupp += 1
                    ngen += 1
                    if freq >= minFrequency:
                        F += [newl]
                        if verbose:
                            nfreq += 1
                            print("%s  (%g)" % (newl, freq)) # print frequent sets
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
    apriori('../statement/Datasets/chess.dat', 0.99, verbose=True)