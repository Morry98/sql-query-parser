from unittest import TestCase

from lib.exceptions.object_blocked_exception import ObjectBlockedException
from lib.sql_parser.table import Table


class TableTest(TestCase):

    # Create setup for all tests
    def setUp(self):
        self.table_alias_a_1 = Table(alias="a")
        self.table_alias_a_2 = Table(alias="a")
        self.table_alias_b_1 = Table(alias="b")
        self.blocked_table = Table(alias="a")
        self.blocked_table.blocked = True

    def test_eq_not_Table_type(self):
        with self.assertRaises(TypeError):
            _ = self.table_alias_a_1 == 1

    def test_eq_alais(self):
        self.assertEqual(self.table_alias_a_1, self.table_alias_a_2)

    def test_not_eq_alias(self):
        self.assertNotEqual(self.table_alias_a_1, self.table_alias_b_1)

    def test_eq_name(self):
        self.table_alias_a_1.name = "name1"
        self.table_alias_a_2.name = "name1"
        self.assertEqual(self.table_alias_a_1, self.table_alias_a_2)

    def test_not_eq_name(self):
        self.table_alias_a_1.name = "name1"
        self.table_alias_a_2.name = "name2"
        self.assertNotEqual(self.table_alias_a_1, self.table_alias_a_2)

    def test_eq_columns(self):
        self.table_alias_a_1.columns = {"col1": "alias1"}
        self.table_alias_a_2.columns = {"col1": "alias1"}
        self.assertEqual(self.table_alias_a_1, self.table_alias_a_2)

    def test_not_eq_columns(self):
        self.table_alias_a_1.columns = {"col1": "alias1"}
        self.table_alias_a_2.columns = {"col2": "alias2"}
        self.assertNotEqual(self.table_alias_a_1, self.table_alias_a_2)

    def test_eq_functions(self):
        self.table_alias_a_1.functions = {"fun1": "alias1"}
        self.table_alias_a_2.functions = {"fun1": "alias1"}
        self.assertEqual(self.table_alias_a_1, self.table_alias_a_2)

    def test_not_eq_functions(self):
        self.table_alias_a_1.functions = {"fun1": "alias1"}
        self.table_alias_a_2.functions = {"fun2": "alias2"}
        self.assertNotEqual(self.table_alias_a_1, self.table_alias_a_2)

    def test_eq_blocked(self):
        self.table_alias_a_1.blocked = True
        self.table_alias_a_2.blocked = True
        self.assertEqual(self.table_alias_a_1, self.table_alias_a_2)

    def test_not_eq_blocked(self):
        self.table_alias_a_1.blocked = True
        self.table_alias_a_2.blocked = False
        self.assertNotEqual(self.table_alias_a_1, self.table_alias_a_2)

    def test_setter_alais(self):
        self.table_alias_a_1.alias = "alias1"
        self.assertEqual(self.table_alias_a_1.alias, "alias1")

    def test_getter_alais(self):
        self.assertEqual(self.table_alias_a_1.alias, "a")

    def test_getter_name(self):
        name = "name1"
        self.table_alias_a_1.name = name
        self.assertEqual(self.table_alias_a_1.name, name)

    def test_getter_columns(self):
        columns = {"col1": "alias1"}
        self.table_alias_a_1.columns = columns
        self.assertEqual(self.table_alias_a_1.columns, columns)

    def test_getter_functions(self):
        functions = {"fun1": "alias1"}
        self.table_alias_a_1.functions = functions
        self.assertEqual(self.table_alias_a_1.functions, functions)

    def test_getter_blocked(self):
        blocked = True
        self.table_alias_a_1.blocked = blocked
        self.assertEqual(self.table_alias_a_1.blocked, blocked)

    def test_blocked_setter_alais(self):
        with self.assertRaises(ObjectBlockedException):
            self.blocked_table.alias = "alias1"

    def test_blocked_setter_name(self):
        with self.assertRaises(ObjectBlockedException):
            self.blocked_table.name = "name1"

    def test_blocked_setter_columns(self):
        with self.assertRaises(ObjectBlockedException):
            self.blocked_table.columns = {"col1": "alias1"}

    def test_blocked_setter_functions(self):
        with self.assertRaises(ObjectBlockedException):
            self.blocked_table.functions = {"fun1": "alias1"}

    def test_blocked_setter_blocked(self):
        with self.assertRaises(ObjectBlockedException):
            self.blocked_table.blocked = True

    def test_block_table(self):
        self.table_alias_a_1.block_table()
        self.assertEqual(self.table_alias_a_1.blocked, True)
        with self.assertRaises(ObjectBlockedException):
            self.blocked_table.name = "name1"

    def test_add_column(self):
        self.table_alias_a_1.add_column(column="col1")
        self.assertEqual(self.table_alias_a_1.columns, {"col1": "col1"})

    def test_blocked_add_column(self):
        with self.assertRaises(ObjectBlockedException):
            self.blocked_table.add_column(column="col1")

    def test_add_column_and_alias(self):
        self.table_alias_a_1.add_column(column="col1", alias="alias1")
        self.assertEqual(self.table_alias_a_1.columns, {"col1": "alias1"})

    def test_add_function(self):
        self.table_alias_a_1.add_function(function="fun1")
        self.assertEqual(self.table_alias_a_1.functions, {"fun1": "fun1"})

    def test_add_function_and_alias(self):
        self.table_alias_a_1.add_function(function="fun1", alias="alias1")
        self.assertEqual(self.table_alias_a_1.functions, {"fun1": "alias1"})

    def test_blocked_add_function(self):
        with self.assertRaises(ObjectBlockedException):
            self.blocked_table.add_function(function="fun1")
