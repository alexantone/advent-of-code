#!/bin/env python3
"""Day 5: Doesn't He Have Intern-Elves For This? P1"""

import sys


VOWELS = set("aeiou")
FORBIDDEN = set(tuple(s) for s in ["ab", "cd", "pq", "xy"])

def read_input(path):
    with open(path, mode="r", encoding="utf-8") as fp:
        return fp.read().splitlines()

def check_nice(word):
    n_vowels = 0
    doubled_letter = False

    n_vowels += word[0] in VOWELS
    for c1, c2 in zip(word[:-1], word[1:]):
        if (c1, c2) in FORBIDDEN:
            return False

        n_vowels += c2 in VOWELS
        if c1 == c2:
            doubled_letter = True

    return n_vowels >= 3 and doubled_letter

def main():
    input_path = sys.argv[1]
    total = sum(check_nice(w) for w in read_input(input_path))
    print(total)

if __name__ == "__main__":
    main()
