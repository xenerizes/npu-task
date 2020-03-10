from .base import BaseLexer, BaseParser
from .ast import *


class MatchActionLexer(BaseLexer):
    simple_tokens = [
        'ID', 'COLON'
    ]
    # Reserved tokens
    reserved = {
        'match_action': 'MA',
        'PHV': 'PHV',
        'PORTMASK': 'PORTMASK',
        'mov': 'MOV',
        'call': 'CALL',
        'cmpje': 'CMPJE',
        'cmpjn': 'CMPJN',
        'or': 'OR',
        'and': 'AND',
        'xor': 'XOR',
        'mod': 'MOD',
        'shl': 'SHL',
        'shr': 'SHR',
        'j': 'J',
        'r1': 'R1',
        'r2': 'R2',
        'r3': 'R3',
        'halt': 'HALT'
    }

    tokens = simple_tokens + BaseLexer.simple_tokens + list(reserved.values())

    t_COLON = r'\:'

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = MatchActionLexer.reserved.get(t.value, 'ID')  # Check for reserved words
        return t


class MatchActionParser(BaseParser):
    tokens = MatchActionLexer.tokens
    start = 'ma'

    def parse(self, text):
        lexer = MatchActionLexer()
        lexer.build()
        self.build()
        return self.parser.parse(text, lexer=lexer.lexer)

    def p_ma(self, p):
        'ma : MA INT code'
        p[0] = Node(p[3], Section(p[2]))

    def p_code(self, p):
        '''code : empty
              | instruction code
              | label code'''
        if len(p) == 3:
            p[0] = Node(p[2], p[1])
        else:
            p[0] = None

    def p_instruction(self, p):
        '''instruction : mov
                       | cmpje
                       | cmpjn
                       | j
                       | or
                       | and
                       | xor
                       | mod
                       | shl
                       | shr
                       | call'''
        p[0] = p[1]

    def p_mov(self, p):
        'mov : MOV regmem COMMA allval COMMA INT'
        p[0] = TernaryOp('mov', p[2], p[4], p[6])

    def p_cmpje(self, p):
        'cmpje : CMPJE reg COMMA number COMMA label_j_id'
        p[0] = Jump('cmpje', p[2], p[4], p[6])

    def p_cmpjn(self, p):
        'cmpjn : CMPJN reg COMMA number COMMA label_j_id'
        p[0] = Jump('cmpjn', p[2], p[4], p[6])

    def p_j(self, p):
        'j : J label_j_id'
        p[0] = Jump('j', 0, 0, p[2])

    def p_or(self, p):
        'or : OR regpm COMMA regnum'
        p[0] = BinOp('or_op', p[2], p[4])

    def p_and(self, p):
        'and : AND regpm COMMA regnum'
        p[0] = BinOp('and_op', p[2], p[4])

    def p_xor(self, p):
        'xor : XOR regpm COMMA regnum'
        p[0] = BinOp('xor_op', p[2], p[4])

    def p_mod(self, p):
        'mod : MOD reg COMMA regnum'
        p[0] = BinOp('mod_op', p[2], p[4])

    def p_shl(self, p):
        'shl : SHL reg COMMA number'
        p[0] = BinOp('shl', p[2], p[4])

    def p_shr(self, p):
        'shr : SHR reg COMMA number'
        p[0] = BinOp('shr', p[2], p[4])

    def p_call(self, p):
        'call : CALL ID'
        p[0] = Call(p[2])

    def p_label(self, p):
        'label : label_id COLON'
        p[0] = Label(p[1])

    def p_label_id(self, p):
        '''label_id : ID'''
        p[0] = p[1]

    def p_label_j_id(self, p):
        '''label_j_id : ID
                      | HALT'''
        p[0] = p[1]

    def p_reg(self, p):
        '''reg : R1
               | R2
               | R3'''
        p[0] = Reg(p[1])

    def p_phv(self, p):
        'phv : PHV shift'
        p[0] = Phv(p[2])

    def p_portmask(self, p):
        'portmask : PORTMASK'
        p[0] = Portmask()

    def p_mem(self,p ):
        '''mem : phv
               | portmask'''
        p[0] = p[1]

    def p_regmem(self, p):
        '''regmem : reg
                  | mem'''
        p[0] = p[1]

    def p_regpm(self, p):
        '''regpm : reg
                  | portmask'''
        p[0] = p[1]

    def p_regnum(self, p):
        '''regnum : reg
                  | number'''
        p[0] = p[1]

    def p_allval(self, p):
        '''allval : reg
                  | number
                  | mem'''
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

