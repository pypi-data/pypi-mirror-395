from complycube.model.complycubeobject import ComplyCubeObject

class LiveVideo(ComplyCubeObject):
    """[A Live Video is a video of the client performing recital and movement challenges to ensure liveness. 
    Typically, along with an ID document, they are used to perform Enhanced Identity Checks.]

    Attributes:
        id (str): [The unique identifier for the live video.]
        client_id (str): [The ID of the client associated with this live video.]
        language (str): [The language expected in the live video.]
        challenges ([Challenge]]): [The challenges the client has been issued.]
        created_at (str): [The date and time when the live video was created.]
        updated_at (str): [The date and time when the live video was updated.]
    """
    def __init__(self, *args, **kwargs):
        self.id = None
        self.client_id = None
        self.language = None
        self.challenges = None
        self.createdAt = None
        self.updatedAt = None
        super(LiveVideo, self).__init__(*args,**kwargs)

class Challenge(ComplyCubeObject):
    def __init__(self, *args, **kwargs):
        self.type = None
        self.value = None
        super(Challenge, self).__init__(*args,**kwargs)