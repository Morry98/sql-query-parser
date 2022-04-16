from sql_query_parser.query import Query
from sql_query_parser import word_recognition
from sql_query_parser.configurations import Configurations


def parse_query(
        query_str: str
) -> Query:
    config = Configurations(query=Query(text=query_str))
    query_str = query_str.replace('\n', '').replace(";", "")
    for word in query_str.split(' '):
        if word == '':
            continue
        result, config = word_recognition.compute(word=word, config=config)
        if not result:
            raise Exception(f'{word} Statement not implemented')

    config.check_conditions_type()
    config.compute_condition()

    query: Query = config.query
    for table in query.tables:
        table.block_table()
    for condition in query.condition:
        condition.block_condition()
    query.block_query()
    return query
