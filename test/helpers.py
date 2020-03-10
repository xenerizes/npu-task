from unittest import TestCase
from code.ast import *


class ParserTestCase(TestCase):
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
