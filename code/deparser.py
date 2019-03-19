from .base import BaseLexer


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
