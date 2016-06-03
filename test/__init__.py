import os
import psycopg2
from urllib.parse import urlparse


DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgres://postgres:postgres@{}:5432/postgres'.format(os.getenv('DB_1_PORT_5432_TCP_ADDR'))
)


def db_conn():
    parts = urlparse(DATABASE_URL)
    db = parts.path.strip('/')
    user = parts.username
    pw = parts.password
    port = parts.port
    host = parts.hostname
    connection = psycopg2.connect(
        host=host, port=port, user=user, password=pw, database=db)
    connection.set_session(autocommit=True)
    return connection


INITIAL_DATA = [
    {"name": "Black Panther", "alter_ego": "T'Challa"},
    {"name": "Captain America", "alter_ego": "Sam Wilson"},
    {"name": "Spider-Man", "alter_ego": "Peter Parker"},
    {"name": "Captain Marvel", "alter_ego": "Carol Danvers"},
    {"name": "Nova", "alter_ego": "Richard Ryder"},
    {"name": "Ms Marvel", "alter_ego": "Kamala Kahn"},
    {"name": "Robin", "alter_ego": "Damian Wayne"},
    {"name": "Batman", "alter_ego": "Bruce Wayne"},
    {"name": "Superman", "alter_ego": "Clark Kent"},
    {"name": "Flash", "alter_ego": "Barry Allen"},
    {"name": "Cyborg", "alter_ego": "Victor Stone"}
]
