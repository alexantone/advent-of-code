#!/bin/env python3
"""Day 5: Print Queue P1"""

import sys
from collections import defaultdict

def read_input(path):
    rules = defaultdict(set)
    updates = []
    rules_ended = False
    with open(path, mode="r", encoding="utf-8") as fp:
        for line in fp.readlines():
            line = line.strip()
            if not line:
               rules_ended = True
               continue

            # Can still keep anything as strings for now
            if not rules_ended:
                a,b = line.split('|')
                rules[a].add(b)
            else:
                 updates.append(line.split(','))

        return rules, updates

def is_valid(update, rules):
    for ix, page in enumerate(update):
        for other in update[:ix]:
            if other in rules[page]:
                return False
    return True

def main():
    input_path = sys.argv[1]
    rules, updates = read_input(input_path)

    total = 0
    for update in updates:
        if is_valid(update, rules):
            total += int(update[len(update) // 2])

    print(total)


if __name__ == "__main__":
    main()
