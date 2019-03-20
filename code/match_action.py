from .base import BaseLexer, BaseParser


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
        'shl': 'SHL',
        'shr': 'SHR',
        'j': 'J',
        'r1': 'R1',
        'r2': 'R2',
        'r3': 'R3',
        'halt': 'HALT'
    }

    tokens = simple_tokens + BaseLexer.simple_tokens + list(reserved.values())

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = MatchActionLexer.reserved.get(t.value, 'ID')  # Check for reserved words
        return t


class MatchActionParser(BaseParser):
    tokens = MatchActionLexer.tokens
    start = 'ma_sequence'

    def p_ma_sequence(self, p):
        '''ma_sequence : empty
                       | ma ma_sequence'''

    def p_ma(self, p):
        'ma : MA INT code'

    def p_code(self, p):
        '''code : empty
              | instruction code'''

    def p_instruction(self, p):
        '''instruction : mov
                       | cmpje
                       | cmpjn
                       | j
                       | or
                       | and
                       | xor
                       | shl
                       | shr
                       | call
                       | label'''

    def p_mov(self, p):
        'mov : MOV regmem COMMA allval COMMA INT'

    def p_cmpje(self, p):
        'cmpje : CMPJE reg COMMA number COMMA label_id'

    def p_cmpjn(self, p):
        'cmpjn : CMPJN reg COMMA number COMMA label_id'

    def p_j(self, p):
        'j : J label_id'

    def p_or(self, p):
        'or : OR regmem COMMA regnum'

    def p_and(self, p):
        'and : AND regmem COMMA regnum'

    def p_xor(self, p):
        'xor : XOR regmem COMMA regnum'

    def p_shl(self, p):
        'shl : SHL reg COMMA number'

    def p_shr(self, p):
        'shr : SHR reg COMMA number'

    def p_call(self, p):
        'call : CALL ID'

    def p_label(self, p):
        'label : label_id COLON'

    def p_label_id(self, p):
        '''label_id : ID
                    | HALT'''

    def p_reg(self, p):
        '''reg : R1
               | R2
               | R3'''

    def p_phv(self, p):
        'phv : PHV shift'

    def p_portmask(self, p):
        'portmask : PORTMASK shift'

    def p_mem(self,p ):
        '''mem : phv
               | portmask'''

    def p_regmem(self, p):
        '''regmem : reg
                  | mem'''

    def p_regnum(self, p):
        '''regnum : reg
                  | number'''

    def p_allval(self, p):
        '''allval : reg
                  | number
                  | mem'''

    def p_shift(self, p):
        '''shift : empty
                 | PLUS INT'''

    def p_number(self, p):
        '''number : INT
                  | HEX'''
        p[0] = p[1]

