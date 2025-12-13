from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RoughnessAndPermeability(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "assigned_members", "assigned_surfaces", "assigned_solids", "assigned_visual_objects", "assigned_ifc_objects", "type_of_surface", "sand_grain_roughness_definition", "height_of_sand_grain_roughness", "roughness_constant", "darcy_coefficient", "inertial_coefficient", "porous_media_length_in_flow_direction", "comment", "id_for_export_import", "metadata_for_export_import")
    class TypeOfSurface(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TYPE_OF_SURFACE_SMOOTH: _ClassVar[RoughnessAndPermeability.TypeOfSurface]
        TYPE_OF_SURFACE_PERMEABLE: _ClassVar[RoughnessAndPermeability.TypeOfSurface]
        TYPE_OF_SURFACE_ROUGH: _ClassVar[RoughnessAndPermeability.TypeOfSurface]
    TYPE_OF_SURFACE_SMOOTH: RoughnessAndPermeability.TypeOfSurface
    TYPE_OF_SURFACE_PERMEABLE: RoughnessAndPermeability.TypeOfSurface
    TYPE_OF_SURFACE_ROUGH: RoughnessAndPermeability.TypeOfSurface
    class SandGrainRoughnessDefinition(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SAND_GRAIN_ROUGHNESS_DEFINITION_MANUAL_DEFINITION: _ClassVar[RoughnessAndPermeability.SandGrainRoughnessDefinition]
        SAND_GRAIN_ROUGHNESS_DEFINITION_BRICKWORK: _ClassVar[RoughnessAndPermeability.SandGrainRoughnessDefinition]
        SAND_GRAIN_ROUGHNESS_DEFINITION_BRIGHT_STEEL: _ClassVar[RoughnessAndPermeability.SandGrainRoughnessDefinition]
        SAND_GRAIN_ROUGHNESS_DEFINITION_CAST_IRON: _ClassVar[RoughnessAndPermeability.SandGrainRoughnessDefinition]
        SAND_GRAIN_ROUGHNESS_DEFINITION_FINE_PAINT: _ClassVar[RoughnessAndPermeability.SandGrainRoughnessDefinition]
        SAND_GRAIN_ROUGHNESS_DEFINITION_GALVANISED_STEEL: _ClassVar[RoughnessAndPermeability.SandGrainRoughnessDefinition]
        SAND_GRAIN_ROUGHNESS_DEFINITION_GLASS: _ClassVar[RoughnessAndPermeability.SandGrainRoughnessDefinition]
        SAND_GRAIN_ROUGHNESS_DEFINITION_PLANED_WOOD: _ClassVar[RoughnessAndPermeability.SandGrainRoughnessDefinition]
        SAND_GRAIN_ROUGHNESS_DEFINITION_POLISHED_METAL: _ClassVar[RoughnessAndPermeability.SandGrainRoughnessDefinition]
        SAND_GRAIN_ROUGHNESS_DEFINITION_ROUGH_CONCRETE: _ClassVar[RoughnessAndPermeability.SandGrainRoughnessDefinition]
        SAND_GRAIN_ROUGHNESS_DEFINITION_ROUGH_SAWN_WOOD: _ClassVar[RoughnessAndPermeability.SandGrainRoughnessDefinition]
        SAND_GRAIN_ROUGHNESS_DEFINITION_RUST: _ClassVar[RoughnessAndPermeability.SandGrainRoughnessDefinition]
        SAND_GRAIN_ROUGHNESS_DEFINITION_SMOOTH_CONCRETE: _ClassVar[RoughnessAndPermeability.SandGrainRoughnessDefinition]
        SAND_GRAIN_ROUGHNESS_DEFINITION_SPRAY_PAINT: _ClassVar[RoughnessAndPermeability.SandGrainRoughnessDefinition]
    SAND_GRAIN_ROUGHNESS_DEFINITION_MANUAL_DEFINITION: RoughnessAndPermeability.SandGrainRoughnessDefinition
    SAND_GRAIN_ROUGHNESS_DEFINITION_BRICKWORK: RoughnessAndPermeability.SandGrainRoughnessDefinition
    SAND_GRAIN_ROUGHNESS_DEFINITION_BRIGHT_STEEL: RoughnessAndPermeability.SandGrainRoughnessDefinition
    SAND_GRAIN_ROUGHNESS_DEFINITION_CAST_IRON: RoughnessAndPermeability.SandGrainRoughnessDefinition
    SAND_GRAIN_ROUGHNESS_DEFINITION_FINE_PAINT: RoughnessAndPermeability.SandGrainRoughnessDefinition
    SAND_GRAIN_ROUGHNESS_DEFINITION_GALVANISED_STEEL: RoughnessAndPermeability.SandGrainRoughnessDefinition
    SAND_GRAIN_ROUGHNESS_DEFINITION_GLASS: RoughnessAndPermeability.SandGrainRoughnessDefinition
    SAND_GRAIN_ROUGHNESS_DEFINITION_PLANED_WOOD: RoughnessAndPermeability.SandGrainRoughnessDefinition
    SAND_GRAIN_ROUGHNESS_DEFINITION_POLISHED_METAL: RoughnessAndPermeability.SandGrainRoughnessDefinition
    SAND_GRAIN_ROUGHNESS_DEFINITION_ROUGH_CONCRETE: RoughnessAndPermeability.SandGrainRoughnessDefinition
    SAND_GRAIN_ROUGHNESS_DEFINITION_ROUGH_SAWN_WOOD: RoughnessAndPermeability.SandGrainRoughnessDefinition
    SAND_GRAIN_ROUGHNESS_DEFINITION_RUST: RoughnessAndPermeability.SandGrainRoughnessDefinition
    SAND_GRAIN_ROUGHNESS_DEFINITION_SMOOTH_CONCRETE: RoughnessAndPermeability.SandGrainRoughnessDefinition
    SAND_GRAIN_ROUGHNESS_DEFINITION_SPRAY_PAINT: RoughnessAndPermeability.SandGrainRoughnessDefinition
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_SURFACES_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_SOLIDS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_VISUAL_OBJECTS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_IFC_OBJECTS_FIELD_NUMBER: _ClassVar[int]
    TYPE_OF_SURFACE_FIELD_NUMBER: _ClassVar[int]
    SAND_GRAIN_ROUGHNESS_DEFINITION_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_OF_SAND_GRAIN_ROUGHNESS_FIELD_NUMBER: _ClassVar[int]
    ROUGHNESS_CONSTANT_FIELD_NUMBER: _ClassVar[int]
    DARCY_COEFFICIENT_FIELD_NUMBER: _ClassVar[int]
    INERTIAL_COEFFICIENT_FIELD_NUMBER: _ClassVar[int]
    POROUS_MEDIA_LENGTH_IN_FLOW_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    assigned_members: _containers.RepeatedScalarFieldContainer[int]
    assigned_surfaces: _containers.RepeatedScalarFieldContainer[int]
    assigned_solids: _containers.RepeatedScalarFieldContainer[int]
    assigned_visual_objects: _containers.RepeatedScalarFieldContainer[int]
    assigned_ifc_objects: _containers.RepeatedScalarFieldContainer[int]
    type_of_surface: RoughnessAndPermeability.TypeOfSurface
    sand_grain_roughness_definition: RoughnessAndPermeability.SandGrainRoughnessDefinition
    height_of_sand_grain_roughness: float
    roughness_constant: float
    darcy_coefficient: float
    inertial_coefficient: float
    porous_media_length_in_flow_direction: float
    comment: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., assigned_members: _Optional[_Iterable[int]] = ..., assigned_surfaces: _Optional[_Iterable[int]] = ..., assigned_solids: _Optional[_Iterable[int]] = ..., assigned_visual_objects: _Optional[_Iterable[int]] = ..., assigned_ifc_objects: _Optional[_Iterable[int]] = ..., type_of_surface: _Optional[_Union[RoughnessAndPermeability.TypeOfSurface, str]] = ..., sand_grain_roughness_definition: _Optional[_Union[RoughnessAndPermeability.SandGrainRoughnessDefinition, str]] = ..., height_of_sand_grain_roughness: _Optional[float] = ..., roughness_constant: _Optional[float] = ..., darcy_coefficient: _Optional[float] = ..., inertial_coefficient: _Optional[float] = ..., porous_media_length_in_flow_direction: _Optional[float] = ..., comment: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
