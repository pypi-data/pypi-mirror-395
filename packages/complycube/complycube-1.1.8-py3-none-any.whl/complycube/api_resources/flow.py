from complycube.model import flow
from complycube.api_resource_actions import CreateResourceMixin
from complycube.api_resources.complycuberesource import ComplyCubeResource

class Flow(ComplyCubeResource, CreateResourceMixin):

    @property
    def endpoint(self):
        return 'flow/sessions' 

    def resource_object(self,**response):
        return flow.FlowSession(**response)
