class Section(object):
    def __init__(self, name):
        self.name = name


class BinOp(object):
    def __init__(self, opcode, left, right):
        self.opcode = opcode
        self.left, self.right = left, right


class TernaryOp(object):
    def __init__(self, opcode, one, two, three):
        self.opcode = opcode
        self.one, self.two, self.three = one, two, three


class Jump(object):
    def __init__(self, reg, num, label):
        self.reg = reg
        self.num = num
        self.label = label


class Label(object):
    def __init__(self, name):
        self.name = name


class Phv(object):
    def __init__(self, shift):
        self.shift = shift


class Hdr(object):
    def __init__(self, shift):
        self.shift = shift


class Halt(object):
    pass


class Reg(object):
    def __init__(self, name):
        self.name = name
