from __future__ import annotations
from typing import List, Dict, Optional

from lib.sql_parser.object_blocked_exception import ObjectBlockedException


class Condition:

    def __repr__(self) -> str:
        return f"{self.__condition_type}({self.__conditions})"

    def __init__(self, condition_type: str) -> None:
        self.__condition_type: str = condition_type
        self.__conditions: List[Condition | str] = []
        self.__blocked: bool = False

    @property
    def blocked(self) -> bool:
        return self.__blocked

    @property
    def condition_type(self) -> str:
        return self.__condition_type

    @property
    def conditions(self) -> List[Condition | str]:
        return self.__conditions.copy()

    @condition_type.setter
    def condition_type(self, condition_type: str):
        if not self.__blocked:
            self.__condition_type = condition_type
        else:
            raise ObjectBlockedException(object_type="Condition")

    @conditions.setter
    def conditions(self, conditions: List[Condition | str]):
        if not self.__blocked:
            self.__conditions = conditions
        else:
            raise ObjectBlockedException(object_type="Condition")

    def block_condition(self):
        self.__blocked = False

    def add_condition(self, condition: Condition | str):
        if not self.__blocked:
            self.__conditions.append(condition)
        else:
            raise ObjectBlockedException(object_type="Condition")
