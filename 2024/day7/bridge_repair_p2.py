#!/bin/env python3
"""Day 7: Bridge Repair P2"""

import sys
import re


OP_MAP = {
    0: '+',
    1: '*',
    2: '||',
}

def fmt_operators(operators):
    return [OP_MAP[o] for o in operators]

def dec_to_b3(n):
    if n == 0:
        return [0,]

    digits = []
    while n:
        digits.append(n % 3)
        n //= 3
    return digits[-1::-1]

def ints(s: str):
    return [int(n) for n in re.findall(r"-?\d+", s)]

def read_input(path):
    with open(path, mode="r", encoding="utf-8") as fp:
        eqs = [ints(l) for l in fp.readlines()]
        eqs = [(e[0], e[1:]) for e in eqs]
        return eqs

def check_equation(equation):
    result, coefs = equation

    start = 3 ** (len(coefs) - 1)
    stop =  2 * start

    for ix in range(start, stop):
        total = coefs[0]
        operators = dec_to_b3(ix)[1:]

        for op, coef in zip(operators, coefs[1:]):
            if op == 0:
                total += coef
            elif op == 1:
                total *= coef
            elif op == 2:
                total = int(f"{total}{coef}")

        if total == result:
            print(f"{result} {coefs} {fmt_operators(operators)}")
            return result

    return 0


def main():
    input_path = sys.argv[1]
    equations = read_input(input_path)
    print(sum(check_equation(eq) for eq in equations))

if __name__ == "__main__":
    main()
