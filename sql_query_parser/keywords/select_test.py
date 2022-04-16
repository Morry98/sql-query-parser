from copy import copy
from unittest import TestCase
from sql_query_parser.keywords import select

from sql_query_parser.configurations import Configurations
from sql_query_parser.query import Query


class SelectTest(TestCase):

    def test_no_select_word(self):
        configuration = Configurations(query=Query(text=""))
        result = select.compute(word="", config=copy(configuration))
        self.assertEqual(2, len(result))
        self.assertEqual(False, result[0])
        self.assertEqual(configuration, result[1])

    def test_select_word(self):
        configuration = Configurations(query=Query(text=""))
        result = select.compute(word="select", config=configuration)
        self.assertEqual(2, len(result))
        self.assertEqual(True, result[0])
        self.assertEqual(configuration, result[1])

    def test_select_is_not_first_keyword(self):
        configuration = Configurations(query=Query(text=""))
        configuration.add_keyword(keyword="from")
        with self.assertRaises(Exception):
            _ = select.compute(word="select", config=copy(configuration))
