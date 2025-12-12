from typing import Dict, List


class WebhookConfig:
    def __init__(
        self,
        url: str = None,
        byEvents: bool = False,
        base64: bool = True,
        headers: Dict = None,
        events: List[str] = None,
    ):
        self.url = url
        self.byEvents = byEvents
        self.base64 = base64
        self.headers = headers
        self.events = events


class EventsConfig:
    def __init__(self, enabled: bool = True, events: List[str] = None):
        self.enabled = enabled
        self.events = events


class ChatwootConfig:
    def __init__(
        self,
        accountId: str = None,
        token: str = None,
        url: str = None,
        signMsg: bool = True,
        reopenConversation: bool = True,
        conversationPending: bool = False,
        importContacts: bool = True,
        nameInbox: str = "evolution",
        mergeBrazilContacts: bool = True,
        importMessages: bool = True,
        daysLimitImportMessages: int = 3,
        organization: str = "Evolution Bot",
        logo: str = "https://evolution-api.com/files/evolution-api-favicon.png",
    ):
        self.chatwootAccountId = accountId
        self.chatwootToken = token
        self.chatwootUrl = url
        self.chatwootSignMsg = signMsg
        self.chatwootReopenConversation = reopenConversation
        self.chatwootConversationPending = conversationPending
        self.chatwootImportContacts = importContacts
        self.chatwootNameInbox = nameInbox
        self.chatwootMergeBrazilContacts = mergeBrazilContacts
        self.chatwootImportMessages = importMessages
        self.chatwootDaysLimitImportMessages = daysLimitImportMessages
        self.chatwootOrganization = organization
        self.chatwootLogo = logo


class InstanceConfig:
    def __init__(
        self,
        instanceName: str,
        integration: str = None,
        token: str = None,
        number: str = None,
        qrcode: bool = None,
        rejectCall: bool = None,
        msgCall: str = None,
        groupsIgnore: bool = None,
        alwaysOnline: bool = None,
        readMessages: bool = None,
        readStatus: bool = None,
        syncFullHistory: bool = None,
    ):
        self.__dict__["instanceName"] = instanceName

        for key, value in locals().items():
            if key != "self" and key != "instanceName" and value is not None:
                self.__dict__[key] = value
