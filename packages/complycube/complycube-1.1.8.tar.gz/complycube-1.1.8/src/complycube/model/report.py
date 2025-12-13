from complycube.model.complycubeobject import ComplyCubeObject

class Report(ComplyCubeObject):
    """[A client or check report]

    Attributes:
        content_type (str): [Type of Base64 content]
        data (str): [Base64 encoded data of Report]
    """
    def __init__(self, *args, **kwargs):
        self.content_type = None
        self.data = None
        super(Report, self).__init__(*args,**kwargs)