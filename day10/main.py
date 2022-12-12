#!/usr/bin/env python3
from pathlib import Path
from typing import TextIO
from dataclasses import dataclass, field

CYCLE_MAP = {
    'noop': 1,
    'addx': 2
}

@dataclass
class Instruction:
    name: str
    cycles: int
    arg: int = 0
    
@dataclass
class SignalStrengthProbe:
    start: int
    every: int
    max_times: int
    values: list[int] = field(default_factory=list)
    times: int = 0

class CRT:
    
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.pixel_screen = []
        for i in range(height):
            self.pixel_screen.append([])
            for _ in range(width):
                self.pixel_screen[i].append('.')
    
    def draw(self, x: int, cycle: int):
        y = int(cycle/self.width)
        a = cycle%self.width
        if a in [x-1, x, x+1]:
            self.pixel_screen[y][a] = '#'
    
    def print(self):
        for row in self.pixel_screen:
            print(''.join(row))

@dataclass
class ProgramContext:
    cycles: int
    X: int
    crt: CRT



def parse_instruction(line: str):
    args = line.strip('\n').split(' ')
    if len(args) > 1:
        return Instruction(args[0], CYCLE_MAP[args[0]], int(args[1]))
    return Instruction(args[0], CYCLE_MAP[args[0]])

def run_instruction(instruction: Instruction, context: ProgramContext, probe: SignalStrengthProbe):
    context.crt.draw(context.X, context.cycles)
    context.cycles += 1
    context.crt.draw(context.X, context.cycles)
    probe_signal(context, probe)
    if instruction.cycles == 1:
        return
    context.cycles += 1
    probe_signal(context, probe)
    context.X += instruction.arg
    context.crt.draw(context.X, context.cycles)
    
def probe_signal(context: ProgramContext, probe: SignalStrengthProbe):
    probe_at = probe.start + probe.every * (probe.times)
    if context.cycles < probe_at:
        return
    probe.values.append(context.X * context.cycles)
    probe.times += 1

def signal_strength(stream: TextIO, probe: SignalStrengthProbe):
    crt = CRT(40, 6)
    context = ProgramContext(0, 1, crt)
    for line in stream:
        instr = parse_instruction(line)
        run_instruction(instr, context, probe)
    crt.print()


if __name__ == '__main__':
    input_file = Path(__file__).parent / 'ok.txt'
    with open(input_file) as f:
        probe = SignalStrengthProbe(20, 40, 6)
        signal_strength(f, probe)
        print(sum(probe.values))