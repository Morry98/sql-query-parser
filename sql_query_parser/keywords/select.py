from typing import Tuple

from sql_query_parser.configurations import Configurations


def compute(
        word: str,
        config: Configurations
) -> Tuple[bool, Configurations]:
    if "select" in word:
        keywords = config.keywords
        if len(keywords) > 0:
            raise Exception(f'select is not the first keyword, case not implemented\n{keywords=}')
        config.add_keyword("select")
        return True, config
    return False, config
