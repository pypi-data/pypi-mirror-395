from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CanMessages(_message.Message):
    __slots__ = ("messages",)
    class Message(_message.Message):
        __slots__ = ("id", "data")
        ID_FIELD_NUMBER: _ClassVar[int]
        DATA_FIELD_NUMBER: _ClassVar[int]
        id: int
        data: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, id: _Optional[int] = ..., data: _Optional[_Iterable[int]] = ...) -> None: ...
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    messages: _containers.RepeatedCompositeFieldContainer[CanMessages.Message]
    def __init__(self, messages: _Optional[_Iterable[_Union[CanMessages.Message, _Mapping]]] = ...) -> None: ...
