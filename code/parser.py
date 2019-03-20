from .base import BaseLexer, BaseParser
from .ast import *


class ParserLexer(BaseLexer):
    simple_tokens = [
        'ID', 'COLON'
    ]
    # Reserved tokens
    reserved = {
        'parser': 'PARSE',
        'PHV': 'PHV',
        'HEADER': 'HEADER',
        'store': 'STORE',
        'mov': 'MOV',
        'cmpje': 'CMPJE',
        'cmpjn': 'CMPJN',
        'j': 'J',
        'r1': 'R1',
        'r2': 'R2',
        'halt': 'HALT'
    }

    t_COLON = r'\:'

    tokens = simple_tokens + BaseLexer.simple_tokens + list(reserved.values())

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = ParserLexer.reserved.get(t.value, 'ID')  # Check for reserved words
        return t


class ParserParser(BaseParser):
    tokens = ParserLexer.tokens
    start = 'parser'

    def parse(self, text):
        lexer = ParserLexer()
        lexer.build()
        self.build()
        return self.parser.parse(text, lexer=lexer.lexer)

    def p_parser(self, p):
        'parser : PARSE parse_code'
        p[0] = Node([p[2]], Section('parse'))

    def p_parse_code(self, p):
        '''parse_code : empty
                      | instruction parse_code'''
        if len(p) == 3:
            p[0] = Node([p[2]], p[1])
        else:
            p[0] = Node()

    def p_instructions(self, p):
        '''instruction : store
                       | mov
                       | cmpje
                       | cmpjn
                       | j
                       | label'''
        p[0] = p[1]

    def p_store(self, p):
        'store : STORE phv COMMA header COMMA INT'
        p[0] = Node([], TernaryOp('store', p[2], p[4], p[6]))

    def p_mov(self, p):
        'mov : MOV regmem COMMA allval COMMA INT'
        p[0] = Node([], TernaryOp('store', p[2], p[4], p[6]))

    def p_cmpje(self, p):
        'cmpje : CMPJE reg COMMA number COMMA label_id'
        p[0] = Node([], Jump(p[2], p[4], p[6]))

    def p_cmpjn(self, p):
        'cmpjn : CMPJN reg COMMA number COMMA label_id'
        p[0] = Node([], Jump(p[2], p[4], p[6]))

    def p_j(self, p):
        'j : J label_id'
        p[0] = Node([], Jump(0, 0, p[2]))

    def p_label(self, p):
        'label : label_id COLON'
        p[0] = Node([], Label(p[1]))

    def p_label_id(self, p):
        '''label_id : ID
                    | HALT'''
        p[0] = p[1]

    def p_reg(self, p):
        '''reg : R1
               | R2'''
        p[0] = Reg(p[1])

    def p_phv(self, p):
        'phv : PHV shift'
        p[0] = Phv(p[2])

    def p_header(self, p):
        'header : HEADER shift'
        p[0] = Hdr(p[2])

    def p_regmem(self, p):
        '''regmem : reg
                  | phv'''
        p[0] = p[1]

    def p_allval(self, p):
        '''allval : reg
                  | number
                  | phv'''
        p[0] = p[1]

    def p_shift(self, p):
        '''shift : empty
                 | PLUS INT'''
        if len(p) == 3:
            p[0] = p[2]
        else:
            p[0] = 0

    def p_number(self, p):
        '''number : INT
                  | HEX'''
        p[0] = p[1]
