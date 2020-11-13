from llvmlite import ir

CELLS = 30000

int8 = ir.IntType(8)
int32 = ir.IntType(32)
int64 = ir.IntType(64)

arr8 = ir.ArrayType(int8, CELLS)
arr64 = ir.ArrayType(int64, CELLS)

class Program:

    def __init__(self, instructions):
        self.instructions = instructions

    def construct(self, triple):
        self.module = ir.Module()
        self.module.triple = triple

        self.add_functions()
        self.memory_setup()

        self.builder = ir.IRBuilder(self.main.append_basic_block(name = 'entry'))
        self.ptr = self.builder.gep(self.memory, [int8(0), int8(0)], "ptr")

        self.stack = []

        self.construct_instructions()

        self.builder.ret(ir.IntType(64)(0))

        return self.module

    def construct_instructions(self):
        for i in range(len(self.instructions)):
            instruction = self.instructions[i]
            if (isinstance(instruction, Open_Loop) or isinstance(instruction, Close_Loop)):
                instruction.construct(self, i)
            else:    
                instruction.construct(self)

    def add_functions(self):
        func_type = ir.FunctionType(int64, [])
        self.main = ir.Function(self.module, func_type, name='main')

        putchar_type = ir.FunctionType(int64, [int64])
        self.putchar = ir.Function(self.module, putchar_type, 'putchar')

        getchar_type = ir.FunctionType(int64, [])
        self.getchar = ir.Function(self.module, getchar_type, 'getchar')

    def memory_setup(self):
        self.memory = ir.GlobalVariable(self.module, arr8, 'memory')
        self.memory.initializer = arr8([0] * CELLS)

    def move_memptr(self, steps):
        self.ptr = self.builder.gep(self.ptr, [int8(steps)])
    
class Shift_Right:
    def construct(self, program):
        program.move_memptr(1)
    
class Shift_Left:
    def construct(self, program):
        program.move_memptr(-1)
    
class Increment:     
    def construct(self, program):
        val = program.builder.load(program.ptr)
        val = program.builder.add(val, int8(1))
        program.builder.store(val, program.ptr)

class Decrement: 
    def construct(self, program):
        val = program.builder.load(program.ptr)
        val = program.builder.sub(val, int8(1))
        program.builder.store(val, program.ptr)

class Output:
    def construct(self, program):
        val = program.builder.load(program.ptr)
        val = program.builder.zext(val, int64)
        program.builder.call(program.putchar, [val])

class Input:
    def construct(self, program):
        val = program.builder.call(program.getchar, [])
        val = program.builder.trunc(val, int8)
        program.builder.store(val, program.ptr)

class Open_Loop:
    def construct(self, program, loc):
        loop = Loop()
        loop.entry = program.builder.block
        loop.body = program.builder.append_basic_block("body")
        loop.exit = program.builder.append_basic_block("exit")

        val = program.builder.load(program.ptr)
        condition = program.builder.icmp_unsigned("!=",val,int64(0))
        program.builder.cbranch(condition, loop.body, loop.exit)

        with program.builder.goto_block(loop.exit):
            loop.ptr_exit = program.builder.phi(int8.as_pointer(), "ptr")
            loop.ptr_exit.add_incoming(program.ptr, loop.entry)

        with program.builder.goto_block(loop.body):
            loop.ptr_body = program.builder.phi(int8.as_pointer(), "ptr")
            loop.ptr_body.add_incoming(program.ptr, loop.entry)

        program.builder.position_at_end(loop.body)
        program.ptr = loop.ptr_body
        program.stack.append(loop)

class Close_Loop:
    def construct(self, program, loc):
        if (len(program.stack) == 0):
            exit(1)

        loop = program.stack.pop()

        loop.ptr_body.add_incoming(program.ptr, program.builder.block)
        loop.ptr_exit.add_incoming(program.ptr, program.builder.block)

        value = program.builder.load(program.ptr)
        condition = program.builder.icmp_unsigned("!=",value, int64(0))
        program.builder.cbranch(condition, loop.body, loop.exit)

        program.ptr = loop.ptr_exit
        program.builder.position_at_end(loop.exit)

class Loop:
    pass