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
from collections import defaultdict, deque

def apriori_naive(filepath, minFrequency):
    """Runs the apriori algorithm on the specified file with the given minimum frequency
       This function implements the naive version of the algorithm"""
    import itertools
    comb = itertools.combinations
    transactions_set = list()
    items = 0

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
        return len(list(filter(itemset.issubset, transactions_set)))/trans

    level = 1
    F = [[[]]] # frequent sets
    while F[level-1] != []:
        F.append([])
        Clist = [list(i) for i in comb(range(1, items + 1), level)] # list of subsets of items of size level
        for C in Clist:
            subsets = [list(i) for i in comb(C, len(C) - 1)] # subsets of C with one element removed
            allIn = True # flag variable; are all subsets frequent?
            for s in subsets:
                if s not in F[level-1] and s != (): # if some subset is not frequent, C is not a candidate
                    allIn = False
                    break
            freq = frequency(set(C))
            if allIn and freq >= minFrequency and C != []:
                F[level].append(C) # append frequent itemsets
                print("%s  (%g)" % (C, freq)) # print frequent itemsets
        level += 1

def apriori(filepath, minFrequency):
    """Runs the improved apriori algorithm on the specified file with the given minimum frequency
       This function implements an improved version of the algorithm using prefixes,
       and uses a different membership detection algorithm"""

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

    F = [] # frequent sets
    for i in range(items):
        supp = len(singleton_projection[i + 1])
        if supp >= minSupport:
            F += [[i+1]]
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
                    supp = support(tuple(newl))
                    if supp >= minSupport:
                        F += [newl]
                        print("%s  (%g)" % (newl, supp/trans)) # print frequent sets
                else: # prefix will never be the same again, we can skip
                    break
            cnt += 1

def alternative_miner(filepath, minFrequency):
    """Runs the alternative frequent itemset mining algorithm on the specified file with the given minimum frequency
       This function implements a DFS algorithm"""
    def support(itemset):
        """Returns the support of the given itemset for the current list of transactions"""
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

    myStack = deque()
    freq_list = []
    for i in range(items, 0, -1):
        if len(singleton_projection[i]) >= minSupport:
               myStack.append([i])
               freq_list.append(i)

    def add(stack, itemset):
        """Generate candidates to put on the stack"""
        def ge(x):
            return x > itemset[-1]
        for i in filter(ge, freq_list):
            s = itemset + [i]
            supp = support(tuple(s))
            if supp >= minSupport:
                stack.append(s)

    while not len(myStack) == 0:
        e = myStack.pop()
        if len(e) == 1:
                print("%s  (%g)" % (e, len(singleton_projection[e[0]])/trans))
                add(myStack, e)
        else:
            print("%s  (%g)" % (e, len(member[hash(tuple(e))])/trans))
            add(myStack, e)

    print(minSupport)

if __name__== "__main__":
    s = time.perf_counter()
    alternative_miner("../statement/Datasets/accidents.dat", 0.8)
    t = time.perf_counter()
    print(t - s)
    print()
    s = time.perf_counter()
    #apriori("../statement/Datasets/retail.dat", 0.01)
    t = time.perf_counter()
    print(t - s)
    print()
    s = time.perf_counter()
    #alternative_miner("../statement/Datasets/chess.dat", 0.9)
    t = time.perf_counter()
    print(t - s)

    # cProfile.run('alternative_miner("../statement/Datasets/chess.dat", 0.9)')