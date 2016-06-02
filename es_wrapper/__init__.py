from elasticsearch import Elasticsearch
import os


ES_NODE_URL = os.getenv('ES_NODE_URL')
ES_NODE_PORT = int(os.getenv('ES_NODE_PORT', 9200))


def es_conn():
    return Elasticsearch([{'host': ES_NODE_URL, 'port': ES_NODE_PORT}])
