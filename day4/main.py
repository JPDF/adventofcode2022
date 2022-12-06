#!/usr/bin/env python3
from pathlib import Path

PARTIAL = 1
FULL = 2
input_file = Path(__file__).parent / 'input.txt'

def read_input(input_file):
    with open(input_file) as f:
        for line in f:
            s1, s2 = line.strip('\n').split(',')
            yield (
                tuple(map(int, s1.split('-'))), 
                tuple(map(int, s2.split('-')))
            )

def is_overlapping(l1, h1, l2, h2):
    if h1 >= l2 and h2 >= l1:
        if (l1 <= l2 and h1 >= h2) or (l2 <= l1 and h2 >= h1):
            return FULL
        return PARTIAL
    return 0

if __name__ == '__main__':
    pairs = read_input(input_file)
    nr_of_full_overlap = 0
    nr_of_overlap = 0
    for pair in pairs:
        overlap = is_overlapping(*pair[0], *pair[1])
        if overlap == FULL:
            nr_of_full_overlap += 1;
        if overlap:
            nr_of_overlap += 1
    print(f'full overlaps: {nr_of_full_overlap}')
    print(f'total overlaps: {nr_of_overlap}')
