#!/bin/env python3

import sys
from collections import Counter


def read_input(path):
    with open(path, mode="r", encoding="utf-8") as fp:
        return ((int(a), int(b)) for (a, b) in (l.split() for l in fp.readlines()))

def main():
    input_path = sys.argv[1]
    l,r = zip(*read_input(input_path))
    r = Counter(r)
    print(sum((r[n] *n) for n in l))


if __name__ == "__main__":
    main()
