from typing import Tuple, Optional

from lib.sql_parser.table import Table
from lib.sql_parser2 import function_parser, keyword_parser
from lib.sql_parser2.configurations import Configurations


def compute(word: str, config: Configurations) -> Tuple[bool, Configurations]:
    if type(word) is not str:
        raise Exception('word must be a string!')
    for class_ in [function_parser, keyword_parser]:
        result, config = class_.compute(word=word.strip().lower(), config=config)
        if result is True:
            return True, config
    for function in [
        __parse_select_columns,
        __parse_from_tables
    ]:
        result, config = function(word=word.strip().lower(), config=config)
        if result is True:
            return True, config
    return False, config


def __parse_select_columns(word: str, config: Configurations) -> Tuple[bool, Configurations]:
    if (len(config.keywords) > 0 and config.keywords[-1] == "select") or (
            len(config.keywords) > 1 and config.keywords[-2] == "select" and config.keywords[-1] == "as"):
        if "as" in word:
            config.add_keyword("as")
        else:
            if config.keywords[-1] == "as":
                add_column_to_query(config=config, alias=word)
                config.pop_last_keyword()
            elif "," in word:
                word = word[:-1]
                config.add_parsing_value(parsing_value=(word, None))
                add_column_to_query(config=config)
                config.pop_last_parsing_value()
            else:
                config.add_parsing_value(parsing_value=(word, None))
                add_column_to_query(config=config)
        return True, config
    return False, config


def __parse_from_tables(word: str, config: Configurations) -> Tuple[bool, Configurations]:
    if (len(config.keywords) > 0 and config.keywords[-1] == "from") or (
            len(config.keywords) > 1 and config.keywords[-2] == "from" and config.keywords[-1] == "as"):
        if "as" in word:
            config.add_keyword("as")
        else:
            if config.keywords[-1] == "as":
                add_table_to_query(config=config, alias=word)
                config.pop_last_keyword()
            elif "," in word:
                word = word[:-1]
                config.add_parsing_value(parsing_value=(word, None))
                add_table_to_query(config=config)
                config.pop_last_parsing_value()
            else:
                if len(config.parsing_value) > 0:
                    raise Exception(f"Parsing value already present when parsing from table with alias,"
                                    f" this case is not implemented. "
                                    f"table= {word}  parsing_values= {config.parsing_value}")
                config.add_parsing_value(parsing_value=(word, None))
        return True, config
    return False, config


def add_column_to_query(config: Configurations, alias: Optional[str] = None):
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


def add_table_to_query(config: Configurations, alias: Optional[str] = None):
    parsing_table = config.pop_last_parsing_value()
    table_str = parsing_table[0]
    if alias is None:
        config.add_parsing_value(parsing_value=parsing_table)
        alias = parsing_table[1]
    elif parsing_table[1] is not None:
        raise Exception(f"Double alias for {table_str} table: {parsing_table[1]} and {alias}")
    alias = alias.replace(",", "") if alias is not None else None
    table_by_name = config.query.get_table_by_name_or_alias(table_str)
    table_by_alias = config.query.get_table_by_name_or_alias(alias)
    if table_by_name is not None and table_by_alias is not None:
        raise Exception(f"Found double table object for table {table_str} alias {alias}")
    table = table_by_alias if table_by_alias is not None else table_by_name
    if table is None:
        table = Table(alias=alias)
        config.query.add_table(table)
    table.name = table_str
    table.alias = alias
