from enum import Enum
from typing import List, Optional, Union


class MediaType(Enum):
    IMAGE = "image"
    VIDEO = "video"
    DOCUMENT = "document"


class StatusType(Enum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"


class FontType(Enum):
    SERIF = 1
    NORICAN_REGULAR = 2
    BRYNDAN_WRITE = 3
    BEBASNEUE_REGULAR = 4
    OSWALD_HEAVY = 5


class BaseMessage:
    def __init__(self, **kwargs):
        self.__dict__.update({k: v for k, v in kwargs.items() if v is not None})


class QuotedMessage(BaseMessage):
    def __init__(self, key: dict, message: Optional[dict] = None):
        super().__init__(key=key, message=message)


class TextMessage(BaseMessage):
    def __init__(
        self,
        number: str,
        text: str,
        delay: Optional[int] = None,
        quoted: Optional[QuotedMessage] = None,
        linkPreview: Optional[bool] = None,
        mentionsEveryOne: Optional[bool] = None,
        mentioned: Optional[List[str]] = None,
    ):
        super().__init__(
            number=number,
            text=text,
            delay=delay,
            quoted=quoted.__dict__ if quoted else None,
            linkPreview=linkPreview,
            mentionsEveryOne=mentionsEveryOne,
            mentioned=mentioned,
        )


class MediaMessage(BaseMessage):
    def __init__(
        self,
        number: str,
        media: dict = None,
        mediatype: Optional[str] = None,
        caption: str = None,
        mimetype: str = None,
        fileName: str = None,
        delay: Optional[Union[int, float, str]] = None,
        quoted: Optional[QuotedMessage] = None,
        mentionsEveryOne: Optional[bool] = None,
        mentioned: Optional[List[str]] = None,
    ):
        data = {
            "number": number,
            "mediatype": mediatype,
            "caption": caption,
            "mimetype": mimetype,
            "fileName": fileName,
            "quoted": quoted.__dict__ if quoted else None,
            "mentionsEveryOne": mentionsEveryOne,
            "mentioned": mentioned,
        }

        if delay is not None:
            data["delay"] = delay

        if media and media != {}:
            data["media"] = media

        super().__init__(**{k: v for k, v in data.items() if v is not None})


class StatusMessage(BaseMessage):
    def __init__(
        self,
        type: StatusType,
        content: str,
        caption: Optional[str] = None,
        backgroundColor: Optional[str] = None,
        font: Optional[FontType] = None,
        allContacts: bool = False,
        statusJidList: Optional[List[str]] = None,
    ):
        super().__init__(
            type=type.value,
            content=content,
            caption=caption,
            backgroundColor=backgroundColor,
            font=font.value if font else None,
            allContacts=allContacts,
            statusJidList=statusJidList,
        )


class LocationMessage(BaseMessage):
    def __init__(
        self,
        number: str,
        name: str,
        address: str,
        latitude: float,
        longitude: float,
        delay: Optional[int] = None,
        quoted: Optional[QuotedMessage] = None,
    ):
        super().__init__(
            number=number,
            name=name,
            address=address,
            latitude=latitude,
            longitude=longitude,
            delay=delay,
            quoted=quoted.__dict__ if quoted else None,
        )


class Contact(BaseMessage):
    def __init__(
        self,
        fullName: str,
        wuid: str,
        phoneNumber: str,
        organization: Optional[str] = None,
        email: Optional[str] = None,
        url: Optional[str] = None,
    ):
        super().__init__(
            fullName=fullName,
            wuid=wuid,
            phoneNumber=phoneNumber,
            organization=organization,
            email=email,
            url=url,
        )


class ContactMessage(BaseMessage):
    def __init__(self, number: str, contact: List[Contact]):
        super().__init__(number=number, contact=[c.__dict__ for c in contact])


class ReactionMessage(BaseMessage):
    def __init__(self, key: dict, reaction: str):
        super().__init__(key=key, reaction=reaction)


class PollMessage(BaseMessage):
    def __init__(
        self,
        number: str,
        name: str,
        selectableCount: int,
        values: List[str],
        delay: Optional[int] = None,
        quoted: Optional[QuotedMessage] = None,
    ):
        super().__init__(
            number=number,
            name=name,
            selectableCount=selectableCount,
            values=values,
            delay=delay,
            quoted=quoted.__dict__ if quoted else None,
        )


class ListRow(BaseMessage):
    def __init__(self, title: str, description: str, rowId: str):
        super().__init__(title=title, description=description, rowId=rowId)


class ListSection(BaseMessage):
    def __init__(self, title: str, rows: List[ListRow]):
        super().__init__(title=title, rows=[r.__dict__ for r in rows])


class ListMessage(BaseMessage):
    def __init__(
        self,
        number: str,
        title: str,
        description: str,
        buttonText: str,
        footerText: str,
        sections: List[ListSection],
        delay: Optional[int] = None,
        quoted: Optional[QuotedMessage] = None,
    ):
        super().__init__(
            number=number,
            title=title,
            description=description,
            buttonText=buttonText,
            footerText=footerText,
            sections=[s.__dict__ for s in sections],
            delay=delay,
            quoted=quoted.__dict__ if quoted else None,
        )


class Button(BaseMessage):
    def __init__(
        self,
        type: str,
        displayText: str,
        id: Optional[str] = None,
        copyCode: Optional[str] = None,
        url: Optional[str] = None,
        phoneNumber: Optional[str] = None,
        currency: Optional[str] = None,
        name: Optional[str] = None,
        keyType: Optional[str] = None,
        key: Optional[str] = None,
    ):
        super().__init__(
            type=type,
            displayText=displayText,
            id=id,
            copyCode=copyCode,
            url=url,
            phoneNumber=phoneNumber,
            currency=currency,
            name=name,
            keyType=keyType,
            key=key,
        )


class ButtonMessage(BaseMessage):
    def __init__(
        self,
        number: str,
        title: str,
        description: str,
        footer: str,
        buttons: List[Button],
        delay: Optional[int] = None,
        quoted: Optional[QuotedMessage] = None,
    ):
        super().__init__(
            number=number,
            title=title,
            description=description,
            footer=footer,
            buttons=[b.__dict__ for b in buttons],
            delay=delay,
            quoted=quoted.__dict__ if quoted else None,
        )
