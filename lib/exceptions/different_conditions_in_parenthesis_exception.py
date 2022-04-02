
class DifferentConditionsInParenthesisException(Exception):
    """Exception raised when in a parenthesis there are different conditions.
    Ad example: WHERE a = 1 and b = 1 or c = 1

    Attributes:
        message: explanation of the error
    """

    def __init__(
            self,
            message: str = "There are different conditions type in a parenthesis"
    ) -> None:
        self.message: str = message
        super().__init__(self.message)

    def __str__(self) -> str:
        string = f"Message: {self.message}"
        return string
