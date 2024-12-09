#!/bin/env python3
"""Day 9: Disk Fragmenter P2"""

import sys
from collections import deque
import numpy as np

EMPTY_BLOCK_ID = -1

def read_input(path):
    with open(path, mode="r", encoding="utf-8") as fp:
        return  [int(d) for d in fp.read()]

def get_blocks(disk_layout):
    blocks = []
    for ix, num_blocks in enumerate(disk_layout):
        fid = int(ix/2)
        if ix % 2 == 0:
            blocks.append(deque([(fid, num_blocks),]))
        else:
            blocks.append(deque([(EMPTY_BLOCK_ID, num_blocks)]))
    return blocks

def compact_disk(blocks, disk_size):
    disk = np.zeros(disk_size, dtype="int")

    for blkid, block in reversed(list(enumerate(blocks))):
        fid, fsize = block[0]
        if fid == EMPTY_BLOCK_ID:
            continue
        for space in blocks[:blkid]:
            sid, ssize = space[EMPTY_BLOCK_ID]
            if sid != EMPTY_BLOCK_ID:
                continue
            if ssize >= fsize:
                # Move file
                space[EMPTY_BLOCK_ID] = (fid, fsize)
                space.append((EMPTY_BLOCK_ID, ssize - fsize))
                block[0] = (EMPTY_BLOCK_ID, fsize)
                break

    pos = 0
    for block in blocks:
        for fid, fsize in block:
            disk[pos:pos+fsize] = fid
            pos += fsize

    return disk

def checksum(disk):
    return sum(ix*id for ix,id in enumerate(disk) if id != EMPTY_BLOCK_ID)

def main():
    input_path = sys.argv[1]
    disk_layout = read_input(input_path)
    disk_size = sum(disk_layout)
    blocks = get_blocks(disk_layout)
    disk = compact_disk(blocks, disk_size)
    chksum = checksum(disk)
    print(chksum)


if __name__ == "__main__":
    main()
