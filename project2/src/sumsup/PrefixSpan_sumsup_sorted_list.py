#!/usr/bin/env python3

import sys

from collections import defaultdict
from bisect import insort, bisect_left
from operator import itemgetter

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

        # Create a wordmap to work on integers and make new db.
        self.wordmap = {}

        for doc in self.transactions:
            for word in doc:
                if not word in self.wordmap:
                    self.wordmap[word] = len(self.wordmap)
        self.db = [
            [self.wordmap[w] for w in doc]
            for doc in self.transactions
        ]

        self.transactions = [] # Clear useless db.

        # Invert wordmap.
        self.invwordmap = invert(self.wordmap)

        self.wordmap = {} # Clear wordmap.

        self.results = [] # Result tuples (sup, patt, matches)
        self.supdict = defaultdict(int) # Current dictionary of top-k supports.


def invert(d):
    """
    Inverts a dictionary.
    """
    return {v: k for k, v in d.items()}


# Functions to compute list of new matches.
def invertedindex(seqs, entries):
    index = defaultdict(list)

    for k, seq in enumerate(seqs):
        i, lastpos = entries[k]

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


def main(pf=None, nf=None, k=None, verbose=True):
    if pf is None or nf is None or k is None:
        pos_filepath = sys.argv[1] # filepath to positive class file
        neg_filepath = sys.argv[2] # filepath to negative class file
        k = int(sys.argv[3])
    else:
        if verbose:
            prefix = "../../statement/Datasets/"
        else:
            prefix = "../statement/Datasets/"
        pos_filepath = prefix + pf # filepath to positive class file
        neg_filepath = prefix + nf # filepath to negative class file

    if k == 0: # Corner case.
        return

    # Initialize database.
    data = Dataset(pos_filepath, neg_filepath)


    def signsup(matches):
        """
        Compute positive and negative support.
        """
        pos_support = bisect_left(matches, (data.npos, -1))
        neg_support = len(matches) - pos_support
        return pos_support, neg_support


    def bound_and_key(matches):
        """
        Compute value for the bound and key (total support in this case).
        """
        return len(matches), len(matches)


    def topk_verify(patt, matches, sup):
        """
        Try to insert pattern in results.
        """
        # If worse than kth best, ignore pattern.
        # For support score, this does not matter, but for other scoring functions it does.
        if len(data.supdict) == k and sup < data.results[0][0]:
            return

        data.supdict[sup] += 1

        # If there were k support values in the results and we add a new one,
        # we must remove the values with the lowest support previously.
        if len(data.supdict) == k + 1:
            val = data.supdict[data.results[0][0]]
            del data.supdict[data.results[0][0]]
            data.results = data.results[val:]

        # Maintain sorted property.
        insort(data.results, (sup, patt, matches))


    def topk_rec(patt, matches, sup):
        """
        Main function, calls itself recursively in a DFS manner.
        """
        if patt != []:
            topk_verify(patt, matches, sup)

        # Update list of matches.
        occurs = nextentries(data.db, matches)

        # New search directions.
        new = [(x[0], x[1], bound_and_key(x[1])) for x in occurs.items()]
        new.sort(key=itemgetter(2), reverse=True) # Sort on support.
        for newitem, newmatches, (bnd, key) in new:
            # If the support is lower than the existing kth best, prune search tree.
            if len(data.supdict) == k and bnd < data.results[0][0]:
                break

            newpatt = patt + [newitem] # Construct new pattern.

            topk_rec(newpatt, newmatches, key) # Recursive call.


    topk_rec([], [(i, -1) for i in range(len(data.db))], 0) # Last arg ignored.

    # Print results.
    for (sup, patt, matches) in data.results:
        p, n = signsup(matches)
        if verbose:
            print("[{}] {} {} {}".format(', '.join((data.invwordmap[i] for i in patt)), p, n, sup))


if __name__ == "__main__":
    if len(sys.argv) == 1:
        import cProfile
        import time
        a = time.perf_counter()
        #main("Reuters/earn.txt", "Reuters/acq.txt", 3)
        main("Test/positive.txt", "Test/negative.txt", 3)
        print(time.perf_counter() - a)
    else:
        main()