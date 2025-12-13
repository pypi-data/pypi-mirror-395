from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class Obstacle(_message.Message):
    __slots__ = ()
    class ObstacleTypeEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ObstacleTypeUnknown: _ClassVar[Obstacle.ObstacleTypeEnum]
        ObstacleTypeFacility: _ClassVar[Obstacle.ObstacleTypeEnum]
        ObstacleTypeFacilitySignal: _ClassVar[Obstacle.ObstacleTypeEnum]
        ObstacleTypeFacilitySign: _ClassVar[Obstacle.ObstacleTypeEnum]
        ObstacleTypeFacilityCone: _ClassVar[Obstacle.ObstacleTypeEnum]
        ObstacleTypeFacilityPole: _ClassVar[Obstacle.ObstacleTypeEnum]
        ObstacleTypeFacilityBarricade: _ClassVar[Obstacle.ObstacleTypeEnum]
        ObstacleTypeFacilityRoadMark: _ClassVar[Obstacle.ObstacleTypeEnum]
        ObstacleTypePerson: _ClassVar[Obstacle.ObstacleTypeEnum]
        ObstacleTypeLowSpeed: _ClassVar[Obstacle.ObstacleTypeEnum]
        ObstacleTypeLowSpeedBicycle: _ClassVar[Obstacle.ObstacleTypeEnum]
        ObstacleTypeLowSpeedScooter: _ClassVar[Obstacle.ObstacleTypeEnum]
        ObstacleTypeVehicle: _ClassVar[Obstacle.ObstacleTypeEnum]
        ObstacleTypeVehicleMotorcycle: _ClassVar[Obstacle.ObstacleTypeEnum]
        ObstacleTypeVehicleCar: _ClassVar[Obstacle.ObstacleTypeEnum]
        ObstacleTypeVehicleVan: _ClassVar[Obstacle.ObstacleTypeEnum]
        ObstacleTypeVehiclePickup: _ClassVar[Obstacle.ObstacleTypeEnum]
        ObstacleTypeVehicleBus: _ClassVar[Obstacle.ObstacleTypeEnum]
        ObstacleTypeVehicleTruck: _ClassVar[Obstacle.ObstacleTypeEnum]
        ObstacleTypeVehicleTractor: _ClassVar[Obstacle.ObstacleTypeEnum]
        ObstacleTypeVehicleTrailer: _ClassVar[Obstacle.ObstacleTypeEnum]
        ObstacleTypeOthers: _ClassVar[Obstacle.ObstacleTypeEnum]
        ObstacleTypeUnclassified: _ClassVar[Obstacle.ObstacleTypeEnum]
    ObstacleTypeUnknown: Obstacle.ObstacleTypeEnum
    ObstacleTypeFacility: Obstacle.ObstacleTypeEnum
    ObstacleTypeFacilitySignal: Obstacle.ObstacleTypeEnum
    ObstacleTypeFacilitySign: Obstacle.ObstacleTypeEnum
    ObstacleTypeFacilityCone: Obstacle.ObstacleTypeEnum
    ObstacleTypeFacilityPole: Obstacle.ObstacleTypeEnum
    ObstacleTypeFacilityBarricade: Obstacle.ObstacleTypeEnum
    ObstacleTypeFacilityRoadMark: Obstacle.ObstacleTypeEnum
    ObstacleTypePerson: Obstacle.ObstacleTypeEnum
    ObstacleTypeLowSpeed: Obstacle.ObstacleTypeEnum
    ObstacleTypeLowSpeedBicycle: Obstacle.ObstacleTypeEnum
    ObstacleTypeLowSpeedScooter: Obstacle.ObstacleTypeEnum
    ObstacleTypeVehicle: Obstacle.ObstacleTypeEnum
    ObstacleTypeVehicleMotorcycle: Obstacle.ObstacleTypeEnum
    ObstacleTypeVehicleCar: Obstacle.ObstacleTypeEnum
    ObstacleTypeVehicleVan: Obstacle.ObstacleTypeEnum
    ObstacleTypeVehiclePickup: Obstacle.ObstacleTypeEnum
    ObstacleTypeVehicleBus: Obstacle.ObstacleTypeEnum
    ObstacleTypeVehicleTruck: Obstacle.ObstacleTypeEnum
    ObstacleTypeVehicleTractor: Obstacle.ObstacleTypeEnum
    ObstacleTypeVehicleTrailer: Obstacle.ObstacleTypeEnum
    ObstacleTypeOthers: Obstacle.ObstacleTypeEnum
    ObstacleTypeUnclassified: Obstacle.ObstacleTypeEnum
    def __init__(self) -> None: ...

class LaneMark(_message.Message):
    __slots__ = ()
    class LaneMarkPatternEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LaneMarkPatternUnknown: _ClassVar[LaneMark.LaneMarkPatternEnum]
        LaneMarkPatternSolid: _ClassVar[LaneMark.LaneMarkPatternEnum]
        LaneMarkPatternDashed: _ClassVar[LaneMark.LaneMarkPatternEnum]
        LaneMarkPatternDotted: _ClassVar[LaneMark.LaneMarkPatternEnum]
        LaneMarkPatternUnclassified: _ClassVar[LaneMark.LaneMarkPatternEnum]
    LaneMarkPatternUnknown: LaneMark.LaneMarkPatternEnum
    LaneMarkPatternSolid: LaneMark.LaneMarkPatternEnum
    LaneMarkPatternDashed: LaneMark.LaneMarkPatternEnum
    LaneMarkPatternDotted: LaneMark.LaneMarkPatternEnum
    LaneMarkPatternUnclassified: LaneMark.LaneMarkPatternEnum
    class LaneMarkWeightEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LaneMarkWeightUnknown: _ClassVar[LaneMark.LaneMarkWeightEnum]
        LaneMarkWeightThin: _ClassVar[LaneMark.LaneMarkWeightEnum]
        LaneMarkWeightNormal: _ClassVar[LaneMark.LaneMarkWeightEnum]
        LaneMarkWeightBold: _ClassVar[LaneMark.LaneMarkWeightEnum]
        LaneMarkWeightUnclassified: _ClassVar[LaneMark.LaneMarkWeightEnum]
    LaneMarkWeightUnknown: LaneMark.LaneMarkWeightEnum
    LaneMarkWeightThin: LaneMark.LaneMarkWeightEnum
    LaneMarkWeightNormal: LaneMark.LaneMarkWeightEnum
    LaneMarkWeightBold: LaneMark.LaneMarkWeightEnum
    LaneMarkWeightUnclassified: LaneMark.LaneMarkWeightEnum
    class LaneMarkColorEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LaneMarkColorUnknown: _ClassVar[LaneMark.LaneMarkColorEnum]
        LaneMarkColorWhite: _ClassVar[LaneMark.LaneMarkColorEnum]
        LaneMarkColorYellow: _ClassVar[LaneMark.LaneMarkColorEnum]
        LaneMarkColorUnclassified: _ClassVar[LaneMark.LaneMarkColorEnum]
    LaneMarkColorUnknown: LaneMark.LaneMarkColorEnum
    LaneMarkColorWhite: LaneMark.LaneMarkColorEnum
    LaneMarkColorYellow: LaneMark.LaneMarkColorEnum
    LaneMarkColorUnclassified: LaneMark.LaneMarkColorEnum
    def __init__(self) -> None: ...
