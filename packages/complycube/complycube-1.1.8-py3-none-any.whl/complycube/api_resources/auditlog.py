from complycube.model import auditlog
from complycube.api_resource_actions import GetResourceMixin
from complycube.api_resource_actions import ListResourceMixin
from complycube.api_resources.complycuberesource import ComplyCubeResource

class AuditLog(ComplyCubeResource, GetResourceMixin, ListResourceMixin):

    @property
    def endpoint(self):
        return 'auditLogs' 

    def get(self,id,**kwargs):
        """[This endpoint allows you to retrieve a specific audit log.]

        Args:
            id ([str]): [The ID of the audit log.]
            
        Returns:
            [AuditLog]: [Returns the audit log.]
        """
        return super(AuditLog, self).get(id,**kwargs)

    def resource_object(self,**response):
        return auditlog.AuditLog(**response)
