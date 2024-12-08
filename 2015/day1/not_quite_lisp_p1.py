#!/bin/env python3
"""Day 1: Not Quite Lisp P1"""

import sys

DIRECTION_MAP = {
    '(': +1,
    ')': -1,
}
def read_input(path):
    with open(path, mode="r", encoding="utf-8") as fp:
        return fp.read()

def main():
    input_path = sys.argv[1]
    floor = 0
    for ix, c in enumerate(read_input(input_path), start=1):
        floor += DIRECTION_MAP[c]

    print(floor)

if __name__ == "__main__":
    main()
