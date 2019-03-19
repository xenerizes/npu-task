from .base import BaseLexer


class ParserLexer(BaseLexer):
    # Reserved tokens
    reserved = {
        'parser': 'PRS',
        'PHV': 'PHV',
        'HEADER': 'HEADER',
        'PORTMASK': 'PORTMASK',
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
