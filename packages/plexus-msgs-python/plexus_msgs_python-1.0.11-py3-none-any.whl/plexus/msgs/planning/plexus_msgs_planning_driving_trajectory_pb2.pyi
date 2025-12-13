from plexus.msgs import plexus_common_geom_pb2 as _plexus_common_geom_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DrivingTrajectory(_message.Message):
    __slots__ = ("trajectory",)
    class Trajectory(_message.Message):
        __slots__ = ("world_polygon3",)
        WORLD_POLYGON3_FIELD_NUMBER: _ClassVar[int]
        world_polygon3: _plexus_common_geom_pb2.Polygon3
        def __init__(self, world_polygon3: _Optional[_Union[_plexus_common_geom_pb2.Polygon3, _Mapping]] = ...) -> None: ...
    TRAJECTORY_FIELD_NUMBER: _ClassVar[int]
    trajectory: DrivingTrajectory.Trajectory
    def __init__(self, trajectory: _Optional[_Union[DrivingTrajectory.Trajectory, _Mapping]] = ...) -> None: ...
