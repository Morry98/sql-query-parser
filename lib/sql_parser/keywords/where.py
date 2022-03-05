from typing import Tuple

from lib.sql_parser.configurations import Configurations


def compute(word: str, config: Configurations) -> Tuple[bool, Configurations]:
    if type(word) is not str:
        raise Exception('word must be a string!')
    if "where" in word:
        keywords = config.keywords
        parsing_value = config.parsing_value
        if len(keywords) == 1 and keywords[-1] == "from":
            if len(parsing_value) > 1:
                raise Exception(f'where keyword found with more than 1 parsing table\n{parsing_value=}')
            elif len(parsing_value) == 1:
                config.pop_last_parsing_value()
            config.pop_last_keyword()
        else:
            raise Exception(f'where is not the first keyword, case not implemented\n{keywords=}')
        config.add_keyword("where")
        return True, config
    return False, config
