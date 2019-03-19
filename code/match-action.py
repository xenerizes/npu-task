from .base import BaseLexer


class MatchActionLexer(BaseLexer):
    # Reserved tokens
    reserved = {
        'match-action': 'MA',
        'PHV': 'PHV',
        'PORTMASK': 'PORTMASK',
        'mov': 'MOV',
        'call': 'CALL',
        'cmpje': 'CMPJE',
        'cmpjn': 'CMPJN',
        'or': 'OR',
        'and': 'AND',
        'xor': 'XOR',
        'j': 'J',
        'r1': 'R1',
        'r2': 'R2',
        'r3': 'R3',
        'halt': 'HALT'
    }

    tokens = BaseLexer.simple_tokens + list(reserved.values())

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = MatchActionLexer.reserved.get(t.value, 'ID')  # Check for reserved words
        return t
