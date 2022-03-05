from typing import List, Dict, Optional

from lib.sql_parser.condition import Condition
from lib.exceptions.object_blocked_exception import ObjectBlockedException
from lib.sql_parser.table import Table


class Query:

    def __repr__(self) -> str:
        string: str = "Tables:\n"
        for t in self.__tables:
            string += f"{t}\n"
        string += f"Condition: \n{self.__condition}"
        return string

    def __init__(self, text: str) -> None:
        self.__text: str = text
        self.__tables: List[Table] = []
        self.__tables_by_alias: Dict[str, int] = {}
        self.__tables_by_name: Dict[str, int] = {}
        self.__condition: List[Condition] = []
        self.__blocked: bool = False

    @property
    def blocked(self) -> bool:
        return self.__blocked

    @property
    def text(self) -> str:
        return self.__text

    @property
    def tables(self) -> List[Table]:
        return self.__tables.copy()

    def get_table_by_name_or_alias(self, name: str) -> Optional[Table]:
        if name in self.__tables_by_alias:
            return self.__tables[self.__tables_by_alias[name]]
        if name in self.__tables_by_name:
            return self.__tables[self.__tables_by_name[name]]
        return None

    @property
    def condition(self) -> List[Condition]:
        return self.__condition.copy()

    @tables.setter
    def tables(self, tables: List[Table]):
        if not self.__blocked:
            self.__tables = tables.copy()
            self.__tables_by_name = {}
            self.__tables_by_alias = {}
            i = 0
            for t in self.__tables:
                self.__tables_by_name[t.name] = i
                self.__tables_by_alias[t.alias] = i
                i += 1
        else:
            raise ObjectBlockedException(object_type="Query")

    @condition.setter
    def condition(self, condition: List[Condition]):
        if not self.__blocked:
            self.__condition = condition.copy()
        else:
            raise ObjectBlockedException(object_type="Query")

    def block_query(self):
        self.__blocked = False

    def add_table(self, table: Table):
        if not self.__blocked:
            self.__tables.append(table)
            self.__tables_by_name[table.name] = len(self.__tables) - 1
            self.__tables_by_alias[table.alias] = len(self.__tables) - 1
        else:
            raise ObjectBlockedException(object_type="Query")

    def add_condition(self, condition: Condition):
        if not self.__blocked:
            self.__condition.append(condition)
        else:
            raise ObjectBlockedException(object_type="Query")
