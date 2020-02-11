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

import itertools


class Dataset:
    """Utility class to manage a dataset stored in a external file."""

    def __init__(self, filepath):
        """reads the dataset file and initializes files"""
        self.transactions = list()
        self.items = set()

        try:
            lines = [line.strip() for line in open(filepath, "r")]
            lines = [line for line in lines if line]  # Skipping blank lines
            for line in lines:
                transaction = list(map(int, line.split(" ")))
                self.transactions.append(transaction)
                for item in transaction:
                    self.items.add(item)
        except IOError as e:
            print("Unable to read dataset file!\n" + e)

    def trans_num(self):
        """Returns the number of transactions in the dataset"""
        return len(self.transactions)

    def items_num(self):
        """Returns the number of different items in the dataset"""
        return len(self.items)

    def get_transaction(self, i):
        """Returns the transaction at index i as an int array"""
        return self.transactions[i]

    def covers(self, i, itemset):
        """Returns whether the given itemset covers transaction i"""
        return itemset.issubset(self.get_transaction(i))

    def support(self, itemset):
        """Returns the support of the given itemset for the current list of transactions"""
        s = 0
        for i in range(self.trans_num()):
            if self.covers(i, itemset):
                s += 1
        return s

    def frequency(self, itemset):
        """Returns the frequency of the given itemset for the current list of transactions"""
        return self.support(itemset)/self.trans_num()


def apriori(filepath, minFrequency):
    """Runs the apriori algorithm on the specified file with the given minimum frequency
       This function implements the naive version of the algorithm"""
    data = Dataset(filepath) # read data
    minSupport = minFrequency * data.trans_num() # compute minimal support

    level = 1
    F = [[set([])]] # frequent sets
    while True:
        F.append([])
        # list of subsets of items of size level
        Clist = [set(i) for i in itertools.combinations(range(1, data.items_num() + 1), level)]
        for C in Clist:
            subsets = [set(i) for i in itertools.combinations(C, len(C) - 1)]
            # subsets of C with one element removed
            allIn = True
            for s in subsets:
                if s not in F[level-1]:
                    # if some subset is not frequent, C is not a candidate
                    allIn = False
                    break
            if allIn and data.support(C) >= minSupport:
                # append frequent itemsets
                F[level].append(C)
        if (len(F[level]) != 0):
            for s in F[level]:
                if s != set([]):
                    print(list(s), " ({:g})".format(data.frequency(s))) # print frequent sets
        else:
            break

        level += 1

def alternative_miner(filepath, minFrequency):
    """Runs the alternative frequent itemset mining algorithm on the specified file with the given minimum frequency"""
    # TODO: either second implementation of the apriori algorithm or implementation of the depth first search algorithm
    print("Not implemented")

if __name__== "__main__":
    apriori("../statement/Datasets/toy.dat", 0.125)
