#!/bin/env python3
"""Day 20: Race Condition P1, P2"""

import sys
import re
import itertools
from collections import deque, defaultdict
import numpy as np


WALL = '#'
EMPTY = '.'
START = 'S'
FINISH = 'E'

DIRECTIONS_MAP = {
    "^": np.array([-1, 0], dtype=np.int8),
    ">": np.array([ 0, 1], dtype=np.int8),
    "v": np.array([ 1, 0], dtype=np.int8),
    "<": np.array([ 0,-1], dtype=np.int8),
}

DIRECTIONS = np.array([
    [-1, 0],
    [ 0, 1],
    [ 1, 0],
    [ 0,-1],
])

def ints(s: str):
    return [int(n) for n in re.findall(r"-?\d+", s)]

def read_grid_input(path):
    with open(path, mode="r", encoding="utf-8") as f:
        return np.array([list(l) for l in f.read().splitlines()]) # grid

def find_all(grid, value):
    return [tuple(pos) for pos, item in np.ndenumerate(grid) if item == value]

def find_one(grid, value):
    return next((tuple(pos) for pos, item in np.ndenumerate(grid) if item == value), None)

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

def in_bounds(grid, pos):
    r,c = grid.shape
    x,y = pos
    return (0 <= x < r and 0 <= y < c)

def walk(grid, start, finish, saved_costs):
    null_saved_cost = (np.inf, [])
    saved_costs[start] = (1, [start])

    if start == finish:
        return saved_costs[finish]

    exploration_queue=deque((get_dest(start, d), start) for d in DIRECTIONS_MAP)
    while exploration_queue:
        pos, prev = exploration_queue.popleft()
        prev_cost, trail = saved_costs[prev]

        if not in_bounds(grid, pos): continue
        if grid[pos] == WALL: continue

        cost = prev_cost + 1
        old_cost, _ = saved_costs.get(pos, null_saved_cost)
        if cost >= old_cost: continue

        finish_cost, _ = saved_costs.get(finish, null_saved_cost)
        if cost >= finish_cost: continue  # Cost exceeded

        saved_costs[pos] = cost, trail + [pos, ]  # Make copy and append

        for move_direction in DIRECTIONS_MAP:
            next_pos = get_dest(pos, move_direction)
            if next_pos == prev: continue  # No walking back

            # Update queue (optimization: avoid duplicates by searching from the end)
            if (next_pos, pos) not in reversed(exploration_queue):
                exploration_queue.append((next_pos, pos))

    return saved_costs.get(finish, null_saved_cost)

def get_distance(pa, pb):
    ax, ay = get_xy(pa)
    bx, by = get_xy(pb)
    return abs(bx - ax) + abs(by - ay)

def cheat_p1(grid, min_saving, trail):
    cheats = defaultdict(list)

    trail_map = dict((pos, ix) for ix, pos in enumerate(trail))
    for pos in trail_map:
        for move_direction in DIRECTIONS_MAP:
            cheat_pos = get_dest(pos, move_direction)
            if not in_bounds(grid, cheat_pos): continue
            if not grid[cheat_pos] == WALL: continue

            other_side = get_dest(pos, move_direction*2)
            if other_side in trail_map: # We found a shortcut:
                cost_saved = trail_map[other_side] - (trail_map[pos] + 2)
                if cost_saved >= min_saving:
                    cheats[cost_saved].append(cheat_pos)

    return cheats

def cheat_p2(max_cheat, min_saving, trail):
    cheats = defaultdict(list)

    trail_len = len(trail)
    for ix in range(min_saving, trail_len):
        if ix % 100 == 0: print(f"Iteration: {ix}/{trail_len}")  # Periodic status

        for jx in range(ix - min_saving - 1):
            dist = get_distance(trail[ix], trail[jx])
            cost_saved = ix - (jx + dist)
            if dist <= max_cheat and cost_saved >= min_saving:
                cheats[cost_saved].append((jx, ix))

    return cheats

def print_cheats(cheats: dict):
    for cost_save, teleports in sorted(cheats.items()):
        print(f"  - There are {len(teleports)} cheats that save {cost_save} picoseconds.")

def main():
    input_path = sys.argv[1]
    minsaving = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    grid = read_grid_input(input_path)
    start = find_one(grid, START)
    finish = find_one(grid, FINISH)

    finish_cost, trail = walk(grid, start, finish, {})

    cheats_p1=cheat_p1(grid, minsaving, trail)
    print("P1 cheats:")
    print_cheats(cheats_p1)

    cheats_p2=cheat_p2(20, minsaving, trail)
    print("P2 cheats:")
    print_cheats(cheats_p2)

    print(f"P1: {sum(len(teleports) for teleports in cheats_p1.values())}")
    print(f"P2: {sum(len(teleports) for teleports in cheats_p2.values())}")


if __name__ == "__main__":
    main()
