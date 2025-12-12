from ..models.presence import PresenceConfig, PresenceStatus


class InstanceOperationsService:
    def __init__(self, client):
        self.client = client

    def connect(self, instance_id: str, instance_token: str):
        return self.client.get(f"instance/connect/{instance_id}", instance_token)

    def restart(self, instance_id: str, instance_token: str):
        return self.client.post(f"instance/restart/{instance_id}", instance_token=instance_token)

    def set_presence(self, instance_id: str, presence: PresenceStatus, instance_token: str):
        config = PresenceConfig(presence)
        return self.client.post(
            f"instance/setPresence/{instance_id}",
            data=config.__dict__,
            instance_token=instance_token,
        )

    def get_connection_state(self, instance_id: str, instance_token: str):
        return self.client.get(f"instance/connectionState/{instance_id}", instance_token)

    def logout(self, instance_id: str, instance_token: str):
        return self.client.delete(f"instance/logout/{instance_id}", instance_token)

    def delete(self, instance_id: str, instance_token: str):
        return self.client.delete(f"instance/delete/{instance_id}", instance_token)
