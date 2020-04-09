#!/usr/bin/env python3

import sys

from collections import defaultdict
from itertools import count
from bisect import insort, bisect_left
from operator import itemgetter
from math import log2
from scipy.optimize import minimize

import time

class Dataset:
    """Utility class to manage a dataset stored in a external file."""

    def __init__(self, filepath1, filepath2):
        """Reads the dataset file and initializes files"""
        self.transactions = [[]]
        try:
            lines = [line.strip() for line in open(filepath1, "r")]
            i = 0
            for line in lines:
                if line:
                    self.transactions[i].append(line.split(" ")[0])
                elif self.transactions[i] != []:
                    self.transactions.append([])
                    i += 1
            self.npos = len(self.transactions) - 1
            lines = [line.strip() for line in open(filepath2, "r")]
            for line in lines:
                if line:
                    self.transactions[i].append(line.split(" ")[0])
                elif self.transactions[i] != []:
                    self.transactions.append([])
                    i += 1
        except IOError as e:
            print(e)

        self.transactions = self.transactions[:-1]

        self.translen = [len(i) for i in self.transactions]

        self.wordmap = {}

        c = count()
        for doc in self.transactions:
            for word in doc:
                if not word in self.wordmap:
                    self.wordmap[word] = next(c)
        self.db = [
            [self.wordmap[w] for w in doc]
            for doc in self.transactions
        ]

        self.invwordmap = self.invert(self.wordmap)

        # Save memory
        self.wordmap = {}
        self.transactions = []

        self.results = []

        self.cmn = len(self.db)
        self.nneg = self.cmn - self.npos

        self.supdict = defaultdict(int)

        self.k = 0

        self.seenpatterns = []

        self.pn = [[round(self.information_gain(p, n), 5) for n in range(self.nneg+1)] for p in range(self.npos+1)]

        self.cumulativepn = [row[:] for row in self.pn]
        for i in range(self.npos+1):
            for j in range(self.nneg+1):
                if i == j == 0:
                    self.cumulativepn[i][j] = self.pn[i][j]
                elif j == 0:
                    self.cumulativepn[i][j] = max(self.cumulativepn[i-1][j], self.pn[i][j])
                elif i == 0:
                    self.cumulativepn[i][j] = max(self.cumulativepn[i][j-1], self.pn[i][j])
                else:
                    self.cumulativepn[i][j] = max(self.cumulativepn[i][j-1], self.cumulativepn[i-1][j], self.pn[i][j])

    def entropy(self, x):
        if x <= 0 or x >= 1:
            return 0
        return -x * log2(x) - (1 - x) * log2(1 - x)

    def information_gain(self, p, n):
        P = self.npos
        N = self.nneg
        if p == P and n == N or p == n == 0:
            return 0
        return self.entropy(P / self.cmn) - (p + n) * self.entropy(p / (p + n)) / self.cmn - (self.cmn - p - n) * self.entropy((P - p) / (self.cmn - p - n)) / self.cmn

    def invert(self, d):
        return {v: k for k, v in d.items()}

def invertedindex(seqs, entries):
    index = defaultdict(list)

    for k, seq in enumerate(seqs):
        i, lastpos = entries[k]

        for p, item in enumerate(seq, start=(lastpos + 1)):
            l = index[item]
            if len(l) != 0 and l[-1][0] == i:
                continue
            l.append((i, p))

    return index


def nextentries(data, entries):
    return invertedindex(
        (data[i][lastpos + 1:] for i, lastpos in entries),
        entries
    )

def main(pf=None, nf=None, k=None):
    if pf is None or nf is None or k is None:
        pos_filepath = sys.argv[1] # filepath to positive class file
        neg_filepath = sys.argv[2] # filepath to negative class file
        k = int(sys.argv[3])
    else:
        prefix = "../../../statement/Datasets/"
        pos_filepath = prefix + pf # filepath to positive class file
        neg_filepath = prefix + nf # filepath to negative class file

    if k == 0:
        return

    data = Dataset(pos_filepath, neg_filepath)

    def bound_and_key(matches):
        """
        Computes bound and value for information gain.
        """
        p, n = signsup(matches)
        return data.cumulativepn[p][n], data.pn[p][n], p, n

    def signsup(matches):
        """
        Computes the supports in the positive and negative classes.
        """
        pos_support = bisect_left(matches, (data.npos, -1))
        neg_support = len(matches) - pos_support
        return pos_support, neg_support

    def contains(patt1, patt2):
        """
        Returns whether patt1 contains patt2.
        """
        k = -1
        for i in range(len(patt2)):
            for j in range(k+1, len(patt1) + 1):
                if j == len(patt1):
                    return False
                if patt1[j] == patt2[i]:
                    k = j
                    break
        return True

    def isclosed(patt, p, n):
        for tup in data.results:
            if tup[3] == p and tup[4] == n and len(tup[1]) > len(patt) and contains(tup[1], patt):
                # If contained in existing pattern, not closed.
                return False

        # Not contained in any patterns.
        return True

    def closedcanprune(patt, ps, ns):
        for tup in data.seenpatterns:
            if tup[1] == ps and tup[2] == ns:
                if contains(tup[0], patt):
                    # If contained in existing pattern, not closed.
                    return True

        # Not contained in any patterns.
        return False

    def clospan_score(matches, npos):
        pscore = sum([data.translen[t] - p + 1 for (t, p) in matches[:npos]])
        nscore = sum([data.translen[t] - p + 1 for (t, p) in matches[npos:]])
        return pscore, nscore

    def topk_verify(patt, matches, sup, p, n, ps, ns):
        """
        Tries to insert a new pattern into the results.
        """
        data.seenpatterns.append((patt, ps, ns))
        if (sup, patt, matches, p, n) in data.results or len(data.supdict) == data.k and sup < data.results[0][0]:
            return

        data.supdict[sup] += 1

        # If there were k support values in the results and we add a new one,
        # we must remove the values with the lowest support previously.
        if len(data.supdict) == data.k + 1:
            val = data.supdict[data.results[0][0]]
            del data.supdict[data.results[0][0]]
            data.results = data.results[val:]

        insort(data.results, (sup, patt, matches, p, n))

    def topk_rec(patt, matches, sup, p, n, ps, ns):
        if patt != []:
            topk_verify(patt, matches, sup, p, n, ps, ns)

        occurs = nextentries(data.db, matches)

        new = [(x[0], x[1], bound_and_key(x[1])) for x in occurs.items()]
        new.sort(key=itemgetter(2), reverse=True) # Sort on bound, then value of infogain.
        for newitem, newmatches, (bnd, sup, p, n) in new:
            if len(data.supdict) == data.k and bnd < data.results[0][0]:
                break

            newpatt = patt + [newitem]

            ps, ns = clospan_score(newmatches, p)
            if closedcanprune(newpatt, ps, ns):
                continue

            topk_rec(newpatt, newmatches, sup, p, n, ps, ns)

    for j in range(1, k+1):
        data.k = j # This loop stops the miner from getting stuck on large datasets.
        data.seenpatterns = []
        topk_rec([], [(i, -1) for i in range(len(data.db))], 0, 0, 0, 0, 0) # Last arguments ignored.

    for (sup, patt, _, p, n) in data.results:
        if isclosed(patt, p, n):
            print("[{}] {} {} {}".format(', '.join((data.invwordmap[i] for i in patt)), p, n, sup))

if __name__ == "__main__":
    if len(sys.argv) == 1:
        import cProfile
        a = time.perf_counter()
        #cProfile.run('main("Reuters/earn.txt", "Reuters/acq.txt", 10)')
        #cProfile.run('main("Protein/SRC1521.txt", "Protein/PKA_group15.txt", 95)')
        #main("Protein/SRC1521.txt", "Protein/PKA_group15.txt", 5)
        main("Test/positive.txt", "Test/negative.txt", 1)
        print(time.perf_counter() - a)
    else:
        main()