from .base import BaseLexer, BaseParser


class ParserLexer(BaseLexer):
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

    tokens = BaseLexer.simple_tokens + list(reserved.values())

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = ParserLexer.reserved.get(t.value, 'ID')  # Check for reserved words
        return t


class ParserParser(BaseParser):
    tokens = ParserLexer.tokens
    start = 'parser'

    def p_parser(self, p):
        'parser : PARSE parse_code'

    def p_parse_code(self, p):
        '''parse_code : empty
                      | instructions parse_code'''

    def p_instructions(self, p):
        '''instructions : store
                        | mov
                        | cmpje
                        | cmpjn
                        | j
                        | label'''

    def p_store(self, p):
        'store : STORE phv COMMA header COMMA INT'

    def p_mov(self, p):
        'mov : MOV regmem COMMA allval COMMA INT'

    def p_cmpje(self, p):
        'cmpje : CMPJE reg COMMA number COMMA label_id'

    def p_cmpjn(self, p):
        'cmpjn : CMPJN reg COMMA number COMMA label_id'

    def p_j(self, p):
        'j : J label'

    def p_label(self, p):
        'label : label_id COLON'

    def p_label_id(self, p):
        '''label_id : ID
                    | HALT'''

    def p_reg(self, p):
        '''reg : R1
               | R2'''

    def p_phv(self, p):
        'phv : PHV shift'

    def p_header(self, p):
        'header : HEADER shift'

    def p_regmem(self, p):
        '''regmem : reg
                  | phv'''

    def p_allval(self, p):
        '''allval : reg
                  | number
                  | phv'''

    def p_shift(self, p):
        '''shift : empty
                 | PLUS INT'''

    def p_number(self, p):
        '''number : INT
                  | HEX'''
        p[0] = p[1]
