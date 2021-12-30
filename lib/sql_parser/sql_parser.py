from typing import List, Dict, Optional

import sqlparse

from lib.sql_parser.table import Table


def parse_query(query: str) -> List[Table]:
    tables = __visit(token=sqlparse.parse(query)[0])
    tables_list: List[Table] = []
    for table_str in tables.keys():
        if tables[table_str] not in tables_list:
            tables[table_str].block_table()
            tables_list.append(tables[table_str])
    return tables_list


def __visit(token, config_dict: Optional[Dict] = None, tables: Optional[Dict[str, Table]] = None) -> Dict[str, Table]:
    if config_dict is None:
        config_dict = {"query_type": None}
    if tables is None:
        tables = {}

    value = token.value  # TODO Remove

    if (config_dict["query_type"] == "select" and token.ttype == sqlparse.tokens.Punctuation and str(
            token.value).lower().strip() == ",") or token.is_keyword and \
            str(token.value).lower().strip() == "from":
        if "column_name" in config_dict:
            table_name = "" if len(str(config_dict["column_name"]).split(".")) < 2 else str(
                config_dict["column_name"]).split(".")[0]
            if table_name not in tables:
                tables[table_name] = Table(alias=table_name)
            table = tables[table_name]
            if str(config_dict["column_name"]) not in table.columns:
                alias = str(config_dict["column_alias"]) if "column_alias" in config_dict else None
                column_name = str(config_dict["column_name"])[0] if len(
                    str(config_dict["column_name"]).split(".")) < 2 else str(
                    config_dict["column_name"]).split(".")[1]
                table.add_column(column=column_name, alias=alias)
            if "function_value" in config_dict:
                table.add_function(str(config_dict["function_value"]))
        config_dict.pop("is_function", None)
        config_dict.pop("column_name", None)
        config_dict.pop("is_parenthesis", None)
        config_dict.pop("is_function", None)
        config_dict.pop("column_has_alias", None)
        config_dict.pop("function_value", None)
        config_dict.pop("column_alias", None)

    elif config_dict["query_type"] == "from" and token.ttype == sqlparse.tokens.Punctuation and str(
            token.value).lower().strip() in [",", ";"] or token.is_keyword and \
            str(token.value).lower().strip() == "where":
        table_alias = str(config_dict["table_alias"]) if "table_alias" in config_dict else None
        if "table_name" in config_dict:
            table_name = config_dict["table_name"]
            table = None
            if table_name in tables:
                table = tables[table_name]
            elif table_alias is not None and table_alias in tables:
                table = tables[table_alias]
            if table is None:
                table = Table(alias=table_name)
            table.name = table_name
            if table_alias is not None:
                table.alias = table_alias
            tables.pop(table_alias, None)
            tables.pop(table_name, None)
            tables[table_name] = table
        config_dict.pop("table_alias", None)
        config_dict.pop("table_name", None)

    if token.is_keyword and str(token.value).lower().strip() == "select":
        config_dict["query_type"] = "select"
    elif token.is_keyword and str(token.value).lower().strip() == "from":
        config_dict["query_type"] = "from"

    if config_dict["query_type"] == "select" and not token.is_whitespace:
        __parse_select_query(token, config_dict)

    if config_dict["query_type"] == "from" and not token.is_whitespace:
        __parse_from_query(token, config_dict)

    if token.is_group:
        for child in token.tokens:
            __visit(child, config_dict=config_dict, tables=tables)

    return tables


def __parse_select_query(token, config_dict):
    column_has_alias: Optional[bool] = None
    if token.is_keyword and str(token.value).lower().strip() == "as":
        column_has_alias = True

    if isinstance(token, sqlparse.sql.Function):
        config_dict["is_function"] = True
        config_dict["function_value"] = token.value

    elif isinstance(token, sqlparse.sql.Parenthesis):
        config_dict["is_parenthesis"] = True

    if isinstance(token, sqlparse.sql.Identifier):
        if ("is_function" not in config_dict or (
                "is_function" in config_dict and "is_parenthesis" in config_dict)) and (
                "column_has_alias" not in config_dict or "column_has_alias" in config_dict and
                not config_dict["column_has_alias"]):
            config_dict["column_name"] = str(token.value)

    elif "column_has_alias" in config_dict and "column_name" in config_dict and config_dict["column_has_alias"]:
        config_dict["column_alias"] = str(token.value)

    if column_has_alias is not None:
        config_dict["column_has_alias"] = column_has_alias


def __parse_from_query(token, config_dict):
    if token.is_keyword or token.is_whitespace or token.is_group:
        return

    if "table_name" not in config_dict:
        config_dict["table_name"] = str(token.value)
    else:
        config_dict["table_alias"] = str(token.value)
