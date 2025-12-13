from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InnerStudsStructure(_message.Message):
    __slots__ = ("no", "type", "user_defined_name_enabled", "name", "section", "number_of_inner_studs", "spacing_definition_relative", "spacing_relative", "spacing_absolute", "offset_of_first_stud_absolute", "spacing_distribution_gap", "inner_studs_reverse_distribution", "inclination_relative_to_surface_y_axis", "comment", "thicknesses", "is_generated", "generating_object_info", "id_for_export_import", "metadata_for_export_import")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TYPE_UNKNOWN: _ClassVar[InnerStudsStructure.Type]
        TYPE_STANDARD: _ClassVar[InnerStudsStructure.Type]
    TYPE_UNKNOWN: InnerStudsStructure.Type
    TYPE_STANDARD: InnerStudsStructure.Type
    NO_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SECTION_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_INNER_STUDS_FIELD_NUMBER: _ClassVar[int]
    SPACING_DEFINITION_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    SPACING_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    SPACING_ABSOLUTE_FIELD_NUMBER: _ClassVar[int]
    OFFSET_OF_FIRST_STUD_ABSOLUTE_FIELD_NUMBER: _ClassVar[int]
    SPACING_DISTRIBUTION_GAP_FIELD_NUMBER: _ClassVar[int]
    INNER_STUDS_REVERSE_DISTRIBUTION_FIELD_NUMBER: _ClassVar[int]
    INCLINATION_RELATIVE_TO_SURFACE_Y_AXIS_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    THICKNESSES_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    type: InnerStudsStructure.Type
    user_defined_name_enabled: bool
    name: str
    section: int
    number_of_inner_studs: int
    spacing_definition_relative: bool
    spacing_relative: float
    spacing_absolute: float
    offset_of_first_stud_absolute: float
    spacing_distribution_gap: bool
    inner_studs_reverse_distribution: bool
    inclination_relative_to_surface_y_axis: float
    comment: str
    thicknesses: _containers.RepeatedScalarFieldContainer[int]
    is_generated: bool
    generating_object_info: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., type: _Optional[_Union[InnerStudsStructure.Type, str]] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., section: _Optional[int] = ..., number_of_inner_studs: _Optional[int] = ..., spacing_definition_relative: bool = ..., spacing_relative: _Optional[float] = ..., spacing_absolute: _Optional[float] = ..., offset_of_first_stud_absolute: _Optional[float] = ..., spacing_distribution_gap: bool = ..., inner_studs_reverse_distribution: bool = ..., inclination_relative_to_surface_y_axis: _Optional[float] = ..., comment: _Optional[str] = ..., thicknesses: _Optional[_Iterable[int]] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
