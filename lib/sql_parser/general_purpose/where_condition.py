from typing import Tuple, Optional

from lib.sql_parser.conditions import conditions_parser
from lib.sql_parser.configurations import Configurations


def compute(word: str, config: Configurations) -> Tuple[bool, Configurations]:
    if len(config.keywords) > 0 and "where" in config.keywords:
        for class_ in [conditions_parser]:
            result, config = class_.compute(word=word.strip().lower(), config=config)
            if result is True:
                return True, config
        match word:
            case "and" | "or":
                config.add_condition_type(word)
                config.is_new_condition = True
            case _:
                round_bracket_close = False
                if "(" in word:
                    word = word.replace("(", "")
                    config.condition_position += 1
                    config.is_new_condition = True
                elif ")" in word:
                    word = word.replace(")", "")
                    round_bracket_close = True
                if config.is_new_condition:
                    config.add_value_to_condition(word)
                    config.is_new_condition = False
                else:
                    value = config.pop_value_from_condition()
                    value = value + " " + word
                    config.add_value_to_condition(value)
                if round_bracket_close:
                    config.condition_position -= 1
                    config.is_new_condition = True
        return True, config
    return False, config
