#!/usr/bin/env python3
from pathlib import Path
from dataclasses import dataclass
from copy import deepcopy
from pprint import pprint

@dataclass
class Procedure:
    move_count: int
    source: int
    target: int
    
    def __repr__(self) -> str:
        return f'move {self.move} from {self.source} to {self.target}'

def read_input(input_file):
    def parse_procedures(procedure_data):
        for line in procedure_data.splitlines():
            a = list(map(int, line.split(' ')[1::2]))
            a[1] -= 1
            a[2] -= 1
            yield Procedure(*a)
    def parse_stacks(stacks_data):
        data = stacks_data.splitlines()
        data_idx = data.pop()
        nr_of_stacks = len(data_idx) - data_idx.count(' ')
        stacks = [''] * nr_of_stacks
        for d in data:
            for i in range(nr_of_stacks):
                c = d[4*i+1]
                if c != ' ':
                    stacks[i] += c
        return stacks

    with open(input_file) as f:
        data = f.read()
    stacks_data, procedure_data = data.split('\n\n', 2)
    procedures = parse_procedures(procedure_data)
    stacks = parse_stacks(stacks_data)
    pprint(procedures)
    pprint(stacks)
    return stacks, procedures

def move_crates(stacks: list[str], source, target, amount):
    cargo = stacks[source][:amount]
    stacks[target] = cargo + stacks[target]
    stacks[source] = stacks[source][amount:]

def run_procedure_9000(stacks: list[str], procedure: Procedure):
    for i in range(procedure.move_count):
        move_crates(stacks, procedure.source, procedure.target, 1)

def run_procedure_9001(stacks: list[str], procedure: Procedure):
    move_crates(stacks, procedure.source, procedure.target, procedure.move_count)

input_file = Path(__file__).parent / 'input.txt'
stacks_9000, procedures = read_input(input_file)
stacks_9001 = deepcopy(stacks_9000)
for procedure in procedures:
    run_procedure_9000(stacks_9000, procedure)
    run_procedure_9001(stacks_9001, procedure)
print(''.join([s[0] for s in stacks_9000[:]]))
print(''.join([s[0] for s in stacks_9001[:]]))
