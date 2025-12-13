from plexus.msgs import plexus_common_pb2 as _plexus_common_pb2
from plexus.msgs import plexus_common_carto_pb2 as _plexus_common_carto_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Positioning(_message.Message):
    __slots__ = ("geo_coord", "world_position", "proj")
    GEO_COORD_FIELD_NUMBER: _ClassVar[int]
    WORLD_POSITION_FIELD_NUMBER: _ClassVar[int]
    PROJ_FIELD_NUMBER: _ClassVar[int]
    geo_coord: _plexus_common_carto_pb2.GeoCoord
    world_position: _plexus_common_pb2.Vector3
    proj: _plexus_common_carto_pb2.CartoProj
    def __init__(self, geo_coord: _Optional[_Union[_plexus_common_carto_pb2.GeoCoord, _Mapping]] = ..., world_position: _Optional[_Union[_plexus_common_pb2.Vector3, _Mapping]] = ..., proj: _Optional[_Union[_plexus_common_carto_pb2.CartoProj, _Mapping]] = ...) -> None: ...
