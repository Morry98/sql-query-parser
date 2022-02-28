from typing import List, Dict, Optional

from lib.sql_parser.condition import Condition
from lib.sql_parser.query import Query
from lib.sql_parser.table import Table
from lib.sql_parser2 import word_recognition
from lib.sql_parser2.configurations import Configurations


def parse_query(query_str: str) -> Query:
    config = Configurations(query=Query(text=query_str))
    query_str = query_str.replace('\n', '').replace(";", "")
    for word in query_str.split(' '):
        if word == '':
            continue
        # TODO REMOVE
        # if word.lower().strip() == 'and':
        #     break
        result, config = word_recognition.compute(word=word, config=config)
        if not result:
            raise Exception(f'{word} Statement not implemented')

    query = config.query
    for table in query.tables:
        table.block_table()
    for condition in query.condition:
        condition.block_condition()
    query.block_query()
    return query
