from complycube.model.complycubeobject import ComplyCubeObject

class Webhook(ComplyCubeObject):
    """[ComplyCube uses webhooks to notify your application when an event happens in your account. 
        Webhooks are particularly useful for asynchronous events like when a check has concluded.]

    Attributes:
        id (str): [The unique identifier for the webhook.]
        description (str): [n optional description of what the wehbook is used for.]
        url (str): [The URL of the webhook endpoint - must be HTTPS.]
        enabled (bool): [Determines if the webhook should be active.]
        events (list of str): [The list of events types enabled for this endpoint. [’*’] indicates that all events are enabled, except those that require explicit selection.]
        secret (str): [The endpoint’s secret, used to generate webhook signatures. Only returned at creation.]
        created_at (str): [The date and time when the webhook was created.]
        updated_at (str): [The date and time when the webhook was updated.]
    """
    def __init__(self, *args, **kwargs):
        self.id = None
        self.description = None
        self.url = None
        self.enabled = None
        self.events = None
        self.secret = None
        self.createdAt = None
        self.updatedAt = None
        super(Webhook, self).__init__(*args,**kwargs)

class Event(ComplyCubeObject):
    """[An action or change in data that generates notifications. Webhooks can be used to create alerts that trigger for these events]

    Attributes:
        id (str): [The unique identifier for the event, which a webhook listener can use bypass notification processing on a webhook notification that is sent more than once.]
        type (str): [The event type that initiated the event e.g. check.completed.]
        resource_type (str): [The type of the object contained within the payload e.g. check object.]
        payload (object): [The object associated with this event.]
        created_at (str): [The date and time when the event was created.]
    """
    def __init__(self, *args, **kwargs):
        self.id = None
        self.type = None
        self.resource_type = None
        self.payload = None
        super(Event, self).__init__(*args,**kwargs)