from typing import Tuple

from lib.sql_parser2 import function_parser, keyword_parser
from lib.sql_parser2.configurations import Configurations


def compute(word: str, config: Configurations) -> Tuple[bool, Configurations]:
    if type(word) is not str:
        raise Exception('word must be a string!')
    for class_ in [keyword_parser, function_parser]:
        result, config = class_.compute(word=word.strip().lower(), config=config)
        if result is True:
            print(f"Matched {word}")
            return True, config
    return False, config
