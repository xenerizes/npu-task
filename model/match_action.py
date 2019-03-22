from code.ast import *
from code import MatchActionParser
from .defines import *
from .byte_conversion import *

PORTMASK_SZ = 255


class MatchAction(object):
    def __init__(self, data):
        self.text = data
        self.ast = self.__generate_ast()
        self.labels = self.__fill_labels()
        self.phv = None
        self.portmask = None
        self.r1 = None
        self.r2 = None
        self.r3 = None
        self.table = None

    def load_table(self, tables):
        instance = self.ast.leaf.id
        if instance not in tables:
            raise Exception("Table with id {} is undefined. "
                            "Check your section enumeration".format(instance))
        self.table = tables[instance]

    def __clear_mem(self):
        self.r1 = [0] * REGISTER_LEN
        self.r2 = [0] * REGISTER_LEN
        self.r3 = [0] * REGISTER_LEN

    def __generate_ast(self):
        parser = MatchActionParser()
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

    def process(self, context):
        self.__clear_mem()
        current = self.ast
        self.phv = context.phv
        self.portmask = context.portmask
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

    def mov(self, op):
        value = None
        src = op.second
        dst = op.first
        nbytes = op.third
        if isinstance(src, Phv):
            phv_shift = src.shift
            value = self.phv[phv_shift:phv_shift + nbytes]
        elif isinstance(src, Portmask):
            if nbytes > 1:
                raise Exception("Cannot mov more than 1 byte from portmask!")
            value = self.portmask[:]
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
        elif isinstance(dst, Portmask):
            if nbytes > 1:
                raise Exception("Cannot mov more than 1 byte to portmask!")
            self.portmask = value
        else:
            raise Exception('Unknown type of first operand for mov: {}'.format(type(op.dst)))

    def or_op(self, op):
        value = None
        src = op.second
        dst = op.first
        if isinstance(src, int):
            value = src
        elif isinstance(src, Reg):
            value = getattr(self, src.name)
        else:
            raise Exception('Unknown type of second operand for or: {}'.format(type(src)))

        if isinstance(dst, Reg):
            reg = getattr(self, dst.name)
            value = to_register(value)
            reg[:] = [reg[i] or value[i] for i in range(len(value))]
        elif isinstance(dst, Portmask):
            if len(value) > 1:
                raise Exception("Cannot mov more than 1 byte to portmask!")
            self.portmask[0] = self.portmask[0] or value[0]
        else:
            raise Exception('Unknown type of first operand for mov: {}'.format(type(op.dst)))

    def cmpje(self, op):
        return getattr(self, op.reg.name) == op.num

    def cmpjn(self, op):
        return getattr(self, op.reg.name) != op.num

    def j(self, op):
        return True
