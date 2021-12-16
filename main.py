from lib.engine import Engine
import os
from loguru import logger

db_path = "sqlite:///test.db"
logger.info(db_path)

x = Engine(db_path)
x.update_dag("""
CREATE VIEW test AS
SELECT story_id, COUNT(*) AS vcount
FROM votes GROUP BY story_id;
""")
x.update_dag("""
CREATE VIEW StoriesWithVC AS
SELECT id, author, title, url, vcount
FROM stories
JOIN VoteCount ON VoteCount.story_id = stories.id
WHERE stories.id = ?;
""")

x.print_dag()