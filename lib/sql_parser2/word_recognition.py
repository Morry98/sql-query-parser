from typing import Optional, Dict

from lib.sql_parser2 import function_parser


def compute(word: str, config: Optional[Dict] = None):  # TODO Config probably will be a specific class
    if type(word) is not str:
        raise Exception('word must be a string!')
    for class_ in [function_parser]:
        result, config = class_.compute(word=word.strip().lower(), config=config)
        if result is True:
            print(f"Matched {word}")
            return True
    raise Exception(f'{word} Statement not implemented')


if __name__ == '__main__':  # TODO Remove this, it will be called by other functions to be created
    compute("count(table.col)")
