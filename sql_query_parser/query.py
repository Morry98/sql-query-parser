from typing import List, Dict, Optional

from sql_query_parser.condition import Condition
from sql_query_parser.exceptions.object_blocked_exception import ObjectBlockedException
from sql_query_parser.table import Table


class Query:

    def __init__(
            self,
            text: str
    ) -> None:
        self.__text: str = text
        self.__tables: List[Table] = []
        self.__tables_by_alias: Dict[str, int] = {}
        self.__tables_by_name: Dict[str, int] = {}
        self.__condition: Optional[Condition] = None
        self.__blocked: bool = False

    def __repr__(self) -> str:
        string: str = "Tables:\n"
        for t in self.__tables:
            string += f"{t}\n"
        if self.__condition is not None:
            string += f"Condition:\n{self.__condition}\n"
        return string

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(
            self,
            other: object
    ) -> bool:
        if isinstance(other, Query):
            return (
                self.__text == other.__text and
                self.__tables == other.__tables and
                self.__tables_by_alias == other.__tables_by_alias and
                self.__tables_by_name == other.__tables_by_name and
                self.__condition == other.__condition and
                self.__blocked == other.__blocked
            )
        return False

    def copy(self) -> "Query":
        q: Query = Query(self.__text)
        q.__tables = self.__tables.copy()
        q.__tables_by_alias = self.__tables_by_alias.copy()
        q.__tables_by_name = self.__tables_by_name.copy()
        if self.__condition is not None:
            q.__condition = self.__condition.copy()
        q.__blocked = self.__blocked
        return q

    @property
    def blocked(self) -> bool:
        return self.__blocked

    @blocked.setter
    def blocked(
            self,
            blocked: bool
    ) -> None:
        if not self.__blocked:
            self.__blocked = blocked
        else:
            raise ObjectBlockedException(object_type="Table", object_name="Query")

    @property
    def text(self) -> str:
        return self.__text

    @property
    def tables(self) -> List[Table]:
        return self.__tables.copy()

    @tables.setter
    def tables(
            self,
            tables: List[Table]
    ) -> None:
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

    def get_table_by_name_or_alias(
            self,
            name: Optional[str]
    ) -> Optional[Table]:
        if name in self.__tables_by_alias:
            return self.__tables[self.__tables_by_alias[name]]
        if name in self.__tables_by_name:
            return self.__tables[self.__tables_by_name[name]]
        return None

    @property
    def condition(self) -> Optional[Condition]:
        if self.__condition is None:
            return self.__condition
        return self.__condition.copy()

    @condition.setter
    def condition(
            self,
            condition: Condition
    ) -> None:
        if not self.__blocked:
            self.__condition = condition.copy()
        else:
            raise ObjectBlockedException(object_type="Query")

    def block_query(self) -> None:
        self.__blocked = True

    def add_table(
            self,
            table: Table
    ) -> None:
        if not self.__blocked:
            self.__tables.append(table)
            self.__tables_by_name[table.name] = len(self.__tables) - 1
            self.__tables_by_alias[table.alias] = len(self.__tables) - 1
        else:
            raise ObjectBlockedException(object_type="Query")

    def add_condition(
            self,
            condition: Condition,
            condition_type: Optional[str] = None
    ) -> None:
        if not self.__blocked:
            if self.__condition is None and condition_type is not None:
                self.__condition = Condition(condition_type=condition_type)
            elif self.__condition is not None and \
                    condition_type is not None and \
                    self.__condition.condition_type != condition_type:
                raise ValueError("Condition type is not consistent")
            if self.__condition is None:
                raise ValueError("Query Condition is None")
            self.__condition.add_condition(condition)
        else:
            raise ObjectBlockedException(object_type="Query")
