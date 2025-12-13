from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CuttingPatternLoad(_message.Message):
    __slots__ = ("no", "load_type", "cutting_patterns", "cutting_patterns_and_lines", "load_case", "load_distribution", "magnitude_x", "magnitude_y", "magnitude", "comment", "load_graphic_position_below", "id_for_export_import", "metadata_for_export_import")
    class LoadType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LOAD_TYPE_UNKNOWN: _ClassVar[CuttingPatternLoad.LoadType]
        LOAD_TYPE_COMPENSATION: _ClassVar[CuttingPatternLoad.LoadType]
        LOAD_TYPE_EDGE_COMPENSATION: _ClassVar[CuttingPatternLoad.LoadType]
    LOAD_TYPE_UNKNOWN: CuttingPatternLoad.LoadType
    LOAD_TYPE_COMPENSATION: CuttingPatternLoad.LoadType
    LOAD_TYPE_EDGE_COMPENSATION: CuttingPatternLoad.LoadType
    class LoadDistribution(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LOAD_DISTRIBUTION_UNIFORM: _ClassVar[CuttingPatternLoad.LoadDistribution]
    LOAD_DISTRIBUTION_UNIFORM: CuttingPatternLoad.LoadDistribution
    NO_FIELD_NUMBER: _ClassVar[int]
    LOAD_TYPE_FIELD_NUMBER: _ClassVar[int]
    CUTTING_PATTERNS_FIELD_NUMBER: _ClassVar[int]
    CUTTING_PATTERNS_AND_LINES_FIELD_NUMBER: _ClassVar[int]
    LOAD_CASE_FIELD_NUMBER: _ClassVar[int]
    LOAD_DISTRIBUTION_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_X_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_Y_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    LOAD_GRAPHIC_POSITION_BELOW_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    load_type: CuttingPatternLoad.LoadType
    cutting_patterns: _containers.RepeatedScalarFieldContainer[int]
    cutting_patterns_and_lines: str
    load_case: int
    load_distribution: CuttingPatternLoad.LoadDistribution
    magnitude_x: float
    magnitude_y: float
    magnitude: float
    comment: str
    load_graphic_position_below: bool
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., load_type: _Optional[_Union[CuttingPatternLoad.LoadType, str]] = ..., cutting_patterns: _Optional[_Iterable[int]] = ..., cutting_patterns_and_lines: _Optional[str] = ..., load_case: _Optional[int] = ..., load_distribution: _Optional[_Union[CuttingPatternLoad.LoadDistribution, str]] = ..., magnitude_x: _Optional[float] = ..., magnitude_y: _Optional[float] = ..., magnitude: _Optional[float] = ..., comment: _Optional[str] = ..., load_graphic_position_below: bool = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
