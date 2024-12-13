#!/bin/env python3
"""Day 13: Claw Contraption P1"""

import sys
import re


A_COST = 3
B_COST = 1

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
                prize = ints(desc)

    return machines

def solve_1d(a, b, p):
    solutions = set()
    for ka in range(p // a + 1):
        if (p - a * ka) % b == 0:
            kb = (p - a * ka) // b
            cost = ka * A_COST + kb * B_COST
            solutions.add((cost, ka, kb))
    return solutions

def main():
    input_path = sys.argv[1]
    machines = read_input(input_path)

    total_cost = 0
    for a, b, prize in machines:
        xa, ya = a
        xb, yb = b
        xp, yp = prize
        solx = solve_1d(xa, xb, xp)
        soly = solve_1d(ya, yb, yp)
        res = solx & soly
        cost, na, nb = next(iter(sorted(res)), (0, 0, 0))
        if cost != 0 and max(na, nb) <= 100:
            total_cost += cost

    print(total_cost)


if __name__ == "__main__":
    main()
