class InstanceService:
    def __init__(self, client):
        self.client = client

    def fetch_instances(self):
        return self.client.get("instance/fetchInstances")

    def create_instance(self, config):
        return self.client.post("instance/create", data=config.__dict__)
