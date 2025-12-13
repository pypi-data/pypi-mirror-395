class CreateResourceMixin(object):
    def create(self, **kwargs):
        """Create resource"""
        response , _ = self.client._execute_api_request ("%s" % (self.endpoint), 'POST', **kwargs)
        if response: 
            return self.resource_object(**response)