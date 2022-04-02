from typing import Optional


class ObjectBlockedException(Exception):
    """Exception raised when an object is already blocked.

    Attributes:
        object_type: The type of the object
        object_name: the name of the object
        message: explanation of the error
    """

    def __init__(
            self,
            object_type: str,
            object_name: Optional[str] = None,
            message: str = "The table is already blocked."
    ) -> None:
        self.object_type: str = object_type
        self.object_name: Optional[str] = object_name
        self.message: str = message
        super().__init__(self.message)

    def __str__(self) -> str:
        string: str = f"Object Type: {self.object_type}\n"
        if self.object_name is not None:
            string += f"Object Name: {self.object_name}\n"
        string += f"Message: {self.message}"
        return string
