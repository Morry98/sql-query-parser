#!/bin/bash

sqlite3 ../test.db "CREATE TABLE stories (
  id INTEGER PRIMARY KEY,
  author TEXT NOT NULL,
  title TEXT NOT NULL,
  url TEXT NOT NULL UNIQUE
);"

sqlite3 ../test.db "CREATE TABLE votes (
  id INTEGER PRIMARY KEY,
  story_id INTEGER,
  FOREIGN KEY (story_id) REFERENCES stories (id)
);"

sqlite3 ../test.db "INSERT INTO stories(id, author, title, url) VALUES (1, 'Mario Rossi', 'Un gatto sul tetto', 'ref1');"
sqlite3 ../test.db "INSERT INTO stories(id, author, title, url) VALUES (2, 'Pinco Palla', 'la prima si', 'ref2');"
sqlite3 ../test.db "INSERT INTO stories(id, author, title, url) VALUES (3, 'Matteo Verdi', 'Il volo', 'ref3');"

sqlite3 ../test.db "INSERT INTO votes(id, story_id) VALUES (1, 3);"
sqlite3 ../test.db "INSERT INTO votes(id, story_id) VALUES (2, 1);"
sqlite3 ../test.db "INSERT INTO votes(id, story_id) VALUES (3, 2);"
sqlite3 ../test.db "INSERT INTO votes(id, story_id) VALUES (4, 1);"
sqlite3 ../test.db "INSERT INTO votes(id, story_id) VALUES (5, 1);"
sqlite3 ../test.db "INSERT INTO votes(id, story_id) VALUES (6, 3);"
sqlite3 ../test.db "INSERT INTO votes(id, story_id) VALUES (7, 1);"
sqlite3 ../test.db "INSERT INTO votes(id, story_id) VALUES (8, 3);"
sqlite3 ../test.db "INSERT INTO votes(id, story_id) VALUES (9, 1);"
sqlite3 ../test.db "INSERT INTO votes(id, story_id) VALUES (10, 1);"
sqlite3 ../test.db "INSERT INTO votes(id, story_id) VALUES (11, 1);"
sqlite3 ../test.db "INSERT INTO votes(id, story_id) VALUES (12, 3);"