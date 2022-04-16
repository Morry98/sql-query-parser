from __future__ import annotations
from typing import List

from lib.exceptions.object_blocked_exception import ObjectBlockedException


class Condition:

    def __repr__(self) -> str:
        return f"{self.__condition_type}({self.__conditions})"

    def __init__(
            self,
            condition_type: str
    ) -> None:
        self.__condition_type: str = condition_type
        self.__conditions: List[Condition | str] = []
        self.__blocked: bool = False

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
        self.__blocked = False

    def add_condition(
            self,
            condition: Condition | str
    ) -> None:
        if not self.__blocked:
            self.__conditions.append(condition)
        else:
            raise ObjectBlockedException(object_type="Condition")
