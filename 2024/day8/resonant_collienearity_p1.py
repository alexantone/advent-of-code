#!/bin/env python3
"""Day 8: Resonant Collinearity P1"""

import sys
import itertools
from collections import defaultdict
import numpy as np


def read_input(path):
    antennnas = defaultdict(list)
    with open(path, mode="r", encoding="utf-8") as fp:
        grid = [list(l) for l in fp.read().splitlines()]

    r,c = len(grid), len(grid[0])
    for i, j in itertools.product(range(r), range(c)):
        if grid[i][j] != '.':
            antennnas[grid[i][j]].append((i,j))

    return grid, antennnas

def main():
    antinodes = []
    input_path = sys.argv[1]
    grid, antennas = read_input(input_path)

    r, c = len(grid), len(grid[0])
    for freq, positions in antennas.items():
        for pos1, pos2 in itertools.combinations(positions, 2):
            pos1 = np.array(pos1)
            pos2 = np.array(pos2)
            dxy = pos2 - pos1

            for nx, ny in [pos1 - dxy, pos2 + dxy]:
                if 0 <= nx < r and 0 <= ny < c:
                    antinodes.append((nx, ny))

    print(len(set(antinodes)))

if __name__ == "__main__":
    main()
