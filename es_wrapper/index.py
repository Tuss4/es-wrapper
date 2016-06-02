from . import es_conn


class IndexManager(object):

    conn = es_conn()

    # Creates an index on the node.
    def create_index(self, index_name, mapping):
        return self.conn.indices.create(index=index_name, body=mapping)

    # Retrieve an index and its settings on the node.
    def retrieve_index(self, index_name):
        return self.conn.indices.get(index=[index_name])

    # Deletes an index from the node.
    def delete_index(self, index_name):
        return self.conn.indices.delete(index=[index_name])
