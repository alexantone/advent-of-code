#!/bin/env python3
"""Day 4: Ceres Search P1"""

import sys
import itertools
import numpy as np

WORD_LIST = ["XMAS", "SAMX"]

def read_input(path):
    with open(path, mode="r", encoding="utf-8") as fp:
        return np.array([list(l[:-1]) for l in fp.readlines()])

def search_pos(matrix, i, j, word):
    """Search row, column and up/down diagonals starting from i, j"""
    rows, cols = matrix.shape
    wordlen=len(word)

    return sum([
        (j + wordlen <= cols) and np.array_equal(matrix[i, j:(j + wordlen)], word),  # row
        (i + wordlen <= rows) and np.array_equal(matrix[i:(i + wordlen), j], word),  # column
        (i + wordlen <= rows and j + wordlen <= cols)
            and np.array_equal(matrix[np.arange(i, i + wordlen, 1), np.arange(j, j + wordlen, 1)], word), # diagonal down
        (i - wordlen >= -1 and j + wordlen <= cols)
            and np.array_equal(matrix[np.arange(i, i - wordlen, -1), np.arange(j, j + wordlen, 1)], word), # diagonal up
    ])

def search(matrix, words):
    rows, cols = matrix.shape
    return sum(search_pos(matrix, i, j, word)
               for word in words
               for (i,j) in itertools.product(range(rows), range(cols)))

def main():
    input_path = sys.argv[1]
    matrix = read_input(input_path)

    print(search(matrix, [np.array(list(w)) for w in WORD_LIST]))


if __name__ == "__main__":
    main()
