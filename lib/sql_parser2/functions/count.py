from typing import Tuple, Optional
import re

from lib.sql_parser.table import Table
from lib.sql_parser2.configurations import Configurations

REGEX_PATTERN = re.compile("count\((.*)\)")


def compute(word: str, config: Configurations) -> Tuple[bool, Configurations]:
    if type(word) is not str:
        raise Exception('word must be a string!')
    if len(config.keywords) > 0 and config.keywords[-1] == "function_count":
        if "as" in word:
            config.add_keyword("as")
            return True, config
    elif len(config.keywords) > 1 and config.keywords[-2] == "function_count":
        if config.keywords[-1] == "as":
            if len(config.parsing_column) != 1:
                raise Exception(f"Function count support only one column, {len(config.parsing_column)} found")
            add_to_query(word=word, config=config)
            config.pop_last_keyword()
            config.pop_last_keyword()
            return True, config
        raise Exception(f'{config.keywords[-1]} keyword not supported in count function')
    else:
        if "count" in word:
            matches = REGEX_PATTERN.findall(word)
            if len(matches) == 1:
                config.add_keyword("function_count")
                config.add_parsing_column(parsing_column=(matches[0], ""))
                add_to_query(config=config)
            return True, config
    return False, config


def add_to_query(config: Configurations, word: Optional[str] = None):
    parsing_column = config.parsing_column[0][0]
    split_parsing_column = parsing_column.split(".")
    table_str: str = "" if len(split_parsing_column) > 1 else split_parsing_column[0]
    table = config.query.get_table_by_name_or_alias(table_str)
    if table is None:
        table = Table(alias=table_str)
        config.query.add_table(table)
    word = word.replace(",", "") if word is not None else None
    table.add_function(function="count(" + parsing_column + ")", alias=word)
