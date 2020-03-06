from unittest import TestCase
from code.deparser import DeparserParser
from code.ast import *


class DeparserParserTestCase(TestCase):
    def setUp(self):
        self.parser = DeparserParser()

    def test_parse_empty(self):
        test_str = "deparser"
        ast = self.parser.parse(test_str)
        self.assertEqual(ast, None)

    def test_parse_one_empty(self):
        test_str = "deparser " \
                   "load HEADER, PHV, 0"
        ast = self.parser.parse(test_str)
        self.assertIsInstance(ast, Node)
        self.assertEqual(ast.child, None)
        self.assertIsInstance(ast.leaf, TernaryOp)
        self.assertEqual(ast.leaf, TernaryOp('load', Hdr(0), Phv(0), 0))
