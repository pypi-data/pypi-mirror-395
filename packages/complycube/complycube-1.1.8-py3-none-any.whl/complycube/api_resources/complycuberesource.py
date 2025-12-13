class ComplyCubeResource(object):

    def __init__(self, client):
        self.client = client

    @property
    def resource_object(self):
        raise NotImplementedError
