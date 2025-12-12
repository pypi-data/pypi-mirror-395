from enum import Enum


class PresenceStatus(Enum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"


class PresenceConfig:
    def __init__(self, presence: PresenceStatus):
        self.presence = presence.value
