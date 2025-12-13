from complycube.model import riskprofile
from complycube.api_resource_actions import GetResourceMixin
from complycube.api_resource_actions import CreateResourceMixin
from complycube.api_resource_actions import UpdateResourceMixin
from complycube.api_resource_actions import DeleteResourceMixin
from complycube.api_resource_actions import ListResourceMixin
from complycube.api_resources.complycuberesource import ComplyCubeResource

class RiskProfile(ComplyCubeResource, GetResourceMixin):

    @property
    def endpoint(self):
        return 'clients' 

    def get(self,id,**kwargs):
        return super(RiskProfile, self).get('%s/riskProfile' % (id))

    def resource_object(self,**response):
        return riskprofile.RiskProfile(**response)
