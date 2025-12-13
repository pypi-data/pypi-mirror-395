class UpdateResourceMixin(object):
    def update(self, id,**params):
        """Update resource by Id"""
        response , _  = self.client._execute_api_request(
                "%s/%s" % (self.endpoint, id),'POST',**params)
        return self.resource_object(**response)