#!/usr/bin/env python3
from pathlib import Path
from dataclasses import dataclass
import math
from copy import copy

DIRECTION_TABLE = {
    'R': 1,
    'L': -1,
    'U': 2,
    'D': -2
}

@dataclass
class Motion:
    direction: int
    steps: int

@dataclass
class Coordinate:
    x: int
    y: int
    
    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))

class Rope:
    
    def __init__(self, head: Coordinate, length: int) -> None:
        self.segments: list[Coordinate] = []
        for _ in range(length):
            self.segments.append(copy(head))
        self.head = self.segments[0]
        self.tail = self.segments[-1]
        self.length = length
        self.tail_path = []
        self.tail_path.append(copy(self.segments[-1]))
        self.path = []
    
    def step(self, direction: int):
        move_horizontal = abs(direction) == 1
        magnitude = math.copysign(1, direction)
        if move_horizontal:
            self.head.x += magnitude
        else:
            self.head.y += magnitude
        for i in range(1, len(self.segments)):
            update_segment(self.segments[i-1], self.segments[i])
        if self.tail not in self.tail_path:
            self.tail_path.append(copy(self.tail))

    def move(self, motion: Motion):
        for _ in range(motion.steps):
            self.step(motion.direction)

def read_motions(input_file: str):
    with open(input_file) as f:
        for line in f:
            direction, steps = line.strip('\n').split(' ')
            yield Motion(DIRECTION_TABLE[direction], int(steps))


def update_segment(head: Coordinate, tail: Coordinate):
    head_set = (head.x, head.y)
    tail_set = (tail.x, tail.y)
    dist = math.dist(head_set, tail_set)
    if math.floor(dist) > 1:
        left = (head_set[0]-1, head_set[1])
        right = (head_set[0]+1, head_set[1])
        up = (head_set[0], head_set[1]+1)
        down = (head_set[0], head_set[1]-1)
        left_dist = math.dist(tail_set, left)
        right_dist = math.dist(tail_set, right)
        up_dist = math.dist(tail_set, up)
        down_dist = math.dist(tail_set, down)
        dists = [left_dist, right_dist, up_dist, down_dist]
        coords = [left, right, up, down]
        min_dist = min(dists)
        min_index = dists.index(min_dist)
        res = coords[min_index]
        # åh nej
        if min_dist > 2:
            min_dist = -1
            for i in [-1, 1]:
                for j in [-1, 1]:
                    c = (head_set[0]+i, head_set[1]+j)
                    d = math.dist(tail_set, c)
                    if d < min_dist or min_dist == -1:
                        min_dist = d
                        res = c
        tail.x = res[0]
        tail.y = res[1]
        

def run_motions(rope: Rope, motions: list[Motion]):
    for motion in motions:
        rope.move(motion)
    print(len(rope.tail_path))

def show_tail_movement(rope: Rope):
    tail_path = rope.tail_path
    _x = [p.x for p in tail_path]
    _y = [p.y for p in tail_path]
    min_x = min(_x)
    min_y = min(_y)
    __x = [int(x - min_x) for x in _x]
    __y = [int(y - min_y) for y in _y]
    max_x = max(__x)
    max_y = max(__y)
    m = []
    for i in range(max_y+1):
        m.append([])
        for j in range(max_x+1):
            m[i].append('.')
    for i in range(len(tail_path)):
        m[__y[i]][__x[i]] = '#'
    m[__y[0]][__x[0]] = 'S'
    m[__y[-1]][__x[-1]] = 'T'
    with open('map.txt', 'w') as f:
        for i in reversed(range(len(m))):
            f.write(''.join(m[i]) + '\n')


def show_movement(rope: Rope):
    tail_path = rope.tail_path
    _x = [p.x for p in tail_path]
    _y = [p.y for p in tail_path]
    min_x = min(_x)
    min_y = min(_y)
    __x = [int(x - min_x) for x in _x]
    __y = [int(y - min_y) for y in _y]
    max_x = max(__x)
    max_y = max(__y)
    m = []
    for i in range(max_y+1):
        m.append([])
        for _ in range(max_x+1):
            m[i].append('.')
    for i in range(len(tail_path)):
        m[__y[i]][__x[i]] = '#'
    m[__y[0]][__x[0]] = 'S'
    m[__y[-1]][__x[-1]] = 'T'
    with open('map.txt', 'w') as f:
        for i in reversed(range(len(m))):
            f.write(''.join(m[i]) + '\n')
    

if __name__ == '__main__':
    input_file = Path(__file__).parent / 'input.txt'
    motions = read_motions(input_file)
    rope = Rope(Coordinate(0, 0), length=10)
    run_motions(rope, motions)
    show_tail_movement(rope)
