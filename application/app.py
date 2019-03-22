from argparse import ArgumentParser
from model import *
from scapy.packet import Raw
from scapy.utils import rdpcap


def make_parser():
    parser = ArgumentParser(description='NPU model')
    parser.add_argument('asm', metavar='ASM', type=str,
                        help='filename with assembler code')
    parser.add_argument('-i', '--input', metavar='PCAP', type=str, default=None,
                        help='pcap file with ')
    parser.add_argument('-o', '--output', metavar='DIR', type=str, default=None,
                        help='directory containing output pcap files')
    return parser


def compare_output(real, expected):
    return True


class Application(object):
    def __init__(self, args):
        parser = make_parser()
        self.args = parser.parse_args(args)
        self.asm = None
        self.syntax = None
        self.input = None
        self.output = None
        self.expected = None
        self.processors = []

    def run(self):
        self.asm = self.__read_asm()
        self.syntax = self.__split()
        self.__make_processors()
        self.input = self.__load_in_pcaps()
        if self.input is not None:
            self.expected = self.__load_out_pcaps()
            self.output = self.__run_model()
            if compare_output(self.output, self.expected):
                print('ok!')

    def __read_asm(self):
        with open(self.args.asm, 'r') as f:
            f.seek(0)
            data = f.readlines()
            return " ".join(data).replace('\n', ' ')

    def __split(self):
        lst = self.asm.split('.')
        parser_data = [x for x in lst if x.startswith('parser')]
        ma_data = [x for x in lst if x.startswith('match_action')]
        deparser_data = [x for x in lst if x.startswith('deparser')]
        if len(parser_data) != 1 or len(ma_data) < 1 or len(deparser_data) != 1:
            raise SyntaxError("At least one section of each type .parser, "
                              ".match-action and .deparser are required")
        return {
            Parser: parser_data,
            MatchAction: ma_data,
            Deparser: deparser_data
        }

    def __make_processors(self):
        for processor, data in self.syntax.items():
            for section in data:
                self.processors.append(processor(section))

    def __load_in_pcaps(self):
        return None if self.args.input is None \
            else [Raw(packet).load for packet in rdpcap(self.args.input)]

    def __load_out_pcaps(self):
        pass

    def __run_model(self):
        output = []
        for packet in self.input:
            portmask = None
            for p in self.processors:
                pkt, portmask = p.process(packet)
                if not pkt:
                    break
            output.append((pkt, portmask))
        return output
