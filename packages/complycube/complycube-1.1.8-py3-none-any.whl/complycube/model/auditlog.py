from complycube.model.complycubeobject import ComplyCubeObject

class AuditLog(ComplyCubeObject):
    """[The API allows you to retrieve audit logs for a given client, action, resource, or trigger.]

    Attributes:
        id (str): [The unique identifier for an audit log.]
        member_id (str): [The team member whose actions triggered the audit log creation.]
        resource_type (str): [The type of the audited resource. Valid values include: client, address, document, check]
        resource_id (str): [The id of the audited resource.]
        client_id (str): [The id of the client associated with audited resource.]
        trigger (str): [The event that triggered the audit log creation e.g. updateClient.]
        action (str): [The type of action. Possible values are: create, update, delete]
        diff (array[object]): [The diff between the old and new values of the audited resource.]
        created_at (str): [The date and time when the audit log was created.] 
    """
    def __init__(self, *args, **kwargs):
        self.id = None
        self.member_id = None
        self.resource_type = None
        self.resource_id = None
        self.client_id = None
        self.trigger = None
        self.action = None
        self.diff = None
        self.created_at = None
        super(AuditLog, self).__init__(*args,**kwargs)