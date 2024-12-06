#!/bin/env python3
"""Day 6: Guard Gallivant P1"""

import sys


DIRECTIONS_MAP = {
    # direction: (dx,dy), changed direction
    "^": ((-1, 0), ">"),
    "v": (( 1, 0), "<"), #V": (( 1, 0), "<"),
    ">": (( 0, 1), "v"),
    "<": (( 0,-1), "^"),
}

def read_input(path):
    matrix = []
    with open(path, mode="r", encoding="utf-8") as fp:
        for line in fp.readlines():
            matrix.append(list(line.strip()))
    return matrix

def find_guard(matrix):
    for ix, row in enumerate(matrix):
        for jx, ch in enumerate(row):
            if ch in DIRECTIONS_MAP:
                return (ix, jx, ch)

def walk(matrix, x, y, direction):
    rows = len(matrix)
    cols = len(matrix[0])
    trail = []
    seen = set()
    cycle = False

    while True:
        if (x, y, direction) in seen:
            cycle = True
            break

        trail.append((x, y, direction))
        seen.add((x, y, direction))

        (dx, dy), new_direction = DIRECTIONS_MAP[direction]

        if not (-1 < x + dx < rows and -1 < y + dy < cols):
            break

        if matrix[x + dx][y + dy] != "#":
            x += dx
            y += dy
        else:
            direction = new_direction

    return trail, cycle

def walk_multiverse(matrix):
    x, y, direction = find_guard(matrix)

    # Find original guard path
    trail, cycle = walk(matrix, x, y, direction)

    total = 0
    # Try placing obstacles on the unique positions of the original path
    for ix, jx in set((x, y) for x, y, d in trail):
        # Cannot place block on guard starting position
        if (ix, jx) == (x, y):
            continue

        # Should not happen, but just in case to avoid counting existing block
        if matrix[ix][jx] == '#':
            continue

        matrix[ix][jx] = '#'  # add obstacle
        _, cycle = walk(matrix, x, y, direction)
        matrix[ix][jx] = '.'  # revert obstacle

        total += cycle  # test if cycle detected

    return total

def main():
    input_path = sys.argv[1]
    matrix = read_input(input_path)
    res = walk_multiverse(matrix)
    print(res)

if __name__ == "__main__":
    main()
