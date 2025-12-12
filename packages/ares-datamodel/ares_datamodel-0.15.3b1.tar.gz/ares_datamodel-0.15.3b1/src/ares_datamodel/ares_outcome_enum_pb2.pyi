from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class Outcome(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNSPECIFIED_OUTCOME: _ClassVar[Outcome]
    SUCCESS: _ClassVar[Outcome]
    FAILURE: _ClassVar[Outcome]
    WARNING: _ClassVar[Outcome]
    CANCELED: _ClassVar[Outcome]
UNSPECIFIED_OUTCOME: Outcome
SUCCESS: Outcome
FAILURE: Outcome
WARNING: Outcome
CANCELED: Outcome
