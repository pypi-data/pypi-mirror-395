from complycube.model import teammember
from complycube.api_resource_actions import GetResourceMixin
from complycube.api_resource_actions import ListResourceMixin
from complycube.api_resources.complycuberesource import ComplyCubeResource

class TeamMember(ComplyCubeResource, GetResourceMixin, ListResourceMixin):

    @property
    def endpoint(self):
        return 'teamMembers' 

    def get(self,id,**kwargs):
        """[This endpoint allows you to retrieve a specific team member.]

        Args:
            id ([str]): [The ID of the team member.]
            
        Returns:
            [TeamMember]: [Returns the requested team members details.]
        """
        return super(TeamMember, self).get(id,**kwargs)

    def resource_object(self,**response):
        return teammember.TeamMember(**response)
