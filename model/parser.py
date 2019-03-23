from code.ast import *
from code import ParserParser
from .defines import *
from .byte_conversion import *
from .meta import Context
import logging


class Parser(object):
    def __init__(self, data):
        self.text = data
        self.ast = self.__generate_ast()
        self.labels = self.__fill_labels()
        self.phv = None
        self.header = None
        self.r1 = None
        self.r2 = None

    def __clear_mem(self):
        self.r1 = [0] * REGISTER_LEN
        self.r2 = [0] * REGISTER_LEN

    def __generate_ast(self):
        parser = ParserParser()
        return parser.parse(self.text)

    def __fill_labels(self):
        current = self.ast
        labels = dict()
        while True:
            if current is None:
                break
            if type(current.leaf) is Label:
                labels[current.leaf.name] = current
            current = current.child

        return labels

    def __dump_registers(self):
        return "\tPHV: {}\n\tHEADER: {}\n\tR1: {}\n\tR2: {}"\
            .format(bytestr(self.phv), bytestr(self.header),
                    bytestr(self.r1), bytestr(self.r2))

    def process(self, context):
        self.__clear_mem()
        current = self.ast
        self.phv = context.phv
        self.header = context.header
        while True:
            if current is None:
                break
            leaf = current.leaf
            if isinstance(leaf, Op):
                getattr(self, leaf.opcode)(leaf)
                logging.debug("Parser memory dump after op \'{}\'\n{}\n"
                              .format(leaf.opcode, self.__dump_registers()))
            elif isinstance(leaf, Jump):
                if getattr(self, leaf.opcode)(leaf):
                    if leaf.label == HALT_LABEL:
                        return None, None
                    if leaf.label not in self.labels:
                        raise Exception("Unknown label: {}".format(leaf.label))
                    current = self.labels[leaf.label].child
                    continue
            elif isinstance(leaf, Label):
                pass
            else:
                raise Exception("Unexpected leaf type: {}".format(type(leaf)))

            current = current.child
        return Context(context.packet, self.header, self.phv, context.portmask)

    def store(self, op):
        phv_shift = op.first.shift
        hdr_shift = op.second.shift
        nbytes = op.third
        self.phv[phv_shift:phv_shift + nbytes] = self.header[hdr_shift:hdr_shift + nbytes]

    def mov(self, op):
        value = None
        src = op.second
        dst = op.first
        nbytes = op.third
        if isinstance(src, Phv):
            phv_shift = src.shift
            value = self.phv[phv_shift:phv_shift + nbytes]
        elif isinstance(src, int):
            value = to_bytes(src, nbytes)
        elif isinstance(src, Reg):
            value = getattr(self, src.name)[:nbytes]
        else:
            raise Exception('Unknown type of second operand for mov: {}'.format(type(src)))

        if isinstance(dst, Phv):
            self.phv[dst.shift:dst.shift + nbytes] = value
        elif isinstance(dst, Reg):
            reg = getattr(self, dst.name)
            reg[:nbytes] = value
        else:
            raise Exception('Unknown type of first operand for mov: {}'.format(type(dst)))

    def cmpje(self, op):
        return getattr(self, op.reg.name) == op.num

    def cmpjn(self, op):
        return getattr(self, op.reg.name) != op.num

    def j(self, op):
        return True
