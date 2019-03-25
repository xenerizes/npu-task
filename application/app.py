from argparse import ArgumentParser
from model import *
from scapy.packet import Raw
from scapy.layers.l2 import Ether
from scapy.plist import PacketList
from scapy.utils import rdpcap
from glob import glob
from json import loads
import logging

LOGGING_FORMAT = '%(levelname)s: %(message)s'


def make_parser():
    parser = ArgumentParser(description='NPU model')
    parser.add_argument('asm', metavar='ASM', type=str,
                        help='filename with assembler code')
    parser.add_argument('-i', '--input', metavar='PCAP', type=str, default=None,
                        help='pcap file with ')
    parser.add_argument('-o', '--output', metavar='DIR', type=str, default=None,
                        help='name of directory containing output pcap files')
    parser.add_argument('-t', '--tables', metavar='JSON', type=str, default=None,
                        help='json file containing switch tables')
    parser.add_argument('--debug', action='store_true',
                        help='enable debug mode')
    return parser


def convert_portmask(portmask):
    if portmask is None:
        return []
    bits = reversed(list('{0:08b}'.format(portmask)))
    return [b for b, v in enumerate(bits) if v is '1']


def visual(real, expected):
    logging.info("Expected packets are:")
    PacketList([Ether(p) for p in real]).show()
    logging.info("Processed packets are:")
    PacketList([Ether(p) for p in expected]).show()


def compare_output(real, expected):
    if None in [real, expected]:
        logging.error("Nothing to compare at one of the sides!")
        return False

    for port, packets in real.items():
        if port not in expected.keys():
            if len(packets) > 0:
                logging.error("No packets expected on port {}, got {}"
                              .format(port, len(packets)))
                return False
            continue
        if set(packets) != set(expected[port]):

            if len(packets) == len(expected[port]):
                logging.error("Expected packets with different headers on port {}"
                              .format(port))
                visual(packets, expected[port])
            else:
                logging.error("Expected {} packets on port {}, got {}"
                              .format(len(expected[port]), port, len(packets)))
                visual(packets, expected[port])
            return False
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
        self.syntax_mode = False
        self.processors = []
        self.tables = None
        loglevel = logging.DEBUG if self.args.debug else logging.INFO
        logging.basicConfig(format=LOGGING_FORMAT, level=loglevel)

    def run(self):
        self.asm = self.__read_asm()
        self.syntax = self.__split()
        self.input = self.__load_in_pcaps()
        self.syntax_mode = self.input is None or self.args.tables is None
        if self.syntax_mode:
            logging.warning('Empty input, syntax check mode')

        self.__make_processors()
        logging.info("Syntax is correct")
        if self.syntax_mode:
            return

        self.expected = self.__load_out_pcaps()
        self.output = self.__run_model()
        if compare_output(self.output, self.expected):
            logging.info('Ok!')
        else:
            logging.error('Packets didn\'t go as expected')

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
        return [
            (Parser, parser_data),
            (MatchAction, ma_data),
            (Deparser, deparser_data)
        ]

    def __load_tables(self):
        with open(self.args.tables, 'r') as file:
            data = loads(file.read())
        if "tables" not in data.keys():
            raise Exception("Incorrect tables file format")
        return data["tables"]

    def __make_processors(self):
        for processor, data in self.syntax:
            for section in data:
                self.processors.append(processor(section))

        self.tables = self.__load_tables()
        for ma in filter(lambda x: isinstance(x, MatchAction), self.processors):
            ma.load_table(self.tables)

    def __load_in_pcaps(self):
        return None if self.args.input is None \
            else [Raw(packet).load for packet in rdpcap(self.args.input)]

    def __load_out_pcaps(self):
        if self.args.output is None:
            return None

        pcap_list = glob('{}/*.pcap'.format(self.args.output))
        packet_map = dict()
        for port in range(8):
            port_pcap = [pcap for pcap in pcap_list
                         if pcap.endswith('{}.pcap'.format(port))]
            if len(port_pcap):
                packet_map[port] = [Raw(packet).load for packet in rdpcap(port_pcap[0])]
        return packet_map

    def __run_model(self):
        output = {port: list() for port in range(8)}
        for packet in self.input:
            logging.debug("Starting packet processing...")
            context = Context(packet)
            for p in self.processors:
                logging.debug("Processing by {} stage...".format(type(p).__name__))
                context = p.process(context)
                if context is None:
                    logging.debug("Packet dropped\n")
                    break
            if context is None:
                continue
            logging.debug("Packet context after processing:\n{}\n".format(context))
            output_ports = convert_portmask(context.portmask)
            for port in output_ports:
                output[port].append(context.packet)
        return output
