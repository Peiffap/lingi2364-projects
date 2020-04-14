#!/usr/bin/env python3

import sys

from bisect import insort, bisect_left
from collections import deque, defaultdict

import time

class Dataset:
    """Utility class to manage a dataset stored in a external file."""

    def __init__(self, filepath1, filepath2):
        """Reads the dataset file and initializes files"""
        self.itemsmap = {}
        self.member = defaultdict(list)
        self.freq = defaultdict(list)
        self.top = 0
        self.npos = 0

        # Read the positive class file.
        lines = [line.strip() for line in open(filepath1, "r")]
        i = 0
        for line in lines:
            if line:
                l = line.split()
                self.member[l[0]].append([i, int(l[1])])
                if tuple(l[0]) not in self.freq:
                    self.freq[tuple(l[0])].append(i)
                elif i not in self.freq[tuple(l[0])]:
                    self.freq[tuple(l[0])].append(i)
            else:
                i += 1

        # Read the negative class file.
        i = i - 1
        self.npos = i
        lines = [line.strip() for line in open(filepath2, "r")]
        for line in lines:
            if line:
                l = line.split()
                self.member[l[0]].append([i, int(l[1])])
                if tuple(l[0]) not in self.freq:
                    self.freq[tuple(l[0])].append(i)
                elif i not in self.freq[tuple(l[0])]:
                    self.freq[tuple(l[0])].append(i)
            else:
                i += 1

        self.sortedList = []


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

    if k == 0:
        return

    data = Dataset(pos_filepath, neg_filepath)
    frequentElements = deque() # Queue that contains next frequent items to explore.
    topSupp = [] # Top-k supports so far.


    def nsupp(itemList):
        """
        Count support of the item.
        """
        npos = 0
        nneg = 0
        for el in itemList:
            if el <= data.npos:
                npos += 1
            else:
                nneg += 1
        return nneg+npos, npos, nneg


    def dlt(supp):
        """
        Delete all the supports less than supp in the topSupp list.
        """
        pos = bisect_left(data.sortedList, [supp + 0.1])
        data.sortedList = data.sortedList[pos:]


    def frequentItemset(dict, item):
        """
        Explore frequent items in DFS.
        """

        # If there is no more items in the queue, then stop to exlore this branch.
        if len(frequentElements) == 0:
            return

        # Select positions of the item that we explore in the vertical representation.
        prev = 0
        itemPosition = defaultdict(list)
        for position in dict[item[len(item)-1]]:
            if(position[0] != prev):
                itemPosition[position[0]].append(position[1])
                prev = position[0]


        # Select next items to explore.
        positionToSave = defaultdict(list)
        itemToExplore = []
        for items in dict:
            for position in dict[items]:
                for pos in itemPosition[position[0]]:
                    if pos < position[1]:
                        positionToSave[items].append([position[0], position[1]])
                        if tuple(item + [items]) not in data.freq:
                            data.freq[tuple(item + [items])].append(position[0])
                        elif position[0] not in data.freq[tuple(item + [items])]:
                            data.freq[tuple(item + [items])].append(position[0])

            supp, npos, nneg = nsupp(data.freq[tuple(item + [items])])

            # Add the item to the frequentElements queue if the item is in the top k frequent.
            if supp in topSupp: # Add the item to the list if its support is already in the top-k supports.
                insort(data.sortedList, [supp, npos, nneg, item + [items]])
                frequentElements.append(item + [items])
                itemToExplore.append([items])
            elif data.top < k: # Add the item to the list if the list of the top-k supports is not full.
                insort(data.sortedList, [supp, npos, nneg, item + [items]])
                frequentElements.append(item + [items])
                itemToExplore.append([items])
                topSupp.append(supp)
                data.top = data.top + 1
            elif data.top == k and data.sortedList[0][0] < supp: # Add the item in the list if its support is greater than the smallest of the top-k supports.
                insort(data.sortedList, [supp, npos, nneg, item + [items]])
                frequentElements.append(item + [items])
                itemToExplore.append([items])
                topSupp.append(supp)
                topSupp.remove(data.sortedList[0][0])
                dlt(data.sortedList[0][0])

        for item in itemToExplore: # Explore all the frequent items that we have found previously.
            frequentItemset(positionToSave, frequentElements.pop())


    # Identify frequent length-1 elements.
    order = [] # Frequent items are sorted by descending order of their support.

    for item in data.member:
        supp, npos, nneg = nsupp(data.freq[tuple(item)])
        if supp in topSupp: # Add the item to the list if its support is already in the top-k supports.
            insort(data.sortedList, [supp, npos, nneg, [item]])
            insort(order, [-supp, [item]])
            frequentElements.append([item])
        elif data.top < k: # Add the item to the list if the list of top-k supports is not full.
            insort(data.sortedList, [supp, npos, nneg, [item]])
            topSupp.append(supp)
            insort(order, [-supp, [item]])
            frequentElements.append([item])
            data.top = data.top + 1
        elif data.top == k and data.sortedList[0][0] < supp: # Add the item to the list if its support is greater than the smallest of the top-k supports.
            topSupp.append(supp)
            topSupp.remove(data.sortedList[0][0])
            insort(data.sortedList, [supp, npos, nneg, [item]])
            insort(order, [-supp, [item]])
            frequentElements.append([item])
            dlt(data.sortedList[0][0])

    # Explore the items by descending order of their support.
    for item in order:
        frequentItemset(data.member, item[1])

    for sup, pos, neg, patt in data.sortedList:
        if verbose:
            print("[{}] {} {} {}".format(', '.join((i for i in patt)), pos, neg, sup))


if __name__ == "__main__":
    if len(sys.argv) == 1:
        a = time.perf_counter()
        #main("Protein/SRC1521.txt", "Protein/PKA_group15.txt", 13)
        main("Reuters/earn.txt", "Reuters/acq.txt", 64)
        #main("Test/positive.txt", "Test/negative.txt", 6)
        print(time.perf_counter() - a)
    else:
        main()