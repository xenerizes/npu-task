from .helpers import ParserTestCase
from code.match_action import MatchActionParser
from code.ast import *


class MAParserTestCase(ParserTestCase):
    def setUp(self):
        self.parser = MatchActionParser()

    def ast_level_1(self, ast):
        self.assertNotEqual(ast, None)
        self.assertNotEqual(ast.child, None)
        self.assertEqual(ast.child.child, None)

    def test_empty(self):
        test_str = "match_action 48"
        ast = self.parser.parse(test_str)
        self.assertNotEqual(ast, None)
        self.assertEqual(ast.child, None)
        self.assertEqual(ast.leaf, Section(48))

    def test_mov(self):
        test_str = "match_action 1 " \
                   "mov r1, r1, 16"
        ast = self.parser.parse(test_str)
        self.ast_level_1(ast)
        self.node_ternary_eq(ast.child, "mov", Reg('r1'), Reg('r1'), 16)

        test_str = "match_action 1 " \
                   "mov PHV + 5, r1, 8"
        ast = self.parser.parse(test_str)
        self.ast_level_1(ast)
        self.node_ternary_eq(ast.child, "mov", Phv(5), Reg('r1'), 8)

        test_str = "match_action 1 " \
                   "mov PORTMASK, r2, 4"
        ast = self.parser.parse(test_str)
        self.ast_level_1(ast)
        self.node_ternary_eq(ast.child, "mov", Portmask(), Reg('r2'), 4)

        test_str = "match_action 1 " \
                   "mov r1, 35, 4"
        ast = self.parser.parse(test_str)
        self.ast_level_1(ast)
        self.node_ternary_eq(ast.child, "mov", Reg('r1'), 35, 4)

        test_str = "match_action 1 " \
                   "mov PHV, 10, 8"
        ast = self.parser.parse(test_str)
        self.ast_level_1(ast)
        self.node_ternary_eq(ast.child, "mov", Phv(0), 10, 8)

        test_str = "match_action 1 " \
                   "mov PORTMASK, 17, 7"
        ast = self.parser.parse(test_str)
        self.ast_level_1(ast)
        self.node_ternary_eq(ast.child, "mov", Portmask(), 17, 7)

    def test_logic(self):
        test_str = "match_action 1 " \
                   "or r1, r2 " \
                   "and r1, 7 " \
                   "xor PORTMASK, r3 " \
                   "xor PORTMASK, 16"
        ast = self.parser.parse(test_str)
        self.assertEqual(ast.child.child.child.child.child, None)
        self.node_binary_eq(ast.child, 'or_op', Reg('r1'), Reg('r2'))
        self.node_binary_eq(ast.child.child, 'and_op', Reg('r1'),7)
        self.node_binary_eq(ast.child.child.child, 'xor_op', Portmask(), Reg('r3'))
        self.node_binary_eq(ast.child.child.child.child, 'xor_op', Portmask(), 16)

    def test_jumps(self):
        test_str = "match_action 1 " \
                   "cmpje r1, 10, label1 " \
                   "cmpjn r2, 5, halt " \
                   "j start"
        ast = self.parser.parse(test_str)
        self.assertEqual(ast.child.child.child.child, None)
        self.node_j_eq(ast.child, 'cmpje', Reg('r1'), 10, 'label1')
        self.node_j_eq(ast.child.child, 'cmpjn', Reg('r2'), 5, 'halt')
        self.node_j_eq(ast.child.child.child, 'j', 0, 0, 'start')

    def test_arithm(self):
        test_str = "match_action 1 " \
                   "mod r1, 4 " \
                   "mod r2, r1"
        ast = self.parser.parse(test_str)
        self.assertEqual(ast.child.child.child, None)
        self.node_binary_eq(ast.child, 'mod_op', Reg('r1'), 4)
        self.node_binary_eq(ast.child.child, 'mod_op', Reg('r2'), Reg('r1'))

    def test_shifts(self):
        test_str = "match_action 2 " \
                   "shl r1, 11 " \
                   "shr r2, 0x778"
        ast = self.parser.parse(test_str)
        self.assertEqual(ast.child.child.child, None)
        self.node_binary_eq(ast.child, 'shl', Reg('r1'), 11)
        self.node_binary_eq(ast.child.child, 'shr', Reg('r2'), 0x778)

    def test_labels(self):
        test_str = "match_action 2 " \
                   "l1: "
        ast = self.parser.parse(test_str)
        self.ast_level_1(ast)
        self.node_label_eq(ast.child, "l1")

        test_str = "match_action 2 " \
                   "xor r1, r1 " \
                   "l2: " \
                   "and r2, 0 " \
                   "j l2"
        ast = self.parser.parse(test_str)
        self.assertEqual(ast.child.child.child.child.child, None)
        self.node_label_eq(ast.child.child, "l2")

    def test_call(self):
        test_str = "match_action 21 " \
                   "call procedure"
        ast = self.parser.parse(test_str)
        self.assertEqual(ast.child.leaf, Call('procedure'))
