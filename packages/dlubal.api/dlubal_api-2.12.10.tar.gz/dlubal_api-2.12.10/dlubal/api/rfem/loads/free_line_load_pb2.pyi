from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FreeLineLoad(_message.Message):
    __slots__ = ("no", "surfaces", "load_case", "coordinate_system", "load_projection", "load_direction", "load_acting_region_from", "load_acting_region_to", "comment", "is_generated", "generating_object_info", "load_distribution", "magnitude_uniform", "magnitude_first", "magnitude_second", "load_location_first_x", "load_location_first_y", "load_location_second_x", "load_location_second_y", "varying_load_parameters_are_defined_as_relative", "varying_load_parameters", "varying_load_parameters_sorted", "import_support_reaction", "import_support_reaction_model_name", "import_support_reaction_model_description", "import_support_reaction_length_of_line", "import_support_reaction_load_direction", "id_for_export_import", "metadata_for_export_import")
    class LoadProjection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LOAD_PROJECTION_XY_OR_UV: _ClassVar[FreeLineLoad.LoadProjection]
        LOAD_PROJECTION_XZ_OR_UW: _ClassVar[FreeLineLoad.LoadProjection]
        LOAD_PROJECTION_YZ_OR_VW: _ClassVar[FreeLineLoad.LoadProjection]
    LOAD_PROJECTION_XY_OR_UV: FreeLineLoad.LoadProjection
    LOAD_PROJECTION_XZ_OR_UW: FreeLineLoad.LoadProjection
    LOAD_PROJECTION_YZ_OR_VW: FreeLineLoad.LoadProjection
    class LoadDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LOAD_DIRECTION_LOCAL_X: _ClassVar[FreeLineLoad.LoadDirection]
        LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_PROJECTED_LENGTH: _ClassVar[FreeLineLoad.LoadDirection]
        LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_TRUE_LENGTH: _ClassVar[FreeLineLoad.LoadDirection]
        LOAD_DIRECTION_GLOBAL_X_PROJECTED_LENGTH: _ClassVar[FreeLineLoad.LoadDirection]
        LOAD_DIRECTION_GLOBAL_X_TRUE_LENGTH: _ClassVar[FreeLineLoad.LoadDirection]
        LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_PROJECTED_LENGTH: _ClassVar[FreeLineLoad.LoadDirection]
        LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_TRUE_LENGTH: _ClassVar[FreeLineLoad.LoadDirection]
        LOAD_DIRECTION_GLOBAL_Y_PROJECTED_LENGTH: _ClassVar[FreeLineLoad.LoadDirection]
        LOAD_DIRECTION_GLOBAL_Y_TRUE_LENGTH: _ClassVar[FreeLineLoad.LoadDirection]
        LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_PROJECTED_LENGTH: _ClassVar[FreeLineLoad.LoadDirection]
        LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_TRUE_LENGTH: _ClassVar[FreeLineLoad.LoadDirection]
        LOAD_DIRECTION_GLOBAL_Z_PROJECTED_LENGTH: _ClassVar[FreeLineLoad.LoadDirection]
        LOAD_DIRECTION_GLOBAL_Z_TRUE_LENGTH: _ClassVar[FreeLineLoad.LoadDirection]
        LOAD_DIRECTION_LOCAL_Y: _ClassVar[FreeLineLoad.LoadDirection]
        LOAD_DIRECTION_LOCAL_Z: _ClassVar[FreeLineLoad.LoadDirection]
    LOAD_DIRECTION_LOCAL_X: FreeLineLoad.LoadDirection
    LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_PROJECTED_LENGTH: FreeLineLoad.LoadDirection
    LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_TRUE_LENGTH: FreeLineLoad.LoadDirection
    LOAD_DIRECTION_GLOBAL_X_PROJECTED_LENGTH: FreeLineLoad.LoadDirection
    LOAD_DIRECTION_GLOBAL_X_TRUE_LENGTH: FreeLineLoad.LoadDirection
    LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_PROJECTED_LENGTH: FreeLineLoad.LoadDirection
    LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_TRUE_LENGTH: FreeLineLoad.LoadDirection
    LOAD_DIRECTION_GLOBAL_Y_PROJECTED_LENGTH: FreeLineLoad.LoadDirection
    LOAD_DIRECTION_GLOBAL_Y_TRUE_LENGTH: FreeLineLoad.LoadDirection
    LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_PROJECTED_LENGTH: FreeLineLoad.LoadDirection
    LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_TRUE_LENGTH: FreeLineLoad.LoadDirection
    LOAD_DIRECTION_GLOBAL_Z_PROJECTED_LENGTH: FreeLineLoad.LoadDirection
    LOAD_DIRECTION_GLOBAL_Z_TRUE_LENGTH: FreeLineLoad.LoadDirection
    LOAD_DIRECTION_LOCAL_Y: FreeLineLoad.LoadDirection
    LOAD_DIRECTION_LOCAL_Z: FreeLineLoad.LoadDirection
    class LoadDistribution(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LOAD_DISTRIBUTION_UNIFORM: _ClassVar[FreeLineLoad.LoadDistribution]
        LOAD_DISTRIBUTION_LINEAR: _ClassVar[FreeLineLoad.LoadDistribution]
        LOAD_DISTRIBUTION_VARYING: _ClassVar[FreeLineLoad.LoadDistribution]
    LOAD_DISTRIBUTION_UNIFORM: FreeLineLoad.LoadDistribution
    LOAD_DISTRIBUTION_LINEAR: FreeLineLoad.LoadDistribution
    LOAD_DISTRIBUTION_VARYING: FreeLineLoad.LoadDistribution
    class ImportSupportReactionLoadDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_FORCE_GLOBAL_X: _ClassVar[FreeLineLoad.ImportSupportReactionLoadDirection]
        IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_FORCE_GLOBAL_Y: _ClassVar[FreeLineLoad.ImportSupportReactionLoadDirection]
        IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_FORCE_GLOBAL_Z: _ClassVar[FreeLineLoad.ImportSupportReactionLoadDirection]
        IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_FORCE_LOCAL_X: _ClassVar[FreeLineLoad.ImportSupportReactionLoadDirection]
        IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_FORCE_LOCAL_Y: _ClassVar[FreeLineLoad.ImportSupportReactionLoadDirection]
        IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_FORCE_LOCAL_Z: _ClassVar[FreeLineLoad.ImportSupportReactionLoadDirection]
    IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_FORCE_GLOBAL_X: FreeLineLoad.ImportSupportReactionLoadDirection
    IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_FORCE_GLOBAL_Y: FreeLineLoad.ImportSupportReactionLoadDirection
    IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_FORCE_GLOBAL_Z: FreeLineLoad.ImportSupportReactionLoadDirection
    IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_FORCE_LOCAL_X: FreeLineLoad.ImportSupportReactionLoadDirection
    IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_FORCE_LOCAL_Y: FreeLineLoad.ImportSupportReactionLoadDirection
    IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_FORCE_LOCAL_Z: FreeLineLoad.ImportSupportReactionLoadDirection
    class VaryingLoadParametersTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[FreeLineLoad.VaryingLoadParametersRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[FreeLineLoad.VaryingLoadParametersRow, _Mapping]]] = ...) -> None: ...
    class VaryingLoadParametersRow(_message.Message):
        __slots__ = ("no", "description", "distance", "delta_distance", "magnitude")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        DISTANCE_FIELD_NUMBER: _ClassVar[int]
        DELTA_DISTANCE_FIELD_NUMBER: _ClassVar[int]
        MAGNITUDE_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        distance: float
        delta_distance: float
        magnitude: float
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., distance: _Optional[float] = ..., delta_distance: _Optional[float] = ..., magnitude: _Optional[float] = ...) -> None: ...
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
    LOAD_DISTRIBUTION_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_UNIFORM_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_FIRST_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_SECOND_FIELD_NUMBER: _ClassVar[int]
    LOAD_LOCATION_FIRST_X_FIELD_NUMBER: _ClassVar[int]
    LOAD_LOCATION_FIRST_Y_FIELD_NUMBER: _ClassVar[int]
    LOAD_LOCATION_SECOND_X_FIELD_NUMBER: _ClassVar[int]
    LOAD_LOCATION_SECOND_Y_FIELD_NUMBER: _ClassVar[int]
    VARYING_LOAD_PARAMETERS_ARE_DEFINED_AS_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    VARYING_LOAD_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    VARYING_LOAD_PARAMETERS_SORTED_FIELD_NUMBER: _ClassVar[int]
    IMPORT_SUPPORT_REACTION_FIELD_NUMBER: _ClassVar[int]
    IMPORT_SUPPORT_REACTION_MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    IMPORT_SUPPORT_REACTION_MODEL_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IMPORT_SUPPORT_REACTION_LENGTH_OF_LINE_FIELD_NUMBER: _ClassVar[int]
    IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    surfaces: _containers.RepeatedScalarFieldContainer[int]
    load_case: int
    coordinate_system: int
    load_projection: FreeLineLoad.LoadProjection
    load_direction: FreeLineLoad.LoadDirection
    load_acting_region_from: float
    load_acting_region_to: float
    comment: str
    is_generated: bool
    generating_object_info: str
    load_distribution: FreeLineLoad.LoadDistribution
    magnitude_uniform: float
    magnitude_first: float
    magnitude_second: float
    load_location_first_x: float
    load_location_first_y: float
    load_location_second_x: float
    load_location_second_y: float
    varying_load_parameters_are_defined_as_relative: bool
    varying_load_parameters: FreeLineLoad.VaryingLoadParametersTable
    varying_load_parameters_sorted: bool
    import_support_reaction: bool
    import_support_reaction_model_name: str
    import_support_reaction_model_description: str
    import_support_reaction_length_of_line: float
    import_support_reaction_load_direction: FreeLineLoad.ImportSupportReactionLoadDirection
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., surfaces: _Optional[_Iterable[int]] = ..., load_case: _Optional[int] = ..., coordinate_system: _Optional[int] = ..., load_projection: _Optional[_Union[FreeLineLoad.LoadProjection, str]] = ..., load_direction: _Optional[_Union[FreeLineLoad.LoadDirection, str]] = ..., load_acting_region_from: _Optional[float] = ..., load_acting_region_to: _Optional[float] = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., load_distribution: _Optional[_Union[FreeLineLoad.LoadDistribution, str]] = ..., magnitude_uniform: _Optional[float] = ..., magnitude_first: _Optional[float] = ..., magnitude_second: _Optional[float] = ..., load_location_first_x: _Optional[float] = ..., load_location_first_y: _Optional[float] = ..., load_location_second_x: _Optional[float] = ..., load_location_second_y: _Optional[float] = ..., varying_load_parameters_are_defined_as_relative: bool = ..., varying_load_parameters: _Optional[_Union[FreeLineLoad.VaryingLoadParametersTable, _Mapping]] = ..., varying_load_parameters_sorted: bool = ..., import_support_reaction: bool = ..., import_support_reaction_model_name: _Optional[str] = ..., import_support_reaction_model_description: _Optional[str] = ..., import_support_reaction_length_of_line: _Optional[float] = ..., import_support_reaction_load_direction: _Optional[_Union[FreeLineLoad.ImportSupportReactionLoadDirection, str]] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
