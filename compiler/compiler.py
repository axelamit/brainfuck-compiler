from llvmlite import binding

from lexer import Lexer
from parser import Parser

class Compiler:

    def __init__(self):
        self.lexer = Lexer()
        self.parser = Parser()
    
    def compile(self, code):
        tokens = self.lexer.tokenize(code)
        program = self.parser.parse(tokens)

        binding.initialize()
        binding.initialize_native_target()
        binding.initialize_native_asmprinter()
        triple = binding.Target.from_default_triple().triple

        return program.construct(triple)

if __name__ == "__main__":
    code = ""
    with open("../brainfuck/mandelbrot.bf", "r") as f:
        for line in f.readlines():
            code += str(line)
    compiler = Compiler()
    ll = compiler.compile(code)
    with open("mandelbrot.ll", "w") as f:
        f.write(str(ll))