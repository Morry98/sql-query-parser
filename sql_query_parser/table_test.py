from unittest import TestCase

from sql_query_parser.exceptions.object_blocked_exception import ObjectBlockedException
from sql_query_parser.table import Table


class TableTest(TestCase):
    """
    Test class for Table
    """

    def setUp(self):
        """
        Create two table with alias a;
        Create a table with alias b;
        Create a blocked table with alias a;
        """
        self.table_alias_a_1 = Table(alias="a")
        self.table_alias_a_2 = Table(alias="a")
        self.table_alias_b_1 = Table(alias="b")
        self.blocked_table = Table(alias="a")
        self.blocked_table.blocked = True

    def test_eq_not_Table_type(self):
        """
        Test __eq__ function if the object is not a Table
        """
        self.assertFalse(self.table_alias_a_1 == 1)

    def test_eq_alais(self):
        """
        Test __eq__ function with same alias
        """
        self.assertEqual(self.table_alias_a_1, self.table_alias_a_2)

    def test_not_eq_alias(self):
        self.assertNotEqual(self.table_alias_a_1, self.table_alias_b_1)

    def test_eq_name(self):
        """
        Test __eq__ function with same name
        """
        self.table_alias_a_1.name = "name1"
        self.table_alias_a_2.name = "name1"
        self.assertEqual(self.table_alias_a_1, self.table_alias_a_2)

    def test_not_eq_name(self):
        """
        Test __eq__ function with different name
        """
        self.table_alias_a_1.name = "name1"
        self.table_alias_a_2.name = "name2"
        self.assertNotEqual(self.table_alias_a_1, self.table_alias_a_2)

    def test_eq_columns(self):
        """
        Test __eq__ function with same columns
        """
        self.table_alias_a_1.columns = {"col1": "alias1"}
        self.table_alias_a_2.columns = {"col1": "alias1"}
        self.assertEqual(self.table_alias_a_1, self.table_alias_a_2)

    def test_not_eq_columns(self):
        """
        Test __eq__ function with different columns
        """
        self.table_alias_a_1.columns = {"col1": "alias1"}
        self.table_alias_a_2.columns = {"col2": "alias2"}
        self.assertNotEqual(self.table_alias_a_1, self.table_alias_a_2)

    def test_eq_functions(self):
        """
        Test __eq__ function with same functions
        """
        self.table_alias_a_1.functions = {"fun1": "alias1"}
        self.table_alias_a_2.functions = {"fun1": "alias1"}
        self.assertEqual(self.table_alias_a_1, self.table_alias_a_2)

    def test_not_eq_functions(self):
        """
        Test __eq__ function with different functions
        """
        self.table_alias_a_1.functions = {"fun1": "alias1"}
        self.table_alias_a_2.functions = {"fun2": "alias2"}
        self.assertNotEqual(self.table_alias_a_1, self.table_alias_a_2)

    def test_eq_blocked(self):
        """
        Test __eq__ function with same blocked
        """
        self.table_alias_a_1.blocked = True
        self.table_alias_a_2.blocked = True
        self.assertEqual(self.table_alias_a_1, self.table_alias_a_2)

    def test_not_eq_blocked(self):
        """
        Test __eq__ function with different blocked
        """
        self.table_alias_a_1.blocked = True
        self.table_alias_a_2.blocked = False
        self.assertNotEqual(self.table_alias_a_1, self.table_alias_a_2)

    def test_setter_alais(self):
        """
        Test setter for alias
        """
        self.table_alias_a_1.alias = "alias1"
        self.assertEqual(self.table_alias_a_1.alias, "alias1")

    def test_getter_alais(self):
        """
        Test getter for alias
        """
        self.assertEqual(self.table_alias_a_1.alias, "a")

    def test_getter_name(self):
        """
        Test getter for name
        """
        self.assertEqual(self.table_alias_a_1.name, "a")
        name = "name1"
        self.table_alias_a_1.name = name
        self.assertEqual(self.table_alias_a_1.name, name)

    def test_getter_columns(self):
        """
        Test getter for columns
        """
        self.assertEqual(self.table_alias_a_1.columns, {})
        columns = {"col1": "alias1"}
        self.table_alias_a_1.columns = columns
        self.assertEqual(self.table_alias_a_1.columns, columns)

    def test_getter_functions(self):
        """
        Test getter for functions
        """
        self.assertEqual(self.table_alias_a_1.functions, {})
        functions = {"fun1": "alias1"}
        self.table_alias_a_1.functions = functions
        self.assertEqual(self.table_alias_a_1.functions, functions)

    def test_getter_blocked(self):
        """
        Test getter for blocked
        """
        blocked = True
        self.table_alias_a_1.blocked = blocked
        self.assertEqual(self.table_alias_a_1.blocked, blocked)

    def test_blocked_setter_alais(self):
        """
        Test alias setter for blocked object
        """
        with self.assertRaises(ObjectBlockedException):
            self.blocked_table.alias = "alias1"

    def test_blocked_setter_name(self):
        """
        Test name setter for blocked object
        """
        with self.assertRaises(ObjectBlockedException):
            self.blocked_table.name = "name1"

    def test_blocked_setter_columns(self):
        """
        Test columns setter for blocked object
        """
        with self.assertRaises(ObjectBlockedException):
            self.blocked_table.columns = {"col1": "alias1"}

    def test_blocked_setter_functions(self):
        """
        Test functions setter for blocked object
        """
        with self.assertRaises(ObjectBlockedException):
            self.blocked_table.functions = {"fun1": "alias1"}

    def test_blocked_setter_blocked(self):
        """
        Test blocked setter for blocked object
        """
        with self.assertRaises(ObjectBlockedException):
            self.blocked_table.blocked = True

    def test_block_table(self):
        """
        Test block table function
        """
        self.table_alias_a_1.block_table()
        self.assertEqual(self.table_alias_a_1.blocked, True)
        with self.assertRaises(ObjectBlockedException):
            self.blocked_table.name = "name1"

    def test_add_column(self):
        """
        Test add column function
        """
        self.table_alias_a_1.add_column(column="col1")
        self.assertEqual(self.table_alias_a_1.columns, {"col1": "col1"})

    def test_blocked_add_column(self):
        """
        Test add column function for blocked object
        """
        with self.assertRaises(ObjectBlockedException):
            self.blocked_table.add_column(column="col1")

    def test_add_column_and_alias(self):
        """
        Test add column and alias function
        """
        self.table_alias_a_1.add_column(column="col1", alias="alias1")
        self.assertEqual(self.table_alias_a_1.columns, {"col1": "alias1"})

    def test_add_function(self):
        """
        Test add function function
        """
        self.table_alias_a_1.add_function(function="fun1")
        self.assertEqual(self.table_alias_a_1.functions, {"fun1": "fun1"})

    def test_add_function_and_alias(self):
        """
        Test add function and alias function
        """
        self.table_alias_a_1.add_function(function="fun1", alias="alias1")
        self.assertEqual(self.table_alias_a_1.functions, {"fun1": "alias1"})

    def test_blocked_add_function(self):
        """
        Test add function function for blocked object
        """
        with self.assertRaises(ObjectBlockedException):
            self.blocked_table.add_function(function="fun1")

    def test_hash(self):
        """
        Test hash function
        """
        self.assertEqual(hash(self.table_alias_a_1), hash(self.table_alias_a_2))
        self.table_alias_a_2.name = "name2"
        self.assertNotEqual(hash(self.table_alias_a_1), hash(self.table_alias_a_2))

    def test_copy(self):
        """
        Test copy function
        """

        self.table_alias_a_1.name = "name1"
        self.table_alias_a_1.columns = {"col1": "alias1"}
        self.table_alias_a_1.functions = {"fun1": "alias1"}

        table_alias_a_1_copy = self.table_alias_a_1.copy()

        self.assertEqual(self.table_alias_a_1, table_alias_a_1_copy)

        table_alias_a_1_copy.alias = "alias2"
        self.assertNotEqual(self.table_alias_a_1, table_alias_a_1_copy)
        table_alias_a_1_copy.name = "name2"
        self.assertNotEqual(self.table_alias_a_1, table_alias_a_1_copy)
        table_alias_a_1_copy.columns = {"col2": "alias1"}
        self.assertNotEqual(self.table_alias_a_1, table_alias_a_1_copy)
        table_alias_a_1_copy.functions = {"fun2": "alias1"}
        self.assertNotEqual(self.table_alias_a_1, table_alias_a_1_copy)
