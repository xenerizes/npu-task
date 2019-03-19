from .parser import ParserLexer


def l2sw_example():
    with open('examples/l2sw.asm', 'r') as f:
        f.seek(0)
        data = f.readlines()
        return " ".join(data).replace('\n', ' ')


def split_parse(text):
    lst = text.split('.')
    parser_data = [x for x in lst if x.startswith('parser')]
    ma_data = [x for x in lst if x.startswith('match-action')]
    deparser_data = [x for x in lst if x.startswith('deparser')]
    if len(parser_data) != 1 or len(ma_data) < 1 or len(deparser_data) != 1:
        raise SyntaxError("At least one section of each type .parser, "
                          ".match-action and .deparser are required")
    pl = ParserLexer()
    pl.build()
    print(parser_data)
    pl.analyze(parser_data[0])


def test():
    text = l2sw_example()
    split_parse(text)
