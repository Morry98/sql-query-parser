from typing import List, Dict, Optional, Tuple

from lib.exceptions.different_conditions_in_parenthesis_exception import DifferentConditionsInParenthesisException
from lib.sql_parser.condition import Condition
from lib.sql_parser.query import Query
from lib.sql_parser.table import Table


class Configurations:

    def __init__(self, query: Query) -> None:
        self.__keyword: List[str] = []
        self.__parsing_value: List[Tuple[str, Optional[str]]] = []  # [(column, alias)]
        self.__query = query
        self.__conditions_type: List[str | List[str]] = []
        self.__conditions: List[str | List[str]] = []
        self.__condition_position: int = 0
        self.__is_new_condition: bool = True

    @property
    def keywords(self) -> List[str]:
        return self.__keyword.copy()

    @property
    def is_new_condition(self) -> bool:
        return self.__is_new_condition

    @property
    def conditions(self) -> List[str | List[str]]:
        return self.__conditions.copy()

    @property
    def conditions_type(self) -> List[str | List[str]]:
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

    @parsing_value.setter  # type:ignore
    def parsing_value(self, parsing_value: List[Tuple[str, Optional[str]]]):
        self.__parsing_value = parsing_value.copy()

    @is_new_condition.setter  # type:ignore
    def is_new_condition(self, is_new_condition: bool):
        self.__is_new_condition = is_new_condition

    @keywords.setter  # type:ignore
    def keywords(self, keywords: List[str]):
        self.__keyword = keywords.copy()

    @conditions.setter  # type:ignore
    def conditions(self, conditions: List[str | List[str]]):
        self.__conditions = conditions.copy()

    @conditions_type.setter  # type:ignore
    def conditions_type(self, conditions_type: List[str | List[str]]):
        self.__conditions_type = conditions_type.copy()

    @condition_position.setter  # type:ignore
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
        self.__conditions_type.append([])

    def add_value_to_condition(self, value: str):
        if self.__condition_position == 0:
            self.__conditions.append(value)
        else:
            self.__conditions[self.__condition_position].append(value)

    def pop_value_from_condition(self) -> str:
        if self.__condition_position == 0:
            return self.__conditions.pop(-1)
        else:
            return self.__conditions[self.__condition_position].pop(-1)

    def pop_last_condition(self) -> str | List[str]:
        if len(self.__conditions) == 0 or self.__conditions is None:
            raise Exception("No conditions to pop")
        return self.__conditions.pop(-1)

    def add_condition_type(self, type_: str):
        if self.__condition_position == 0:
            self.__conditions_type.append(type_)
        else:
            self.__conditions_type[self.__condition_position].append(type_)
        if self.check_conditions_type() is not True:
            raise DifferentConditionsInParenthesisException()

    def add_parsing_value(self, parsing_value: Tuple[str, Optional[str]]):
        self.__parsing_value.append(parsing_value)

    def pop_last_parsing_value(self) -> Tuple[str, Optional[str]]:
        if len(self.__parsing_value) == 0 or self.__parsing_value is None:
            raise Exception("No parsing_value to pop")
        return self.__parsing_value.pop(-1)

    def check_conditions_type(self) -> bool:
        return check_lists_all_equal_value(self.__conditions_type)

    def compute_condition(self) -> None:
        condition: Condition = get_query_condition_from_lists(
            conditions=self.__conditions,
            conditions_type=self.__conditions_type)
        self.query.add_condition(condition)


def check_lists_all_equal_value(list_to_check: List[str | List]) -> bool:
    c_type: Optional[str] = None
    for cond_type in list_to_check:
        if type(cond_type) == list:
            result = check_lists_all_equal_value(cond_type)
            if result is False:
                return False
        else:
            if c_type is None:
                c_type = cond_type
            elif c_type != cond_type:
                return False
    return True


def get_query_condition_from_lists(conditions: List[str | List[str]],
                                   conditions_type: List[str | List[str]]
                                   ) -> Condition:
    # TODO Check if the where condition starts with open parenthesis
    cond = Condition(condition_type=conditions_type[0])
    index = 0
    for c in conditions:
        if type(c) == list:
            cond.add_condition(get_query_condition_from_lists(conditions=c,  # type:ignore
                                                              conditions_type=conditions_type[index]))  # type:ignore
        else:
            cond.add_condition(c)  # type:ignore
        index += 1
    return cond
