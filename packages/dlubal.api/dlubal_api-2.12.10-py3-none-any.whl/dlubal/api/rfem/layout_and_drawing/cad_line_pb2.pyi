from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CadLine(_message.Message):
    __slots__ = ("no", "definition_nodes", "type", "length", "position", "position_short", "comment", "arc_first_node", "arc_second_node", "arc_control_point_object", "arc_control_point", "arc_control_point_x", "arc_control_point_y", "arc_control_point_z", "arc_center", "arc_center_x", "arc_center_y", "arc_center_z", "arc_radius", "arc_height", "arc_alpha", "arc_alpha_adjustment_target", "circle_center", "circle_center_coordinate_1", "circle_center_coordinate_2", "circle_center_coordinate_3", "circle_normal", "circle_normal_coordinate_1", "circle_normal_coordinate_2", "circle_normal_coordinate_3", "circle_rotation", "circle_node", "circle_node_coordinate_1", "circle_node_coordinate_2", "circle_node_coordinate_3", "circle_radius", "elliptical_arc_first_node", "elliptical_arc_second_node", "elliptical_arc_alpha", "elliptical_arc_beta", "elliptical_arc_normal", "elliptical_arc_normal_x", "elliptical_arc_normal_y", "elliptical_arc_normal_z", "elliptical_arc_major_radius", "elliptical_arc_minor_radius", "elliptical_arc_center", "elliptical_arc_center_x", "elliptical_arc_center_y", "elliptical_arc_center_z", "elliptical_arc_focus_1", "elliptical_arc_focus_1_x", "elliptical_arc_focus_1_y", "elliptical_arc_focus_1_z", "elliptical_arc_focus_2", "elliptical_arc_focus_2_x", "elliptical_arc_focus_2_y", "elliptical_arc_focus_2_z", "elliptical_arc_first_control_point_object", "elliptical_arc_first_control_point", "elliptical_arc_first_control_point_x", "elliptical_arc_first_control_point_y", "elliptical_arc_first_control_point_z", "elliptical_arc_second_control_point_object", "elliptical_arc_second_control_point", "elliptical_arc_second_control_point_x", "elliptical_arc_second_control_point_y", "elliptical_arc_second_control_point_z", "elliptical_arc_perimeter_control_point_object", "elliptical_arc_perimeter_control_point", "elliptical_arc_perimeter_control_point_x", "elliptical_arc_perimeter_control_point_y", "elliptical_arc_perimeter_control_point_z", "ellipse_first_node", "ellipse_second_node", "ellipse_control_point_object", "ellipse_control_point", "ellipse_control_point_x", "ellipse_control_point_y", "ellipse_control_point_z", "parabola_first_node", "parabola_second_node", "parabola_control_point_object", "parabola_control_point", "parabola_control_point_x", "parabola_control_point_y", "parabola_control_point_z", "parabola_focus_directrix_distance", "parabola_alpha", "parabola_focus", "parabola_focus_x", "parabola_focus_y", "parabola_focus_z", "nurbs_order", "nurbs_control_points_by_components", "nurbs_control_points", "nurbs_knots", "rotation_specification_type", "rotation_angle", "rotation_help_node", "rotation_plane", "is_rotated", "parent_layer", "is_locked_by_parent_layer", "is_generated", "generating_object_info", "color_by", "color", "line_type_by", "line_type", "line_thickness_by", "line_thickness", "start_point", "start_point_coordinates", "start_point_x", "start_point_y", "start_point_z", "end_point", "end_point_coordinates", "end_point_x", "end_point_y", "end_point_z", "definition_points", "id_for_export_import", "metadata_for_export_import")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TYPE_UNKNOWN: _ClassVar[CadLine.Type]
        TYPE_ARC: _ClassVar[CadLine.Type]
        TYPE_CIRCLE: _ClassVar[CadLine.Type]
        TYPE_CUT_VIA_SECTION: _ClassVar[CadLine.Type]
        TYPE_CUT_VIA_TWO_LINES: _ClassVar[CadLine.Type]
        TYPE_ELLIPSE: _ClassVar[CadLine.Type]
        TYPE_ELLIPTICAL_ARC: _ClassVar[CadLine.Type]
        TYPE_NURBS: _ClassVar[CadLine.Type]
        TYPE_PARABOLA: _ClassVar[CadLine.Type]
        TYPE_POLYLINE: _ClassVar[CadLine.Type]
        TYPE_SPLINE: _ClassVar[CadLine.Type]
    TYPE_UNKNOWN: CadLine.Type
    TYPE_ARC: CadLine.Type
    TYPE_CIRCLE: CadLine.Type
    TYPE_CUT_VIA_SECTION: CadLine.Type
    TYPE_CUT_VIA_TWO_LINES: CadLine.Type
    TYPE_ELLIPSE: CadLine.Type
    TYPE_ELLIPTICAL_ARC: CadLine.Type
    TYPE_NURBS: CadLine.Type
    TYPE_PARABOLA: CadLine.Type
    TYPE_POLYLINE: CadLine.Type
    TYPE_SPLINE: CadLine.Type
    class ArcAlphaAdjustmentTarget(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ARC_ALPHA_ADJUSTMENT_TARGET_BEGINNING_OF_ARC: _ClassVar[CadLine.ArcAlphaAdjustmentTarget]
        ARC_ALPHA_ADJUSTMENT_TARGET_ARC_CONTROL_POINT: _ClassVar[CadLine.ArcAlphaAdjustmentTarget]
        ARC_ALPHA_ADJUSTMENT_TARGET_END_OF_ARC: _ClassVar[CadLine.ArcAlphaAdjustmentTarget]
    ARC_ALPHA_ADJUSTMENT_TARGET_BEGINNING_OF_ARC: CadLine.ArcAlphaAdjustmentTarget
    ARC_ALPHA_ADJUSTMENT_TARGET_ARC_CONTROL_POINT: CadLine.ArcAlphaAdjustmentTarget
    ARC_ALPHA_ADJUSTMENT_TARGET_END_OF_ARC: CadLine.ArcAlphaAdjustmentTarget
    class RotationSpecificationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ROTATION_SPECIFICATION_TYPE_BY_ANGLE: _ClassVar[CadLine.RotationSpecificationType]
        ROTATION_SPECIFICATION_TYPE_GLASS_COMPOSITION_MODEL: _ClassVar[CadLine.RotationSpecificationType]
        ROTATION_SPECIFICATION_TYPE_INSIDE: _ClassVar[CadLine.RotationSpecificationType]
        ROTATION_SPECIFICATION_TYPE_SURFACE: _ClassVar[CadLine.RotationSpecificationType]
        ROTATION_SPECIFICATION_TYPE_TO_NODE: _ClassVar[CadLine.RotationSpecificationType]
    ROTATION_SPECIFICATION_TYPE_BY_ANGLE: CadLine.RotationSpecificationType
    ROTATION_SPECIFICATION_TYPE_GLASS_COMPOSITION_MODEL: CadLine.RotationSpecificationType
    ROTATION_SPECIFICATION_TYPE_INSIDE: CadLine.RotationSpecificationType
    ROTATION_SPECIFICATION_TYPE_SURFACE: CadLine.RotationSpecificationType
    ROTATION_SPECIFICATION_TYPE_TO_NODE: CadLine.RotationSpecificationType
    class RotationPlane(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ROTATION_PLANE_XY: _ClassVar[CadLine.RotationPlane]
        ROTATION_PLANE_XZ: _ClassVar[CadLine.RotationPlane]
    ROTATION_PLANE_XY: CadLine.RotationPlane
    ROTATION_PLANE_XZ: CadLine.RotationPlane
    class ColorBy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        COLOR_BY_PROPERTY_BY_PARENT_LAYER: _ClassVar[CadLine.ColorBy]
        COLOR_BY_PROPERTY_BY_LINE: _ClassVar[CadLine.ColorBy]
    COLOR_BY_PROPERTY_BY_PARENT_LAYER: CadLine.ColorBy
    COLOR_BY_PROPERTY_BY_LINE: CadLine.ColorBy
    class LineTypeBy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LINE_TYPE_BY_PROPERTY_BY_PARENT_LAYER: _ClassVar[CadLine.LineTypeBy]
        LINE_TYPE_BY_PROPERTY_BY_LINE: _ClassVar[CadLine.LineTypeBy]
    LINE_TYPE_BY_PROPERTY_BY_PARENT_LAYER: CadLine.LineTypeBy
    LINE_TYPE_BY_PROPERTY_BY_LINE: CadLine.LineTypeBy
    class LineType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LINE_TYPE_SOLID: _ClassVar[CadLine.LineType]
        LINE_TYPE_DASHED: _ClassVar[CadLine.LineType]
        LINE_TYPE_DOTTED: _ClassVar[CadLine.LineType]
        LINE_TYPE_DOT_DASHED: _ClassVar[CadLine.LineType]
        LINE_TYPE_LOOSELY_DASHED: _ClassVar[CadLine.LineType]
    LINE_TYPE_SOLID: CadLine.LineType
    LINE_TYPE_DASHED: CadLine.LineType
    LINE_TYPE_DOTTED: CadLine.LineType
    LINE_TYPE_DOT_DASHED: CadLine.LineType
    LINE_TYPE_LOOSELY_DASHED: CadLine.LineType
    class LineThicknessBy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LINE_THICKNESS_BY_PROPERTY_BY_PARENT_LAYER: _ClassVar[CadLine.LineThicknessBy]
        LINE_THICKNESS_BY_PROPERTY_BY_LINE: _ClassVar[CadLine.LineThicknessBy]
    LINE_THICKNESS_BY_PROPERTY_BY_PARENT_LAYER: CadLine.LineThicknessBy
    LINE_THICKNESS_BY_PROPERTY_BY_LINE: CadLine.LineThicknessBy
    class NurbsControlPointsByComponentsTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[CadLine.NurbsControlPointsByComponentsRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[CadLine.NurbsControlPointsByComponentsRow, _Mapping]]] = ...) -> None: ...
    class NurbsControlPointsByComponentsRow(_message.Message):
        __slots__ = ("no", "description", "global_coordinate_x", "global_coordinate_y", "global_coordinate_z", "weight")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        GLOBAL_COORDINATE_X_FIELD_NUMBER: _ClassVar[int]
        GLOBAL_COORDINATE_Y_FIELD_NUMBER: _ClassVar[int]
        GLOBAL_COORDINATE_Z_FIELD_NUMBER: _ClassVar[int]
        WEIGHT_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        global_coordinate_x: float
        global_coordinate_y: float
        global_coordinate_z: float
        weight: float
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., global_coordinate_x: _Optional[float] = ..., global_coordinate_y: _Optional[float] = ..., global_coordinate_z: _Optional[float] = ..., weight: _Optional[float] = ...) -> None: ...
    class NurbsControlPointsTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[CadLine.NurbsControlPointsRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[CadLine.NurbsControlPointsRow, _Mapping]]] = ...) -> None: ...
    class NurbsControlPointsRow(_message.Message):
        __slots__ = ("no", "description", "control_point", "global_coordinates", "coordinates", "weight")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        CONTROL_POINT_FIELD_NUMBER: _ClassVar[int]
        GLOBAL_COORDINATES_FIELD_NUMBER: _ClassVar[int]
        COORDINATES_FIELD_NUMBER: _ClassVar[int]
        WEIGHT_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        control_point: int
        global_coordinates: _common_pb2.Vector3d
        coordinates: _common_pb2.Vector3d
        weight: float
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., control_point: _Optional[int] = ..., global_coordinates: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., coordinates: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., weight: _Optional[float] = ...) -> None: ...
    class NurbsKnotsTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[CadLine.NurbsKnotsRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[CadLine.NurbsKnotsRow, _Mapping]]] = ...) -> None: ...
    class NurbsKnotsRow(_message.Message):
        __slots__ = ("no", "description", "knot_value")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        KNOT_VALUE_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        knot_value: float
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., knot_value: _Optional[float] = ...) -> None: ...
    class DefinitionPointsTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[CadLine.DefinitionPointsRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[CadLine.DefinitionPointsRow, _Mapping]]] = ...) -> None: ...
    class DefinitionPointsRow(_message.Message):
        __slots__ = ("no", "description", "coordinate_x", "coordinate_y", "coordinate_z", "cad_line_point_no")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        COORDINATE_X_FIELD_NUMBER: _ClassVar[int]
        COORDINATE_Y_FIELD_NUMBER: _ClassVar[int]
        COORDINATE_Z_FIELD_NUMBER: _ClassVar[int]
        CAD_LINE_POINT_NO_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        coordinate_x: float
        coordinate_y: float
        coordinate_z: float
        cad_line_point_no: int
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., coordinate_x: _Optional[float] = ..., coordinate_y: _Optional[float] = ..., coordinate_z: _Optional[float] = ..., cad_line_point_no: _Optional[int] = ...) -> None: ...
    NO_FIELD_NUMBER: _ClassVar[int]
    DEFINITION_NODES_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    POSITION_SHORT_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    ARC_FIRST_NODE_FIELD_NUMBER: _ClassVar[int]
    ARC_SECOND_NODE_FIELD_NUMBER: _ClassVar[int]
    ARC_CONTROL_POINT_OBJECT_FIELD_NUMBER: _ClassVar[int]
    ARC_CONTROL_POINT_FIELD_NUMBER: _ClassVar[int]
    ARC_CONTROL_POINT_X_FIELD_NUMBER: _ClassVar[int]
    ARC_CONTROL_POINT_Y_FIELD_NUMBER: _ClassVar[int]
    ARC_CONTROL_POINT_Z_FIELD_NUMBER: _ClassVar[int]
    ARC_CENTER_FIELD_NUMBER: _ClassVar[int]
    ARC_CENTER_X_FIELD_NUMBER: _ClassVar[int]
    ARC_CENTER_Y_FIELD_NUMBER: _ClassVar[int]
    ARC_CENTER_Z_FIELD_NUMBER: _ClassVar[int]
    ARC_RADIUS_FIELD_NUMBER: _ClassVar[int]
    ARC_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    ARC_ALPHA_FIELD_NUMBER: _ClassVar[int]
    ARC_ALPHA_ADJUSTMENT_TARGET_FIELD_NUMBER: _ClassVar[int]
    CIRCLE_CENTER_FIELD_NUMBER: _ClassVar[int]
    CIRCLE_CENTER_COORDINATE_1_FIELD_NUMBER: _ClassVar[int]
    CIRCLE_CENTER_COORDINATE_2_FIELD_NUMBER: _ClassVar[int]
    CIRCLE_CENTER_COORDINATE_3_FIELD_NUMBER: _ClassVar[int]
    CIRCLE_NORMAL_FIELD_NUMBER: _ClassVar[int]
    CIRCLE_NORMAL_COORDINATE_1_FIELD_NUMBER: _ClassVar[int]
    CIRCLE_NORMAL_COORDINATE_2_FIELD_NUMBER: _ClassVar[int]
    CIRCLE_NORMAL_COORDINATE_3_FIELD_NUMBER: _ClassVar[int]
    CIRCLE_ROTATION_FIELD_NUMBER: _ClassVar[int]
    CIRCLE_NODE_FIELD_NUMBER: _ClassVar[int]
    CIRCLE_NODE_COORDINATE_1_FIELD_NUMBER: _ClassVar[int]
    CIRCLE_NODE_COORDINATE_2_FIELD_NUMBER: _ClassVar[int]
    CIRCLE_NODE_COORDINATE_3_FIELD_NUMBER: _ClassVar[int]
    CIRCLE_RADIUS_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_FIRST_NODE_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_SECOND_NODE_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_ALPHA_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_BETA_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_NORMAL_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_NORMAL_X_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_NORMAL_Y_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_NORMAL_Z_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_MAJOR_RADIUS_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_MINOR_RADIUS_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_CENTER_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_CENTER_X_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_CENTER_Y_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_CENTER_Z_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_FOCUS_1_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_FOCUS_1_X_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_FOCUS_1_Y_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_FOCUS_1_Z_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_FOCUS_2_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_FOCUS_2_X_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_FOCUS_2_Y_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_FOCUS_2_Z_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_FIRST_CONTROL_POINT_OBJECT_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_FIRST_CONTROL_POINT_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_FIRST_CONTROL_POINT_X_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_FIRST_CONTROL_POINT_Y_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_FIRST_CONTROL_POINT_Z_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_SECOND_CONTROL_POINT_OBJECT_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_SECOND_CONTROL_POINT_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_SECOND_CONTROL_POINT_X_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_SECOND_CONTROL_POINT_Y_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_SECOND_CONTROL_POINT_Z_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_PERIMETER_CONTROL_POINT_OBJECT_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_PERIMETER_CONTROL_POINT_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_PERIMETER_CONTROL_POINT_X_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_PERIMETER_CONTROL_POINT_Y_FIELD_NUMBER: _ClassVar[int]
    ELLIPTICAL_ARC_PERIMETER_CONTROL_POINT_Z_FIELD_NUMBER: _ClassVar[int]
    ELLIPSE_FIRST_NODE_FIELD_NUMBER: _ClassVar[int]
    ELLIPSE_SECOND_NODE_FIELD_NUMBER: _ClassVar[int]
    ELLIPSE_CONTROL_POINT_OBJECT_FIELD_NUMBER: _ClassVar[int]
    ELLIPSE_CONTROL_POINT_FIELD_NUMBER: _ClassVar[int]
    ELLIPSE_CONTROL_POINT_X_FIELD_NUMBER: _ClassVar[int]
    ELLIPSE_CONTROL_POINT_Y_FIELD_NUMBER: _ClassVar[int]
    ELLIPSE_CONTROL_POINT_Z_FIELD_NUMBER: _ClassVar[int]
    PARABOLA_FIRST_NODE_FIELD_NUMBER: _ClassVar[int]
    PARABOLA_SECOND_NODE_FIELD_NUMBER: _ClassVar[int]
    PARABOLA_CONTROL_POINT_OBJECT_FIELD_NUMBER: _ClassVar[int]
    PARABOLA_CONTROL_POINT_FIELD_NUMBER: _ClassVar[int]
    PARABOLA_CONTROL_POINT_X_FIELD_NUMBER: _ClassVar[int]
    PARABOLA_CONTROL_POINT_Y_FIELD_NUMBER: _ClassVar[int]
    PARABOLA_CONTROL_POINT_Z_FIELD_NUMBER: _ClassVar[int]
    PARABOLA_FOCUS_DIRECTRIX_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    PARABOLA_ALPHA_FIELD_NUMBER: _ClassVar[int]
    PARABOLA_FOCUS_FIELD_NUMBER: _ClassVar[int]
    PARABOLA_FOCUS_X_FIELD_NUMBER: _ClassVar[int]
    PARABOLA_FOCUS_Y_FIELD_NUMBER: _ClassVar[int]
    PARABOLA_FOCUS_Z_FIELD_NUMBER: _ClassVar[int]
    NURBS_ORDER_FIELD_NUMBER: _ClassVar[int]
    NURBS_CONTROL_POINTS_BY_COMPONENTS_FIELD_NUMBER: _ClassVar[int]
    NURBS_CONTROL_POINTS_FIELD_NUMBER: _ClassVar[int]
    NURBS_KNOTS_FIELD_NUMBER: _ClassVar[int]
    ROTATION_SPECIFICATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    ROTATION_ANGLE_FIELD_NUMBER: _ClassVar[int]
    ROTATION_HELP_NODE_FIELD_NUMBER: _ClassVar[int]
    ROTATION_PLANE_FIELD_NUMBER: _ClassVar[int]
    IS_ROTATED_FIELD_NUMBER: _ClassVar[int]
    PARENT_LAYER_FIELD_NUMBER: _ClassVar[int]
    IS_LOCKED_BY_PARENT_LAYER_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    COLOR_BY_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    LINE_TYPE_BY_FIELD_NUMBER: _ClassVar[int]
    LINE_TYPE_FIELD_NUMBER: _ClassVar[int]
    LINE_THICKNESS_BY_FIELD_NUMBER: _ClassVar[int]
    LINE_THICKNESS_FIELD_NUMBER: _ClassVar[int]
    START_POINT_FIELD_NUMBER: _ClassVar[int]
    START_POINT_COORDINATES_FIELD_NUMBER: _ClassVar[int]
    START_POINT_X_FIELD_NUMBER: _ClassVar[int]
    START_POINT_Y_FIELD_NUMBER: _ClassVar[int]
    START_POINT_Z_FIELD_NUMBER: _ClassVar[int]
    END_POINT_FIELD_NUMBER: _ClassVar[int]
    END_POINT_COORDINATES_FIELD_NUMBER: _ClassVar[int]
    END_POINT_X_FIELD_NUMBER: _ClassVar[int]
    END_POINT_Y_FIELD_NUMBER: _ClassVar[int]
    END_POINT_Z_FIELD_NUMBER: _ClassVar[int]
    DEFINITION_POINTS_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    definition_nodes: _containers.RepeatedScalarFieldContainer[int]
    type: CadLine.Type
    length: float
    position: str
    position_short: str
    comment: str
    arc_first_node: int
    arc_second_node: int
    arc_control_point_object: int
    arc_control_point: _common_pb2.Vector3d
    arc_control_point_x: float
    arc_control_point_y: float
    arc_control_point_z: float
    arc_center: _common_pb2.Vector3d
    arc_center_x: float
    arc_center_y: float
    arc_center_z: float
    arc_radius: float
    arc_height: float
    arc_alpha: float
    arc_alpha_adjustment_target: CadLine.ArcAlphaAdjustmentTarget
    circle_center: _common_pb2.Vector3d
    circle_center_coordinate_1: float
    circle_center_coordinate_2: float
    circle_center_coordinate_3: float
    circle_normal: _common_pb2.Vector3d
    circle_normal_coordinate_1: float
    circle_normal_coordinate_2: float
    circle_normal_coordinate_3: float
    circle_rotation: float
    circle_node: _common_pb2.Vector3d
    circle_node_coordinate_1: float
    circle_node_coordinate_2: float
    circle_node_coordinate_3: float
    circle_radius: float
    elliptical_arc_first_node: int
    elliptical_arc_second_node: int
    elliptical_arc_alpha: float
    elliptical_arc_beta: float
    elliptical_arc_normal: _common_pb2.Vector3d
    elliptical_arc_normal_x: float
    elliptical_arc_normal_y: float
    elliptical_arc_normal_z: float
    elliptical_arc_major_radius: float
    elliptical_arc_minor_radius: float
    elliptical_arc_center: _common_pb2.Vector3d
    elliptical_arc_center_x: float
    elliptical_arc_center_y: float
    elliptical_arc_center_z: float
    elliptical_arc_focus_1: _common_pb2.Vector3d
    elliptical_arc_focus_1_x: float
    elliptical_arc_focus_1_y: float
    elliptical_arc_focus_1_z: float
    elliptical_arc_focus_2: _common_pb2.Vector3d
    elliptical_arc_focus_2_x: float
    elliptical_arc_focus_2_y: float
    elliptical_arc_focus_2_z: float
    elliptical_arc_first_control_point_object: int
    elliptical_arc_first_control_point: _common_pb2.Vector3d
    elliptical_arc_first_control_point_x: float
    elliptical_arc_first_control_point_y: float
    elliptical_arc_first_control_point_z: float
    elliptical_arc_second_control_point_object: int
    elliptical_arc_second_control_point: _common_pb2.Vector3d
    elliptical_arc_second_control_point_x: float
    elliptical_arc_second_control_point_y: float
    elliptical_arc_second_control_point_z: float
    elliptical_arc_perimeter_control_point_object: int
    elliptical_arc_perimeter_control_point: _common_pb2.Vector3d
    elliptical_arc_perimeter_control_point_x: float
    elliptical_arc_perimeter_control_point_y: float
    elliptical_arc_perimeter_control_point_z: float
    ellipse_first_node: int
    ellipse_second_node: int
    ellipse_control_point_object: int
    ellipse_control_point: _common_pb2.Vector3d
    ellipse_control_point_x: float
    ellipse_control_point_y: float
    ellipse_control_point_z: float
    parabola_first_node: int
    parabola_second_node: int
    parabola_control_point_object: int
    parabola_control_point: _common_pb2.Vector3d
    parabola_control_point_x: float
    parabola_control_point_y: float
    parabola_control_point_z: float
    parabola_focus_directrix_distance: float
    parabola_alpha: float
    parabola_focus: _common_pb2.Vector3d
    parabola_focus_x: float
    parabola_focus_y: float
    parabola_focus_z: float
    nurbs_order: int
    nurbs_control_points_by_components: CadLine.NurbsControlPointsByComponentsTable
    nurbs_control_points: CadLine.NurbsControlPointsTable
    nurbs_knots: CadLine.NurbsKnotsTable
    rotation_specification_type: CadLine.RotationSpecificationType
    rotation_angle: float
    rotation_help_node: int
    rotation_plane: CadLine.RotationPlane
    is_rotated: bool
    parent_layer: int
    is_locked_by_parent_layer: bool
    is_generated: bool
    generating_object_info: str
    color_by: CadLine.ColorBy
    color: str
    line_type_by: CadLine.LineTypeBy
    line_type: CadLine.LineType
    line_thickness_by: CadLine.LineThicknessBy
    line_thickness: int
    start_point: int
    start_point_coordinates: _common_pb2.Vector3d
    start_point_x: float
    start_point_y: float
    start_point_z: float
    end_point: int
    end_point_coordinates: _common_pb2.Vector3d
    end_point_x: float
    end_point_y: float
    end_point_z: float
    definition_points: CadLine.DefinitionPointsTable
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., definition_nodes: _Optional[_Iterable[int]] = ..., type: _Optional[_Union[CadLine.Type, str]] = ..., length: _Optional[float] = ..., position: _Optional[str] = ..., position_short: _Optional[str] = ..., comment: _Optional[str] = ..., arc_first_node: _Optional[int] = ..., arc_second_node: _Optional[int] = ..., arc_control_point_object: _Optional[int] = ..., arc_control_point: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., arc_control_point_x: _Optional[float] = ..., arc_control_point_y: _Optional[float] = ..., arc_control_point_z: _Optional[float] = ..., arc_center: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., arc_center_x: _Optional[float] = ..., arc_center_y: _Optional[float] = ..., arc_center_z: _Optional[float] = ..., arc_radius: _Optional[float] = ..., arc_height: _Optional[float] = ..., arc_alpha: _Optional[float] = ..., arc_alpha_adjustment_target: _Optional[_Union[CadLine.ArcAlphaAdjustmentTarget, str]] = ..., circle_center: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., circle_center_coordinate_1: _Optional[float] = ..., circle_center_coordinate_2: _Optional[float] = ..., circle_center_coordinate_3: _Optional[float] = ..., circle_normal: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., circle_normal_coordinate_1: _Optional[float] = ..., circle_normal_coordinate_2: _Optional[float] = ..., circle_normal_coordinate_3: _Optional[float] = ..., circle_rotation: _Optional[float] = ..., circle_node: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., circle_node_coordinate_1: _Optional[float] = ..., circle_node_coordinate_2: _Optional[float] = ..., circle_node_coordinate_3: _Optional[float] = ..., circle_radius: _Optional[float] = ..., elliptical_arc_first_node: _Optional[int] = ..., elliptical_arc_second_node: _Optional[int] = ..., elliptical_arc_alpha: _Optional[float] = ..., elliptical_arc_beta: _Optional[float] = ..., elliptical_arc_normal: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., elliptical_arc_normal_x: _Optional[float] = ..., elliptical_arc_normal_y: _Optional[float] = ..., elliptical_arc_normal_z: _Optional[float] = ..., elliptical_arc_major_radius: _Optional[float] = ..., elliptical_arc_minor_radius: _Optional[float] = ..., elliptical_arc_center: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., elliptical_arc_center_x: _Optional[float] = ..., elliptical_arc_center_y: _Optional[float] = ..., elliptical_arc_center_z: _Optional[float] = ..., elliptical_arc_focus_1: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., elliptical_arc_focus_1_x: _Optional[float] = ..., elliptical_arc_focus_1_y: _Optional[float] = ..., elliptical_arc_focus_1_z: _Optional[float] = ..., elliptical_arc_focus_2: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., elliptical_arc_focus_2_x: _Optional[float] = ..., elliptical_arc_focus_2_y: _Optional[float] = ..., elliptical_arc_focus_2_z: _Optional[float] = ..., elliptical_arc_first_control_point_object: _Optional[int] = ..., elliptical_arc_first_control_point: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., elliptical_arc_first_control_point_x: _Optional[float] = ..., elliptical_arc_first_control_point_y: _Optional[float] = ..., elliptical_arc_first_control_point_z: _Optional[float] = ..., elliptical_arc_second_control_point_object: _Optional[int] = ..., elliptical_arc_second_control_point: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., elliptical_arc_second_control_point_x: _Optional[float] = ..., elliptical_arc_second_control_point_y: _Optional[float] = ..., elliptical_arc_second_control_point_z: _Optional[float] = ..., elliptical_arc_perimeter_control_point_object: _Optional[int] = ..., elliptical_arc_perimeter_control_point: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., elliptical_arc_perimeter_control_point_x: _Optional[float] = ..., elliptical_arc_perimeter_control_point_y: _Optional[float] = ..., elliptical_arc_perimeter_control_point_z: _Optional[float] = ..., ellipse_first_node: _Optional[int] = ..., ellipse_second_node: _Optional[int] = ..., ellipse_control_point_object: _Optional[int] = ..., ellipse_control_point: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., ellipse_control_point_x: _Optional[float] = ..., ellipse_control_point_y: _Optional[float] = ..., ellipse_control_point_z: _Optional[float] = ..., parabola_first_node: _Optional[int] = ..., parabola_second_node: _Optional[int] = ..., parabola_control_point_object: _Optional[int] = ..., parabola_control_point: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., parabola_control_point_x: _Optional[float] = ..., parabola_control_point_y: _Optional[float] = ..., parabola_control_point_z: _Optional[float] = ..., parabola_focus_directrix_distance: _Optional[float] = ..., parabola_alpha: _Optional[float] = ..., parabola_focus: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., parabola_focus_x: _Optional[float] = ..., parabola_focus_y: _Optional[float] = ..., parabola_focus_z: _Optional[float] = ..., nurbs_order: _Optional[int] = ..., nurbs_control_points_by_components: _Optional[_Union[CadLine.NurbsControlPointsByComponentsTable, _Mapping]] = ..., nurbs_control_points: _Optional[_Union[CadLine.NurbsControlPointsTable, _Mapping]] = ..., nurbs_knots: _Optional[_Union[CadLine.NurbsKnotsTable, _Mapping]] = ..., rotation_specification_type: _Optional[_Union[CadLine.RotationSpecificationType, str]] = ..., rotation_angle: _Optional[float] = ..., rotation_help_node: _Optional[int] = ..., rotation_plane: _Optional[_Union[CadLine.RotationPlane, str]] = ..., is_rotated: bool = ..., parent_layer: _Optional[int] = ..., is_locked_by_parent_layer: bool = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., color_by: _Optional[_Union[CadLine.ColorBy, str]] = ..., color: _Optional[str] = ..., line_type_by: _Optional[_Union[CadLine.LineTypeBy, str]] = ..., line_type: _Optional[_Union[CadLine.LineType, str]] = ..., line_thickness_by: _Optional[_Union[CadLine.LineThicknessBy, str]] = ..., line_thickness: _Optional[int] = ..., start_point: _Optional[int] = ..., start_point_coordinates: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., start_point_x: _Optional[float] = ..., start_point_y: _Optional[float] = ..., start_point_z: _Optional[float] = ..., end_point: _Optional[int] = ..., end_point_coordinates: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., end_point_x: _Optional[float] = ..., end_point_y: _Optional[float] = ..., end_point_z: _Optional[float] = ..., definition_points: _Optional[_Union[CadLine.DefinitionPointsTable, _Mapping]] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
