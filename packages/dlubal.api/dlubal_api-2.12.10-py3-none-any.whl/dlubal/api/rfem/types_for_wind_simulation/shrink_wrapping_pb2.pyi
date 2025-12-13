from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ShrinkWrapping(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "assigned_members", "assigned_surfaces", "assigned_solids", "assigned_visual_objects", "assigned_ifc_objects", "simplification_defined_by", "level_of_detail", "detail_size", "deactivate_shrink_wrapping", "mesh_defined_by", "mesh_level_of_detail", "mesh_cell_size", "small_openings_closure_type", "closure_relative_to_model_parameter", "closure_real_size", "orient_normals_for_surface_results", "comment", "id_for_export_import", "metadata_for_export_import")
    class SimplificationDefinedBy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SIMPLIFICATION_DEFINED_BY_LEVEL_OF_DETAILS: _ClassVar[ShrinkWrapping.SimplificationDefinedBy]
        SIMPLIFICATION_DEFINED_BY_DETAIL_SIZE: _ClassVar[ShrinkWrapping.SimplificationDefinedBy]
    SIMPLIFICATION_DEFINED_BY_LEVEL_OF_DETAILS: ShrinkWrapping.SimplificationDefinedBy
    SIMPLIFICATION_DEFINED_BY_DETAIL_SIZE: ShrinkWrapping.SimplificationDefinedBy
    class MeshDefinedBy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        MESH_DEFINED_BY_MESH_CELL_SIZE: _ClassVar[ShrinkWrapping.MeshDefinedBy]
        MESH_DEFINED_BY_LEVEL_OF_DETAIL: _ClassVar[ShrinkWrapping.MeshDefinedBy]
    MESH_DEFINED_BY_MESH_CELL_SIZE: ShrinkWrapping.MeshDefinedBy
    MESH_DEFINED_BY_LEVEL_OF_DETAIL: ShrinkWrapping.MeshDefinedBy
    class SmallOpeningsClosureType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SMALL_OPENINGS_CLOSURE_TYPE_PERCENT_OF_MODEL_DIAMETER: _ClassVar[ShrinkWrapping.SmallOpeningsClosureType]
        SMALL_OPENINGS_CLOSURE_TYPE_REAL_SIZE: _ClassVar[ShrinkWrapping.SmallOpeningsClosureType]
    SMALL_OPENINGS_CLOSURE_TYPE_PERCENT_OF_MODEL_DIAMETER: ShrinkWrapping.SmallOpeningsClosureType
    SMALL_OPENINGS_CLOSURE_TYPE_REAL_SIZE: ShrinkWrapping.SmallOpeningsClosureType
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_SURFACES_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_SOLIDS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_VISUAL_OBJECTS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_IFC_OBJECTS_FIELD_NUMBER: _ClassVar[int]
    SIMPLIFICATION_DEFINED_BY_FIELD_NUMBER: _ClassVar[int]
    LEVEL_OF_DETAIL_FIELD_NUMBER: _ClassVar[int]
    DETAIL_SIZE_FIELD_NUMBER: _ClassVar[int]
    DEACTIVATE_SHRINK_WRAPPING_FIELD_NUMBER: _ClassVar[int]
    MESH_DEFINED_BY_FIELD_NUMBER: _ClassVar[int]
    MESH_LEVEL_OF_DETAIL_FIELD_NUMBER: _ClassVar[int]
    MESH_CELL_SIZE_FIELD_NUMBER: _ClassVar[int]
    SMALL_OPENINGS_CLOSURE_TYPE_FIELD_NUMBER: _ClassVar[int]
    CLOSURE_RELATIVE_TO_MODEL_PARAMETER_FIELD_NUMBER: _ClassVar[int]
    CLOSURE_REAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    ORIENT_NORMALS_FOR_SURFACE_RESULTS_FIELD_NUMBER: _ClassVar[int]
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
    simplification_defined_by: ShrinkWrapping.SimplificationDefinedBy
    level_of_detail: int
    detail_size: float
    deactivate_shrink_wrapping: bool
    mesh_defined_by: ShrinkWrapping.MeshDefinedBy
    mesh_level_of_detail: int
    mesh_cell_size: float
    small_openings_closure_type: ShrinkWrapping.SmallOpeningsClosureType
    closure_relative_to_model_parameter: float
    closure_real_size: float
    orient_normals_for_surface_results: bool
    comment: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., assigned_members: _Optional[_Iterable[int]] = ..., assigned_surfaces: _Optional[_Iterable[int]] = ..., assigned_solids: _Optional[_Iterable[int]] = ..., assigned_visual_objects: _Optional[_Iterable[int]] = ..., assigned_ifc_objects: _Optional[_Iterable[int]] = ..., simplification_defined_by: _Optional[_Union[ShrinkWrapping.SimplificationDefinedBy, str]] = ..., level_of_detail: _Optional[int] = ..., detail_size: _Optional[float] = ..., deactivate_shrink_wrapping: bool = ..., mesh_defined_by: _Optional[_Union[ShrinkWrapping.MeshDefinedBy, str]] = ..., mesh_level_of_detail: _Optional[int] = ..., mesh_cell_size: _Optional[float] = ..., small_openings_closure_type: _Optional[_Union[ShrinkWrapping.SmallOpeningsClosureType, str]] = ..., closure_relative_to_model_parameter: _Optional[float] = ..., closure_real_size: _Optional[float] = ..., orient_normals_for_surface_results: bool = ..., comment: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
