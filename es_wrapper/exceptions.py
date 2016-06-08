class IndexConflictError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr('{} index already exists on node.'.format(self.value))
