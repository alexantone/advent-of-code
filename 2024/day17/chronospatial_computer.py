#!/bin/env python3
"""Day 17: Chronospatial Computer P1,P2"""

import sys
import re


def ints(s: str):
    return [int(n) for n in re.findall(r"-?\d+", s)]

def read_input(path):
    with open(path, mode="r", encoding="utf-8") as f:
        registers, program = f.read().split('\n\n')
        return ints(registers), ints(program)

class Instructions():
    @staticmethod
    def combo_operand(v, registers):
        return v if v <= 3 else registers[v%4]

    @staticmethod
    def adv(v, registers, pc):
        A,B,C = registers
        A = A // (2**Instructions.combo_operand(v, registers))
        return ((A,B,C), pc+2, None)

    @staticmethod
    def bxl(v, registers, pc):
        A,B,C = registers
        B ^= v
        return ((A,B,C), pc+2, None)

    @staticmethod
    def bst(v, registers, pc):
        A,B,C = registers
        B = Instructions.combo_operand(v, registers) % 8
        return ((A,B,C), pc+2, None)

    @staticmethod
    def jnz(v, registers, pc):
        A,B,C = registers
        return (registers, pc+2, None) if A == 0 else (registers, v, None)

    @staticmethod
    def bxc(v, registers, pc):
        A,B,C = registers
        B ^= C
        return ((A,B,C), pc+2, None)

    @staticmethod
    def out(v, registers, pc):
        A,B,C = registers
        out_v = Instructions.combo_operand(v, registers) % 8
        return ((A,B,C), pc+2, out_v)

    @staticmethod
    def bdv(v, registers, pc):
        A,B,C = registers
        B = A // (2**Instructions.combo_operand(v, registers))
        return ((A,B,C), pc+2, None)

    @staticmethod
    def cdv(v, registers, pc):
        A,B,C = registers
        C = A // (2**Instructions.combo_operand(v, registers))
        return ((A,B,C), pc+2, None)

OPCODES_MAP = {
    0: Instructions.adv,
    1: Instructions.bxl,
    2: Instructions.bst,
    3: Instructions.jnz,
    4: Instructions.bxc,
    5: Instructions.out,
    6: Instructions.bdv,
    7: Instructions.cdv,
}

def execute(registers, pc, program, output: list):
    allowed_pc = len(program) - 2

    while pc <= allowed_pc:
        instr_code, operand = program[pc:pc + 2]
        registers, pc, out_val = (OPCODES_MAP[instr_code])(operand, registers, pc)

        if out_val is not None:
            output.append(out_val)

    return output

def execute_check_output(registers, pc, program, output: list):
    """Runs progam up until the output diverges"""
    allowed_pc = len(program) - 2
    while pc <= allowed_pc:
        instr_code, operand = program[pc:pc + 2]
        registers, pc, out_val = (OPCODES_MAP[instr_code])(operand, registers, pc)

        if out_val is not None:
            output.append(out_val)
            if len(output) > len(program):  # Output exceeds program length
                break
            if out_val != program[len(output) - 1]:  # Divergence point abort
                break

    return output

MAX_BINARY_DIGITS=100

def analyze_bit_patterns(values):
    """"Finds common bits between values producing a common prefix length of the program"""
    binary_vals = [f"{bin(v)[2:]:>{MAX_BINARY_DIGITS}}" for v in values]

    bitmask=""
    for digits in zip(*binary_vals):
        digits = ''.join(digits)
        if '1' in digits and '0' in digits:
            bitmask += '_'
        else:
            digits = digits.strip() + ' '
            bitmask += digits[0]

    bitmask = bitmask.strip()[1:] # Ignore first bit since we don't have enough info to be certain

    # Print some analysis
    # for b in binary_vals:
    #     print(b)
    print(f"{bitmask:>{MAX_BINARY_DIGITS}}")

    return bitmask

def transform(val, bitmask):
    """
    Shoves bits of A into a new value using the bitmask as fixed bits
    Example: for val=7 (0b111) and bitmask='01_1'
        value:   11  1
        mask:    __01_0
        result:  110110
    """

    val = f"{bin(val + (1 << MAX_BINARY_DIGITS))}"[3:]

    k = 0
    res = []
    for m in reversed(bitmask):
        if m == '_':
            k += 1
            res.append(val[-k])
        else:
            res.append(m)

    for j in range(k+1, len(val) + 1):
        res.append(val[-j])

    res = ''.join(reversed(res))
    return int(res, 2)


def solve(registers, program):
    bitmask='_' # Starting mask
    starting_prefix_len = 1
    current_prefix_len = starting_prefix_len
    values_to_analyze = 1 << 7 # Heuristic: adds 7 extra bits of information each round
    give_up_iters = 1 << 20
    found = False
    masks = []

    while current_prefix_len <= len(program) and not found:
        ix = 0
        values = []

        # Collect at least values_to_analyze values to perform analysis on
        print(f"Collecting {values_to_analyze} values,  {current_prefix_len=} -> ", end="")
        while len(values) < values_to_analyze and ix < give_up_iters:
            A = transform(ix, bitmask)
            registers[0] = A
            output = execute_check_output(registers, 0, program, [])

            if output == program:
                found = True
                break

            common_prefix_len = len(output) - 1
            if common_prefix_len >= current_prefix_len:
                values.append(A)

            ix += 1

        if not found:
            # Perform analysis on collected values and return new bitmask
            print(f"iterations={ix}, {len(values)} values")
            bitmask = analyze_bit_patterns(values)
            masks.append(bitmask)
            current_prefix_len += 1

    print(f"\n{found=}")

    # Print mask evolution:
    for ix, mask in enumerate(masks, start=starting_prefix_len):
        print(f"Mask for prefix len {ix:>2}: {mask:>{MAX_BINARY_DIGITS}}")
    return A, output


def main():
    input_path = sys.argv[1]
    registers, program = read_input(input_path)
    print(f"{registers=}")
    print(f"{program=}")

    p1_solution = ",".join(str(x) for x in execute(registers, 0, program, []))
    p2_solution, output = solve(registers, program)

    print(f"P1: {p1_solution}")
    print(f"P2: {p2_solution} {output=} {len(output)}\n")


if __name__ == "__main__":
    main()
