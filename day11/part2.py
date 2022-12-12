#!/usr/bin/env python3
from pathlib import Path
from dataclasses import dataclass
from collections.abc import Callable
from pprint import pprint

@dataclass
class DivisionTest:
    divident: int
    right: int
    wrong: int

@dataclass
class Monkey:
    inventory: list[int]
    operation: Callable[[int], int]
    test: DivisionTest
    inspection_count: int = 0


def run_test(i: int, test: DivisionTest):
    if i % test.divident == 0:
        return test.right
    return test.wrong

def parse_monkey(monkey_text: str):
    data = monkey_text.split('\n')
    inventory = eval(data[1].split(': ')[1])
    if isinstance(inventory, int):
        inventory = [inventory]
    else:
        inventory = list(inventory)
    operation = data[2].split(' = ')[1]
    test_lines = data[3:]
    test_divident = int(test_lines[0].split(' ')[-1])
    test_right = int(test_lines[1].split(' ')[-1])
    test_wrong = int(test_lines[2].split(' ')[-1])
    test = DivisionTest(test_divident, test_right, test_wrong)
    return Monkey(inventory, lambda old: eval(operation), test)

def monkey_inspect(monkey: Monkey, all_monkeys: list[Monkey]):
    while monkey.inventory:
        item = monkey.inventory.pop(0)
        item = int(monkey.operation(item))
        answer = run_test(item, monkey.test)
        all_monkeys[answer].inventory.append(item)
        monkey.inspection_count += 1

def do_round(monkeys: list[Monkey]):
    for monkey in monkeys:
        monkey_inspect(monkey, monkeys)

def create_monkeys(file: str):
    monkeys: list[Monkey] = []
    with open(file) as f:
        data = f.read().split('\n\n')
        for d in data:
            monkey = parse_monkey(d)
            monkeys.append(monkey)
    return monkeys

def get_highest_monkey_inspections(monkeys: list[Monkey], amount: int):
    inspections = [m.inspection_count for m in monkeys]
    inspections.sort(reverse=True)
    return inspections[:amount]

def get_monkey_shenanigans(monkeys: list[Monkey]):
    m = get_highest_monkey_inspections(monkeys, 2)
    return m[0] * m[1]

if __name__ == '__main__':
    input_file = Path(__file__).parent / 'example.txt'
    monkeys = create_monkeys(input_file)
    pprint(monkeys)
    for i in range(10000):
        do_round(monkeys)
        print(i)
    monkey_shenanigans = get_monkey_shenanigans(monkeys)
    print(monkey_shenanigans)
    
