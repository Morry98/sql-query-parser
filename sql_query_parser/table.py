from typing import Dict, Optional

from sql_query_parser.exceptions.object_blocked_exception import ObjectBlockedException


class Table:

    def __init__(
            self,
            alias: str
    ) -> None:
        self.__name: str = alias
        self.__alias: str = alias
        self.__columns: Dict[str, str] = {}  # Col: Alias
        self.__functions: Dict[str, str] = {}
        self.__blocked: bool = False

    def __repr__(self) -> str:
        return f"Table= {self.__name}\nAlias= {self.__alias}\nColumns= {self.__columns}\n" \
               f"Functions= {self.__functions}\n"

    def __hash__(self):
        return hash(str(self))

    def __eq__(
            self,
            other: object
    ) -> bool:
        if isinstance(other, Table):
            return (
                self.__name == other.__name and
                self.__alias == other.__alias and
                self.__columns == other.__columns and
                self.__functions == other.__functions and
                self.__blocked == other.__blocked
            )
        return False

    def copy(self) -> 'Table':
        """
        Copy table

        Returns: Table
        """
        table = Table(
            alias=self.__alias
        )
        table.__name = self.__name
        table.__columns = self.__columns.copy()
        table.__functions = self.__functions.copy()
        table.__blocked = self.__blocked
        return table

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
            raise ObjectBlockedException(object_type="Table", object_name=self.__name)

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(
            self,
            name: str
    ) -> None:
        if not self.__blocked:
            self.__name = name
        else:
            raise ObjectBlockedException(object_type="Table", object_name=self.__name)

    @property
    def alias(self) -> str:
        return self.__alias

    @alias.setter
    def alias(
            self,
            alias: str
    ) -> None:
        if not self.__blocked:
            self.__alias = alias
        else:
            raise ObjectBlockedException(object_type="Table", object_name=self.__name)

    @property
    def columns(self) -> Dict[str, str]:
        return self.__columns.copy()

    @columns.setter
    def columns(
            self,
            columns: Dict[str, str]
    ) -> None:
        if not self.__blocked:
            self.__columns = columns.copy()
        else:
            raise ObjectBlockedException(object_type="Table", object_name=self.__name)

    @property
    def functions(self) -> Dict[str, str]:
        return self.__functions.copy()

    @functions.setter
    def functions(
            self,
            functions: Dict[str, str]
    ) -> None:
        if not self.__blocked:
            self.__functions = functions.copy()
        else:
            raise ObjectBlockedException(object_type="Table", object_name=self.__name)

    def block_table(self) -> None:
        """
        Block table

        Returns: None
        """
        self.__blocked = True

    def add_column(
            self,
            column: str,
            alias: Optional[str] = None
    ) -> None:
        """
        Add column to table

        Args:
            column: Column name
            alias: Column alias

        Raises: ObjectBlockedException when table is blocked

        Returns: None
        """
        if not self.__blocked:
            if alias is None:
                alias = column
            self.__columns[column] = alias
        else:
            raise ObjectBlockedException(object_type="Table", object_name=self.__name)

    def add_function(
            self,
            function: str,
            alias: Optional[str] = None
    ) -> None:
        """
        Add function to table

        Args:
            function: Function name
            alias: Function alias

        Raises: ObjectBlockedException when table is blocked

        Returns: None
        """
        if not self.__blocked:
            if alias is None:
                alias = function.lower().strip()
            self.__functions[function] = alias
        else:
            raise ObjectBlockedException(object_type="Table", object_name=self.__name)
