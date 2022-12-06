#!/usr/bin/env python3
from pathlib import Path

input_file = Path(__file__).parent / 'input.txt'
buffer = ''
START_OF_PACKET = 14
with open(input_file) as f:
    stream = f.read()
    for i in range(len(stream)):
        packet = stream[i:i+START_OF_PACKET]
        if len(set(packet)) == START_OF_PACKET:
            print(i+START_OF_PACKET)
            break
