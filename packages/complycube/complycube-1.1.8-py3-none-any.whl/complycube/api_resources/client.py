from complycube.model import client
from complycube.api_resource_actions import GetResourceMixin
from complycube.api_resource_actions import CreateResourceMixin
from complycube.api_resource_actions import UpdateResourceMixin
from complycube.api_resource_actions import DeleteResourceMixin
from complycube.api_resource_actions import ListResourceMixin
from complycube.api_resources.complycuberesource import ComplyCubeResource

class Client(ComplyCubeResource, GetResourceMixin, CreateResourceMixin, UpdateResourceMixin, DeleteResourceMixin, ListResourceMixin):

    @property
    def endpoint(self):
        return 'clients' 
    
    def list(self,**kwargs):
        """[This endpoint allows you to list all existing clients.
                The clients are returned sorted by creation date, with the most recent clients appearing first.]

        Returns:
            [ComplyCubeCollection]: [A collection of clients and fetched page information]
        """
        return super(Client,self).list(**kwargs)
        
    def create(self,type,email,**kwargs):
        """[Creates a new client.]

        Args:
            type ([str]): [The type of client. Valid values are:
                                    1. person 
                                    2. company]
            email ([str]): [The client's email address.]
            **kwargs: [Key value pairs of optional client attributes.
                        Note 
                            if type = Person you must provide a personDetails key
                            if type = Company you must provide a companyDetails key
                        ]

        Returns:
            [Client]: [The client object of the newly created client]
        """
        return super(Client, self).create(type=type,email=email,**kwargs)

    def resource_object(self,**response):
        return client.Client(**response)
