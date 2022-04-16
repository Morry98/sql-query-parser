from loguru import logger

from sql_query_parser import sql_query_parser

logger.info("START")

query1 = sql_query_parser.parse_query("""SELECT
    COUNT(v.star) AS aa,
    COUNT(t1.b),
    v.story_id,
    t1.test as tt,
    v.test1,
    COUNT(t1.ff)
    FROM votes as v, t1
    where v.story_id = :story_id and (v.date > :date or v.role = :role) and t1.test = v.test;
    """)
# query2 = sql_query_parser.parse_query("""
#     SELECT stories.id, stories.author, stories.title, stories.url, stories.vcount
#     FROM stories
#     JOIN VoteCount ON VoteCount.story_id = stories.id
#     WHERE stories.id = ?;""")

print(query1)
# print(query2)
