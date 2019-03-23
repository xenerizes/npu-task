from code.ast import *
from code import MatchActionParser
from .defines import *
from .byte_conversion import *
from .meta import Context
import logging


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
                labels[current.leaf.name] = current
            current = current.child

        return labels

    def __dump_registers(self):
        return "\tPHV: {}\n\tPORTMASK: {}\n\tR1: {}\n\tR2: {}\n\tR3: {}"\
            .format(bytestr(self.phv), self.portmask,
                    bytestr(self.r1), bytestr(self.r2), bytestr(self.r3))

    def process(self, context):
        self.__clear_mem()
        current = self.ast.child
        self.phv = context.phv
        self.portmask = context.portmask
        while True:
            if current is None:
                break
            leaf = current.leaf
            if isinstance(leaf, Op):
                logging.debug("Applying op \'{}\'...".format(leaf.opcode))
                getattr(self, leaf.opcode)(leaf)
                logging.debug("Match-Action memory dump after op \'{}\'\n{}\n"
                              .format(leaf.opcode, self.__dump_registers()))
            elif isinstance(leaf, Jump):
                logging.debug("Applying \'{}\' to label \'{}\'..."
                              .format(leaf.opcode, leaf.label))
                if getattr(self, leaf.opcode)(leaf):
                    if leaf.label == HALT_LABEL:
                        return None, None
                    if leaf.label not in self.labels:
                        raise Exception("Unknown label: {}".format(leaf.label))
                    current = self.labels[leaf.label].child
                    continue
            elif isinstance(leaf, Call):
                logging.debug("Calling \'{}\'..."
                              .format(leaf.procedure))
                self.call(leaf.procedure)
                logging.debug("Match-Action memory dump after op \'call\'\n{}\n"
                              .format(self.__dump_registers()))
            elif isinstance(leaf, Label):
                pass
            else:
                raise Exception("Unexpected leaf type: {}".format(type(leaf)))

            current = current.child
        return Context(context.packet, context.header, self.phv, self.portmask)

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
            value = [int(self.portmask)]
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
            self.portmask = value[0]
        else:
            raise Exception('Unknown type of first operand for mov: {}'.format(type(dst)))

    def op_impl(self, op, func):
        dst = op.left
        src = op.right
        if isinstance(dst, Reg):
            reg = getattr(self, dst.name)
            value = to_register(src) if isinstance(src, int) \
                else getattr(self, src.name) if isinstance(src, Reg) \
                else None
            res = [func(r, v) for r, v in zip(reg, value)]
            setattr(self, dst, res)
        elif isinstance(dst, Portmask):
            value = src if isinstance(src, int) \
                else getattr(self, src.name)[0] if isinstance(src, Reg) \
                else None
            self.portmask = func(self.portmask, value)
        else:
            raise Exception('Unknown type of first operand for {}: {}'
                            .format(op.opcode, type(dst)))

    def or_op(self, op):
        self.op_impl(op, lambda x, y: x | y)

    def and_op(self, op):
        self.op_impl(op, lambda x, y: x & y)

    def xor_op(self, op):
        self.op_impl(op, lambda x, y: x ^ y)

    def shl(self, op):
        reg = getattr(self, op.left)
        reg[op.right:] = reg[:-op.right]
        reg[:op.right] = [0] * op.right

    def shr(self, op):
        reg = getattr(self, op.left)
        reg[:op.right] = reg[op.right:]
        reg[op.right:] = [0] * (REGISTER_LEN - op.right)

    def call(self, procedure):
        if procedure not in ["exact_match", "longest_prefix_match"]:
            raise Exception("Cannot find procedure {}".format(procedure))
        self.search()

    def search(self):
        key = str(self.r1[:6])
        self.r2 = [0] * REGISTER_LEN
        if self.ast.leaf.id == 1:
            table_src = {
                '\x01\x02\x03\x04\x05\x06': 4,
                '\x01\x02\x04\x08\x16\x32': 5
            }
            if key in table_src:
                self.r1 = [0] * REGISTER_LEN
                self.r1[:6] = table_src[key]
            else:
                self.r2[0] = 1
        else:
            table_dst = {
                '\x01\x02\x04\x08\x16\x32': 5
            }
            if key in table_dst:
                self.r1 = [0] * REGISTER_LEN
                self.r1[:6] = table_dst[key]
            else:
                self.r2[0] = 1

    def cmpje(self, op):
        return getattr(self, op.reg.name) == op.num

    def cmpjn(self, op):
        return getattr(self, op.reg.name) != op.num

    def j(self, op):
        return True
