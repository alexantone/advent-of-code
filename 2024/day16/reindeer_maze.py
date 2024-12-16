#!/bin/env python3
"""Day 16: Reindeer Maze P1, P2"""

import sys
import itertools
from collections import deque
import numpy as np


WALL = '#'
START = 'S'
FINISH = 'E'

DIRECTIONS_MAP = {
    "^": np.array([-1, 0], dtype=np.int8),
    ">": np.array([ 0, 1], dtype=np.int8),
    "v": np.array([ 1, 0], dtype=np.int8),
    "<": np.array([ 0,-1], dtype=np.int8),
}

OPPOSING_DIRECTIONS_MAP = {
    '^': 'v',
    'v': '^',
    '<': '>',
    '>': '<',
}


def read_grid_input(path):
    with open(path, mode="r", encoding="utf-8") as f:
        return np.array([list(l) for l in f.read().splitlines()]) # grid

def find_all(grid, value):
    return [tuple(pos) for pos, item in np.ndenumerate(grid) if item == value]

def find_one(grid, value):
    return next((tuple(pos) for pos, item in np.ndenumerate(grid) if item == value), None)

def get_xy(pos):
    return tuple(int(v) for v in pos)

def get_dest(pos, directions):
    pos = np.array(pos, dtype=np.int32)
    pos += sum(DIRECTIONS_MAP[d] for d in directions)
    return get_xy(pos)

def render_grid(grid):
    for row in grid:
        print("".join(itertools.chain.from_iterable(zip(row, ' ' * len(row)))))
    print()

def render_grid_visited(grid, visited):
    grid = np.array(grid) # Make a copy of original grid
    for pos in visited:
        grid[pos] = 'o'
    render_grid(grid)

def walk(grid, start_pos, facing, saved_costs, stop_pos):
    start_key = (start_pos, facing)
    exploration_queue=deque([start_key])
    saved_costs[start_key] = 0, set([start_pos, ])
    finish_cost = np.inf

    while exploration_queue:
        pos, facing = exploration_queue.popleft()
        cost, tiles = saved_costs[(pos, facing)]

        for move_direction in DIRECTIONS_MAP:
            next_pos = get_dest(pos, move_direction)

            if move_direction == OPPOSING_DIRECTIONS_MAP[facing]: continue # No walking back
            if grid[next_pos] == WALL: continue

            key = (next_pos, move_direction)
            next_cost = cost + 1 + int(facing != move_direction) * 1000
            next_tiles = tiles | set([next_pos, ])

            if next_pos == stop_pos and next_cost < finish_cost:
                finish_cost = next_cost

            old_cost, old_tiles = saved_costs.get(key, (np.inf, set()))
            if next_cost < old_cost:
                saved_costs[key] = next_cost, next_tiles
            elif next_cost == old_cost:
                saved_costs[key] = old_cost, old_tiles | next_tiles  # Combine tiles
            else:
                continue

            # Update queue
            if key not in exploration_queue:
                exploration_queue.append(key)

    return finish_cost

def main():
    input_path = sys.argv[1]
    grid = read_grid_input(input_path)
    start = find_one(grid, START)
    finish = find_one(grid, FINISH)

    saved_costs = {}
    finish_cost = walk(grid, start, '>', saved_costs, finish)
    all_tiles = set()

    if np.isinf(finish_cost):
        print("Finish cannot be reached!!")
        return

    for direction in DIRECTIONS_MAP:
        cost, tiles = saved_costs.get((finish, direction), (np.inf, set()))
        if cost == finish_cost:
            all_tiles |= tiles

    render_grid_visited(grid, all_tiles)
    print(f"{start=} {finish=}")
    print(finish_cost)
    print(len(all_tiles))

if __name__ == "__main__":
    main()
