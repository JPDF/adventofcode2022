#!/usr/bin/env python3
from pathlib import Path


ROOT = Path(__file__).parent
TOP = 3

input_file = ROOT / 'input.txt'

elves_calories = []
elve_total = 0
with open(input_file) as f:
    for line in f:
        if not line or line == '\n':
            elves_calories.append(elve_total)
            elve_total = 0
            continue
        elve_total += int(line)

elves_calories.sort(reverse=True)
total = sum(elves_calories[:TOP])
print(total)
