#!/usr/bin/env python3
from pathlib import Path
from pprint import pprint

# Priority score:
#   a-z = 1-26
#   A-Z = 27-52
# Could use character keycodes for since they are alphabetically linear 
# "ord('a')"
#   a-z = 97-122
#   A-Z = 65-90

def parse_file(file_path: str):
    with open(file_path) as f:
        for line in f:
            line = line.strip('\n')
            compartment_size = int(len(line) / 2)
            yield (line[:compartment_size], line[compartment_size:])

def get_duplicates(c1: list, c2: list):
    dups = []
    for item in c1:
        if item not in dups and item in c2:
            dups.append(item)
    return dups

def find_errors(rucksack: tuple[str, str]):
    faulty_items = get_duplicates(rucksack[0], rucksack[1])
    return faulty_items

def get_priority(item: str):
    key_code = ord(item)
    x = 96 if item.islower() else 38
    return key_code - x

def get_priorities(items: str):
    return [get_priority(i) for i in items]

def get_badge(rucksacks: list[tuple[str, str]]):
    items_a = ''.join(rucksacks[0])
    items_b = ''.join(rucksacks[1])
    dups_ab = get_duplicates(items_a, items_b)
    items_c = ''.join(rucksacks[2])
    dups_bc = get_duplicates(items_c, dups_ab)
    return dups_bc[0]

input_file = Path(__file__).parent / 'input.txt'
rucksacks = list(parse_file(input_file))

total = 0
for rucksack in rucksacks:
    errors = find_errors(rucksack)
    priorities = get_priorities(errors)
    total += sum(priorities)
print(f'Total error priority: {total}')

RUCKSACKS_PER_GROUP = 3
total = 0
for i in range(0,len(rucksacks), RUCKSACKS_PER_GROUP):
    badge = get_badge([
        rucksacks[i],
        rucksacks[i+1],
        rucksacks[i+2]
    ])
    total += get_priority(badge)
print(f'Total badge priority: {total}')
