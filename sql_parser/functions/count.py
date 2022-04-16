from typing import Tuple, Optional
import re

from sql_parser.table import Table
from sql_parser.configurations import Configurations

REGEX_PATTERN = re.compile(r"count\((.*)\)")


def compute(
        word: str,
        config: Configurations
) -> Tuple[bool, Configurations]:
    if len(config.keywords) > 0 and config.keywords[-1] == "function_count":
        if "as" in word:
            config.add_keyword("as")
            return True, config
        if "from" in word:  # TODO Can be found a better solution
            config.pop_last_keyword()
            config.pop_last_parsing_value()
            return False, config
    elif len(config.keywords) > 1 and config.keywords[-2] == "function_count":
        if config.keywords[-1] == "as":
            if len(config.parsing_value) != 1:
                raise Exception(f"Function count support only one column, {len(config.parsing_value)} found")
            add_to_query(alias=word, config=config)
            config.pop_last_keyword()
            config.pop_last_keyword()
            return True, config
        raise Exception(f'{config.keywords[-1]} keyword not supported in count function')
    else:
        if "count" in word:
            matches = REGEX_PATTERN.findall(word)
            if len(matches) == 1:
                config.add_keyword("function_count")
                config.add_parsing_value(parsing_value=(matches[0], None))
                add_to_query(config=config)
                if "," in word:
                    config.pop_last_keyword()
                    config.pop_last_parsing_value()
            return True, config
    return False, config


def add_to_query(
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
    table.add_function(function="count(" + column + ")", alias=alias)
