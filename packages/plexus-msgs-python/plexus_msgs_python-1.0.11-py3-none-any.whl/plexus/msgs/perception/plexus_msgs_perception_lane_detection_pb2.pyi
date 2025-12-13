from plexus.msgs import plexus_common_pb2 as _plexus_common_pb2
from plexus.msgs import plexus_common_message_pb2 as _plexus_common_message_pb2
from plexus.msgs import plexus_common_geom_pb2 as _plexus_common_geom_pb2
from plexus.msgs import plexus_common_entity_pb2 as _plexus_common_entity_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LaneDetection(_message.Message):
    __slots__ = ("lane_boundaries", "lanes")
    class CameraPolygon2LaneMarkDetection(_message.Message):
        __slots__ = ("detection_uid", "camera_message_header", "image_polygon2", "lane_mark_pattern", "lane_mark_weight", "lane_mark_color", "properties")
        DETECTION_UID_FIELD_NUMBER: _ClassVar[int]
        CAMERA_MESSAGE_HEADER_FIELD_NUMBER: _ClassVar[int]
        IMAGE_POLYGON2_FIELD_NUMBER: _ClassVar[int]
        LANE_MARK_PATTERN_FIELD_NUMBER: _ClassVar[int]
        LANE_MARK_WEIGHT_FIELD_NUMBER: _ClassVar[int]
        LANE_MARK_COLOR_FIELD_NUMBER: _ClassVar[int]
        PROPERTIES_FIELD_NUMBER: _ClassVar[int]
        detection_uid: str
        camera_message_header: _plexus_common_message_pb2.MessageHeader
        image_polygon2: _plexus_common_geom_pb2.Polygon2
        lane_mark_pattern: _plexus_common_entity_pb2.LaneMark.LaneMarkPatternEnum
        lane_mark_weight: _plexus_common_entity_pb2.LaneMark.LaneMarkWeightEnum
        lane_mark_color: _plexus_common_entity_pb2.LaneMark.LaneMarkColorEnum
        properties: _containers.RepeatedCompositeFieldContainer[_plexus_common_pb2.KeyValue]
        def __init__(self, detection_uid: _Optional[str] = ..., camera_message_header: _Optional[_Union[_plexus_common_message_pb2.MessageHeader, _Mapping]] = ..., image_polygon2: _Optional[_Union[_plexus_common_geom_pb2.Polygon2, _Mapping]] = ..., lane_mark_pattern: _Optional[_Union[_plexus_common_entity_pb2.LaneMark.LaneMarkPatternEnum, str]] = ..., lane_mark_weight: _Optional[_Union[_plexus_common_entity_pb2.LaneMark.LaneMarkWeightEnum, str]] = ..., lane_mark_color: _Optional[_Union[_plexus_common_entity_pb2.LaneMark.LaneMarkColorEnum, str]] = ..., properties: _Optional[_Iterable[_Union[_plexus_common_pb2.KeyValue, _Mapping]]] = ...) -> None: ...
    class LidarPolygon3LaneMarkDetection(_message.Message):
        __slots__ = ("detection_uid", "lidar_message_header", "world_polygon3", "lane_mark_pattern", "lane_mark_weight", "lane_mark_color", "properties")
        DETECTION_UID_FIELD_NUMBER: _ClassVar[int]
        LIDAR_MESSAGE_HEADER_FIELD_NUMBER: _ClassVar[int]
        WORLD_POLYGON3_FIELD_NUMBER: _ClassVar[int]
        LANE_MARK_PATTERN_FIELD_NUMBER: _ClassVar[int]
        LANE_MARK_WEIGHT_FIELD_NUMBER: _ClassVar[int]
        LANE_MARK_COLOR_FIELD_NUMBER: _ClassVar[int]
        PROPERTIES_FIELD_NUMBER: _ClassVar[int]
        detection_uid: str
        lidar_message_header: _plexus_common_message_pb2.MessageHeader
        world_polygon3: _plexus_common_geom_pb2.Polygon3
        lane_mark_pattern: _plexus_common_entity_pb2.LaneMark.LaneMarkPatternEnum
        lane_mark_weight: _plexus_common_entity_pb2.LaneMark.LaneMarkWeightEnum
        lane_mark_color: _plexus_common_entity_pb2.LaneMark.LaneMarkColorEnum
        properties: _containers.RepeatedCompositeFieldContainer[_plexus_common_pb2.KeyValue]
        def __init__(self, detection_uid: _Optional[str] = ..., lidar_message_header: _Optional[_Union[_plexus_common_message_pb2.MessageHeader, _Mapping]] = ..., world_polygon3: _Optional[_Union[_plexus_common_geom_pb2.Polygon3, _Mapping]] = ..., lane_mark_pattern: _Optional[_Union[_plexus_common_entity_pb2.LaneMark.LaneMarkPatternEnum, str]] = ..., lane_mark_weight: _Optional[_Union[_plexus_common_entity_pb2.LaneMark.LaneMarkWeightEnum, str]] = ..., lane_mark_color: _Optional[_Union[_plexus_common_entity_pb2.LaneMark.LaneMarkColorEnum, str]] = ..., properties: _Optional[_Iterable[_Union[_plexus_common_pb2.KeyValue, _Mapping]]] = ...) -> None: ...
    class LaneMarkDetectionVariant(_message.Message):
        __slots__ = ("camera_polygon2", "lidar_polygon3")
        CAMERA_POLYGON2_FIELD_NUMBER: _ClassVar[int]
        LIDAR_POLYGON3_FIELD_NUMBER: _ClassVar[int]
        camera_polygon2: LaneDetection.CameraPolygon2LaneMarkDetection
        lidar_polygon3: LaneDetection.LidarPolygon3LaneMarkDetection
        def __init__(self, camera_polygon2: _Optional[_Union[LaneDetection.CameraPolygon2LaneMarkDetection, _Mapping]] = ..., lidar_polygon3: _Optional[_Union[LaneDetection.LidarPolygon3LaneMarkDetection, _Mapping]] = ...) -> None: ...
    class LaneMark(_message.Message):
        __slots__ = ("lane_mark_uid", "detections", "world_polygon3", "lane_mark_pattern", "lane_mark_weight", "lane_mark_color", "properties")
        LANE_MARK_UID_FIELD_NUMBER: _ClassVar[int]
        DETECTIONS_FIELD_NUMBER: _ClassVar[int]
        WORLD_POLYGON3_FIELD_NUMBER: _ClassVar[int]
        LANE_MARK_PATTERN_FIELD_NUMBER: _ClassVar[int]
        LANE_MARK_WEIGHT_FIELD_NUMBER: _ClassVar[int]
        LANE_MARK_COLOR_FIELD_NUMBER: _ClassVar[int]
        PROPERTIES_FIELD_NUMBER: _ClassVar[int]
        lane_mark_uid: str
        detections: _containers.RepeatedCompositeFieldContainer[LaneDetection.LaneMarkDetectionVariant]
        world_polygon3: _plexus_common_geom_pb2.Polygon3
        lane_mark_pattern: _plexus_common_entity_pb2.LaneMark.LaneMarkPatternEnum
        lane_mark_weight: _plexus_common_entity_pb2.LaneMark.LaneMarkWeightEnum
        lane_mark_color: _plexus_common_entity_pb2.LaneMark.LaneMarkColorEnum
        properties: _containers.RepeatedCompositeFieldContainer[_plexus_common_pb2.KeyValue]
        def __init__(self, lane_mark_uid: _Optional[str] = ..., detections: _Optional[_Iterable[_Union[LaneDetection.LaneMarkDetectionVariant, _Mapping]]] = ..., world_polygon3: _Optional[_Union[_plexus_common_geom_pb2.Polygon3, _Mapping]] = ..., lane_mark_pattern: _Optional[_Union[_plexus_common_entity_pb2.LaneMark.LaneMarkPatternEnum, str]] = ..., lane_mark_weight: _Optional[_Union[_plexus_common_entity_pb2.LaneMark.LaneMarkWeightEnum, str]] = ..., lane_mark_color: _Optional[_Union[_plexus_common_entity_pb2.LaneMark.LaneMarkColorEnum, str]] = ..., properties: _Optional[_Iterable[_Union[_plexus_common_pb2.KeyValue, _Mapping]]] = ...) -> None: ...
    class LaneBoundary(_message.Message):
        __slots__ = ("lane_boundary_uid", "lane_marks", "properties")
        LANE_BOUNDARY_UID_FIELD_NUMBER: _ClassVar[int]
        LANE_MARKS_FIELD_NUMBER: _ClassVar[int]
        PROPERTIES_FIELD_NUMBER: _ClassVar[int]
        lane_boundary_uid: str
        lane_marks: _containers.RepeatedCompositeFieldContainer[LaneDetection.LaneMark]
        properties: _containers.RepeatedCompositeFieldContainer[_plexus_common_pb2.KeyValue]
        def __init__(self, lane_boundary_uid: _Optional[str] = ..., lane_marks: _Optional[_Iterable[_Union[LaneDetection.LaneMark, _Mapping]]] = ..., properties: _Optional[_Iterable[_Union[_plexus_common_pb2.KeyValue, _Mapping]]] = ...) -> None: ...
    class Lane(_message.Message):
        __slots__ = ("lane_uid", "left_lane_boundary_uid", "right_lane_boundary_uid", "properties")
        LANE_UID_FIELD_NUMBER: _ClassVar[int]
        LEFT_LANE_BOUNDARY_UID_FIELD_NUMBER: _ClassVar[int]
        RIGHT_LANE_BOUNDARY_UID_FIELD_NUMBER: _ClassVar[int]
        PROPERTIES_FIELD_NUMBER: _ClassVar[int]
        lane_uid: str
        left_lane_boundary_uid: str
        right_lane_boundary_uid: str
        properties: _containers.RepeatedCompositeFieldContainer[_plexus_common_pb2.KeyValue]
        def __init__(self, lane_uid: _Optional[str] = ..., left_lane_boundary_uid: _Optional[str] = ..., right_lane_boundary_uid: _Optional[str] = ..., properties: _Optional[_Iterable[_Union[_plexus_common_pb2.KeyValue, _Mapping]]] = ...) -> None: ...
    LANE_BOUNDARIES_FIELD_NUMBER: _ClassVar[int]
    LANES_FIELD_NUMBER: _ClassVar[int]
    lane_boundaries: _containers.RepeatedCompositeFieldContainer[LaneDetection.LaneBoundary]
    lanes: _containers.RepeatedCompositeFieldContainer[LaneDetection.Lane]
    def __init__(self, lane_boundaries: _Optional[_Iterable[_Union[LaneDetection.LaneBoundary, _Mapping]]] = ..., lanes: _Optional[_Iterable[_Union[LaneDetection.Lane, _Mapping]]] = ...) -> None: ...
