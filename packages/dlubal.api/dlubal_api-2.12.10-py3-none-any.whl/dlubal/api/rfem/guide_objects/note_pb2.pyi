from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Note(_message.Message):
    __slots__ = ("no", "type", "user_defined_name_enabled", "name", "text", "point_coordinate_x", "point_coordinate_y", "point_coordinate_z", "point_coordinates", "snap_position_coordinate_x", "snap_position_coordinate_y", "snap_position_coordinate_z", "snap_position_coordinates", "node", "cad_line_point", "member", "member_reference_type", "member_length", "member_distance_is_defined_as_relative", "member_distance_relative", "member_distance_absolute", "line", "line_length", "surface", "surface_reference_type", "surface_first_coordinate", "surface_second_coordinate", "solid", "solid_reference_type", "solid_first_coordinate", "solid_second_coordinate", "offset", "offset_type", "offset_coordinate_x", "offset_coordinate_y", "offset_coordinate_z", "offset_coordinate", "rotation", "show_comment", "display_properties_index", "comment", "parent_layer", "is_locked_by_parent_layer", "detail_note_parent_object", "id_for_export_import", "metadata_for_export_import")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TYPE_UNKNOWN: _ClassVar[Note.Type]
        TYPE_CAD_LINE_POINT: _ClassVar[Note.Type]
        TYPE_LINE: _ClassVar[Note.Type]
        TYPE_MEMBER: _ClassVar[Note.Type]
        TYPE_NODE: _ClassVar[Note.Type]
        TYPE_POINT: _ClassVar[Note.Type]
        TYPE_SNAP_POSITION: _ClassVar[Note.Type]
        TYPE_SOLID: _ClassVar[Note.Type]
        TYPE_SURFACE: _ClassVar[Note.Type]
    TYPE_UNKNOWN: Note.Type
    TYPE_CAD_LINE_POINT: Note.Type
    TYPE_LINE: Note.Type
    TYPE_MEMBER: Note.Type
    TYPE_NODE: Note.Type
    TYPE_POINT: Note.Type
    TYPE_SNAP_POSITION: Note.Type
    TYPE_SOLID: Note.Type
    TYPE_SURFACE: Note.Type
    class MemberReferenceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        MEMBER_REFERENCE_TYPE_L: _ClassVar[Note.MemberReferenceType]
        MEMBER_REFERENCE_TYPE_XY: _ClassVar[Note.MemberReferenceType]
        MEMBER_REFERENCE_TYPE_XZ: _ClassVar[Note.MemberReferenceType]
        MEMBER_REFERENCE_TYPE_YZ: _ClassVar[Note.MemberReferenceType]
    MEMBER_REFERENCE_TYPE_L: Note.MemberReferenceType
    MEMBER_REFERENCE_TYPE_XY: Note.MemberReferenceType
    MEMBER_REFERENCE_TYPE_XZ: Note.MemberReferenceType
    MEMBER_REFERENCE_TYPE_YZ: Note.MemberReferenceType
    class SurfaceReferenceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SURFACE_REFERENCE_TYPE_UNKNOWN: _ClassVar[Note.SurfaceReferenceType]
        SURFACE_REFERENCE_TYPE_XY: _ClassVar[Note.SurfaceReferenceType]
        SURFACE_REFERENCE_TYPE_XZ: _ClassVar[Note.SurfaceReferenceType]
        SURFACE_REFERENCE_TYPE_YZ: _ClassVar[Note.SurfaceReferenceType]
    SURFACE_REFERENCE_TYPE_UNKNOWN: Note.SurfaceReferenceType
    SURFACE_REFERENCE_TYPE_XY: Note.SurfaceReferenceType
    SURFACE_REFERENCE_TYPE_XZ: Note.SurfaceReferenceType
    SURFACE_REFERENCE_TYPE_YZ: Note.SurfaceReferenceType
    class SolidReferenceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SOLID_REFERENCE_TYPE_UNKNOWN: _ClassVar[Note.SolidReferenceType]
        SOLID_REFERENCE_TYPE_XY: _ClassVar[Note.SolidReferenceType]
        SOLID_REFERENCE_TYPE_XZ: _ClassVar[Note.SolidReferenceType]
        SOLID_REFERENCE_TYPE_YZ: _ClassVar[Note.SolidReferenceType]
    SOLID_REFERENCE_TYPE_UNKNOWN: Note.SolidReferenceType
    SOLID_REFERENCE_TYPE_XY: Note.SolidReferenceType
    SOLID_REFERENCE_TYPE_XZ: Note.SolidReferenceType
    SOLID_REFERENCE_TYPE_YZ: Note.SolidReferenceType
    class OffsetType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        OFFSET_TYPE_XYZ: _ClassVar[Note.OffsetType]
        OFFSET_TYPE_XY: _ClassVar[Note.OffsetType]
        OFFSET_TYPE_XZ: _ClassVar[Note.OffsetType]
        OFFSET_TYPE_YZ: _ClassVar[Note.OffsetType]
    OFFSET_TYPE_XYZ: Note.OffsetType
    OFFSET_TYPE_XY: Note.OffsetType
    OFFSET_TYPE_XZ: Note.OffsetType
    OFFSET_TYPE_YZ: Note.OffsetType
    NO_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    POINT_COORDINATE_X_FIELD_NUMBER: _ClassVar[int]
    POINT_COORDINATE_Y_FIELD_NUMBER: _ClassVar[int]
    POINT_COORDINATE_Z_FIELD_NUMBER: _ClassVar[int]
    POINT_COORDINATES_FIELD_NUMBER: _ClassVar[int]
    SNAP_POSITION_COORDINATE_X_FIELD_NUMBER: _ClassVar[int]
    SNAP_POSITION_COORDINATE_Y_FIELD_NUMBER: _ClassVar[int]
    SNAP_POSITION_COORDINATE_Z_FIELD_NUMBER: _ClassVar[int]
    SNAP_POSITION_COORDINATES_FIELD_NUMBER: _ClassVar[int]
    NODE_FIELD_NUMBER: _ClassVar[int]
    CAD_LINE_POINT_FIELD_NUMBER: _ClassVar[int]
    MEMBER_FIELD_NUMBER: _ClassVar[int]
    MEMBER_REFERENCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    MEMBER_LENGTH_FIELD_NUMBER: _ClassVar[int]
    MEMBER_DISTANCE_IS_DEFINED_AS_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    MEMBER_DISTANCE_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    MEMBER_DISTANCE_ABSOLUTE_FIELD_NUMBER: _ClassVar[int]
    LINE_FIELD_NUMBER: _ClassVar[int]
    LINE_LENGTH_FIELD_NUMBER: _ClassVar[int]
    SURFACE_FIELD_NUMBER: _ClassVar[int]
    SURFACE_REFERENCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SURFACE_FIRST_COORDINATE_FIELD_NUMBER: _ClassVar[int]
    SURFACE_SECOND_COORDINATE_FIELD_NUMBER: _ClassVar[int]
    SOLID_FIELD_NUMBER: _ClassVar[int]
    SOLID_REFERENCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SOLID_FIRST_COORDINATE_FIELD_NUMBER: _ClassVar[int]
    SOLID_SECOND_COORDINATE_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    OFFSET_TYPE_FIELD_NUMBER: _ClassVar[int]
    OFFSET_COORDINATE_X_FIELD_NUMBER: _ClassVar[int]
    OFFSET_COORDINATE_Y_FIELD_NUMBER: _ClassVar[int]
    OFFSET_COORDINATE_Z_FIELD_NUMBER: _ClassVar[int]
    OFFSET_COORDINATE_FIELD_NUMBER: _ClassVar[int]
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    SHOW_COMMENT_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_PROPERTIES_INDEX_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    PARENT_LAYER_FIELD_NUMBER: _ClassVar[int]
    IS_LOCKED_BY_PARENT_LAYER_FIELD_NUMBER: _ClassVar[int]
    DETAIL_NOTE_PARENT_OBJECT_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    type: Note.Type
    user_defined_name_enabled: bool
    name: str
    text: str
    point_coordinate_x: float
    point_coordinate_y: float
    point_coordinate_z: float
    point_coordinates: _common_pb2.Vector3d
    snap_position_coordinate_x: float
    snap_position_coordinate_y: float
    snap_position_coordinate_z: float
    snap_position_coordinates: _common_pb2.Vector3d
    node: int
    cad_line_point: int
    member: int
    member_reference_type: Note.MemberReferenceType
    member_length: float
    member_distance_is_defined_as_relative: bool
    member_distance_relative: float
    member_distance_absolute: float
    line: int
    line_length: float
    surface: int
    surface_reference_type: Note.SurfaceReferenceType
    surface_first_coordinate: float
    surface_second_coordinate: float
    solid: int
    solid_reference_type: Note.SolidReferenceType
    solid_first_coordinate: float
    solid_second_coordinate: float
    offset: bool
    offset_type: Note.OffsetType
    offset_coordinate_x: float
    offset_coordinate_y: float
    offset_coordinate_z: float
    offset_coordinate: _common_pb2.Vector3d
    rotation: float
    show_comment: bool
    display_properties_index: int
    comment: str
    parent_layer: int
    is_locked_by_parent_layer: bool
    detail_note_parent_object: int
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., type: _Optional[_Union[Note.Type, str]] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., text: _Optional[str] = ..., point_coordinate_x: _Optional[float] = ..., point_coordinate_y: _Optional[float] = ..., point_coordinate_z: _Optional[float] = ..., point_coordinates: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., snap_position_coordinate_x: _Optional[float] = ..., snap_position_coordinate_y: _Optional[float] = ..., snap_position_coordinate_z: _Optional[float] = ..., snap_position_coordinates: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., node: _Optional[int] = ..., cad_line_point: _Optional[int] = ..., member: _Optional[int] = ..., member_reference_type: _Optional[_Union[Note.MemberReferenceType, str]] = ..., member_length: _Optional[float] = ..., member_distance_is_defined_as_relative: bool = ..., member_distance_relative: _Optional[float] = ..., member_distance_absolute: _Optional[float] = ..., line: _Optional[int] = ..., line_length: _Optional[float] = ..., surface: _Optional[int] = ..., surface_reference_type: _Optional[_Union[Note.SurfaceReferenceType, str]] = ..., surface_first_coordinate: _Optional[float] = ..., surface_second_coordinate: _Optional[float] = ..., solid: _Optional[int] = ..., solid_reference_type: _Optional[_Union[Note.SolidReferenceType, str]] = ..., solid_first_coordinate: _Optional[float] = ..., solid_second_coordinate: _Optional[float] = ..., offset: bool = ..., offset_type: _Optional[_Union[Note.OffsetType, str]] = ..., offset_coordinate_x: _Optional[float] = ..., offset_coordinate_y: _Optional[float] = ..., offset_coordinate_z: _Optional[float] = ..., offset_coordinate: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., rotation: _Optional[float] = ..., show_comment: bool = ..., display_properties_index: _Optional[int] = ..., comment: _Optional[str] = ..., parent_layer: _Optional[int] = ..., is_locked_by_parent_layer: bool = ..., detail_note_parent_object: _Optional[int] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
