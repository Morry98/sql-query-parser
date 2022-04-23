
     _____  _____ _      ______                        
    /  ___||  _  | |     | ___ \                       
    \ `--. | | | | |     | |_/ /_ _ _ __ ___  ___ _ __ 
     `--. \| | | | |     |  __/ _` | '__/ __|/ _ \ '__|
    /\__/ /\ \/' / |____ | | | (_| | |  \__ \  __/ |   
    \____/  \_/\_\_____/ \_|  \__,_|_|  |___/\___|_|   

### This is an alpha version

![GitHub](https://img.shields.io/github/license/morry98/sql-query-parser)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/morry98/sql-query-parser)
![GitHub top language](https://img.shields.io/github/languages/top/morry98/sql-query-parser)
![GitHub issues](https://img.shields.io/github/issues/morry98/sql-query-parser)
[![PyPI Downloads](https://img.shields.io/pypi/dm/sql-query-parser?color=green&label=Pypi%20download)](
https://pypi.org/project/sql-query-parser/)

[![Coverage Status](https://coveralls.io/repos/github/Morry98/sql-query-parser/badge.svg?branch=master)](
https://coveralls.io/github/Morry98/sql-query-parser?branch=master)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=Morry98_sql-query-parser&metric=bugs)](
https://sonarcloud.io/summary/new_code?id=Morry98_sql-query-parser)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=Morry98_sql-query-parser&metric=vulnerabilities)](
https://sonarcloud.io/summary/new_code?id=Morry98_sql-query-parser)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=Morry98_sql-query-parser&metric=code_smells)](
https://sonarcloud.io/summary/new_code?id=Morry98_sql-query-parser)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Morry98_sql-query-parser&metric=alert_status)](
https://sonarcloud.io/summary/new_code?id=Morry98_sql-query-parser)

[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=Morry98_sql-query-parser&metric=ncloc)](
https://sonarcloud.io/summary/new_code?id=Morry98_sql-query-parser)
![GitHub stars](https://img.shields.io/github/stars/morry98/sql-query-parser)
![GitHub pull requests](https://img.shields.io/github/issues-pr/morry98/sql-query-parser)

An advanced python sql query parser, It takes a sql query and returns a specific data structure with table,
columns, functions and conditions.

## Quickstart
Tested only on python 3.10, it doesn't work with lower versions.

## Usage

```python
from sql_query_parser.sql_query_parser import parse_query

parsed_query = parse_query("""SELECT
        COUNT(v.star) AS aa,
        COUNT(t1.b),
        v.story_id,
        t1.test as tt,
        v.test1,
        COUNT(t1.ff)
        FROM votes as v, t1
        where v.story_id = :story_id and (v.date > :date or v.role = :role) and t1.test = v.test;
        """)
print(parsed_query)
```

## PYPI page
https://pypi.org/project/sql-query-parser/
