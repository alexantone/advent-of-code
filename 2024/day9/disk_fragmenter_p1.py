#!/bin/env python3
"""Day 9: Disk Fragmenter P1"""

import sys
import numpy as np

EMPTY_BLOCK_ID = -1

def read_input(path):
    with open(path, mode="r", encoding="utf-8") as fp:
        return  [int(d) for d in fp.read()]

def render_disk(disk_layout):
    disk_size = sum(disk_layout)

    disk = np.zeros(disk_size, dtype="int")
    pos = 0
    for ix, nb in enumerate(disk_layout):
        if ix % 2 == 0:
            disk[pos:pos+nb] = ix / 2
        else:
            disk[pos:pos+nb] = EMPTY_BLOCK_ID
        pos += nb

    return disk

def compact_disk(disk):
    r, l = 0, len(disk)-1
    while r < l:
        while r < l and disk[r] != EMPTY_BLOCK_ID:
            r += 1
        while r < l and disk[l] == EMPTY_BLOCK_ID:
            l -= 1
        while r < l and disk[r] == EMPTY_BLOCK_ID and disk[l] != EMPTY_BLOCK_ID:
            disk[r], disk[l] = disk[l], disk[r]
            r, l = r+1, l-1
    return disk

def checksum(disk):
    return sum(ix*id for ix,id in enumerate(disk) if id != EMPTY_BLOCK_ID)

def main():
    input_path = sys.argv[1]
    disk_layout = read_input(input_path)
    disk = render_disk(disk_layout)
    disk = compact_disk(disk)
    chksum = checksum(disk)
    print(chksum)


if __name__ == "__main__":
    main()
