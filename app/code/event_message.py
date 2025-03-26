import json


class EventMessage(object):
    test_id = '0'
    name = ''
    payload = {}

    def __init__(self):
        self.test_id = '0'
        self.name = ''
        self.payload = {}

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value):
        self._name = value.lower()

    @property
    def test_id(self) -> int:
        return self._test_id

    @test_id.setter
    def test_id(self, value):
        self._test_id = int(value)

    @property
    def payload(self) -> dict:
        return self._payload

    @payload.setter
    def payload(self, value):
        self._payload = value

    def create_message_to_send(self):
        this_message = dict(test_id=str(self.test_id), event=self.name)
        if self.payload:
            this_message['payload'] = self.payload
        return this_message
    
    def extract_consumed_message_information(self, consumed_message):
        body_dict = json.loads(consumed_message)
        self.test_id = body_dict.get('test_id', 0)
        self.name = body_dict.get('event', '')
        self.payload = body_dict.get('payload', {})
        return self
