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

    # If trail gets longer than matrix size, the guard entered a cycle
    while len(trail) < rows*cols:
        trail.append((x, y))
        (dx, dy), new_direction = DIRECTIONS_MAP[direction]

        if not (-1 < x + dx < rows and -1 < y + dy < cols):
            break

        if matrix[x + dx][y + dy] != "#":
            x += dx
            y += dy
        else:
            direction = new_direction

    return trail

def main():
    input_path = sys.argv[1]
    matrix = read_input(input_path)

    trail = walk(matrix, *find_guard(matrix))
    print(len(set(trail)))

if __name__ == "__main__":
    main()
