from complycube.api_resources.complycuberesource import ComplyCubeResource
from complycube.api_resource_actions import GetResourceMixin
from complycube.api_resource_actions import DeleteResourceMixin
from complycube.api_resource_actions import ListResourceMixin
from complycube.model import document,livephoto

class LivePhoto(ComplyCubeResource, GetResourceMixin, DeleteResourceMixin, ListResourceMixin):

    @property
    def endpoint(self):
        return 'livePhotos' 

    def list(self,clientId,**kwargs):
        if clientId is None:
            raise ValueError('clientId must not be None')
        return super(LivePhoto, self).list(clientId=clientId,**kwargs)

    def upload(self,clientId,data,performLivenessCheck=True):
        """[Uploads a new live photo.
        The live photo image must be either in JPG or PNG format. 
        The size must be between 34 KB and 4 MB.]

        Args:
            id ([str]): [The ID of the client.]
            data ([str]): [Base64 encoded image of the client.]
            performLivenessCheck ([bool]): [Flag to set if a liveness check is performed on upload.]
        
        Returns:
            [Image]: [Image uploaded metadata]
        """
        response , _  = self.client._execute_api_request(   self.endpoint,
                                                            'POST',
                                                            clientId=clientId,
                                                            data=data,
                                                            performLivenessCheck=performLivenessCheck)
        return document.Image(**response)

    def download(self,photo_id):
        """[Downloads an existing live photo.]

        Returns:
            [Image]: [Live Photo with Base64 encoded image data]
        """
        url = '%s/%s/download' % (self.endpoint, photo_id)
        response , _  = self.client._execute_api_request(url,'GET')
        return document.Image(**response)

    def deleteImage(self,photo_id):
        """[Deletes an existing live photo.
        You will not be able to delete a live photo once used to perform a check.]

        Returns:
            [Image]: [Live Photo with Base64 encoded image data]
        """
        url = '%s/%s' % (self.endpoint, photo_id)
        self.client._execute_api_request(url,'DELETE')
        return 

    def resource_object(self,**response):
        return livephoto.LivePhoto(**response)