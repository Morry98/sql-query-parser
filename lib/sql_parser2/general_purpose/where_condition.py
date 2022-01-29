from typing import Tuple, Optional

from lib.sql_parser2.conditions import conditions_parser
from lib.sql_parser2.configurations import Configurations


def compute(word: str, config: Configurations) -> Tuple[bool, Configurations]:
    if len(config.keywords) > 0 and "where" in config.keywords[-1]:
        for class_ in [conditions_parser]:
            result, config = class_.compute(word=word.strip().lower(), config=config)
            if result is True:
                return True, config
        if len(config.parsing_value) == 0:
            config.add_parsing_value((word, None))
        else:
            parsing_value = config.parsing_value
            parsing_value[-1] = (config.parsing_value[-1][0] + " " + word, None)
            config.parsing_value = parsing_value
        return True, config
    return False, config


def __add_table_to_query(config: Configurations, alias: Optional[str] = None):
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
