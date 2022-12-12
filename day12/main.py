from pathlib import Path
from pprint import pprint
from dataclasses import dataclass
import math
from typing import Callable

@dataclass(eq=True, frozen=True)
class Point:
    x: int
    y: int
    
    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y

@dataclass(eq=True, frozen=True)
class FScorePoint:
    fscore: int
    point: Point
    
    def __eq__(self, __o: object) -> bool:
        return self.point == __o

def parse_heightmap(map_data: list[str]):
    height_map = []
    for line in map_data:
        row = []
        for elevation in line:
            row.append(ord(elevation))
        height_map.append(row)
    return height_map

def find_location(heightmap: list[str], char: str):
    for y in range(len(heightmap)):
        x = heightmap[y].find(char)
        if x != -1:
            return Point(x, y)

def read_input(input_file: str):
    with open(input_file) as f:
        data = [d.strip('\n') for d in f.readlines()]
        start = find_location(data, 'S')
        end = find_location(data, 'E')
        
        data[start.y] = data[start.y].replace('S', 'a')
        data[end.y] = data[end.y].replace('E', 'z')
        heightmap = parse_heightmap(data)
    return heightmap, start, end

def heuristic(start: Point, end: Point):
    return math.dist((start.x, start.y), (end.x, end.y))

def print_map(m):
    for r in m:
        if isinstance(r[0], int):
            print(''.join(map(str, r)).replace('-1','i'))
        else:
            print(''.join(r))
    print()

def plan_path(heightmap: list[int], start: Point, end: Point, h: Callable[[Point], float]):
    def neighbours(p: Point):
        for i, j in enumerate([-1, 1, -1, 1]):
            if i >= 2:
                new_x = p.x+j
                if 0 <= new_x < map_width:
                    yield Point(new_x, p.y)
            else:
                new_y = p.y+j
                if 0 <= new_y < map_height:
                    yield Point(p.x, new_y)
    def reconstruct_path(came_from: dict, current):
        path = [current]
        while current in came_from.keys():
            current = came_from[current]
            path.append(current)
        return path
    open_set = [FScorePoint(0, start)]
    came_from = {}
    map_width = len(heightmap[0])
    map_height = len(heightmap)
    
    gscore = [[-1 for _ in range(map_width)] for _ in range(map_height)]
    gscore[start.y][start.x] = 0
    
    while len(open_set) > 0:
        current = open_set.pop(0).point
        if current == end:
            print('Path found!')
            return reconstruct_path(came_from, current)
        for neighbour in neighbours(current):
            height_diff = heightmap[neighbour.y][neighbour.x] - heightmap[current.y][current.x]
            if height_diff > 1:
                continue
            # distance is always 1 to neighbour
            tentative_gscore = gscore[current.y][current.x] + 1
            neighbour_gscore = gscore[neighbour.y][neighbour.x]
            if tentative_gscore < neighbour_gscore or neighbour_gscore == -1:
                came_from[neighbour] = current
                gscore[neighbour.y][neighbour.x] = tentative_gscore
                if neighbour not in open_set:
                    fscore = tentative_gscore + h(neighbour)
                    new_point = FScorePoint(fscore, neighbour)
                    open_set.append(new_point)
        open_set.sort(key=lambda p: p.fscore)
    print('Path not found!')

if __name__ == '__main__':
    input_file = Path(__file__).parent / 'input.txt'
    heightmap, start, end = read_input(input_file)
    # Print map to file
    with open('map.txt', 'w') as f:
        for r in heightmap:
            f.write(''.join(map(chr,r)) + '\n')
    print(start)
    print(end)
    h = lambda p: heuristic(p, end)
    path = plan_path(heightmap, start, end, h)
    print(path)
    print(len(path)-1)
    
    shortest_path = -1
    for i in range(len(heightmap)):
        start = Point(1, i)
        path = plan_path(heightmap, start, end, h)
        path_length = len(path)
        if shortest_path == -1 or path_length < shortest_path:
            shortest_path = path_length
    print(shortest_path)
    
    
