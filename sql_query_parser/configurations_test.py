from unittest import TestCase
from sql_query_parser.configurations import Configurations
from sql_query_parser.query import Query


class ConfigurationsTest(TestCase):

    def setUp(self):
        """
        Setup for each test
        """
        self.configurations_query_a1 = Configurations(query=Query("a"))
        self.configurations_query_a2 = Configurations(query=Query("a"))
        self.configurations_query_b1 = Configurations(query=Query("b"))

    def test_eq_not_configurations_type(self):
        self.assertFalse(self.configurations_query_a1 == Query(""))

    def test_eq_query(self):
        self.assertEqual(self.configurations_query_a1, self.configurations_query_a1)

    def test_not_eq_query(self):
        self.assertNotEqual(self.configurations_query_a1, self.configurations_query_b1)

    def test_eq_keyword(self):
        self.configurations_query_a1.keywords = ["a"]
        self.configurations_query_a2.keywords = ["a"]
        self.assertEqual(self.configurations_query_a1, self.configurations_query_a2)

    def test_not_eq_keyword(self):
        self.configurations_query_a1.keywords = ["a"]
        self.configurations_query_a2.keywords = ["b"]
        self.assertNotEqual(self.configurations_query_a1, self.configurations_query_a2)

    def test_eq_parsing_value(self):
        self.configurations_query_a1.parsing_value = [("a", "b")]
        self.configurations_query_a2.parsing_value = [("a", "b")]
        self.assertEqual(self.configurations_query_a1, self.configurations_query_a2)

    def test_not_eq_parsing_value(self):
        self.configurations_query_a1.parsing_value = [("a", "b")]
        self.configurations_query_a2.parsing_value = [("a", "c")]
        self.assertNotEqual(self.configurations_query_a1, self.configurations_query_a2)

    def test_eq_conditions_type(self):
        self.configurations_query_a1.conditions_type = ["a"]
        self.configurations_query_a2.conditions_type = ["a"]
        self.assertEqual(self.configurations_query_a1, self.configurations_query_a2)

    def test_not_eq_conditions_type(self):
        self.configurations_query_a1.conditions_type = ["a"]
        self.configurations_query_a2.conditions_type = ["b"]
        self.assertNotEqual(self.configurations_query_a1, self.configurations_query_a2)

    def test_eq_conditions_type_list(self):
        self.configurations_query_a1.conditions_type = [["a"]]
        self.configurations_query_a2.conditions_type = [["a"]]
        self.assertEqual(self.configurations_query_a1, self.configurations_query_a2)

    def test_not_eq_conditions_type_list(self):
        self.configurations_query_a1.conditions_type = [["a"]]
        self.configurations_query_a2.conditions_type = [["b"]]
        self.assertNotEqual(self.configurations_query_a1, self.configurations_query_a2)

    def test_eq_conditions(self):
        self.configurations_query_a1.conditions = ["a"]
        self.configurations_query_a2.conditions = ["a"]
        self.assertEqual(self.configurations_query_a1, self.configurations_query_a2)

    def test_not_eq_conditions(self):
        self.configurations_query_a1.conditions = ["a"]
        self.configurations_query_a2.conditions = ["b"]
        self.assertNotEqual(self.configurations_query_a1, self.configurations_query_a2)

    def test_eq_conditions_list(self):
        self.configurations_query_a1.conditions = [["a"]]
        self.configurations_query_a2.conditions = [["a"]]
        self.assertEqual(self.configurations_query_a1, self.configurations_query_a2)

    def test_not_eq_conditions_list(self):
        self.configurations_query_a1.conditions = [["a"]]
        self.configurations_query_a2.conditions = [["b"]]
        self.assertNotEqual(self.configurations_query_a1, self.configurations_query_a2)

    def test_eq_condition_position(self):
        self.configurations_query_a1.condition_position = 0
        self.configurations_query_a2.condition_position = 0
        self.assertEqual(self.configurations_query_a1, self.configurations_query_a2)

    def test_not_eq_condition_position(self):
        self.configurations_query_a1.condition_position = 1
        self.configurations_query_a2.condition_position = 0
        self.assertNotEqual(self.configurations_query_a1, self.configurations_query_a2)

    def test_eq_is_new_condition(self):
        self.configurations_query_a1.is_new_condition = True
        self.configurations_query_a2.is_new_condition = True
        self.assertEqual(self.configurations_query_a1, self.configurations_query_a2)

    def test_not_eq_is_new_condition(self):
        self.configurations_query_a1.is_new_condition = False
        self.configurations_query_a2.is_new_condition = True
        self.assertNotEqual(self.configurations_query_a1, self.configurations_query_a2)

    def test_is_new_condition_getter_setter(self):
        self.configurations_query_a1.is_new_condition = True
        self.assertTrue(self.configurations_query_a1.is_new_condition)

    def test_hash(self):
        self.assertEqual(hash(self.configurations_query_a1), hash(self.configurations_query_a2))

    def test_copy(self):
        self.configurations_query_a1.keywords = ["a"]
        self.configurations_query_a1.parsing_values = [("a", "a")]
        self.configurations_query_a1.conditions_type = ["a"]
        self.configurations_query_a1.conditions = ["a"]
        self.configurations_query_a1.condition_position = 0
        self.configurations_query_a1.is_new_condition = True
        configurations_copy = self.configurations_query_a1.copy()
        self.assertEqual(self.configurations_query_a1, configurations_copy)
        configurations_copy.keywords = ["b"]
        self.assertNotEqual(self.configurations_query_a1, configurations_copy)
        configurations_copy.parsing_values = [("b", "b")]
        self.assertNotEqual(self.configurations_query_a1, configurations_copy)
        configurations_copy.conditions_type = ["b"]
        self.assertNotEqual(self.configurations_query_a1, configurations_copy)
        configurations_copy.conditions = ["b"]
        self.assertNotEqual(self.configurations_query_a1, configurations_copy)
        configurations_copy.condition_position = 1
        self.assertNotEqual(self.configurations_query_a1, configurations_copy)
        configurations_copy.is_new_condition = False
        self.assertNotEqual(self.configurations_query_a1, configurations_copy)

    def test_keywords_getter_and_setter(self):
        self.configurations_query_a1.keywords = ["a"]
        self.assertEqual(self.configurations_query_a1.keywords, ["a"])

    def test_parsing_values_getter_and_setter(self):
        self.configurations_query_a1.parsing_values = [("a", "a")]
        self.assertEqual(self.configurations_query_a1.parsing_values, [("a", "a")])

    def test_conditions_type_getter_and_setter(self):
        self.configurations_query_a1.conditions_type = ["a"]
        self.assertEqual(self.configurations_query_a1.conditions_type, ["a"])

    def test_conditions_getter_and_setter(self):
        self.configurations_query_a1.conditions = ["a"]
        self.assertEqual(self.configurations_query_a1.conditions, ["a"])

    def test_condition_position_getter_and_setter(self):
        self.configurations_query_a1.condition_position = 0
        self.assertEqual(self.configurations_query_a1.condition_position, 0)

    def test_is_new_condition_getter_and_setter(self):
        self.configurations_query_a1.is_new_condition = True
        self.assertTrue(self.configurations_query_a1.is_new_condition)

    def test_query_getter(self):
        self.assertEqual(self.configurations_query_a1.query, Query("a"))

    def test_add_keyword(self):
        self.configurations_query_a1.add_keyword("a")
        self.assertEqual(self.configurations_query_a1.keywords, ["a"])

    def test_pop_last_keyword(self):
        self.configurations_query_a1.keywords = ["a"]
        last_keyword = self.configurations_query_a1.pop_last_keyword()
        self.assertEqual(last_keyword, "a")
        self.assertEqual(self.configurations_query_a1.keywords, [])
        with self.assertRaises(IndexError):
            self.configurations_query_a1.pop_last_keyword()
