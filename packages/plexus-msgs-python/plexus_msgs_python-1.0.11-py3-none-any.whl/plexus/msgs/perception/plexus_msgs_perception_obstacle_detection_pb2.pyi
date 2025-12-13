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

class ObstacleDetection(_message.Message):
    __slots__ = ("obstacles",)
    class MonoCameraRectObstacleDetection(_message.Message):
        __slots__ = ("detection_uid", "camera_message_header", "image_rect", "obstacle_type", "properties")
        DETECTION_UID_FIELD_NUMBER: _ClassVar[int]
        CAMERA_MESSAGE_HEADER_FIELD_NUMBER: _ClassVar[int]
        IMAGE_RECT_FIELD_NUMBER: _ClassVar[int]
        OBSTACLE_TYPE_FIELD_NUMBER: _ClassVar[int]
        PROPERTIES_FIELD_NUMBER: _ClassVar[int]
        detection_uid: str
        camera_message_header: _plexus_common_message_pb2.MessageHeader
        image_rect: _plexus_common_geom_pb2.Rect
        obstacle_type: _plexus_common_entity_pb2.Obstacle.ObstacleTypeEnum
        properties: _containers.RepeatedCompositeFieldContainer[_plexus_common_pb2.KeyValue]
        def __init__(self, detection_uid: _Optional[str] = ..., camera_message_header: _Optional[_Union[_plexus_common_message_pb2.MessageHeader, _Mapping]] = ..., image_rect: _Optional[_Union[_plexus_common_geom_pb2.Rect, _Mapping]] = ..., obstacle_type: _Optional[_Union[_plexus_common_entity_pb2.Obstacle.ObstacleTypeEnum, str]] = ..., properties: _Optional[_Iterable[_Union[_plexus_common_pb2.KeyValue, _Mapping]]] = ...) -> None: ...
    class StereoCameraRectObstacleDetection(_message.Message):
        __slots__ = ("detection_uid", "left_camera_message_header", "right_camera_message_header", "left_image_rect", "right_image_rect", "obstacle_type", "properties")
        DETECTION_UID_FIELD_NUMBER: _ClassVar[int]
        LEFT_CAMERA_MESSAGE_HEADER_FIELD_NUMBER: _ClassVar[int]
        RIGHT_CAMERA_MESSAGE_HEADER_FIELD_NUMBER: _ClassVar[int]
        LEFT_IMAGE_RECT_FIELD_NUMBER: _ClassVar[int]
        RIGHT_IMAGE_RECT_FIELD_NUMBER: _ClassVar[int]
        OBSTACLE_TYPE_FIELD_NUMBER: _ClassVar[int]
        PROPERTIES_FIELD_NUMBER: _ClassVar[int]
        detection_uid: str
        left_camera_message_header: _plexus_common_message_pb2.MessageHeader
        right_camera_message_header: _plexus_common_message_pb2.MessageHeader
        left_image_rect: _plexus_common_geom_pb2.Rect
        right_image_rect: _plexus_common_geom_pb2.Rect
        obstacle_type: _plexus_common_entity_pb2.Obstacle.ObstacleTypeEnum
        properties: _containers.RepeatedCompositeFieldContainer[_plexus_common_pb2.KeyValue]
        def __init__(self, detection_uid: _Optional[str] = ..., left_camera_message_header: _Optional[_Union[_plexus_common_message_pb2.MessageHeader, _Mapping]] = ..., right_camera_message_header: _Optional[_Union[_plexus_common_message_pb2.MessageHeader, _Mapping]] = ..., left_image_rect: _Optional[_Union[_plexus_common_geom_pb2.Rect, _Mapping]] = ..., right_image_rect: _Optional[_Union[_plexus_common_geom_pb2.Rect, _Mapping]] = ..., obstacle_type: _Optional[_Union[_plexus_common_entity_pb2.Obstacle.ObstacleTypeEnum, str]] = ..., properties: _Optional[_Iterable[_Union[_plexus_common_pb2.KeyValue, _Mapping]]] = ...) -> None: ...
    class LidarCuboidObstacleDetection(_message.Message):
        __slots__ = ("detection_uid", "lidar_message_header", "world_cuboid", "obstacle_type", "properties")
        DETECTION_UID_FIELD_NUMBER: _ClassVar[int]
        LIDAR_MESSAGE_HEADER_FIELD_NUMBER: _ClassVar[int]
        WORLD_CUBOID_FIELD_NUMBER: _ClassVar[int]
        OBSTACLE_TYPE_FIELD_NUMBER: _ClassVar[int]
        PROPERTIES_FIELD_NUMBER: _ClassVar[int]
        detection_uid: str
        lidar_message_header: _plexus_common_message_pb2.MessageHeader
        world_cuboid: _plexus_common_geom_pb2.Cuboid
        obstacle_type: _plexus_common_entity_pb2.Obstacle.ObstacleTypeEnum
        properties: _containers.RepeatedCompositeFieldContainer[_plexus_common_pb2.KeyValue]
        def __init__(self, detection_uid: _Optional[str] = ..., lidar_message_header: _Optional[_Union[_plexus_common_message_pb2.MessageHeader, _Mapping]] = ..., world_cuboid: _Optional[_Union[_plexus_common_geom_pb2.Cuboid, _Mapping]] = ..., obstacle_type: _Optional[_Union[_plexus_common_entity_pb2.Obstacle.ObstacleTypeEnum, str]] = ..., properties: _Optional[_Iterable[_Union[_plexus_common_pb2.KeyValue, _Mapping]]] = ...) -> None: ...
    class ObstacleDetectionVariant(_message.Message):
        __slots__ = ("mono_camera_rect", "stereo_camera_rect", "lidar_cuboid")
        MONO_CAMERA_RECT_FIELD_NUMBER: _ClassVar[int]
        STEREO_CAMERA_RECT_FIELD_NUMBER: _ClassVar[int]
        LIDAR_CUBOID_FIELD_NUMBER: _ClassVar[int]
        mono_camera_rect: ObstacleDetection.MonoCameraRectObstacleDetection
        stereo_camera_rect: ObstacleDetection.StereoCameraRectObstacleDetection
        lidar_cuboid: ObstacleDetection.LidarCuboidObstacleDetection
        def __init__(self, mono_camera_rect: _Optional[_Union[ObstacleDetection.MonoCameraRectObstacleDetection, _Mapping]] = ..., stereo_camera_rect: _Optional[_Union[ObstacleDetection.StereoCameraRectObstacleDetection, _Mapping]] = ..., lidar_cuboid: _Optional[_Union[ObstacleDetection.LidarCuboidObstacleDetection, _Mapping]] = ...) -> None: ...
    class Obstacle(_message.Message):
        __slots__ = ("obstacle_uid", "detections", "world_cuboid", "obstacle_type", "properties")
        OBSTACLE_UID_FIELD_NUMBER: _ClassVar[int]
        DETECTIONS_FIELD_NUMBER: _ClassVar[int]
        WORLD_CUBOID_FIELD_NUMBER: _ClassVar[int]
        OBSTACLE_TYPE_FIELD_NUMBER: _ClassVar[int]
        PROPERTIES_FIELD_NUMBER: _ClassVar[int]
        obstacle_uid: str
        detections: _containers.RepeatedCompositeFieldContainer[ObstacleDetection.ObstacleDetectionVariant]
        world_cuboid: _plexus_common_geom_pb2.Cuboid
        obstacle_type: _plexus_common_entity_pb2.Obstacle.ObstacleTypeEnum
        properties: _containers.RepeatedCompositeFieldContainer[_plexus_common_pb2.KeyValue]
        def __init__(self, obstacle_uid: _Optional[str] = ..., detections: _Optional[_Iterable[_Union[ObstacleDetection.ObstacleDetectionVariant, _Mapping]]] = ..., world_cuboid: _Optional[_Union[_plexus_common_geom_pb2.Cuboid, _Mapping]] = ..., obstacle_type: _Optional[_Union[_plexus_common_entity_pb2.Obstacle.ObstacleTypeEnum, str]] = ..., properties: _Optional[_Iterable[_Union[_plexus_common_pb2.KeyValue, _Mapping]]] = ...) -> None: ...
    OBSTACLES_FIELD_NUMBER: _ClassVar[int]
    obstacles: _containers.RepeatedCompositeFieldContainer[ObstacleDetection.Obstacle]
    def __init__(self, obstacles: _Optional[_Iterable[_Union[ObstacleDetection.Obstacle, _Mapping]]] = ...) -> None: ...
