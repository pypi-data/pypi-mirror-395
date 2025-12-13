from complycube.model.complycubeobject import ComplyCubeObject

class TeamMember(ComplyCubeObject):
    """[A client or check report]

    Attributes:
        id (str): [The ID of the team member.]
        first_name (str): [First name of the team member.]
        last_name (str): [Last name of the team member.]
        role (str): [Role of the team member.]
    """
    def __init__(self, *args, **kwargs):
        self.id = None
        self.first_name = None
        self.last_name = None
        self.role = None
        self.created_at = None
        super(TeamMember, self).__init__(*args,**kwargs)