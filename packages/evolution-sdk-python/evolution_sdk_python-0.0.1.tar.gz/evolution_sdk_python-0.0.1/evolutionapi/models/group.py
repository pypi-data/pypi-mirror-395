from dataclasses import dataclass
from typing import List, Literal, Optional


@dataclass
class CreateGroup:
    subject: str
    participants: List[str]
    description: Optional[str] = None


@dataclass
class GroupPicture:
    image: str


@dataclass
class GroupSubject:
    subject: str


@dataclass
class GroupDescription:
    description: str


@dataclass
class GroupInvite:
    groupJid: str
    description: str
    numbers: List[str]


@dataclass
class UpdateParticipant:
    action: Literal["add", "remove", "promote", "demote"]
    participants: List[str]


@dataclass
class UpdateSetting:
    action: Literal["announcement", "not_announcement", "locked", "unlocked"]


@dataclass
class ToggleEphemeral:
    expiration: int
