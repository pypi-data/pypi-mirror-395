from complycube.api_resources.complycuberesource import ComplyCubeResource
from complycube.api_resource_actions import GetResourceMixin
from complycube.api_resource_actions import DeleteResourceMixin
from complycube.api_resource_actions import ListResourceMixin
from complycube.model import livevideo

class LiveVideo(ComplyCubeResource, GetResourceMixin, DeleteResourceMixin, ListResourceMixin):

    @property
    def endpoint(self):
        return 'liveVideos' 

    def list(self,clientId,**kwargs):
        if clientId is None:
            raise ValueError('clientId must not be None')
        return super(LiveVideo, self).list(clientId=clientId,**kwargs)

    def resource_object(self,**response):
        return livevideo.LiveVideo(**response)