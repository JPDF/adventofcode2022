#!/usr/bin/env 
from pathlib import Path

# Opponent choices:
#   A: Rock
#   B: Paper
#   C: Scissors

# My choices:
#   X: Rock
#   Y: Paper
#   Z: Scissors

# Score is based on shape + outcome
# Outcome score:
#   lost: 0
#   draw: 3
#   won: 6
# Shape score:
#   Rock: 1
#   Paper: 2
#   Scissors: 3

# Score is based on my selection
SCORE_TABLE = {
    'rock': 1,
    'paper': 2,
    'scissors': 3,
    'lost': 0,
    'draw': 3,
    'win': 6
}

STRATEGY_TABLE = {
    'A': 'rock',
    'B': 'paper',
    'C': 'scissors',
    'X': 'rock',
    'Y': 'paper',
    'Z': 'scissors'
}

RULE_TABLE = {
    'rock': 'scissors',
    'scissors': 'paper',
    'paper': 'rock'
}

def read_strategy_guide(file_path: str):
    with open(file_path) as f:
        for line in f:
            a, b = line.strip('\n').split(' ')
            yield [STRATEGY_TABLE[a], STRATEGY_TABLE[b]]

def outcome(a: str, b: str):
    if a == b:
        return 'draw'
    elif RULE_TABLE[b] == a:
        return 'win'
    return 'lost'

def score(a: str, b: str):
    outcome_str = outcome(a, b)
    score_b = SCORE_TABLE[b]
    outcome_score = SCORE_TABLE[outcome_str]
    return score_b + outcome_score

input_file = Path(__file__, '..', 'input.txt')
strategy_guide = read_strategy_guide(input_file)

total = sum([score(*shapes) for shapes in strategy_guide])
print(total)
