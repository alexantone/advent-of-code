#!/bin/env python3
"""Day 10: Hoof It P1"""

import sys
import itertools
import numpy as np

DIRECTIONS = np.array([
    [-1, 0],
    [ 0, 1],
    [ 1, 0],
    [ 0,-1],
])

def read_input(path):
    with open(path, mode="r", encoding="utf-8") as fp:
        return np.array([[int(c if c != '.' else -1) for c in l]
                            for l in fp.read().splitlines()],
                        dtype="int8")

def find_trailheads(grid):
    trailheads = []
    r, c  = grid.shape
    for x,y in itertools.product(range(r), range(c)):
        if grid[x,y] == 0:
            trailheads.append((x,y))
    return trailheads

def get_score(grid, pos, visited):
    r, c = grid.shape
    x, y = pos
    score=0
    visited.add(pos)
    cheight = grid[x,y]

    if cheight == 9:
        return 1

    neighbors = np.array([[x, y]] * 4) + DIRECTIONS
    for nx, ny in neighbors:
        if (0<= nx < r and 0<= ny < c and grid[nx, ny] == cheight + 1
            and (nx,ny) not in visited):
            score += get_score(grid, (nx, ny), visited)
    return score

def main():
    input_path = sys.argv[1]
    grid = read_input(input_path)
    trailheads = find_trailheads(grid)
    print(sum(get_score(grid, th, set()) for th in trailheads))


if __name__ == "__main__":
    main()
