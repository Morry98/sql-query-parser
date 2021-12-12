# CIUF (Caching interface unified format)
[Image of a train, NotImplementedYet()]

Ciuf is a unified caching technology used for blazing fast access queried using SQL language.

This project is heavily inspired by the [Noria DB](https://github.com/mit-pdos/noria) project.

## Quickstart
Running on python 3.10

## Examples
```sql
/* base tables */
CREATE TABLE stories (id int, title text);
CREATE TABLE votes (story_id int, user int);
/* vote count per story */
CREATE VIEW VoteCount AS
SELECT story_id, COUNT(*) AS vcount
FROM votes GROUP BY story_id;
/* story details */
CREATE VIEW StoriesWithVC AS
SELECT id, author, title, url, vcount
FROM stories
JOIN VoteCount ON VoteCount.story_id = stories.id
WHERE stories.id = ?;
/* Distinct voted story ids */
CREATE VIEW StoryIds AS
SELECT distinct(story_id) FROM votes;
```
