from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DbwCommand(_message.Message):
    __slots__ = ("steering", "throttle", "brake", "gear", "auto_mode")
    class AutoModeEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        AutoModeNeither: _ClassVar[DbwCommand.AutoModeEnum]
        AutoModeLateral: _ClassVar[DbwCommand.AutoModeEnum]
        AutoModeLongitudinal: _ClassVar[DbwCommand.AutoModeEnum]
        AutoModeBoth: _ClassVar[DbwCommand.AutoModeEnum]
    AutoModeNeither: DbwCommand.AutoModeEnum
    AutoModeLateral: DbwCommand.AutoModeEnum
    AutoModeLongitudinal: DbwCommand.AutoModeEnum
    AutoModeBoth: DbwCommand.AutoModeEnum
    class Command(_message.Message):
        __slots__ = ("input_value", "output_value", "command_value", "overridden")
        INPUT_VALUE_FIELD_NUMBER: _ClassVar[int]
        OUTPUT_VALUE_FIELD_NUMBER: _ClassVar[int]
        COMMAND_VALUE_FIELD_NUMBER: _ClassVar[int]
        OVERRIDDEN_FIELD_NUMBER: _ClassVar[int]
        input_value: float
        output_value: float
        command_value: float
        overridden: bool
        def __init__(self, input_value: _Optional[float] = ..., output_value: _Optional[float] = ..., command_value: _Optional[float] = ..., overridden: bool = ...) -> None: ...
    STEERING_FIELD_NUMBER: _ClassVar[int]
    THROTTLE_FIELD_NUMBER: _ClassVar[int]
    BRAKE_FIELD_NUMBER: _ClassVar[int]
    GEAR_FIELD_NUMBER: _ClassVar[int]
    AUTO_MODE_FIELD_NUMBER: _ClassVar[int]
    steering: DbwCommand.Command
    throttle: DbwCommand.Command
    brake: DbwCommand.Command
    gear: DbwCommand.Command
    auto_mode: DbwCommand.AutoModeEnum
    def __init__(self, steering: _Optional[_Union[DbwCommand.Command, _Mapping]] = ..., throttle: _Optional[_Union[DbwCommand.Command, _Mapping]] = ..., brake: _Optional[_Union[DbwCommand.Command, _Mapping]] = ..., gear: _Optional[_Union[DbwCommand.Command, _Mapping]] = ..., auto_mode: _Optional[_Union[DbwCommand.AutoModeEnum, str]] = ...) -> None: ...
