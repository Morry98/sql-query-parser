from typing import Dict, Optional

from lib.exceptions.object_blocked_exception import ObjectBlockedException


class Table:

    def __repr__(self) -> str:
        return f"Table= {self.__name}\nAlias= {self.__alias}\nColumns= {self.__columns}\n" \
               f"Functions= {self.__functions}\n"

    def __init__(self, alias: str) -> None:
        self.__name: str = alias
        self.__alias: str = alias
        self.__columns: Dict[str, str] = {}  # Col: Alias
        self.__functions: Dict[str, str] = {}
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
    def columns(self) -> Dict[str, str]:
        return self.__columns.copy()

    @property
    def functions(self) -> Dict[str, str]:
        return self.__functions.copy()

    @name.setter
    def name(self, name: str):
        if not self.__blocked:
            self.__name = name
        else:
            raise ObjectBlockedException(object_type="Table", object_name=self.__name)

    @alias.setter
    def alias(self, alias):
        if not self.__blocked:
            self.__alias = alias
        else:
            raise ObjectBlockedException(object_type="Table", object_name=self.__name)

    def block_table(self):
        self.__blocked = False

    def add_column(self, column: str, alias: Optional[str] = None):
        if not self.__blocked:
            if alias is None:
                alias = column
            self.__columns[column] = alias
        else:
            raise ObjectBlockedException(object_type="Table", object_name=self.__name)

    def add_function(self, function: str, alias: Optional[str] = None):
        if not self.__blocked:
            if alias is None:
                alias = function.lower().strip()
            self.__functions[function] = alias
        else:
            raise ObjectBlockedException(object_type="Table", object_name=self.__name)
