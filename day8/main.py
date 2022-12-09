#!/usr/bin/env python3
from pathlib import Path
from pprint import pprint

# Number represents a tree height
# 0 shortest, 9 tallest

# Only look up, down, left, right
#       ^
#       |
#     <-T->
#       |
#       v

def read_tree_map(file_path):
    tree_map = []
    with open(file_path) as f:
        for line in f:
            tree_row = list(map(int, line.strip('\n')))
            tree_map.append(tree_row)
    return tree_map

def is_tree_visible(row, col, tree_map: list[list[int]]):
    size = tree_map[row][col]
    tree_map_col = [t[col] for t in tree_map]
    left = max(tree_map[row][:col]) < size
    right = max(tree_map[row][col+1:]) < size
    up = max(tree_map_col[:row]) < size
    down = max(tree_map_col[row+1:]) < size
    return left or right or up or down

def scenic_score(row, col, tree_map: list[list[int]]):
    size = tree_map[row][col]
    tree_map_col = [t[col] for t in tree_map]
    left = 0
    right = 0
    up = 0
    down = 0
    for t in reversed(tree_map[row][:col]):
        left += 1
        if t >= size:
            break
    for t in tree_map[row][col+1:]:
        right += 1
        if t >= size:
            break
    for t in reversed(tree_map_col[:row]):
        up += 1
        if t >= size:
            break
    for t in tree_map_col[row+1:]:
        down += 1
        if t >= size:
            break
    return left * right * up * down

def count_visible_trees(tree_map: list[list[int]]):
    row_len = len(tree_map)
    col_len = len(tree_map[0])
    counter = 0
    highest_scenic_score = 0
    for row in range(1, row_len-1):
        for col in range(1, col_len-1):
            visible = is_tree_visible(row, col, tree_map)
            score = scenic_score(row, col, tree_map)
            if highest_scenic_score < score:
                highest_scenic_score = score
            if (visible):
                counter += 1
    print(highest_scenic_score)
    return counter + row_len*2 + col_len*2 - 4


if __name__ == '__main__':
    input_file = Path(__file__).parent / 'input.txt'
    tree_map = read_tree_map(input_file)
    nr_of_visible_trees = count_visible_trees(tree_map)
    print(nr_of_visible_trees)