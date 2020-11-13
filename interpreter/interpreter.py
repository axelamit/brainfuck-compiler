import sys

class Parser(): 
    def __init__(self, filename):
        self.filename = filename
    
    def run(self):
        tokens = self.tokenize()
        jumps = self.find_jumps(tokens)
        self.eval(tokens, jumps)

    def tokenize(self):
        tokens = []
        with open(self.filename, "r") as f: 
            for line in f: 
                for ch in line:
                    if (ch != '' and ch != ' ' and ch != '\n'):
                        tokens.append(ch)
        return tokens
    
    def find_jumps(self, tokens):
        stack = []
        mp = {}
        for i in range(len(tokens)):
            if (tokens[i] == '['):
                stack.append(i)
            elif (tokens[i] == ']'):
                start = stack.pop()
                mp[start] = i
                mp[i] = start
        return mp

    def eval(self, tokens, jumps):
        stack = [0]
        i = 0
        pointer = 0
        while i < len(tokens):
            command = tokens[i]
            if (command == '>'):
                pointer += 1
                if (pointer == len(stack)):
                    stack.append(0)
            elif (command == '<'):
                pointer -= 1
                if (pointer < 0):
                    pointer = 0
            elif (command == '+'):
                stack[pointer] += 1
            elif (command == '-'):
                stack[pointer] -= 1
            elif (command == '.'):
                out = chr(stack[pointer])
                print (out, end='')
            elif (command == ','):
                try:
                    inp = int(input())+48
                except:
                    inp = ord(input())
                stack[pointer] = inp
            elif (command == '['):
                if (stack[pointer] == 0):
                    i = jumps[i]
            elif (command == ']'):
                if (stack[pointer] != 0):
                    i = jumps[i]

            i += 1
def main():
    program = Parser("../brainfuck/mandelbrot.bf")
    program.run()

if __name__ == "__main__":
    main()