#!/bin/env python3
"""Day 5: Doesn't He Have Intern-Elves For This? P2"""

import sys
from collections import defaultdict


def read_input(path):
    with open(path, mode="r", encoding="utf-8") as fp:
        return fp.read().splitlines()

def check_nice_rule1(word):
    seen_dict = defaultdict(list)
    for ix,s in enumerate(zip(word[:-1], word[1:])):
        seen = seen_dict[s]
        seen.append(ix)
        if len(seen) == 2:
            a,b = seen
            if b -a >= 2:
                return True
        if len(seen) >= 3:
            return True

    return False

def check_nice_rule2(word):
    for c1,c3 in zip(word[:-2], word[2:]):
        if c1 == c3:
            return True
    return False

def check_nice(word):
    return check_nice_rule1(word) and check_nice_rule2(word)

def main():
    input_path = sys.argv[1]
    total = sum(check_nice(w) for w in read_input(input_path))
    print(total)

if __name__ == "__main__":
    main()
