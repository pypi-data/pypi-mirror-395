from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DiagonalBrace(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "members", "member_sets", "components", "is_generated", "generating_object_info", "comment", "id_for_export_import", "metadata_for_export_import")
    class ComponentsTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[DiagonalBrace.ComponentsRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[DiagonalBrace.ComponentsRow, _Mapping]]] = ...) -> None: ...
    class ComponentsRow(_message.Message):
        __slots__ = ("no", "description", "brace_type", "position", "multiple", "note", "multiple_number", "multiple_offset_definition_type", "multiple_offset", "section_purlin", "span_between_purlins", "section_diagonal_brace", "span_between_purlins_with_diagonal_brace", "definition_type", "angle_between_purlin_and_brace", "vertical_projection_of_brace_length", "brace_length", "distance_of_connection_from_member_axis", "offset_of_brace_from_beam_axis")
        class BraceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            BRACE_TYPE_DIAGONAL_BRACE_COMPONENT_TYPE_PURLIN_WITH_DIAGONAL_BRACE: _ClassVar[DiagonalBrace.ComponentsRow.BraceType]
            BRACE_TYPE_DIAGONAL_BRACE_COMPONENT_TYPE_PURLIN: _ClassVar[DiagonalBrace.ComponentsRow.BraceType]
        BRACE_TYPE_DIAGONAL_BRACE_COMPONENT_TYPE_PURLIN_WITH_DIAGONAL_BRACE: DiagonalBrace.ComponentsRow.BraceType
        BRACE_TYPE_DIAGONAL_BRACE_COMPONENT_TYPE_PURLIN: DiagonalBrace.ComponentsRow.BraceType
        class MultipleOffsetDefinitionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            MULTIPLE_OFFSET_DEFINITION_TYPE_ABSOLUTE: _ClassVar[DiagonalBrace.ComponentsRow.MultipleOffsetDefinitionType]
            MULTIPLE_OFFSET_DEFINITION_TYPE_RELATIVE: _ClassVar[DiagonalBrace.ComponentsRow.MultipleOffsetDefinitionType]
        MULTIPLE_OFFSET_DEFINITION_TYPE_ABSOLUTE: DiagonalBrace.ComponentsRow.MultipleOffsetDefinitionType
        MULTIPLE_OFFSET_DEFINITION_TYPE_RELATIVE: DiagonalBrace.ComponentsRow.MultipleOffsetDefinitionType
        class DefinitionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            DEFINITION_TYPE_ALPHA_E_B: _ClassVar[DiagonalBrace.ComponentsRow.DefinitionType]
            DEFINITION_TYPE_ALPHA_LK_B: _ClassVar[DiagonalBrace.ComponentsRow.DefinitionType]
            DEFINITION_TYPE_ALPHA_LT_B: _ClassVar[DiagonalBrace.ComponentsRow.DefinitionType]
        DEFINITION_TYPE_ALPHA_E_B: DiagonalBrace.ComponentsRow.DefinitionType
        DEFINITION_TYPE_ALPHA_LK_B: DiagonalBrace.ComponentsRow.DefinitionType
        DEFINITION_TYPE_ALPHA_LT_B: DiagonalBrace.ComponentsRow.DefinitionType
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        BRACE_TYPE_FIELD_NUMBER: _ClassVar[int]
        POSITION_FIELD_NUMBER: _ClassVar[int]
        MULTIPLE_FIELD_NUMBER: _ClassVar[int]
        NOTE_FIELD_NUMBER: _ClassVar[int]
        MULTIPLE_NUMBER_FIELD_NUMBER: _ClassVar[int]
        MULTIPLE_OFFSET_DEFINITION_TYPE_FIELD_NUMBER: _ClassVar[int]
        MULTIPLE_OFFSET_FIELD_NUMBER: _ClassVar[int]
        SECTION_PURLIN_FIELD_NUMBER: _ClassVar[int]
        SPAN_BETWEEN_PURLINS_FIELD_NUMBER: _ClassVar[int]
        SECTION_DIAGONAL_BRACE_FIELD_NUMBER: _ClassVar[int]
        SPAN_BETWEEN_PURLINS_WITH_DIAGONAL_BRACE_FIELD_NUMBER: _ClassVar[int]
        DEFINITION_TYPE_FIELD_NUMBER: _ClassVar[int]
        ANGLE_BETWEEN_PURLIN_AND_BRACE_FIELD_NUMBER: _ClassVar[int]
        VERTICAL_PROJECTION_OF_BRACE_LENGTH_FIELD_NUMBER: _ClassVar[int]
        BRACE_LENGTH_FIELD_NUMBER: _ClassVar[int]
        DISTANCE_OF_CONNECTION_FROM_MEMBER_AXIS_FIELD_NUMBER: _ClassVar[int]
        OFFSET_OF_BRACE_FROM_BEAM_AXIS_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        brace_type: DiagonalBrace.ComponentsRow.BraceType
        position: float
        multiple: bool
        note: str
        multiple_number: int
        multiple_offset_definition_type: DiagonalBrace.ComponentsRow.MultipleOffsetDefinitionType
        multiple_offset: float
        section_purlin: int
        span_between_purlins: float
        section_diagonal_brace: int
        span_between_purlins_with_diagonal_brace: float
        definition_type: DiagonalBrace.ComponentsRow.DefinitionType
        angle_between_purlin_and_brace: float
        vertical_projection_of_brace_length: float
        brace_length: float
        distance_of_connection_from_member_axis: float
        offset_of_brace_from_beam_axis: float
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., brace_type: _Optional[_Union[DiagonalBrace.ComponentsRow.BraceType, str]] = ..., position: _Optional[float] = ..., multiple: bool = ..., note: _Optional[str] = ..., multiple_number: _Optional[int] = ..., multiple_offset_definition_type: _Optional[_Union[DiagonalBrace.ComponentsRow.MultipleOffsetDefinitionType, str]] = ..., multiple_offset: _Optional[float] = ..., section_purlin: _Optional[int] = ..., span_between_purlins: _Optional[float] = ..., section_diagonal_brace: _Optional[int] = ..., span_between_purlins_with_diagonal_brace: _Optional[float] = ..., definition_type: _Optional[_Union[DiagonalBrace.ComponentsRow.DefinitionType, str]] = ..., angle_between_purlin_and_brace: _Optional[float] = ..., vertical_projection_of_brace_length: _Optional[float] = ..., brace_length: _Optional[float] = ..., distance_of_connection_from_member_axis: _Optional[float] = ..., offset_of_brace_from_beam_axis: _Optional[float] = ...) -> None: ...
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    MEMBER_SETS_FIELD_NUMBER: _ClassVar[int]
    COMPONENTS_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    members: _containers.RepeatedScalarFieldContainer[int]
    member_sets: _containers.RepeatedScalarFieldContainer[int]
    components: DiagonalBrace.ComponentsTable
    is_generated: bool
    generating_object_info: str
    comment: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., members: _Optional[_Iterable[int]] = ..., member_sets: _Optional[_Iterable[int]] = ..., components: _Optional[_Union[DiagonalBrace.ComponentsTable, _Mapping]] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., comment: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
