from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SteelJoint(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "nodes", "stand_alone_point_x", "stand_alone_point_y", "stand_alone_point_z", "stand_alone_point", "members", "comment", "to_design", "nodes_to_design", "all_nodes_to_design", "components", "ultimate_configuration", "stiffness_analysis_configuration", "id_for_export_import", "metadata_for_export_import")
    class MembersTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelJoint.MembersRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelJoint.MembersRow, _Mapping]]] = ...) -> None: ...
    class MembersRow(_message.Message):
        __slots__ = ("no", "description", "is_active", "status", "members_no", "end_type", "supported", "comment", "errors", "sections_interaction", "stand_alone_cross_section", "stand_alone_position_definition_type", "stand_alone_displacement_x", "stand_alone_displacement_y", "stand_alone_displacement_z", "stand_alone_rotation_x", "stand_alone_rotation_y", "stand_alone_rotation_z")
        class EndType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            END_TYPE_UNKNOWN: _ClassVar[SteelJoint.MembersRow.EndType]
            END_TYPE_MEMBER_CONTINUOUS: _ClassVar[SteelJoint.MembersRow.EndType]
            END_TYPE_MEMBER_ENDED: _ClassVar[SteelJoint.MembersRow.EndType]
        END_TYPE_UNKNOWN: SteelJoint.MembersRow.EndType
        END_TYPE_MEMBER_CONTINUOUS: SteelJoint.MembersRow.EndType
        END_TYPE_MEMBER_ENDED: SteelJoint.MembersRow.EndType
        class SectionsInteraction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            SECTIONS_INTERACTION_UNKNOWN: _ClassVar[SteelJoint.MembersRow.SectionsInteraction]
        SECTIONS_INTERACTION_UNKNOWN: SteelJoint.MembersRow.SectionsInteraction
        class StandAlonePositionDefinitionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            STAND_ALONE_POSITION_DEFINITION_TYPE_ROTATION: _ClassVar[SteelJoint.MembersRow.StandAlonePositionDefinitionType]
        STAND_ALONE_POSITION_DEFINITION_TYPE_ROTATION: SteelJoint.MembersRow.StandAlonePositionDefinitionType
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
        STATUS_FIELD_NUMBER: _ClassVar[int]
        MEMBERS_NO_FIELD_NUMBER: _ClassVar[int]
        END_TYPE_FIELD_NUMBER: _ClassVar[int]
        SUPPORTED_FIELD_NUMBER: _ClassVar[int]
        COMMENT_FIELD_NUMBER: _ClassVar[int]
        ERRORS_FIELD_NUMBER: _ClassVar[int]
        SECTIONS_INTERACTION_FIELD_NUMBER: _ClassVar[int]
        STAND_ALONE_CROSS_SECTION_FIELD_NUMBER: _ClassVar[int]
        STAND_ALONE_POSITION_DEFINITION_TYPE_FIELD_NUMBER: _ClassVar[int]
        STAND_ALONE_DISPLACEMENT_X_FIELD_NUMBER: _ClassVar[int]
        STAND_ALONE_DISPLACEMENT_Y_FIELD_NUMBER: _ClassVar[int]
        STAND_ALONE_DISPLACEMENT_Z_FIELD_NUMBER: _ClassVar[int]
        STAND_ALONE_ROTATION_X_FIELD_NUMBER: _ClassVar[int]
        STAND_ALONE_ROTATION_Y_FIELD_NUMBER: _ClassVar[int]
        STAND_ALONE_ROTATION_Z_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        is_active: bool
        status: str
        members_no: _containers.RepeatedScalarFieldContainer[int]
        end_type: SteelJoint.MembersRow.EndType
        supported: bool
        comment: str
        errors: _common_pb2.Value
        sections_interaction: SteelJoint.MembersRow.SectionsInteraction
        stand_alone_cross_section: int
        stand_alone_position_definition_type: SteelJoint.MembersRow.StandAlonePositionDefinitionType
        stand_alone_displacement_x: float
        stand_alone_displacement_y: float
        stand_alone_displacement_z: float
        stand_alone_rotation_x: float
        stand_alone_rotation_y: float
        stand_alone_rotation_z: float
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., is_active: bool = ..., status: _Optional[str] = ..., members_no: _Optional[_Iterable[int]] = ..., end_type: _Optional[_Union[SteelJoint.MembersRow.EndType, str]] = ..., supported: bool = ..., comment: _Optional[str] = ..., errors: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., sections_interaction: _Optional[_Union[SteelJoint.MembersRow.SectionsInteraction, str]] = ..., stand_alone_cross_section: _Optional[int] = ..., stand_alone_position_definition_type: _Optional[_Union[SteelJoint.MembersRow.StandAlonePositionDefinitionType, str]] = ..., stand_alone_displacement_x: _Optional[float] = ..., stand_alone_displacement_y: _Optional[float] = ..., stand_alone_displacement_z: _Optional[float] = ..., stand_alone_rotation_x: _Optional[float] = ..., stand_alone_rotation_y: _Optional[float] = ..., stand_alone_rotation_z: _Optional[float] = ...) -> None: ...
    class ComponentsTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelJoint.ComponentsRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelJoint.ComponentsRow, _Mapping]]] = ...) -> None: ...
    class ComponentsRow(_message.Message):
        __slots__ = ("no", "description", "is_active", "type", "name", "settings_attributes", "errors")
        class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            TYPE_MEMBER_CUT: _ClassVar[SteelJoint.ComponentsRow.Type]
            TYPE_ANCHOR_BOLT: _ClassVar[SteelJoint.ComponentsRow.Type]
            TYPE_AUXILIARY_PLANE: _ClassVar[SteelJoint.ComponentsRow.Type]
            TYPE_AUXILIARY_SOLID: _ClassVar[SteelJoint.ComponentsRow.Type]
            TYPE_BASE_PLATE: _ClassVar[SteelJoint.ComponentsRow.Type]
            TYPE_BOLT: _ClassVar[SteelJoint.ComponentsRow.Type]
            TYPE_CAP_PLATE: _ClassVar[SteelJoint.ComponentsRow.Type]
            TYPE_CLEAT: _ClassVar[SteelJoint.ComponentsRow.Type]
            TYPE_CONCRETE_BLOCK: _ClassVar[SteelJoint.ComponentsRow.Type]
            TYPE_CONNECTING_PLATE: _ClassVar[SteelJoint.ComponentsRow.Type]
            TYPE_CONTACT: _ClassVar[SteelJoint.ComponentsRow.Type]
            TYPE_ELEMENTARY_WELD: _ClassVar[SteelJoint.ComponentsRow.Type]
            TYPE_END_PLATE: _ClassVar[SteelJoint.ComponentsRow.Type]
            TYPE_END_PLATE_TO_PLATE: _ClassVar[SteelJoint.ComponentsRow.Type]
            TYPE_FASTENER_GROUP: _ClassVar[SteelJoint.ComponentsRow.Type]
            TYPE_FIN_PLATE: _ClassVar[SteelJoint.ComponentsRow.Type]
            TYPE_HAUNCH: _ClassVar[SteelJoint.ComponentsRow.Type]
            TYPE_INSERTED_MEMBER: _ClassVar[SteelJoint.ComponentsRow.Type]
            TYPE_MEMBER: _ClassVar[SteelJoint.ComponentsRow.Type]
            TYPE_MEMBER_EDITOR: _ClassVar[SteelJoint.ComponentsRow.Type]
            TYPE_PLATE: _ClassVar[SteelJoint.ComponentsRow.Type]
            TYPE_PLATE_CUT: _ClassVar[SteelJoint.ComponentsRow.Type]
            TYPE_PLATE_EDITOR: _ClassVar[SteelJoint.ComponentsRow.Type]
            TYPE_PLATE_TO_PLATE: _ClassVar[SteelJoint.ComponentsRow.Type]
            TYPE_RIB: _ClassVar[SteelJoint.ComponentsRow.Type]
            TYPE_SECTION_ROUNDING: _ClassVar[SteelJoint.ComponentsRow.Type]
            TYPE_STIFFENER: _ClassVar[SteelJoint.ComponentsRow.Type]
            TYPE_STUB: _ClassVar[SteelJoint.ComponentsRow.Type]
        TYPE_MEMBER_CUT: SteelJoint.ComponentsRow.Type
        TYPE_ANCHOR_BOLT: SteelJoint.ComponentsRow.Type
        TYPE_AUXILIARY_PLANE: SteelJoint.ComponentsRow.Type
        TYPE_AUXILIARY_SOLID: SteelJoint.ComponentsRow.Type
        TYPE_BASE_PLATE: SteelJoint.ComponentsRow.Type
        TYPE_BOLT: SteelJoint.ComponentsRow.Type
        TYPE_CAP_PLATE: SteelJoint.ComponentsRow.Type
        TYPE_CLEAT: SteelJoint.ComponentsRow.Type
        TYPE_CONCRETE_BLOCK: SteelJoint.ComponentsRow.Type
        TYPE_CONNECTING_PLATE: SteelJoint.ComponentsRow.Type
        TYPE_CONTACT: SteelJoint.ComponentsRow.Type
        TYPE_ELEMENTARY_WELD: SteelJoint.ComponentsRow.Type
        TYPE_END_PLATE: SteelJoint.ComponentsRow.Type
        TYPE_END_PLATE_TO_PLATE: SteelJoint.ComponentsRow.Type
        TYPE_FASTENER_GROUP: SteelJoint.ComponentsRow.Type
        TYPE_FIN_PLATE: SteelJoint.ComponentsRow.Type
        TYPE_HAUNCH: SteelJoint.ComponentsRow.Type
        TYPE_INSERTED_MEMBER: SteelJoint.ComponentsRow.Type
        TYPE_MEMBER: SteelJoint.ComponentsRow.Type
        TYPE_MEMBER_EDITOR: SteelJoint.ComponentsRow.Type
        TYPE_PLATE: SteelJoint.ComponentsRow.Type
        TYPE_PLATE_CUT: SteelJoint.ComponentsRow.Type
        TYPE_PLATE_EDITOR: SteelJoint.ComponentsRow.Type
        TYPE_PLATE_TO_PLATE: SteelJoint.ComponentsRow.Type
        TYPE_RIB: SteelJoint.ComponentsRow.Type
        TYPE_SECTION_ROUNDING: SteelJoint.ComponentsRow.Type
        TYPE_STIFFENER: SteelJoint.ComponentsRow.Type
        TYPE_STUB: SteelJoint.ComponentsRow.Type
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        SETTINGS_ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
        ERRORS_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        is_active: bool
        type: SteelJoint.ComponentsRow.Type
        name: str
        settings_attributes: str
        errors: str
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., is_active: bool = ..., type: _Optional[_Union[SteelJoint.ComponentsRow.Type, str]] = ..., name: _Optional[str] = ..., settings_attributes: _Optional[str] = ..., errors: _Optional[str] = ...) -> None: ...
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NODES_FIELD_NUMBER: _ClassVar[int]
    STAND_ALONE_POINT_X_FIELD_NUMBER: _ClassVar[int]
    STAND_ALONE_POINT_Y_FIELD_NUMBER: _ClassVar[int]
    STAND_ALONE_POINT_Z_FIELD_NUMBER: _ClassVar[int]
    STAND_ALONE_POINT_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    TO_DESIGN_FIELD_NUMBER: _ClassVar[int]
    NODES_TO_DESIGN_FIELD_NUMBER: _ClassVar[int]
    ALL_NODES_TO_DESIGN_FIELD_NUMBER: _ClassVar[int]
    COMPONENTS_FIELD_NUMBER: _ClassVar[int]
    ULTIMATE_CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    STIFFNESS_ANALYSIS_CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    nodes: _containers.RepeatedScalarFieldContainer[int]
    stand_alone_point_x: float
    stand_alone_point_y: float
    stand_alone_point_z: float
    stand_alone_point: _common_pb2.Vector3d
    members: SteelJoint.MembersTable
    comment: str
    to_design: bool
    nodes_to_design: _containers.RepeatedScalarFieldContainer[int]
    all_nodes_to_design: bool
    components: SteelJoint.ComponentsTable
    ultimate_configuration: int
    stiffness_analysis_configuration: int
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., nodes: _Optional[_Iterable[int]] = ..., stand_alone_point_x: _Optional[float] = ..., stand_alone_point_y: _Optional[float] = ..., stand_alone_point_z: _Optional[float] = ..., stand_alone_point: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., members: _Optional[_Union[SteelJoint.MembersTable, _Mapping]] = ..., comment: _Optional[str] = ..., to_design: bool = ..., nodes_to_design: _Optional[_Iterable[int]] = ..., all_nodes_to_design: bool = ..., components: _Optional[_Union[SteelJoint.ComponentsTable, _Mapping]] = ..., ultimate_configuration: _Optional[int] = ..., stiffness_analysis_configuration: _Optional[int] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
