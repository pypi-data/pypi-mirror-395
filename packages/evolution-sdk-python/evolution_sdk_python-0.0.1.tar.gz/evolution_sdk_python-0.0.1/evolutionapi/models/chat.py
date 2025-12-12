from typing import Any, Dict, List, Optional


class BaseChat:
    def __init__(self, **kwargs):
        self.__dict__.update({k: v for k, v in kwargs.items() if v is not None})


class CheckIsWhatsappNumber(BaseChat):
    def __init__(self, numbers: List[str]):
        super().__init__(numbers=numbers)


class MessageKey:
    def __init__(self, remote_jid: str, from_me: bool, id: str, participant: Optional[str] = None):
        self.remoteJid = remote_jid
        self.fromMe = from_me
        self.id = id
        self.participant = participant


class ReadMessage:
    def __init__(self, remote_jid: str, from_me: bool, id: str):
        self.remoteJid = remote_jid
        self.fromMe = from_me
        self.id = id


class ArchiveChat:
    def __init__(self, last_message: Dict[str, Any], chat: str, archive: bool):
        self.lastMessage = last_message
        self.chat = chat
        self.archive = archive


class UnreadChat:
    def __init__(self, last_message: Dict[str, Any], chat: str):
        self.lastMessage = last_message
        self.chat = chat


class ProfilePicture:
    def __init__(self, number: str):
        self.number = number


class MediaMessage:
    def __init__(self, message: Dict[str, Any], convert_to_mp4: bool = False):
        self.message = message
        self.convertToMp4 = convert_to_mp4


class UpdateMessage:
    def __init__(self, number: str, key: Dict[str, Any], text: str):
        self.number = number
        self.key = key
        self.text = text


class Presence:
    def __init__(self, number: str, delay: int, presence: str):
        self.number = number
        self.delay = delay
        self.presence = presence
