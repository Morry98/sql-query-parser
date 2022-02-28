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
        self.__conditions_type: List[str] = []
        self.__conditions: List[List[str]] = [[]]
        self.__condition_position: int = 0
        self.__is_new_condition: bool = True

    @property
    def keywords(self) -> List[str]:
        return self.__keyword.copy()

    @property
    def is_new_condition(self) -> bool:
        return self.__is_new_condition

    @property
    def conditions(self) -> List[List[str]]:
        return self.__conditions.copy()

    @property
    def conditions_type(self) -> List[str]:
        return self.__conditions_type.copy()

    @property
    def condition_position(self) -> int:
        return self.__condition_position

    @property
    def query(self) -> Query:
        return self.__query

    @property
    def parsing_value(self) -> List[Tuple[str, Optional[str]]]:
        return self.__parsing_value.copy()

    @parsing_value.setter
    def parsing_value(self, parsing_value: List[Tuple[str, Optional[str]]]):
        self.__parsing_value = parsing_value.copy()

    @is_new_condition.setter
    def is_new_condition(self, is_new_condition: bool):
        self.__is_new_condition = is_new_condition

    @keywords.setter
    def keywords(self, keywords: List[Table]):
        self.__keyword = keywords.copy()

    @conditions.setter
    def conditions(self, conditions: List[List[str]]):
        self.__conditions = conditions.copy()

    @conditions_type.setter
    def conditions_type(self, conditions_type: List[str]):
        self.__conditions_type = conditions_type.copy()

    @condition_position.setter
    def condition_position(self, position: int):
        self.__condition_position = position
        i = self.__condition_position + 1 - len(self.__conditions)
        for _ in range(i):
            self.create_new_condition()

    def add_keyword(self, keyword: str):
        self.__keyword.append(keyword)

    def pop_last_keyword(self) -> str:
        if len(self.__keyword) == 0 or self.__keyword is None:
            raise Exception("No Keyword to pop")
        return self.__keyword.pop(-1)

    def create_new_condition(self):
        self.__conditions.append([])

    def add_condition(self, condition: List[str]):
        self.__conditions.append(condition.copy())

    def add_value_to_condition(self, value: str):
        self.__conditions[self.__condition_position].append(value)

    def pop_value_from_condition(self) -> str:
        return self.__conditions[self.__condition_position].pop(-1)

    def pop_last_condition(self) -> List[str]:
        if len(self.__conditions) == 0 or self.__conditions is None:
            raise Exception("No conditions to pop")
        return self.__conditions.pop(-1)

    def add_condition_type(self, type_: str):
        self.__conditions_type.append(type_)

    def add_parsing_value(self, parsing_value: Tuple[str, Optional[str]]):
        self.__parsing_value.append(parsing_value)

    def pop_last_parsing_value(self) -> Tuple[str, Optional[str]]:
        if len(self.__parsing_value) == 0 or self.__parsing_value is None:
            raise Exception("No parsing_value to pop")
        return self.__parsing_value.pop(-1)
