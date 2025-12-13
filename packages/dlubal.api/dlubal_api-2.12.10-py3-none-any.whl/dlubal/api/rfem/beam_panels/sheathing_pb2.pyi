from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Sheathing(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "thickness", "assigned_thicknesses", "rotation_of_input_axes", "sheathing_pattern", "sheathing_unit_width", "sheathing_unit_width_offset", "sheathing_unit_height", "sheathing_unit_height_offset", "reverse_horizontal", "reverse_vertical", "adjust_to_boundary_member_centerlines", "is_generated", "generating_object_info", "comment", "id_for_export_import", "metadata_for_export_import")
    class SheathingPattern(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SHEATHING_PATTERN_CASE_1: _ClassVar[Sheathing.SheathingPattern]
        SHEATHING_PATTERN_CASE_2: _ClassVar[Sheathing.SheathingPattern]
        SHEATHING_PATTERN_CASE_3: _ClassVar[Sheathing.SheathingPattern]
        SHEATHING_PATTERN_CASE_4: _ClassVar[Sheathing.SheathingPattern]
        SHEATHING_PATTERN_CASE_5: _ClassVar[Sheathing.SheathingPattern]
        SHEATHING_PATTERN_CASE_6: _ClassVar[Sheathing.SheathingPattern]
    SHEATHING_PATTERN_CASE_1: Sheathing.SheathingPattern
    SHEATHING_PATTERN_CASE_2: Sheathing.SheathingPattern
    SHEATHING_PATTERN_CASE_3: Sheathing.SheathingPattern
    SHEATHING_PATTERN_CASE_4: Sheathing.SheathingPattern
    SHEATHING_PATTERN_CASE_5: Sheathing.SheathingPattern
    SHEATHING_PATTERN_CASE_6: Sheathing.SheathingPattern
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    THICKNESS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_THICKNESSES_FIELD_NUMBER: _ClassVar[int]
    ROTATION_OF_INPUT_AXES_FIELD_NUMBER: _ClassVar[int]
    SHEATHING_PATTERN_FIELD_NUMBER: _ClassVar[int]
    SHEATHING_UNIT_WIDTH_FIELD_NUMBER: _ClassVar[int]
    SHEATHING_UNIT_WIDTH_OFFSET_FIELD_NUMBER: _ClassVar[int]
    SHEATHING_UNIT_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    SHEATHING_UNIT_HEIGHT_OFFSET_FIELD_NUMBER: _ClassVar[int]
    REVERSE_HORIZONTAL_FIELD_NUMBER: _ClassVar[int]
    REVERSE_VERTICAL_FIELD_NUMBER: _ClassVar[int]
    ADJUST_TO_BOUNDARY_MEMBER_CENTERLINES_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    thickness: int
    assigned_thicknesses: _containers.RepeatedScalarFieldContainer[int]
    rotation_of_input_axes: float
    sheathing_pattern: Sheathing.SheathingPattern
    sheathing_unit_width: float
    sheathing_unit_width_offset: float
    sheathing_unit_height: float
    sheathing_unit_height_offset: float
    reverse_horizontal: bool
    reverse_vertical: bool
    adjust_to_boundary_member_centerlines: bool
    is_generated: bool
    generating_object_info: str
    comment: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., thickness: _Optional[int] = ..., assigned_thicknesses: _Optional[_Iterable[int]] = ..., rotation_of_input_axes: _Optional[float] = ..., sheathing_pattern: _Optional[_Union[Sheathing.SheathingPattern, str]] = ..., sheathing_unit_width: _Optional[float] = ..., sheathing_unit_width_offset: _Optional[float] = ..., sheathing_unit_height: _Optional[float] = ..., sheathing_unit_height_offset: _Optional[float] = ..., reverse_horizontal: bool = ..., reverse_vertical: bool = ..., adjust_to_boundary_member_centerlines: bool = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., comment: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
