from typing import Optional, Dict, Tuple
import re

REGEX_PATTERN = re.compile("count\((.*)\)")


def compute(word: str, config: Optional[Dict] = None) -> Tuple[bool, Dict]:
    if type(word) is not str:
        raise Exception('word must be a string!')
    if "count" in word:
        matches = REGEX_PATTERN.findall(word)
        if len(matches) == 1:
            print(f"Function Count, column= {matches[0]}")  # TODO The logic must be implemented
        return True, config
    return False, config
