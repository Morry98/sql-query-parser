from typing import Tuple, Optional

from lib.sql_parser.configurations import Configurations
from lib.sql_parser.table import Table


def compute(
        word: str,
        config: Configurations
) -> Tuple[bool, Configurations]:
    if (len(config.keywords) > 0 and config.keywords[-1] == "select") or (
            len(config.keywords) > 1 and config.keywords[-2] == "select" and config.keywords[-1] == "as"):
        if "as" in word:
            config.add_keyword("as")
        else:
            if config.keywords[-1] == "as":
                __add_column_to_query(config=config, alias=word)
                config.pop_last_keyword()
            elif "," in word:
                word = word[:-1]
                config.add_parsing_value(parsing_value=(word, None))
                __add_column_to_query(config=config)
                config.pop_last_parsing_value()
            else:
                config.add_parsing_value(parsing_value=(word, None))
                __add_column_to_query(config=config)
        return True, config
    return False, config


def __add_column_to_query(
        config: Configurations,
        alias: Optional[str] = None
) -> None:
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
    table.add_column(column=column, alias=alias)
