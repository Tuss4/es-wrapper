CREATE_TEST_TABLE = """
CREATE TABLE IF NOT EXISTS superheroes (
    id        SERIAL PRIMARY KEY,
    name      VARCHAR(30),
    alter_ego VARCHAR(50)
);
"""


DROP_TABLES = """
DROP SCHEMA PUBLIC CASCADE;
CREATE SCHEMA PUBLIC;
"""


POPULATE_TABLE = """
INSERT INTO superheroes (name, alter_ego)
SELECT name, alter_ego
FROM
    json_populate_recordset(null::superheroes, %s);
"""
