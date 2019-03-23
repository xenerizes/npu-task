from code import DeparserParser
from .defines import *
from code.ast import *
from .meta import Context
from .byte_conversion import bytestr
import logging


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

    def __dump_registers(self):
        return "PHV: {}\nHEADER: {}"\
            .format(bytestr(self.phv), bytestr(self.header))

    def process(self, context):
        current = self.ast
        self.phv = context.phv
        self.header = context.header
        while True:
            if current is None:
                break
            leaf = current.leaf
            if isinstance(leaf, Op):
                logging.debug("Applying op \'{}\'...".format(leaf.opcode))
                getattr(self, leaf.opcode)(leaf)
                logging.debug("Deparser memory dump after op \'{}\'\n{}\n"
                              .format(leaf.opcode, self.__dump_registers()))
            else:
                raise Exception("Unexpected leaf type: {}".format(type(leaf)))
        _update_header(context.packet, context.header)

        return Context(context.packet, self.header, self.phv, context.portmask)

    def load(self, op):
        phv_shift = op.first.shift
        hdr_shift = op.second.shift
        nbytes = op.third
        self.header[hdr_shift:hdr_shift + nbytes] = self.phv[phv_shift:phv_shift + nbytes]
