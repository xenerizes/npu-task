from code.ast import *


class Parser(object):
    def __init__(self, ast):
        self.ast = ast
        self.phv = [0] * 80
        self.header = [0] * 80
        self.r1 = [0] * 64
        self.r2 = [0] * 64

    def process(self, packet):
        pass

    def store(self, phv_shift, hdr_shift, nbytes):
        self.header[hdr_shift:hdr_shift + nbytes] = self.phv[phv_shift:phv_shift + nbytes]

    def mov(self, dst, src, nbytes):
        value = None
        if type(src) == Phv:
            value = self.phv[src.shift:src.shift + nbytes]
        else:
            value = getattr(self, src)[:nbytes]
        if type(dst) == Phv:
            self.phv[dst.shift:dst.shift + nbytes] = value
        else:
            setattr(self, dst, value)

    def cmpje(self, reg, number, label):
        pass

    def cmpjn(self, reg, number, label):
        pass

    def j(self, reg, number, label):
        pass

    def halt(self):
        pass
