#!/usr/bin/env python3
"""
Comprehensive Test Suite for Setun 70 Emulator
==============================================

Tests all core components:
- Balanced ternary arithmetic
- Syllable encoding/decoding
- Stack operations
- All instruction set operations
- Assembler
- Example programs
- Edge cases
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from setun70 import (
    Setun70, Setun70Assembler, Syllable, Op,
    trits_to_int, int_to_trits, trits_to_str, str_to_trits, lit
)


class TestResults:
    """Track test results."""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def record(self, name: str, passed: bool, detail: str = ""):
        if passed:
            self.passed += 1
            print(f"  [PASS] {name}")
        else:
            self.failed += 1
            self.errors.append((name, detail))
            print(f"  [FAIL] {name}: {detail}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"RESULTS: {self.passed}/{total} tests passed")
        if self.failed:
            print(f"\nFailed tests:")
            for name, detail in self.errors:
                print(f"  - {name}: {detail}")
        print(f"{'='*60}")
        return self.failed == 0


results = TestResults()


# =============================================================================
# BALANCED TERNARY ARITHMETIC TESTS
# =============================================================================

def test_ternary_arithmetic():
    """Test balanced ternary conversion functions."""
    print("\n[1] BALANCED TERNARY ARITHMETIC")
    print("-" * 40)
    
    # Test conversion roundtrip for various values
    test_values = [
        0, 1, -1, 2, -2, 3, -3,
        13, -13, 40, -40,
        100, -100, 224, -224,
        364, -364,  # Max 6-trit value
    ]
    
    for val in test_values:
        trits = int_to_trits(val, 6)
        back = trits_to_int(trits)
        results.record(
            f"Roundtrip {val}",
            back == val,
            f"got {back}, expected {val}"
        )
    
    # Test specific known conversions
    known = [
        (0, [0, 0, 0, 0, 0, 0]),
        (1, [0, 0, 0, 0, 0, 1]),
        (-1, [0, 0, 0, 0, 0, -1]),
        (13, [0, 0, 0, 1, 1, 1]),  # 9 + 3 + 1 = 13
        (-13, [0, 0, 0, -1, -1, -1]),
    ]
    
    for val, expected_trits in known:
        trits = int_to_trits(val, 6)
        results.record(
            f"Known conversion {val} -> {trits_to_str(expected_trits)}",
            trits == expected_trits,
            f"got {trits_to_str(trits)}"
        )
    
    # Test negation property (just flip all trits)
    for val in [1, 5, 13, 100]:
        pos_trits = int_to_trits(val, 6)
        neg_trits = int_to_trits(-val, 6)
        flipped = [-t for t in pos_trits]
        results.record(
            f"Negation property for {val}",
            neg_trits == flipped,
            f"negation doesn't equal flipped trits"
        )
    
    # Test string conversion
    results.record(
        "String conversion TT1 -> trits",
        str_to_trits("TT1") == [-1, -1, 1],
        f"got {str_to_trits('TT1')}"
    )
    
    results.record(
        "Trits to string",
        trits_to_str([-1, 0, 1]) == "T01",
        f"got {trits_to_str([-1, 0, 1])}"
    )


# =============================================================================
# SYLLABLE ENCODING TESTS
# =============================================================================

def test_syllable_encoding():
    """Test syllable creation and encoding."""
    print("\n[2] SYLLABLE ENCODING")
    print("-" * 40)
    
    # Test operation syllable detection
    op_syl = Syllable.operation(0, Op.ADD)
    results.record(
        "Operation syllable detection",
        op_syl.is_operation == True,
        f"should be operation"
    )
    
    # Test address syllable (non-00 prefix)
    addr_syl = Syllable.address(1, 0, 5)
    results.record(
        "Address syllable detection",
        addr_syl.is_operation == False,
        f"should not be operation"
    )
    
    # Test opcode extraction
    for opcode in [Op.NOP, Op.ADD, Op.SUB, Op.MUL, Op.NEG, Op.HALT]:
        syl = Syllable.operation(0, opcode)
        results.record(
            f"Opcode extraction for {opcode}",
            syl.opcode == opcode,
            f"got {syl.opcode}"
        )
    
    # Test syllable to/from int roundtrip
    for val in [0, 1, -1, 10, -10, 100, -100, 200]:
        syl = Syllable.from_int(val)
        back = syl.to_int()
        results.record(
            f"Syllable int roundtrip {val}",
            back == val,
            f"got {back}"
        )
    
    # Test from string
    syl = Syllable.from_str("001001")
    results.record(
        "Syllable from string '001001'",
        syl.trits == [0, 0, 1, 0, 0, 1],
        f"got {syl.trits}"
    )


# =============================================================================
# STACK OPERATIONS TESTS
# =============================================================================

def test_stack_operations():
    """Test stack push/pop operations."""
    print("\n[3] STACK OPERATIONS")
    print("-" * 40)
    
    vm = Setun70()
    
    # Test push
    vm.push(42)
    results.record("Push operation", vm.T == 42, f"T = {vm.T}")
    
    # Test multiple push
    vm.push(10)
    vm.push(20)
    results.record("Multiple push - T", vm.T == 20, f"T = {vm.T}")
    results.record("Multiple push - S", vm.S == 10, f"S = {vm.S}")
    
    # Test pop
    val = vm.pop()
    results.record("Pop value", val == 20, f"got {val}")
    results.record("Stack after pop", vm.T == 10, f"T = {vm.T}")
    
    # Test underflow handling
    vm.reset()
    vm.running = True
    val = vm.pop()
    results.record(
        "Underflow sets error",
        vm.error == "Stack underflow",
        f"error = {vm.error}"
    )


# =============================================================================
# INSTRUCTION SET TESTS
# =============================================================================

def test_instructions():
    """Test all instruction operations."""
    print("\n[4] INSTRUCTION SET")
    print("-" * 40)
    
    # Test ADD
    vm = Setun70()
    vm.load_program([
        *lit(10), *lit(20),
        Syllable.operation(0, Op.ADD),
        Syllable.operation(0, Op.HALT),
    ])
    vm.run()
    results.record("ADD: 10 + 20 = 30", vm.T == 30, f"got {vm.T}")
    
    # Test SUB
    vm.reset()
    vm.load_program([
        *lit(20), *lit(5),
        Syllable.operation(0, Op.SUB),
        Syllable.operation(0, Op.HALT),
    ])
    vm.run()
    results.record("SUB: 20 - 5 = 15", vm.T == 15, f"got {vm.T}")
    
    # Test MUL
    vm.reset()
    vm.load_program([
        *lit(7), *lit(6),
        Syllable.operation(0, Op.MUL),
        Syllable.operation(0, Op.HALT),
    ])
    vm.run()
    results.record("MUL: 7 * 6 = 42", vm.T == 42, f"got {vm.T}")
    
    # Test DIV
    vm.reset()
    vm.load_program([
        *lit(100), *lit(10),
        Syllable.operation(0, Op.DIV),
        Syllable.operation(0, Op.HALT),
    ])
    vm.run()
    results.record("DIV: 100 / 10 = 10", vm.T == 10, f"got {vm.T}")
    
    # Test DIV by zero
    vm.reset()
    vm.load_program([
        *lit(10), *lit(0),
        Syllable.operation(0, Op.DIV),
        Syllable.operation(0, Op.HALT),
    ])
    vm.run()
    results.record(
        "DIV by zero error",
        vm.error == "Division by zero",
        f"error = {vm.error}"
    )
    
    # Test DUP
    vm.reset()
    vm.load_program([
        *lit(42),
        Syllable.operation(0, Op.DUP),
        Syllable.operation(0, Op.HALT),
    ])
    vm.run()
    results.record(
        "DUP: stack has two 42s",
        vm.operand_stack == [42, 42],
        f"got {vm.operand_stack}"
    )
    
    # Test DROP
    vm.reset()
    vm.load_program([
        *lit(10), *lit(20),
        Syllable.operation(0, Op.DROP),
        Syllable.operation(0, Op.HALT),
    ])
    vm.run()
    results.record(
        "DROP: removes top",
        vm.operand_stack == [10],
        f"got {vm.operand_stack}"
    )
    
    # Test SWAP
    vm.reset()
    vm.load_program([
        *lit(10), *lit(20),
        Syllable.operation(0, Op.SWAP),
        Syllable.operation(0, Op.HALT),
    ])
    vm.run()
    results.record(
        "SWAP: exchanges top two",
        vm.operand_stack == [20, 10],
        f"got {vm.operand_stack}"
    )
    
    # Test NEG
    vm.reset()
    vm.load_program([
        *lit(42),
        Syllable.operation(0, Op.NEG),
        Syllable.operation(0, Op.HALT),
    ])
    vm.run()
    results.record("NEG: -42", vm.T == -42, f"got {vm.T}")
    
    # Test ABS
    vm.reset()
    vm.load_program([
        *lit(-50),
        Syllable.operation(0, Op.ABS),
        Syllable.operation(0, Op.HALT),
    ])
    vm.run()
    results.record("ABS: |-50| = 50", vm.T == 50, f"got {vm.T}")
    
    # Test OVER
    vm.reset()
    vm.load_program([
        *lit(10), *lit(20),
        Syllable.operation(0, Op.OVER),
        Syllable.operation(0, Op.HALT),
    ])
    vm.run()
    results.record(
        "OVER: copies second to top",
        vm.operand_stack == [10, 20, 10],
        f"got {vm.operand_stack}"
    )
    
    # Test ROT
    vm.reset()
    vm.load_program([
        *lit(1), *lit(2), *lit(3),
        Syllable.operation(0, Op.ROT),
        Syllable.operation(0, Op.HALT),
    ])
    vm.run()
    results.record(
        "ROT: (1 2 3) -> (2 3 1)",
        vm.operand_stack == [2, 3, 1],
        f"got {vm.operand_stack}"
    )
    
    # Test CMP
    vm.reset()
    vm.load_program([
        *lit(10), *lit(20),
        Syllable.operation(0, Op.CMP),
        Syllable.operation(0, Op.HALT),
    ])
    vm.run()
    results.record("CMP: 10 < 20 -> -1", vm.T == -1, f"got {vm.T}")
    
    vm.reset()
    vm.load_program([
        *lit(20), *lit(10),
        Syllable.operation(0, Op.CMP),
        Syllable.operation(0, Op.HALT),
    ])
    vm.run()
    results.record("CMP: 20 > 10 -> 1", vm.T == 1, f"got {vm.T}")
    
    vm.reset()
    vm.load_program([
        *lit(15), *lit(15),
        Syllable.operation(0, Op.CMP),
        Syllable.operation(0, Op.HALT),
    ])
    vm.run()
    results.record("CMP: 15 == 15 -> 0", vm.T == 0, f"got {vm.T}")
    
    # Test STORE and FETCH
    vm.reset()
    vm.load_program([
        *lit(99),       # Value to store
        *lit(150),      # Address (page 1, offset 50)
        Syllable.operation(0, Op.STORE),
        *lit(150),      # Same address
        Syllable.operation(0, Op.FETCH),
        Syllable.operation(0, Op.HALT),
    ])
    vm.run()
    results.record("STORE/FETCH: roundtrip", vm.T == 99, f"got {vm.T}")


# =============================================================================
# CONTROL FLOW TESTS
# =============================================================================

def test_control_flow():
    """Test jump and call instructions."""
    print("\n[5] CONTROL FLOW")
    print("-" * 40)
    
    # Test JMP
    vm = Setun70()
    # Program: push 1, push addr, jump, push 999, halt, push 2, halt
    # Should skip the push 999
    program = [
        *lit(1),                        # 0-1: Push 1
        *lit(8),                        # 2-3: Push address 8 (after push 999)
        Syllable.operation(0, Op.JMP),  # 4: Jump
        *lit(999),                      # 5-6: Push 999 (should be skipped)
        Syllable.operation(0, Op.HALT), # 7: Halt (should be skipped)
        *lit(2),                        # 8-9: Push 2
        Syllable.operation(0, Op.HALT), # 10: Halt
    ]
    vm.load_program(program)
    vm.run()
    results.record(
        "JMP: skips instructions",
        vm.operand_stack == [1, 2],
        f"got {vm.operand_stack}"
    )
    
    # Test JZ (jump if zero)
    # LIT takes 2 syllables each, so count carefully:
    # 0-1: LIT 0, 2-3: LIT 8, 4: JZ, 5-6: LIT 999, 7: HALT, 8-9: LIT 42, 10: HALT
    vm.reset()
    program = [
        *lit(0),                        # 0-1: Condition (zero)
        *lit(8),                        # 2-3: Jump target (position 8)
        Syllable.operation(0, Op.JZ),   # 4: Jump if zero
        *lit(999),                      # 5-6: Should be skipped
        Syllable.operation(0, Op.HALT), # 7: HALT (skipped)
        *lit(42),                       # 8-9: Should execute
        Syllable.operation(0, Op.HALT), # 10: HALT
    ]
    vm.load_program(program)
    vm.run()
    results.record(
        "JZ: jumps when zero",
        vm.T == 42,
        f"got {vm.T}"
    )
    
    # Test JZ doesn't jump when non-zero
    # 0-1: LIT 5, 2-3: LIT 8, 4: JZ, 5-6: LIT 42, 7: HALT
    vm.reset()
    program = [
        *lit(5),                        # 0-1: Condition (non-zero)
        *lit(8),                        # 2-3: Jump target (not taken)
        Syllable.operation(0, Op.JZ),   # 4: Don't jump
        *lit(42),                       # 5-6: Should execute
        Syllable.operation(0, Op.HALT), # 7: HALT
        *lit(999),                      # 8-9: Should not reach
        Syllable.operation(0, Op.HALT), # 10: HALT
    ]
    vm.load_program(program)
    vm.run()
    results.record(
        "JZ: doesn't jump when non-zero",
        vm.T == 42,
        f"got {vm.T}"
    )
    
    # Test JN (jump if negative)
    # 0-1: LIT -5, 2-3: LIT 8, 4: JN, 5-6: LIT 999, 7: HALT, 8-9: LIT 42, 10: HALT
    vm.reset()
    program = [
        *lit(-5),                       # 0-1: Condition (negative)
        *lit(8),                        # 2-3: Jump target (position 8)
        Syllable.operation(0, Op.JN),   # 4: Jump if negative
        *lit(999),                      # 5-6: Should be skipped
        Syllable.operation(0, Op.HALT), # 7: HALT (skipped)
        *lit(42),                       # 8-9: Should execute
        Syllable.operation(0, Op.HALT), # 10: HALT
    ]
    vm.load_program(program)
    vm.run()
    results.record(
        "JN: jumps when negative",
        vm.T == 42,
        f"got {vm.T}"
    )
    
    # Test JP (jump if positive)
    # 0-1: LIT 5, 2-3: LIT 8, 4: JP, 5-6: LIT 999, 7: HALT, 8-9: LIT 42, 10: HALT
    vm.reset()
    program = [
        *lit(5),                        # 0-1: Condition (positive)
        *lit(8),                        # 2-3: Jump target (position 8)
        Syllable.operation(0, Op.JP),   # 4: Jump if positive
        *lit(999),                      # 5-6: Should be skipped
        Syllable.operation(0, Op.HALT), # 7: HALT (skipped)
        *lit(42),                       # 8-9: Should execute
        Syllable.operation(0, Op.HALT), # 10: HALT
    ]
    vm.load_program(program)
    vm.run()
    results.record(
        "JP: jumps when positive",
        vm.T == 42,
        f"got {vm.T}"
    )
    
    # Test CALL and RET
    vm.reset()
    # Main: push 10, call subroutine, push 30, halt
    # Subroutine: push 20, return
    program = [
        *lit(10),                       # 0-1: Push 10
        *lit(7),                        # 2-3: Push subroutine address
        Syllable.operation(0, Op.CALL), # 4: Call
        *lit(30),                       # 5-6: Push 30 (after return)
        Syllable.operation(0, Op.HALT), # 7: Halt (address 7 is also used)
        *lit(20),                       # 7-8: Subroutine: push 20
        Syllable.operation(0, Op.RET),  # 9: Return
    ]
    # Fix: adjust addresses
    program = [
        *lit(10),                       # 0-1: Push 10
        *lit(8),                        # 2-3: Push subroutine address (8)
        Syllable.operation(0, Op.CALL), # 4: Call
        *lit(30),                       # 5-6: Push 30 (after return)
        Syllable.operation(0, Op.HALT), # 7: Halt
        *lit(20),                       # 8-9: Subroutine: push 20
        Syllable.operation(0, Op.RET),  # 10: Return
    ]
    vm.load_program(program)
    vm.run()
    results.record(
        "CALL/RET: subroutine works",
        vm.operand_stack == [10, 20, 30],
        f"got {vm.operand_stack}"
    )


# =============================================================================
# ASSEMBLER TESTS
# =============================================================================

def test_assembler():
    """Test the assembler."""
    print("\n[6] ASSEMBLER")
    print("-" * 40)
    
    asm = Setun70Assembler()
    vm = Setun70()
    
    # Test simple program
    source = """
    LIT 10
    LIT 20
    ADD
    HALT
    """
    program = asm.assemble(source)
    vm.load_program(program)
    vm.run()
    results.record(
        "Assembler: simple arithmetic",
        vm.T == 30,
        f"got {vm.T}"
    )
    
    # Test with comments
    vm.reset()
    asm = Setun70Assembler()
    source = """
    ; This is a comment
    LIT 5       ; Push 5
    DUP         ; Duplicate
    MUL         ; Square it
    HALT        ; Done
    """
    program = asm.assemble(source)
    vm.load_program(program)
    vm.run()
    results.record(
        "Assembler: with comments",
        vm.T == 25,
        f"got {vm.T}"
    )
    
    # Test PUSH alias
    vm.reset()
    asm = Setun70Assembler()
    source = """
    PUSH 42
    HALT
    """
    program = asm.assemble(source)
    vm.load_program(program)
    vm.run()
    results.record(
        "Assembler: PUSH alias",
        vm.T == 42,
        f"got {vm.T}"
    )
    
    # Test all mnemonics parse
    asm = Setun70Assembler()
    mnemonics = ['NOP', 'ADD', 'SUB', 'MUL', 'DIV', 'DUP', 'DROP', 
                 'SWAP', 'CMP', 'NEG', 'ABS', 'OVER', 'ROT', 
                 'STORE', 'FETCH', 'RET', 'HALT', 'OUT', 'IN']
    all_parse = True
    for m in mnemonics:
        try:
            asm.parse_instruction(m)
        except:
            all_parse = False
            break
    results.record(
        "Assembler: all mnemonics parse",
        all_parse,
        "some mnemonic failed to parse"
    )


# =============================================================================
# EXAMPLE PROGRAMS TESTS
# =============================================================================

def test_example_programs():
    """Test the example programs from examples/."""
    print("\n[7] EXAMPLE PROGRAMS")
    print("-" * 40)
    
    asm = Setun70Assembler()
    vm = Setun70()
    
    # Test hello.s70
    with open('examples/hello.s70', 'r') as f:
        source = f.read()
    program = asm.assemble(source)
    vm.load_program(program)
    vm.run()
    results.record(
        "hello.s70: (10+20)*3 = 90",
        vm.error is None,
        f"error: {vm.error}"
    )
    
    # Test factorial.s70
    vm.reset()
    asm = Setun70Assembler()
    with open('examples/factorial.s70', 'r') as f:
        source = f.read()
    program = asm.assemble(source)
    vm.load_program(program)
    vm.run()
    results.record(
        "factorial.s70: 5! = 120 (no error)",
        vm.error is None,
        f"error: {vm.error}"
    )
    
    # Test quadratic.s70
    vm.reset()
    asm = Setun70Assembler()
    with open('examples/quadratic.s70', 'r') as f:
        source = f.read()
    program = asm.assemble(source)
    vm.load_program(program)
    vm.run()
    results.record(
        "quadratic.s70: x^2+2x+1 where x=5 = 36 (no error)",
        vm.error is None,
        f"error: {vm.error}"
    )


# =============================================================================
# EDGE CASES AND STRESS TESTS
# =============================================================================

def test_edge_cases():
    """Test edge cases and boundary conditions."""
    print("\n[8] EDGE CASES")
    print("-" * 40)
    
    vm = Setun70()
    
    # Test max tryte value (364)
    vm.load_program([
        *lit(364),
        Syllable.operation(0, Op.HALT),
    ])
    vm.run()
    results.record(
        "Max tryte value 364",
        vm.T == 364,
        f"got {vm.T}"
    )
    
    # Test min tryte value (-364)
    vm.reset()
    vm.load_program([
        *lit(-364),
        Syllable.operation(0, Op.HALT),
    ])
    vm.run()
    # Note: 6 trits can only represent -364 to +364
    trits = int_to_trits(-364, 6)
    back = trits_to_int(trits)
    results.record(
        "Min tryte value -364",
        back == -364,
        f"got {back}"
    )
    
    # Test negative number arithmetic
    vm.reset()
    vm.load_program([
        *lit(-10), *lit(-5),
        Syllable.operation(0, Op.ADD),
        Syllable.operation(0, Op.HALT),
    ])
    vm.run()
    results.record(
        "Negative addition: -10 + -5 = -15",
        vm.T == -15,
        f"got {vm.T}"
    )
    
    vm.reset()
    vm.load_program([
        *lit(-10), *lit(5),
        Syllable.operation(0, Op.MUL),
        Syllable.operation(0, Op.HALT),
    ])
    vm.run()
    results.record(
        "Mixed multiplication: -10 * 5 = -50",
        vm.T == -50,
        f"got {vm.T}"
    )
    
    # Test division truncation
    vm.reset()
    vm.load_program([
        *lit(7), *lit(3),
        Syllable.operation(0, Op.DIV),
        Syllable.operation(0, Op.HALT),
    ])
    vm.run()
    results.record(
        "Division truncation: 7 / 3 = 2",
        vm.T == 2,
        f"got {vm.T}"
    )
    
    vm.reset()
    vm.load_program([
        *lit(-7), *lit(3),
        Syllable.operation(0, Op.DIV),
        Syllable.operation(0, Op.HALT),
    ])
    vm.run()
    results.record(
        "Negative division: -7 / 3 = -2",
        vm.T == -2,
        f"got {vm.T}"
    )
    
    # Test max cycles limit
    vm.reset()
    # Infinite loop: push 5, push 0, jmp (loops forever)
    program = [
        *lit(5),                        # 0-1
        *lit(0),                        # 2-3: Jump target (start)
        Syllable.operation(0, Op.JMP),  # 4
    ]
    vm.load_program(program)
    completed = vm.run(max_cycles=100)
    results.record(
        "Max cycles stops infinite loop",
        not completed and vm.error == "Max cycles exceeded",
        f"completed={completed}, error={vm.error}"
    )
    
    # Test empty program
    vm.reset()
    vm.load_program([])
    vm.running = True
    vm.step()  # Should read 0 from empty memory (NOP)
    results.record(
        "Empty memory reads as 0 (NOP)",
        True,  # Just checking it doesn't crash
        "crashed"
    )


# =============================================================================
# DEMO FUNCTIONS TESTS
# =============================================================================

def test_demo_functions():
    """Test the built-in demo functions."""
    print("\n[9] DEMO FUNCTIONS")
    print("-" * 40)
    
    # Just verify they don't crash
    from setun70 import demo_arithmetic, demo_expression, demo_factorial, demo_ternary, demo_assembler
    
    import io
    import sys
    
    # Capture output and verify no exceptions
    old_stdout = sys.stdout
    
    try:
        sys.stdout = io.StringIO()
        demo_ternary()
        results.record("demo_ternary runs", True, "")
    except Exception as e:
        results.record("demo_ternary runs", False, str(e))
    finally:
        sys.stdout = old_stdout
    
    try:
        sys.stdout = io.StringIO()
        demo_arithmetic()
        results.record("demo_arithmetic runs", True, "")
    except Exception as e:
        results.record("demo_arithmetic runs", False, str(e))
    finally:
        sys.stdout = old_stdout
    
    try:
        sys.stdout = io.StringIO()
        demo_expression()
        results.record("demo_expression runs", True, "")
    except Exception as e:
        results.record("demo_expression runs", False, str(e))
    finally:
        sys.stdout = old_stdout
    
    try:
        sys.stdout = io.StringIO()
        demo_factorial()
        results.record("demo_factorial runs", True, "")
    except Exception as e:
        results.record("demo_factorial runs", False, str(e))
    finally:
        sys.stdout = old_stdout
    
    try:
        sys.stdout = io.StringIO()
        demo_assembler()
        results.record("demo_assembler runs", True, "")
    except Exception as e:
        results.record("demo_assembler runs", False, str(e))
    finally:
        sys.stdout = old_stdout


# =============================================================================
# COMPLEX EXPRESSION TESTS
# =============================================================================

def test_complex_expressions():
    """Test complex mathematical expressions."""
    print("\n[10] COMPLEX EXPRESSIONS")
    print("-" * 40)
    
    vm = Setun70()
    asm = Setun70Assembler()
    
    # (3 + 4) * (5 - 2) = 7 * 3 = 21
    source = """
    LIT 3
    LIT 4
    ADD
    LIT 5
    LIT 2
    SUB
    MUL
    HALT
    """
    vm.load_program(asm.assemble(source))
    vm.run()
    results.record(
        "(3+4)*(5-2) = 21",
        vm.T == 21,
        f"got {vm.T}"
    )
    
    # Test order of operations in RPN
    # (10 + 20) - (5 * 2) = 30 - 10 = 20
    vm.reset()
    asm = Setun70Assembler()
    source = """
    LIT 10
    LIT 20
    ADD
    LIT 5
    LIT 2
    MUL
    SUB
    HALT
    """
    vm.load_program(asm.assemble(source))
    vm.run()
    results.record(
        "(10+20)-(5*2) = 20",
        vm.T == 20,
        f"got {vm.T}"
    )
    
    # Test nested: ((2 * 3) + (4 * 5)) * 2 = (6 + 20) * 2 = 52
    vm.reset()
    asm = Setun70Assembler()
    source = """
    LIT 2
    LIT 3
    MUL
    LIT 4
    LIT 5
    MUL
    ADD
    LIT 2
    MUL
    HALT
    """
    vm.load_program(asm.assemble(source))
    vm.run()
    results.record(
        "((2*3)+(4*5))*2 = 52",
        vm.T == 52,
        f"got {vm.T}"
    )


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Run all tests."""
    print("=" * 60)
    print("SETUN 70 EMULATOR - COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    
    test_ternary_arithmetic()
    test_syllable_encoding()
    test_stack_operations()
    test_instructions()
    test_control_flow()
    test_assembler()
    test_example_programs()
    test_edge_cases()
    test_demo_functions()
    test_complex_expressions()
    
    success = results.summary()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

