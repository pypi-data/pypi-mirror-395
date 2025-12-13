from complycube.model.complycubeobject import ComplyCubeObject

class Token(ComplyCubeObject):
    """[Token generate for use with ComplyCube SDKs]

    Attributes:
        token (str): [The JWT token that has been generated for the requested clientId.]
    """
    def __init__(self, *args, **kwargs):
        self.token = None
        super(Token, self).__init__(*args,**kwargs)