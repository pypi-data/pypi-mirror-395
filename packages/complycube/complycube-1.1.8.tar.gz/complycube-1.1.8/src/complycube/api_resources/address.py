from complycube.model import address
from complycube.api_resource_actions import GetResourceMixin
from complycube.api_resource_actions import CreateResourceMixin
from complycube.api_resource_actions import UpdateResourceMixin
from complycube.api_resource_actions import DeleteResourceMixin
from complycube.api_resource_actions import ListResourceMixin
from complycube.api_resources.complycuberesource import ComplyCubeResource

class Address(ComplyCubeResource, GetResourceMixin, CreateResourceMixin, UpdateResourceMixin, DeleteResourceMixin, ListResourceMixin):
    
    @property
    def endpoint(self):
        return 'addresses'

    def list(self,clientId,**kwargs):
        """[This endpoint allows you to list all existing addresses for a given client.]

        Args:
            clientId ([str]): [The ID of the client whose addresses are being listed]
        Returns:
            [ComplyCubeCollection]: [A collection of address for the supplied clientId and the page information]
        """
        if clientId is None:
            raise ValueError('clientId must not be None')
        return super(Address, self).list(clientId=clientId,**kwargs)

    def create(self,clientId,line,city,country,**kwargs):
        """[Creates a new address.]

        Args:
            clientId ([str]): [The ID of the client associated with this address.]
            line ([str]): [The line of the client's address. ]
            city ([str]): [The city or town of the client's address.]
            country ([str]): [The country of the client's address. This will be the two-letter country ISO code.]

        Returns:
            [Address]: [An address can be associated with an individual or a company client]
        """
        return super(Address, self).create(clientId=clientId,line=line,city=city,country=country,**kwargs)

    def resource_object(self,**response):
        return address.Address(**response)
