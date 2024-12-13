#!/bin/env python3
"""Day 13: Claw Contraption P2"""

import sys
import re


A_COST = 3
B_COST = 1
OFFSET = 10000000000000

def ints(s):
    return [int(n) for n in re.findall(r"-?\d+", s)]

def read_input(path):
    machines = []
    button_a = None
    button_b = None
    prize = None
    with open(path, mode="r", encoding="utf-8") as fp:
        for line in fp.read().splitlines():
            if line == "":
                machines.append((button_a, button_b, prize))
                continue

            item, desc = line.split(':')
            if item == "Button A":
                button_a = ints(desc)
            if item == "Button B":
                button_b = ints(desc)
            if item == "Prize":
                px, py = ints(desc)
                prize = (px + OFFSET, py + OFFSET)

    return machines

def solve_2d(a, b, p):
    ax, ay = a
    bx, by = b
    px, py = p
    ka = (px*by - py*bx) / (ax*by - ay*bx)
    kb = (px*ay - py*ax) / (bx*ay - by*ax)
    if ka == int(ka) and kb == int(kb):
        return int(ka * A_COST + kb * B_COST)
    return 0

def main():
    input_path = sys.argv[1]
    machines = read_input(input_path)
    total_cost = sum(solve_2d(a, b, p) for a, b, p in machines)
    print(total_cost)


if __name__ == "__main__":
    main()
