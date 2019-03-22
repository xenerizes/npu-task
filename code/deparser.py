from .base import BaseLexer, BaseParser
from .ast import *


class DeparserLexer(BaseLexer):
    # Reserved tokens
    reserved = {
        'deparser': 'DPRS',
        'PHV': 'PHV',
        'HEADER': 'HEADER',
        'load': 'LOAD'
    }

    tokens = BaseLexer.simple_tokens + list(reserved.values())

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = DeparserLexer.reserved.get(t.value, 'ID')  # Check for reserved words
        return t


class DeparserParser(BaseParser):
    tokens = DeparserLexer.tokens
    start = 'deparser'

    def parse(self, text):
        lexer = DeparserLexer()
        lexer.build()
        self.build()
        return self.parser.parse(text, lexer=lexer.lexer)

    def p_deparser(self, p):
        'deparser : DPRS code'
        p[0] = p[2]

    def p_code(self, p):
        '''code : empty
                | load code'''
        if len(p) == 3:
            p[0] = Node(p[2], p[1])
        else:
            p[0] = None

    def p_load(self, p):
        'load : LOAD header COMMA phv COMMA INT'
        p[0] = TernaryOp('load', p[2], p[4], p[6])

    def p_phv(self, p):
        'phv : PHV shift'
        p[0] = Phv(p[2])

    def p_header(self, p):
        'header : HEADER shift'
        p[0] = Hdr(p[2])

    def p_shift(self, p):
        '''shift : empty
                 | PLUS number'''
        if len(p) == 3:
            p[0] = p[2]
        else:
            p[0] = 0

    def p_number(self, p):
        '''number : INT
                  | HEX'''
        p[0] = p[1]
