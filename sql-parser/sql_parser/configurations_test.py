from unittest import TestCase
from lib.sql_parser.configurations import Configurations
from lib.sql_parser.query import Query


class ConfigurationsTest(TestCase):

    def test_eq_not_configurations_type(self):
        configurations1 = Configurations(query=Query(""))
        configurations2 = Query("")
        with self.assertRaises(TypeError):
            _ = configurations1 == configurations2

    def test_eq_query(self):
        configurations1 = Configurations(query=Query(""))
        configurations2 = Configurations(query=Query(""))
        self.assertEqual(configurations1, configurations2)

    def test_not_eq_query(self):
        configurations1 = Configurations(query=Query(""))
        configurations2 = Configurations(query=Query("a"))
        self.assertNotEqual(configurations1, configurations2)

    def test_eq_keyword(self):
        configurations1 = Configurations(query=Query(""))
        configurations2 = Configurations(query=Query(""))
        configurations1.keywords = ["a"]
        configurations2.keywords = ["a"]
        self.assertEqual(configurations1, configurations2)

    def test_not_eq_keyword(self):
        configurations1 = Configurations(query=Query(""))
        configurations2 = Configurations(query=Query(""))
        configurations1.keywords = ["a"]
        configurations2.keywords = ["b"]
        self.assertNotEqual(configurations1, configurations2)

    def test_eq_parsing_value(self):
        configurations1 = Configurations(query=Query(""))
        configurations2 = Configurations(query=Query(""))
        configurations1.parsing_value = [("a", "b")]
        configurations2.parsing_value = [("a", "b")]
        self.assertEqual(configurations1, configurations2)

    def test_not_eq_parsing_value(self):
        configurations1 = Configurations(query=Query(""))
        configurations2 = Configurations(query=Query(""))
        configurations1.parsing_value = [("a", "b")]
        configurations2.parsing_value = [("a", "c")]
        self.assertNotEqual(configurations1, configurations2)

    def test_eq_conditions_type(self):
        configurations1 = Configurations(query=Query(""))
        configurations2 = Configurations(query=Query(""))
        configurations1.conditions_type = ["a"]
        configurations2.conditions_type = ["a"]
        self.assertEqual(configurations1, configurations2)

    def test_not_eq_conditions_type(self):
        configurations1 = Configurations(query=Query(""))
        configurations2 = Configurations(query=Query(""))
        configurations1.conditions_type = ["a"]
        configurations2.conditions_type = ["b"]
        self.assertNotEqual(configurations1, configurations2)

    def test_eq_conditions_type_list(self):
        configurations1 = Configurations(query=Query(""))
        configurations2 = Configurations(query=Query(""))
        configurations1.conditions_type = [["a"]]
        configurations2.conditions_type = [["a"]]
        self.assertEqual(configurations1, configurations2)

    def test_not_eq_conditions_type_list(self):
        configurations1 = Configurations(query=Query(""))
        configurations2 = Configurations(query=Query(""))
        configurations1.conditions_type = [["a"]]
        configurations2.conditions_type = [["b"]]
        self.assertNotEqual(configurations1, configurations2)

    def test_eq_conditions(self):
        configurations1 = Configurations(query=Query(""))
        configurations2 = Configurations(query=Query(""))
        configurations1.conditions = ["a"]
        configurations2.conditions = ["a"]
        self.assertEqual(configurations1, configurations2)

    def test_not_eq_conditions(self):
        configurations1 = Configurations(query=Query(""))
        configurations2 = Configurations(query=Query(""))
        configurations1.conditions = ["a"]
        configurations2.conditions = ["b"]
        self.assertNotEqual(configurations1, configurations2)

    def test_eq_conditions_list(self):
        configurations1 = Configurations(query=Query(""))
        configurations2 = Configurations(query=Query(""))
        configurations1.conditions = [["a"]]
        configurations2.conditions = [["a"]]
        self.assertEqual(configurations1, configurations2)

    def test_not_eq_conditions_list(self):
        configurations1 = Configurations(query=Query(""))
        configurations2 = Configurations(query=Query(""))
        configurations1.conditions = [["a"]]
        configurations2.conditions = [["b"]]
        self.assertNotEqual(configurations1, configurations2)

    def test_eq_condition_position(self):
        configurations1 = Configurations(query=Query(""))
        configurations2 = Configurations(query=Query(""))
        configurations1.condition_position = 0
        configurations2.condition_position = 0
        self.assertEqual(configurations1, configurations2)

    def test_not_eq_condition_position(self):
        configurations1 = Configurations(query=Query(""))
        configurations2 = Configurations(query=Query(""))
        configurations1.condition_position = 1
        configurations2.condition_position = 0
        self.assertNotEqual(configurations1, configurations2)

    def test_eq_is_new_condition(self):
        configurations1 = Configurations(query=Query(""))
        configurations2 = Configurations(query=Query(""))
        configurations1.is_new_condition = True
        configurations2.is_new_condition = True
        self.assertEqual(configurations1, configurations2)

    def test_not_eq_is_new_condition(self):
        configurations1 = Configurations(query=Query(""))
        configurations2 = Configurations(query=Query(""))
        configurations1.is_new_condition = False
        configurations2.is_new_condition = True
        self.assertNotEqual(configurations1, configurations2)
