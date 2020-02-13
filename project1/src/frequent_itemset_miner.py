"""
Skeleton file for the project 1 of the LINGI2364 course.
Use this as your submission file. Every piece of code that is used in your program should be put inside this file.

This file given to you as a skeleton for your implementation of the Apriori and Depth
First Search algorithms. You are not obligated to use them and are free to write any class or method as long as the
following requirements are respected:

Your apriori and alternativeMiner methods must take as parameters a string corresponding to the path to a valid
dataset file and a double corresponding to the minimum frequency.
You must write on the standard output (use the print() method) all the itemsets that are frequent in the dataset file
according to the minimum frequency given. Each itemset has to be printed on one line following the format:
[<item 1>, <item 2>, ... <item k>] (<frequency>).
Tip: you can use Arrays.toString(int[] a) to print an itemset.

The items in an itemset must be printed in lexicographical order. However, the itemsets themselves can be printed in
any order.

Do not change the signature of the apriori and alternative_miner methods as they will be called by the test script.

__authors__ = Group 13, Gilles Peiffer & Liliya Semerikova
"""
import time
import cProfile
import numpy as np

def apriori_naive(filepath, minFrequency):
    """Runs the apriori algorithm on the specified file with the given minimum frequency
       This function implements the naive version of the algorithm

       WARNING: TO FIX"""
    import itertools
    comb = itertools.combinations
    transactions_set = list()

    lines = filter(None, open(filepath, "r").read().splitlines())
    app = transactions_set.append
    for line in lines:
        transaction = list(map(int, line.rstrip().split(" ")))
        app(set(transaction))
    trans = len(transactions_set)
    items = max(max(t) for t in transactions_set)

    def frequency(itemset):
        """Returns the frequency of the given itemset for the current list of transactions"""
        return len(list(filter(itemset.issubset, transactions_set)))/trans

    level = 1
    F = [[[]]] # frequent sets
    while F[level-1] != []:
        F.append([])
        # list of subsets of items of size level
        Clist = [list(i) for i in comb(range(1, items + 1), level)]
        for C in Clist:
            subsets = [list(i) for i in comb(C, len(C) - 1)]
            # subsets of C with one element removed
            allIn = True
            for s in subsets:
                if s not in F[level-1] and s != ():
                    # if some subset is not frequent, C is not a candidate
                    allIn = False
                    break
            freq = frequency(set(C))
            if allIn and freq >= minFrequency:
                # append frequent itemsets
                F[level].append(C)
                if C != []:
                    print("%s  (%g)" % (C, freq))
        level += 1

def apriori(filepath, minFrequency):
    """Runs the improved apriori algorithm on the specified file with the given minimum frequency
       This function implements an improved version of the algorithm, and uses a different membership detection"""
    transactions_set = list()
    lines = filter(None, open(filepath, "r").read().splitlines())
    app = transactions_set.append
    items = 0
    for line in lines:
        transaction = list(map(int, line.rstrip().split(" ")))
        items = max(items, transaction[-1])
        app(set(transaction))
    trans = len(transactions_set)

    member = [set() for i in range(items+1)]
    for t in range(len(transactions_set)):
        for i in transactions_set[t]:
            member[i].add(t)

    def frequency(itemset):
        """Returns the frequency of the given itemset for the current list of transactions"""
        s = member[itemset[0]]
        if len(itemset) > 1:
            for i in itemset[1:]:
                s = s & member[i]
                if len(s) < trans * minFrequency:
                    return 0
        return len(s)/trans

    F = [] # frequent sets
    for i in range(items):
        freq = frequency([i + 1])
        if freq >= minFrequency:
            F += [[i+1]]
            print("%s  (%g)" % ([i+1], freq)) # print frequent sets
    while F != []:
        # list of subsets of items of size level
        l = F[:] # copy the list
        F = []
        cnt = 1
        for l1 in l[:-1]:
            l11 = l1[:-1]
            for l2 in l[cnt:]:
                if l11 == l2[:-1]: # if the sets share a common prefix
                    newl = l1 + [l2[-1]]
                    freq = frequency(newl)
                    if freq >= minFrequency:
                        F += [newl]
                        print("%s  (%g)" % (newl, freq))
                else: # prefix will never be the same again, we can skip
                    break
            cnt += 1

def alternative_miner(filepath, minFrequency):
    """Runs the alternative frequent itemset mining algorithm on the specified file with the given minimum frequency
       This function implements the ECLAT algorithm"""
    # TODO
    print("TODO")

if __name__== "__main__":
    s = time.perf_counter()
    apriori_naive("../statement/Datasets/chess.dat", 0.9)
    t = time.perf_counter()
    print(t - s)
    print()
    s = time.perf_counter()
    #apriori("../statement/Datasets/accidents.dat", 0.8)
    t = time.perf_counter()
    print(t - s)
    print()
    s = time.perf_counter()
    #alternative_miner("../statement/Datasets/chess.dat", 0.9)
    t = time.perf_counter()
    print(t - s)

    #cProfile.run('apriori("../statement/Datasets/chess.dat", 0.9)')
