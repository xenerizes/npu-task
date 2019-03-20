import ply.lex as lex
import ply.yacc as yacc


class BaseLexer(object):
    simple_tokens = [
        'COLON', 'PLUS', 'COMMA',
        'INT', 'HEX',
        'ID'
    ]

    # Regex for simple tokens
    t_PLUS = r'\+'
    t_COMMA = r'\,'
    t_COLON = r'\:'

    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'

    def t_HEX(self, t):
        r'0[xX][0-9a-fA-F]+'
        t.value = int(t.value, 0)
        return t

    def t_INT(self, t):
        r'\b[0-9]+\b'
        t.value = int(t.value)
        return t

    # Error handling rule
    def t_error(self, t):
        raise SyntaxError("Illegal character {}".format(t.value[0]))

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def analyze(self, text):
        self.lexer.input(text)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)


class BaseParser(object):
    def p_empty(self, p):
        'empty :'
        pass

    def p_error(self, p):
        raise SyntaxError("Syntax error in input: {}".format(p))

    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)

    def parse(self, text, lexer):
        result = self.parser.parse(text, lexer=lexer)
        print(result)
