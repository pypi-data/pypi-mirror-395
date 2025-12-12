"""Simulator for ENG1448 8-bit accumulator-based processor
   (c) 2020-2025 Wouter Caarls, PUC-Rio
"""

import copy
from .disassembler import Disassembler

class State:
    """Machine state for simulator."""
    def __init__(self):
        self.acc = 0
        self.regs = [0 for i in range(16)]
        self.mem = [0 for i in range(256)]
        self.regs[14] = 255
        self.zero = False
        self.carry = False
        self.negative = False
        self.overflow = False

    def diff(self, state):
        """Calculates difference between this state and another."""
        d = ''

        if self.acc != state.acc:
            d += f', acc <- {state.acc}'
        for i in range(14):
            if self.regs[i] != state.regs[i]:
                d += f', r{i} <- {state.regs[i]}'
        for i in range(256):
            if self.mem[i] != state.mem[i]:
                d += f', [{i}] <- {state.mem[i]}'
        if self.regs[14] != state.regs[14]:
            d += f', sp <- {state.regs[14]}'
        if self.zero != state.zero:
            d += f', zf <- {state.zero}'
        if self.carry != state.carry:
            d += f', cf <- {state.carry}'
        if self.negative != state.negative:
            d += f', nf <- {state.negative}'
        if self.overflow != state.overflow:
            d += f', vf <- {state.overflow}'

        if d != '':
            d = d[2:]
        return d

    def __str__(self):
        s = f'acc = {self.acc}, '
        for i in range(14):
            s += f'r{i} = {self.regs[i]}, '
        s += f'pc = {self.regs[15]}, sp = {self.regs[14]}, zf = {self.zero}, cf = {self.carry}, nf = {self.negative}, vf = {self.overflow}'

        return s

class Simulator:
    """Simulates machine code."""
    def __init__(self, map = None):
        self.disassembler = Disassembler(map)

    def execute(self, bin, bin2, state):
        """Returns machine state after executing instruction."""
        # Disassemble instruction
        m, _ = self.disassembler.process(bin, bin2)

        opcode = bin[0:4]
        r = int(bin[4:8], 2)
        imm = int(bin2, 2)
        next = copy.deepcopy(state)
        next.regs[15] += 1

        val = next.regs[r]

        # Simulate instructions
        if m == 'lda':
            if val == 2:
                inp = input('Enter keyboard character: ')
                if len(inp) > 0:
                    next.acc = ord(inp[0])
                else:
                    next.acc = 0
            else:
                next.acc = state.mem[val]
        elif m == 'sta':
            if val == 7:
                print(chr(state.acc), end='')
            elif val == 8 and state.acc == 1:
                print()
            else:
                next.mem[val] = state.acc
        elif m == 'ldi':
            next.acc = imm
            next.regs[15] += 1
        elif m[0] == 'b':
            # Direct jumps
            if ( m == 'b' or
                (m == 'bz' and state.zero) or (m == 'bnz' and not state.zero) or
                (m == 'bcs' and state.carry) or (m == 'bcc' and not state.carry) or
                (m == 'blt' and (state.overflow != state.negative)) or
                (m == 'bge' and (state.overflow == state.negative))):
                    next.regs[15] = imm
            else:
                next.regs[15] += 1
        elif m == 'get':
            next.acc = val
        elif m == 'set':
            next.regs[r] = state.acc
        else:
            # ALU instructions (modify flags)
            next.overflow = 0
            if m == 'add':
                res = state.acc + val
                next.overflow = bool((~(state.acc ^ val) & (state.acc ^ res)) & 128)
            elif m == 'inc':
                res = val + 1
                next.overflow = bool((~(val ^ 1) & (val ^ res)) & 128)
            elif m == 'sub':
                res = state.acc + (256-val)
                next.overflow = bool(( (state.acc ^ val) & (state.acc ^ res)) & 128)
            elif m == 'dec':
                res = val + 255
                next.overflow = bool(( (val ^ 1) & (val ^ res)) & 128)
            elif m == 'shft':
                if val > 127:
                    res = state.acc >> (256-val)
                else:
                    res = state.acc << val
            elif m == 'and':
                res = state.acc & val
            elif m == 'or':
                res = state.acc | val
            elif m == 'xor':
                res = state.acc ^ val
            else:
                raise ValueError(f'Unknown opcode {opcode} (\'{m}\')')

            next.zero = ((res&255) == 0)
            next.carry = bool(res & 256)
            next.negative = bool(res & 128)

            if m == 'inc' or m == 'dec':
                next.regs[r] = res&255
            else:
                next.acc = res&255

        return next

    def help(self):
        print("""Available commands:
   h       This help.
   n       Advance to next instruction.
   b a     Set or clear breakpoint at address a.
   c       Execute continuously until halted.
   p       Print current state.
   q       Exit simulator.
   rx      Print contents of register x.
   rx = y  Set register x to value y.
   [a]     Print contents of memory address a.
   [a] = y Set memory address a to value y.
""")

    def process(self, mem):
        """Simulate machine code."""
        state = State()
        for i, c in enumerate(mem['data']):
            state.mem[i] = int(c[0], 2)

        breakpoints = []
        quiet = False
        men = None

        while True:
            # Print current instruction
            bin = mem['code'][state.regs[15]][0]
            bin2 = mem['code'][(state.regs[15]+1)%len(mem['code'])][0]

            if quiet:
                next = copy.deepcopy(self.execute(bin, bin2, state))
                if next.regs[15] == state.regs[15] or next.regs[15] in breakpoints:
                    quiet = False
                state = next
                continue

            mne, dis = self.disassembler.process(bin, bin2)
            if mne == 'ldi' or mne[0] == 'b':
                print(f'{state.regs[15]:3}: {bin[0:4]} {bin[4:8]} {bin2} ({dis})')
            else:
                print(f'{state.regs[15]:3}: {bin[0:4]} {bin[4:8]} ({dis})')

            next = copy.deepcopy(state)

            # Present interface
            cmd = input('>> ').strip()
            if cmd == '' or cmd == 'n':
                # Advance to next instruction
                next = self.execute(bin, bin2, state)
            elif cmd == 'c':
                # Execute continuously
                quiet = True
            elif cmd[0] == 'b':
                # Set (or clear) breakpoint
                try:
                    line = int(cmd[2:], 0)
                    if line in breakpoints:
                        breakpoints.remove(line)
                    else:
                        breakpoints.append(line)
                    print('breakpoints: ', breakpoints)
                except Exception as e:
                    print(e)
            elif cmd == 'p':
                # Print current state
                print(state)
            elif cmd == 'q':
                # Exit simulator
                return
            elif cmd[0] == 'r':
                # Set register
                tokens = [t.strip() for t in cmd.split('=')]
                if len(tokens[0]) < 2:
                    self.help()
                elif len(tokens) == 1:
                    try:
                        print(f'r{int(tokens[0][1:])} = {state.regs[int(tokens[0][1:])]}')
                    except Exception as e:
                        print(e)
                elif len(tokens) == 2:
                    try:
                        next.regs[int(tokens[0][1:])] = int(tokens[1], 0)&255
                    except Exception as e:
                        print(e)
                else:
                    self.help()
            elif cmd[0] == '[':
                # Set memory address
                tokens = [t.strip() for t in cmd.split('=')]
                if len(tokens[0]) < 2 or tokens[0][0] != '[' or tokens[0][-1] != ']':
                    self.help()
                elif len(tokens) == 1:
                    try:
                        print(f'[{int(tokens[0][1:-1])}] = {state.mem[int(tokens[0][1:-1])]}')
                    except Exception as e:
                        print(e)
                elif len(tokens) == 2:
                    try:
                        next.mem[int(tokens[0][1:-1])] = int(tokens[1], 0)&255
                    except Exception as e:
                        print(e)
                else:
                    self.help()
            else:
                self.help()

            # Print resulting difference
            diff = state.diff(next)
            if diff != '':
                print('     ' + diff)
            state = copy.deepcopy(next)

    def run(self, mem, steps=1000):
        """Simulate machine code for a set number of steps and return PC."""
        state = State()
        for i, c in enumerate(mem['data']):
            state.mem[i] = int(c[0], 2)

        for s in range(steps):
            bin = mem['code'][state.regs[15]][0]
            bin2 = mem['code'][(state.regs[15]+1)%len(mem['code'])][0]
            state = copy.deepcopy(self.execute(bin, bin2, state))

        return state.regs[15]
