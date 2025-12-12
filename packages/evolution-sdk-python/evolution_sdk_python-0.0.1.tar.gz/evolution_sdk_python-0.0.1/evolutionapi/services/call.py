from ..models.call import FakeCall


class CallService:
    def __init__(self, client):
        self.client = client

    def fake_call(self, instance_id: str, data: FakeCall, instance_token: str):
        return self.client.post(
            f"call/offer/{instance_id}", data=data.__dict__, instance_token=instance_token
        )
