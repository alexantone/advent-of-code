#!/bin/env python3
"""Day 2: Red-Nosed Reports"""

import sys

def convert_line(line):
    return [int(n) for n in line.split()]

def read_input(path):
    with open(path, mode="r", encoding="utf-8") as fp:
        return (convert_line(l) for l in fp.readlines())

def check_safe_single(report):
    delta = report[-1] - report[0]
    if delta == 0:
        return False
    order = 1 if delta > 0 else -1
    allowed_levels = set(n * order for n in [1, 2, 3])
    return all((d in allowed_levels) for d in (b-a for (a, b) in zip(report[:-1], report[1:])))

def check_safe_naive(report):
    if check_safe_single(report):
        return True

    for ix in range(len(report)):
        new_report = report[:ix] + report[(ix + 1):]
        if check_safe_single(new_report):
            return True

    return False


def main():
    input_file = sys.argv[1]
    print(sum(check_safe_naive(report) for report in read_input(input_file)))


if __name__ == "__main__":
    main()