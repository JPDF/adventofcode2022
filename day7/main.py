#!/usr/bin/env python3
from pathlib import Path
from pprint import pprint

CURRENT_DIRS = []
DIR_SIZES = {}

def change_dir(dir: str):
    if dir == '..':
        CURRENT_DIRS.pop()
    else:
        CURRENT_DIRS.append(dir)

total_size = 0
input_file = Path(__file__).parent / 'input.txt'
with open(input_file) as f:
    for line in f:
        args = line.strip('\n').split(' ')
        if args[0] == '':
            break
        elif args[0] == '$':
            l = len(CURRENT_DIRS)
            for i in range(l):
                current_path = '/'.join(CURRENT_DIRS[:l-i])
                if not current_path in DIR_SIZES:
                    DIR_SIZES[current_path] = total_size
                else:
                    DIR_SIZES[current_path] += total_size
            total_size = 0
            if args[1] == 'cd':
                change_dir(args[2])
        elif args[0] != 'dir':
            total_size += int(args[0])

pprint(DIR_SIZES)
total = 0
for size in DIR_SIZES.values():
    if size <= 100000:
        total += size
print(total)

TOTAL_SPACE = 70000000
UPDATE_SPACE = 30000000

used_space = DIR_SIZES['/']
unused_space = TOTAL_SPACE - used_space
print(unused_space)
for size in sorted(DIR_SIZES.values()):
    if unused_space + size >= UPDATE_SPACE:
        print(size)
        break
