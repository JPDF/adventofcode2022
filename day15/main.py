#!/usr/bin/env python3
from pathlib import Path
from dataclasses import dataclass
from pprint import pprint
import re



@dataclass
class Point:
    x: int
    y: int

@dataclass
class Sensor:
    position: Point
    closest_beacon: Point
    sensor_range: int

@dataclass
class Boundary:
    min_point: Point
    max_point: Point

def manhattan(a: Point, b: Point):
    return abs(a.x-b.x) + abs(a.y-b.y)

def get_coverage_boundary(sensors: list[Sensor]):
    min_x = min([s.position.x-s.sensor_range for s in sensors])
    min_y = min([s.position.y-s.sensor_range for s in sensors])
    max_x = max([s.position.x+s.sensor_range for s in sensors])
    max_y = max([s.position.y+s.sensor_range for s in sensors])
    return Boundary(Point(min_x, min_y), Point(max_x+1, max_y+1))

def parse_input_line(line: str):
    coords = list(map(int, re.findall(r'=(-?\d+)', line)))
    sensor_point = Point(*coords[:2])
    beacon_point = Point(*coords[2:])
    sensor_range = manhattan(sensor_point, beacon_point)
    return Sensor(sensor_point, beacon_point, sensor_range)

def read_input(input_file):
    sensors = []
    with open(input_file) as f:
        for line in f:
            sensor = parse_input_line(line)
            sensors.append(sensor)
    return sensors

def is_in_sensor_range(sensor: Sensor, point: Point):
    return manhattan(sensor.position, point) <= sensor.sensor_range

def is_in_any_sensor_range(sensors: list[Sensor], point: Point):
    for sensor in sensors:
        if is_in_sensor_range(sensor, point):
            return True
    return False

def get_unique_beacons(sensors: list[Sensor]):
    unique_beacons = []
    for sensor in sensors:
        if sensor.closest_beacon not in unique_beacons:
            unique_beacons.append(sensor.closest_beacon)
    return unique_beacons

def count_coverage_at_row(sensors: list[Sensor], y: int, boundary: Boundary):
    counter = 0
    for x in range(boundary.min_point.x, boundary.max_point.x):
        current_position = Point(x, y)
        if is_in_any_sensor_range(sensors, current_position):
            counter += 1
    beacons = get_unique_beacons(sensors)
    for beacon in beacons:
        if beacon.y == y:
            counter -= 1
    return counter

def get_right_sensor_edge_at_row(sensor: Sensor, y: int):
    dy = abs(sensor.position.y - y)
    return Point(sensor.position.x+sensor.sensor_range-dy, y)
    

def find_distress_beacon(sensors: list[Sensor], boundary: Boundary):
    current_point = Point(boundary.min_point.x, boundary.min_point.y)
    while True:
        found = False
        for sensor in sensors:
            if is_in_sensor_range(sensor, current_point):
                current_point = get_right_sensor_edge_at_row(sensor, current_point.y)
                current_point.x += 1
                found = True
                if current_point.x >= boundary.max_point.x:
                    current_point.y += 1
                    current_point.x = boundary.min_point.x
                break
        if current_point.y >= boundary.max_point.y:
            print('Failed to find distress beacon!')
            break
        elif not found:
            return current_point
                    
        if not found:
            return current_point

if __name__ == '__main__':
    input_file = Path(__file__).parent / 'input.txt'
    sensors = read_input(input_file)
    boundary = get_coverage_boundary(sensors)
    pprint(boundary)
    pprint(sensors)
    # Part 1
    #print(count_coverage_at_row(sensors, 2000000, boundary))
    # Part 2
    distress_beacon = find_distress_beacon(
        sensors, 
        Boundary(
            Point(0, 0), 
            Point(4000000, 4000000)
        )
    )
    #4000000
    print(distress_beacon)
    print(distress_beacon.x*4000000+distress_beacon.y)
    