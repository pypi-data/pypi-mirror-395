from complycube.model import document
from complycube.api_resource_actions import GetResourceMixin
from complycube.api_resource_actions import CreateResourceMixin
from complycube.api_resource_actions import UpdateResourceMixin
from complycube.api_resource_actions import DeleteResourceMixin
from complycube.api_resource_actions import ListResourceMixin
from complycube.api_resources.complycuberesource import ComplyCubeResource
 

class Document(ComplyCubeResource, GetResourceMixin, CreateResourceMixin, UpdateResourceMixin, DeleteResourceMixin, ListResourceMixin):

    @property
    def endpoint(self):
        return 'documents' 

    def auto_list(self,clientId,**kwargs):
        """[Provides a generator to list all existing documents for a given client.
                The documents are returned sorted by creation date, with the most recent documents appearing first.]

        Returns:
            [Generator]: [Generator for a collection of documents and fetched page information]
        """
        if clientId is None:
            raise ValueError('client_id must not be None')
        return super(Document, self).auto_list(clientId=clientId,**kwargs)

    def list(self,clientId,**kwargs):
        """[This endpoint allows you to list all existing documents for a given client.
                The documents are returned sorted by creation date, with the most recent documents appearing first.]

        Returns:
            [ComplyCubeCollection]: [A collection of documents and fetched page information]
        """
        if clientId is None:
            raise ValueError('client_id must not be None')
        return super(Document, self).list(clientId=clientId,**kwargs)

    def upload(self,document_id,document_side,fileName,data):
        """[Associates an image attachment to an existing document.
                The images must be either in JPG, PNG, or PDF format.  Each side of the document must be between 34 KB and 4 MB.]

        Returns:
            [Image]: [The metadata of the uploaded image]
        """
        url = '%s/%s/upload/%s' % (self.endpoint, document_id,document_side)
        response , _  = self.client._execute_api_request(url,'POST',fileName=fileName,data=data)
        return document.Image(**response)

    def download(self,document_id,document_side):
        """[Downloads an existing image attachment.]

        Returns:
            [Image]: [Image object with Base64 encoded data]
        """
        url = '%s/%s/download/%s' % (self.endpoint, document_id,document_side)
        response , _  = self.client._execute_api_request(url,'GET')
        return document.Image(**response)

    def deleteImage(self,document_id,document_side):
        """[Downloads an existing image attachment.]

        Returns:
            [Image]: [Image object with Base64 encoded data]
        """
        url = '%s/%s/%s' % (self.endpoint, document_id,document_side)
        self.client._execute_api_request(url,'DELETE')
        return 

    def create(self,clientId,type,**kwargs):
        """[Creates a new document.]

        Returns:
            [Document]: [The created Document.]
        """
        return super(Document, self).create(clientId=clientId,type=type,**kwargs)

    def resource_object(self,**response):
        return document.Document(**response)