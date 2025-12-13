#!/usr/bin/env python3
"""
Setun 70 Emulator
=================

A working emulator of the Soviet Setun 70 ternary computer (1970),
reconstructed from archival documentation.

Based on: POLIZ_PROGRAMMING_MANUAL.md
Source: Brusentsov, Zhogolev, Maslov - "General Characteristics of 
        the Small Digital Machine 'Setun 70'" (1970)

Architecture:
- Balanced ternary number system (trits: -1, 0, +1)
- 6-trit syllables (trytes)
- Two-stack POLIZ (Reverse Polish) execution model
- 27 pages × 81 syllables memory

Usage:
    from setun70 import Setun70
    
    vm = Setun70()
    vm.load_program([...])
    vm.run()
    print(vm.operand_stack)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Callable
from enum import IntEnum


# =============================================================================
# BALANCED TERNARY ARITHMETIC
# =============================================================================

class Trit(IntEnum):
    """A single ternary digit."""
    NEG = -1  # Often written as 'T' or 'ī'
    ZERO = 0
    POS = 1


def trits_to_int(trits: List[int]) -> int:
    """Convert balanced ternary trits to decimal integer.
    
    Example: [1, 0, -1, 1, 0, -1] = 1×243 + 0×81 - 1×27 + 1×9 + 0×3 - 1×1 = 224
    """
    result = 0
    for i, t in enumerate(trits):
        result += t * (3 ** (len(trits) - 1 - i))
    return result


def int_to_trits(n: int, width: int = 6) -> List[int]:
    """Convert decimal integer to balanced ternary trits.
    
    Uses the standard balanced ternary conversion algorithm:
    - Divide by 3, remainder determines trit
    - If remainder is 2, use -1 and carry 1
    """
    if n == 0:
        return [0] * width
    
    trits = []
    is_negative = n < 0
    n = abs(n)
    
    for _ in range(width):
        rem = n % 3
        if rem == 0:
            trits.append(0)
        elif rem == 1:
            trits.append(1)
        else:  # rem == 2
            trits.append(-1)
            n += 1
        n //= 3
    
    result = list(reversed(trits))
    
    if is_negative:
        # Negate: flip all trits
        result = [-t for t in result]
    
    return result


def trits_to_str(trits: List[int]) -> str:
    """Convert trits to readable string. -1 shown as 'T'."""
    chars = {-1: 'T', 0: '0', 1: '1'}
    return ''.join(chars[t] for t in trits)


def str_to_trits(s: str) -> List[int]:
    """Parse trit string. 'T' or '-' = -1, '0' = 0, '1' = 1."""
    chars = {'T': -1, '-': -1, '0': 0, '1': 1}
    return [chars[c] for c in s.upper()]


# =============================================================================
# SYLLABLE ENCODING
# =============================================================================

@dataclass
class Syllable:
    """A 6-trit syllable (tryte)."""
    trits: List[int] = field(default_factory=lambda: [0, 0, 0, 0, 0, 0])
    
    def __post_init__(self):
        assert len(self.trits) == 6, "Syllable must be exactly 6 trits"
        assert all(-1 <= t <= 1 for t in self.trits), "Trits must be -1, 0, or 1"
    
    @property
    def is_operation(self) -> bool:
        """True if this syllable encodes an operation (k[0:2] == 00)."""
        return self.trits[0] == 0 and self.trits[1] == 0
    
    @property
    def op_type(self) -> int:
        """Operation type: 0=basic, 1=service, -1=macro."""
        assert self.is_operation
        return self.trits[2]
    
    @property
    def opcode(self) -> int:
        """Operation code (3 trits -> -13 to +13)."""
        assert self.is_operation
        return trits_to_int(self.trits[3:6])
    
    @property
    def addr_length(self) -> int:
        """Address word length: -1=3 syllables, 0=2 syllables, 1=1 syllable."""
        assert not self.is_operation
        return self.trits[0]
    
    @property
    def addr_page_reg(self) -> int:
        """Page register index (-1, 0, or 1)."""
        assert not self.is_operation
        return self.trits[1]
    
    @property
    def addr_offset(self) -> int:
        """Offset within page (4 trits -> -40 to +40)."""
        assert not self.is_operation
        return trits_to_int(self.trits[2:6])
    
    def to_int(self) -> int:
        """Convert syllable to integer value."""
        return trits_to_int(self.trits)
    
    @classmethod
    def from_int(cls, n: int) -> 'Syllable':
        """Create syllable from integer."""
        return cls(int_to_trits(n, 6))
    
    @classmethod
    def from_str(cls, s: str) -> 'Syllable':
        """Create syllable from trit string (e.g., '00001T')."""
        return cls(str_to_trits(s))
    
    @classmethod
    def operation(cls, op_type: int, opcode: int) -> 'Syllable':
        """Create an operation syllable."""
        trits = [0, 0, op_type] + int_to_trits(opcode, 3)
        return cls(trits)
    
    @classmethod
    def address(cls, length: int, page_reg: int, offset: int) -> 'Syllable':
        """Create an address syllable."""
        trits = [length, page_reg] + int_to_trits(offset, 4)
        return cls(trits)
    
    def __repr__(self):
        return f"Syllable({trits_to_str(self.trits)})"


# =============================================================================
# INSTRUCTION SET
# =============================================================================

class Op:
    """Operation codes for Setun 70."""
    
    # Basic operations (type = 0)
    NOP   = 0   # No operation
    ADD   = 1   # T := S + T
    SUB   = 2   # T := S - T
    MUL   = 3   # T := S × T
    DIV   = 4   # T := S ÷ T
    DUP   = 5   # Duplicate T
    DROP  = 6   # Remove T
    SWAP  = 7   # Exchange T and S
    CMP   = 8   # Compare S and T
    JMP   = 9   # Jump
    JZ    = 10  # Jump if zero
    JN    = 11  # Jump if negative
    JP    = 12  # Jump if positive
    CALL  = 13  # Call procedure
    
    # Extended operations (negative opcodes)
    NEG   = -1  # Negate T
    ABS   = -2  # Absolute value
    OVER  = -3  # Copy S to top
    ROT   = -4  # Rotate three
    STORE = -5  # Store to memory
    FETCH = -6  # Fetch from memory
    RET   = -7  # Return from call
    HALT  = -8  # Stop execution
    
    # Additional math operations (negative opcodes continued)
    MOD   = -9   # Modulo: S mod T
    MIN   = -10  # Minimum of S and T
    MAX   = -11  # Maximum of S and T
    SGN   = -12  # Sign of T: returns -1, 0, or 1 (perfect for ternary!)
    NIP   = -13  # Remove second element (a b -- b)
    
    # Service operations (type = 1) for literal push
    # These have opcode that encodes a small literal value
    LIT   = 0   # Literal push (value in next syllable)


# =============================================================================
# SETUN 70 VIRTUAL MACHINE
# =============================================================================

class Setun70:
    """
    Setun 70 Ternary Computer Emulator.
    
    Architecture:
    - Balanced ternary number system
    - 6-trit syllables (trytes)
    - Two-stack POLIZ execution
    - 27 pages × 81 syllables = 2,187 syllable memory
    """
    
    # Memory configuration (from specification)
    NUM_PAGES = 27          # 3^3 pages
    PAGE_SIZE = 81          # 3^4 syllables per page
    NUM_PAGE_REGISTERS = 3  # Page registers indexed -1, 0, 1
    
    def __init__(self, debug: bool = False):
        """Initialize the Setun 70 virtual machine."""
        self.debug = debug
        self.reset()
    
    def reset(self):
        """Reset the machine to initial state."""
        # Two stacks
        self.operand_stack: List[int] = []
        self.return_stack: List[int] = []
        
        # Memory: dict of (page, offset) -> syllable value
        self.memory: Dict[Tuple[int, int], int] = {}
        
        # Page registers: indexed by -1, 0, 1
        self.page_registers: Dict[int, int] = {-1: 0, 0: 1, 1: 2}
        
        # Program counter: (page, offset)
        self.pc_page: int = 0
        self.pc_offset: int = 0
        
        # Execution state
        self.running: bool = False
        self.cycles: int = 0
        self.comparison_flag: int = 0
        
        # Error state
        self.error: Optional[str] = None
    
    # -------------------------------------------------------------------------
    # Stack Operations
    # -------------------------------------------------------------------------
    
    def push(self, value: int):
        """Push value onto operand stack."""
        self.operand_stack.append(value)
    
    def pop(self) -> int:
        """Pop value from operand stack."""
        if not self.operand_stack:
            self.error = "Stack underflow"
            self.running = False
            return 0
        return self.operand_stack.pop()
    
    @property
    def T(self) -> int:
        """Top of stack."""
        return self.operand_stack[-1] if self.operand_stack else 0
    
    @property
    def S(self) -> int:
        """Second element (under-top)."""
        return self.operand_stack[-2] if len(self.operand_stack) >= 2 else 0
    
    def push_return(self, addr: Tuple[int, int]):
        """Push return address onto return stack."""
        # Encode as single integer: page * 100 + offset
        self.return_stack.append(addr[0] * 100 + addr[1])
    
    def pop_return(self) -> Tuple[int, int]:
        """Pop return address from return stack."""
        if not self.return_stack:
            self.error = "Return stack underflow"
            self.running = False
            return (0, 0)
        addr = self.return_stack.pop()
        return (addr // 100, addr % 100)
    
    # -------------------------------------------------------------------------
    # Memory Operations
    # -------------------------------------------------------------------------
    
    def read_memory(self, page: int, offset: int) -> int:
        """Read syllable from memory."""
        return self.memory.get((page, offset), 0)
    
    def write_memory(self, page: int, offset: int, value: int):
        """Write syllable to memory."""
        self.memory[(page, offset)] = value
    
    def resolve_address(self, syllable: Syllable) -> Tuple[int, int]:
        """Resolve address syllable to (page, offset)."""
        page_reg = syllable.addr_page_reg
        page = self.page_registers.get(page_reg, 0)
        offset = syllable.addr_offset
        return (page, offset)
    
    # -------------------------------------------------------------------------
    # Program Loading
    # -------------------------------------------------------------------------
    
    def load_program(self, syllables: List[Syllable], start_page: int = 0, start_offset: int = 0):
        """Load a program into memory."""
        page = start_page
        offset = start_offset
        
        for syl in syllables:
            self.write_memory(page, offset, syl.to_int())
            offset += 1
            if offset >= self.PAGE_SIZE:
                offset = 0
                page += 1
        
        # Set program counter to start
        self.pc_page = start_page
        self.pc_offset = start_offset
    
    def load_data(self, values: List[int], start_page: int, start_offset: int):
        """Load data values into memory."""
        page = start_page
        offset = start_offset
        
        for val in values:
            self.write_memory(page, offset, val)
            offset += 1
            if offset >= self.PAGE_SIZE:
                offset = 0
                page += 1
    
    # -------------------------------------------------------------------------
    # Execution
    # -------------------------------------------------------------------------
    
    def step(self) -> bool:
        """Execute one instruction. Returns True if still running."""
        if not self.running:
            return False
        
        # Fetch syllable at PC
        syl_value = self.read_memory(self.pc_page, self.pc_offset)
        syllable = Syllable.from_int(syl_value)
        
        if self.debug:
            print(f"PC=({self.pc_page},{self.pc_offset}) "
                  f"Syllable={syllable} "
                  f"Stack={self.operand_stack}")
        
        # Advance PC
        self.pc_offset += 1
        if self.pc_offset >= self.PAGE_SIZE:
            self.pc_offset = 0
            self.pc_page += 1
        
        # Execute
        if syllable.is_operation:
            self.execute_operation(syllable)
        else:
            self.execute_address(syllable)
        
        self.cycles += 1
        return self.running
    
    def execute_address(self, syllable: Syllable):
        """Execute an address syllable: push value from memory."""
        page, offset = self.resolve_address(syllable)
        value = self.read_memory(page, offset)
        self.push(value)
    
    def execute_operation(self, syllable: Syllable):
        """Execute an operation syllable."""
        op_type = syllable.op_type
        opcode = syllable.opcode
        
        if op_type == 0:
            self.execute_basic_op(opcode)
        elif op_type == 1:
            self.execute_service_op(opcode)
        elif op_type == -1:
            self.execute_macro_op(opcode)
    
    def execute_basic_op(self, opcode: int):
        """Execute a basic operation."""
        match opcode:
            case Op.NOP:
                pass
            
            case Op.ADD:
                b = self.pop()
                a = self.pop()
                self.push(a + b)
            
            case Op.SUB:
                b = self.pop()
                a = self.pop()
                self.push(a - b)
            
            case Op.MUL:
                b = self.pop()
                a = self.pop()
                self.push(a * b)
            
            case Op.DIV:
                b = self.pop()
                a = self.pop()
                if b == 0:
                    self.error = "Division by zero"
                    self.running = False
                else:
                    # Ternary-style truncation toward zero
                    self.push(int(a / b))
            
            case Op.DUP:
                self.push(self.T)
            
            case Op.DROP:
                self.pop()
            
            case Op.SWAP:
                if len(self.operand_stack) >= 2:
                    self.operand_stack[-1], self.operand_stack[-2] = \
                        self.operand_stack[-2], self.operand_stack[-1]
            
            case Op.CMP:
                b = self.pop()
                a = self.pop()
                if a < b:
                    self.comparison_flag = -1
                    self.push(-1)
                elif a > b:
                    self.comparison_flag = 1
                    self.push(1)
                else:
                    self.comparison_flag = 0
                    self.push(0)
            
            case Op.JMP:
                addr = self.pop()
                self.pc_page = addr // 100
                self.pc_offset = addr % 100
            
            case Op.JZ:
                addr = self.pop()
                cond = self.pop()
                if cond == 0:
                    self.pc_page = addr // 100
                    self.pc_offset = addr % 100
            
            case Op.JN:
                addr = self.pop()
                cond = self.pop()
                if cond < 0:
                    self.pc_page = addr // 100
                    self.pc_offset = addr % 100
            
            case Op.JP:
                addr = self.pop()
                cond = self.pop()
                if cond > 0:
                    self.pc_page = addr // 100
                    self.pc_offset = addr % 100
            
            case Op.CALL:
                addr = self.pop()
                self.push_return((self.pc_page, self.pc_offset))
                self.pc_page = addr // 100
                self.pc_offset = addr % 100
            
            case Op.NEG:
                self.push(-self.pop())
            
            case Op.ABS:
                self.push(abs(self.pop()))
            
            case Op.OVER:
                if len(self.operand_stack) >= 2:
                    self.push(self.operand_stack[-2])
            
            case Op.ROT:
                if len(self.operand_stack) >= 3:
                    a = self.operand_stack[-3]
                    self.operand_stack[-3] = self.operand_stack[-2]
                    self.operand_stack[-2] = self.operand_stack[-1]
                    self.operand_stack[-1] = a
            
            case Op.STORE:
                addr = self.pop()
                val = self.pop()
                page = addr // 100
                offset = addr % 100
                self.write_memory(page, offset, val)
            
            case Op.FETCH:
                addr = self.pop()
                page = addr // 100
                offset = addr % 100
                self.push(self.read_memory(page, offset))
            
            case Op.RET:
                page, offset = self.pop_return()
                self.pc_page = page
                self.pc_offset = offset
            
            case Op.HALT:
                self.running = False
            
            case Op.MOD:
                b = self.pop()
                a = self.pop()
                if b == 0:
                    self.error = "Modulo by zero"
                    self.running = False
                else:
                    self.push(a % b)
            
            case Op.MIN:
                b = self.pop()
                a = self.pop()
                self.push(min(a, b))
            
            case Op.MAX:
                b = self.pop()
                a = self.pop()
                self.push(max(a, b))
            
            case Op.SGN:
                # Sign function: returns -1, 0, or 1 (perfect for ternary!)
                val = self.pop()
                if val < 0:
                    self.push(-1)
                elif val > 0:
                    self.push(1)
                else:
                    self.push(0)
            
            case Op.NIP:
                # Remove second element: (a b -- b)
                if len(self.operand_stack) >= 2:
                    del self.operand_stack[-2]
            
            case _:
                self.error = f"Unknown opcode: {opcode}"
                self.running = False
    
    def execute_service_op(self, opcode: int):
        """Execute a service operation (I/O)."""
        match opcode:
            case 0:  # LIT - push next syllable as literal
                # Read next syllable as literal value
                lit_value = self.read_memory(self.pc_page, self.pc_offset)
                self.pc_offset += 1
                if self.pc_offset >= self.PAGE_SIZE:
                    self.pc_offset = 0
                    self.pc_page += 1
                self.push(lit_value)
            case 1:  # OUT
                # Output top of stack
                val = self.pop()
                print(f"OUT: {val} (ternary: {trits_to_str(int_to_trits(val))})")
            case 2:  # IN
                # Read from input (for now, just push 0)
                self.push(0)
            case 3:  # DEPTH - push stack depth
                self.push(len(self.operand_stack))
            case 4:  # TAND - Ternary AND (min of trits)
                b = self.pop()
                a = self.pop()
                a_trits = int_to_trits(a, 18)
                b_trits = int_to_trits(b, 18)
                result_trits = [min(at, bt) for at, bt in zip(a_trits, b_trits)]
                self.push(trits_to_int(result_trits))
            case 5:  # TOR - Ternary OR (max of trits)
                b = self.pop()
                a = self.pop()
                a_trits = int_to_trits(a, 18)
                b_trits = int_to_trits(b, 18)
                result_trits = [max(at, bt) for at, bt in zip(a_trits, b_trits)]
                self.push(trits_to_int(result_trits))
            case 6:  # TNOT - Ternary NOT (negate each trit)
                val = self.pop()
                val_trits = int_to_trits(val, 18)
                result_trits = [-t for t in val_trits]
                self.push(trits_to_int(result_trits))
            case 7:  # 2DUP - duplicate top two
                if len(self.operand_stack) >= 2:
                    a, b = self.operand_stack[-2], self.operand_stack[-1]
                    self.push(a)
                    self.push(b)
            case 8:  # 2DROP - drop top two
                if len(self.operand_stack) >= 2:
                    self.pop()
                    self.pop()
            case _:
                pass  # Other service ops not implemented
    
    def execute_macro_op(self, opcode: int):
        """Execute a macro operation (user-defined)."""
        # Would dispatch to user-defined routines
        # For now, treat as NOP
        pass
    
    def run(self, max_cycles: int = 10000) -> bool:
        """Run until halt or max cycles. Returns True if completed normally."""
        self.running = True
        self.cycles = 0
        
        while self.running and self.cycles < max_cycles:
            self.step()
        
        if self.cycles >= max_cycles:
            self.error = "Max cycles exceeded"
            return False
        
        return self.error is None
    
    # -------------------------------------------------------------------------
    # Debugging
    # -------------------------------------------------------------------------
    
    def dump_state(self):
        """Print current machine state."""
        print("=" * 50)
        print("SETUN 70 STATE")
        print("=" * 50)
        print(f"PC: page={self.pc_page}, offset={self.pc_offset}")
        print(f"Cycles: {self.cycles}")
        print(f"Running: {self.running}")
        print(f"Error: {self.error}")
        print(f"Operand Stack: {self.operand_stack}")
        print(f"Return Stack: {self.return_stack}")
        print(f"Page Registers: {self.page_registers}")
        print(f"Comparison Flag: {self.comparison_flag}")
        print("=" * 50)


# =============================================================================
# ASSEMBLER
# =============================================================================

class Setun70Assembler:
    """Simple assembler for Setun 70 POLIZ programs."""
    
    MNEMONICS = {
        'NOP': (0, Op.NOP),
        'ADD': (0, Op.ADD),
        'SUB': (0, Op.SUB),
        'MUL': (0, Op.MUL),
        'DIV': (0, Op.DIV),
        'DUP': (0, Op.DUP),
        'DROP': (0, Op.DROP),
        'SWAP': (0, Op.SWAP),
        'CMP': (0, Op.CMP),
        'JMP': (0, Op.JMP),
        'JZ': (0, Op.JZ),
        'JN': (0, Op.JN),
        'JP': (0, Op.JP),
        'CALL': (0, Op.CALL),
        'NEG': (0, Op.NEG),
        'ABS': (0, Op.ABS),
        'OVER': (0, Op.OVER),
        'ROT': (0, Op.ROT),
        'STORE': (0, Op.STORE),
        'FETCH': (0, Op.FETCH),
        'RET': (0, Op.RET),
        'HALT': (0, Op.HALT),
        # New math operations
        'MOD': (0, Op.MOD),
        'MIN': (0, Op.MIN),
        'MAX': (0, Op.MAX),
        'SGN': (0, Op.SGN),
        'NIP': (0, Op.NIP),
        # Service operations
        'OUT': (1, 1),
        'IN': (1, 2),
        'DEPTH': (1, 3),
        'TAND': (1, 4),
        'TOR': (1, 5),
        'TNOT': (1, 6),
        '2DUP': (1, 7),
        '2DROP': (1, 8),
    }
    
    def __init__(self):
        self.labels: Dict[str, int] = {}
        self.current_address = 0
    
    def assemble(self, source: str) -> List[Syllable]:
        """Assemble source code to syllables."""
        syllables = []
        lines = source.strip().split('\n')
        
        # First pass: collect labels (accounting for LIT taking 2 syllables)
        self.current_address = 0
        for line in lines:
            line = line.split(';')[0].strip()  # Remove comments
            if not line:
                continue
            
            if ':' in line:
                label, rest = line.split(':', 1)
                self.labels[label.strip()] = self.current_address
                line = rest.strip()
            
            if line:
                parts = line.upper().split()
                if parts[0] == 'LIT':
                    self.current_address += 2  # LIT takes 2 syllables
                else:
                    self.current_address += 1
        
        # Second pass: generate syllables
        self.current_address = 0
        for line in lines:
            line = line.split(';')[0].strip()
            if not line:
                continue
            
            if ':' in line:
                _, line = line.split(':', 1)
                line = line.strip()
            
            if not line:
                continue
            
            result = self.parse_instruction(line)
            if isinstance(result, list):
                syllables.extend(result)
                self.current_address += len(result)
            else:
                syllables.append(result)
                self.current_address += 1
        
        return syllables
    
    def parse_instruction(self, line: str):
        """Parse a single instruction. Returns Syllable or list of Syllables."""
        parts = line.upper().split()
        mnemonic = parts[0]
        
        if mnemonic in self.MNEMONICS:
            op_type, opcode = self.MNEMONICS[mnemonic]
            return Syllable.operation(op_type, opcode)
        
        elif mnemonic == 'LIT':
            # LIT <value> - push literal (2 syllables: LIT op + value)
            val = self.parse_value(parts[1])
            return [
                Syllable.operation(1, 0),  # LIT instruction
                Syllable.from_int(val),    # Value
            ]
        
        elif mnemonic == 'PUSH':
            # Alias for LIT
            val = self.parse_value(parts[1])
            return [
                Syllable.operation(1, 0),
                Syllable.from_int(val),
            ]
        
        elif mnemonic == 'ADDR':
            # ADDR <page_reg> <offset> or ADDR <label>
            if len(parts) == 2:
                if parts[1] in self.labels:
                    addr = self.labels[parts[1]]
                    return Syllable.address(0, 1, addr)
                else:
                    offset = self.parse_value(parts[1])
                    return Syllable.address(0, 1, offset)
            else:
                page_reg = self.parse_value(parts[1])
                offset = self.parse_value(parts[2])
                return Syllable.address(0, page_reg, offset)
        
        elif mnemonic.startswith('.'):
            return self.parse_directive(mnemonic, parts[1:])
        
        else:
            raise ValueError(f"Unknown instruction: {line}")
    
    def parse_value(self, s: str) -> int:
        """Parse a numeric value."""
        s = s.strip()
        if s in self.labels:
            return self.labels[s]
        if s.startswith('0T') or s.startswith('T'):
            return trits_to_int(str_to_trits(s.replace('0T', '')))
        return int(s)
    
    def parse_directive(self, directive: str, args: List[str]) -> Syllable:
        """Parse an assembler directive."""
        match directive:
            case '.WORD':
                val = self.parse_value(args[0]) if args else 0
                return Syllable.from_int(val)
            case _:
                return Syllable.from_int(0)


# =============================================================================
# DEMONSTRATION PROGRAMS
# =============================================================================

def lit(value: int) -> List[Syllable]:
    """Create a literal push sequence: LIT instruction + value."""
    return [
        Syllable.operation(1, 0),  # LIT (service op 0)
        Syllable.from_int(value),  # Literal value
    ]


def demo_arithmetic():
    """Demonstrate basic arithmetic: (3 + 4) × 5 = 35"""
    print("\n" + "=" * 60)
    print("DEMO: Arithmetic (3 + 4) x 5 = 35")
    print("=" * 60)
    
    vm = Setun70(debug=True)
    
    # Program: 3 4 + 5 × HALT
    # POLIZ: Push 3, Push 4, ADD, Push 5, MUL, OUT, HALT
    # Use LIT instruction to push literals
    program = [
        *lit(3),                        # LIT 3
        *lit(4),                        # LIT 4
        Syllable.operation(0, Op.ADD),  # ADD
        *lit(5),                        # LIT 5
        Syllable.operation(0, Op.MUL),  # MUL
        Syllable.operation(1, 1),       # OUT
        Syllable.operation(0, Op.HALT), # HALT
    ]
    
    vm.load_program(program)
    vm.run()
    
    print(f"\nResult: {vm.operand_stack}")
    print(f"Expected: 35")
    vm.dump_state()


def demo_expression():
    """Demonstrate: (10 + 20) x (5 - 2) = 90"""
    print("\n" + "=" * 60)
    print("DEMO: Expression (10 + 20) x (5 - 2) = 90")
    print("=" * 60)
    
    vm = Setun70(debug=False)
    
    # POLIZ: 10 20 + 5 2 - × OUT HALT
    program = [
        *lit(10),                       # LIT 10
        *lit(20),                       # LIT 20
        Syllable.operation(0, Op.ADD),  # ADD -> 30
        *lit(5),                        # LIT 5
        *lit(2),                        # LIT 2
        Syllable.operation(0, Op.SUB),  # SUB -> 3
        Syllable.operation(0, Op.MUL),  # MUL -> 90
        Syllable.operation(1, 1),       # OUT
        Syllable.operation(0, Op.HALT), # HALT
    ]
    
    vm.load_program(program)
    vm.run()
    
    print(f"\nResult: {vm.operand_stack}")
    print(f"Expected: 90")


def demo_ternary():
    """Demonstrate balanced ternary arithmetic."""
    print("\n" + "=" * 60)
    print("DEMO: Balanced Ternary Arithmetic")
    print("=" * 60)
    
    # Show ternary representations
    for n in [-13, -5, -1, 0, 1, 5, 13, 100, 224]:
        trits = int_to_trits(n)
        back = trits_to_int(trits)
        print(f"{n:4d} -> {trits_to_str(trits)} -> {back}")
    
    print("\nBalanced ternary features:")
    print("- Negation: just flip all trits")
    n = 13
    trits = int_to_trits(n)
    neg_trits = [-t for t in trits]
    print(f"  {n} = {trits_to_str(trits)}")
    print(f"  -{n} = {trits_to_str(neg_trits)} = {trits_to_int(neg_trits)}")


def demo_assembler():
    """Demonstrate the assembler."""
    print("\n" + "=" * 60)
    print("DEMO: Assembler")
    print("=" * 60)
    
    source = """
    ; Calculate 10 + 20 and output
    LIT 10      ; Push 10 (LIT instruction + value)
    LIT 20      ; Push 20
    ADD         ; Add them -> 30
    OUT         ; Output result
    HALT        ; Stop
    """
    
    print("Source:")
    print(source)
    
    asm = Setun70Assembler()
    program = asm.assemble(source)
    
    print("\nAssembled syllables:")
    for i, syl in enumerate(program):
        print(f"  {i}: {syl}")
    
    vm = Setun70()
    vm.load_program(program)
    vm.run()
    
    print(f"\nFinal stack: {vm.operand_stack}")


def demo_factorial():
    """Demonstrate: Calculate 5! = 120 (iterative)"""
    print("\n" + "=" * 60)
    print("DEMO: Factorial 5! = 120")
    print("=" * 60)
    
    vm = Setun70(debug=False)
    
    # Simpler: direct calculation 1x2x3x4x5
    program = [
        *lit(1),                        # LIT 1
        *lit(2),                        # LIT 2
        Syllable.operation(0, Op.MUL),  # 1x2 = 2
        *lit(3),                        # LIT 3
        Syllable.operation(0, Op.MUL),  # 2x3 = 6
        *lit(4),                        # LIT 4
        Syllable.operation(0, Op.MUL),  # 6x4 = 24
        *lit(5),                        # LIT 5
        Syllable.operation(0, Op.MUL),  # 24x5 = 120
        Syllable.operation(1, 1),       # OUT
        Syllable.operation(0, Op.HALT), # HALT
    ]
    
    vm.load_program(program)
    vm.run()
    
    print(f"5! = {vm.operand_stack[0] if vm.operand_stack else 'ERROR'}")
    print(f"Expected: 120")
    print(f"Cycles: {vm.cycles}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Main entry point for the Setun 70 emulator."""
    import sys
    
    banner = """
+==================================================================+
|                     SETUN 70 EMULATOR                            |
|         Soviet Ternary Computer (1970) - Reconstructed           |
|                                                                  |
|  Based on: Brusentsov, Zhogolev, Maslov                          |
|  "General Characteristics of the Small Digital Machine           |
|   'Setun 70'" (1970)                                             |
|                                                                  |
|  Architecture:                                                   |
|    - Balanced ternary (trits: -1, 0, +1)                         |
|    - 6-trit syllables (729 values each)                          |
|    - Two-stack POLIZ execution                                   |
|    - 27 pages x 81 syllables memory                              |
+==================================================================+
    """
    
    if len(sys.argv) > 1:
        # Run a file
        filename = sys.argv[1]
        print(banner)
        print(f"Loading: {filename}")
        
        with open(filename, 'r') as f:
            source = f.read()
        
        asm = Setun70Assembler()
        program = asm.assemble(source)
        
        vm = Setun70(debug='--debug' in sys.argv)
        vm.load_program(program)
        vm.run()
        
        if vm.error:
            print(f"Error: {vm.error}")
            sys.exit(1)
        
        print(f"\nCompleted in {vm.cycles} cycles")
        if vm.operand_stack:
            print(f"Stack: {vm.operand_stack}")
    else:
        # Run demos
        print(banner)
        demo_ternary()
        demo_arithmetic()
        demo_expression()
        demo_factorial()
        demo_assembler()
        
        print("\n" + "=" * 60)
        print("All demos completed successfully!")
        print("=" * 60)
        print("\nUsage: setun70 [program.s70] [--debug]")


if __name__ == "__main__":
    main()

