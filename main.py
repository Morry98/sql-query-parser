import sqlparse

from lib.engine import Engine
from loguru import logger

from lib.sql_parser.sql_parser_test import SqlParserTest
from lib.sql_parser import sql_parser as old_sql_parser
from lib.sql_parser2 import sql_parser

db_path = "sqlite:///D:\\PersonalProject\\ciuf\\test.db"
logger.info(db_path)

# x = Engine(db_path)
#
# x.update_dag(
#     """
#     CREATE VIEW test AS
#     SELECT story_id, COUNT(*) AS vcount
#     FROM votes GROUP BY story_id;
#     """
# )
#
# x.update_dag(
#     """
#     CREATE VIEW StoriesWithVC AS
#     SELECT id, author, title, url, vcount
#     FROM stories
#     JOIN VoteCount ON VoteCount.story_id = stories.id
#     WHERE stories.id = ?;
#     """
# )
#
# x.print_dag()



# Old
# sql_parser_test = SqlParserTest()
#
# sql_parser_test.query = """SELECT v.story_id, COUNT(v.pippo) AS aa
#      FROM votes as v;
#     """
#
# sql_parser_test.test(sqlparse.parse("""SELECT v.story_id, COUNT(v.pippo) AS aa
#      FROM votes as v;
#     """)[0])
# sql_parser_test.print()
#
# print("\n\n\n")
#
# print(f"{sql_parser_test.tables=}")
# print(f"{sql_parser_test.functions=}")
# print(f"{sql_parser_test.columns=}")


query1 = sql_parser.parse_query("""SELECT
    COUNT(v.star) AS aa,
    COUNT(t1.b),
    v.story_id,
    t1.test as tt,
    v.test1,
    COUNT(t1.ff)
    FROM votes as v, t1
    where v.story_id = :story_id and (v.date > :date or v.role = :role) and t1.test = v.test;
     """)
query1_old = old_sql_parser.parse_query("""SELECT COUNT(v.star) AS vote, v.story_id
     FROM votes as v
     where v.story_id = :story_id and (v.date > :date or v.role = :role);
     """)

#query2 = sql_parser.parse_query("""
#SELECT stories.id, stories.author, stories.title, stories.url, stories.vcount
#     FROM stories
#     JOIN VoteCount ON VoteCount.story_id = stories.id
#     WHERE stories.id = ?;""")

print(query1)
#print(query1_old)
#print(query2)
