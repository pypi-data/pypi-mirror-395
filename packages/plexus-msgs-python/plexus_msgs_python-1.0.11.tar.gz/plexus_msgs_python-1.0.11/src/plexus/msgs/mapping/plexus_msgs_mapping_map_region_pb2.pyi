from plexus.msgs import plexus_common_pb2 as _plexus_common_pb2
from plexus.msgs import plexus_common_carto_pb2 as _plexus_common_carto_pb2
from plexus.msgs import plexus_common_entity_pb2 as _plexus_common_entity_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MapRegion(_message.Message):
    __slots__ = ("center", "lane_paths", "lane_edges", "lanes")
    class Coord(_message.Message):
        __slots__ = ("proj_coord", "geo_coord")
        PROJ_COORD_FIELD_NUMBER: _ClassVar[int]
        GEO_COORD_FIELD_NUMBER: _ClassVar[int]
        proj_coord: _plexus_common_pb2.Vector3
        geo_coord: _plexus_common_carto_pb2.GeoCoord
        def __init__(self, proj_coord: _Optional[_Union[_plexus_common_pb2.Vector3, _Mapping]] = ..., geo_coord: _Optional[_Union[_plexus_common_carto_pb2.GeoCoord, _Mapping]] = ...) -> None: ...
    class Waypoint(_message.Message):
        __slots__ = ("coord", "way_id", "prev_node_id", "next_node_id", "displacement", "altitude", "curvature", "pitch", "roll")
        COORD_FIELD_NUMBER: _ClassVar[int]
        WAY_ID_FIELD_NUMBER: _ClassVar[int]
        PREV_NODE_ID_FIELD_NUMBER: _ClassVar[int]
        NEXT_NODE_ID_FIELD_NUMBER: _ClassVar[int]
        LAMBDA_FIELD_NUMBER: _ClassVar[int]
        DISPLACEMENT_FIELD_NUMBER: _ClassVar[int]
        ALTITUDE_FIELD_NUMBER: _ClassVar[int]
        CURVATURE_FIELD_NUMBER: _ClassVar[int]
        PITCH_FIELD_NUMBER: _ClassVar[int]
        ROLL_FIELD_NUMBER: _ClassVar[int]
        coord: MapRegion.Coord
        way_id: int
        prev_node_id: int
        next_node_id: int
        displacement: float
        altitude: float
        curvature: float
        pitch: float
        roll: float
        def __init__(self, coord: _Optional[_Union[MapRegion.Coord, _Mapping]] = ..., way_id: _Optional[int] = ..., prev_node_id: _Optional[int] = ..., next_node_id: _Optional[int] = ..., displacement: _Optional[float] = ..., altitude: _Optional[float] = ..., curvature: _Optional[float] = ..., pitch: _Optional[float] = ..., roll: _Optional[float] = ..., **kwargs) -> None: ...
    class LanePath(_message.Message):
        __slots__ = ("way_id", "begin_waypoint", "end_waypoint", "coords", "attributes")
        class Attributes(_message.Message):
            __slots__ = ("upper_speed_limit", "lower_speed_limit")
            UPPER_SPEED_LIMIT_FIELD_NUMBER: _ClassVar[int]
            LOWER_SPEED_LIMIT_FIELD_NUMBER: _ClassVar[int]
            upper_speed_limit: float
            lower_speed_limit: float
            def __init__(self, upper_speed_limit: _Optional[float] = ..., lower_speed_limit: _Optional[float] = ...) -> None: ...
        WAY_ID_FIELD_NUMBER: _ClassVar[int]
        BEGIN_WAYPOINT_FIELD_NUMBER: _ClassVar[int]
        END_WAYPOINT_FIELD_NUMBER: _ClassVar[int]
        COORDS_FIELD_NUMBER: _ClassVar[int]
        ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
        way_id: int
        begin_waypoint: MapRegion.Waypoint
        end_waypoint: MapRegion.Waypoint
        coords: _containers.RepeatedCompositeFieldContainer[MapRegion.Coord]
        attributes: MapRegion.LanePath.Attributes
        def __init__(self, way_id: _Optional[int] = ..., begin_waypoint: _Optional[_Union[MapRegion.Waypoint, _Mapping]] = ..., end_waypoint: _Optional[_Union[MapRegion.Waypoint, _Mapping]] = ..., coords: _Optional[_Iterable[_Union[MapRegion.Coord, _Mapping]]] = ..., attributes: _Optional[_Union[MapRegion.LanePath.Attributes, _Mapping]] = ...) -> None: ...
    class LaneEdge(_message.Message):
        __slots__ = ("way_id", "begin_waypoint", "end_waypoint", "coords", "attributes")
        class Attributes(_message.Message):
            __slots__ = ("lane_mark_color", "lane_mark_pattern", "lane_mark_weight", "is_road_boundary", "is_fence")
            LANE_MARK_COLOR_FIELD_NUMBER: _ClassVar[int]
            LANE_MARK_PATTERN_FIELD_NUMBER: _ClassVar[int]
            LANE_MARK_WEIGHT_FIELD_NUMBER: _ClassVar[int]
            IS_ROAD_BOUNDARY_FIELD_NUMBER: _ClassVar[int]
            IS_FENCE_FIELD_NUMBER: _ClassVar[int]
            lane_mark_color: _plexus_common_entity_pb2.LaneMark.LaneMarkColorEnum
            lane_mark_pattern: _plexus_common_entity_pb2.LaneMark.LaneMarkPatternEnum
            lane_mark_weight: _plexus_common_entity_pb2.LaneMark.LaneMarkWeightEnum
            is_road_boundary: bool
            is_fence: bool
            def __init__(self, lane_mark_color: _Optional[_Union[_plexus_common_entity_pb2.LaneMark.LaneMarkColorEnum, str]] = ..., lane_mark_pattern: _Optional[_Union[_plexus_common_entity_pb2.LaneMark.LaneMarkPatternEnum, str]] = ..., lane_mark_weight: _Optional[_Union[_plexus_common_entity_pb2.LaneMark.LaneMarkWeightEnum, str]] = ..., is_road_boundary: bool = ..., is_fence: bool = ...) -> None: ...
        WAY_ID_FIELD_NUMBER: _ClassVar[int]
        BEGIN_WAYPOINT_FIELD_NUMBER: _ClassVar[int]
        END_WAYPOINT_FIELD_NUMBER: _ClassVar[int]
        COORDS_FIELD_NUMBER: _ClassVar[int]
        ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
        way_id: int
        begin_waypoint: MapRegion.Waypoint
        end_waypoint: MapRegion.Waypoint
        coords: _containers.RepeatedCompositeFieldContainer[MapRegion.Coord]
        attributes: MapRegion.LaneEdge.Attributes
        def __init__(self, way_id: _Optional[int] = ..., begin_waypoint: _Optional[_Union[MapRegion.Waypoint, _Mapping]] = ..., end_waypoint: _Optional[_Union[MapRegion.Waypoint, _Mapping]] = ..., coords: _Optional[_Iterable[_Union[MapRegion.Coord, _Mapping]]] = ..., attributes: _Optional[_Union[MapRegion.LaneEdge.Attributes, _Mapping]] = ...) -> None: ...
    class Lane(_message.Message):
        __slots__ = ("left_edge_index", "right_edge_index")
        LEFT_EDGE_INDEX_FIELD_NUMBER: _ClassVar[int]
        RIGHT_EDGE_INDEX_FIELD_NUMBER: _ClassVar[int]
        left_edge_index: int
        right_edge_index: int
        def __init__(self, left_edge_index: _Optional[int] = ..., right_edge_index: _Optional[int] = ...) -> None: ...
    CENTER_FIELD_NUMBER: _ClassVar[int]
    LANE_PATHS_FIELD_NUMBER: _ClassVar[int]
    LANE_EDGES_FIELD_NUMBER: _ClassVar[int]
    LANES_FIELD_NUMBER: _ClassVar[int]
    center: MapRegion.Coord
    lane_paths: _containers.RepeatedCompositeFieldContainer[MapRegion.LanePath]
    lane_edges: _containers.RepeatedCompositeFieldContainer[MapRegion.LaneEdge]
    lanes: _containers.RepeatedCompositeFieldContainer[MapRegion.Lane]
    def __init__(self, center: _Optional[_Union[MapRegion.Coord, _Mapping]] = ..., lane_paths: _Optional[_Iterable[_Union[MapRegion.LanePath, _Mapping]]] = ..., lane_edges: _Optional[_Iterable[_Union[MapRegion.LaneEdge, _Mapping]]] = ..., lanes: _Optional[_Iterable[_Union[MapRegion.Lane, _Mapping]]] = ...) -> None: ...
