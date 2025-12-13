# Setun 70 Emulator

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A working emulator of the Soviet Setun 70 ternary computer (1970), reconstructed from archival documentation.**

![Setun 70](https://img.shields.io/badge/Architecture-Balanced_Ternary-green)
![Stack Machine](https://img.shields.io/badge/Execution-POLIZ_Stack-orange)

## What Is This?

The Setun 70 was a **balanced ternary computer** developed at Moscow State University in 1970. It used:

- **Balanced ternary numbers**: digits are -1, 0, +1 (not 0, 1 like binary)
- **POLIZ execution**: Reverse Polish Notation with a two-stack architecture
- **Syllable-based programs**: 6-trit "trytes" instead of bytes

This emulator reconstructs the architecture from the original 1970 paper by Brusentsov, Zhogolev, and Maslov, recovered from the Russian Virtual Computer Museum and Bitsavers archives.

## 🌐 Try It Online

**[Launch Web Emulator →](https://zaneham.github.io/setun70-emulator/web/)**

No installation required. Write POLIZ assembly and watch the ternary stack machine execute.

## Installation

### From PyPI

```bash
pip install setun70
```

### From Source

```bash
git clone https://github.com/Zaneham/setun70-emulator.git
cd setun70-emulator
pip install -e .
```

## Quick Start

### Run the demos

```bash
python setun70.py
```

### Run a program file

```bash
python setun70.py examples/hello.s70
python setun70.py examples/factorial.s70 --debug
```

### Use as a library

```python
from setun70 import Setun70, Setun70Assembler

source = """
    LIT 10      ; Push 10
    LIT 20      ; Push 20
    ADD         ; Add them
    OUT         ; Output result
    HALT        ; Stop
"""

asm = Setun70Assembler()
program = asm.assemble(source)

vm = Setun70()
vm.load_program(program)
vm.run()
# Output: OUT: 30 (ternary: 001010)
```

## Demo Output

```
+==================================================================+
|                     SETUN 70 EMULATOR                            |
|         Soviet Ternary Computer (1970) - Reconstructed           |
+==================================================================+

DEMO: Balanced Ternary Arithmetic
 -13 -> 000TTT -> -13
  -5 -> 000T11 -> -5
   0 -> 000000 -> 0
  13 -> 000111 -> 13
 224 -> 10T10T -> 224

DEMO: Arithmetic (3 + 4) x 5 = 35
OUT: 35 (ternary: 00110T)

DEMO: Factorial 5! = 120
OUT: 120 (ternary: 011110)
```

## Why Balanced Ternary?

| Feature | Binary | Balanced Ternary |
|---------|--------|------------------|
| Digits | 0, 1 | -1, 0, +1 |
| Negation | Complex (two's complement) | Just flip all digits! |
| Rounding | Biased | Perfect (truncation = rounding) |
| Signed/unsigned | Two representations | One representation |
| Efficiency | Baseline | 5.4% better |

```
Decimal 13:
  Binary:           001101 (6 bits)
  Balanced Ternary: 000111 (6 trits, ~9.5 bits equivalent)
  Negated:          000TTT = -13 (just flip!)
```

## Assembly Language

### Instructions

| Mnemonic | Stack Effect | Description |
|----------|--------------|-------------|
| `LIT n` | -- n | Push literal value |
| `ADD` | a b -- a+b | Add |
| `SUB` | a b -- a-b | Subtract |
| `MUL` | a b -- a*b | Multiply |
| `DIV` | a b -- a/b | Divide |
| `DUP` | a -- a a | Duplicate |
| `DROP` | a -- | Remove top |
| `SWAP` | a b -- b a | Exchange |
| `NEG` | a -- -a | Negate |
| `OUT` | a -- | Print value |
| `HALT` | -- | Stop execution |

### Example Program

```asm
; quadratic.s70 - Calculate x^2 + 2x + 1 where x = 5

    LIT 5       ; x = 5
    DUP         ; x x
    MUL         ; x^2 = 25
    
    LIT 5       ; x
    LIT 2       ; 2
    MUL         ; 2x = 10
    
    ADD         ; 25 + 10 = 35
    LIT 1       ; 1
    ADD         ; 35 + 1 = 36
    
    OUT         ; Output: 36
    HALT
```

## Architecture

### Memory Model

- **27 pages** (3^3) of **81 syllables** (3^4) each
- **3 page registers** for bank switching
- Total: 2,187 syllables (~20KB equivalent)

### Syllable Format (6 trits)

```
Operation: [0 0 | type | opcode (3 trits)]
Address:   [length | page_reg | offset (4 trits)]
```

## Historical Context

The Setun 70 was developed at Moscow State University's Computing Center. Key facts:

- **1958**: Original Setun built - world's only production ternary computer
- **1965**: Production cancelled despite demand ("an ugly duckling")
- **1970**: Setun 70 designed - research into optimal architectures
- **1970**: Charles Moore independently creates Forth (similar stack model)
- **1995**: Sun creates JVM (similar stack bytecode)
- **2025**: This emulator reconstructed from archived papers

The DSSP (Dialogue System of Structured Programming) continues to emulate Setun 70 on binary computers **to this day** because the architecture's programming advantages remain compelling.

## Project Structure

```
setun70-emulator/
├── setun70.py          # Python emulator (~600 lines)
├── setun70_spec.md     # Formal specification
├── README.md           # This file
├── LICENSE             # MIT License
├── pyproject.toml      # Python package config
├── web/
│   └── index.html      # Browser-based emulator (self-contained)
└── examples/
    ├── hello.s70       # Simple arithmetic
    ├── factorial.s70   # 5! = 120
    └── quadratic.s70   # Polynomial evaluation
```

## Contributing

Contributions welcome! Ideas:

- [ ] Add more instructions (comparisons, jumps)
- [ ] Implement the return stack for procedures
- [ ] Port programs from the 1968 Soviet program catalog
- [x] ~~Create a web-based emulator~~ ✓ Done!

## Deploying to GitHub Pages

To enable the web emulator at `https://YOUR_USERNAME.github.io/setun70-emulator/web/`:

1. Go to your repo → **Settings** → **Pages**
2. Under "Source", select **Deploy from a branch**
3. Select **main** branch and **/ (root)** folder
4. Click **Save**

The web emulator will be live within a few minutes.

## References

1. Brusentsov, N.P., Zhogolev, E.A., Maslov, S.P. "General Characteristics of the Small Digital Machine 'Setun 70'" (1970)
2. Russian Virtual Computer Museum: http://computer-museum.ru/english/setun.htm
3. Bitsavers Soviet computing archive: http://bitsavers.org/pdf/ussr/

## License

MIT License - see [LICENSE](LICENSE)

---

*Part of The Ian Index - Reconstructing Lost Computing Architectures*

**Go find it for goodness sake.**
