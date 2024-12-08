#!/bin/env python3
"""Day 2: I Was Told There Would Be No Math P2"""

import sys
import re


def ints(s: str):
    return [int(n) for n in re.findall(r"-?\d+", s)]

def read_input(path):
    presents = []
    with open(path, mode="r", encoding="utf-8") as fp:
        for l in fp.readlines():
            presents.append(ints(l))
    return presents

def present_ribon_required(present):
    l,w,h = present
    return 2*min([l+w, w+h, h+l]) + l*w*h

def main():
    input_path = sys.argv[1]
    read_input(input_path)

    presents = read_input(input_path)

    print(sum(present_ribon_required(p) for p in presents))

if __name__ == "__main__":
    main()
