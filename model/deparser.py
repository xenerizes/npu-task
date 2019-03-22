from code import DeparserParser
from .defines import *
from code.ast import *


def _update_header(packet, header):
    packet = bytearray(packet)
    packet[:HEADER_LEN] = header
    packet = bytes(packet)


class Deparser(object):
    def __init__(self, data):
        self.text = data
        self.ast = self.__generate_ast()
        self.phv = None
        self.header = None

    def __generate_ast(self):
        parser = DeparserParser()
        return parser.parse(self.text)

    def process(self, context):
        _update_header(context.packet, context.header)
