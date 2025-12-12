class BaseCall:
    def __init__(self, **kwargs):
        self.__dict__.update({k: v for k, v in kwargs.items() if v is not None})


class FakeCall(BaseCall):
    def __init__(self, number: str, isVideo: bool, callDuration: int):
        super().__init__(number=number, isVideo=isVideo, callDuration=callDuration)
