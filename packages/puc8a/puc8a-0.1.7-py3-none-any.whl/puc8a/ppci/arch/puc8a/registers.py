""" Description of mips registers """

from ..registers import Register, RegisterClass
from ... import ir

class PUC8aRegister(Register):
    bitsize = 8

    @classmethod
    def from_num(cls, num):
        return num_reg_map[num]

r0 = PUC8aRegister("r0", num=0)
r1 = PUC8aRegister("r1", num=1)
r2 = PUC8aRegister("r2", num=2)
r3 = PUC8aRegister("r3", num=3)
r4 = PUC8aRegister("r4", num=4)
r5 = PUC8aRegister("r5", num=5)
r6 = PUC8aRegister("r6", num=6)
r7 = PUC8aRegister("r7", num=7)
r8 = PUC8aRegister("r8", num=8)
r9 = PUC8aRegister("r9", num=9)
r10 = PUC8aRegister("r10", num=10)
r11 = PUC8aRegister("r11", num=11)
z = PUC8aRegister("r12", num=12, aka=("z",))
fp = PUC8aRegister("r13", num=13, aka=("fp",))
sp = PUC8aRegister("r14", num=14, aka=("sp",))
pc = PUC8aRegister("r15", num=15, aka=("pc",))

PUC8aRegister.registers = [r0, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, z, fp, sp, pc]
num_reg_map = {r.num: r for r in PUC8aRegister.registers}
alloc_registers = [r0, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11]

register_classes = [
    RegisterClass(
        "reg",
        [ir.i8, ir.u8, ir.ptr],
        PUC8aRegister,
        alloc_registers,
    ),
]

caller_save = [r0, r1, r2, r3, r4, r9, r10, r11]
callee_save = [r5, r6, r7, r8]
