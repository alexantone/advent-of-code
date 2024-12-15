#!/bin/env python3
"""Day 15: Warehouse Woes P1"""

import sys
import numpy as np


BOX = 'O'
WALL = '#'
ROBOT = '@'
EMPTY = '.'

DIRECTIONS_MAP = {
    "^": np.array([-1, 0], dtype=np.int8),
    ">": np.array([ 0, 1], dtype=np.int8),
    "v": np.array([ 1, 0], dtype=np.int8),
    "<": np.array([ 0,-1], dtype=np.int8),
}

def read_input(path):
    with open(path, mode="r", encoding="utf-8") as f:
        sgrid, sdirections = f.read().split('\n\n')
        grid = np.array([list(l) for l in sgrid.splitlines()], dtype="U1") # grid
        directions = "".join(sdirections.splitlines())
    return grid, directions

def find_robot(grid):
    for pos, item in np.ndenumerate(grid):
        if item == ROBOT:
            grid[pos] = EMPTY # Extract robot
            return tuple(pos)
    return None

def find_all_boxes(grid):
    boxes = []
    for pos, item in np.ndenumerate(grid):
        if item == BOX:
            boxes.append(tuple(pos))
    return boxes

def push_box(pos, grid, direction):
    nx, ny = np.array(pos, dtype=np.int32) + DIRECTIONS_MAP[direction]
    if grid[nx,ny] == WALL:
        return pos
    if grid[nx,ny] == EMPTY:
        grid[pos], grid[nx,ny] = grid[nx,ny], grid[pos] # Swap
        return (nx, ny)

    if grid[nx,ny] == BOX:
        push_box((nx,ny), grid, direction)
        if grid[nx,ny] == EMPTY:
            grid[pos], grid[nx,ny] = grid[nx,ny], grid[pos] # Swap
            return (nx, ny)

    return pos

def move(pos, grid, direction):
    r, c = grid.shape
    nx, ny = np.array(pos, dtype=np.int32) + DIRECTIONS_MAP[direction]

    if not (0 <= nx < r and 0<= ny < c):
        return pos
    if grid[nx,ny] == WALL:
        return pos
    if grid[nx,ny] == EMPTY:
        return (nx, ny)
    if grid[nx,ny] == BOX:
        push_box((nx, ny), grid, direction)
        if grid[nx,ny] == EMPTY:
            return (nx, ny)
    return pos

def get_gps(x, y):
    return x * 100 + y

def render_grid(robot, grid):
    grid[robot] = '@'
    for row in grid:
        print("".join(row))
    grid[robot] = '.'
    print()


def main():
    input_path = sys.argv[1]
    grid, directions = read_input(input_path)

    pos = find_robot(grid)
    for ix, d in enumerate(directions, start=1):
        pos = move(pos, grid, d)
        # print(f"\nMove {ix} {d} resulting state:")
        # render_grid(pos, grid)

    boxes = find_all_boxes(grid)
    total = sum(get_gps(*pos) for pos in boxes)
    render_grid(pos, grid)
    print(total)


if __name__ == "__main__":
    main()
