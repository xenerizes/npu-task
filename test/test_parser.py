from unittest import TestCase
from code.ast import *
from code.parser import ParserParser


class ParserParserTestCase(TestCase):
    def setUp(self):
        self.parser = ParserParser()

    def node_ternary_eq(self, ast, op, v1, v2, v3):
        self.assertIsInstance(ast, Node)
        self.assertIsInstance(ast.leaf, TernaryOp)
        self.assertEqual(ast.leaf, TernaryOp(op, v1, v2, v3))

    def node_binary_eq(self, ast, op, v1, v2):
        self.assertIsInstance(ast, Node)
        self.assertIsInstance(ast.leaf, BinOp)
        self.assertEqual(ast.leaf, BinOp(op, v1, v2))

    def node_j_eq(self, ast, op, reg, num, label):
        self.assertIsInstance(ast, Node)
        self.assertIsInstance(ast.leaf, Jump)
        self.assertEqual(ast.leaf, Jump(op, reg, num, label))

    def node_label_eq(self, ast, name):
        self.assertIsInstance(ast, Node)
        self.assertIsInstance(ast.leaf, Label)
        self.assertEqual(ast.leaf, Label(name))

    def test_empty(self):
        test_str = "parser "
        ast = self.parser.parse(test_str)
        self.assertEqual(ast, None)

    def test_store(self):
        test_str = "parser " \
                   "store PHV, HEADER, 0"
        ast = self.parser.parse(test_str)
        self.assertEqual(ast.child, None)
        self.node_ternary_eq(ast, "store", Phv(0), Hdr(0), 0)

        test_str = "parser " \
                   "store PHV + 1, HEADER+2, 33"
        ast = self.parser.parse(test_str)
        self.assertEqual(ast.child, None)
        self.node_ternary_eq(ast, "store", Phv(1), Hdr(2), 33)

        test_str = "parser " \
                   "store PHV, HEADER +55, 1"
        ast = self.parser.parse(test_str)
        self.assertEqual(ast.child, None)
        self.node_ternary_eq(ast, "store", Phv(0), Hdr(55), 1)

    def test_mov(self):
        test_str = "parser " \
                   "mov r1, r1, 16"
        ast = self.parser.parse(test_str)
        self.assertEqual(ast.child, None)
        self.node_ternary_eq(ast, "mov", Reg('r1'), Reg('r1'), 16)

        test_str = "parser " \
                   "mov PHV, r1, 8"
        ast = self.parser.parse(test_str)
        self.assertEqual(ast.child, None)
        self.node_ternary_eq(ast, "mov", Phv(0), Reg('r1'), 8)

        test_str = "parser " \
                   "mov r1, r2, 0"
        ast = self.parser.parse(test_str)
        self.assertEqual(ast.child, None)
        self.node_ternary_eq(ast, "mov", Reg('r1'), Reg('r2'), 0)

        test_str = "parser " \
                   "mov r1, 35, 2"
        ast = self.parser.parse(test_str)
        self.assertEqual(ast.child, None)
        self.node_ternary_eq(ast, "mov", Reg('r1'), 35, 2)

    def test_logic(self):
        test_str = "parser " \
                   "or r1, r1  " \
                   "and r1, r2 " \
                   "xor r2, 6"
        ast = self.parser.parse(test_str)
        self.assertNotEqual(ast, None)
        self.assertNotEqual(ast.child, None)
        self.assertNotEqual(ast.child.child, None)
        self.assertEqual(ast.child.child.child, None)
        self.node_binary_eq(ast, 'or_op', Reg('r1'), Reg('r1'))
        self.node_binary_eq(ast.child, 'and_op', Reg('r1'), Reg('r2'))
        self.node_binary_eq(ast.child.child, 'xor_op', Reg('r2'), 6)

    def test_jumps(self):
        test_str = "parser " \
                   "cmpje r1, 10, label1 " \
                   "cmpjn r2, 5, halt " \
                   "j start"
        ast = self.parser.parse(test_str)
        self.assertNotEqual(ast, None)
        self.assertNotEqual(ast.child, None)
        self.assertNotEqual(ast.child.child, None)
        self.assertEqual(ast.child.child.child, None)
        self.node_j_eq(ast, 'cmpje', Reg('r1'), 10, 'label1')
        self.node_j_eq(ast.child, 'cmpjn', Reg('r2'), 5, 'halt')
        self.node_j_eq(ast.child.child, 'j', 0, 0, 'start')

    def test_labels(self):
        test_str = "parser " \
                   "l1: "
        ast = self.parser.parse(test_str)
        self.assertEqual(ast.child, None)
        self.node_label_eq(ast, "l1")

        test_str = "parser " \
                   "xor r1, r1 " \
                   "l2: " \
                   "and r2, 0 " \
                   "j l2"
        ast = self.parser.parse(test_str)
        self.assertNotEqual(ast, None)
        self.assertNotEqual(ast.child, None)
        self.assertNotEqual(ast.child.child, None)
        self.assertNotEqual(ast.child.child.child, None)
        self.assertEqual(ast.child.child.child.child, None)
        self.node_label_eq(ast.child, "l2")
