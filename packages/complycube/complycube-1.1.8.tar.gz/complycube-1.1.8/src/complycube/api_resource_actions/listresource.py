import complycube.util as u
from complycube.model import ComplyCubeCollection

class ListResourceMixin(object):
    
    def auto_list(self,**kwargs):
        """Get resource list"""
        flat_kwargs = u.flatten(kwargs,sep='.')
        while True:
            response , _  = self.client._execute_api_request(self.endpoint,'GET',**flat_kwargs)
            for resource in (response.get('items') or []):
                yield self.resource_object(**resource)
            if (response['page'] == response['pages']) or (response['pages']==0):
                break
            flat_kwargs['page'] = str(int(response['page']) + 1)

    def list(self,**kwargs):
        """Get resource list"""
        flat_kwargs = u.flatten(kwargs,sep='.')
        response , _  = self.client._execute_api_request(self.endpoint,'GET',**flat_kwargs)
        return ComplyCubeCollection(**response)