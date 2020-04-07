#!/usr/bin/env python3

import sys

from collections import defaultdict, Counter
from heapq import heappush, heappushpop, heappop

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
            print("Unable to read dataset file!\n" + e)

        self.transactions = self.transactions[:-1]

        self.wordmap = {}

        for doc in self.transactions:
            for word in doc:
                if not word in self.wordmap:
                    self.wordmap[word] = len(self.wordmap)
        self.db = [
            [self.wordmap[w] for w in doc]
            for doc in self.transactions
        ]

        self.invwordmap = self.invert(self.wordmap)

        self.results = []

    def invert(self, d):
        return {v: k for k, v in d.items()}

    def trans_num(self):
        """Returns the number of transactions in the dataset"""
        return len(self.transactions)

    def get_transaction(self, i):
        """Returns the transaction at index i as an array"""
        return self.transactions[i]

def invertedindex(seqs, entries):
    index = defaultdict(list)

    for k, seq in enumerate(seqs):
        i, lastpos = entries[k] if entries else (k, -1)

        for p, item in enumerate(seq, start=(lastpos + 1)):
            l = index[item]
            if len(l) and l[-1][0] == i:
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
        pos_filepath = pf # filepath to positive class file
        neg_filepath = nf # filepath to negative class file

    if k == 0:
        return

    data = Dataset(pos_filepath, neg_filepath)

    key = bound = lambda patt, matches: len(matches)

    def nsupp():
        if data.results == []:
            return 0, 0
        vals = Counter([i[0] for i in data.results]).values()
        return len(vals), list(vals)[0]

    def topk_canpass(sup):
        return nsupp()[0] == k and sup < data.results[0][0]

    def topk_verify(patt, matches):
        sup = key(patt, matches)

        if topk_canpass(sup):
            return

        ns = nsupp()
        if ns[0] <= k:
            heappush(data.results, (sup, patt, matches))
        else:
            heappushpop(data.results, (sup, patt, matches))
            ns = nsupp()
            if ns[0] > k:
                ind = ns[1]
                while ind > 0:
                    heappop(data.results)
                    ind -= 1

    def topk_rec(patt, matches):
        if len(patt) > 0:
            topk_verify(patt, matches)

        occurs = nextentries(data.db, matches)

        for newitem, newmatches in sorted(
                occurs.items(),
                key=lambda x: key(patt + [x[0]], x[1]),
                reverse=True
            ):
            newpatt = patt + [newitem]

            if topk_canpass(bound(newpatt, newmatches)):
                break

            topk_rec(newpatt, newmatches)

    topk_rec([], [(i, -1) for i in range(len(data.db))])

    for (sup, patt, matches) in data.results:
        pos_support = 0
        neg_support = 0
        for (tr, _) in matches:
            if tr < data.npos:
                pos_support += 1
            else:
                neg_support += 1
        print("[{}] {} {} {}".format(', '.join((data.invwordmap[i] for i in patt)), pos_support, neg_support, sup))

if __name__ == "__main__":
    if len(sys.argv) == 1:
        a = time.perf_counter()
        #main("../statement/Datasets/Protein/PKA_group15.txt", "../statement/Datasets/Protein/SRC1521.txt", 14)
        main("../statement/Datasets/Test/positive.txt", "../statement/Datasets/Test/negative.txt", 3)
        print(time.perf_counter() - a)
    else:
        main()