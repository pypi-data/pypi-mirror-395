from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CuttingPattern(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "material_change_enabled", "material", "pattern_orientation_category", "angular_rotation", "axis", "parralel_to_lines", "coordinate_system", "boundary_lines", "cutting_line_settings_table", "comment", "id_for_export_import", "metadata_for_export_import")
    class PatternOrientationCategory(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PATTERN_ORIENTATION_CATEGORY_ANGULAR_ROTATION: _ClassVar[CuttingPattern.PatternOrientationCategory]
        PATTERN_ORIENTATION_CATEGORY_PARALLEL_TO_COORDINATE_SYSTEM: _ClassVar[CuttingPattern.PatternOrientationCategory]
        PATTERN_ORIENTATION_CATEGORY_PARALLEL_TO_LINES: _ClassVar[CuttingPattern.PatternOrientationCategory]
    PATTERN_ORIENTATION_CATEGORY_ANGULAR_ROTATION: CuttingPattern.PatternOrientationCategory
    PATTERN_ORIENTATION_CATEGORY_PARALLEL_TO_COORDINATE_SYSTEM: CuttingPattern.PatternOrientationCategory
    PATTERN_ORIENTATION_CATEGORY_PARALLEL_TO_LINES: CuttingPattern.PatternOrientationCategory
    class Axis(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        AXIS_X: _ClassVar[CuttingPattern.Axis]
        AXIS_Y: _ClassVar[CuttingPattern.Axis]
    AXIS_X: CuttingPattern.Axis
    AXIS_Y: CuttingPattern.Axis
    class CuttingLineSettingsTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[CuttingPattern.CuttingLineSettingsTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[CuttingPattern.CuttingLineSettingsTableRow, _Mapping]]] = ...) -> None: ...
    class CuttingLineSettingsTableRow(_message.Message):
        __slots__ = ("no", "description", "line", "cutting_line_settings")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        LINE_FIELD_NUMBER: _ClassVar[int]
        CUTTING_LINE_SETTINGS_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        line: int
        cutting_line_settings: int
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., line: _Optional[int] = ..., cutting_line_settings: _Optional[int] = ...) -> None: ...
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    MATERIAL_CHANGE_ENABLED_FIELD_NUMBER: _ClassVar[int]
    MATERIAL_FIELD_NUMBER: _ClassVar[int]
    PATTERN_ORIENTATION_CATEGORY_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_ROTATION_FIELD_NUMBER: _ClassVar[int]
    AXIS_FIELD_NUMBER: _ClassVar[int]
    PARRALEL_TO_LINES_FIELD_NUMBER: _ClassVar[int]
    COORDINATE_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    BOUNDARY_LINES_FIELD_NUMBER: _ClassVar[int]
    CUTTING_LINE_SETTINGS_TABLE_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    material_change_enabled: bool
    material: int
    pattern_orientation_category: CuttingPattern.PatternOrientationCategory
    angular_rotation: float
    axis: CuttingPattern.Axis
    parralel_to_lines: _containers.RepeatedScalarFieldContainer[int]
    coordinate_system: int
    boundary_lines: _containers.RepeatedScalarFieldContainer[int]
    cutting_line_settings_table: CuttingPattern.CuttingLineSettingsTable
    comment: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., material_change_enabled: bool = ..., material: _Optional[int] = ..., pattern_orientation_category: _Optional[_Union[CuttingPattern.PatternOrientationCategory, str]] = ..., angular_rotation: _Optional[float] = ..., axis: _Optional[_Union[CuttingPattern.Axis, str]] = ..., parralel_to_lines: _Optional[_Iterable[int]] = ..., coordinate_system: _Optional[int] = ..., boundary_lines: _Optional[_Iterable[int]] = ..., cutting_line_settings_table: _Optional[_Union[CuttingPattern.CuttingLineSettingsTable, _Mapping]] = ..., comment: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
