from plexus.msgs import plexus_common_pb2 as _plexus_common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Transform2(_message.Message):
    __slots__ = ("translation", "rotation")
    TRANSLATION_FIELD_NUMBER: _ClassVar[int]
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    translation: _plexus_common_pb2.Vector2
    rotation: _plexus_common_pb2.Matrix2
    def __init__(self, translation: _Optional[_Union[_plexus_common_pb2.Vector2, _Mapping]] = ..., rotation: _Optional[_Union[_plexus_common_pb2.Matrix2, _Mapping]] = ...) -> None: ...

class Transform3(_message.Message):
    __slots__ = ("translation", "rotation")
    TRANSLATION_FIELD_NUMBER: _ClassVar[int]
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    translation: _plexus_common_pb2.Vector3
    rotation: _plexus_common_pb2.Matrix3
    def __init__(self, translation: _Optional[_Union[_plexus_common_pb2.Vector3, _Mapping]] = ..., rotation: _Optional[_Union[_plexus_common_pb2.Matrix3, _Mapping]] = ...) -> None: ...

class Pose(_message.Message):
    __slots__ = ("position", "orientation")
    POSITION_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    position: _plexus_common_pb2.Vector3
    orientation: _plexus_common_pb2.Vector4
    def __init__(self, position: _Optional[_Union[_plexus_common_pb2.Vector3, _Mapping]] = ..., orientation: _Optional[_Union[_plexus_common_pb2.Vector4, _Mapping]] = ...) -> None: ...

class Twist(_message.Message):
    __slots__ = ("linear", "angular")
    LINEAR_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_FIELD_NUMBER: _ClassVar[int]
    linear: _plexus_common_pb2.Vector3
    angular: _plexus_common_pb2.Vector3
    def __init__(self, linear: _Optional[_Union[_plexus_common_pb2.Vector3, _Mapping]] = ..., angular: _Optional[_Union[_plexus_common_pb2.Vector3, _Mapping]] = ...) -> None: ...

class Box2(_message.Message):
    __slots__ = ("sizes",)
    SIZES_FIELD_NUMBER: _ClassVar[int]
    sizes: _plexus_common_pb2.Vector2
    def __init__(self, sizes: _Optional[_Union[_plexus_common_pb2.Vector2, _Mapping]] = ...) -> None: ...

class Box3(_message.Message):
    __slots__ = ("sizes",)
    SIZES_FIELD_NUMBER: _ClassVar[int]
    sizes: _plexus_common_pb2.Vector3
    def __init__(self, sizes: _Optional[_Union[_plexus_common_pb2.Vector3, _Mapping]] = ...) -> None: ...

class BoxN(_message.Message):
    __slots__ = ("sizes",)
    SIZES_FIELD_NUMBER: _ClassVar[int]
    sizes: _plexus_common_pb2.VectorN
    def __init__(self, sizes: _Optional[_Union[_plexus_common_pb2.VectorN, _Mapping]] = ...) -> None: ...

class Ellipsoid2(_message.Message):
    __slots__ = ("radii",)
    RADII_FIELD_NUMBER: _ClassVar[int]
    radii: _plexus_common_pb2.Vector2
    def __init__(self, radii: _Optional[_Union[_plexus_common_pb2.Vector2, _Mapping]] = ...) -> None: ...

class Ellipsoid3(_message.Message):
    __slots__ = ("radii",)
    RADII_FIELD_NUMBER: _ClassVar[int]
    radii: _plexus_common_pb2.Vector3
    def __init__(self, radii: _Optional[_Union[_plexus_common_pb2.Vector3, _Mapping]] = ...) -> None: ...

class EllipsoidN(_message.Message):
    __slots__ = ("radii",)
    RADII_FIELD_NUMBER: _ClassVar[int]
    radii: _plexus_common_pb2.VectorN
    def __init__(self, radii: _Optional[_Union[_plexus_common_pb2.VectorN, _Mapping]] = ...) -> None: ...

class Polygon2(_message.Message):
    __slots__ = ("vertices",)
    VERTICES_FIELD_NUMBER: _ClassVar[int]
    vertices: _containers.RepeatedCompositeFieldContainer[_plexus_common_pb2.Vector2]
    def __init__(self, vertices: _Optional[_Iterable[_Union[_plexus_common_pb2.Vector2, _Mapping]]] = ...) -> None: ...

class Polygon3(_message.Message):
    __slots__ = ("vertices",)
    VERTICES_FIELD_NUMBER: _ClassVar[int]
    vertices: _containers.RepeatedCompositeFieldContainer[_plexus_common_pb2.Vector3]
    def __init__(self, vertices: _Optional[_Iterable[_Union[_plexus_common_pb2.Vector3, _Mapping]]] = ...) -> None: ...

class PolygonN(_message.Message):
    __slots__ = ("vertices",)
    VERTICES_FIELD_NUMBER: _ClassVar[int]
    vertices: _containers.RepeatedCompositeFieldContainer[_plexus_common_pb2.VectorN]
    def __init__(self, vertices: _Optional[_Iterable[_Union[_plexus_common_pb2.VectorN, _Mapping]]] = ...) -> None: ...

class Rect(_message.Message):
    __slots__ = ("transform2", "box2")
    TRANSFORM2_FIELD_NUMBER: _ClassVar[int]
    BOX2_FIELD_NUMBER: _ClassVar[int]
    transform2: Transform2
    box2: Box2
    def __init__(self, transform2: _Optional[_Union[Transform2, _Mapping]] = ..., box2: _Optional[_Union[Box2, _Mapping]] = ...) -> None: ...

class Cuboid(_message.Message):
    __slots__ = ("transform3", "box3")
    TRANSFORM3_FIELD_NUMBER: _ClassVar[int]
    BOX3_FIELD_NUMBER: _ClassVar[int]
    transform3: Transform3
    box3: Box3
    def __init__(self, transform3: _Optional[_Union[Transform3, _Mapping]] = ..., box3: _Optional[_Union[Box3, _Mapping]] = ...) -> None: ...

class Cylinder(_message.Message):
    __slots__ = ("transform3", "base_ellipsoid2", "height")
    TRANSFORM3_FIELD_NUMBER: _ClassVar[int]
    BASE_ELLIPSOID2_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    transform3: Transform3
    base_ellipsoid2: Ellipsoid2
    height: float
    def __init__(self, transform3: _Optional[_Union[Transform3, _Mapping]] = ..., base_ellipsoid2: _Optional[_Union[Ellipsoid2, _Mapping]] = ..., height: _Optional[float] = ...) -> None: ...

class Cone(_message.Message):
    __slots__ = ("transform3", "base_ellipsoid2", "height")
    TRANSFORM3_FIELD_NUMBER: _ClassVar[int]
    BASE_ELLIPSOID2_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    transform3: Transform3
    base_ellipsoid2: Ellipsoid2
    height: float
    def __init__(self, transform3: _Optional[_Union[Transform3, _Mapping]] = ..., base_ellipsoid2: _Optional[_Union[Ellipsoid2, _Mapping]] = ..., height: _Optional[float] = ...) -> None: ...

class Prism(_message.Message):
    __slots__ = ("transform3", "base_polygon2", "height")
    TRANSFORM3_FIELD_NUMBER: _ClassVar[int]
    BASE_POLYGON2_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    transform3: Transform3
    base_polygon2: Polygon2
    height: float
    def __init__(self, transform3: _Optional[_Union[Transform3, _Mapping]] = ..., base_polygon2: _Optional[_Union[Polygon2, _Mapping]] = ..., height: _Optional[float] = ...) -> None: ...

class Pyramid(_message.Message):
    __slots__ = ("transform3", "base_polygon2", "height")
    TRANSFORM3_FIELD_NUMBER: _ClassVar[int]
    BASE_POLYGON2_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    transform3: Transform3
    base_polygon2: Polygon2
    height: float
    def __init__(self, transform3: _Optional[_Union[Transform3, _Mapping]] = ..., base_polygon2: _Optional[_Union[Polygon2, _Mapping]] = ..., height: _Optional[float] = ...) -> None: ...
