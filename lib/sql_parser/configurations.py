from typing import List, Optional, Tuple

from lib.exceptions.different_conditions_in_parenthesis_exception import DifferentConditionsInParenthesisException
from lib.sql_parser.condition import Condition
from lib.sql_parser.query import Query


class Configurations:

    def __init__(
            self,
            query: Query
    ) -> None:
        self.__keyword: List[str] = []
        self.__parsing_value: List[Tuple[str, Optional[str]]] = []  # [(column, alias)]
        self.__query = query
        self.__conditions_type: List[str | List[str]] = []
        self.__conditions: List[str | List[str]] = []
        self.__condition_position: int = 0
        self.__is_new_condition: bool = True

    def __eq__(
            self,
            other: object
    ) -> bool:
        if not isinstance(other, Configurations):
            raise TypeError("Configurations can only be compared to other Configurations")
        if self.__query != other.query:
            return False
        if self.__keyword != other.__keyword:
            return False
        if self.__parsing_value != other.__parsing_value:
            return False
        if self.__condition_position != other.__condition_position:
            return False
        if self.__conditions != other.__conditions:
            return False
        if self.__conditions_type != other.__conditions_type:
            return False
        if self.__is_new_condition != other.__is_new_condition:
            return False
        return True

    @property
    def keywords(self) -> List[str]:
        return self.__keyword.copy()

    @keywords.setter
    def keywords(
            self,
            keywords: List[str]
    ) -> None:
        self.__keyword = keywords.copy()

    @property
    def is_new_condition(self) -> bool:
        return self.__is_new_condition

    @is_new_condition.setter
    def is_new_condition(
            self,
            is_new_condition: bool
    ) -> None:
        self.__is_new_condition = is_new_condition

    @property
    def conditions(self) -> List[str | List[str]]:
        return self.__conditions.copy()

    @conditions.setter
    def conditions(
            self,
            conditions: List[str | List[str]]
    ) -> None:
        self.__conditions = conditions.copy()

    @property
    def conditions_type(self) -> List[str | List[str]]:
        return self.__conditions_type.copy()

    @conditions_type.setter
    def conditions_type(
            self,
            conditions_type: List[str | List[str]]
    ) -> None:
        self.__conditions_type = conditions_type.copy()

    @property
    def condition_position(self) -> int:
        return self.__condition_position

    @condition_position.setter
    def condition_position(
            self,
            position: int
    ) -> None:
        self.__condition_position = position
        i = self.__condition_position + 1 - len(self.__conditions)
        for _ in range(i):
            self.create_new_condition()

    @property
    def query(self) -> Query:
        return self.__query

    @property
    def parsing_value(self) -> List[Tuple[str, Optional[str]]]:
        return self.__parsing_value.copy()

    @parsing_value.setter
    def parsing_value(
            self,
            parsing_value: List[Tuple[str, Optional[str]]]
    ) -> None:
        self.__parsing_value = parsing_value.copy()

    def add_keyword(
            self,
            keyword: str
    ) -> None:
        self.__keyword.append(keyword)

    def pop_last_keyword(self) -> str:
        if len(self.__keyword) == 0 or self.__keyword is None:
            raise Exception("No Keyword to pop")
        return self.__keyword.pop(-1)

    def create_new_condition(self) -> None:
        self.__conditions.append([])
        self.__conditions_type.append([])

    def add_value_to_condition(
            self,
            value: str
    ) -> None:
        if self.__condition_position == 0:
            self.__conditions.append(value)
        else:
            self.__conditions[self.__condition_position].append(value)  # type: ignore

    def pop_value_from_condition(self) -> str:
        if self.__condition_position == 0:
            return str(self.__conditions.pop(-1))
        else:
            return str(self.__conditions[self.__condition_position].pop(-1))  # type: ignore

    def pop_last_condition(self) -> str | List[str]:
        if len(self.__conditions) == 0 or self.__conditions is None:
            raise Exception("No conditions to pop")
        return self.__conditions.pop(-1)

    def add_condition_type(
            self,
            type_: str
    ) -> None:
        if self.__condition_position == 0:
            self.__conditions_type.append(type_)
        else:
            self.__conditions_type[self.__condition_position].append(type_)  # type: ignore
        if self.check_conditions_type() is not True:
            raise DifferentConditionsInParenthesisException()

    def add_parsing_value(
            self,
            parsing_value: Tuple[str, Optional[str]]
    ) -> None:
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
            result = check_lists_all_equal_value(list(cond_type))
            if result is False:
                return False
        else:
            cond_type = str(cond_type)
            if c_type is None:
                c_type = cond_type
            elif c_type != cond_type:
                return False
    return True


def get_query_condition_from_lists(conditions: List[str | List[str]],
                                   conditions_type: List[str | List[str]]
                                   ) -> Condition:
    # TODO Check if the where condition starts with open parenthesis
    cond: Condition = Condition(
        condition_type=str(conditions_type[0]) if type(conditions_type[0]) == str else conditions_type[0][0])
    index = 0
    for c in conditions:
        condition: Condition | str
        if type(c) == list:
            condition_type: List[str | List[str]] = list(conditions_type[index]) if \
                type(conditions_type[index]) is list else [str(conditions_type[index])]
            condition = get_query_condition_from_lists(conditions=list(c),
                                                       conditions_type=condition_type)
        else:
            condition = str(c)
        cond.add_condition(condition)
        index += 1
    return cond
