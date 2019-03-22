from code.ast import *
from code import ParserParser

PHV_LEN = 80
HEADER_LEN = 80
REGISTER_LEN = 64


def _split_header(packet):
    pass


def _update_header(packet, header):
    pass


class Parser(object):
    def __init__(self, data):
        self.text = data
        self.ast = self.__generate_ast()
        self.labels = self.__fill_labels()
        self.phv = None
        self.header = None
        self.r1 = None
        self.r2 = None
        print(self.ast)

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
        labels = {
            'halt': Node(None, Label('halt'))
        }
        while True:
            if current is None:
                break
            if type(current.leaf) is Label:
                labels[current.name] = current
            current = current.child

        return labels

    def process(self, packet):
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
                if getattr(self, leaf.opcode)():
                    if leaf.label not in self.labels:
                        raise Exception("Unknown label: {}".format(leaf.label))
                    current = self.labels[leaf.label].child
                    continue
            else:
                raise Exception("Unexpected leaf type: {}".format(type(leaf)))

            current = current.child

        return _update_header(packet, self.header)

    def store(self, phv, hdr, nbytes):
        self.header[hdr.shift:hdr.shift + nbytes] = self.phv[phv.shift:phv.shift + nbytes]

    def mov(self, op):
        value = None
        if type(op.src) is Phv:
            value = self.phv[op.src.shift:op.src.shift + op.nbytes]
        elif type(op.src) is int:
            value = int
        elif type(op.src) is str:
            pass
        elif type(op.src) is Reg:
            value = getattr(self, op.src.name)[:op.nbytes]
        else:
            raise Exception('Unknown type of first operand for mov: {}'.format(type(op.src)))

        if type(op.dst) is Phv:
            self.phv[op.dst.shift:op.dst.shift + op.nbytes] = value
        elif type(op.dst) is str:
            setattr(self, op.dst, value)
        else:
            raise Exception('Unknown type of second operand for mov: {}'.format(type(op.dst)))

    def cmpje(self, reg, number):
        return getattr(self, reg) == number

    def cmpjn(self, reg, number):
        return getattr(self, reg) != number

    def j(self, reg, number):
        return True
