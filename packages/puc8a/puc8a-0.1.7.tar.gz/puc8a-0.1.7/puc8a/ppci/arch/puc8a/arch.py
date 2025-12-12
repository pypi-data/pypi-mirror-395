""" Define PUC8a architecture """

from ... import ir
from ...binutils.assembler import BaseAssembler
from ..arch import Architecture
from ..arch_info import ArchInfo, TypeInfo
from ..generic_instructions import Label, Alignment, RegisterUseDef
from ..runtime import get_runtime_files
from . import instructions, registers
from ..data_instructions import data_isa

class PUC8aArch(Architecture):
    """ PUC8a architecture """

    name = "puc8a"

    def __init__(self, options=None):
        super().__init__(options=options)
        self.info = ArchInfo(
            type_infos={
                ir.i8: TypeInfo(1, 1),
                ir.u8: TypeInfo(1, 1),
                ir.i16: TypeInfo(1, 1),
                ir.u16: TypeInfo(1, 1),
                ir.f32: TypeInfo(1, 1),
                ir.f64: TypeInfo(1, 1),
                "int": ir.i8,
                "long": ir.i8,
                "ptr": ir.u8,
                ir.ptr: ir.u8,
            },
            register_classes=registers.register_classes,
        )

        self.isa = instructions.isa + data_isa

        self.assembler = BaseAssembler()
        self.assembler.gen_asm_parser(self.isa)

    def get_runtime(self):
        """ Retrieve the runtime for this target """
        return asm(io.StringIO(""), self)

    def determine_arg_locations(self, arg_types):
        arg_locs = []
        int_regs = [registers.r11, registers.r10, registers.r9]
        for arg_type in arg_types:
            # Determine register:
            if arg_type in [
                ir.i8,
                ir.u8,
                ir.ptr,
            ]:
                reg = int_regs.pop(0)
            else:  # pragma: no cover
                raise NotImplementedError(str(arg_type))
            arg_locs.append(reg)
        return arg_locs

    def determine_rv_location(self, ret_type):
        """ return value in r0 """
        if ret_type in [ir.i8, ir.u8, ir.ptr]:
            rv = registers.r0
        else:  # pragma: no cover
            raise NotImplementedError(str(ret_type))
        return rv

    def gen_prologue(self, frame):
        """ Returns prologue instruction sequence """
        # Label indication function:
        yield Label(frame.name)

        # Callee save registers:
        for reg in self.get_callee_saved(frame):
            yield from self.push(reg)

        # Allocate stack and set frame pointer
        if frame.stacksize > 0:
            yield from self.push(registers.fp)
            yield from self.move(registers.fp, registers.sp)

            ss = frame.stacksize
            while ss > 0:
                yield instructions.Dec(registers.sp)
                ss -= 1

    def gen_epilogue(self, frame):
        """ Return epilogue sequence """
        # Restore stack and frame pointers
        if frame.stacksize > 0:
            ss = frame.stacksize
            while ss > 0:
                yield instructions.Inc(registers.sp)
                ss -= 1

            yield from self.pop(registers.fp)

        # Pop save registers back:
        for reg in reversed(self.get_callee_saved(frame)):
            yield from self.pop(reg)

        # Return
        yield from self.pop(registers.pc)

    def get_callee_saved(self, frame):
        saved_registers = []
        for reg in registers.callee_save:
            if frame.is_used(reg, self.info.alias):
                saved_registers.append(reg)
        return saved_registers

    def gen_call(self, frame, label, args, rv):
        arg_types = [a[0] for a in args]
        arg_locs = self.determine_arg_locations(arg_types)

        arg_regs = []
        for arg_loc, arg2 in zip(arg_locs, args):
            arg = arg2[1]
            if isinstance(arg_loc, registers.PUC8aRegister):
                arg_regs.append(arg_loc)
                yield from self.move(arg_loc, arg)
            else:  # pragma: no cover
                raise NotImplementedError("Parameters in memory not impl")

        yield RegisterUseDef(uses=arg_regs)

        yield instructions.LdiC(5)
        yield instructions.Add(registers.pc)
        yield instructions.Sta(registers.sp)
        yield instructions.Dec(registers.sp)
        yield instructions.LdiL(label)
        yield instructions.Set(registers.pc, clobbers=registers.caller_save)

        if rv:
            retval_loc = self.determine_rv_location(rv[0])
            yield RegisterUseDef(defs=(retval_loc,))
            yield from self.move(rv[1], retval_loc)

    def gen_function_enter(self, args):
        arg_types = [a[0] for a in args]
        arg_locs = self.determine_arg_locations(arg_types)

        arg_regs = set(
            l for l in arg_locs if isinstance(l, registers.PUC8aRegister)
        )
        yield RegisterUseDef(defs=arg_regs)

        for arg_loc, arg2 in zip(arg_locs, args):
            arg = arg2[1]
            if isinstance(arg_loc, registers.PUC8aRegister):
                yield from self.move(arg, arg_loc)
            else:  # pragma: no cover
                raise NotImplementedError("Parameters in memory not impl")

    def gen_function_exit(self, rv):
        live_out = set()
        if rv:
            retval_loc = self.determine_rv_location(rv[0])
            yield from self.move(retval_loc, rv[1])
            live_out.add(retval_loc)
        yield RegisterUseDef(uses=live_out)

    def move(self, dst, src):
        yield instructions.Mov(dst, src, ismove=True)

    def push(self, reg):
        yield instructions.Get(reg)
        yield instructions.Sta(registers.sp)
        yield instructions.Dec(registers.sp)

    def pop(self, reg):
        yield instructions.Inc(registers.sp)
        yield instructions.Lda(registers.sp)
        yield instructions.Set(reg)
