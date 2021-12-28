from typing import List, Dict, Optional

import sqlparse


class SqlParser:
    def __init__(self) -> None:
        self.__query = ""
        self.__functions: List = []
        self.__columns: Dict = {}
        self.__tables: Dict = {}

        # TODO Remove following variables
        self.NameAliasMixin = []
        self.Token = []
        self.TokenList = []
        self.Statement = []
        self.Identifier = []
        self.IdentifierList = []
        self.TypedLiteral = []
        self.Parenthesis = []
        self.SquareBrackets = []
        self.Assignment = []
        self.If = []
        self.For = []
        self.Comparison = []
        self.Comment = []
        self.Where = []
        self.Having = []
        self.Case = []
        self.Function = []
        self.Begin = []
        self.Operation = []
        self.Values = []
        self.Command = []
        self.Keyword = []

    @property
    def query(self) -> str:
        return self.__query

    @query.setter
    def query(self, query: str) -> None:
        self.__query = query
        self.__visit(sqlparse.parse(self.__query)[0])

    @property
    def functions(self) -> List:
        return self.__functions.copy()

    @property
    def columns(self) -> Dict:
        return self.__columns.copy()

    @property
    def tables(self) -> Dict:
        return self.__tables.copy()

    def __visit(self, token, config_dict: Optional[Dict] = None) -> None:
        if config_dict is None:
            config_dict = {"select_query": False}

        value = token.value  # TODO Remove

        if token.is_keyword and str(token.value).lower().strip() == "select":
            config_dict["select_query"] = True
        elif token.is_keyword and str(token.value).lower().strip() == "from":
            config_dict["select_query"] = False

        if config_dict["select_query"] and not token.is_whitespace:
            if token.is_keyword and str(token.value).lower().strip() == "as":
                config_dict["column_has_alias"] = True

            if isinstance(token, sqlparse.sql.Function):
                self.__functions += [token.value]
                config_dict["is_function"] = True

            elif isinstance(token, sqlparse.sql.Parenthesis):
                config_dict["is_parenthesis"] = True

            if isinstance(token, sqlparse.sql.Identifier):
                if ("is_function" not in config_dict or (
                        "is_function" in config_dict and "is_parenthesis" in config_dict)) and (
                        "column_has_alias" not in config_dict or "column_has_alias" in config_dict and
                        not config_dict["column_has_alias"]):
                    config_dict["column_name"] = str(token.value)

            elif "column_has_alias" in config_dict and "column_name" in config_dict and config_dict["column_has_alias"]:
                self.__columns[str(config_dict["column_name"])] = str(token.value)

            if token.ttype == sqlparse.tokens.Punctuation and str(token.value).lower().strip() == ",":
                if "column_name" in config_dict and str(config_dict["column_name"]) not in self.__columns:
                    self.__columns[str(config_dict["column_name"])] = str(config_dict["column_name"])
                config_dict.pop("is_function", None)
                config_dict.pop("column_name", None)
                config_dict.pop("is_parenthesis", None)
                config_dict.pop("is_function", None)
                config_dict.pop("column_has_alias", None)

        if token.is_group:
            for child in token.tokens:
                self.__visit(child, config_dict)

        return None

    def test(self, token, count=0) -> int:  # TODO Remove
        is_group = token.is_group
        is_keyword = token.is_keyword
        is_whitespace = token.is_whitespace
        normalized = token.normalized
        ttype = token.ttype
        if not token.is_whitespace:
            print(f"{is_group=}")
            print(f"{is_keyword=}")
            print(f"{is_whitespace=}")
            print(f"{normalized=}")
            print(f"{ttype=}")
            print(f"value={token.value}")
            print(f"is_function={isinstance(token, sqlparse.sql.Function)}")
            print("\n\n")

        if token.is_keyword:
            self.Keyword += [(token.value, count)]

        if isinstance(token, sqlparse.sql.NameAliasMixin):
            self.NameAliasMixin += [(token.value, count)]

        if isinstance(token, sqlparse.sql.Token):
            self.Token += [(token.value, count)]

        if isinstance(token, sqlparse.sql.TokenList):
            self.TokenList += [(token.value, count)]

        if isinstance(token, sqlparse.sql.Statement):
            self.Statement += [(token.value, count)]

        if isinstance(token, sqlparse.sql.Identifier):
            self.Identifier += [(token.value, count)]

        if isinstance(token, sqlparse.sql.IdentifierList):
            self.IdentifierList += [(token.value, count)]

        if isinstance(token, sqlparse.sql.TypedLiteral):
            self.TypedLiteral += [(token.value, count)]

        if isinstance(token, sqlparse.sql.Parenthesis):
            self.Parenthesis += [(token.value, count)]

        if isinstance(token, sqlparse.sql.SquareBrackets):
            self.SquareBrackets += [(token.value, count)]

        if isinstance(token, sqlparse.sql.Assignment):
            self.Assignment += [(token.value, count)]

        if isinstance(token, sqlparse.sql.If):
            self.If += [(token.value, count)]

        if isinstance(token, sqlparse.sql.For):
            self.For += [(token.value, count)]

        if isinstance(token, sqlparse.sql.Comparison):
            self.Comparison += [(token.value, count)]

        if isinstance(token, sqlparse.sql.Comment):
            self.Comment += [(token.value, count)]

        if isinstance(token, sqlparse.sql.Where):
            self.Where += [(token.value, count)]

        if isinstance(token, sqlparse.sql.Having):
            self.Having += [(token.value, count)]

        if isinstance(token, sqlparse.sql.Case):
            self.Case += [(token.value, count)]

        if isinstance(token, sqlparse.sql.Function):
            self.Function += [(token.value, count)]

        if isinstance(token, sqlparse.sql.Begin):
            self.Begin += [(token.value, count)]

        if isinstance(token, sqlparse.sql.Operation):
            self.Operation += [(token.value, count)]

        if isinstance(token, sqlparse.sql.Values):
            self.Values += [(token.value, count)]

        if isinstance(token, sqlparse.sql.Command):
            self.Command += [(token.value, count)]

        if token.is_group:
            for child in token.tokens:
                count = self.test(child, count + 1)

        return count

    def print(self):  # TODO Remove
        print(f"NameAliasMixin={self.NameAliasMixin}")

        print(f"Token={self.Token}")

        print(f"TokenList={self.TokenList}")

        print(f"Statement={self.Statement}")

        print(f"Identifier={self.Identifier}")

        print(f"IdentifierList={self.IdentifierList}")

        print(f"TypedLiteral={self.TypedLiteral}")

        print(f"Parenthesis={self.Parenthesis}")

        print(f"SquareBrackets={self.SquareBrackets}")

        print(f"Assignment={self.Assignment}")

        print(f"If={self.If}")

        print(f"For={self.For}")

        print(f"Comparison={self.Comparison}")

        print(f"Comment={self.Comment}")

        print(f"Where={self.Where}")

        print(f"Having={self.Having}")

        print(f"Case={self.Case}")

        print(f"Function={self.Function}")

        print(f"Begin={self.Begin}")

        print(f"Operation={self.Operation}")

        print(f"Values={self.Values}")

        print(f"Command={self.Command}")

        print(f"Keyword={self.Keyword}")
