#!/bin/env python3
"""Day 3: Mull It Over"""

import sys
import re

def read_input(path):
    with open(path, mode="r", encoding="utf-8") as fp:
        return fp.read()

def main():
    input_path = sys.argv[1]
    text = read_input(input_path)
    sum = 0
    for instr in re.findall(r"mul\(\d+,\d+\)", text):
        a, b = re.findall(r"\d+", instr)
        sum += int(a) * int(b)

    print(sum)


if __name__ == "__main__":
    main()
