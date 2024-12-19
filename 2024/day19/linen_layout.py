#!/bin/env python3
"""Day 19: Linen Layout P1, P2"""

import sys
import functools
from collections import defaultdict


def lmap(func, *iterables):
    return list(map(func, *iterables))

def min_max(l):
    return min(l), max(l)

def read_input(path):
    with open(path, mode="r", encoding="utf-8") as f:
        towels, patterns = f.read().split('\n\n')
        return sorted(towels.split(", ")), patterns.splitlines()

def build_towels_prefixes_map(towels):
    """Pre-computes a map of common prefixes"""
    prefix_map = defaultdict(list)
    min_l, max_l = min_max(lmap(len, towels))

    for prefix_len in range(min_l, max_l):
        for towel in towels:
            if len(towel) >= prefix_len:
                prefix_map[towel[:prefix_len]].append(towel)

    return prefix_map, min_l, max_l

def solve(pattern, prefix_map, find_all=False):
    @functools.cache
    def _solve(pattern, find_all):
        """
        Defined as closure with access to the unhashable prefix_map such that it
        still caches partial solutions for all patterns in the input.
        """
        bins, min_l, _ = prefix_map

        if len(pattern) == 0:
            return 1

        if len(pattern) < min_l:
            return 0

        s = 0
        for towel in bins[pattern[:min_l]]:
            if pattern.startswith(towel):
                s += _solve(pattern[len(towel):], find_all)
                if s > 0  and not find_all:
                    return 1
        return s

    return _solve(pattern, find_all)


def main():
    input_path = sys.argv[1]
    towels, patterns = read_input(input_path)

    prefix_map = build_towels_prefixes_map(towels)

    print(f"P1: {sum(solve(p, prefix_map) for p in patterns)}")
    print(f"P2: {sum(solve(p, prefix_map, find_all=True) for p in patterns)}")


if __name__ == "__main__":
    main()
