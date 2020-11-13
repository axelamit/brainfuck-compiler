# axenil-compiler
LLVM compiler for [Brainfuck](https://esolangs.org/wiki/Brainfuck_implementations) written in Python 3. The compiler uses ```rply``` for lexing and parsing and ```llvmlite``` for generating the code. 

## Benchmarks

Benchmarks are timed with ```time python3 interpreter.py``` for the interpreter and ```time lli program.ll``` for the compiler. The time displayed in the table is the sum om ```user``` and ```sys``` time. 

### Mandelbrot

| Interpreter | Compiler |
| --- | --- |
| 35min 41.077s | 1.865s |