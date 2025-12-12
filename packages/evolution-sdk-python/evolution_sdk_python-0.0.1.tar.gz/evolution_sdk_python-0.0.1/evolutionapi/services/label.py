from ..models.label import HandleLabel


class LabelService:
    def __init__(self, client):
        self.client = client

    def find_labels(self, instance_id: str, instance_token: str):
        return self.client.get(f"label/findLabels/{instance_id}", instance_token=instance_token)

    def handle_label(self, instance_id: str, data: HandleLabel, instance_token: str):
        return self.client.post(
            f"label/handleLabel/{instance_id}", data=data.__dict__, instance_token=instance_token
        )
