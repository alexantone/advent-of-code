#!/bin/env python3

import sys
from sortedcontainers import SortedList


def read_input(path):
    with open(path, mode="r", encoding="utf-8") as fp:
        return ((int(a), int(b)) for (a, b) in (l.split() for l in fp.readlines()))

def main():
    input_path = sys.argv[1]
    l = SortedList()
    r = SortedList()
    for (a, b) in read_input(input_path):
        l.add(a)
        r.add(b)
    
    print(sum(abs(a-b) for (a,b) in zip(l, r)))


if __name__ == "__main__":
    main()
