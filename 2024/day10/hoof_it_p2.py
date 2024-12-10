#!/bin/env python3
"""Day 10: Hoof It P2"""

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
    r,c  = grid.shape
    for x,y in itertools.product(range(r), range(c)):
        if grid[x,y] == 0:
            trailheads.append((x,y))
    return trailheads

def get_rating(grid, pos):
    r, c = grid.shape
    x, y = pos
    rating = 0
    cheight = grid[x,y]

    if cheight == 9:
        return 1

    neighbors = np.array([[x, y]] * 4) + DIRECTIONS
    for nx, ny in neighbors:
        if 0<= nx < r and 0<= ny < c and grid[nx, ny] == cheight + 1:
            rating += get_rating(grid, (nx, ny))
    return rating

def main():
    input_path = sys.argv[1]
    grid = read_input(input_path)
    trailheads = find_trailheads(grid)
    print(sum(get_rating(grid, th) for th in trailheads))


if __name__ == "__main__":
    main()
