#!/bin/env python3
"""Day 18: RAM Run P1, P2"""

import sys
import re
import itertools
from collections import deque
import numpy as np


WALL = '#'
EMPTY = '.'

DIRECTIONS_MAP = {
    "^": np.array([-1, 0], dtype=np.int8),
    ">": np.array([ 0, 1], dtype=np.int8),
    "v": np.array([ 1, 0], dtype=np.int8),
    "<": np.array([ 0,-1], dtype=np.int8),
}


def ints(s: str):
    return [int(n) for n in re.findall(r"-?\d+", s)]

def render_grid(grid):
    for row in grid:
        print("".join(itertools.chain.from_iterable(zip(row, ' ' * len(row)))))
    print()

def render_grid_visited(grid, visited, symbol='o'):
    grid = np.array(grid) # Make a copy of original grid
    for pos in visited:
        grid[pos] = symbol
    render_grid(grid)
    return grid

def set_grid(grid, pos_list, value):
    for pos in pos_list:
        grid[pos] = value

def get_xy(pos):
    return tuple(int(v) for v in pos)

def get_dest(pos, directions):
    pos = np.array(pos, dtype=np.int32)
    pos += sum(DIRECTIONS_MAP[d] for d in directions)
    return get_xy(pos)

def read_input(path):
    with open(path, mode="r", encoding="utf-8") as f:
        return [(x,y) for y,x in (ints(l) for l in f.read().splitlines())]


def walk(grid, start, finish, saved_costs, exit_immediately=False):
    r, c = grid.shape
    keep_tiles = not exit_immediately
    start_key = start
    exploration_queue=deque([(start_key, start_key)])
    saved_costs[start_key] = 0, keep_tiles and set([start, ])
    finish_cost = np.inf

    while exploration_queue:
        pos, prev = exploration_queue.popleft()
        cost, tiles = saved_costs[pos]

        for move_direction in DIRECTIONS_MAP:
            next_pos = get_dest(pos, move_direction)
            nx, ny = get_xy(next_pos)

            if next_pos == prev: continue # No walking back
            if not (0 <= nx < r and 0<= ny < c): continue # Outside the grid
            if grid[next_pos] == WALL: continue

            if next_pos == finish:
                if exit_immediately:
                    saved_costs[finish] = cost + 1, keep_tiles and (tiles | set([next_pos, ]))
                    return

            key = next_pos
            next_cost, next_tiles = cost + 1, keep_tiles and (tiles | set([next_pos, ]))

            if next_pos == finish and next_cost < finish_cost:
                finish_cost = next_cost

            old_cost, old_tiles = saved_costs.get(key, (np.inf, set()))
            if next_cost < old_cost:
                saved_costs[key] = next_cost, keep_tiles and next_tiles
            elif next_cost == old_cost:
                saved_costs[key] = old_cost, keep_tiles and (old_tiles | next_tiles)  # Combine tiles
            else:
                continue

            # Update queue (optimization: avoid duplicates by searching from the end)
            if (next_pos, pos) not in reversed(exploration_queue):
                exploration_queue.append((next_pos, pos))

    return finish_cost


def main():
    grid_size = 71
    nfirst_bytes = 1024

    input_path = sys.argv[1]
    if len(sys.argv) > 3:
        grid_size = int(sys.argv[2])
        nfirst_bytes = int(sys.argv[3])

    all_bytes = read_input(input_path)
    first_bytes = all_bytes[:nfirst_bytes]

    grid = np.full((grid_size, grid_size), '.', dtype='U1')
    set_grid(grid, first_bytes, WALL)

    # P1: A*
    start, finish = (0,0), (grid_size -1, grid_size - 1)
    saved_costs = {}
    p1_finish_cost = walk(grid, start, finish, saved_costs)


    # P2: Do a plain binary search
    l, r = nfirst_bytes, len(all_bytes) - 1
    while l < r:
        mid = l + (r - l) // 2
        test_bytes = all_bytes[nfirst_bytes:mid + 1]

        set_grid(grid, test_bytes, WALL)

        saved_costs = {}
        walk(grid, start, finish, saved_costs, exit_immediately=True)

        if finish not in saved_costs:
            l,r = l,mid
        else:
            l,r = mid+1,r

        set_grid(grid, test_bytes, EMPTY)

    # Print solutions:
    print(f"P1: {p1_finish_cost}")

    if finish not in saved_costs:
        y, x = get_xy(all_bytes[r])  # Invert coordinates
        print(f"P2: First blocking byte at position {r}: {x},{y}")
    else:
        print("P2: No solution!")


if __name__ == "__main__":
    main()
