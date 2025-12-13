"""
Z-Machine opcode decoder and instruction set

Implements the complete Z-Machine instruction set for all versions
"""

from typing import Dict, List, Tuple, Optional, Any
from enum import Enum
import struct


class OperandType(Enum):
    """Operand types in Z-machine instructions"""
    LARGE_CONST = 0  # 16-bit constant
    SMALL_CONST = 1  # 8-bit constant
    VARIABLE = 2     # Variable number
    OMITTED = 3      # No operand


class OpcodeForm(Enum):
    """Instruction forms"""
    LONG = 0      # 2OP with small constant/variable operands
    SHORT = 1     # 0OP or 1OP
    EXTENDED = 2  # EXT (V5+)
    VARIABLE = 3  # 2OP or VAR with variable operand count


class Instruction:
    """Represents a decoded Z-machine instruction"""

    def __init__(self, address: int, opcode: int, name: str,
                 operands: List[Any], store_var: Optional[int] = None,
                 branch_offset: Optional[int] = None, branch_on_true: bool = True,
                 text: Optional[str] = None):
        self.address = address
        self.opcode = opcode
        self.name = name
        self.operands = operands
        self.store_var = store_var
        self.branch_offset = branch_offset
        self.branch_on_true = branch_on_true
        self.text = text  # For print instructions
        self.size = 0  # Total instruction size in bytes

    def __repr__(self):
        parts = [f"{self.address:04X}: {self.name}"]
        if self.operands:
            ops = ", ".join(str(op) for op in self.operands)
            parts.append(f"({ops})")
        if self.store_var is not None:
            parts.append(f" -> var{self.store_var}")
        if self.branch_offset is not None:
            parts.append(f" [{'' if self.branch_on_true else '~'}{self.branch_offset:+d}]")
        if self.text:
            parts.append(f' "{self.text}"')
        return " ".join(parts)


class OpcodeDecoder:
    """Decode Z-machine instructions"""

    # Opcode tables for different forms
    SHORT_0OP = {
        0x00: ("rtrue", False, False),
        0x01: ("rfalse", False, False),
        0x02: ("print", False, False),  # Followed by literal string
        0x03: ("print_ret", False, False),  # Print + rtrue
        0x04: ("nop", False, False),
        0x05: ("save", False, True),  # V1-3: branch; V4+: store (handled in decoder)
        0x06: ("restore", False, True),  # V1-3: branch; V4+: store (handled in decoder)
        0x07: ("restart", False, False),
        0x08: ("ret_popped", False, False),
        0x09: ("pop", False, False),  # V1-4 catch, V5+ pop
        0x0A: ("quit", False, False),
        0x0B: ("new_line", False, False),
        0x0C: ("show_status", False, False),  # V3 only
        0x0D: ("verify", False, True),  # Branch
        0x0E: ("extended", False, False),  # V5+, special case
        0x0F: ("piracy", False, True),  # Branch
    }

    SHORT_1OP = {
        0x00: ("jz", False, True),
        0x01: ("get_sibling", True, True),
        0x02: ("get_child", True, True),
        0x03: ("get_parent", True, False),
        0x04: ("get_prop_len", True, False),
        0x05: ("inc", False, False),
        0x06: ("dec", False, False),
        0x07: ("print_addr", False, False),
        0x08: ("call_1s", True, False),  # V4+
        0x09: ("remove_obj", False, False),
        0x0A: ("print_obj", False, False),
        0x0B: ("ret", False, False),
        0x0C: ("jump", False, False),
        0x0D: ("print_paddr", False, False),
        0x0E: ("load", True, False),
        0x0F: ("not", True, False),  # V1-4 not, V5+ call_1n
    }

    LONG_2OP = {
        0x01: ("je", False, True),
        0x02: ("jl", False, True),
        0x03: ("jg", False, True),
        0x04: ("dec_chk", False, True),
        0x05: ("inc_chk", False, True),
        0x06: ("jin", False, True),
        0x07: ("test", False, True),
        0x08: ("or", True, False),
        0x09: ("and", True, False),
        0x0A: ("test_attr", False, True),
        0x0B: ("set_attr", False, False),
        0x0C: ("clear_attr", False, False),
        0x0D: ("store", False, False),
        0x0E: ("insert_obj", False, False),
        0x0F: ("loadw", True, False),
        0x10: ("loadb", True, False),
        0x11: ("get_prop", True, False),
        0x12: ("get_prop_addr", True, False),
        0x13: ("get_next_prop", True, False),
        0x14: ("add", True, False),
        0x15: ("sub", True, False),
        0x16: ("mul", True, False),
        0x17: ("div", True, False),
        0x18: ("mod", True, False),
        0x19: ("call_2s", True, False),  # V4+
        0x1A: ("call_2n", False, False),  # V5+
        0x1B: ("set_colour", False, False),  # V5+
        0x1C: ("throw", False, False),  # V5+
    }

    VAR_2OP = LONG_2OP  # Same opcodes, variable operand form

    VAR_VAR = {
        0x00: ("call", True, False),  # V1-3 call, V4+ call_vs
        0x01: ("storew", False, False),
        0x02: ("storeb", False, False),
        0x03: ("put_prop", False, False),
        0x04: ("sread", False, False),  # V1-3 sread, V4+ aread, V5+ read
        0x05: ("print_char", False, False),
        0x06: ("print_num", False, False),
        0x07: ("random", True, False),
        0x08: ("push", False, False),
        0x09: ("pull", False, False),  # V1-5,V8: pull [var]; V6-7: pull -> store (handled in decoder)
        0x0A: ("split_window", False, False),  # V3+
        0x0B: ("set_window", False, False),  # V3+
        0x0C: ("call_vs2", True, False),  # V4+
        0x0D: ("erase_window", False, False),  # V4+
        0x0E: ("erase_line", False, False),  # V4+
        0x0F: ("set_cursor", False, False),  # V4+
        0x10: ("get_cursor", False, False),  # V4+
        0x11: ("set_text_style", False, False),  # V4+
        0x12: ("buffer_mode", False, False),  # V4+
        0x13: ("output_stream", False, False),  # V3+
        0x14: ("input_stream", False, False),  # V3+
        0x15: ("sound_effect", False, False),  # V3+
        0x16: ("read_char", True, False),  # V4+
        0x17: ("scan_table", True, True),  # V4+
        0x18: ("not", True, False),  # V5+
        0x19: ("call_vn", False, False),  # V5+
        0x1A: ("call_vn2", False, False),  # V5+
        0x1B: ("tokenise", False, False),  # V5+
        0x1C: ("encode_text", False, False),  # V5+
        0x1D: ("copy_table", False, False),  # V5+
        0x1E: ("print_table", False, False),  # V5+
        0x1F: ("check_arg_count", False, True),  # V5+
    }

    EXTENDED = {
        0x00: ("save", True, False),  # V5+
        0x01: ("restore", True, False),  # V5+
        0x02: ("log_shift", True, False),  # V5+
        0x03: ("art_shift", True, False),  # V5+
        0x04: ("set_font", True, False),  # V5+
        0x05: ("draw_picture", False, False),  # V6
        0x06: ("picture_data", False, True),  # V6
        0x07: ("erase_picture", False, False),  # V6
        0x08: ("set_margins", False, False),  # V6
        0x09: ("save_undo", True, False),  # V5+
        0x0A: ("restore_undo", True, False),  # V5+
        0x0B: ("print_unicode", False, False),  # V5+
        0x0C: ("check_unicode", True, False),  # V5+
        0x0D: ("set_true_colour", False, False),  # V6
        0x10: ("move_window", False, False),  # V6
        0x11: ("window_size", False, False),  # V6
        0x12: ("window_style", False, False),  # V6
        0x13: ("get_wind_prop", True, False),  # V6
        0x14: ("scroll_window", False, False),  # V6
        0x15: ("pop_stack", False, False),  # V6
        0x16: ("read_mouse", False, False),  # V6
        0x17: ("mouse_window", False, False),  # V6
        0x18: ("push_stack", False, True),  # V6
        0x19: ("put_wind_prop", False, False),  # V6
        0x1A: ("print_form", False, False),  # V6
        0x1B: ("make_menu", False, True),  # V6
        0x1C: ("picture_table", False, False),  # V6
        0x1D: ("buffer_screen", True, False),  # V6
    }

    def __init__(self, memory: bytes, version: int):
        self.memory = memory
        self.version = version

    def decode(self, address: int) -> Instruction:
        """Decode instruction at given address"""
        pc = address
        opcode_byte = self.memory[pc]
        pc += 1

        # Determine instruction form
        if opcode_byte == 0xBE and self.version >= 5:
            # Extended form
            return self._decode_extended(address, pc)
        elif opcode_byte & 0xC0 == 0xC0:
            # Variable form (11xxxxxx)
            if opcode_byte < 0xE0:
                # 2OP variable form (110xxxxx)
                return self._decode_variable_2op(address, pc, opcode_byte & 0x1F)
            else:
                # VAR variable form (111xxxxx)
                return self._decode_variable_var(address, pc, opcode_byte & 0x1F)
        elif opcode_byte & 0x80 == 0x80:
            # Short form (10xxxxxx)
            return self._decode_short(address, pc, opcode_byte)
        else:
            # Long form (0xxxxxxx)
            return self._decode_long(address, pc, opcode_byte)

    def _decode_short(self, start_addr: int, pc: int, opcode: int) -> Instruction:
        """Decode short form instruction"""
        op_type = (opcode >> 4) & 0x03
        opnum = opcode & 0x0F

        operands = []
        if op_type != 0x03:  # Not 0OP
            if op_type == 0x00:  # Large constant
                operands.append(struct.unpack('>H', self.memory[pc:pc+2])[0])
                pc += 2
            elif op_type == 0x01:  # Small constant
                operands.append(self.memory[pc])
                pc += 1
            elif op_type == 0x02:  # Variable
                operands.append(('var', self.memory[pc]))
                pc += 1

        # Get opcode info
        if op_type == 0x03:  # 0OP
            info = self.SHORT_0OP.get(opnum, (f"0op_{opnum:02x}", False, False))
        else:  # 1OP
            info = self.SHORT_1OP.get(opnum, (f"1op_{opnum:02x}", False, False))

        name, has_store, has_branch = info

        # Version-specific opcode behavior for 0OP instructions:
        # save (0x05) and restore (0x06):
        # - V1-3: branch (no store)
        # - V4+: store (no branch) - but V5+ typically uses extended form save/restore
        if op_type == 0x03 and opnum in [0x05, 0x06]:
            if self.version >= 4:
                has_store = True
                has_branch = False

        # Handle special cases
        if name in ["print", "print_ret"]:
            # Decode inline string
            text, pc = self._decode_string(pc)
            inst = Instruction(start_addr, opcode, name, operands, text=text)
        else:
            inst = Instruction(start_addr, opcode, name, operands)

        # Read store variable if needed
        if has_store:
            inst.store_var = self.memory[pc]
            pc += 1

        # Read branch offset if needed
        if has_branch:
            branch_byte = self.memory[pc]
            pc += 1
            inst.branch_on_true = bool(branch_byte & 0x80)

            if branch_byte & 0x40:
                # Short form branch (6-bit offset)
                offset = branch_byte & 0x3F
            else:
                # Long form branch (14-bit signed offset)
                offset = ((branch_byte & 0x3F) << 8) | self.memory[pc]
                pc += 1
                if offset & 0x2000:  # Sign extend
                    offset |= 0xC000
                offset = struct.unpack('>h', struct.pack('>H', offset))[0]

            inst.branch_offset = offset

        inst.size = pc - start_addr
        return inst

    def _decode_long(self, start_addr: int, pc: int, opcode: int) -> Instruction:
        """Decode long form instruction"""
        opnum = opcode & 0x1F

        operands = []
        # First operand
        if opcode & 0x40:  # Variable
            operands.append(('var', self.memory[pc]))
        else:  # Small constant
            operands.append(self.memory[pc])
        pc += 1

        # Second operand
        if opcode & 0x20:  # Variable
            operands.append(('var', self.memory[pc]))
        else:  # Small constant
            operands.append(self.memory[pc])
        pc += 1

        info = self.LONG_2OP.get(opnum, (f"2op_{opnum:02x}", False, False))
        name, has_store, has_branch = info

        inst = Instruction(start_addr, opcode, name, operands)

        # Read store variable if needed
        if has_store:
            inst.store_var = self.memory[pc]
            pc += 1

        # Read branch offset if needed
        if has_branch:
            branch_byte = self.memory[pc]
            pc += 1
            inst.branch_on_true = bool(branch_byte & 0x80)

            if branch_byte & 0x40:
                offset = branch_byte & 0x3F
            else:
                offset = ((branch_byte & 0x3F) << 8) | self.memory[pc]
                pc += 1
                if offset & 0x2000:
                    offset |= 0xC000
                offset = struct.unpack('>h', struct.pack('>H', offset))[0]

            inst.branch_offset = offset

        inst.size = pc - start_addr
        return inst

    def _decode_variable_2op(self, start_addr: int, pc: int, opnum: int) -> Instruction:
        """Decode variable form 2OP instruction"""
        return self._decode_variable(start_addr, pc, opnum, self.VAR_2OP)

    def _decode_variable_var(self, start_addr: int, pc: int, opnum: int) -> Instruction:
        """Decode variable form VAR instruction"""
        return self._decode_variable(start_addr, pc, opnum, self.VAR_VAR)

    def _decode_variable(self, start_addr: int, pc: int, opnum: int,
                         opcode_table: Dict) -> Instruction:
        """Decode variable form instruction"""
        # Read operand types
        types_byte = self.memory[pc]
        pc += 1

        operands = []
        for i in range(4):
            op_type = (types_byte >> (6 - i * 2)) & 0x03
            if op_type == 0x03:  # Omitted
                break
            elif op_type == 0x00:  # Large constant
                operands.append(struct.unpack('>H', self.memory[pc:pc+2])[0])
                pc += 2
            elif op_type == 0x01:  # Small constant
                operands.append(self.memory[pc])
                pc += 1
            elif op_type == 0x02:  # Variable
                operands.append(('var', self.memory[pc]))
                pc += 1

        # Check for extended operand types (up to 8 operands in call_vs2/vn2)
        if opnum in [0x0C, 0x1A] and len(operands) == 4:
            types_byte = self.memory[pc]
            pc += 1
            for i in range(4):
                op_type = (types_byte >> (6 - i * 2)) & 0x03
                if op_type == 0x03:
                    break
                elif op_type == 0x00:
                    operands.append(struct.unpack('>H', self.memory[pc:pc+2])[0])
                    pc += 2
                elif op_type == 0x01:
                    operands.append(self.memory[pc])
                    pc += 1
                elif op_type == 0x02:
                    operands.append(('var', self.memory[pc]))
                    pc += 1

        info = opcode_table.get(opnum, (f"var_{opnum:02x}", False, False))
        name, has_store, has_branch = info

        # Version-specific opcode behavior:
        # PULL (opcode 0x09 in VAR_VAR table):
        # - V1-5, V8: pull (variable) - operand is target variable, NO store byte
        # - V6-7: pull stack -> (result) - HAS store byte
        if opcode_table == self.VAR_VAR and opnum == 0x09:
            if self.version == 6 or self.version == 7:
                has_store = True

        inst = Instruction(start_addr, opnum | 0xE0 if opcode_table == self.VAR_VAR else opnum | 0xC0,
                          name, operands)

        # Read store variable if needed
        if has_store:
            inst.store_var = self.memory[pc]
            pc += 1

        # Read branch offset if needed
        if has_branch:
            branch_byte = self.memory[pc]
            pc += 1
            inst.branch_on_true = bool(branch_byte & 0x80)

            if branch_byte & 0x40:
                offset = branch_byte & 0x3F
            else:
                offset = ((branch_byte & 0x3F) << 8) | self.memory[pc]
                pc += 1
                if offset & 0x2000:
                    offset |= 0xC000
                offset = struct.unpack('>h', struct.pack('>H', offset))[0]

            inst.branch_offset = offset

        inst.size = pc - start_addr
        return inst

    def _decode_extended(self, start_addr: int, pc: int) -> Instruction:
        """Decode extended form instruction (V5+)"""
        ext_opnum = self.memory[pc]
        pc += 1

        # Read operand types
        types_byte = self.memory[pc]
        pc += 1

        operands = []
        for i in range(4):
            op_type = (types_byte >> (6 - i * 2)) & 0x03
            if op_type == 0x03:
                break
            elif op_type == 0x00:
                operands.append(struct.unpack('>H', self.memory[pc:pc+2])[0])
                pc += 2
            elif op_type == 0x01:
                operands.append(self.memory[pc])
                pc += 1
            elif op_type == 0x02:
                operands.append(('var', self.memory[pc]))
                pc += 1

        info = self.EXTENDED.get(ext_opnum, (f"ext_{ext_opnum:02x}", False, False))
        name, has_store, has_branch = info

        inst = Instruction(start_addr, 0xBE00 | ext_opnum, name, operands)

        # Read store variable if needed
        if has_store:
            inst.store_var = self.memory[pc]
            pc += 1

        # Read branch offset if needed
        if has_branch:
            branch_byte = self.memory[pc]
            pc += 1
            inst.branch_on_true = bool(branch_byte & 0x80)

            if branch_byte & 0x40:
                offset = branch_byte & 0x3F
            else:
                offset = ((branch_byte & 0x3F) << 8) | self.memory[pc]
                pc += 1
                if offset & 0x2000:
                    offset |= 0xC000
                offset = struct.unpack('>h', struct.pack('>H', offset))[0]

            inst.branch_offset = offset

        inst.size = pc - start_addr
        return inst

    def _decode_string(self, pc: int) -> Tuple[str, int]:
        """Decode a Z-string at current PC"""
        # Simplified Z-string decoding
        result = []
        while True:
            word = struct.unpack('>H', self.memory[pc:pc+2])[0]
            pc += 2

            # Extract three 5-bit characters
            chars = [
                (word >> 10) & 0x1F,
                (word >> 5) & 0x1F,
                word & 0x1F
            ]

            for c in chars:
                if c == 0:
                    result.append(' ')
                elif 6 <= c <= 31:
                    # Alphabet A1 (lowercase)
                    result.append(chr(ord('a') + c - 6))

            # Check end bit
            if word & 0x8000:
                break

        return ''.join(result), pc