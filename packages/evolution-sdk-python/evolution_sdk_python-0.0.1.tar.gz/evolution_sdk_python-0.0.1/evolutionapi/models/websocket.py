from dataclasses import dataclass
from typing import List


@dataclass
class WebSocketConfig:
    enabled: bool
    events: List[str]

    def __init__(self, enabled: bool, events: List[str]):
        self.enabled = enabled
        self.events = events


@dataclass
class WebSocketInfo:
    enabled: bool
    events: List[str]

    def __init__(self, **kwargs):
        self.enabled = kwargs.get("enabled", False)
        self.events = kwargs.get("events", [])
