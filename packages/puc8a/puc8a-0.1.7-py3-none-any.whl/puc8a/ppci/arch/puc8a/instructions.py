""" PUC8a instruction definitions.
"""

from ..encoding import Instruction, Operand, Syntax
from ..isa import Relocation, Isa
from ..token import Token, bit_range, Endianness
from .registers import PUC8aRegister
from . import registers
from math import log2
from .. import effects

isa = Isa()

class PUC8aToken(Token):
    class Info:
        size = 32
        endianness=Endianness.BIG,

    opcode = bit_range(4, 8)
    reg = bit_range(0, 4)
    c8 = bit_range(8, 16)
    dst = bit_range(8, 12)
    src = bit_range(0, 4)

class PUC8aInstruction(Instruction):
    isa = isa

def make(mnemonic, opcode):
    syntax = Syntax([mnemonic])

    patterns = {
        "opcode": opcode,
    }
    members = {
        "tokens": [PUC8aToken],
        "syntax": syntax,
        "patterns": patterns,
    }
    return type(mnemonic.title(), (PUC8aInstruction,), members)

def make_m(mnemonic, opcode):
    dst = Operand("dst", PUC8aRegister, read=False, write=True)
    src = Operand("src", PUC8aRegister, read=True, write=False)
    #syntax = Syntax(["get", " ", src, "\n", "set", " ", dst])
    syntax = Syntax(["mov", " ", dst, ",", " ", src])

    patterns = {
        "opcode": opcode,
        "dst": dst,
        "src": src,
    }
    members = {
        "tokens": [PUC8aToken],
        "dst": dst,
        "src": src,
        "syntax": syntax,
        "patterns": patterns,
    }
    return type(mnemonic.title(), (PUC8aInstruction,), members)


def make_r(mnemonic, opcode, addr=False, read=True, write=False):
    reg = Operand("reg", PUC8aRegister, read=read, write=write)
    if addr:
        syntax = Syntax([mnemonic, " ", "[", reg, "]"])
    else:
        syntax = Syntax([mnemonic, " ", reg])

    patterns = {
        "opcode": opcode,
        "reg": reg,
    }
    members = {
        "tokens": [PUC8aToken],
        "reg": reg,
        "syntax": syntax,
        "patterns": patterns,
    }
    return type(mnemonic.title(), (PUC8aInstruction,), members)

@isa.register_relocation
class Abs8DataRelocation(Relocation):
    """ Apply 8 bit data relocation """

    name = "abs8data"
    token = PUC8aToken
    field = "c8"

    def calc(self, sym_value, reloc_value):
        return sym_value

def data_relocations(self):
     if self.label:
         yield Abs8DataRelocation(self.c8)

def make_ldi(mnemonic, opcode, label=False):
    if label:
        c8 = Operand("c8", str)
        syntax = Syntax([mnemonic, " ", "@", c8])
    else:
        c8 = Operand("c8", int)
        syntax = Syntax([mnemonic, " ", c8])

    patterns = {
        "opcode": opcode,
    }
    if not label:
        patterns["c8"] = c8;
    members = {
        "label": label,
        "tokens": [PUC8aToken],
        "c8": c8,
        "syntax": syntax,
        "patterns": patterns,
        "gen_relocations": data_relocations,
    }
    return type(mnemonic.title(), (PUC8aInstruction,), members)

@isa.register_relocation
class Abs8BranchRelocation(Relocation):
    """ Apply 8 bit branch relocation """

    name = "abs8branch"
    token = PUC8aToken
    field = "c8"

    def calc(self, sym_value, reloc_value):
        # Imem is fake 32-bit
        return sym_value // 4

def branch_relocations(self):
     if self.label:
         yield Abs8BranchRelocation(self.c8)

def make_b(mnemonic, opcode, cond, label=True):
    if label:
        c8 = Operand("c8", str)
        syntax = Syntax([mnemonic, " ", "@", c8])
    else:
        c8 = Operand("c8", int)
        syntax = Syntax([mnemonic, " ", c8])

    patterns = {
        "opcode": opcode,
        "reg": cond
    }
    if not label:
        patterns["c8"] = c8;
    members = {
        "label": label,
        "tokens": [PUC8aToken],
        "c8": c8,
        "syntax": syntax,
        "patterns": patterns,
        "gen_relocations": branch_relocations,
    }
    return type(mnemonic.title(), (PUC8aInstruction,), members)

# Memory instructions:
Lda  = make_r  ("lda",   0, addr=True)
Sta  = make_r  ("sta",   1, addr=True)
LdiC = make_ldi("ldi",   4, label=False)
LdiL = make_ldi("ldi",   4, label=True)

# Branch instructions
B    = make_b  ("b",     5, 0)
B.effect = lambda self: [effects.Assign(effects.PC, self.c8)]
BZ   = make_b  ("bz",    5, 1)
BNZ  = make_b  ("bnz",   5, 2)
BCS  = make_b  ("bcs",   5, 3)
BCC  = make_b  ("bcc",   5, 4)
BLT  = make_b  ("blt",   5, 5)
BGE  = make_b  ("bge",   5, 6)

# Register transfer instructions
Mov  = make_m  ("mov",   0) # pseudo-instruction
Get  = make_r  ("get",   6)
Set  = make_r  ("set",   7, read=False, write=True)

# ALU instructions:
Add  = make_r  ("add",   8)
Sub  = make_r  ("sub",   9)
Inc  = make_r  ("inc",  10, write=True)
Dec  = make_r  ("dec",  11, write=True)
And  = make_r  ("and",  12)
Or   = make_r  ("or",   13)
XOr  = make_r  ("xor",  14)
Shft = make_r  ("shft", 15)

@isa.pattern("reg", "ADDI8(reg, reg)")
@isa.pattern("reg", "ADDU8(reg, reg)")
def pattern_add(context, tree, c0, c1):
    d = context.new_reg(PUC8aRegister)
    context.emit(Get(c0))
    context.emit(Add(c1))
    context.emit(Set(d))
    return d

@isa.pattern("reg", "SUBI8(reg, reg)")
@isa.pattern("reg", "SUBU8(reg, reg)")
def pattern_sub(context, tree, c0, c1):
    d = context.new_reg(PUC8aRegister)
    context.emit(Get(c0))
    context.emit(Sub(c1))
    context.emit(Set(d))
    return d

@isa.pattern("reg", "ADDI8(reg, CONSTI8)", condition=lambda t: t[1].value == 1)
@isa.pattern("reg", "ADDU8(reg, CONSTI8)", condition=lambda t: t[1].value == 1)
@isa.pattern("reg", "ADDI8(reg, CONSTU8)", condition=lambda t: t[1].value == 1)
@isa.pattern("reg", "ADDU8(reg, CONSTU8)", condition=lambda t: t[1].value == 1)
def pattern_addc(context, tree, c0):
    context.emit(Inc(c0))
    return c0

@isa.pattern("reg", "SUBI8(reg, CONSTI8)", condition=lambda t: t[1].value == 1)
@isa.pattern("reg", "SUBU8(reg, CONSTI8)", condition=lambda t: t[1].value == 1)
@isa.pattern("reg", "SUBI8(reg, CONSTU8)", condition=lambda t: t[1].value == 1)
@isa.pattern("reg", "SUBU8(reg, CONSTU8)", condition=lambda t: t[1].value == 1)
def pattern_subc(context, tree, c0):
    context.emit(Dec(c0))
    return c0

@isa.pattern("reg", "NEGI8(reg)", size=2, cycles=2, energy=2)
def pattern_neg(context, tree, c0):
    r = context.new_reg(PUC8aRegister)
    context.emit(LdiC(0))
    context.emit(Sub(c0))
    context.emit(Set(d))
    return d

@isa.pattern("reg", "INVU8(reg)", size=2, cycles=2, energy=2)
@isa.pattern("reg", "INVI8(reg)", size=2, cycles=2, energy=2)
def pattern_inv(context, tree, c0):
    r = context.new_reg(PUC8aRegister)
    context.emit(LdiC(255))
    context.emit(Xor(c0))
    context.emit(Set(d))
    return d

@isa.pattern("reg", "ANDI8(reg, reg)")
@isa.pattern("reg", "ANDU8(reg, reg)")
def pattern_and(context, tree, c0, c1):
    d = context.new_reg(PUC8aRegister)
    context.emit(Get(c0))
    context.emit(And(c1))
    context.emit(Set(d))
    return d

@isa.pattern("reg", "ORI8(reg, reg)")
@isa.pattern("reg", "ORU8(reg, reg)")
def pattern_or(context, tree, c0, c1):
    d = context.new_reg(PUC8aRegister)
    context.emit(Get(c0))
    context.emit(Or(c1))
    context.emit(Set(d))
    return d

@isa.pattern("reg", "XORI8(reg, reg)")
@isa.pattern("reg", "XORU8(reg, reg)")
def pattern_xor(context, tree, c0, c1):
    d = context.new_reg(PUC8aRegister)
    context.emit(Get(c0))
    context.emit(XOr(c1))
    context.emit(Set(d))
    return d

@isa.pattern("reg", "MULU8(reg, CONSTI8)", condition=lambda t: t[1].value >= 0 and (t[1].value == 0 or log2(t[1].value).is_integer()))
@isa.pattern("reg", "MULU8(reg, CONSTU8)", condition=lambda t: t[1].value >= 0 and (t[1].value == 0 or log2(t[1].value).is_integer()))
def pattern_mul(context, tree, c0):
    # Multiply with constant is needed for array handling; emulate
    if tree[1].value == 0:
        context.emit(LdiC(0))
        return c0
    elif tree[1].value == 1:
        return c0

    assert(tree[1].value > 1)
    n = log2(tree[1].value) - 1
    assert(n.is_integer())

    d = context.new_reg(PUC8aRegister)
    context.emit(LdiC(tree[1].value))
    context.emit(Set(d))
    context.emit(Get(c0))
    context.emit(Shft(d))
    context.emit(Set(d))
    return d

@isa.pattern("reg", "SHLI8(reg, CONSTU8)")
@isa.pattern("reg", "SHLU8(reg, CONSTU8)")
@isa.pattern("reg", "SHLI8(reg, CONSTI8)")
@isa.pattern("reg", "SHLU8(reg, CONSTI8)")
def pattern_shl(context, tree, c0):
    if tree.value == 0:
        return c0

    assert(tree[1].value > 0)
    d = context.new_reg(PUC8aRegister)
    context.emit(LdiC(tree[1].value))
    context.emit(Set(d))
    context.emit(Get(c0))
    context.emit(Shft(d))
    context.emit(Set(d))
    return d

@isa.pattern("reg", "SHRI8(reg, CONSTU8)")
@isa.pattern("reg", "SHRU8(reg, CONSTU8)")
@isa.pattern("reg", "SHRI8(reg, CONSTI8)")
@isa.pattern("reg", "SHRU8(reg, CONSTI8)")
def pattern_shr(context, tree, c0):
    if tree.value == 0:
        return c0

    assert(tree[1].value > 0)
    d = context.new_reg(PUC8aRegister)
    context.emit(-LdiC(tree[1].value))
    context.emit(Set(d))
    context.emit(Get(c0))
    context.emit(Shft(d))
    context.emit(Set(d))
    return d

@isa.pattern("reg", "FPRELU8")
def pattern_fprelu8(context, tree):
    # First stack element is at fp. Previous fp is at fp+1
    d = context.new_reg(PUC8aRegister)
    if tree.value.offset != -1:
        context.emit(LdiC(tree.value.offset+1))
        context.emit(Add(registers.fp))
        context.emit(Set(d))
    else:
        context.emit(Get(registers.fp))
        context.emit(Set(d))
    return d

@isa.pattern("stm", "STRI8(reg, reg)", energy=2)
@isa.pattern("stm", "STRU8(reg, reg)", energy=2)
def pattern_str(context, tree, c0, c1):
    context.emit(Get(c1))
    context.emit(Sta(c0))

@isa.pattern("reg", "LDRI8(reg)", energy=2)
@isa.pattern("reg", "LDRU8(reg)", energy=2)
def pattern_ldr(context, tree, c0):
    d = context.new_reg(PUC8aRegister)
    context.emit(Lda(c0))
    context.emit(Set(d))
    return d

# Misc patterns:
@isa.pattern("reg", "CONSTI8")
@isa.pattern("reg", "CONSTU8")
def pattern_ldic(context, tree):
    d = context.new_reg(PUC8aRegister)
    context.emit(LdiC(tree.value))
    context.emit(Set(d))
    return d

@isa.pattern("reg", "LABEL")
def pattern_ldil(context, tree):
    d = context.new_reg(PUC8aRegister)
    context.emit(LdiL(tree.value))
    context.emit(Set(d))
    return d

@isa.pattern("stm", "MOVI8(reg)")
@isa.pattern("stm", "MOVU8(reg)")
def pattern_mov(context, tree, c0):
    d = tree.value
    context.emit(Mov(d, c0, ismove=True))

#@isa.pattern("stm", "MOVI8(reg)")
#@isa.pattern("stm", "MOVU8(reg)")
#def pattern_mov(context, tree, c0):
#    d = tree.value
#    context.emit(Get(c0))
#    context.emit(Set(d))

@isa.pattern("reg", "REGI8", size=0, cycles=0, energy=0)
@isa.pattern("reg", "REGU8", size=0, cycles=0, energy=0)
def pattern_reg(context, tree):
    return tree.value

@isa.pattern("reg", "I8TOU8(reg)", size=0, cycles=0, energy=0)
@isa.pattern("reg", "U8TOI8(reg)", size=0, cycles=0, energy=0)
def pattern_cast(context, tree, c0):
    return c0

# Jumping around:
@isa.pattern("stm", "JMP")
def pattern_jmp(context, tree):
    tgt = tree.value
    context.emit(B(tgt.name, jumps=[tgt]))

@isa.pattern("stm", "CJMPI8(reg, reg)", size=3, cycles=2, energy=2, condition=lambda t: t.value[0] == "==" or t.value[0] == "!=")
def pattern_cjmpi(context, tree, c0, c1):
    op, yes_label, no_label = tree.value
    opnames = {
        "==": BZ,
        "!=": BNZ,
    }
    Bop = opnames[op]
    context.emit(Get(c0))
    context.emit(Sub(c1))
    jmp_ins = B(no_label.name, jumps=[no_label])
    context.emit(Bop(yes_label.name, jumps=[yes_label, jmp_ins]))
    context.emit(jmp_ins)

@isa.pattern("stm", "CJMPU8(reg, reg)", size=3, cycles=2, energy=2)
def pattern_cjmpu(context, tree, c0, c1):
    op, yes_label, no_label = tree.value
    opnames = {
        "==": (BZ, False),
        "!=": (BNZ, False),
        "<": (BCC, False),
        ">": (BCC, True),
        "<=": (BCS, True),
        ">=": (BCS, False),
    }
    Bop, swap = opnames[op]
    if swap:
        context.emit(Get(c1))
        context.emit(Sub(c0))
    else:
        context.emit(Get(c0))
        context.emit(Sub(c1))
    jmp_ins = B(no_label.name, jumps=[no_label])
    context.emit(Bop(yes_label.name, jumps=[yes_label, jmp_ins]))
    context.emit(jmp_ins)

#@isa.pattern("stm", "CJMPI8(reg, CONSTI8)", size=3, cycles=2, energy=2, condition=lambda t: t[1].value == 0 and (t.value[0] == "==" or t.value[0] == "!="))
#@isa.pattern("stm", "CJMPU8(reg, CONSTI8)", size=3, cycles=2, energy=2, condition=lambda t: t[1].value == 0 and (t.value[0] == "==" or t.value[0] == "!="))
#@isa.pattern("stm", "CJMPI8(reg, CONSTU8)", size=3, cycles=2, energy=2, condition=lambda t: t[1].value == 0 and (t.value[0] == "==" or t.value[0] == "!="))
#@isa.pattern("stm", "CJMPU8(reg, CONSTU8)", size=3, cycles=2, energy=2, condition=lambda t: t[1].value == 0 and (t.value[0] == "==" or t.value[0] == "!="))
#def pattern_cjmp0(context, tree, c0):
#    # Special case for comparison to 0 (more efficient)
#    op, yes_label, no_label = tree.value
#    opnames = {
#        "==": BZ,
#        "!=": BNZ,
#    }
#    Bop = opnames[op]
#    d = context.new_reg(PUC8aRegister)
#    context.emit(MovR(c0, c0));
#    jmp_ins = B(no_label.name, jumps=[no_label])
#    context.emit(Bop(yes_label.name, jumps=[yes_label, jmp_ins]))
#    context.emit(jmp_ins)
