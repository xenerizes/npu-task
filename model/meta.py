from .defines import *


def _split_header(packet):
    return [b for b in packet[:HEADER_LEN]]


class Context(object):
    def __init__(self, packet, header=None, phv=None, portmask=None):
        self.packet = packet
        self.header = _split_header(packet) if header is None else header
        self.phv = [0] * PHV_LEN if phv is None else phv
        self.portmask = [0x00] if portmask is None else portmask
