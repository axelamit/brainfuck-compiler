from rply import LexerGenerator

class Lexer:
    def __init__(self):
        self.lexer = LexerGenerator()
        self.add_tokens()
        self.lex = self.lexer.build()
    
    def add_tokens(self):
        self.lexer.add('SHIFT_RIGHT', r'\>')
        self.lexer.add('SHIFT_LEFT', r'\<')
        self.lexer.add('INCREMENT', r'\+')
        self.lexer.add('DECREMENT', r'\-')
        self.lexer.add('OUTPUT', r'\.')
        self.lexer.add('INPUT', r'\,')
        self.lexer.add('OPEN_LOOP', r'\[')
        self.lexer.add('CLOSE_LOOP', r'\]')
        self.lexer.ignore(r'\s+')

    def tokenize(self, text):
        return self.lex.lex(text)