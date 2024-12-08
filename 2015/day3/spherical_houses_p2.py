#!/bin/env python3
"""Day 3: Perfectly Spherical Houses in a Vacuum P2"""

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
    pos_santa = np.array([0, 0])
    pos_robot = np.array([0, 0])
    houses = set()

    santas_turn = True
    for c in read_input(input_path):
        if santas_turn:
            houses.add(tuple(pos_santa))
            pos_santa += DIRECTIONS_MAP.get(c, np.array([0, 0]))
        else:
            houses.add(tuple(pos_robot))
            pos_robot += DIRECTIONS_MAP.get(c, np.array([0, 0]))

        santas_turn = not santas_turn

    print(len(houses))

if __name__ == "__main__":
    main()
