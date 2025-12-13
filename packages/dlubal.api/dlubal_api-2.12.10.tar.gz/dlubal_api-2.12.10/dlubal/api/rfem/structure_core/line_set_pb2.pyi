from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LineSet(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "set_type", "lines", "length", "center_of_gravity", "center_of_gravity_x", "center_of_gravity_y", "center_of_gravity_z", "position", "position_short", "comment", "parent_layer", "is_locked_by_parent_layer", "is_generated", "generating_object_info", "design_properties_activated", "line_timber_design_uls_configuration", "line_timber_design_sls_configuration", "id_for_export_import", "metadata_for_export_import")
    class SetType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SET_TYPE_CONTINUOUS: _ClassVar[LineSet.SetType]
        SET_TYPE_GROUP: _ClassVar[LineSet.SetType]
    SET_TYPE_CONTINUOUS: LineSet.SetType
    SET_TYPE_GROUP: LineSet.SetType
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SET_TYPE_FIELD_NUMBER: _ClassVar[int]
    LINES_FIELD_NUMBER: _ClassVar[int]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    CENTER_OF_GRAVITY_FIELD_NUMBER: _ClassVar[int]
    CENTER_OF_GRAVITY_X_FIELD_NUMBER: _ClassVar[int]
    CENTER_OF_GRAVITY_Y_FIELD_NUMBER: _ClassVar[int]
    CENTER_OF_GRAVITY_Z_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    POSITION_SHORT_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    PARENT_LAYER_FIELD_NUMBER: _ClassVar[int]
    IS_LOCKED_BY_PARENT_LAYER_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    DESIGN_PROPERTIES_ACTIVATED_FIELD_NUMBER: _ClassVar[int]
    LINE_TIMBER_DESIGN_ULS_CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    LINE_TIMBER_DESIGN_SLS_CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    set_type: LineSet.SetType
    lines: _containers.RepeatedScalarFieldContainer[int]
    length: float
    center_of_gravity: _common_pb2.Vector3d
    center_of_gravity_x: float
    center_of_gravity_y: float
    center_of_gravity_z: float
    position: str
    position_short: str
    comment: str
    parent_layer: int
    is_locked_by_parent_layer: bool
    is_generated: bool
    generating_object_info: str
    design_properties_activated: bool
    line_timber_design_uls_configuration: int
    line_timber_design_sls_configuration: int
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., set_type: _Optional[_Union[LineSet.SetType, str]] = ..., lines: _Optional[_Iterable[int]] = ..., length: _Optional[float] = ..., center_of_gravity: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., center_of_gravity_x: _Optional[float] = ..., center_of_gravity_y: _Optional[float] = ..., center_of_gravity_z: _Optional[float] = ..., position: _Optional[str] = ..., position_short: _Optional[str] = ..., comment: _Optional[str] = ..., parent_layer: _Optional[int] = ..., is_locked_by_parent_layer: bool = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., design_properties_activated: bool = ..., line_timber_design_uls_configuration: _Optional[int] = ..., line_timber_design_sls_configuration: _Optional[int] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
