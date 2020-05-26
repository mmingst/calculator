# Simple Calculator (+,-,*,/) interpreter built in python to handle basic queries
# Written by Max Mingst
#
#
# Credit to Ruslan Spivak and his incredibly comprehensive guide found at:
# ruslanspivak.com

INTEGER, PLUS, MINUS, MUL, DIV, LPAR, RPAR, END = 'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV','(', ')', 'END'


class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, MINUS, MUL, DIV, (, ),  END
        self.type = type
        self.value = value

    def __str__(self):
        """String representation of the class instance."""
        return 'Token({type}, {value})'.format(type=self.type, value=repr(self.value))

    def __repr__(self):
        return self.__str__()


class Lexer(object):
    def __init__(self, text):
        # client string input, e.g. "3 * 5", "12 / 3 * 4", etc
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.c_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid parse')

    def advance(self):
        """Advance `pos` by one and set the `c_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.c_char = None 
        else:
            self.c_char = self.text[self.pos]

    def ignoreSpace(self):
        while self.c_char is not None and self.c_char.isspace():
            self.advance()

    def integer(self):
        """Return positive integer read from input."""
        res = ''
        while self.c_char is not None and self.c_char.isdigit():
            res += self.c_char
            self.advance()
        return int(res)

    def get_next_token(self):
        """Breaks apart text into tokens that can be parsed.
        """
        while self.c_char is not None:

            if self.c_char.isspace():
                self.ignoreSpace()
                continue

            if self.c_char.isdigit():
                return Token(INTEGER, self.integer())
            
            if self.c_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.c_char == '-':
                self.advance()
                return Token(MINUS, '-')
           
            if self.c_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.c_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self.c_char == '(':
                self.advance()
                return Token(LPAR, '(')

            if self.c_char == ')':
                self.advance()
                return Token(RPAR, ')')

            self.error()

        return Token(END, None)


class Interpreter(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.c_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.c_token,
        # otherwise raise an exception.
        if self.c_token.type == token_type:
            self.c_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """Return an INTEGER token value.
        factor : INTEGER
        """
        token = self.c_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return token.value
        elif token.type == LPAR:
            self.eat(LPAR)
            res = self.expr()
            self.eat(RPAR)
            return res
        
    def term(self):
        """Arithmetic expression parser / interpreter.
            expr   : factor ((MUL | DIV) factor)*
        factor : INTEGER
        """
        result = self.factor()

        while self.c_token.type in (MUL, DIV):
            token = self.c_token
            if token.type == MUL:
                self.eat(MUL)
                result = result * self.factor()
            elif token.type == DIV:
                self.eat(DIV)
                result = result / self.factor()
        
        return result
    
    def expr(self):
        """Calculator expression parser."""
        # set current token to the first token taken from the input

        result = self.term()
        while self.c_token.type in (PLUS, MINUS):
            token = self.c_token
            if token.type == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result = result - self.term()

        return result
       
#================================================================
#================================================================

def main():
    while True:
        try:
            text = input('calc> ')
        except ENDError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()