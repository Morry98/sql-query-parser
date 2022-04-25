from unittest import TestCase

from sql_query_parser.condition import Condition
from sql_query_parser.exceptions.object_blocked_exception import ObjectBlockedException
from sql_query_parser.query import Query
from sql_query_parser.table import Table


class QueryTest(TestCase):
    """
    Test class for Query
    """

    def setUp(self):
        """
        Create two query with text a;
        Create a query with text b;
        Create a blocked query with text a;
        """
        self.query_text_a_1 = Query(text="a")
        self.query_text_a_2 = Query(text="a")
        self.query_text_b_1 = Query(text="b")
        self.blocked_query = Query(text="a")
        self.blocked_query.blocked = True

    def test_eq_not_Query_type(self):
        """
        Test __eq__ function if the object is not a Query
        """
        self.assertFalse(self.query_text_a_1 == 1)

    def test_eq_text(self):
        """
        Test __eq__ function with same text
        """
        self.assertEqual(self.query_text_a_1, self.query_text_a_2)

    def test_not_eq_text(self):
        self.assertNotEqual(self.query_text_a_1, self.query_text_b_1)

    def test_eq_tables(self):
        """
        Test __eq__ function with same tables
        """
        self.query_text_a_1.tables = [Table(alias="alias1")]
        self.query_text_a_2.tables = [Table(alias="alias1")]
        self.assertEqual(self.query_text_a_1, self.query_text_a_2)

    def test_not_eq_tables(self):
        """
        Test __eq__ function with different tables
        """
        self.query_text_a_1.tables = [Table(alias="alias1")]
        self.query_text_a_2.tables = [Table(alias="alias2")]
        self.assertNotEqual(self.query_text_a_1, self.query_text_a_2)

    def test_eq_condition(self):
        """
        Test __eq__ function with same condition
        """
        self.query_text_a_1.condition = Condition(condition_type="and")
        self.query_text_a_2.condition = Condition(condition_type="and")
        self.assertEqual(self.query_text_a_1, self.query_text_a_2)

    def test_not_eq_condition(self):
        """
        Test __eq__ function with different condition
        """
        self.query_text_a_1.condition = Condition(condition_type="and")
        self.query_text_a_2.condition = Condition(condition_type="or")
        self.assertNotEqual(self.query_text_a_1, self.query_text_a_2)

    def test_eq_blocked(self):
        """
        Test __eq__ function with same blocked
        """
        self.query_text_a_1.blocked = True
        self.query_text_a_2.blocked = True
        self.assertEqual(self.query_text_a_1, self.query_text_a_2)

    def test_not_eq_blocked(self):
        """
        Test __eq__ function with different blocked
        """
        self.query_text_a_1.blocked = True
        self.query_text_a_2.blocked = False
        self.assertNotEqual(self.query_text_a_1, self.query_text_a_2)

    def test_getter_text(self):
        """
        Test getter for text
        """
        self.assertEqual(self.query_text_a_1.text, "a")

    def test_setter_and_getter_tables(self):
        """
        Test setter for tables
        """
        self.assertEqual(self.query_text_a_1.tables, [])
        tables = [Table(alias="alias1")]
        self.query_text_a_1.tables = tables
        self.assertEqual(self.query_text_a_1.tables, tables)

    def test_getter_blocked(self):
        """
        Test getter for blocked
        """
        blocked = True
        self.query_text_a_1.blocked = blocked
        self.assertEqual(self.query_text_a_1.blocked, blocked)

    def test_blocked_setter_tables(self):
        """
        Test tables setter for blocked object
        """
        with self.assertRaises(ObjectBlockedException):
            self.blocked_query.tables = []

    def test_blocked_setter_blocked(self):
        """
        Test blocked setter for blocked object
        """
        with self.assertRaises(ObjectBlockedException):
            self.blocked_query.blocked = True

    def test_block_query(self):
        """
        Test block query function
        """
        self.query_text_a_1.block_query()
        self.assertEqual(self.query_text_a_1.blocked, True)
        with self.assertRaises(ObjectBlockedException):
            self.query_text_a_1.tables = []

    def test_get_table_by_name_or_alias(self):
        """
        Test get_table_by_name_or_alias function
        """
        tables = [Table(alias="alias1"), Table(alias="alias2")]
        tables[1].name = "name1"
        self.query_text_a_1.tables = tables
        self.assertEqual(self.query_text_a_1.get_table_by_name_or_alias("alias1"), self.query_text_a_1.tables[0])
        self.assertEqual(self.query_text_a_1.get_table_by_name_or_alias("alias2"), self.query_text_a_1.tables[1])
        self.assertEqual(self.query_text_a_1.get_table_by_name_or_alias("name1"), self.query_text_a_1.tables[1])
        self.assertEqual(self.query_text_a_1.get_table_by_name_or_alias("alias3"), None)

    def test_add_table(self):
        """
        Test add table function
        """
        tables = [Table(alias="alias1"), Table(alias="alias2")]
        self.query_text_a_1.add_table(table=tables[0])
        self.assertEqual(self.query_text_a_1.tables, tables[:1])
        self.query_text_a_1.add_table(table=tables[1])
        self.assertEqual(self.query_text_a_1.tables, tables)

    def test_blocked_add_table(self):
        """
        Test add table function for blocked object
        """
        with self.assertRaises(ObjectBlockedException):
            self.blocked_query.add_table(table=Table(alias="alias1"))

    def test_none_condition_getter(self):
        """
        Test getter for condition
        """
        self.assertEqual(self.query_text_a_1.condition, None)

    def test_condition_setter(self):
        """
        Test condition setter
        """
        condition = Condition(condition_type="and")
        self.query_text_a_1.condition = condition
        self.assertEqual(self.query_text_a_1.condition, condition)

    def test_blocked_condition_setter(self):
        """
        Test condition setter for blocked object
        """
        with self.assertRaises(ObjectBlockedException):
            self.blocked_query.condition = Condition(condition_type="and")

    def test_add_condition(self):
        """
        Test add condition function
        """
        conditions = [Condition(condition_type="and"), Condition(condition_type="or")]
        with self.assertRaises(ValueError):
            self.query_text_a_1.add_condition(condition=conditions[0])
        self.query_text_a_1.add_condition(condition=conditions[0], condition_type="and")
        query_condition = Condition(condition_type="and")
        query_condition.add_condition(condition=conditions[0])
        self.assertEqual(self.query_text_a_1.condition, query_condition)
        with self.assertRaises(ValueError):
            self.query_text_a_1.add_condition(condition=conditions[1], condition_type="or")
        self.query_text_a_1.add_condition(condition=conditions[1])
        query_condition.add_condition(condition=conditions[1])
        self.assertEqual(self.query_text_a_1.condition, query_condition)

    def test_blocked_add_condition(self):
        """
        Test add condition function for blocked object
        """
        with self.assertRaises(ObjectBlockedException):
            self.blocked_query.add_condition(condition=Condition(condition_type="or"))

    def test_copy(self):
        """
        Test copy function
        """
        self.query_text_a_1.tables = [Table(alias="alias1")]
        self.query_text_a_1.condition = Condition(condition_type="and")
        query_copy = self.query_text_a_1.copy()
        self.assertEqual(query_copy, self.query_text_a_1)
        query_copy.tables = [Table(alias="alias1"), Table(alias="alias2")]
        query_copy.condition = Condition(condition_type="or")
        self.assertNotEqual(query_copy, self.query_text_a_1)

    def test_hash(self):
        """
        Test copy function
        """
        self.assertEqual(hash(self.query_text_a_2), hash(self.query_text_a_1))
        self.query_text_a_2.tables = [Table(alias="alias1"), Table(alias="alias2")]
        self.assertNotEqual(hash(self.query_text_a_2), hash(self.query_text_a_1))
