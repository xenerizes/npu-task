from .defines import *


def _update_header(packet, header):
    packet[:HEADER_LEN] = header


class Deparser(object):
    def __init__(self, data):
        self.text = data
        self.phv = None
        self.header = None

    def process(self, packet, header, portmask):
        return packet, header, portmask
