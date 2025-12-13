from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Vector2(_message.Message):
    __slots__ = ("x", "y")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ...) -> None: ...

class Vector3(_message.Message):
    __slots__ = ("x", "y", "z")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    z: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ..., z: _Optional[float] = ...) -> None: ...

class Vector4(_message.Message):
    __slots__ = ("x", "y", "z", "w")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    W_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    z: float
    w: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ..., z: _Optional[float] = ..., w: _Optional[float] = ...) -> None: ...

class VectorN(_message.Message):
    __slots__ = ("length", "data")
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    length: int
    data: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, length: _Optional[int] = ..., data: _Optional[_Iterable[float]] = ...) -> None: ...

class VectorS(_message.Message):
    __slots__ = ("length", "data", "indices")
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    INDICES_FIELD_NUMBER: _ClassVar[int]
    length: int
    data: _containers.RepeatedScalarFieldContainer[float]
    indices: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, length: _Optional[int] = ..., data: _Optional[_Iterable[float]] = ..., indices: _Optional[_Iterable[int]] = ...) -> None: ...

class Matrix2(_message.Message):
    __slots__ = ("x", "y")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    x: Vector2
    y: Vector2
    def __init__(self, x: _Optional[_Union[Vector2, _Mapping]] = ..., y: _Optional[_Union[Vector2, _Mapping]] = ...) -> None: ...

class Matrix3(_message.Message):
    __slots__ = ("x", "y", "z")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    x: Vector3
    y: Vector3
    z: Vector3
    def __init__(self, x: _Optional[_Union[Vector3, _Mapping]] = ..., y: _Optional[_Union[Vector3, _Mapping]] = ..., z: _Optional[_Union[Vector3, _Mapping]] = ...) -> None: ...

class Matrix4(_message.Message):
    __slots__ = ("x", "y", "z", "w")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    W_FIELD_NUMBER: _ClassVar[int]
    x: Vector4
    y: Vector4
    z: Vector4
    w: Vector4
    def __init__(self, x: _Optional[_Union[Vector4, _Mapping]] = ..., y: _Optional[_Union[Vector4, _Mapping]] = ..., z: _Optional[_Union[Vector4, _Mapping]] = ..., w: _Optional[_Union[Vector4, _Mapping]] = ...) -> None: ...

class MatrixN(_message.Message):
    __slots__ = ("rows", "cols", "data")
    ROWS_FIELD_NUMBER: _ClassVar[int]
    COLS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    rows: int
    cols: int
    data: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, rows: _Optional[int] = ..., cols: _Optional[int] = ..., data: _Optional[_Iterable[float]] = ...) -> None: ...

class MatrixS(_message.Message):
    __slots__ = ("rows", "cols", "data", "row_indices", "col_indices")
    ROWS_FIELD_NUMBER: _ClassVar[int]
    COLS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    ROW_INDICES_FIELD_NUMBER: _ClassVar[int]
    COL_INDICES_FIELD_NUMBER: _ClassVar[int]
    rows: int
    cols: int
    data: _containers.RepeatedScalarFieldContainer[float]
    row_indices: _containers.RepeatedScalarFieldContainer[int]
    col_indices: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, rows: _Optional[int] = ..., cols: _Optional[int] = ..., data: _Optional[_Iterable[float]] = ..., row_indices: _Optional[_Iterable[int]] = ..., col_indices: _Optional[_Iterable[int]] = ...) -> None: ...

class Timestamp(_message.Message):
    __slots__ = ("seconds", "nanos")
    SECONDS_FIELD_NUMBER: _ClassVar[int]
    NANOS_FIELD_NUMBER: _ClassVar[int]
    seconds: int
    nanos: int
    def __init__(self, seconds: _Optional[int] = ..., nanos: _Optional[int] = ...) -> None: ...

class Color(_message.Message):
    __slots__ = ("r", "g", "b", "a")
    R_FIELD_NUMBER: _ClassVar[int]
    G_FIELD_NUMBER: _ClassVar[int]
    B_FIELD_NUMBER: _ClassVar[int]
    A_FIELD_NUMBER: _ClassVar[int]
    r: int
    g: int
    b: int
    a: int
    def __init__(self, r: _Optional[int] = ..., g: _Optional[int] = ..., b: _Optional[int] = ..., a: _Optional[int] = ...) -> None: ...

class Variant(_message.Message):
    __slots__ = ("value_int32", "value_int64", "value_float", "value_double", "value_string", "value_bytes", "value_bool", "value_vector2", "value_vector3", "value_vector4", "value_matrix2", "value_matrix3", "value_matrix4", "value_timestamp", "value_color")
    VALUE_INT32_FIELD_NUMBER: _ClassVar[int]
    VALUE_INT64_FIELD_NUMBER: _ClassVar[int]
    VALUE_FLOAT_FIELD_NUMBER: _ClassVar[int]
    VALUE_DOUBLE_FIELD_NUMBER: _ClassVar[int]
    VALUE_STRING_FIELD_NUMBER: _ClassVar[int]
    VALUE_BYTES_FIELD_NUMBER: _ClassVar[int]
    VALUE_BOOL_FIELD_NUMBER: _ClassVar[int]
    VALUE_VECTOR2_FIELD_NUMBER: _ClassVar[int]
    VALUE_VECTOR3_FIELD_NUMBER: _ClassVar[int]
    VALUE_VECTOR4_FIELD_NUMBER: _ClassVar[int]
    VALUE_MATRIX2_FIELD_NUMBER: _ClassVar[int]
    VALUE_MATRIX3_FIELD_NUMBER: _ClassVar[int]
    VALUE_MATRIX4_FIELD_NUMBER: _ClassVar[int]
    VALUE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VALUE_COLOR_FIELD_NUMBER: _ClassVar[int]
    value_int32: int
    value_int64: int
    value_float: float
    value_double: float
    value_string: str
    value_bytes: bytes
    value_bool: bool
    value_vector2: Vector2
    value_vector3: Vector3
    value_vector4: Vector4
    value_matrix2: Matrix2
    value_matrix3: Matrix3
    value_matrix4: Matrix4
    value_timestamp: Timestamp
    value_color: Color
    def __init__(self, value_int32: _Optional[int] = ..., value_int64: _Optional[int] = ..., value_float: _Optional[float] = ..., value_double: _Optional[float] = ..., value_string: _Optional[str] = ..., value_bytes: _Optional[bytes] = ..., value_bool: bool = ..., value_vector2: _Optional[_Union[Vector2, _Mapping]] = ..., value_vector3: _Optional[_Union[Vector3, _Mapping]] = ..., value_vector4: _Optional[_Union[Vector4, _Mapping]] = ..., value_matrix2: _Optional[_Union[Matrix2, _Mapping]] = ..., value_matrix3: _Optional[_Union[Matrix3, _Mapping]] = ..., value_matrix4: _Optional[_Union[Matrix4, _Mapping]] = ..., value_timestamp: _Optional[_Union[Timestamp, _Mapping]] = ..., value_color: _Optional[_Union[Color, _Mapping]] = ...) -> None: ...

class KeyValue(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: Variant
    def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Variant, _Mapping]] = ...) -> None: ...
