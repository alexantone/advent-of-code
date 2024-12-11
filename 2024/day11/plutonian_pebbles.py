#!/bin/env python3
"""Day 11: Plutonian Pebbles P1, P2"""

import sys
import functools

def read_input(path):
    with open(path, mode="r", encoding="utf-8") as fp:
        return [int(n) for n in fp.read().split()]

@functools.cache
def blink(stone, times):
    if times == 0:
        return 1

    end_stones = 0

    if stone == 0:
        end_stones += blink(1, times - 1)
    elif len(str(stone)) % 2 == 0:
        s = str(stone)
        end_stones += blink(int(s[:len(s)//2]), times - 1)
        end_stones += blink(int(s[len(s)//2:]), times - 1)
    else:
        end_stones += blink(stone * 2024, times - 1)

    return end_stones

def main():
    input_path = sys.argv[1]
    n_blinks = int(sys.argv[2])
    stones = read_input(input_path)

    print(sum(blink(s, n_blinks) for s in stones))


if __name__ == "__main__":
    main()
