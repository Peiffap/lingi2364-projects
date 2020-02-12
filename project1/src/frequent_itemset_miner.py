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


class Dataset:
    """Utility class to manage a dataset stored in a external file."""

    def __init__(self, filepath):
        """reads the dataset file and initializes files"""
        self.transactions_set = list()
        self.items = 0
        self.trans = 0

        try:
            lines = [line.strip() for line in open(filepath, "r")]
            lines = [line for line in lines if line]  # Skipping blank lines
            self.trans = len(lines)
            for line in lines:
                transaction = set(map(int, line.split(" ")))
                self.transactions_set.append(transaction)
            self.items = max([max(i) for i in self.transactions_set])
        except IOError as e:
            print("Unable to read dataset file!\n" + e)

    def trans_num(self):
        """Returns the number of transactions in the dataset"""
        return self.trans

    def items_num(self):
        """Returns the number of different items in the dataset"""
        return self.items

    def get_transaction_set(self, i):
        """Returns the transaction at index i as a set"""
        return self.transactions_set[i]

    def covers(self, i, itemset):
        """Returns whether the given itemset covers transaction i"""
        return itemset.issubset(self.get_transaction_set(i))

    def support(self, itemset):
        """Returns the support of the given itemset for the current list of transactions"""
        return sum([1 for i in range(self.trans_num()) if self.covers(i, itemset)])

    def frequency(self, itemset):
        """Returns the frequency of the given itemset for the current list of transactions"""
        return self.support(itemset)/self.trans_num()


def apriori_naive(filepath, minFrequency):
    """Runs the apriori algorithm on the specified file with the given minimum frequency
       This function implements the naive version of the algorithm"""
    import itertools
    data = Dataset(filepath) # read data
    minSupport = minFrequency * data.trans_num() # compute minimal support

    level = 1
    F = [[[]]] # frequent sets
    while True:
        F.append([])
        # list of subsets of items of size level
        Clist = [i for i in itertools.combinations(range(1, data.items_num() + 1), level)]
        for C in Clist:
            subsets = [i for i in itertools.combinations(C, len(C) - 1)]
            # subsets of C with one element removed
            allIn = True
            for s in subsets:
                if s not in F[level-1] and s != ():
                    # if some subset is not frequent, C is not a candidate
                    allIn = False
                    break
            if allIn and data.support(set(C)) >= minSupport:
                # append frequent itemsets
                F[level].append(C)
        if len(F[level]) != 0:
            for s in F[level]:
                if s != []:
                    print(list(s), " ({:g})".format(data.frequency(set(s)))) # print frequent sets
        else:
            break

        level += 1

def apriori(filepath, minFrequency):
    """Runs the improved apriori algorithm on the specified file with the given minimum frequency
       This function implements an improved version of the algorithm"""
    data = Dataset(filepath) # read data

    def generate_candidates(l):
        """Return list of candidate sets obtained by prefix matching on previous frequent sets"""
        candidates = []
        for i in range(len(l)):
            l1 = l[i]
            prev = -1
            for j in range(i+1, len(l)):
                l2 = l[j]
                if l2[-1] <= prev: # if prev is not negative, the prefix must've gone too high -> skip remaining l2's
                    break
                if l1[:-1] == l2[:-1]: # if the sets share a common prefix
                    candidates.append(l1 + [l2[-1]])
                    prev = l2[-1]
        return candidates


    F = [] # frequent sets
    freq = list(map(data.frequency, [set([i]) for i in range(1, data.items_num() + 1)]))
    for i in range(0, len(freq)):
        if freq[i] >= minFrequency:
            F.append([i + 1])
            print("%s  (%g)" % ([i+1], freq[i])) # print frequent sets
    while F != []:
        # list of subsets of items of size level
        Clist = generate_candidates(F)
        F = []
        freq = list(map(data.frequency, [set(C) for C in Clist]))
        for i in range(len(freq)):
            if freq[i] >= minFrequency:
                # append frequent itemsets
                F.append(Clist[i])
                print("%s  (%g)" % (Clist[i], freq[i]))

def alternative_miner(filepath, minFrequency):
    """Runs the alternative frequent itemset mining algorithm on the specified file with the given minimum frequency
       This function implements the ECLAT algorithm"""
    # TODO
    apriori(filepath, minFrequency)

if __name__== "__main__":
    s = time.perf_counter()
    #apriori_naive("../statement/Datasets/toy.dat", 0.125)
    t = time.perf_counter()
    print(t - s)
    print()
    s = time.perf_counter()
    apriori("../statement/Datasets/chess.dat", 0.9)
    t = time.perf_counter()
    print(t - s)
    print()
    s = time.perf_counter()
    #alternative_miner("../statement/Datasets/chess.dat", 0.9)
    t = time.perf_counter()
    print(t - s)
