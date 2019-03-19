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
    t_HEX = r'0[xX][0-9a-fA-F]+'

    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'

    def t_NUMBER(self, t):
        r'[+-]?\b[0-9]+\b'
        t.value = int(t.value)
        return t

    # Error handling rule
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
