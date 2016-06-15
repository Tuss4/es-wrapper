import json
import os
import subprocess
from es_map_writer import writer
from importlib import import_module
from unittest import TestCase
from es_wrapper import es_conn
from es_wrapper.index import IndexManager
from es_wrapper.exceptions import IndexConflictError
from . import db_conn, INITIAL_DATA, DATABASE_URL
from .queries import CREATE_TEST_TABLE, POPULATE_TABLE, DROP_TABLES


class TestIndex(TestCase):

    conn = db_conn()
    es = es_conn()
    index_name = 'superheroes_index'

    def _create_table(self):
        with self.conn.cursor() as c:
            c.execute(CREATE_TEST_TABLE)

    def _populate_table(self):
        with self.conn.cursor() as c:
            c.execute(POPULATE_TABLE, (json.dumps(INITIAL_DATA), ))

    def _create_mapping(self):
        w = writer.Writer(DATABASE_URL)
        w.write_mapping('superheroes', 'hero_document', '/code/test')
        module = import_module('test.superheroes_es_mapping')
        self.assertTrue(hasattr(module, 'superheroes_mapping'))
        mapping = getattr(module, 'superheroes_mapping')
        return mapping

    def _clear_table(self):
        with self.conn.cursor() as c:
            c.execute(DROP_TABLES)

    def _clear_mapping(self):
        files = os.listdir('{}/test'.format(os.getcwd()))
        cmd = "rm {}/test/{}".format(os.getcwd(), 'superheroes_es_mapping.py')
        if 'superheroes_es_mapping.py' in files:
            subprocess.run([cmd], shell=True, check=True)

    def _clear_indices(self):
        if self.es.indices.exists([self.index_name]):
            self.es.indices.delete([self.index_name])

    def setUp(self):
        self._create_table()
        self._populate_table()

    def tearDown(self):
        self._clear_table()
        self._clear_mapping()
        self._clear_indices()

    def test_bruh(self):
        with self.conn.cursor() as c:
            c.execute("select * from superheroes;")
            self.assertEqual(len(c.fetchall()), 11)

    def test_create_index(self):
        mapping = self._create_mapping()
        index = IndexManager()
        index.create_index(self.index_name, mapping)
        self.assertTrue(self.es.indices.exists([self.index_name]))

        with self.assertRaises(IndexConflictError) as cm:
            index.create_index(self.index_name, mapping)
        excp = cm.exception
        self.assertEqual(excp.__str__(), "'superheroes_index index already exists on node.'")

        # Check mapping
        mappping = self.es.indices.get_mapping([self.index_name])
        expected = {
            'id': {'type': 'integer'},
            'name': {'type': 'string'},
            'alter_ego': {'type': 'string'},
        }
        self.assertEqual(mapping['mappings']['hero_document']['properties'], expected)

    def test_retrieve_index(self):
        mapping = self._create_mapping()
        index = IndexManager()
        index.create_index(self.index_name, mapping)
        self.assertTrue(self.es.indices.exists([self.index_name]))

        # Retrieve index
        dex = index.retrieve_index(self.index_name)
        actual = dex['superheroes_index']['mappings']['hero_document']['properties']
        expected = {
            'id': {'type': 'integer'},
            'name': {'type': 'string'},
            'alter_ego': {'type': 'string'},
        }
        self.assertEqual(actual, expected)

    def test_delete_index(self):
        mapping = self._create_mapping()
        index = IndexManager()
        index.create_index(self.index_name, mapping)
        self.assertTrue(self.es.indices.exists([self.index_name]))

        # Delete index
        index.delete_index(self.index_name)
        self.assertFalse(self.es.indices.exists([self.index_name]))
