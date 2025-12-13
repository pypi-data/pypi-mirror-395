from plexus.msgs import plexus_common_pb2 as _plexus_common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GeoCoord(_message.Message):
    __slots__ = ("latitude", "longitude", "elevation")
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    ELEVATION_FIELD_NUMBER: _ClassVar[int]
    latitude: float
    longitude: float
    elevation: float
    def __init__(self, latitude: _Optional[float] = ..., longitude: _Optional[float] = ..., elevation: _Optional[float] = ...) -> None: ...

class CartoProj(_message.Message):
    __slots__ = ("method", "parameters")
    METHOD_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    method: str
    parameters: _containers.RepeatedCompositeFieldContainer[_plexus_common_pb2.KeyValue]
    def __init__(self, method: _Optional[str] = ..., parameters: _Optional[_Iterable[_Union[_plexus_common_pb2.KeyValue, _Mapping]]] = ...) -> None: ...
