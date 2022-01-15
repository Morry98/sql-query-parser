import inspect
from typing import Optional, Dict, Tuple

from lib.sql_parser2 import functions


def compute(word: str, config: Optional[Dict] = None) -> Tuple[bool, Dict]:
    if type(word) is not str:
        raise Exception('word must be a string!')
    basic_word: str = word.strip().lower()
    for class_ in functions.__dict__.items():
        if class_[0].startswith("_"):
            continue
        result, config = class_[1].compute(word=word, config=config)
        if result is True:
            return True, config
    return False, config
