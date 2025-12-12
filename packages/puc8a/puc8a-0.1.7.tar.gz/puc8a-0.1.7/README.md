# PUC8a

Assembler and C compiler for the PUC8a processor

Copyright 2020-2025 Wouter Caarls

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Introduction

PUC8a is an accumulator-based microcontroller with 8-bit registers. It is used in the
ENG4448 course of PUC-Rio. This is the assembler and C compiler
infrastructure for it.

# Instruction set architecture

This very simple processor is a Harvard design, with 8-bit instructions and 8-bit data values.
Both instruction and data memories have 256 addresses.

## Registers

There are 16 registers. `r14` is `sp`; `r15` is `pc`. The C compiler uses `r13` as `fp`.

## Instructions

All ALU instructions set flags.

| Opcode(4)  | Data(4) | Mnm | Effect | Example |
|---|---|---|---|---|
| 0000 | rs | LDA  | acc <- dmem[rs]                        | `lda  r0`    |
| 0001 | rd | STA  | dmem[rd] <- acc                        | `sta  r0`    |
| 0100 | 0000 | LDI  | acc <- imem[pc+1], pc <- pc + 1      | `ldi  42`    |
| 0101 | cond | B<cond>  | if cond then pc <- imem[pc + 1] else pc <- pc + 1 | `bcc  42`    |
| 0110 | rs | GET  | acc <- rs                        | `get  r0`    |
| 0111 | rs | SET  | rs <- acc                        | `set  r0`    |
| 1000 | rs | ADD  | acc <- acc + rs                       | `add  r0`    |
| 1001 | rs | SUB  | acc <- acc - rs                       | `sub  r0`    |
| 1010 | rd | INC  | rd <- rd + 1                       | `inc  r0`    |
| 1011 | rd | DEC  | rd <- rd - 1                       | `dec  r0`    |
| 1100 | rs | AND  | acc <- acc & rs                       | `and  r0`    |
| 1101 | rs | OR  | acc <- acc \| rs                       | `or  r0`    |
| 1110 | rs | XOR  | acc <- acc ^ rs                       | `xor  r0`    |
| 1111 | rs | SHFT  | if (rs >= 0) acc <- acc << rs else acc <- acc >> -rs | `shft  r0`    |

## Condition codes

| Condition | Instruction mnemonic | Meaning |
|---|---|---|
| 0000 | B | Unconditional |
| 0001 | BZ | Zero flag set |
| 0010 | BNZ | Zero flag not set |
| 0011 | BCS | Carry flag set |
| 0100 | BCC | Carry flag not set |
| 0101 | BLT | Signed less than |
| 0110 | BGE | Signed greater than or equal |

## Pseudo-instructions

| Pseudo-instruction | Actual instruction |
|---|---|
| `beq` | `bz` |
| `bne` | `bnz` |
| `bhs` | `bcs` |
| `blo` | `bcc` |

# Assembly language

Assembly statements generally follow the following structure
```asm
[LABEL:] MNEMONIC [OPERAND[, OPERAND]...]
```
The available `MNEMONIC`s can be found in the table above. `OPERAND`s can be registers, constants, or labels. Labels used as operands must be prefixed with `@`:
```asm
loop: b @loop
```
When the operand is used as the contents of a memory address, it must be enclosed in square brackets:
```asm
ldi @inp
set r0
lda [r0]
.section data
inp: .db 0
```
Apart from these statements, the assembler recognizes the following directives:

- ```asm
  .include "FILE"
  ```

  Includes a given `FILE`. The path is relative to the file being processed.

- ```asm
  .section SECTION
  ```

  Define into which memory `SECTION` the subsequent code is assembled. Options are `code` and `data`. The default is `code`.

- ```asm
  .org ADDRESS
  ```

  Sets memory `ADDRESS` at which the subsequent code will be assembled.

- ```asm
  .equ LABEL VALUE
  ```

  Creates a `LABEL` for a specific constant `VALUE`. Values may be character constants, e.g. `"c"`

- ```asm
  .db VALUE
  ```

  Inserts a `VALUE` into the instruction stream. The value may be a string constant, e.g. `"Hello, world"`

- ```asm
  .macro NAME
  ; code
  .endmacro
  ```

  Defines a macro. The code inside the macro can use arguments of the form `$0`, `$1`, etc., which are replaced by the actual arguments when the macro is called using `NAME arg0, arg1`. Labels inside the macro that start with an underscore are localized such that the same macro can be called multiple times.

# Installation

```
pip install puc8a
```

or

```
git clone https://github.com/wcaarls/puc8a
cd puc8a
pip install .
```

# Usage

```
usage: as-puc8a [-h] [-o OUTPUT] [-s] [-t N] [-E] file

PUC8a Assembler (c) 2020-2025 Wouter Caarls, PUC-Rio

positional arguments:
  file                  ASM source file

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file
  -s, --simulate        Simulate resulting program
  -t N, --test N        Simulate for 1000 steps and check whether PC == N
  -E                    Output preprocessed assembly code

```

```
usage: cc-puc8a [-h] [-o OUTPUT] [-s] [-t N] [-S] [-O {0,1,2}] file

PUC8a C compiler (c) 2020-2025 Wouter Caarls, PUC-Rio

positional arguments:
  file                  C source file

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file
  -s, --simulate        Simulate resulting program
  -t N, --test N        Simulate for 1000 steps and check whether PC == N
  -S                    Output assembly code
  -O {0,1,2}            Optimization level

```

# Examples

Directly compile C to VHDL
```
./cc-puc8a examples/c/hello.c
```

Create assembly from C
```
./cc-puc8a examples/c/hello.c -S
```

Assemble to VHDL code
```
./as-puc8a examples/asm/ps2_lcd.asm
```

Assemble to VHDL package
```
./as-puc8a examples/asm/ps2_lcd.asm -o ps2_lcd.vhdl
```

Simulate resulting C or assembly program
```
./cc-puc8a -O0 examples/c/unittest.c -s
./as-puc8a examples/asm/simple.asm -s
```

# Acknowledgments

The C compiler is based on [PPCI](https://github.com/windelbouwman/ppci).

Copyright (c) 2011-2019, Windel Bouwman

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
