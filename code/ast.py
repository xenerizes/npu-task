class Node(object):
    def __init__(self, child=None, leaf=None):
        self.child = child
        self.leaf = leaf

    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
               other.child == self.child and \
               other.leaf == self.leaf


class Section(object):
    def __init__(self, id):
        self.id = id

    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
               self.id == other.id


class Op(object):
    def __init__(self, opcode):
        self.opcode = opcode

    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
               self.opcode == other.opcode


class BinOp(Op):
    def __init__(self, opcode, left, right):
        Op.__init__(self, opcode)
        self.left, self.right = left, right

    def __str__(self):
        return "{} {}, {}".format(self.opcode, self.left, self.right)

    def __eq__(self, other):
        return Op.__eq__(self, other) and \
               isinstance(other, self.__class__) and \
               self.left == other.left and \
               self.right == other.right


class TernaryOp(Op):
    def __init__(self, opcode, one, two, three):
        Op.__init__(self, opcode)
        self.first, self.second, self.third = one, two, three

    def __str__(self):
        return "{} {}, {}, {}".format(self.opcode, self.first,
                                      self.second, self.third)

    def __eq__(self, other):
        return Op.__eq__(self, other) and \
               isinstance(other, self.__class__) and \
               self.first == other.first and \
               self.second == other.second and \
               self.third == other.third


class Jump(object):
    def __init__(self, opcode, reg, num, label):
        self.opcode = opcode
        self.reg = reg
        self.num = num
        self.label = label

    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
               self.opcode == other.opcode and \
               self.reg == other.reg and \
               self.num == other.num and \
               self.label == other.label


class Call(object):
    def __init__(self, procedure):
        self.procedure = procedure

    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
               self.procedure == other.procedure


class Label(object):
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
               self.name == other.name


class Phv(object):
    def __init__(self, shift):
        self.shift = shift

    def __str__(self):
        return "PHV{}".format('+{}'.format(self.shift) if self.shift else '')

    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
               self.shift == other.shift


class Portmask(object):
    def __str__(self):
        return "PORTMASK"

    def __eq__(self, other):
        return isinstance(other, self.__class__)


class Hdr(object):
    def __init__(self, shift):
        self.shift = shift

    def __str__(self):
        return "HEADER{}".format('+{}'.format(self.shift) if self.shift else '')

    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
               self.shift == other.shift


class Reg(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
               self.name == other.name
