import json
from complycube.model.complycubeobject import ComplyCubeObject

class Event(ComplyCubeObject):
    def __init__(self, *args, **kwargs):
        self.id = None
        self.type = None
        self.resource_type = None
        self.payload = None
        self.created_at = None
        self.updated_at = None
        super(Event, self).__init__(*args,**kwargs)

class EventVerifier:
    def __init__(self,secret):
        self._secret = secret

    def construct_event(self,response_body, response_signature):
        import hmac
        import hashlib
        val = bytes(self._secret,'utf-8')
        event_signature = hmac.new(val,response_body,hashlib.sha256).hexdigest() 
        given_signature = response_signature
        print(f'event signature - {event_signature}')
        print(f'given signature - {given_signature}')
        if not hmac.compare_digest(event_signature,given_signature):
            raise VertificationError('Invalid signature for event')
        result = json.loads(response_body.decode('utf-8'))
        return Event(**result)

class VertificationError(Exception):
    def __init__(self, value):
         self.value = value
    def __str__(self):
         return repr(self.value)