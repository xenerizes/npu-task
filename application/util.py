from argparse import ArgumentParser
from scapy.layers.l2 import Ether
from scapy.plist import PacketList
import logging


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


def packet_list_summary(pl):
    return '\t' + '\n\t'.join([Ether(p).summary() for p in pl])


def visual(real, expected):
    logging.info("Expected packets are:\n{}".format(packet_list_summary(expected)))
    logging.info("Processed packets are:\n{}".format(packet_list_summary(real)))


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
