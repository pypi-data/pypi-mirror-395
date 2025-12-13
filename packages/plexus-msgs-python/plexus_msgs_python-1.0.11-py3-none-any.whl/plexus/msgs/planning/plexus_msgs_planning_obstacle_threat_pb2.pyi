from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ObstacleThreat(_message.Message):
    __slots__ = ("threats",)
    class Threat(_message.Message):
        __slots__ = ("obstacle_uid", "distance", "headway_distance", "lateral_distance", "absolute_speed", "relative_speed", "collision_time", "empirical_collision_time", "risk_flags")
        class RiskFlag(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            RiskNothing: _ClassVar[ObstacleThreat.Threat.RiskFlag]
            RiskFrontApproaching: _ClassVar[ObstacleThreat.Threat.RiskFlag]
            RiskBackApproaching: _ClassVar[ObstacleThreat.Threat.RiskFlag]
            RiskLeftApproaching: _ClassVar[ObstacleThreat.Threat.RiskFlag]
            RiskRightApproaching: _ClassVar[ObstacleThreat.Threat.RiskFlag]
            RiskFrontCollision: _ClassVar[ObstacleThreat.Threat.RiskFlag]
            RiskBackCollision: _ClassVar[ObstacleThreat.Threat.RiskFlag]
            RiskLeftCollision: _ClassVar[ObstacleThreat.Threat.RiskFlag]
            RiskRightCollision: _ClassVar[ObstacleThreat.Threat.RiskFlag]
            RiskLaneKeepSuppression: _ClassVar[ObstacleThreat.Threat.RiskFlag]
            RiskLeftLaneChangeSuppression: _ClassVar[ObstacleThreat.Threat.RiskFlag]
            RiskRightLaneChangeSuppression: _ClassVar[ObstacleThreat.Threat.RiskFlag]
        RiskNothing: ObstacleThreat.Threat.RiskFlag
        RiskFrontApproaching: ObstacleThreat.Threat.RiskFlag
        RiskBackApproaching: ObstacleThreat.Threat.RiskFlag
        RiskLeftApproaching: ObstacleThreat.Threat.RiskFlag
        RiskRightApproaching: ObstacleThreat.Threat.RiskFlag
        RiskFrontCollision: ObstacleThreat.Threat.RiskFlag
        RiskBackCollision: ObstacleThreat.Threat.RiskFlag
        RiskLeftCollision: ObstacleThreat.Threat.RiskFlag
        RiskRightCollision: ObstacleThreat.Threat.RiskFlag
        RiskLaneKeepSuppression: ObstacleThreat.Threat.RiskFlag
        RiskLeftLaneChangeSuppression: ObstacleThreat.Threat.RiskFlag
        RiskRightLaneChangeSuppression: ObstacleThreat.Threat.RiskFlag
        OBSTACLE_UID_FIELD_NUMBER: _ClassVar[int]
        DISTANCE_FIELD_NUMBER: _ClassVar[int]
        HEADWAY_DISTANCE_FIELD_NUMBER: _ClassVar[int]
        LATERAL_DISTANCE_FIELD_NUMBER: _ClassVar[int]
        ABSOLUTE_SPEED_FIELD_NUMBER: _ClassVar[int]
        RELATIVE_SPEED_FIELD_NUMBER: _ClassVar[int]
        COLLISION_TIME_FIELD_NUMBER: _ClassVar[int]
        EMPIRICAL_COLLISION_TIME_FIELD_NUMBER: _ClassVar[int]
        RISK_FLAGS_FIELD_NUMBER: _ClassVar[int]
        obstacle_uid: str
        distance: float
        headway_distance: float
        lateral_distance: float
        absolute_speed: float
        relative_speed: float
        collision_time: float
        empirical_collision_time: float
        risk_flags: int
        def __init__(self, obstacle_uid: _Optional[str] = ..., distance: _Optional[float] = ..., headway_distance: _Optional[float] = ..., lateral_distance: _Optional[float] = ..., absolute_speed: _Optional[float] = ..., relative_speed: _Optional[float] = ..., collision_time: _Optional[float] = ..., empirical_collision_time: _Optional[float] = ..., risk_flags: _Optional[int] = ...) -> None: ...
    THREATS_FIELD_NUMBER: _ClassVar[int]
    threats: _containers.RepeatedCompositeFieldContainer[ObstacleThreat.Threat]
    def __init__(self, threats: _Optional[_Iterable[_Union[ObstacleThreat.Threat, _Mapping]]] = ...) -> None: ...
