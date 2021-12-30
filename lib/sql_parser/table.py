from typing import List, Dict, Optional


class Table:

    def __repr__(self) -> str:
        return f"Table= {self.__name}\nAlias= {self.__alias}\nColumns= {self.__columns}\nFunctions= {self.__functions}"

    def __init__(self, alias: str) -> None:
        self.__name: str = alias
        self.__alias: str = alias
        self.__columns: Dict = {}  # Col: Alias
        self.__functions: List = []
        self.__blocked: bool = False

    @property
    def blocked(self) -> bool:
        return self.__blocked

    @property
    def name(self) -> str:
        return self.__name

    @property
    def alias(self) -> str:
        return self.__alias

    @property
    def columns(self) -> Dict:
        return self.__columns.copy()

    @property
    def functions(self) -> List:
        return self.__functions.copy()

    @name.setter
    def name(self, name: str):
        self.__name = name

    @alias.setter
    def alias(self, alias):
        self.__alias = alias

    def block_table(self):
        self.__blocked = False

    def add_column(self, column: str, alias: Optional[str] = None):
        if alias is None:
            alias = column
        self.__columns[column] = alias

    def add_function(self, function: str):
        self.__functions.append(function)

