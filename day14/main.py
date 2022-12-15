#!/usr/bin/env python3
from pathlib import Path
from dataclasses import dataclass
from pprint import pprint
from math import copysign
from copy import copy

ICONS = {
    0: '.',
    1: '#',
    2: 'o',
    3: '+',
    4: '~'
}

@dataclass
class Point:
    x: int
    y: int

def parse_line(line: str):
    split_line = line.split(' -> ')
    points = []
    for p in split_line:
        points.append(Point(*map(int, p.split(','))))
    return points

def read_input(input_file: str):
    with open(input_file) as f:
        shapes = []
        for line in f:
            shapes.append(parse_line(line))
        return shapes
            
def build_map(shapes: list[list[Point]], sand_point: Point, add_floor: bool = False):
    all_points = [point for shape in shapes for point in shape]
    all_points.append(sand_point)
    all_x = [point.x for point in all_points]
    all_y = [point.y for point in all_points]
    min_x = min(all_x)
    max_x = max(all_x)
    min_y = min(all_y)
    max_y = max(all_y)
    map = []
    for i in range(max_y - min_y+1):
        map.append([])
        for _ in range(max_x - min_x+1):
            map[i].append(0)
    for point in all_points:
        point.x -= min_x
        point.y -= min_y
    for shape in shapes:
        for i in range(1,len(shape)):
            from_point = shape[i-1]
            to_point = shape[i]
            sorted_x = sorted([from_point.x, to_point.x])
            sorted_x[1] += 1
            sorted_y = sorted([from_point.y, to_point.y])
            sorted_y[1] += 1
            for x in range(*sorted_x):
                map[from_point.y][x] = 1
            for y in range(*sorted_y):
                map[y][from_point.x] = 1
    map[sand_point.y][sand_point.x] = 3
    if add_floor:
        row = [0 for _ in range(len(map[0]))]
        floor = [1 for _ in range(len(map[0]))]
        map.append(row)
        map.append(floor)
    return map

def widen_map(map: list[list[int]]):
    height = len(map)
    col = [0 for _ in range(height)]
    col[-1] = 1
    for row in map:
        row.insert(0, 0)
        row.append(0)
    if all(c is 1 for c in map[-1][1:-1]):
        map[-1][0] = 1
        map[-1][-1] = 1

def draw_map(map):
    for row in map:
        for col in row:
            print(ICONS[col], end='')
        print()

def get_free_diagonal(map, point: Point):
    if point.x-1 < 0 or point.x+1 >= len(map[0]):
        widen_map(map)
        point.x += 1
    if not map[point.y+1][point.x-1]:
        return point.x-1
    elif not map[point.y+1][point.x+1]:
        return point.x+1
    return None

def produce_sand(map: list[list[int]], sand_point: Point):
    trace = []
    current_x = sand_point.x
    for y, row in enumerate(map[1:]):
        current_point = Point(current_x, y)
        trace.append(current_point)
        if row[current_x]:
            diag = get_free_diagonal(map, current_point)
            sand_point.x = map[0].index(3) # Update sand_point
            if diag is None:
                return current_point, trace
            else:
                current_x = diag
    return None, trace
            

def fill_with_sand(map, sand_point: Point):
    sand_count = 0
    while True:
        sand, trace = produce_sand(map, sand_point)
        if sand is None:
            for p in trace:
                map[p.y][p.x] = 4
            break
        sand_count += 1
        if sand.x == sand_point.x and sand.y == sand_point.y:
            break
        map[sand.y][sand.x] = 2
    return sand_count
        
    

if __name__ == '__main__':
    input_file = Path(__file__).parent / 'input.txt'
    sand_point = Point(500, 0)
    shapes = read_input(input_file)
    map = build_map(shapes, sand_point)
    draw_map(map)
    sand_count = fill_with_sand(map, sand_point)
    print('-'*len(map[0]))
    draw_map(map)
    print(sand_count)
    
    print()
    map = build_map(shapes, sand_point, add_floor=True)
    draw_map(map)
    sand_count = fill_with_sand(map, sand_point)
    draw_map(map)
    print(sand_count)
