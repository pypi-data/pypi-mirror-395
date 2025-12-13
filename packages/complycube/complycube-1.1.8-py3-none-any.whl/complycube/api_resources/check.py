from complycube.model import check
from complycube.api_resource_actions import GetResourceMixin
from complycube.api_resource_actions import CreateResourceMixin
from complycube.api_resource_actions import UpdateResourceMixin
from complycube.api_resource_actions import ListResourceMixin
from complycube.api_resources.complycuberesource import ComplyCubeResource

class Check(ComplyCubeResource, GetResourceMixin, CreateResourceMixin, UpdateResourceMixin,ListResourceMixin):

    @property
    def endpoint(self):
        return 'checks' 

    def create(self,clientId,type,**kwargs):
        """[Creates a new check.]

        Args:
            clientId ([str]): [The ID of the client.]
            type ([str]): [The type of check. Valid values include:
                                1. standard_screening_check
                                2. extensive_screening_check
                                3. document_check
                                4. identity_check
                                5. proof_of_address_check
                                6. multi_bureau_check]

        Returns:
            [Check]: [A client check]
        """
        return super(Check, self).create(clientId=clientId,type=type,**kwargs)

    def update(self, id, **params):
        """[Updates the specified check using parameters passed.]

        Returns:
            [Check]: [The updated client Check]
        """
        return super().update(id, **params)

    def validate(self,id,**params):
        """[Validates the outcome of the specified check.]

        Returns:
            [Outcome]: [The outcome of a check]
        """
        url = '%s/%s/validate' % (self.endpoint, id)
        response , _  = self.client._execute_api_request(url,'POST',**params)
        return check.Outcome(**response)

    def resource_object(self,**response):
        return check.Check(**response)
