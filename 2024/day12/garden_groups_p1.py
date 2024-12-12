#!/bin/env python3
"""Day 12: Garden Groups P1"""

import sys
import itertools
from collections import deque
import numpy as np


DIRECTIONS = np.array([
    [-1, 0],
    [ 0, 1],
    [ 1, 0],
    [ 0,-1],
])

def read_input(path):
    with open(path, mode="r", encoding="utf-8") as fp:
        return np.array([list(l) for l in fp.read().splitlines()], dtype="U1")

def neighbors(pos, grid):
    r ,c = grid.shape
    return [(x.item(), y.item())
            for x,y in (np.array([pos] * 4) + DIRECTIONS)
            if 0 <= x < r and 0<= y < c]

def walk(pos, grid, visited, region=None, to_visit=None):
    if visited[pos]:
        return

    region = region or []
    to_visit = to_visit or deque()
    visited[pos] = True
    region.append(pos)
    planttype = grid[pos]

    for x,y in neighbors(pos, grid):
        if grid[x,y] == planttype:
            to_visit.append((x,y))

    while to_visit:
        walk(to_visit.popleft(), grid, visited, region, to_visit)

    return planttype, region

def get_perimeter(grid, region):
    perimeter = 0
    region = set(region)
    for pos in region:
        perimeter += 4 - sum(n in region for n in neighbors(pos, grid))
    return perimeter

def get_area(region):
    return len(region)

def main():
    input_path = sys.argv[1]
    grid = read_input(input_path)
    visited = np.zeros(grid.shape, dtype=bool)

    regions = []
    r, c = grid.shape
    for x, y in itertools.product(range(r), range(c)):
        if not visited[x,y]:
            regions.append(walk((x,y), grid, visited))

    fence_cost = sum(get_area(r) * get_perimeter(grid, r) for _, r in regions)

    print(fence_cost)


if __name__ == "__main__":
    main()
