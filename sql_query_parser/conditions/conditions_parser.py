import os
from typing import Tuple

from sql_query_parser import conditions
from sql_query_parser.configurations import Configurations


def compute(
        word: str,
        config: Configurations
) -> Tuple[bool, Configurations]:
    for class_ in conditions.__dict__.items():
        if class_[0].startswith("_") or class_[0] == os.path.basename(__file__).replace(".py", ""):
            continue
        result, config = class_[1].compute(word=word, config=config)
        if result is True:
            return True, config
    return False, config
