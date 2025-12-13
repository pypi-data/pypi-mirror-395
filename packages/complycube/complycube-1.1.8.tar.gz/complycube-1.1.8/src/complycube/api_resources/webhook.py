from complycube.model import webhook
from complycube.api_resource_actions import GetResourceMixin
from complycube.api_resource_actions import CreateResourceMixin
from complycube.api_resource_actions import UpdateResourceMixin
from complycube.api_resource_actions import DeleteResourceMixin
from complycube.api_resource_actions import ListResourceMixin
from complycube.api_resources.complycuberesource import ComplyCubeResource

class Webhook(ComplyCubeResource, GetResourceMixin, CreateResourceMixin, UpdateResourceMixin, DeleteResourceMixin, ListResourceMixin):

    @property
    def endpoint(self):
        return 'webhooks' 

    def create(self,url,enabled,events,**kwargs):
        """[Creates a new webhook]

        Args:
            url ([str]): [Returns the webhook endpoint object with the secret field populated.]
            enabled ([bool]): [Determines whether the webhook should be active.]
            events ([list]): [The list of event types which which the endpoint is subscribed for.]

        Returns:
            [Webhook]: [Returns a webhook object with the secret field populated.]
        """
        return super(Webhook, self).create(url=url,enabled=enabled,events=events,**kwargs)

    def resource_object(self,**response):
        return webhook.Webhook(**response)
