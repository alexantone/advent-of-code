#!/bin/env python3
"""Day 14: Restroom Redoubt P1, P2"""

import sys
import re
import math
from collections import Counter, defaultdict

import numpy as np
from PIL import Image


GRID_SIZE_X=101
GRID_SIZE_Y=103

def ints(s: str):
    return [int(n) for n in re.findall(r"-?\d+", s)]

def read_input(path):
    with open(path, mode="r", encoding="utf-8") as fp:
        return [ints(line) for line in fp.read().splitlines()]

def compute_position(robot, seconds):
    px, py, vx, vy = robot
    x = (px + vx * seconds) % GRID_SIZE_X
    y = (py + vy * seconds) % GRID_SIZE_Y
    return x, y

def get_quadrant(px, py):
    if px == GRID_SIZE_X // 2 or py == GRID_SIZE_Y // 2:
        return -1

    if px < GRID_SIZE_X // 2:
        return 1 if py < GRID_SIZE_Y // 2 else 3
    else:
        return 2 if py < GRID_SIZE_Y // 2 else 4

def find_max_consecutive_run(arr):
    arr = set(arr)
    seen = set()
    max_run = 0
    for n in arr:
        if n in seen:
            continue

        r, l = n, n
        while r - 1 in arr:
            seen.add(r - 1)
            r -= 1
        while l + 1 in arr:
            seen.add(l + 1)
            l += 1

        max_run = max(max_run, l - r + 1)

    return max_run

def render_grid_png(robots, seconds):
    grid = np.zeros((GRID_SIZE_Y, GRID_SIZE_X), dtype=np.uint8)
    final_positions = set(compute_position(r, seconds) for r in robots)
    for x,y in final_positions:
        grid[y,x] = 255
    image = Image.fromarray(grid, mode='L')
    image.save(f"evolution_{seconds:09d}.png")


def main():
    input_path = sys.argv[1]
    robots = read_input(input_path)

    final_positions = [compute_position(r, 100) for r in robots]
    qcounts = Counter(get_quadrant(*p) for p in final_positions)
    print(math.prod(qcounts.get(q, 1) for q in [1, 2, 3, 4]))

    # Christmass tree heuristics
    max_x_offset = 40 # Search in an area around the vertical midline of the grid
    min_h = 15 # Tree min height

    candidates = []
    for ix in range(GRID_SIZE_X * GRID_SIZE_Y):
        final_positions = set(compute_position(r, ix) for r in robots)
        x_grouped = defaultdict(set)
        for x,y in final_positions:
            x_grouped[x].add(y)

        for x, yvals in x_grouped.items():
            if abs(x - GRID_SIZE_X // 2) <= max_x_offset:
                curr_h = find_max_consecutive_run(yvals)
                if curr_h >= min_h:
                    print(f"seconds={ix} {x=} height={curr_h}")
                    candidates.append(ix)
                    break

    # Generate images for the candidates
    for ix in candidates:
        render_grid_png(robots, ix)

if __name__ == "__main__":
    main()
