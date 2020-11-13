from rply import ParserGenerator
import ast

class Parser():
    def __init__(self):
        self.pg = ParserGenerator(
            ['SHIFT_RIGHT', 'SHIFT_LEFT', 'INCREMENT', 'DECREMENT', 'OUTPUT', 'INPUT', 'OPEN_LOOP', 'CLOSE_LOOP']
        )
        self.rules()
        self.parser = self.pg.build()

    def parse(self, tokens):
        return self.parser.parse(tokens)
    
    def rules(self):
        @self.pg.production('program : instruction')
        @self.pg.production('program : instruction program')
        def program(p):
            instructions = [p[0]]
            if len(p) == 2:
                instructions += p[1].instructions
            return ast.Program(instructions)

        @self.pg.production('instruction : SHIFT_RIGHT')
        @self.pg.production('instruction : SHIFT_LEFT')
        @self.pg.production('instruction : INCREMENT')
        @self.pg.production('instruction : DECREMENT')
        @self.pg.production('instruction : OUTPUT')
        @self.pg.production('instruction : INPUT')
        @self.pg.production('instruction : OPEN_LOOP')
        @self.pg.production('instruction : CLOSE_LOOP')
        def instruction(p):
            if (p[0].gettokentype() == 'SHIFT_RIGHT'):
                return ast.Shift_Right()
            elif (p[0].gettokentype() == 'SHIFT_LEFT'):
                return ast.Shift_Left()
            elif (p[0].gettokentype() == 'INCREMENT'):
                return ast.Increment()
            elif (p[0].gettokentype() == 'DECREMENT'):
                return ast.Decrement()
            elif (p[0].gettokentype() == 'OUTPUT'):
                return ast.Output()
            elif (p[0].gettokentype() == 'INPUT'):
                return ast.Input()
            elif (p[0].gettokentype() == 'OPEN_LOOP'):
                return ast.Open_Loop()
            elif (p[0].gettokentype() == 'CLOSE_LOOP'):
                return ast.Close_Loop()