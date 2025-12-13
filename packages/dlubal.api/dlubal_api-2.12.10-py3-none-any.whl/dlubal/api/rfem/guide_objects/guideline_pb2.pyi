from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Guideline(_message.Message):
    __slots__ = ("no", "type", "name", "user_defined_name_enabled", "coordinate_system", "work_plane_orientation", "work_plane_offset", "parallel_to_work_plane_axis_offset", "by_two_points_first_point_x", "by_two_points_first_point_y", "by_two_points_second_point_x", "by_two_points_second_point_y", "by_point_and_angle_point_x", "by_point_and_angle_point_y", "by_point_and_angle_angle", "polar_center_x", "polar_center_y", "polar_radius", "label_type", "user_label", "is_locked", "glue_nodes_to_guideline", "comment", "id_for_export_import", "metadata_for_export_import")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TYPE_UNKNOWN: _ClassVar[Guideline.Type]
        TYPE_BY_POINT_AND_ANGLE: _ClassVar[Guideline.Type]
        TYPE_BY_TWO_POINTS: _ClassVar[Guideline.Type]
        TYPE_PARALLEL_TO_FIRST_WORK_PLANE_AXIS: _ClassVar[Guideline.Type]
        TYPE_PARALLEL_TO_SECOND_WORK_PLANE_AXIS: _ClassVar[Guideline.Type]
        TYPE_POLAR: _ClassVar[Guideline.Type]
    TYPE_UNKNOWN: Guideline.Type
    TYPE_BY_POINT_AND_ANGLE: Guideline.Type
    TYPE_BY_TWO_POINTS: Guideline.Type
    TYPE_PARALLEL_TO_FIRST_WORK_PLANE_AXIS: Guideline.Type
    TYPE_PARALLEL_TO_SECOND_WORK_PLANE_AXIS: Guideline.Type
    TYPE_POLAR: Guideline.Type
    class WorkPlaneOrientation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        WORK_PLANE_ORIENTATION_XY: _ClassVar[Guideline.WorkPlaneOrientation]
        WORK_PLANE_ORIENTATION_XZ: _ClassVar[Guideline.WorkPlaneOrientation]
        WORK_PLANE_ORIENTATION_YZ: _ClassVar[Guideline.WorkPlaneOrientation]
    WORK_PLANE_ORIENTATION_XY: Guideline.WorkPlaneOrientation
    WORK_PLANE_ORIENTATION_XZ: Guideline.WorkPlaneOrientation
    WORK_PLANE_ORIENTATION_YZ: Guideline.WorkPlaneOrientation
    class LabelType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LABEL_TYPE_NONE: _ClassVar[Guideline.LabelType]
        LABEL_TYPE_GUIDELINE_NUMBER: _ClassVar[Guideline.LabelType]
        LABEL_TYPE_USER_DEFINED: _ClassVar[Guideline.LabelType]
    LABEL_TYPE_NONE: Guideline.LabelType
    LABEL_TYPE_GUIDELINE_NUMBER: Guideline.LabelType
    LABEL_TYPE_USER_DEFINED: Guideline.LabelType
    NO_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    COORDINATE_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    WORK_PLANE_ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    WORK_PLANE_OFFSET_FIELD_NUMBER: _ClassVar[int]
    PARALLEL_TO_WORK_PLANE_AXIS_OFFSET_FIELD_NUMBER: _ClassVar[int]
    BY_TWO_POINTS_FIRST_POINT_X_FIELD_NUMBER: _ClassVar[int]
    BY_TWO_POINTS_FIRST_POINT_Y_FIELD_NUMBER: _ClassVar[int]
    BY_TWO_POINTS_SECOND_POINT_X_FIELD_NUMBER: _ClassVar[int]
    BY_TWO_POINTS_SECOND_POINT_Y_FIELD_NUMBER: _ClassVar[int]
    BY_POINT_AND_ANGLE_POINT_X_FIELD_NUMBER: _ClassVar[int]
    BY_POINT_AND_ANGLE_POINT_Y_FIELD_NUMBER: _ClassVar[int]
    BY_POINT_AND_ANGLE_ANGLE_FIELD_NUMBER: _ClassVar[int]
    POLAR_CENTER_X_FIELD_NUMBER: _ClassVar[int]
    POLAR_CENTER_Y_FIELD_NUMBER: _ClassVar[int]
    POLAR_RADIUS_FIELD_NUMBER: _ClassVar[int]
    LABEL_TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_LABEL_FIELD_NUMBER: _ClassVar[int]
    IS_LOCKED_FIELD_NUMBER: _ClassVar[int]
    GLUE_NODES_TO_GUIDELINE_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    type: Guideline.Type
    name: str
    user_defined_name_enabled: bool
    coordinate_system: int
    work_plane_orientation: Guideline.WorkPlaneOrientation
    work_plane_offset: float
    parallel_to_work_plane_axis_offset: float
    by_two_points_first_point_x: float
    by_two_points_first_point_y: float
    by_two_points_second_point_x: float
    by_two_points_second_point_y: float
    by_point_and_angle_point_x: float
    by_point_and_angle_point_y: float
    by_point_and_angle_angle: float
    polar_center_x: float
    polar_center_y: float
    polar_radius: float
    label_type: Guideline.LabelType
    user_label: str
    is_locked: bool
    glue_nodes_to_guideline: bool
    comment: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., type: _Optional[_Union[Guideline.Type, str]] = ..., name: _Optional[str] = ..., user_defined_name_enabled: bool = ..., coordinate_system: _Optional[int] = ..., work_plane_orientation: _Optional[_Union[Guideline.WorkPlaneOrientation, str]] = ..., work_plane_offset: _Optional[float] = ..., parallel_to_work_plane_axis_offset: _Optional[float] = ..., by_two_points_first_point_x: _Optional[float] = ..., by_two_points_first_point_y: _Optional[float] = ..., by_two_points_second_point_x: _Optional[float] = ..., by_two_points_second_point_y: _Optional[float] = ..., by_point_and_angle_point_x: _Optional[float] = ..., by_point_and_angle_point_y: _Optional[float] = ..., by_point_and_angle_angle: _Optional[float] = ..., polar_center_x: _Optional[float] = ..., polar_center_y: _Optional[float] = ..., polar_radius: _Optional[float] = ..., label_type: _Optional[_Union[Guideline.LabelType, str]] = ..., user_label: _Optional[str] = ..., is_locked: bool = ..., glue_nodes_to_guideline: bool = ..., comment: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
