class DeleteResourceMixin(object):
    def delete(self, id,**params):
        """Delete resource by Id"""
        _ , status_code  = self.client._execute_api_request(
                "%s/%s" % (self.endpoint, id),'DELETE')
        return None , status_code