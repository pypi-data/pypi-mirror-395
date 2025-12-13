from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ControlCommand(_message.Message):
    __slots__ = ("steering", "throttle", "brake", "gear", "tractor_parking_brake_activated", "trailer_parking_brake_activated")
    class Command(_message.Message):
        __slots__ = ("input_value", "output_value", "command_value", "normalized_value")
        INPUT_VALUE_FIELD_NUMBER: _ClassVar[int]
        OUTPUT_VALUE_FIELD_NUMBER: _ClassVar[int]
        COMMAND_VALUE_FIELD_NUMBER: _ClassVar[int]
        NORMALIZED_VALUE_FIELD_NUMBER: _ClassVar[int]
        input_value: float
        output_value: float
        command_value: float
        normalized_value: float
        def __init__(self, input_value: _Optional[float] = ..., output_value: _Optional[float] = ..., command_value: _Optional[float] = ..., normalized_value: _Optional[float] = ...) -> None: ...
    STEERING_FIELD_NUMBER: _ClassVar[int]
    THROTTLE_FIELD_NUMBER: _ClassVar[int]
    BRAKE_FIELD_NUMBER: _ClassVar[int]
    GEAR_FIELD_NUMBER: _ClassVar[int]
    TRACTOR_PARKING_BRAKE_ACTIVATED_FIELD_NUMBER: _ClassVar[int]
    TRAILER_PARKING_BRAKE_ACTIVATED_FIELD_NUMBER: _ClassVar[int]
    steering: ControlCommand.Command
    throttle: ControlCommand.Command
    brake: ControlCommand.Command
    gear: ControlCommand.Command
    tractor_parking_brake_activated: bool
    trailer_parking_brake_activated: bool
    def __init__(self, steering: _Optional[_Union[ControlCommand.Command, _Mapping]] = ..., throttle: _Optional[_Union[ControlCommand.Command, _Mapping]] = ..., brake: _Optional[_Union[ControlCommand.Command, _Mapping]] = ..., gear: _Optional[_Union[ControlCommand.Command, _Mapping]] = ..., tractor_parking_brake_activated: bool = ..., trailer_parking_brake_activated: bool = ...) -> None: ...
