from .base import BaseLexer, BaseParser


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

    def p_deparser(self, p):
        'deparser : DPRS code'

    def p_code(self, p):
        '''code : empty
                | load code'''

    def p_load(self, p):
        'load : LOAD header COMMA phv COMMA INT'

    def p_phv(self, p):
        'phv : PHV shift'

    def p_header(self, p):
        'header : HEADER shift'

    def p_shift(self, p):
        '''shift : empty
                 | PLUS number'''

    def p_number(self, p):
        '''number : INT
                  | HEX'''
        p[0] = p[1]
