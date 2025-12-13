from complycube.model import accountinfo
from complycube.api_resources.complycuberesource import ComplyCubeResource

class AccountInfo(ComplyCubeResource):

    @property
    def endpoint(self):
        return 'accountInfo' 

    def get(self,**kwargs):
        """[This endpoint allows you to retrieve account information.]
            
        Returns:
            [AccountInfo]: [Returns the account information.]
        """
        response , _  = self.client._execute_api_request(self.endpoint,'GET')
        return self.resource_object(**response)

    def resource_object(self,**response):
        return accountinfo.AccountInfo(**response)
