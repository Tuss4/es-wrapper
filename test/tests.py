import json
from unittest import TestCase
from . import db_conn, INITIAL_DATA
from .queries import CREATE_TEST_TABLE, POPULATE_TABLE, DROP_TABLES


class TestIndex(TestCase):

    conn = db_conn()

    def _create_table(self):
        with self.conn.cursor() as c:
            c.execute(CREATE_TEST_TABLE)

    def _populate_table(self):
        with self.conn.cursor() as c:
            c.execute(POPULATE_TABLE, (json.dumps(INITIAL_DATA), ))

    def _clear_table(self):
        with self.conn.cursor() as c:
            c.execute(DROP_TABLES)

    def setUp(self):
        self._create_table()
        self._populate_table()

    def tearDown(self):
        self._clear_table()

    def test_bruh(self):
        with self.conn.cursor() as c:
            c.execute("select * from superheroes;")
            self.assertEqual(len(c.fetchall()), 11)
