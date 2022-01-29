from typing import Tuple, Optional
import re

from lib.sql_parser.table import Table
from lib.sql_parser2.configurations import Configurations


def compute(word: str, config: Configurations) -> Tuple[bool, Configurations]:
    # TODO Implement and logic
    return False, config


# TODO Refactor this copied function for the new usage
def add_to_query(config: Configurations, alias: Optional[str] = None):
    parsing_column = config.pop_last_parsing_value()
    column = parsing_column[0]
    if alias is None:
        config.add_parsing_value(parsing_value=parsing_column)
        alias = parsing_column[1]
    elif parsing_column[1] is not None:
        raise Exception(f"Double alias for {column} column: {parsing_column[1]} and {alias}")
    split_parsing_column = column.split(".")
    table_str: str = "" if len(split_parsing_column) <= 1 else split_parsing_column[0]
    table = config.query.get_table_by_name_or_alias(table_str)
    if table is None:
        table = Table(alias=table_str)
        config.query.add_table(table)
    alias = alias.replace(",", "") if alias is not None else None
    table.add_function(function="count(" + column + ")", alias=alias)
