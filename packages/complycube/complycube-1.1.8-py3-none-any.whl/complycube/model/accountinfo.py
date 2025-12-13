from complycube.model.complycubeobject import ComplyCubeObject

class AccountInfo(ComplyCubeObject):
    """[The API allows you to retrieve your account info.]

    Attributes:
        username (str): [The administrative username associated with the account]
        plan (str): [The name of the plan you are on.]
        remainingCredit (str): [The remaining credit for a credit based account]
    """
    def __init__(self, *args, **kwargs):
        self.username = None
        self.plan = None
        self.remainingCredit = None
        super(AccountInfo, self).__init__(*args,**kwargs)