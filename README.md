# CIUF (Caching interface unified format)
Ciuf is a unified caching technology used for blazing fast access queried using SQL language.

## Examples
```sql
/* base tables */
CREATE TABLE stories (id int, title text);
CREATE TABLE votes (story_id int, user int);
/* internal view: vote count per story */
CREATE INTERNAL VIEW VoteCount AS
SELECT story_id, COUNT(*) AS vcount
FROM votes GROUP BY story_id;
/* external view: story details */
CREATE VIEW StoriesWithVC AS
SELECT id, author, title, url, vcount
FROM stories
JOIN VoteCount ON VoteCount.story_id = stories.id
WHERE stories.id = ?;
```