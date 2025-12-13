from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FreeConcentratedLoad(_message.Message):
    __slots__ = ("no", "surfaces", "load_case", "coordinate_system", "load_projection", "load_direction", "load_acting_region_from", "load_acting_region_to", "comment", "is_generated", "generating_object_info", "load_type", "magnitude", "load_location_x", "load_location_y", "import_support_reaction", "import_support_reaction_model_name", "import_support_reaction_model_description", "import_support_reaction_load_direction", "id_for_export_import", "metadata_for_export_import")
    class LoadProjection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LOAD_PROJECTION_XY_OR_UV: _ClassVar[FreeConcentratedLoad.LoadProjection]
        LOAD_PROJECTION_XZ_OR_UW: _ClassVar[FreeConcentratedLoad.LoadProjection]
        LOAD_PROJECTION_YZ_OR_VW: _ClassVar[FreeConcentratedLoad.LoadProjection]
    LOAD_PROJECTION_XY_OR_UV: FreeConcentratedLoad.LoadProjection
    LOAD_PROJECTION_XZ_OR_UW: FreeConcentratedLoad.LoadProjection
    LOAD_PROJECTION_YZ_OR_VW: FreeConcentratedLoad.LoadProjection
    class LoadDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LOAD_DIRECTION_LOCAL_X: _ClassVar[FreeConcentratedLoad.LoadDirection]
        LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_TRUE_LENGTH: _ClassVar[FreeConcentratedLoad.LoadDirection]
        LOAD_DIRECTION_GLOBAL_X_TRUE_LENGTH: _ClassVar[FreeConcentratedLoad.LoadDirection]
        LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_TRUE_LENGTH: _ClassVar[FreeConcentratedLoad.LoadDirection]
        LOAD_DIRECTION_GLOBAL_Y_TRUE_LENGTH: _ClassVar[FreeConcentratedLoad.LoadDirection]
        LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_TRUE_LENGTH: _ClassVar[FreeConcentratedLoad.LoadDirection]
        LOAD_DIRECTION_GLOBAL_Z_TRUE_LENGTH: _ClassVar[FreeConcentratedLoad.LoadDirection]
        LOAD_DIRECTION_LOCAL_Y: _ClassVar[FreeConcentratedLoad.LoadDirection]
        LOAD_DIRECTION_LOCAL_Z: _ClassVar[FreeConcentratedLoad.LoadDirection]
    LOAD_DIRECTION_LOCAL_X: FreeConcentratedLoad.LoadDirection
    LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_TRUE_LENGTH: FreeConcentratedLoad.LoadDirection
    LOAD_DIRECTION_GLOBAL_X_TRUE_LENGTH: FreeConcentratedLoad.LoadDirection
    LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_TRUE_LENGTH: FreeConcentratedLoad.LoadDirection
    LOAD_DIRECTION_GLOBAL_Y_TRUE_LENGTH: FreeConcentratedLoad.LoadDirection
    LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_TRUE_LENGTH: FreeConcentratedLoad.LoadDirection
    LOAD_DIRECTION_GLOBAL_Z_TRUE_LENGTH: FreeConcentratedLoad.LoadDirection
    LOAD_DIRECTION_LOCAL_Y: FreeConcentratedLoad.LoadDirection
    LOAD_DIRECTION_LOCAL_Z: FreeConcentratedLoad.LoadDirection
    class LoadType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LOAD_TYPE_UNKNOWN: _ClassVar[FreeConcentratedLoad.LoadType]
        LOAD_TYPE_FORCE: _ClassVar[FreeConcentratedLoad.LoadType]
        LOAD_TYPE_MOMENT: _ClassVar[FreeConcentratedLoad.LoadType]
    LOAD_TYPE_UNKNOWN: FreeConcentratedLoad.LoadType
    LOAD_TYPE_FORCE: FreeConcentratedLoad.LoadType
    LOAD_TYPE_MOMENT: FreeConcentratedLoad.LoadType
    class ImportSupportReactionLoadDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_FORCE_X: _ClassVar[FreeConcentratedLoad.ImportSupportReactionLoadDirection]
        IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_FORCE_Y: _ClassVar[FreeConcentratedLoad.ImportSupportReactionLoadDirection]
        IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_FORCE_Z: _ClassVar[FreeConcentratedLoad.ImportSupportReactionLoadDirection]
        IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_MOMENT_X: _ClassVar[FreeConcentratedLoad.ImportSupportReactionLoadDirection]
        IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_MOMENT_Y: _ClassVar[FreeConcentratedLoad.ImportSupportReactionLoadDirection]
        IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_MOMENT_Z: _ClassVar[FreeConcentratedLoad.ImportSupportReactionLoadDirection]
    IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_FORCE_X: FreeConcentratedLoad.ImportSupportReactionLoadDirection
    IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_FORCE_Y: FreeConcentratedLoad.ImportSupportReactionLoadDirection
    IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_FORCE_Z: FreeConcentratedLoad.ImportSupportReactionLoadDirection
    IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_MOMENT_X: FreeConcentratedLoad.ImportSupportReactionLoadDirection
    IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_MOMENT_Y: FreeConcentratedLoad.ImportSupportReactionLoadDirection
    IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_MOMENT_Z: FreeConcentratedLoad.ImportSupportReactionLoadDirection
    NO_FIELD_NUMBER: _ClassVar[int]
    SURFACES_FIELD_NUMBER: _ClassVar[int]
    LOAD_CASE_FIELD_NUMBER: _ClassVar[int]
    COORDINATE_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    LOAD_PROJECTION_FIELD_NUMBER: _ClassVar[int]
    LOAD_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    LOAD_ACTING_REGION_FROM_FIELD_NUMBER: _ClassVar[int]
    LOAD_ACTING_REGION_TO_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    LOAD_TYPE_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_FIELD_NUMBER: _ClassVar[int]
    LOAD_LOCATION_X_FIELD_NUMBER: _ClassVar[int]
    LOAD_LOCATION_Y_FIELD_NUMBER: _ClassVar[int]
    IMPORT_SUPPORT_REACTION_FIELD_NUMBER: _ClassVar[int]
    IMPORT_SUPPORT_REACTION_MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    IMPORT_SUPPORT_REACTION_MODEL_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    surfaces: _containers.RepeatedScalarFieldContainer[int]
    load_case: int
    coordinate_system: int
    load_projection: FreeConcentratedLoad.LoadProjection
    load_direction: FreeConcentratedLoad.LoadDirection
    load_acting_region_from: float
    load_acting_region_to: float
    comment: str
    is_generated: bool
    generating_object_info: str
    load_type: FreeConcentratedLoad.LoadType
    magnitude: float
    load_location_x: float
    load_location_y: float
    import_support_reaction: bool
    import_support_reaction_model_name: str
    import_support_reaction_model_description: str
    import_support_reaction_load_direction: FreeConcentratedLoad.ImportSupportReactionLoadDirection
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., surfaces: _Optional[_Iterable[int]] = ..., load_case: _Optional[int] = ..., coordinate_system: _Optional[int] = ..., load_projection: _Optional[_Union[FreeConcentratedLoad.LoadProjection, str]] = ..., load_direction: _Optional[_Union[FreeConcentratedLoad.LoadDirection, str]] = ..., load_acting_region_from: _Optional[float] = ..., load_acting_region_to: _Optional[float] = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., load_type: _Optional[_Union[FreeConcentratedLoad.LoadType, str]] = ..., magnitude: _Optional[float] = ..., load_location_x: _Optional[float] = ..., load_location_y: _Optional[float] = ..., import_support_reaction: bool = ..., import_support_reaction_model_name: _Optional[str] = ..., import_support_reaction_model_description: _Optional[str] = ..., import_support_reaction_load_direction: _Optional[_Union[FreeConcentratedLoad.ImportSupportReactionLoadDirection, str]] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
