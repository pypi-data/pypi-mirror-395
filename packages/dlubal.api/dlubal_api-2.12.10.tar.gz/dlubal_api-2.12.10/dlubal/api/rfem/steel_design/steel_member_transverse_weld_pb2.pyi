from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SteelMemberTransverseWeld(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "members", "member_sets", "deep_beams", "shear_walls", "components", "is_generated", "generating_object_info", "comment", "id_for_export_import", "metadata_for_export_import")
    class ComponentsTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelMemberTransverseWeld.ComponentsRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelMemberTransverseWeld.ComponentsRow, _Mapping]]] = ...) -> None: ...
    class ComponentsRow(_message.Message):
        __slots__ = ("no", "description", "weld_type", "position", "multiple", "note", "multiple_number", "multiple_offset_definition_type", "multiple_offset", "size", "method_ec_or_adm", "method_gb", "number_of_heat_paths", "temperature_of_material_between_welding_cycles")
        class WeldType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            WELD_TYPE_WELD_COMPONENT_TYPE_BUTT: _ClassVar[SteelMemberTransverseWeld.ComponentsRow.WeldType]
            WELD_TYPE_WELD_COMPONENT_TYPE_FILLET: _ClassVar[SteelMemberTransverseWeld.ComponentsRow.WeldType]
        WELD_TYPE_WELD_COMPONENT_TYPE_BUTT: SteelMemberTransverseWeld.ComponentsRow.WeldType
        WELD_TYPE_WELD_COMPONENT_TYPE_FILLET: SteelMemberTransverseWeld.ComponentsRow.WeldType
        class MultipleOffsetDefinitionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            MULTIPLE_OFFSET_DEFINITION_TYPE_ABSOLUTE: _ClassVar[SteelMemberTransverseWeld.ComponentsRow.MultipleOffsetDefinitionType]
            MULTIPLE_OFFSET_DEFINITION_TYPE_RELATIVE: _ClassVar[SteelMemberTransverseWeld.ComponentsRow.MultipleOffsetDefinitionType]
        MULTIPLE_OFFSET_DEFINITION_TYPE_ABSOLUTE: SteelMemberTransverseWeld.ComponentsRow.MultipleOffsetDefinitionType
        MULTIPLE_OFFSET_DEFINITION_TYPE_RELATIVE: SteelMemberTransverseWeld.ComponentsRow.MultipleOffsetDefinitionType
        class MethodEcOrAdm(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            METHOD_EC_OR_ADM_WELDING_METHOD_TIG: _ClassVar[SteelMemberTransverseWeld.ComponentsRow.MethodEcOrAdm]
            METHOD_EC_OR_ADM_WELDING_METHOD_MIG: _ClassVar[SteelMemberTransverseWeld.ComponentsRow.MethodEcOrAdm]
        METHOD_EC_OR_ADM_WELDING_METHOD_TIG: SteelMemberTransverseWeld.ComponentsRow.MethodEcOrAdm
        METHOD_EC_OR_ADM_WELDING_METHOD_MIG: SteelMemberTransverseWeld.ComponentsRow.MethodEcOrAdm
        class MethodGb(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            METHOD_GB_WELDING_METHOD_SMAW: _ClassVar[SteelMemberTransverseWeld.ComponentsRow.MethodGb]
            METHOD_GB_WELDING_METHOD_FCAW: _ClassVar[SteelMemberTransverseWeld.ComponentsRow.MethodGb]
            METHOD_GB_WELDING_METHOD_FCAW_S: _ClassVar[SteelMemberTransverseWeld.ComponentsRow.MethodGb]
            METHOD_GB_WELDING_METHOD_GMAW: _ClassVar[SteelMemberTransverseWeld.ComponentsRow.MethodGb]
            METHOD_GB_WELDING_METHOD_GTAW: _ClassVar[SteelMemberTransverseWeld.ComponentsRow.MethodGb]
            METHOD_GB_WELDING_METHOD_SAW: _ClassVar[SteelMemberTransverseWeld.ComponentsRow.MethodGb]
        METHOD_GB_WELDING_METHOD_SMAW: SteelMemberTransverseWeld.ComponentsRow.MethodGb
        METHOD_GB_WELDING_METHOD_FCAW: SteelMemberTransverseWeld.ComponentsRow.MethodGb
        METHOD_GB_WELDING_METHOD_FCAW_S: SteelMemberTransverseWeld.ComponentsRow.MethodGb
        METHOD_GB_WELDING_METHOD_GMAW: SteelMemberTransverseWeld.ComponentsRow.MethodGb
        METHOD_GB_WELDING_METHOD_GTAW: SteelMemberTransverseWeld.ComponentsRow.MethodGb
        METHOD_GB_WELDING_METHOD_SAW: SteelMemberTransverseWeld.ComponentsRow.MethodGb
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        WELD_TYPE_FIELD_NUMBER: _ClassVar[int]
        POSITION_FIELD_NUMBER: _ClassVar[int]
        MULTIPLE_FIELD_NUMBER: _ClassVar[int]
        NOTE_FIELD_NUMBER: _ClassVar[int]
        MULTIPLE_NUMBER_FIELD_NUMBER: _ClassVar[int]
        MULTIPLE_OFFSET_DEFINITION_TYPE_FIELD_NUMBER: _ClassVar[int]
        MULTIPLE_OFFSET_FIELD_NUMBER: _ClassVar[int]
        SIZE_FIELD_NUMBER: _ClassVar[int]
        METHOD_EC_OR_ADM_FIELD_NUMBER: _ClassVar[int]
        METHOD_GB_FIELD_NUMBER: _ClassVar[int]
        NUMBER_OF_HEAT_PATHS_FIELD_NUMBER: _ClassVar[int]
        TEMPERATURE_OF_MATERIAL_BETWEEN_WELDING_CYCLES_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        weld_type: SteelMemberTransverseWeld.ComponentsRow.WeldType
        position: float
        multiple: bool
        note: str
        multiple_number: int
        multiple_offset_definition_type: SteelMemberTransverseWeld.ComponentsRow.MultipleOffsetDefinitionType
        multiple_offset: float
        size: float
        method_ec_or_adm: SteelMemberTransverseWeld.ComponentsRow.MethodEcOrAdm
        method_gb: SteelMemberTransverseWeld.ComponentsRow.MethodGb
        number_of_heat_paths: int
        temperature_of_material_between_welding_cycles: float
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., weld_type: _Optional[_Union[SteelMemberTransverseWeld.ComponentsRow.WeldType, str]] = ..., position: _Optional[float] = ..., multiple: bool = ..., note: _Optional[str] = ..., multiple_number: _Optional[int] = ..., multiple_offset_definition_type: _Optional[_Union[SteelMemberTransverseWeld.ComponentsRow.MultipleOffsetDefinitionType, str]] = ..., multiple_offset: _Optional[float] = ..., size: _Optional[float] = ..., method_ec_or_adm: _Optional[_Union[SteelMemberTransverseWeld.ComponentsRow.MethodEcOrAdm, str]] = ..., method_gb: _Optional[_Union[SteelMemberTransverseWeld.ComponentsRow.MethodGb, str]] = ..., number_of_heat_paths: _Optional[int] = ..., temperature_of_material_between_welding_cycles: _Optional[float] = ...) -> None: ...
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    MEMBER_SETS_FIELD_NUMBER: _ClassVar[int]
    DEEP_BEAMS_FIELD_NUMBER: _ClassVar[int]
    SHEAR_WALLS_FIELD_NUMBER: _ClassVar[int]
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
    deep_beams: _containers.RepeatedScalarFieldContainer[int]
    shear_walls: _containers.RepeatedScalarFieldContainer[int]
    components: SteelMemberTransverseWeld.ComponentsTable
    is_generated: bool
    generating_object_info: str
    comment: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., members: _Optional[_Iterable[int]] = ..., member_sets: _Optional[_Iterable[int]] = ..., deep_beams: _Optional[_Iterable[int]] = ..., shear_walls: _Optional[_Iterable[int]] = ..., components: _Optional[_Union[SteelMemberTransverseWeld.ComponentsTable, _Mapping]] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., comment: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
