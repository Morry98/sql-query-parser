from typing import Tuple

from lib.sql_parser2.general_purpose import general_purpose_parser
from lib.sql_parser2.keywords import keyword_parser
from lib.sql_parser2.functions import function_parser
from lib.sql_parser2.configurations import Configurations


def compute(word: str, config: Configurations) -> Tuple[bool, Configurations]:
    if type(word) is not str:
        raise Exception('word must be a string!')
    for class_ in [function_parser, keyword_parser]:
        result, config = class_.compute(word=word.strip().lower(), config=config)
        if result is True:
            return True, config
    for class_ in [
        general_purpose_parser
    ]:
        result, config = class_.compute(word=word.strip().lower(), config=config)
        if result is True:
            return True, config
    return False, config
