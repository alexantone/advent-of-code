#!/bin/env python3
"""Day 5: Print Queue P2"""

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

def reorder_update(update, rules):
    """Function assumes reordering is possible (i.e. no cycles in the rules)

    Gives up after n*(n-1)/2 (O(n^2))
    """
    invalid = True
    reordered = update[:]  # Make copy of original update
    max_tries = len(update) * (len(update) - 1) / 2 # Max reordering tries O(n^2)
    n = 0

    while invalid and n < max_tries:
        invalid = False
        for ix, page in enumerate(reordered):
            for jx, other in enumerate(reordered[:ix]):
                if other in rules[page]:
                    reordered[ix], reordered[jx] = other, page
                    n += 1
                    invalid = True
                    break
            if invalid:
                break

    return reordered, not invalid

def main():
    input_path = sys.argv[1]
    rules, updates = read_input(input_path)

    total = 0
    invalid_updates = [u for u in updates if not is_valid(u, rules)]

    for update in invalid_updates:
        reordered, valid = reorder_update(update, rules)
        if not valid:
            print("STILL NOT VALID?!")
            continue

        total += int(reordered[len(reordered) // 2])

    print(total)


if __name__ == "__main__":
    main()
