from typing import Tuple

from sql_query_parser.configurations import Configurations


def compute(
        word: str,
        config: Configurations
) -> Tuple[bool, Configurations]:
    if "from" in word:
        keywords = config.keywords
        parsing_value = config.parsing_value
        if len(keywords) == 1 and keywords[-1] == "select":
            if len(parsing_value) > 1:
                raise Exception(f'from keyword found with more than 1 parsing column\n{parsing_value=}')
            elif len(parsing_value) == 1:
                config.pop_last_parsing_value()
            config.pop_last_keyword()
        else:
            raise Exception(f'from is not the first keyword, case not implemented\n{keywords=}')
        config.add_keyword("from")
        return True, config
    return False, config
