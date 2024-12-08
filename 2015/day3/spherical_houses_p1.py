#!/bin/env python3
"""Day 3: Perfectly Spherical Houses in a Vacuum P1"""

import sys
import numpy as np

DIRECTIONS_MAP = {
    # direction: (dx,dy)
    "^": np.array([-1, 0]),
    "v": np.array([ 1, 0]),
    ">": np.array([ 0, 1]),
    "<": np.array([ 0,-1]),
}

def read_input(path):
    with open(path, mode="r", encoding="utf-8") as fp:
        return fp.read()

def main():
    input_path = sys.argv[1]
    pos = np.array([0, 0])
    houses = set()

    for c in read_input(input_path):
        houses.add(tuple(pos))
        pos += DIRECTIONS_MAP.get(c, np.array([0, 0]))

    print(len(houses))

if __name__ == "__main__":
    main()
