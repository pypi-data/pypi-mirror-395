
class ComplyCubeAPIError(Exception):
    def __init__(self,message=None,header=None,code=None):
        super(ComplyCubeAPIError, self).__init__(message)
