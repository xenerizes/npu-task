from unittest import TestCase
from code.deparser import DeparserParser
from code.ast import *


class DeparserParserTestCase(TestCase):
    def setUp(self):
        self.parser = DeparserParser()

    def node_eq(self, ast, v1, v2, v3):
        self.assertIsInstance(ast, Node)
        self.assertIsInstance(ast.leaf, TernaryOp)
        self.assertEqual(ast.leaf, TernaryOp('load', Hdr(v1), Phv(v2), v3))

    def test_parse_empty(self):
        test_str = "deparser"
        ast = self.parser.parse(test_str)
        self.assertEqual(ast, None)

    def test_parse_one_empty(self):
        test_str = "deparser " \
                   "load HEADER, PHV, 0"
        ast = self.parser.parse(test_str)
        self.assertEqual(ast.child, None)
        self.node_eq(ast, 0, 0, 0)

    def test_parse_one_shifted(self):
        test_str = "deparser " \
                   "load HEADER + 2, PHV + 11, 3"
        ast = self.parser.parse(test_str)
        self.assertEqual(ast.child, None)
        self.node_eq(ast, 2, 11, 3)

        test_str = "deparser " \
                   "load HEADER + 0, PHV + 0, 5"
        ast = self.parser.parse(test_str)
        self.assertEqual(ast.child, None)
        self.node_eq(ast, 0, 0, 5)

        test_str = "deparser " \
                   "load HEADER, PHV + 1, 5"
        ast = self.parser.parse(test_str)
        self.assertEqual(ast.child, None)
        self.node_eq(ast, 0, 1, 5)

        test_str = "deparser " \
                   "load HEADER + 7, PHV, 7"
        ast = self.parser.parse(test_str)
        self.assertEqual(ast.child, None)
        self.node_eq(ast, 7, 0, 7)

    def test_parse_multiple(self):
        test_str = "deparser " \
                   "load HEADER, PHV, 3 " \
                   "load HEADER +1, PHV+3, 4 " \
                   "load HEADER + 6, PHV + 7, 2 "
        ast = self.parser.parse(test_str)
        self.assertNotEqual(ast, None)
        self.assertNotEqual(ast.child, None)
        self.assertNotEqual(ast.child.child, None)
        self.node_eq(ast, 0, 0, 3)
        self.node_eq(ast.child, 1, 3, 4)
        self.node_eq(ast.child.child, 6, 7, 2)

    def test_illegal(self):
        test_str = "deparser " \
                   "load"
        self.assertRaises(Exception, self.parser.parse, test_str)
        test_str = "deparser " \
                   "load HEADER - 1, PHV - 1, -153"
        self.assertRaises(Exception, self.parser.parse, test_str)
        test_str = "deparser " \
                   "load PHV, HEADER, 11"
        self.assertRaises(Exception, self.parser.parse, test_str)
