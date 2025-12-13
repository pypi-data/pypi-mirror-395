class GetResourceMixin(object):
    def get(self, id,**params):
        """Get a resource object by it's Id"""
        response , _  = self.client._execute_api_request(
                "%s/%s" % (self.endpoint, id),'GET')
        return self.resource_object(**response)