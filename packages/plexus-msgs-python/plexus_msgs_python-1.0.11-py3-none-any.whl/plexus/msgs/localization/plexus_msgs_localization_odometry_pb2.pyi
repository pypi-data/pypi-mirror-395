from plexus.msgs import plexus_common_geom_pb2 as _plexus_common_geom_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Odometry(_message.Message):
    __slots__ = ("pose", "twist")
    POSE_FIELD_NUMBER: _ClassVar[int]
    TWIST_FIELD_NUMBER: _ClassVar[int]
    pose: _plexus_common_geom_pb2.Pose
    twist: _plexus_common_geom_pb2.Twist
    def __init__(self, pose: _Optional[_Union[_plexus_common_geom_pb2.Pose, _Mapping]] = ..., twist: _Optional[_Union[_plexus_common_geom_pb2.Twist, _Mapping]] = ...) -> None: ...
