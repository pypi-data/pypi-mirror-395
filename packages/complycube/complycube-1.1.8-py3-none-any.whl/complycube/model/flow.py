from complycube.model.complycubeobject import ComplyCubeObject

class FlowSession(ComplyCubeObject):
    """[Flow hosted solution session for client onboarding]

    Attributes:
        redirect_url (str): [The unique url generated for the client to complete on-boarding.]
    """
    def __init__(self, *args, **kwargs):
        self.redirect_url = None
        super(FlowSession, self).__init__(*args,**kwargs)