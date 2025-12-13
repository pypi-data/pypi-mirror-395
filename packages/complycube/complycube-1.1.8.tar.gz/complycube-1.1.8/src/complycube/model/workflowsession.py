from complycube.model.complycubeobject import ComplyCubeObject

class WorkflowSession(ComplyCubeObject):
    """[Residential or business addresses can be linked to your client.]

    Attributes:
        id (str): [The unique identifier for an address.]
        client_id (str): [The ID of the client associated with this address.]
        entity_name (str): [The full name of the client. This will be auto-generated.]
        status (str): [Indicates the current status of the workflow session. The session's status evolves as the client progresses through the session.]
        workflow_template_id (str): [The ID of the workflow template used by the workflow session.]
        workflow_template_name (str): [The name of the workflow template.]
        workflow_template_description (str): [The description of the workflow template.]
        workflow_id (str): [The ID of the workflow version used by the workflow session.]
        workflow_version (str): [The workflow version.]
        compliance_policies ([dict]): [The list of compliance policies enabled for the workflow session. ]
        outcome (str): [The overall outcome of the workflow session based on the results of all checks and verifications performed within the session. Possible values include: clear, review, and decline.]
        all_related_checks ([dict]): [The list of checks or verifications executed as part of this workflow session. Also, see the allRelatedCheck object below.]
        policy_assurance ([dict]): [The detailed outcome of all compliance policies as evaluated against the data and checks within the workflow session.]
        tasks ([dict]): [The tasks that define the structure and execution flow of the workflow session.]
        last_completed_task_id (str): [The ID of the most recently completed task within the workflow session.]
        created_at (str): [The date and time when the workflow session was created.]
        completed_at (str): [The date and time when the workflow session was completed.]
        updated_at (str): [The date and time when the workflow session was last updated.]
    """
    def __init__(self, *args, **kwargs):
        self.id = None
        self.client_id = None
        self.entity_name = None
        self.status = None
        self.workflow_template_id = None
        self.workflow_template_name = None
        self.workflow_template_description = None
        self.workflow_id = None
        self.workflow_version = None
        self.compliance_policies = None
        self.outcome = None
        self.all_related_checks = None
        self.policy_assurance = None
        self.tasks = None
        self.last_completed_task_id = None
        self.created_at = None
        self.completed_at = None
        self.updated_at = None
        super(WorkflowSession, self).__init__(*args, **kwargs)

class WorkflowStatus(ComplyCubeObject):
    pass
