from plexus.msgs import plexus_common_pb2 as _plexus_common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MessageHeader(_message.Message):
    __slots__ = ("topic_name", "payload_type", "cycle_uid", "process_uid", "sequence_number", "envelope_timestamp", "transmit_timestamp")
    TOPIC_NAME_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_TYPE_FIELD_NUMBER: _ClassVar[int]
    CYCLE_UID_FIELD_NUMBER: _ClassVar[int]
    PROCESS_UID_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    ENVELOPE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TRANSMIT_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    topic_name: str
    payload_type: str
    cycle_uid: str
    process_uid: str
    sequence_number: int
    envelope_timestamp: _plexus_common_pb2.Timestamp
    transmit_timestamp: _plexus_common_pb2.Timestamp
    def __init__(self, topic_name: _Optional[str] = ..., payload_type: _Optional[str] = ..., cycle_uid: _Optional[str] = ..., process_uid: _Optional[str] = ..., sequence_number: _Optional[int] = ..., envelope_timestamp: _Optional[_Union[_plexus_common_pb2.Timestamp, _Mapping]] = ..., transmit_timestamp: _Optional[_Union[_plexus_common_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class MessageLandingHeader(_message.Message):
    __slots__ = ("header", "landing_timestamp")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LANDING_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    header: MessageHeader
    landing_timestamp: _plexus_common_pb2.Timestamp
    def __init__(self, header: _Optional[_Union[MessageHeader, _Mapping]] = ..., landing_timestamp: _Optional[_Union[_plexus_common_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class Message(_message.Message):
    __slots__ = ("header", "dependency_headers", "payload")
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DEPENDENCY_HEADERS_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    header: MessageHeader
    dependency_headers: _containers.RepeatedCompositeFieldContainer[MessageLandingHeader]
    payload: bytes
    def __init__(self, header: _Optional[_Union[MessageHeader, _Mapping]] = ..., dependency_headers: _Optional[_Iterable[_Union[MessageLandingHeader, _Mapping]]] = ..., payload: _Optional[bytes] = ...) -> None: ...
