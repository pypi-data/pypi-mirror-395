from google.protobuf import descriptor_pb2 as _descriptor_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class LoggingLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LoggingLevelUnspecified: _ClassVar[LoggingLevel]
    LoggingLevelTrace: _ClassVar[LoggingLevel]
    LoggingLevelDebug: _ClassVar[LoggingLevel]
    LoggingLevelInfo: _ClassVar[LoggingLevel]
    LoggingLevelWarning: _ClassVar[LoggingLevel]
    LoggingLevelError: _ClassVar[LoggingLevel]
    LoggingLevelCritical: _ClassVar[LoggingLevel]
LoggingLevelUnspecified: LoggingLevel
LoggingLevelTrace: LoggingLevel
LoggingLevelDebug: LoggingLevel
LoggingLevelInfo: LoggingLevel
LoggingLevelWarning: LoggingLevel
LoggingLevelError: LoggingLevel
LoggingLevelCritical: LoggingLevel
OMITTED_FIELD_NUMBER: _ClassVar[int]
omitted: _descriptor.FieldDescriptor
LOGGING_LEVEL_FIELD_NUMBER: _ClassVar[int]
logging_level: _descriptor.FieldDescriptor
