#!/usr/bin/env python3
from pathlib import Path
from pprint import pprint


def read_packets(input_file: str):
    packets = []
    with open(input_file) as f:
        for line in f:
            line = line.strip('\n')
            if line == '':
                yield packets
                packets.clear()
            else:
                packets.append(eval(line))
    yield packets

def is_right_order(left: list[int], right: list[int]):
    i = -1
    for i, (l, r) in enumerate(zip(left, right)):
        if isinstance(l, list) or isinstance(r, list):
            if isinstance(l, int):
                l = [l]
            if isinstance(r, int):
                r = [r]
            res = is_right_order(l, r)
            if res is not None:
                return res
        elif l < r:
            return True
        elif r < l:
            return False 
    left_ran_out = i == len(left)-1
    right_ran_out = i == len(right)-1
    if left_ran_out and right_ran_out:
        return None
    elif left_ran_out:
        return True
    elif right_ran_out:
        return False
    return None


if __name__ == '__main__':
    input_file = Path(__file__).parent / 'input.txt'
    packets = read_packets(input_file)
    right_order_count = 0
    DIV1 = [[2]]
    DIV2 = [[6]]
    all_packets = [
        [0, DIV1],
        [0, DIV2]
    ]
    for i, (left, right) in enumerate(packets):
        all_packets.extend([[0, left], [0, right]])
        if is_right_order(left, right):
            print(f'{i+1}: {left} vs {right}')
            right_order_count += i+1
    pprint(all_packets)
    for i, packet1 in enumerate(all_packets):
        for packet2 in (all_packets[:i] + all_packets[i+1:]):
            if is_right_order(packet1[1], packet2[1]):
                packet1[0] += 1
    all_packets.sort(key=lambda k: k[0], reverse=True)
    print('')
    pprint(all_packets)
    part2_answer = 0
    for i, p in enumerate(all_packets):
        if p[1] == DIV1 or p[1] == DIV2:
            if part2_answer:
                part2_answer *= i+1
                break
            else:
                part2_answer = i+1
    print(f'part1_answer: {right_order_count}')
    print(f'part2_answer {part2_answer}')
    
    
    
