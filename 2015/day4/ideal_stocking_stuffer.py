#!/bin/env python3
"""Day 4: The Ideal Stocking Stuffer P1, P2"""

import hashlib

P1_REQ = "0" * 5
P2_REQ = "0" * 6

def md5_hash(s):
    return hashlib.md5(s.encode()).hexdigest()

def solve(key, req):
    n = 1
    while True:
        if md5_hash(f"{key}{n}").startswith(req):
            return n
        n += 1

def main():
    key = 'ckczppom'

    print(solve(key, P1_REQ))
    print(solve(key, P2_REQ))

if __name__ == "__main__":
    main()
