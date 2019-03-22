from .defines import *


def _split_header(packet):
    return [b for b in packet[:HEADER_LEN]]


class Context(object):
    def __init__(self, packet):
        self.packet = packet
        self.header = _split_header(packet)
        self.phv = [0] * PHV_LEN
        self.portmask = 0x00
