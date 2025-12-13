from complycube.model import workflowsession
from complycube.api_resource_actions import GetResourceMixin
from complycube.api_resource_actions import ListResourceMixin
from complycube.api_resources.complycuberesource import ComplyCubeResource

class WorkflowSession(ComplyCubeResource, GetResourceMixin, ListResourceMixin):
    
    @property
    def endpoint(self):
        return 'workflowSessions'

    def complete(self, workflow_session_id, **params):
        url = "{endpoint}/{id}/complete".format(
            endpoint=self.endpoint,
            id=workflow_session_id
        )
        response , _  = self.client._execute_api_request(   url,
                                                            'POST')
        return workflowsession.WorkflowStatus(**response)
    
    def resource_object(self,**response):
        return workflowsession.WorkflowSession(**response)
