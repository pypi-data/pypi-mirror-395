from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RequestMetadata(_message.Message):
    __slots__ = ("system_name", "campaign_name", "campaign_id", "experiment_id")
    SYSTEM_NAME_FIELD_NUMBER: _ClassVar[int]
    CAMPAIGN_NAME_FIELD_NUMBER: _ClassVar[int]
    CAMPAIGN_ID_FIELD_NUMBER: _ClassVar[int]
    EXPERIMENT_ID_FIELD_NUMBER: _ClassVar[int]
    system_name: str
    campaign_name: str
    campaign_id: str
    experiment_id: str
    def __init__(self, system_name: _Optional[str] = ..., campaign_name: _Optional[str] = ..., campaign_id: _Optional[str] = ..., experiment_id: _Optional[str] = ...) -> None: ...
