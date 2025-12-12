import ares_outcome_enum_pb2 as _ares_outcome_enum_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Analysis(_message.Message):
    __slots__ = ("result", "analysis_outcome", "error_string")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    ANALYSIS_OUTCOME_FIELD_NUMBER: _ClassVar[int]
    ERROR_STRING_FIELD_NUMBER: _ClassVar[int]
    result: float
    analysis_outcome: _ares_outcome_enum_pb2.Outcome
    error_string: str
    def __init__(self, result: _Optional[float] = ..., analysis_outcome: _Optional[_Union[_ares_outcome_enum_pb2.Outcome, str]] = ..., error_string: _Optional[str] = ...) -> None: ...
