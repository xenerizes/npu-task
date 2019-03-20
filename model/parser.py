from code.ast import *
from code import ParserParser


class Parser(object):
    def __init__(self, data):
        self.text = data
        self.ast = self.generate_ast()
        self.phv = [0] * 80
        self.header = [0] * 80
        self.r1 = [0] * 64
        self.r2 = [0] * 64
        print(self.ast)

    def generate_ast(self):
        parser = ParserParser()
        return parser.parse(self.text)

    def process(self, packet):
        pass

    def store(self, phv, hdr, nbytes):
        self.header[hdr.shift:hdr.shift + nbytes] = self.phv[phv.shift:phv.shift + nbytes]

    def mov(self, dst, src, nbytes):
        value = None
        if type(src) == Phv:
            value = self.phv[src.shift:src.shift + nbytes]
        elif type(src) == int:
            value = int
        elif type(src) == str:
            pass
        elif type(src) == Reg:
            value = getattr(self, src.name)[:nbytes]
        else:
            raise Exception('Unknown second operand for mov')

        if type(dst) == Phv:
            self.phv[dst.shift:dst.shift + nbytes] = value
        elif type(dst) == str:
            setattr(self, dst, value)
        else:
            raise Exception('Unknown second operand for mov')

    def cmpje(self, reg, number, label):
        if getattr(self, reg) == number:
            pass

    def cmpjn(self, reg, number, label):
        if getattr(self, reg) != number:
            pass

    def j(self, reg, number, label):
        pass

    def halt(self):
        pass
