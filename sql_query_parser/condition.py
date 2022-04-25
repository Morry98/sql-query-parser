from __future__ import annotations
from typing import List

from sql_query_parser.exceptions.object_blocked_exception import ObjectBlockedException


class Condition:

    def __init__(
            self,
            condition_type: str
    ) -> None:
        self.__condition_type: str = condition_type
        self.__conditions: List[Condition | str] = []
        self.__blocked: bool = False

    def __repr__(self) -> str:
        return f"{self.__condition_type}({self.__conditions})"

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Condition):
            return (
                self.__condition_type == other.__condition_type and
                self.__conditions == other.__conditions and
                self.__blocked == other.__blocked
            )
        return False

    def copy(self) -> 'Condition':
        new_condition: Condition = Condition(
            condition_type=self.__condition_type
        )
        new_condition.__conditions = self.__conditions.copy()
        new_condition.__blocked = self.__blocked
        return new_condition

    @property
    def blocked(self) -> bool:
        return self.__blocked

    @property
    def condition_type(self) -> str:
        return self.__condition_type

    @condition_type.setter
    def condition_type(
            self,
            condition_type: str
    ) -> None:
        if not self.__blocked:
            self.__condition_type = condition_type
        else:
            raise ObjectBlockedException(object_type="Condition")

    @property
    def conditions(self) -> List[Condition | str]:
        return self.__conditions.copy()

    @conditions.setter
    def conditions(
            self,
            conditions: List[Condition | str]
    ) -> None:
        if not self.__blocked:
            self.__conditions = conditions
        else:
            raise ObjectBlockedException(object_type="Condition")

    def block_condition(self) -> None:
        # TODO: Block all sub-conditions
        self.__blocked = False

    def add_condition(
            self,
            condition: Condition | str
    ) -> None:
        if not self.__blocked:
            self.__conditions.append(condition)
        else:
            raise ObjectBlockedException(object_type="Condition")
