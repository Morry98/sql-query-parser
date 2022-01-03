from typing import List, Dict, Optional

import sqlparse
from sqlparse import tokens

from lib.sql_parser.condition import Condition
from lib.sql_parser.query import Query
from lib.sql_parser.table import Table


def parse_query(query_str: str) -> Query:
    query: Query = Query(text=query_str)
    __visit(token=sqlparse.parse(query_str)[0], query=query)
    for table in query.tables:
        table.block_table()
    for condition in query.condition:
        condition.block_condition()
    query.block_query()
    return query


def __visit(token, query: Query, config_dict: Optional[Dict] = None) -> None:
    if config_dict is None:
        config_dict = {"query_type": None}

    value = token.value  # TODO Remove

    if (config_dict["query_type"] == "select" and token.ttype == sqlparse.tokens.Punctuation and str(
            token.value).lower().strip() == ",") or token.is_keyword and \
            str(token.value).lower().strip() == "from":
        if "column_name" in config_dict:
            table_name = "" if len(str(config_dict["column_name"]).split(".")) < 2 else str(
                config_dict["column_name"]).split(".")[0]
            table = query.get_table_by_name_or_alias(table_name)
            if table is None:
                table = Table(alias=table_name)
                query.add_table(table)
            alias = str(config_dict["column_alias"]) if "column_alias" in config_dict else None
            if str(config_dict["column_name"]) not in table.columns:
                column_name = str(config_dict["column_name"])[0] if len(
                    str(config_dict["column_name"]).split(".")) < 2 else str(
                    config_dict["column_name"]).split(".")[1]
                table.add_column(column=column_name, alias=alias)
            if "function_value" in config_dict:
                table.add_function(function=str(config_dict["function_value"]), alias=alias)
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
            table = query.get_table_by_name_or_alias(table_alias)
            if table is not None:
                if query.get_table_by_name_or_alias(table_name) is not None:
                    raise Exception(
                        f"Problem parsing table {table_name} with alias {table_alias}, two are present in the query")
            else:
                table = query.get_table_by_name_or_alias(table_name)
            if table is None:
                table = Table(alias=table_name)
                query.add_table(table)
            table.name = table_name
            if table_alias is not None:
                table.alias = table_alias
        config_dict.pop("table_alias", None)
        config_dict.pop("table_name", None)

    elif config_dict["query_type"] == "where" and token.ttype == sqlparse.tokens.Punctuation and str(
            token.value).lower().strip() == ";":
        __add_conditions_in_query(config_dict, query)

    if token.is_keyword and str(token.value).lower().strip() == "select":
        config_dict["query_type"] = "select"
    elif token.is_keyword and str(token.value).lower().strip() == "from":
        config_dict["query_type"] = "from"
    elif token.is_keyword and str(token.value).lower().strip() == "where":
        config_dict["query_type"] = "where"
        config_dict["is_keyword"] = True
    else:
        if config_dict["query_type"] == "select" and not token.is_whitespace:
            __parse_select_query(token, config_dict)

        if config_dict["query_type"] == "from" and not token.is_whitespace:
            __parse_from_query(token, config_dict)

        if config_dict["query_type"] == "where" and not token.is_whitespace:
            __parse_where_query(token, config_dict, query)

    if token.is_group:
        for child in token.tokens:
            __visit(child, query=query, config_dict=config_dict)

    return None


def __parse_select_query(token, config_dict):
    column_has_alias: Optional[bool] = None
    if token.is_keyword and str(token.value).lower().strip() == "as":
        column_has_alias = True

    if isinstance(token, sqlparse.sql.Function):
        config_dict["is_function"] = True
        config_dict["function_value"] = str(token.value).strip()

    elif isinstance(token, sqlparse.sql.Parenthesis):
        config_dict["is_parenthesis"] = True

    if isinstance(token, sqlparse.sql.Identifier):
        if ("is_function" not in config_dict or (
                "is_function" in config_dict and "is_parenthesis" in config_dict)) and (
                "column_has_alias" not in config_dict or "column_has_alias" in config_dict and
                not config_dict["column_has_alias"]):
            config_dict["column_name"] = str(token.value).strip()

    elif "column_has_alias" in config_dict and "column_name" in config_dict and config_dict["column_has_alias"]:
        config_dict["column_alias"] = str(token.value).strip()

    if column_has_alias is not None:
        config_dict["column_has_alias"] = column_has_alias


def __parse_from_query(token, config_dict):
    if token.is_keyword or token.is_whitespace or token.is_group:
        return

    if "table_name" not in config_dict:
        config_dict["table_name"] = str(token.value).strip()
    else:
        config_dict["table_alias"] = str(token.value).strip()


def __parse_where_query(token, config_dict, query):
    if token.is_keyword is True:
        config_dict["is_keyword"] = True
        if "condition_type" not in config_dict:
            config_dict["condition_type"] = [[]]
        if str(token.value).lower().strip() == "and":
            config_dict["condition_type"][-1].append("and")
        if str(token.value).lower().strip() == "or":
            config_dict["condition_type"][-1].append("or")
    elif token.ttype == tokens.Punctuation:
        if str(token.value).lower().strip() == "(":
            config_dict["is_keyword"] = True
            if "condition" not in config_dict:
                config_dict["condition"] = []
            else:
                config_dict["condition"][-1] = config_dict["condition"][-1][:-1]
            config_dict["condition"].append([])
            if "condition_type" not in config_dict:
                config_dict["condition_type"] = []
            config_dict["condition_type"].append([])
        elif str(
                token.value).lower().strip() == ")":  # TODO Implement better inner condition not implemented and not check different inner condition types
            __add_conditions_in_query(config_dict, query)
    elif "is_keyword" in config_dict and config_dict["is_keyword"]:
        if "condition" not in config_dict:
            config_dict["condition"] = [[]]
        config_dict["condition"][-1].append(str(token.value).strip())
        config_dict["is_keyword"] = False

    return


def __add_conditions_in_query(config_dict, query):
    if "condition_type" not in config_dict or len(config_dict["condition_type"]) == 0:
        return
    index = len(config_dict["condition_type"])
    query_condition_len = len(query.condition)
    if query_condition_len < index:
        for i in range(index - query_condition_len):
            query.add_condition(Condition(config_dict["condition_type"][query_condition_len + i]))
    condition_type = config_dict["condition_type"].pop(-1)  # TODO Use for checks and sub condition creation
    conditions = config_dict["condition"].pop(-1)
    condition = query.condition
    for i in range(len(conditions)):
        condition[index - 1].add_condition(conditions[i])
    query.condition = condition
