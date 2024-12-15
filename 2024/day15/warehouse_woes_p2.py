#!/bin/env python3
"""Day 15: Warehouse Woes P2"""

import sys
import numpy as np


BOX = 'O'
WALL = '#'
ROBOT = '@'
EMPTY = '.'

# Wide box
WBOX_L = '['
WBOX_R = ']'

DIRECTIONS_MAP = {
    "^": np.array([-1, 0], dtype=np.int8),
    ">": np.array([ 0, 1], dtype=np.int8),
    "v": np.array([ 1, 0], dtype=np.int8),
    "<": np.array([ 0,-1], dtype=np.int8),
}

def parse_row(row):
    res = ['.'] * (2 * len(row))
    for ix, ch in enumerate(row):
        if ch == WALL:
            res[2*ix], res[2*ix+1] = '#', '#'
        if ch == ROBOT:
            res[2*ix] = '@'
        if ch == BOX:
            res[2*ix], res[2*ix+1] = '[', ']'
    return res

def read_input(path):
    with open(path, mode="r", encoding="utf-8") as f:
        sgrid, sdirections = f.read().split('\n\n')
        grid = np.array([parse_row(l) for l in sgrid.splitlines()], dtype="U1") # grid
        directions = "".join(sdirections.splitlines())
    return grid, directions

def find_robot(grid):
    for pos, item in np.ndenumerate(grid):
        if item == ROBOT:
            grid[pos] = EMPTY # Extract robot
            return tuple(pos)
    return None

def get_dest(pos, directions):
    pos = np.array(pos, dtype=np.int32)
    pos += sum(DIRECTIONS_MAP[d] for d in directions)
    return tuple(pos)

def find_connected_boxes(pos, grid, direction, boxes):
    r, c = grid.shape
    x, y = pos
    if not (0 <= x < r and 0<= y < c):
        return True

    current_tile = grid[pos]
    if current_tile in [EMPTY, WALL]:
        return current_tile == WALL

    box_pos = pos if current_tile == WBOX_L else get_dest(pos, '<')
    if box_pos in boxes: # Already seen this box
        return False

    found_wall = False
    boxes.add(box_pos)
    search_next = []

    if direction in "<>":
        search_next = [get_dest(pos, direction * 2)] # look 2 spaces over
    elif direction in '^v':
        search_next = [get_dest(box_pos, direction), get_dest(box_pos, [direction, '>'])]

    for next_pos in search_next:
        found_wall |= find_connected_boxes(next_pos, grid, direction, boxes)

    return found_wall


def push_boxes(boxes, grid, direction):
    # Clear boxes old positions
    for box in boxes:
        grid[box] = EMPTY
        grid[get_dest(box, '>')] = EMPTY
    # Redraw in new positions
    for box in boxes:
        grid[get_dest(box, direction)] = WBOX_L
        grid[get_dest(box, [direction, '>'])] = WBOX_R

def move(pos, grid, direction):
    next_pos = get_dest(pos, direction)

    boxes = set()
    found_wall = find_connected_boxes(next_pos, grid, direction, boxes)
    if found_wall:
        return pos

    push_boxes(boxes, grid, direction)
    return next_pos

def find_all_boxes(grid):
    boxes = []
    for pos, item in np.ndenumerate(grid):
        if item == WBOX_L:
            boxes.append(tuple(pos))
    return boxes


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
