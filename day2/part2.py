#!/usr/bin/env python3
from pathlib import Path

# Opponent choices:
#   A: Rock
#   B: Paper
#   C: Scissors

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
}

# Rock beats scissors, scissors beats paper, paper beats rock 
RULE_TABLE = {
    'rock': 'scissors',
    'scissors': 'paper',
    'paper': 'rock'
}

def read_strategy_guide(file_path: str):
    with open(file_path) as f:
        for line in f:
            a, b = line.strip('\n').split(' ')
            yield [STRATEGY_TABLE[a], b]

def outcome(opponent: str, reponse: str):
    if opponent == reponse:
        return 'draw'
    elif RULE_TABLE[reponse] == opponent:
        return 'win'
    return 'lost'

def response(opponent_shape: str, strategy: str):
    if strategy == 'Y':
        return opponent_shape
    elif strategy == 'X':
        return RULE_TABLE[opponent_shape]
    return list(RULE_TABLE.keys())[list(RULE_TABLE.values()).index(opponent_shape)]

def score(a: str, b: str):
    res = response(a, b)
    outcome_str = outcome(a, res)
    score_b = SCORE_TABLE[res]
    outcome_score = SCORE_TABLE[outcome_str]
    return score_b + outcome_score

input_file = Path(__file__, '..', 'input.txt')
strategy_guide = read_strategy_guide(input_file)

total = sum([score(*shapes) for shapes in strategy_guide])
print(total)
