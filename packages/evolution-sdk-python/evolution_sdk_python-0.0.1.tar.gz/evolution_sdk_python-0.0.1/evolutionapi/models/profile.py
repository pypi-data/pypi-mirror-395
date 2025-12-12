from typing import Literal


class BaseProfile:
    def __init__(self, **kwargs):
        self.__dict__.update({k: v for k, v in kwargs.items() if v is not None})


class FetchProfile(BaseProfile):
    def __init__(
        self,
        number: str,
    ):
        super().__init__(
            number=number,
        )


class ProfileName(BaseProfile):
    def __init__(
        self,
        name: str,
    ):
        super().__init__(
            name=name,
        )


class ProfileStatus(BaseProfile):
    def __init__(
        self,
        status: str,
    ):
        super().__init__(
            status=status,
        )


class ProfilePicture(BaseProfile):
    def __init__(
        self,
        picture: str,
    ):
        super().__init__(
            picture=picture,
        )


class PrivacySettings(BaseProfile):
    def __init__(
        self,
        readreceipts: Literal["all", "none"],
        profile: Literal["all", "contacts", "contact_blacklist", "none"],
        status: Literal["all", "contacts", "contact_blacklist", "none"],
        online: Literal["all", "match_last_seen"],
        last: Literal["all", "contacts", "contact_blacklist", "none"],
        groupadd: Literal["all", "contacts", "contact_blacklist"],
    ):
        super().__init__(
            readreceipts=readreceipts,
            profile=profile,
            status=status,
            online=online,
            last=last,
            groupadd=groupadd,
        )
