#!/bin/env python3
"""Day 2: I Was Told There Would Be No Math P1"""

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

def present_wrapping_required(present):
    l,w,h = present
    return 2*l*w + 2*w*h + 2*h*l + min([l*w, w*h, h*l])

def main():
    input_path = sys.argv[1]
    read_input(input_path)

    presents = read_input(input_path)

    print(sum(present_wrapping_required(p) for p in presents))

if __name__ == "__main__":
    main()
