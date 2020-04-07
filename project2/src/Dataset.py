#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from itertools import count

class Dataset:
    """Utility class to manage a dataset stored in a external file."""

    def __init__(self, filepath):
        """Reads the dataset file and initializes files"""
        self.transactions = [[]]
        try:
            lines = [line.strip() for line in open(filepath, "r")]
            i = 0
            for line in lines:
                if line:
                    self.transactions[i].append(line.split(" ")[0])
                elif self.transactions[i] != []:
                    self.transactions.append([])
                    i += 1
        except IOError as e:
            print("Unable to read dataset file!\n" + e)

        c = count(start=0)

        self.transactions = self.transactions[:-1]

        self.wordmap = {}

        self.db = [list(self.remap(doc, self.wordmap, c)) for doc in self.transactions]

        self.invwordmap = self.invert(self.wordmap)

    def invert(self, d):
        return {v: k for k, v in d.items()}

    def remap(self, data, mapping, c):
        key = lambda k: next(c)

        for k in data:
            yield mapping.setdefault(k, key(k))

    def trans_num(self):
        """Returns the number of transactions in the dataset"""
        return len(self.transactions)

    def get_transaction(self, i):
        """Returns the transaction at index i as an array"""
        return self.transactions[i]