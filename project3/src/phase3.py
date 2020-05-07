"""The main program that runs gSpan. Two examples are provided"""
# -*- coding=utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import numpy
from sklearn import naive_bayes
from sklearn import tree
from sklearn import metrics

from gspan_mining import gSpan
from gspan_mining import GraphDatabase
from bisect import insort, bisect_left


class PatternGraphs:
    """
    This template class is used to define a task for the gSpan implementation.
    You should not modify this class but extend it to define new tasks
    """

    def __init__(self, database):
        # A list of subsets of graph identifiers.
        # Is used to specify different groups of graphs (classes and training/test sets).
        # The gid-subsets parameter in the pruning and store function will contain for each subset, all the occurrences
        # in which the examined pattern is present.
        self.gid_subsets = []

        self.database = database  # A graphdatabase instance: contains the data for the problem.

    def store(self, dfs_code, gid_subsets):
        """
        Code to be executed to store the pattern, if desired.
        The function will only be called for patterns that have not been pruned.
        In correlated pattern mining, we may prune based on confidence, but then check further conditions before storing.
        :param dfs_code: the dfs code of the pattern (as a string).
        :param gid_subsets: the cover (set of graph ids in which the pattern is present) for each subset in self.gid_subsets
        """
        print("Please implement the store function in a subclass for a specific mining task!")

    def prune(self, gid_subsets):
        """
        prune function: used by the gSpan algorithm to know if a pattern (and its children in the search tree)
        should be pruned.
        :param gid_subsets: A list of the cover of the pattern for each subset.
        :return: true if the pattern should be pruned, false otherwise.
        """
        print("Please implement the prune function in a subclass for a specific mining task!")


class FrequentPositiveGraphs(PatternGraphs):
    """
    Finds the frequent (support >= minsup) subgraphs among the positive graphs.
    This class provides a method to build a feature matrix for each subset.
    """

    def __init__(self, minsup, database, subsets, top_K, eliminate_list):
        """
        Initialize the task.
        :param minsup: the minimum positive support
        :param database: the graph database
        :param subsets: the subsets (train and/or test sets for positive and negative class) of graph ids.
        """
        super().__init__(database)
        self.patterns = []  # The patterns found in the end (as dfs codes represented by strings) with their cover (as a list of graph ids).
        self.minsup = minsup
        self.gid_subsets = subsets
        # self.gid_dubsets = sebset_test
        self.top_list = []  # list with all top items
        self.top_K = top_K
        self.top_current = 0  # current number of top items
        self.eliminate_list = eliminate_list

    """ remove all elements that have c as conference and f as frequency. """

    def remove(self, c, f):
        self.patterns = [item for item in self.patterns if item[0] != c or item[1] != f]
        self.top_list = [item for item in self.top_list if item[0] != c or item[1] != f]

    """ delete the least frequent items with value c as confidence. """

    def delete(self, c):

        min_frequency = float("inf")
        i = 0
        while i < len(self.top_list) and self.top_list[i][0] == c:
            if min_frequency > self.top_list[i][1]:
                min_frequency = self.top_list[i][1]
            i += 1

        # print("je suis viré")
        # print(min_frequency)
        # print(c)
        self.remove(c, min_frequency)

    """ check if there are any items with confidence c and frequency f. """

    def check_eq_freq(self, c, f):
        i = 0
        while i < len(self.top_list):
            if self.top_list[i][0] == c and self.top_list[i][1] == f:
                return True
            i += 1
        return False

    """ check if there are any items with confidence c but their frequency is smaller than f. """

    def check_min_freq(self, c, f):
        i = 0
        while i < len(self.top_list):
            if self.top_list[i][0] == c and self.top_list[i][1] < f:
                return True
            i += 1
        return False

    def in_list(self, dfs_code):
        for elem in self.eliminate_list:
            if elem in dfs_code:
                """print("in list")
                print(elem)
                print(dfs_code)
                print()"""
                return True
        return False

    """ Stores top_K patterns. """

    def store(self, dfs_code, gid_subsets):
        p = len(gid_subsets[0])
        n = len(gid_subsets[2])
        t = p + n
        c = p / t
        if self.in_list(dfs_code):
            return
        if self.check_eq_freq(c, t):
            insort(self.patterns, [c, t, dfs_code, gid_subsets])
            insort(self.top_list, [c, t])
        elif self.top_current < self.top_K:
            insort(self.patterns, [c, t, dfs_code, gid_subsets])
            insort(self.top_list, [c, t])
            self.top_current += 1
        elif self.top_current == self.top_K:
            if self.patterns[0][0] < c:
                self.delete(self.patterns[0][0])
                insort(self.patterns, [c, t, dfs_code, gid_subsets])
                insort(self.top_list, [c, t])
            elif self.patterns[0][0] == c and self.check_min_freq(c, t):
                self.delete(self.patterns[0][0])
                insort(self.patterns, [c, t, dfs_code, gid_subsets])
                insort(self.top_list, [c, t])

    """ Prunes any pattern that is not frequent. """

    def prune(self, gid_subsets):
        # first subset is the set of positive ids
        p = len(gid_subsets[0])
        n = len(gid_subsets[2])
        t = p + n
        return t < self.minsup

    """ creates a column for a feature matrix. """

    def create_fm_col(self, all_gids, subset_gids):
        subset_gids = set(subset_gids)
        bools = []
        for i, val in enumerate(all_gids):
            if val in subset_gids:
                bools.append(1)
            else:
                bools.append(0)
        return bools

    """ return a feature matrix for each subset of examples, in which the columns correspond to patterns
         and the rows to examples in the subset. """

    def get_feature_matrices(self):
        matrices = [[] for _ in self.gid_subsets]
        for pattern in self.patterns:
            for i, gid_subset in enumerate(pattern[3]):
                matrices[i].append(self.create_fm_col(self.gid_subsets[i], gid_subset))
        return [numpy.array(matrix).transpose() for matrix in matrices]


def example2():
    """
    Runs gSpan with the specified positive and negative graphs; finds all frequent subgraphs in the training subset of
    the positive class with a minimum support of minsup.
    Uses the patterns found to train a naive bayesian classifier using Scikit-learn and evaluates its performances on
    the test set.
    Performs a k-fold cross-validation.
    """

    args = sys.argv
    database_file_name_pos = args[1]  # First parameter: path to positive class file
    database_file_name_neg = args[2]  # Second parameter: path to negative class file
    top_K = int(args[3])  # Third parameter: top K
    minsup = int(args[4])  # Forth parameter: minimum support (note: this parameter will be k in case of top-k mining)
    nfolds = int(args[5])  # Fifth parameter: number of folds to use in the k-fold cross-validation.

    if not os.path.exists(database_file_name_pos):
        print('{} does not exist.'.format(database_file_name_pos))
        sys.exit()
    if not os.path.exists(database_file_name_neg):
        print('{} does not exist.'.format(database_file_name_neg))
        sys.exit()

    graph_database = GraphDatabase()  # Graph database object
    pos_ids = graph_database.read_graphs(
        database_file_name_pos)  # Reading positive graphs, adding them to database and getting ids
    neg_ids = graph_database.read_graphs(
        database_file_name_neg)  # Reading negative graphs, adding them to database and getting ids

    # If less than two folds: using the same set as training and test set (note this is not an accurate way to evaluate the performances!)
    if nfolds < 2:
        subsets = [
            pos_ids,  # Positive training set
            pos_ids,  # Positive test set
            neg_ids,  # Negative training set
            neg_ids  # Negative test set
        ]
        # Printing fold number:
        print('fold {}'.format(1))
        train_and_evaluate(minsup, graph_database, subsets, top_K)

    # Otherwise: performs k-fold cross-validation:
    else:
        pos_fold_size = len(pos_ids) // nfolds
        neg_fold_size = len(neg_ids) // nfolds
        for i in range(nfolds):
            # Use fold as test set, the others as training set for each class;
            # identify all the subsets to be maintained by the graph mining algorithm.
            subsets = [
                numpy.concatenate((pos_ids[:i * pos_fold_size], pos_ids[(i + 1) * pos_fold_size:])),
                # Positive training set
                pos_ids[i * pos_fold_size:(i + 1) * pos_fold_size],  # Positive test set
                numpy.concatenate((neg_ids[:i * neg_fold_size], neg_ids[(i + 1) * neg_fold_size:])),
                # Negative training set
                neg_ids[i * neg_fold_size:(i + 1) * neg_fold_size],  # Negative test set
            ]
            # Printing fold number:
            print('fold {}'.format(i + 1))
            train_and_evaluate(minsup, graph_database, subsets, top_K)


def train_and_evaluate(minsup, database, subsets, top_K):
    eliminate_list = []
    result = []

    for i in range(top_K):
        task = FrequentPositiveGraphs(minsup, database, subsets, 1, eliminate_list)  # Creating task
        gSpan(task).run()
        sort_list = []
        for pattern in task.patterns:
            sort_list.append([pattern[2], pattern[0], pattern[1]])
            # [cover in pos train set, cover in pos test set, cover in neg train set, cover in neg test set]
            # print(pattern[3])
        sort_list.sort()
        sort_list.sort(key=len)
        if len(sort_list) > 0:
            eliminate_list.append(sort_list[0][0])
            result.append(sort_list[0])
            for j in [0, 2]:
                for gid in sort_list[0][3][j]:
                    subsets[j].remove(gid)

    for elem in result:
        print('{} {} {}'.format(elem[0], elem[1], elem[2]))
    print()

    """psrint(pattern[2])"""

    """# Printing frequent patterns along with their positive support:
    for pattern in task.patterns:
        total_support = pattern[1]
        confidence = pattern[0]
        print('{} {} {}'.format(pattern[2], confidence, total_support))
    # printing classification results:
    print(predicted.tolist())
    print('accuracy: {}'.format(accuracy))
    print()  # Blank line to indicate end of fold."""


if __name__ == '__main__':
    #
    # example1()
    example2()
