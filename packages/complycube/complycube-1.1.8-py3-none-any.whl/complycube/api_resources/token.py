from complycube.model import token
from complycube.api_resource_actions import GetResourceMixin
from complycube.api_resource_actions import CreateResourceMixin
from complycube.api_resource_actions import UpdateResourceMixin
from complycube.api_resource_actions import DeleteResourceMixin
from complycube.api_resource_actions import ListResourceMixin
from complycube.api_resources.complycuberesource import ComplyCubeResource

class Token(ComplyCubeResource, CreateResourceMixin):

    @property
    def endpoint(self):
        return 'tokens' 

    def create(self,clientId,**kwargs):
        """[Generates an SDK token.]

        Arguments:
            clientId {str} -- [The ID of the client.]
            referrer {str} -- [The referrer attributes specifies the URI of the web page where the Web SDK will be used. The referrer sent by the browser must match the referrer URI pattern in the JWT for the SDK to successfully authenticate. ]
            appId {str} -- [The appId attributes specifies the bundle identifier of the app using the SDK. The bundle ID must match the bundle in the JWT for the SDK to successfully authenticate. ]

        Returns:
            [Token]: [Returns a token object with the generated token set.]
        """
        return super(Token, self).create(clientId=clientId, **kwargs)

    def resource_object(self,**response):
        return token.Token(**response)
