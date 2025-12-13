from plexus.msgs import plexus_common_pb2 as _plexus_common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NavigationInfo(_message.Message):
    __slots__ = ("road_profile", "expressway_profile", "restriction", "routing_checkpoints")
    class RoadProfile(_message.Message):
        __slots__ = ("road_class", "road_name", "direction_sites")
        class RoadClassEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            RoadClassUnknown: _ClassVar[NavigationInfo.RoadProfile.RoadClassEnum]
            RoadClassExpressway: _ClassVar[NavigationInfo.RoadProfile.RoadClassEnum]
            RoadClassExpresswayLink: _ClassVar[NavigationInfo.RoadProfile.RoadClassEnum]
            RoadClassTrunk: _ClassVar[NavigationInfo.RoadProfile.RoadClassEnum]
            RoadClassTrunkLink: _ClassVar[NavigationInfo.RoadProfile.RoadClassEnum]
            RoadClassPrimary: _ClassVar[NavigationInfo.RoadProfile.RoadClassEnum]
            RoadClassPrimaryLink: _ClassVar[NavigationInfo.RoadProfile.RoadClassEnum]
            RoadClassSecondary: _ClassVar[NavigationInfo.RoadProfile.RoadClassEnum]
            RoadClassSecondaryLink: _ClassVar[NavigationInfo.RoadProfile.RoadClassEnum]
            RoadClassResidential: _ClassVar[NavigationInfo.RoadProfile.RoadClassEnum]
            RoadClassPedestrian: _ClassVar[NavigationInfo.RoadProfile.RoadClassEnum]
        RoadClassUnknown: NavigationInfo.RoadProfile.RoadClassEnum
        RoadClassExpressway: NavigationInfo.RoadProfile.RoadClassEnum
        RoadClassExpresswayLink: NavigationInfo.RoadProfile.RoadClassEnum
        RoadClassTrunk: NavigationInfo.RoadProfile.RoadClassEnum
        RoadClassTrunkLink: NavigationInfo.RoadProfile.RoadClassEnum
        RoadClassPrimary: NavigationInfo.RoadProfile.RoadClassEnum
        RoadClassPrimaryLink: NavigationInfo.RoadProfile.RoadClassEnum
        RoadClassSecondary: NavigationInfo.RoadProfile.RoadClassEnum
        RoadClassSecondaryLink: NavigationInfo.RoadProfile.RoadClassEnum
        RoadClassResidential: NavigationInfo.RoadProfile.RoadClassEnum
        RoadClassPedestrian: NavigationInfo.RoadProfile.RoadClassEnum
        ROAD_CLASS_FIELD_NUMBER: _ClassVar[int]
        ROAD_NAME_FIELD_NUMBER: _ClassVar[int]
        DIRECTION_SITES_FIELD_NUMBER: _ClassVar[int]
        road_class: NavigationInfo.RoadProfile.RoadClassEnum
        road_name: str
        direction_sites: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, road_class: _Optional[_Union[NavigationInfo.RoadProfile.RoadClassEnum, str]] = ..., road_name: _Optional[str] = ..., direction_sites: _Optional[_Iterable[str]] = ...) -> None: ...
    class ExpresswayProfile(_message.Message):
        __slots__ = ("expressway_class", "expressway_code", "expressway_short_name", "expressway_full_name", "direction_sites")
        class ExpresswayClassEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            ExpresswayClassUnknown: _ClassVar[NavigationInfo.ExpresswayProfile.ExpresswayClassEnum]
            ExpresswayClassNational: _ClassVar[NavigationInfo.ExpresswayProfile.ExpresswayClassEnum]
            ExpresswayClassProvincial: _ClassVar[NavigationInfo.ExpresswayProfile.ExpresswayClassEnum]
        ExpresswayClassUnknown: NavigationInfo.ExpresswayProfile.ExpresswayClassEnum
        ExpresswayClassNational: NavigationInfo.ExpresswayProfile.ExpresswayClassEnum
        ExpresswayClassProvincial: NavigationInfo.ExpresswayProfile.ExpresswayClassEnum
        EXPRESSWAY_CLASS_FIELD_NUMBER: _ClassVar[int]
        EXPRESSWAY_CODE_FIELD_NUMBER: _ClassVar[int]
        EXPRESSWAY_SHORT_NAME_FIELD_NUMBER: _ClassVar[int]
        EXPRESSWAY_FULL_NAME_FIELD_NUMBER: _ClassVar[int]
        DIRECTION_SITES_FIELD_NUMBER: _ClassVar[int]
        expressway_class: NavigationInfo.ExpresswayProfile.ExpresswayClassEnum
        expressway_code: str
        expressway_short_name: str
        expressway_full_name: str
        direction_sites: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, expressway_class: _Optional[_Union[NavigationInfo.ExpresswayProfile.ExpresswayClassEnum, str]] = ..., expressway_code: _Optional[str] = ..., expressway_short_name: _Optional[str] = ..., expressway_full_name: _Optional[str] = ..., direction_sites: _Optional[_Iterable[str]] = ...) -> None: ...
    class Restriction(_message.Message):
        __slots__ = ("upper_speed_limit", "lower_speed_limit", "weight_limit", "height_limit")
        UPPER_SPEED_LIMIT_FIELD_NUMBER: _ClassVar[int]
        LOWER_SPEED_LIMIT_FIELD_NUMBER: _ClassVar[int]
        WEIGHT_LIMIT_FIELD_NUMBER: _ClassVar[int]
        HEIGHT_LIMIT_FIELD_NUMBER: _ClassVar[int]
        upper_speed_limit: float
        lower_speed_limit: float
        weight_limit: float
        height_limit: float
        def __init__(self, upper_speed_limit: _Optional[float] = ..., lower_speed_limit: _Optional[float] = ..., weight_limit: _Optional[float] = ..., height_limit: _Optional[float] = ...) -> None: ...
    class RoutingCheckpoint(_message.Message):
        __slots__ = ("estimated_time", "estimated_distance", "road_profile", "expressway_profile", "routing_action")
        class RoutingActionEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            RoutingActionNothing: _ClassVar[NavigationInfo.RoutingCheckpoint.RoutingActionEnum]
            RoutingActionStraight: _ClassVar[NavigationInfo.RoutingCheckpoint.RoutingActionEnum]
            RoutingActionLeftTurn: _ClassVar[NavigationInfo.RoutingCheckpoint.RoutingActionEnum]
            RoutingActionRightTurn: _ClassVar[NavigationInfo.RoutingCheckpoint.RoutingActionEnum]
            RoutingActionUTurn: _ClassVar[NavigationInfo.RoutingCheckpoint.RoutingActionEnum]
            RoutingActionKeep: _ClassVar[NavigationInfo.RoutingCheckpoint.RoutingActionEnum]
            RoutingActionMerge: _ClassVar[NavigationInfo.RoutingCheckpoint.RoutingActionEnum]
            RoutingActionLeave: _ClassVar[NavigationInfo.RoutingCheckpoint.RoutingActionEnum]
        RoutingActionNothing: NavigationInfo.RoutingCheckpoint.RoutingActionEnum
        RoutingActionStraight: NavigationInfo.RoutingCheckpoint.RoutingActionEnum
        RoutingActionLeftTurn: NavigationInfo.RoutingCheckpoint.RoutingActionEnum
        RoutingActionRightTurn: NavigationInfo.RoutingCheckpoint.RoutingActionEnum
        RoutingActionUTurn: NavigationInfo.RoutingCheckpoint.RoutingActionEnum
        RoutingActionKeep: NavigationInfo.RoutingCheckpoint.RoutingActionEnum
        RoutingActionMerge: NavigationInfo.RoutingCheckpoint.RoutingActionEnum
        RoutingActionLeave: NavigationInfo.RoutingCheckpoint.RoutingActionEnum
        ESTIMATED_TIME_FIELD_NUMBER: _ClassVar[int]
        ESTIMATED_DISTANCE_FIELD_NUMBER: _ClassVar[int]
        ROAD_PROFILE_FIELD_NUMBER: _ClassVar[int]
        EXPRESSWAY_PROFILE_FIELD_NUMBER: _ClassVar[int]
        ROUTING_ACTION_FIELD_NUMBER: _ClassVar[int]
        estimated_time: _plexus_common_pb2.Timestamp
        estimated_distance: float
        road_profile: NavigationInfo.RoadProfile
        expressway_profile: NavigationInfo.ExpresswayProfile
        routing_action: NavigationInfo.RoutingCheckpoint.RoutingActionEnum
        def __init__(self, estimated_time: _Optional[_Union[_plexus_common_pb2.Timestamp, _Mapping]] = ..., estimated_distance: _Optional[float] = ..., road_profile: _Optional[_Union[NavigationInfo.RoadProfile, _Mapping]] = ..., expressway_profile: _Optional[_Union[NavigationInfo.ExpresswayProfile, _Mapping]] = ..., routing_action: _Optional[_Union[NavigationInfo.RoutingCheckpoint.RoutingActionEnum, str]] = ...) -> None: ...
    ROAD_PROFILE_FIELD_NUMBER: _ClassVar[int]
    EXPRESSWAY_PROFILE_FIELD_NUMBER: _ClassVar[int]
    RESTRICTION_FIELD_NUMBER: _ClassVar[int]
    ROUTING_CHECKPOINTS_FIELD_NUMBER: _ClassVar[int]
    road_profile: NavigationInfo.RoadProfile
    expressway_profile: NavigationInfo.ExpresswayProfile
    restriction: NavigationInfo.Restriction
    routing_checkpoints: _containers.RepeatedCompositeFieldContainer[NavigationInfo.RoutingCheckpoint]
    def __init__(self, road_profile: _Optional[_Union[NavigationInfo.RoadProfile, _Mapping]] = ..., expressway_profile: _Optional[_Union[NavigationInfo.ExpresswayProfile, _Mapping]] = ..., restriction: _Optional[_Union[NavigationInfo.Restriction, _Mapping]] = ..., routing_checkpoints: _Optional[_Iterable[_Union[NavigationInfo.RoutingCheckpoint, _Mapping]]] = ...) -> None: ...
