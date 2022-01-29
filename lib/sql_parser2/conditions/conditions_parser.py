import os
from typing import Tuple

from lib.sql_parser2 import conditions
from lib.sql_parser2.configurations import Configurations


def compute(word: str, config: Configurations) -> Tuple[bool, Configurations]:
    if type(word) is not str:
        raise Exception('word must be a string!')
    for class_ in conditions.__dict__.items():
        if class_[0].startswith("_") or class_[0] == os.path.basename(__file__).replace(".py", ""):
            continue
        result, config = class_[1].compute(word=word, config=config)
        if result is True:
            return True, config
    return False, config
