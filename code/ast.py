class Node(object):
    def __init__(self, child=None, leaf=None):
        self.child = child
        self.leaf = leaf


class Section(object):
    def __init__(self, id):
        self.id = id


class Op(object):
    def __init__(self, opcode):
        self.opcode = opcode


class BinOp(Op):
    def __init__(self, opcode, left, right):
        Op.__init__(self, opcode)
        self.left, self.right = left, right

    def __str__(self):
        return "{} {}, {}".format(self.opcode, self.left, self.right)


class TernaryOp(Op):
    def __init__(self, opcode, one, two, three):
        Op.__init__(self, opcode)
        self.first, self.second, self.third = one, two, three

    def __str__(self):
        return "{} {}, {}, {}".format(self.opcode, self.first,
                                      self.second, self.third)


class Jump(object):
    def __init__(self, opcode, reg, num, label):
        self.opcode = opcode
        self.reg = reg
        self.num = num
        self.label = label


class Call(object):
    def __init__(self, procedure):
        self.procedure = procedure


class Label(object):
    def __init__(self, name):
        self.name = name


class Phv(object):
    def __init__(self, shift):
        self.shift = shift

    def __str__(self):
        return "PHV{}".format('+{}'.format(self.shift) if self.shift else '')


class Portmask(object):
    def __str__(self):
        return "PORTMASK"


class Hdr(object):
    def __init__(self, shift):
        self.shift = shift

    def __str__(self):
        return "HEADER{}".format('+{}'.format(self.shift) if self.shift else '')


class Reg(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
