from typing import List, Dict, Optional, Tuple

from lib.sql_parser.condition import Condition
from lib.sql_parser.object_blocked_exception import ObjectBlockedException
from lib.sql_parser.query import Query
from lib.sql_parser.table import Table


class Configurations:

    def __init__(self, query: Query) -> None:
        self.__keyword: List[str] = []
        self.__parsing_value: List[Tuple[str, Optional[str]]] = []  # [(column, alias)]
        self.__query = query

    @property
    def keywords(self) -> List[str]:
        return self.__keyword.copy()

    @property
    def query(self) -> Query:
        return self.__query

    @property
    def parsing_value(self) -> List[Tuple[str, Optional[str]]]:
        return self.__parsing_value.copy()

    @keywords.setter
    def keywords(self, keywords: List[Table]):
        self.__keyword = keywords.copy()

    def add_keyword(self, keyword: str):
        self.__keyword.append(keyword)

    def pop_last_keyword(self) -> str:
        if len(self.__keyword) == 0 or self.__keyword is None:
            raise Exception("No Keyword to pop")
        return self.__keyword.pop(-1)

    def add_parsing_value(self, parsing_value: Tuple[str, Optional[str]]):
        self.__parsing_value.append(parsing_value)

    def pop_last_parsing_value(self) -> Tuple[str, Optional[str]]:
        if len(self.__parsing_value) == 0 or self.__parsing_value is None:
            raise Exception("No parsing_value to pop")
        return self.__parsing_value.pop(-1)
