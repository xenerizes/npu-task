from code.ast import *
from code import ParserParser
from .defines import *
from .byte_conversion import to_bytes


def _split_header(packet):
    return [b for b in packet[:HEADER_LEN]]


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
        self.phv = [0] * PHV_LEN
        self.header = None
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
                labels[current.name] = current
            current = current.child

        return labels

    def process(self, packet, portmask):
        self.__clear_mem()
        self.header = _split_header(packet)
        current = self.ast
        while True:
            if current is None:
                break
            leaf = current.leaf
            if isinstance(leaf, Op):
                getattr(self, leaf.opcode)(leaf)
            elif isinstance(leaf, Jump):
                if getattr(self, leaf.opcode)(leaf):
                    if leaf.label == HALT_LABEL:
                        return None, None
                    if leaf.label not in self.labels:
                        raise Exception("Unknown label: {}".format(leaf.label))
                    current = self.labels[leaf.label].child
                    continue
            else:
                raise Exception("Unexpected leaf type: {}".format(type(leaf)))

            current = current.child

        return self.header, portmask

    def store(self, op):
        phv_shift = op.first.shift
        hdr_shift = op.second.shift
        nbytes = op.third
        self.header[hdr_shift:hdr_shift + nbytes] = self.phv[phv_shift:phv_shift + nbytes]

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
            raise Exception('Unknown type of first operand for mov: {}'.format(type(op.dst)))

    def cmpje(self, op):
        return getattr(self, op.reg.name) == op.num

    def cmpjn(self, op):
        return getattr(self, op.reg.name) != op.num

    def j(self, op):
        return True
