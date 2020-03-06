from unittest import TestCase
from code.deparser import DeparserParser


class DeparserParserTestCase(TestCase):
    def setUp(self):
        self.parser = DeparserParser()

    def test_parse_empty(self):
        test_str = "deparser"
        self.assertEqual(self.parser.parse(test_str), None)
