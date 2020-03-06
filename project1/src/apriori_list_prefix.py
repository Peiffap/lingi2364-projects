#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def apriori(filepath, minFrequency):
    """Runs the apriori algorithm on the specified file with the given minimum frequency.

        This version has:
            - intelligent candidate generation using prefixes (implemented using lists);
            - frequency computation using traversal, but with precounting for singletons;
            - no additional anti-monotonicity pruning."""

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

    singleton_support = [0] * (items + 1)
    for t in range(len(transactions_set)):
        for i in transactions_set[t]:
            singleton_support[i] += 1

    minSupport = minFrequency * trans
    def frequency(itemset):
        """Returns the frequency of the given itemset for the current list of transactions"""
        # length of the list of transactions where itemset is a subset divided by total number of transactions
        # uses a bit of cpython magic to make it faster
        return len(list(filter(itemset.issubset, transactions_set)))/trans

    F = [] # frequent sets
    for i in range(items):
        supp = singleton_support[i + 1]
        if supp >= minSupport:
            F += [[i+1]]
            print("%s  (%g)" % ([i+1], supp/trans)) # print frequent singleton sets
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
                    freq = frequency(set(newl))
                    if freq >= minFrequency:
                        F += [newl]
                        print("%s  (%g)" % (newl, freq)) # print frequent sets
                else: # prefix will never be the same again, we can skip
                    break
            cnt += 1