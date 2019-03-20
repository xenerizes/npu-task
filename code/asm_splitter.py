from .parser import ParserParser
from .match_action import MatchActionParser
from .deparser import DeparserParser


def l2sw_example():
    with open('examples/l2sw.asm', 'r') as f:
        f.seek(0)
        data = f.readlines()
        return " ".join(data).replace('\n', ' ')


def split_parse(text):
    lst = text.split('.')
    parser_data = [x for x in lst if x.startswith('parser')]
    ma_data = [x for x in lst if x.startswith('match_action')]
    deparser_data = [x for x in lst if x.startswith('deparser')]
    if len(parser_data) != 1 or len(ma_data) < 1 or len(deparser_data) != 1:
        raise SyntaxError("At least one section of each type .parser, "
                          ".match-action and .deparser are required")
    parsers = {
        " ".join(parser_data): ParserParser(),
        " ".join(ma_data): MatchActionParser(),
        " ".join(deparser_data): DeparserParser()
    }

    for data, parser in parsers.items():
        parser.build()
        parser.parse(data)


def test():
    text = l2sw_example()
    split_parse(text)
