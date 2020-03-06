from unittest import TestCase
from code.deparser import DeparserParser
from code.ast import *


class DeparserParserTestCase(TestCase):
    def setUp(self):
        self.parser = DeparserParser()
        self.ast = None

    def ast_eq(self, v1, v2, v3):
        self.assertIsInstance(self.ast, Node)
        self.assertEqual(self.ast.child, None)
        self.assertIsInstance(self.ast.leaf, TernaryOp)
        self.assertEqual(self.ast.leaf, TernaryOp('load', Hdr(v1), Phv(v2), v3))

    def test_parse_empty(self):
        test_str = "deparser"
        self.ast = self.parser.parse(test_str)
        self.assertEqual(self.ast, None)

    def test_parse_one_empty(self):
        test_str = "deparser " \
                   "load HEADER, PHV, 0"
        self.ast = self.parser.parse(test_str)
        self.ast_eq(0, 0, 0)

    def test_parse_one_shifted(self):
        test_str = "deparser " \
                   "load HEADER + 2, PHV + 11, 3"
        self.ast = self.parser.parse(test_str)
        self.ast_eq(2, 11, 3)

        test_str = "deparser " \
                   "load HEADER + 0, PHV + 0, 5"
        self.ast = self.parser.parse(test_str)
        self.ast_eq(0, 0, 5)

        test_str = "deparser " \
                   "load HEADER, PHV + 1, 5"
        self.ast = self.parser.parse(test_str)
        self.ast_eq(0, 1, 5)

        test_str = "deparser " \
                   "load HEADER + 7, PHV, 7"
        self.ast = self.parser.parse(test_str)
        self.ast_eq(7, 0, 7)
