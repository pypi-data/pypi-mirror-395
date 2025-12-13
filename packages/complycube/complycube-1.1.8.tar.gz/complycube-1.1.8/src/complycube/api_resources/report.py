from complycube.model import report
from complycube.api_resource_actions import CreateResourceMixin
from complycube.api_resources.complycuberesource import ComplyCubeResource

class Report(ComplyCubeResource, CreateResourceMixin):

    @property
    def endpoint(self):
        return 'reports' 

    def generate_client_report(self,client_id):
        """[Generates a client Report]

        Args:
            client_id ([str]): [The ID of the client]

        Returns:
            [Report]: [Returns a Base64 encoded Report]
        """
        url = '%s?clientId=%s' % (self.endpoint, client_id)
        response , _ = self.client._execute_api_request(url,'GET')
        return report.Report(**response)


    def generate_check_report(self,check_id):
        """[Generates a check Report]

        Args:
            check_id ([str]): [The ID of the check]

        Returns:
            [Report]: [Returns a Base64 encoded Report]
        """
        url = '%s?checkId=%s' % (self.endpoint, check_id)
        response , _ = self.client._execute_api_request(url,'GET')
        return report.Report(**response)


    def resource_object(self,**response):
        return report.Report(**response)
