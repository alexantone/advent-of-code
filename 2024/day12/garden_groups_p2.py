#!/bin/env python3
"""Day 12: Garden Groups P2"""

import sys
import itertools
from collections import deque, defaultdict
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

def get_consecutive_runs(arr):
    if len(arr) <= 1:
        return len(arr)

    arr = sorted(arr)
    deltas = (b-a for a,b in zip(arr[:-1], arr[1:]))
    return sum(d > 1 for d in deltas) + 1

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

def get_area(region):
    return len(region)

def get_sides(region):
    region = set(region)

    x_grouped = defaultdict(list)
    y_grouped = defaultdict(list)
    for x, y in region:
        x_grouped[x].append(y)
        y_grouped[y].append(x)

    edges_N = 0
    edges_S = 0
    edges_W = 0
    edges_E = 0

    for x, y_list in x_grouped.items():
        on_edge_N = [y for y in y_list if (x - 1, y) not in region]
        on_edge_S = [y for y in y_list if (x + 1, y) not in region]
        edges_N += get_consecutive_runs(on_edge_N)
        edges_S += get_consecutive_runs(on_edge_S)

    for y, x_list in y_grouped.items():
        on_edge_W = [x for x in x_list if (x, y - 1) not in region]
        on_edge_E = [x for x in x_list if (x, y + 1) not in region]
        edges_W += get_consecutive_runs(on_edge_W)
        edges_E += get_consecutive_runs(on_edge_E)

    return edges_N + edges_S + edges_W + edges_E

def main():
    input_path = sys.argv[1]
    grid = read_input(input_path)
    visited = np.zeros(grid.shape, dtype=bool)

    r, c = grid.shape
    regions = []
    for x, y in itertools.product(range(r), range(c)):
        if not visited[x,y]:
            regions.append(walk((x,y), grid, visited))

    fence_cost = sum(get_area(r) * get_sides(r) for _, r in regions)

    print(fence_cost)

if __name__ == "__main__":
    main()
