#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import deque, defaultdict

def dfs(filepath, minFrequency, verbose=True):
    """Runs the alternative frequent itemset mining algorithm on the specified file with the given minimum frequency
       This function implements a DFS algorithm"""
    def support(itemset):
        """Returns the support of the given itemset for the current list of transactions"""
        nsupp[0] += 1
        # compute the intersection of the prefix' support and the last item's
        if len(itemset) == 2: # if length is two, need to use singleton_projection
            tmp = singleton_projection[itemset[0]] & singleton_projection[itemset[1]]
            l = len(tmp)
            if l >= minSupport: # only frequent itemsets will be used as prefixes
                member[hash(itemset)] = tmp
                return l
            return 0
        else:
            tmp = member[hash(itemset[:-1])] & singleton_projection[itemset[-1]]
            l = len(tmp)
            if l >= minSupport:
                member[hash(itemset)] = tmp
                return l
            return 0

    def add(stack, set, limit):
        length = len(set)-1
        for i in range(limit, set[length], -1):
            s = set[:]
            ngen[0] += 1
            s.append(i)
            supp = support(tuple(s))
            if(supp >= minSupport):
                stack.append(s)

    ngen = [0]
    nsupp = [0]
    nfreq = [0]

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

    myStack = deque()
    for i in range(items,0,-1):
        ngen[0] += 1
        nsupp[0] += 1
        supp = len(singleton_projection[i])
        if supp >= minSupport:
            myStack.append([i])

    while not len(myStack)==0:
        e = myStack.pop()
        if len(e) == 1:
            supp = len(singleton_projection[e[0]])
            if supp >= minSupport:
                if verbose:
                    nfreq[0] += 1
                    print("%s  (%g)" % (e, supp/trans))
                add(myStack, e, items)
        else:
            supp = support(tuple(e))
            nsupp[0] -= 1
            if supp >= minSupport:
                if verbose:
                    nfreq[0] += 1
                    print("%s  (%g)" % (e, supp/trans))
                add(myStack, e, items)

    if verbose:
        print(ngen[0])
        print(nsupp[0])
        print(nfreq[0])

if __name__ == "__main__":
    """
    ti = 0
    for i in range(10):
        s = time.perf_counter()
        dfs("../statement/Datasets/accidents.dat", 0.9, verbose=False)
        ti += time.perf_counter() - s
    print(ti/10)
    """
    dfs('../statement/Datasets/chess.dat', 0.98, verbose=True)