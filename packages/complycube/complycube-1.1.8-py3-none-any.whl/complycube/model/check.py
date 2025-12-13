from complycube.model.complycubeobject import ComplyCubeObject

class Outcome(ComplyCubeObject):
    def __init__(self, *args, **kwargs):
        self.outcome = None
        super(Outcome, self).__init__(*args,**kwargs)
        
class Check(ComplyCubeObject):
    """[Checks enable you to run various types of verifications against your clients. You can perform the following types of checks:
            1. Standard AML Screening
            2. Extensive AML Screening
            3. Document Check
            4. Identity Check]

    Attributes:
        id (str): [The unique identifier for an address.]
        client_id (str): [The ID of the client associated with this address.]
        document_id (str): [The ID of the document. This is expected when the type of check is document_check or identity_check.]
        live_photo_id (str): [The ID of the live photo. This is expected when the type of check is identity_check.]
        entity_name (str): [The full name of the client. This will be auto-generated.]
        type (str): [The type of address. Valid values are:
                        1. standard_screening_check (more info)
                        2. extensive_screening_check (more info)
                        3. document_check (more info)
                        4. identity_check(more info)]
        status (str): [The status of the check. As checks are asynchronous, their status will change as their state transitions. Values can be:
                            pending - the status on initiation.
                            complete - the status upon completion.
                            failed - the status if a check fails.]
        result (object): [The result of the check. This will only have a value when a check is complete. The content will depend on the type of check.]
        created_at (str): [The date and time when the check was created.]
        updated_at (str): [The date and time when the check was updated.]
    """
    def __init__(self, *args, **kwargs):
        self.id = None
        self.client_id = None
        self.document_id = None
        self.live_photo_id = None
        self.entity_name = None
        self.type = None
        self.enable_monitoring = None
        self.status = None
        self.result = None
        super(Check, self).__init__(*args,**kwargs)