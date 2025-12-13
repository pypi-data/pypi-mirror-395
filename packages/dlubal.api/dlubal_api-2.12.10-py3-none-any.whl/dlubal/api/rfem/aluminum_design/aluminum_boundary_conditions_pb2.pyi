from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AluminumBoundaryConditions(_message.Message):
    __slots__ = ("no", "definition_type", "coordinate_system", "user_defined_name_enabled", "name", "comment", "members", "member_sets", "deep_beams", "shear_walls", "nodal_supports", "member_hinges", "intermediate_nodes", "different_properties_supports", "different_properties_hinges", "is_generated", "generating_object_info", "id_for_export_import", "metadata_for_export_import")
    class DefinitionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DEFINITION_TYPE_UNKNOWN: _ClassVar[AluminumBoundaryConditions.DefinitionType]
        DEFINITION_TYPE_2D: _ClassVar[AluminumBoundaryConditions.DefinitionType]
    DEFINITION_TYPE_UNKNOWN: AluminumBoundaryConditions.DefinitionType
    DEFINITION_TYPE_2D: AluminumBoundaryConditions.DefinitionType
    class NodalSupportsTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[AluminumBoundaryConditions.NodalSupportsRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[AluminumBoundaryConditions.NodalSupportsRow, _Mapping]]] = ...) -> None: ...
    class NodalSupportsRow(_message.Message):
        __slots__ = ("no", "description", "node_seq_no", "support_type", "support_in_x", "support_in_y", "support_in_z", "restraint_about_x", "restraint_about_y", "restraint_about_z", "restraint_warping", "rotation", "rotation_about_x", "rotation_about_y", "rotation_about_z", "support_spring_in_x", "support_spring_in_y", "support_spring_in_z", "restraint_spring_about_x", "restraint_spring_about_y", "restraint_spring_about_z", "restraint_spring_warping", "eccentricity_type_z", "eccentricity_x", "eccentricity_y", "eccentricity_z", "nodes")
        class SupportType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            SUPPORT_TYPE_NONE: _ClassVar[AluminumBoundaryConditions.NodalSupportsRow.SupportType]
            SUPPORT_TYPE_FIXED_ALL: _ClassVar[AluminumBoundaryConditions.NodalSupportsRow.SupportType]
            SUPPORT_TYPE_FIXED_IN_Y: _ClassVar[AluminumBoundaryConditions.NodalSupportsRow.SupportType]
            SUPPORT_TYPE_FIXED_IN_Y_AND_TORSION: _ClassVar[AluminumBoundaryConditions.NodalSupportsRow.SupportType]
            SUPPORT_TYPE_FIXED_IN_Y_AND_TORSION_AND_WARPING: _ClassVar[AluminumBoundaryConditions.NodalSupportsRow.SupportType]
            SUPPORT_TYPE_FIXED_IN_Y_AND_WARPING: _ClassVar[AluminumBoundaryConditions.NodalSupportsRow.SupportType]
            SUPPORT_TYPE_INDIVIDUALLY: _ClassVar[AluminumBoundaryConditions.NodalSupportsRow.SupportType]
            SUPPORT_TYPE_TORSION: _ClassVar[AluminumBoundaryConditions.NodalSupportsRow.SupportType]
            SUPPORT_TYPE_TORSION_AND_WARPING: _ClassVar[AluminumBoundaryConditions.NodalSupportsRow.SupportType]
        SUPPORT_TYPE_NONE: AluminumBoundaryConditions.NodalSupportsRow.SupportType
        SUPPORT_TYPE_FIXED_ALL: AluminumBoundaryConditions.NodalSupportsRow.SupportType
        SUPPORT_TYPE_FIXED_IN_Y: AluminumBoundaryConditions.NodalSupportsRow.SupportType
        SUPPORT_TYPE_FIXED_IN_Y_AND_TORSION: AluminumBoundaryConditions.NodalSupportsRow.SupportType
        SUPPORT_TYPE_FIXED_IN_Y_AND_TORSION_AND_WARPING: AluminumBoundaryConditions.NodalSupportsRow.SupportType
        SUPPORT_TYPE_FIXED_IN_Y_AND_WARPING: AluminumBoundaryConditions.NodalSupportsRow.SupportType
        SUPPORT_TYPE_INDIVIDUALLY: AluminumBoundaryConditions.NodalSupportsRow.SupportType
        SUPPORT_TYPE_TORSION: AluminumBoundaryConditions.NodalSupportsRow.SupportType
        SUPPORT_TYPE_TORSION_AND_WARPING: AluminumBoundaryConditions.NodalSupportsRow.SupportType
        class EccentricityTypeZ(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            ECCENTRICITY_TYPE_Z_ECCENTRICITY_TYPE_NONE: _ClassVar[AluminumBoundaryConditions.NodalSupportsRow.EccentricityTypeZ]
            ECCENTRICITY_TYPE_Z_ECCENTRICITY_TYPE_AT_LOWER_FLANGE: _ClassVar[AluminumBoundaryConditions.NodalSupportsRow.EccentricityTypeZ]
            ECCENTRICITY_TYPE_Z_ECCENTRICITY_TYPE_AT_UPPER_FLANGE: _ClassVar[AluminumBoundaryConditions.NodalSupportsRow.EccentricityTypeZ]
            ECCENTRICITY_TYPE_Z_ECCENTRICITY_TYPE_USER_VALUE: _ClassVar[AluminumBoundaryConditions.NodalSupportsRow.EccentricityTypeZ]
        ECCENTRICITY_TYPE_Z_ECCENTRICITY_TYPE_NONE: AluminumBoundaryConditions.NodalSupportsRow.EccentricityTypeZ
        ECCENTRICITY_TYPE_Z_ECCENTRICITY_TYPE_AT_LOWER_FLANGE: AluminumBoundaryConditions.NodalSupportsRow.EccentricityTypeZ
        ECCENTRICITY_TYPE_Z_ECCENTRICITY_TYPE_AT_UPPER_FLANGE: AluminumBoundaryConditions.NodalSupportsRow.EccentricityTypeZ
        ECCENTRICITY_TYPE_Z_ECCENTRICITY_TYPE_USER_VALUE: AluminumBoundaryConditions.NodalSupportsRow.EccentricityTypeZ
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        NODE_SEQ_NO_FIELD_NUMBER: _ClassVar[int]
        SUPPORT_TYPE_FIELD_NUMBER: _ClassVar[int]
        SUPPORT_IN_X_FIELD_NUMBER: _ClassVar[int]
        SUPPORT_IN_Y_FIELD_NUMBER: _ClassVar[int]
        SUPPORT_IN_Z_FIELD_NUMBER: _ClassVar[int]
        RESTRAINT_ABOUT_X_FIELD_NUMBER: _ClassVar[int]
        RESTRAINT_ABOUT_Y_FIELD_NUMBER: _ClassVar[int]
        RESTRAINT_ABOUT_Z_FIELD_NUMBER: _ClassVar[int]
        RESTRAINT_WARPING_FIELD_NUMBER: _ClassVar[int]
        ROTATION_FIELD_NUMBER: _ClassVar[int]
        ROTATION_ABOUT_X_FIELD_NUMBER: _ClassVar[int]
        ROTATION_ABOUT_Y_FIELD_NUMBER: _ClassVar[int]
        ROTATION_ABOUT_Z_FIELD_NUMBER: _ClassVar[int]
        SUPPORT_SPRING_IN_X_FIELD_NUMBER: _ClassVar[int]
        SUPPORT_SPRING_IN_Y_FIELD_NUMBER: _ClassVar[int]
        SUPPORT_SPRING_IN_Z_FIELD_NUMBER: _ClassVar[int]
        RESTRAINT_SPRING_ABOUT_X_FIELD_NUMBER: _ClassVar[int]
        RESTRAINT_SPRING_ABOUT_Y_FIELD_NUMBER: _ClassVar[int]
        RESTRAINT_SPRING_ABOUT_Z_FIELD_NUMBER: _ClassVar[int]
        RESTRAINT_SPRING_WARPING_FIELD_NUMBER: _ClassVar[int]
        ECCENTRICITY_TYPE_Z_FIELD_NUMBER: _ClassVar[int]
        ECCENTRICITY_X_FIELD_NUMBER: _ClassVar[int]
        ECCENTRICITY_Y_FIELD_NUMBER: _ClassVar[int]
        ECCENTRICITY_Z_FIELD_NUMBER: _ClassVar[int]
        NODES_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        node_seq_no: str
        support_type: AluminumBoundaryConditions.NodalSupportsRow.SupportType
        support_in_x: bool
        support_in_y: bool
        support_in_z: bool
        restraint_about_x: bool
        restraint_about_y: bool
        restraint_about_z: bool
        restraint_warping: bool
        rotation: float
        rotation_about_x: float
        rotation_about_y: float
        rotation_about_z: float
        support_spring_in_x: float
        support_spring_in_y: float
        support_spring_in_z: float
        restraint_spring_about_x: float
        restraint_spring_about_y: float
        restraint_spring_about_z: float
        restraint_spring_warping: float
        eccentricity_type_z: AluminumBoundaryConditions.NodalSupportsRow.EccentricityTypeZ
        eccentricity_x: float
        eccentricity_y: float
        eccentricity_z: float
        nodes: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., node_seq_no: _Optional[str] = ..., support_type: _Optional[_Union[AluminumBoundaryConditions.NodalSupportsRow.SupportType, str]] = ..., support_in_x: bool = ..., support_in_y: bool = ..., support_in_z: bool = ..., restraint_about_x: bool = ..., restraint_about_y: bool = ..., restraint_about_z: bool = ..., restraint_warping: bool = ..., rotation: _Optional[float] = ..., rotation_about_x: _Optional[float] = ..., rotation_about_y: _Optional[float] = ..., rotation_about_z: _Optional[float] = ..., support_spring_in_x: _Optional[float] = ..., support_spring_in_y: _Optional[float] = ..., support_spring_in_z: _Optional[float] = ..., restraint_spring_about_x: _Optional[float] = ..., restraint_spring_about_y: _Optional[float] = ..., restraint_spring_about_z: _Optional[float] = ..., restraint_spring_warping: _Optional[float] = ..., eccentricity_type_z: _Optional[_Union[AluminumBoundaryConditions.NodalSupportsRow.EccentricityTypeZ, str]] = ..., eccentricity_x: _Optional[float] = ..., eccentricity_y: _Optional[float] = ..., eccentricity_z: _Optional[float] = ..., nodes: _Optional[_Iterable[int]] = ...) -> None: ...
    class MemberHingesTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[AluminumBoundaryConditions.MemberHingesRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[AluminumBoundaryConditions.MemberHingesRow, _Mapping]]] = ...) -> None: ...
    class MemberHingesRow(_message.Message):
        __slots__ = ("no", "description", "node_seq_no", "release_in_x", "release_in_y", "release_in_z", "release_about_x", "release_about_y", "release_about_z", "release_warping", "release_spring_in_x", "release_spring_in_y", "release_spring_in_z", "release_spring_about_x", "release_spring_about_y", "release_spring_about_z", "release_spring_warping", "nodes")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        NODE_SEQ_NO_FIELD_NUMBER: _ClassVar[int]
        RELEASE_IN_X_FIELD_NUMBER: _ClassVar[int]
        RELEASE_IN_Y_FIELD_NUMBER: _ClassVar[int]
        RELEASE_IN_Z_FIELD_NUMBER: _ClassVar[int]
        RELEASE_ABOUT_X_FIELD_NUMBER: _ClassVar[int]
        RELEASE_ABOUT_Y_FIELD_NUMBER: _ClassVar[int]
        RELEASE_ABOUT_Z_FIELD_NUMBER: _ClassVar[int]
        RELEASE_WARPING_FIELD_NUMBER: _ClassVar[int]
        RELEASE_SPRING_IN_X_FIELD_NUMBER: _ClassVar[int]
        RELEASE_SPRING_IN_Y_FIELD_NUMBER: _ClassVar[int]
        RELEASE_SPRING_IN_Z_FIELD_NUMBER: _ClassVar[int]
        RELEASE_SPRING_ABOUT_X_FIELD_NUMBER: _ClassVar[int]
        RELEASE_SPRING_ABOUT_Y_FIELD_NUMBER: _ClassVar[int]
        RELEASE_SPRING_ABOUT_Z_FIELD_NUMBER: _ClassVar[int]
        RELEASE_SPRING_WARPING_FIELD_NUMBER: _ClassVar[int]
        NODES_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        node_seq_no: str
        release_in_x: bool
        release_in_y: bool
        release_in_z: bool
        release_about_x: bool
        release_about_y: bool
        release_about_z: bool
        release_warping: bool
        release_spring_in_x: float
        release_spring_in_y: float
        release_spring_in_z: float
        release_spring_about_x: float
        release_spring_about_y: float
        release_spring_about_z: float
        release_spring_warping: float
        nodes: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., node_seq_no: _Optional[str] = ..., release_in_x: bool = ..., release_in_y: bool = ..., release_in_z: bool = ..., release_about_x: bool = ..., release_about_y: bool = ..., release_about_z: bool = ..., release_warping: bool = ..., release_spring_in_x: _Optional[float] = ..., release_spring_in_y: _Optional[float] = ..., release_spring_in_z: _Optional[float] = ..., release_spring_about_x: _Optional[float] = ..., release_spring_about_y: _Optional[float] = ..., release_spring_about_z: _Optional[float] = ..., release_spring_warping: _Optional[float] = ..., nodes: _Optional[_Iterable[int]] = ...) -> None: ...
    NO_FIELD_NUMBER: _ClassVar[int]
    DEFINITION_TYPE_FIELD_NUMBER: _ClassVar[int]
    COORDINATE_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    MEMBER_SETS_FIELD_NUMBER: _ClassVar[int]
    DEEP_BEAMS_FIELD_NUMBER: _ClassVar[int]
    SHEAR_WALLS_FIELD_NUMBER: _ClassVar[int]
    NODAL_SUPPORTS_FIELD_NUMBER: _ClassVar[int]
    MEMBER_HINGES_FIELD_NUMBER: _ClassVar[int]
    INTERMEDIATE_NODES_FIELD_NUMBER: _ClassVar[int]
    DIFFERENT_PROPERTIES_SUPPORTS_FIELD_NUMBER: _ClassVar[int]
    DIFFERENT_PROPERTIES_HINGES_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    definition_type: AluminumBoundaryConditions.DefinitionType
    coordinate_system: _common_pb2.CoordinateSystemRepresentation
    user_defined_name_enabled: bool
    name: str
    comment: str
    members: _containers.RepeatedScalarFieldContainer[int]
    member_sets: _containers.RepeatedScalarFieldContainer[int]
    deep_beams: _containers.RepeatedScalarFieldContainer[int]
    shear_walls: _containers.RepeatedScalarFieldContainer[int]
    nodal_supports: AluminumBoundaryConditions.NodalSupportsTable
    member_hinges: AluminumBoundaryConditions.MemberHingesTable
    intermediate_nodes: bool
    different_properties_supports: bool
    different_properties_hinges: bool
    is_generated: bool
    generating_object_info: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., definition_type: _Optional[_Union[AluminumBoundaryConditions.DefinitionType, str]] = ..., coordinate_system: _Optional[_Union[_common_pb2.CoordinateSystemRepresentation, _Mapping]] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., comment: _Optional[str] = ..., members: _Optional[_Iterable[int]] = ..., member_sets: _Optional[_Iterable[int]] = ..., deep_beams: _Optional[_Iterable[int]] = ..., shear_walls: _Optional[_Iterable[int]] = ..., nodal_supports: _Optional[_Union[AluminumBoundaryConditions.NodalSupportsTable, _Mapping]] = ..., member_hinges: _Optional[_Union[AluminumBoundaryConditions.MemberHingesTable, _Mapping]] = ..., intermediate_nodes: bool = ..., different_properties_supports: bool = ..., different_properties_hinges: bool = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
