from typing import Literal


class BaseLabel:
    def __init__(self, **kwargs):
        self.__dict__.update({k: v for k, v in kwargs.items() if v is not None})


class HandleLabel(BaseLabel):
    def __init__(self, number: str, label_id: str, action: Literal["add", "remove"]):
        if action not in ["add", "remove"]:
            raise ValueError("action deve ser 'add' ou 'remove'")

        super().__init__(number=number, labelId=label_id, action=action)
