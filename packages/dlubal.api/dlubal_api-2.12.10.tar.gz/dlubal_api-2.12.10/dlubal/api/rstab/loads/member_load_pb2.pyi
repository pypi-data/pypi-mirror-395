from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MemberLoad(_message.Message):
    __slots__ = ("no", "load_type", "members", "load_case", "coordinate_system", "load_distribution", "load_direction", "load_direction_orientation", "form_finding_definition_type", "magnitude", "magnitude_1", "magnitude_2", "magnitude_3", "magnitude_t_c", "magnitude_t_c_1", "magnitude_t_c_2", "magnitude_t_c_3", "magnitude_delta_t", "magnitude_delta_t_1", "magnitude_delta_t_2", "magnitude_delta_t_3", "magnitude_t_t", "magnitude_t_t_1", "magnitude_t_t_2", "magnitude_t_t_3", "magnitude_t_b", "magnitude_t_b_1", "magnitude_t_b_2", "magnitude_t_b_3", "mass_global", "mass_x", "mass_y", "mass_z", "distance_a_is_defined_as_relative", "distance_a_absolute", "distance_a_relative", "distance_b_is_defined_as_relative", "distance_b_absolute", "distance_b_relative", "distance_c_is_defined_as_relative", "distance_c_absolute", "distance_c_relative", "count_n", "varying_load_parameters_are_defined_as_relative", "varying_load_parameters", "varying_load_parameters_sorted", "angular_velocity", "angular_acceleration", "axis_definition_type", "axis_definition_p1", "axis_definition_p1_x", "axis_definition_p1_y", "axis_definition_p1_z", "axis_definition_p2", "axis_definition_p2_x", "axis_definition_p2_y", "axis_definition_p2_z", "axis_definition_axis", "axis_definition_axis_orientation", "filling_height", "coating_contour_thickness", "reference_to_list_of_members", "distance_from_member_end", "load_is_over_total_length", "has_force_eccentricity", "eccentricity_horizontal_alignment", "eccentricity_vertical_alignment", "eccentricity_section_middle", "is_eccentricity_at_end_different_from_start", "eccentricity_y_at_start", "eccentricity_z_at_start", "eccentricity_y_at_end", "eccentricity_z_at_end", "reference_point_a", "reference_point_b", "coating_polygon_area", "rotation_about_axis", "comment", "is_generated", "generating_object_info", "form_finding_internal_force", "form_finding_geometry_definition", "form_finding_force_definition", "form_finding_magnitude_is_defined_as_relative", "form_finding_magnitude_absolute", "form_finding_magnitude_relative", "individual_mass_components", "import_support_reaction", "import_support_reaction_model_name", "import_support_reaction_model_description", "import_support_reaction_length_of_line", "import_support_reaction_load_direction", "has_load_graphic_position_below", "coating_polygon_points", "prestress_tendon_load_definition_type", "prestress_tendon_load_definition", "prestress_tendon_load_ratio", "prestress_tendon_load_absolute_value", "id_for_export_import", "metadata_for_export_import")
    class LoadType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LOAD_TYPE_UNKNOWN: _ClassVar[MemberLoad.LoadType]
        LOAD_TYPE_AXIAL_DISPLACEMENT: _ClassVar[MemberLoad.LoadType]
        LOAD_TYPE_AXIAL_STRAIN: _ClassVar[MemberLoad.LoadType]
        LOAD_TYPE_COATING_CONTOUR: _ClassVar[MemberLoad.LoadType]
        LOAD_TYPE_COATING_POLYGON: _ClassVar[MemberLoad.LoadType]
        LOAD_TYPE_DISPLACEMENT: _ClassVar[MemberLoad.LoadType]
        LOAD_TYPE_END_PRESTRESS: _ClassVar[MemberLoad.LoadType]
        LOAD_TYPE_FORCE: _ClassVar[MemberLoad.LoadType]
        LOAD_TYPE_FORM_FINDING: _ClassVar[MemberLoad.LoadType]
        LOAD_TYPE_INITIAL_PRESTRESS: _ClassVar[MemberLoad.LoadType]
        LOAD_TYPE_INTERNAL_PRESSURE: _ClassVar[MemberLoad.LoadType]
        LOAD_TYPE_MASS: _ClassVar[MemberLoad.LoadType]
        LOAD_TYPE_MOMENT: _ClassVar[MemberLoad.LoadType]
        LOAD_TYPE_PIPE_CONTENT_FULL: _ClassVar[MemberLoad.LoadType]
        LOAD_TYPE_PIPE_CONTENT_PARTIAL: _ClassVar[MemberLoad.LoadType]
        LOAD_TYPE_PRECAMBER: _ClassVar[MemberLoad.LoadType]
        LOAD_TYPE_PRESTRESS_TENDON: _ClassVar[MemberLoad.LoadType]
        LOAD_TYPE_ROTARY_MOTION: _ClassVar[MemberLoad.LoadType]
        LOAD_TYPE_ROTATION: _ClassVar[MemberLoad.LoadType]
        LOAD_TYPE_TEMPERATURE: _ClassVar[MemberLoad.LoadType]
        LOAD_TYPE_TEMPERATURE_CHANGE: _ClassVar[MemberLoad.LoadType]
    LOAD_TYPE_UNKNOWN: MemberLoad.LoadType
    LOAD_TYPE_AXIAL_DISPLACEMENT: MemberLoad.LoadType
    LOAD_TYPE_AXIAL_STRAIN: MemberLoad.LoadType
    LOAD_TYPE_COATING_CONTOUR: MemberLoad.LoadType
    LOAD_TYPE_COATING_POLYGON: MemberLoad.LoadType
    LOAD_TYPE_DISPLACEMENT: MemberLoad.LoadType
    LOAD_TYPE_END_PRESTRESS: MemberLoad.LoadType
    LOAD_TYPE_FORCE: MemberLoad.LoadType
    LOAD_TYPE_FORM_FINDING: MemberLoad.LoadType
    LOAD_TYPE_INITIAL_PRESTRESS: MemberLoad.LoadType
    LOAD_TYPE_INTERNAL_PRESSURE: MemberLoad.LoadType
    LOAD_TYPE_MASS: MemberLoad.LoadType
    LOAD_TYPE_MOMENT: MemberLoad.LoadType
    LOAD_TYPE_PIPE_CONTENT_FULL: MemberLoad.LoadType
    LOAD_TYPE_PIPE_CONTENT_PARTIAL: MemberLoad.LoadType
    LOAD_TYPE_PRECAMBER: MemberLoad.LoadType
    LOAD_TYPE_PRESTRESS_TENDON: MemberLoad.LoadType
    LOAD_TYPE_ROTARY_MOTION: MemberLoad.LoadType
    LOAD_TYPE_ROTATION: MemberLoad.LoadType
    LOAD_TYPE_TEMPERATURE: MemberLoad.LoadType
    LOAD_TYPE_TEMPERATURE_CHANGE: MemberLoad.LoadType
    class LoadDistribution(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LOAD_DISTRIBUTION_UNIFORM: _ClassVar[MemberLoad.LoadDistribution]
        LOAD_DISTRIBUTION_CONCENTRATED_1: _ClassVar[MemberLoad.LoadDistribution]
        LOAD_DISTRIBUTION_CONCENTRATED_2: _ClassVar[MemberLoad.LoadDistribution]
        LOAD_DISTRIBUTION_CONCENTRATED_2_2: _ClassVar[MemberLoad.LoadDistribution]
        LOAD_DISTRIBUTION_CONCENTRATED_N: _ClassVar[MemberLoad.LoadDistribution]
        LOAD_DISTRIBUTION_CONCENTRATED_VARYING: _ClassVar[MemberLoad.LoadDistribution]
        LOAD_DISTRIBUTION_PARABOLIC: _ClassVar[MemberLoad.LoadDistribution]
        LOAD_DISTRIBUTION_TAPERED: _ClassVar[MemberLoad.LoadDistribution]
        LOAD_DISTRIBUTION_TRAPEZOIDAL: _ClassVar[MemberLoad.LoadDistribution]
        LOAD_DISTRIBUTION_UNIFORM_TOTAL: _ClassVar[MemberLoad.LoadDistribution]
        LOAD_DISTRIBUTION_VARYING: _ClassVar[MemberLoad.LoadDistribution]
        LOAD_DISTRIBUTION_VARYING_IN_Z: _ClassVar[MemberLoad.LoadDistribution]
    LOAD_DISTRIBUTION_UNIFORM: MemberLoad.LoadDistribution
    LOAD_DISTRIBUTION_CONCENTRATED_1: MemberLoad.LoadDistribution
    LOAD_DISTRIBUTION_CONCENTRATED_2: MemberLoad.LoadDistribution
    LOAD_DISTRIBUTION_CONCENTRATED_2_2: MemberLoad.LoadDistribution
    LOAD_DISTRIBUTION_CONCENTRATED_N: MemberLoad.LoadDistribution
    LOAD_DISTRIBUTION_CONCENTRATED_VARYING: MemberLoad.LoadDistribution
    LOAD_DISTRIBUTION_PARABOLIC: MemberLoad.LoadDistribution
    LOAD_DISTRIBUTION_TAPERED: MemberLoad.LoadDistribution
    LOAD_DISTRIBUTION_TRAPEZOIDAL: MemberLoad.LoadDistribution
    LOAD_DISTRIBUTION_UNIFORM_TOTAL: MemberLoad.LoadDistribution
    LOAD_DISTRIBUTION_VARYING: MemberLoad.LoadDistribution
    LOAD_DISTRIBUTION_VARYING_IN_Z: MemberLoad.LoadDistribution
    class LoadDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LOAD_DIRECTION_LOCAL_X: _ClassVar[MemberLoad.LoadDirection]
        LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_PROJECTED_LENGTH: _ClassVar[MemberLoad.LoadDirection]
        LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_TRUE_LENGTH: _ClassVar[MemberLoad.LoadDirection]
        LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_PROJECTED_LENGTH: _ClassVar[MemberLoad.LoadDirection]
        LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_TRUE_LENGTH: _ClassVar[MemberLoad.LoadDirection]
        LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_PROJECTED_LENGTH: _ClassVar[MemberLoad.LoadDirection]
        LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_TRUE_LENGTH: _ClassVar[MemberLoad.LoadDirection]
        LOAD_DIRECTION_LOCAL_Y: _ClassVar[MemberLoad.LoadDirection]
        LOAD_DIRECTION_LOCAL_Z: _ClassVar[MemberLoad.LoadDirection]
        LOAD_DIRECTION_PRINCIPAL_U: _ClassVar[MemberLoad.LoadDirection]
        LOAD_DIRECTION_PRINCIPAL_V: _ClassVar[MemberLoad.LoadDirection]
    LOAD_DIRECTION_LOCAL_X: MemberLoad.LoadDirection
    LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_PROJECTED_LENGTH: MemberLoad.LoadDirection
    LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_TRUE_LENGTH: MemberLoad.LoadDirection
    LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_PROJECTED_LENGTH: MemberLoad.LoadDirection
    LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_TRUE_LENGTH: MemberLoad.LoadDirection
    LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_PROJECTED_LENGTH: MemberLoad.LoadDirection
    LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_TRUE_LENGTH: MemberLoad.LoadDirection
    LOAD_DIRECTION_LOCAL_Y: MemberLoad.LoadDirection
    LOAD_DIRECTION_LOCAL_Z: MemberLoad.LoadDirection
    LOAD_DIRECTION_PRINCIPAL_U: MemberLoad.LoadDirection
    LOAD_DIRECTION_PRINCIPAL_V: MemberLoad.LoadDirection
    class LoadDirectionOrientation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LOAD_DIRECTION_ORIENTATION_LOAD_DIRECTION_FORWARD: _ClassVar[MemberLoad.LoadDirectionOrientation]
        LOAD_DIRECTION_ORIENTATION_LOAD_DIRECTION_REVERSED: _ClassVar[MemberLoad.LoadDirectionOrientation]
    LOAD_DIRECTION_ORIENTATION_LOAD_DIRECTION_FORWARD: MemberLoad.LoadDirectionOrientation
    LOAD_DIRECTION_ORIENTATION_LOAD_DIRECTION_REVERSED: MemberLoad.LoadDirectionOrientation
    class FormFindingDefinitionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        FORM_FINDING_DEFINITION_TYPE_GEOMETRIC: _ClassVar[MemberLoad.FormFindingDefinitionType]
        FORM_FINDING_DEFINITION_TYPE_FORCE: _ClassVar[MemberLoad.FormFindingDefinitionType]
    FORM_FINDING_DEFINITION_TYPE_GEOMETRIC: MemberLoad.FormFindingDefinitionType
    FORM_FINDING_DEFINITION_TYPE_FORCE: MemberLoad.FormFindingDefinitionType
    class AxisDefinitionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        AXIS_DEFINITION_TYPE_TWO_POINTS: _ClassVar[MemberLoad.AxisDefinitionType]
        AXIS_DEFINITION_TYPE_POINT_AND_AXIS: _ClassVar[MemberLoad.AxisDefinitionType]
    AXIS_DEFINITION_TYPE_TWO_POINTS: MemberLoad.AxisDefinitionType
    AXIS_DEFINITION_TYPE_POINT_AND_AXIS: MemberLoad.AxisDefinitionType
    class AxisDefinitionAxis(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        AXIS_DEFINITION_AXIS_X: _ClassVar[MemberLoad.AxisDefinitionAxis]
        AXIS_DEFINITION_AXIS_Y: _ClassVar[MemberLoad.AxisDefinitionAxis]
        AXIS_DEFINITION_AXIS_Z: _ClassVar[MemberLoad.AxisDefinitionAxis]
    AXIS_DEFINITION_AXIS_X: MemberLoad.AxisDefinitionAxis
    AXIS_DEFINITION_AXIS_Y: MemberLoad.AxisDefinitionAxis
    AXIS_DEFINITION_AXIS_Z: MemberLoad.AxisDefinitionAxis
    class AxisDefinitionAxisOrientation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        AXIS_DEFINITION_AXIS_ORIENTATION_POSITIVE: _ClassVar[MemberLoad.AxisDefinitionAxisOrientation]
        AXIS_DEFINITION_AXIS_ORIENTATION_NEGATIVE: _ClassVar[MemberLoad.AxisDefinitionAxisOrientation]
    AXIS_DEFINITION_AXIS_ORIENTATION_POSITIVE: MemberLoad.AxisDefinitionAxisOrientation
    AXIS_DEFINITION_AXIS_ORIENTATION_NEGATIVE: MemberLoad.AxisDefinitionAxisOrientation
    class EccentricityHorizontalAlignment(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ECCENTRICITY_HORIZONTAL_ALIGNMENT_LEFT: _ClassVar[MemberLoad.EccentricityHorizontalAlignment]
        ECCENTRICITY_HORIZONTAL_ALIGNMENT_CENTER: _ClassVar[MemberLoad.EccentricityHorizontalAlignment]
        ECCENTRICITY_HORIZONTAL_ALIGNMENT_NONE: _ClassVar[MemberLoad.EccentricityHorizontalAlignment]
        ECCENTRICITY_HORIZONTAL_ALIGNMENT_RIGHT: _ClassVar[MemberLoad.EccentricityHorizontalAlignment]
    ECCENTRICITY_HORIZONTAL_ALIGNMENT_LEFT: MemberLoad.EccentricityHorizontalAlignment
    ECCENTRICITY_HORIZONTAL_ALIGNMENT_CENTER: MemberLoad.EccentricityHorizontalAlignment
    ECCENTRICITY_HORIZONTAL_ALIGNMENT_NONE: MemberLoad.EccentricityHorizontalAlignment
    ECCENTRICITY_HORIZONTAL_ALIGNMENT_RIGHT: MemberLoad.EccentricityHorizontalAlignment
    class EccentricityVerticalAlignment(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ECCENTRICITY_VERTICAL_ALIGNMENT_TOP: _ClassVar[MemberLoad.EccentricityVerticalAlignment]
        ECCENTRICITY_VERTICAL_ALIGNMENT_BOTTOM: _ClassVar[MemberLoad.EccentricityVerticalAlignment]
        ECCENTRICITY_VERTICAL_ALIGNMENT_CENTER: _ClassVar[MemberLoad.EccentricityVerticalAlignment]
        ECCENTRICITY_VERTICAL_ALIGNMENT_NONE: _ClassVar[MemberLoad.EccentricityVerticalAlignment]
    ECCENTRICITY_VERTICAL_ALIGNMENT_TOP: MemberLoad.EccentricityVerticalAlignment
    ECCENTRICITY_VERTICAL_ALIGNMENT_BOTTOM: MemberLoad.EccentricityVerticalAlignment
    ECCENTRICITY_VERTICAL_ALIGNMENT_CENTER: MemberLoad.EccentricityVerticalAlignment
    ECCENTRICITY_VERTICAL_ALIGNMENT_NONE: MemberLoad.EccentricityVerticalAlignment
    class EccentricitySectionMiddle(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ECCENTRICITY_SECTION_MIDDLE_CENTER_OF_GRAVITY: _ClassVar[MemberLoad.EccentricitySectionMiddle]
        ECCENTRICITY_SECTION_MIDDLE_NONE: _ClassVar[MemberLoad.EccentricitySectionMiddle]
        ECCENTRICITY_SECTION_MIDDLE_SHEAR_CENTER: _ClassVar[MemberLoad.EccentricitySectionMiddle]
    ECCENTRICITY_SECTION_MIDDLE_CENTER_OF_GRAVITY: MemberLoad.EccentricitySectionMiddle
    ECCENTRICITY_SECTION_MIDDLE_NONE: MemberLoad.EccentricitySectionMiddle
    ECCENTRICITY_SECTION_MIDDLE_SHEAR_CENTER: MemberLoad.EccentricitySectionMiddle
    class FormFindingInternalForce(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        FORM_FINDING_INTERNAL_FORCE_TENSION: _ClassVar[MemberLoad.FormFindingInternalForce]
        FORM_FINDING_INTERNAL_FORCE_COMPRESSION: _ClassVar[MemberLoad.FormFindingInternalForce]
    FORM_FINDING_INTERNAL_FORCE_TENSION: MemberLoad.FormFindingInternalForce
    FORM_FINDING_INTERNAL_FORCE_COMPRESSION: MemberLoad.FormFindingInternalForce
    class FormFindingGeometryDefinition(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        FORM_FINDING_GEOMETRY_DEFINITION_LENGTH: _ClassVar[MemberLoad.FormFindingGeometryDefinition]
        FORM_FINDING_GEOMETRY_DEFINITION_LOW_POINT_VERTICAL_SAG: _ClassVar[MemberLoad.FormFindingGeometryDefinition]
        FORM_FINDING_GEOMETRY_DEFINITION_MAX_VERTICAL_SAG: _ClassVar[MemberLoad.FormFindingGeometryDefinition]
        FORM_FINDING_GEOMETRY_DEFINITION_SAG: _ClassVar[MemberLoad.FormFindingGeometryDefinition]
        FORM_FINDING_GEOMETRY_DEFINITION_UNSTRESSED_LENGTH: _ClassVar[MemberLoad.FormFindingGeometryDefinition]
    FORM_FINDING_GEOMETRY_DEFINITION_LENGTH: MemberLoad.FormFindingGeometryDefinition
    FORM_FINDING_GEOMETRY_DEFINITION_LOW_POINT_VERTICAL_SAG: MemberLoad.FormFindingGeometryDefinition
    FORM_FINDING_GEOMETRY_DEFINITION_MAX_VERTICAL_SAG: MemberLoad.FormFindingGeometryDefinition
    FORM_FINDING_GEOMETRY_DEFINITION_SAG: MemberLoad.FormFindingGeometryDefinition
    FORM_FINDING_GEOMETRY_DEFINITION_UNSTRESSED_LENGTH: MemberLoad.FormFindingGeometryDefinition
    class FormFindingForceDefinition(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        FORM_FINDING_FORCE_DEFINITION_UNKNOWN: _ClassVar[MemberLoad.FormFindingForceDefinition]
        FORM_FINDING_FORCE_DEFINITION_AVERAGE: _ClassVar[MemberLoad.FormFindingForceDefinition]
        FORM_FINDING_FORCE_DEFINITION_DENSITY: _ClassVar[MemberLoad.FormFindingForceDefinition]
        FORM_FINDING_FORCE_DEFINITION_HORIZONTAL_TENSION_COMPONENT: _ClassVar[MemberLoad.FormFindingForceDefinition]
        FORM_FINDING_FORCE_DEFINITION_MAX_FORCE_MEMBER: _ClassVar[MemberLoad.FormFindingForceDefinition]
        FORM_FINDING_FORCE_DEFINITION_MINIMAL_TENSION_AT_IEND: _ClassVar[MemberLoad.FormFindingForceDefinition]
        FORM_FINDING_FORCE_DEFINITION_MINIMAL_TENSION_AT_JEND: _ClassVar[MemberLoad.FormFindingForceDefinition]
        FORM_FINDING_FORCE_DEFINITION_MIN_FORCE_MEMBER: _ClassVar[MemberLoad.FormFindingForceDefinition]
        FORM_FINDING_FORCE_DEFINITION_TENSION_AT_IEND: _ClassVar[MemberLoad.FormFindingForceDefinition]
        FORM_FINDING_FORCE_DEFINITION_TENSION_AT_JEND: _ClassVar[MemberLoad.FormFindingForceDefinition]
    FORM_FINDING_FORCE_DEFINITION_UNKNOWN: MemberLoad.FormFindingForceDefinition
    FORM_FINDING_FORCE_DEFINITION_AVERAGE: MemberLoad.FormFindingForceDefinition
    FORM_FINDING_FORCE_DEFINITION_DENSITY: MemberLoad.FormFindingForceDefinition
    FORM_FINDING_FORCE_DEFINITION_HORIZONTAL_TENSION_COMPONENT: MemberLoad.FormFindingForceDefinition
    FORM_FINDING_FORCE_DEFINITION_MAX_FORCE_MEMBER: MemberLoad.FormFindingForceDefinition
    FORM_FINDING_FORCE_DEFINITION_MINIMAL_TENSION_AT_IEND: MemberLoad.FormFindingForceDefinition
    FORM_FINDING_FORCE_DEFINITION_MINIMAL_TENSION_AT_JEND: MemberLoad.FormFindingForceDefinition
    FORM_FINDING_FORCE_DEFINITION_MIN_FORCE_MEMBER: MemberLoad.FormFindingForceDefinition
    FORM_FINDING_FORCE_DEFINITION_TENSION_AT_IEND: MemberLoad.FormFindingForceDefinition
    FORM_FINDING_FORCE_DEFINITION_TENSION_AT_JEND: MemberLoad.FormFindingForceDefinition
    class ImportSupportReactionLoadDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_FORCE_GLOBAL_X: _ClassVar[MemberLoad.ImportSupportReactionLoadDirection]
        IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_FORCE_GLOBAL_Y: _ClassVar[MemberLoad.ImportSupportReactionLoadDirection]
        IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_FORCE_GLOBAL_Z: _ClassVar[MemberLoad.ImportSupportReactionLoadDirection]
        IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_FORCE_LOCAL_X: _ClassVar[MemberLoad.ImportSupportReactionLoadDirection]
        IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_FORCE_LOCAL_Y: _ClassVar[MemberLoad.ImportSupportReactionLoadDirection]
        IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_FORCE_LOCAL_Z: _ClassVar[MemberLoad.ImportSupportReactionLoadDirection]
        IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_MOMENT_GLOBAL_X: _ClassVar[MemberLoad.ImportSupportReactionLoadDirection]
        IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_MOMENT_GLOBAL_Y: _ClassVar[MemberLoad.ImportSupportReactionLoadDirection]
        IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_MOMENT_GLOBAL_Z: _ClassVar[MemberLoad.ImportSupportReactionLoadDirection]
        IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_MOMENT_LOCAL_X: _ClassVar[MemberLoad.ImportSupportReactionLoadDirection]
        IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_MOMENT_LOCAL_Y: _ClassVar[MemberLoad.ImportSupportReactionLoadDirection]
        IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_MOMENT_LOCAL_Z: _ClassVar[MemberLoad.ImportSupportReactionLoadDirection]
    IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_FORCE_GLOBAL_X: MemberLoad.ImportSupportReactionLoadDirection
    IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_FORCE_GLOBAL_Y: MemberLoad.ImportSupportReactionLoadDirection
    IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_FORCE_GLOBAL_Z: MemberLoad.ImportSupportReactionLoadDirection
    IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_FORCE_LOCAL_X: MemberLoad.ImportSupportReactionLoadDirection
    IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_FORCE_LOCAL_Y: MemberLoad.ImportSupportReactionLoadDirection
    IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_FORCE_LOCAL_Z: MemberLoad.ImportSupportReactionLoadDirection
    IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_MOMENT_GLOBAL_X: MemberLoad.ImportSupportReactionLoadDirection
    IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_MOMENT_GLOBAL_Y: MemberLoad.ImportSupportReactionLoadDirection
    IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_MOMENT_GLOBAL_Z: MemberLoad.ImportSupportReactionLoadDirection
    IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_MOMENT_LOCAL_X: MemberLoad.ImportSupportReactionLoadDirection
    IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_MOMENT_LOCAL_Y: MemberLoad.ImportSupportReactionLoadDirection
    IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_MOMENT_LOCAL_Z: MemberLoad.ImportSupportReactionLoadDirection
    class PrestressTendonLoadDefinitionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PRESTRESS_TENDON_LOAD_DEFINITION_TYPE_STRESS: _ClassVar[MemberLoad.PrestressTendonLoadDefinitionType]
        PRESTRESS_TENDON_LOAD_DEFINITION_TYPE_FORCE: _ClassVar[MemberLoad.PrestressTendonLoadDefinitionType]
    PRESTRESS_TENDON_LOAD_DEFINITION_TYPE_STRESS: MemberLoad.PrestressTendonLoadDefinitionType
    PRESTRESS_TENDON_LOAD_DEFINITION_TYPE_FORCE: MemberLoad.PrestressTendonLoadDefinitionType
    class PrestressTendonLoadDefinition(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PRESTRESS_TENDON_LOAD_DEFINITION_ABSOLUTE: _ClassVar[MemberLoad.PrestressTendonLoadDefinition]
        PRESTRESS_TENDON_LOAD_DEFINITION_RELATIVE_TO_FPK: _ClassVar[MemberLoad.PrestressTendonLoadDefinition]
        PRESTRESS_TENDON_LOAD_DEFINITION_RELATIVE_TO_FP_MAX: _ClassVar[MemberLoad.PrestressTendonLoadDefinition]
    PRESTRESS_TENDON_LOAD_DEFINITION_ABSOLUTE: MemberLoad.PrestressTendonLoadDefinition
    PRESTRESS_TENDON_LOAD_DEFINITION_RELATIVE_TO_FPK: MemberLoad.PrestressTendonLoadDefinition
    PRESTRESS_TENDON_LOAD_DEFINITION_RELATIVE_TO_FP_MAX: MemberLoad.PrestressTendonLoadDefinition
    class VaryingLoadParametersTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[MemberLoad.VaryingLoadParametersRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[MemberLoad.VaryingLoadParametersRow, _Mapping]]] = ...) -> None: ...
    class VaryingLoadParametersRow(_message.Message):
        __slots__ = ("no", "description", "distance", "delta_distance", "magnitude", "note", "magnitude_t_c", "magnitude_delta_t", "magnitude_t_t", "magnitude_t_b")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        DISTANCE_FIELD_NUMBER: _ClassVar[int]
        DELTA_DISTANCE_FIELD_NUMBER: _ClassVar[int]
        MAGNITUDE_FIELD_NUMBER: _ClassVar[int]
        NOTE_FIELD_NUMBER: _ClassVar[int]
        MAGNITUDE_T_C_FIELD_NUMBER: _ClassVar[int]
        MAGNITUDE_DELTA_T_FIELD_NUMBER: _ClassVar[int]
        MAGNITUDE_T_T_FIELD_NUMBER: _ClassVar[int]
        MAGNITUDE_T_B_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        distance: float
        delta_distance: float
        magnitude: float
        note: str
        magnitude_t_c: float
        magnitude_delta_t: float
        magnitude_t_t: float
        magnitude_t_b: float
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., distance: _Optional[float] = ..., delta_distance: _Optional[float] = ..., magnitude: _Optional[float] = ..., note: _Optional[str] = ..., magnitude_t_c: _Optional[float] = ..., magnitude_delta_t: _Optional[float] = ..., magnitude_t_t: _Optional[float] = ..., magnitude_t_b: _Optional[float] = ...) -> None: ...
    class CoatingPolygonPointsTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[MemberLoad.CoatingPolygonPointsRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[MemberLoad.CoatingPolygonPointsRow, _Mapping]]] = ...) -> None: ...
    class CoatingPolygonPointsRow(_message.Message):
        __slots__ = ("no", "description", "first_coordinate", "second_coordinate", "empty")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        FIRST_COORDINATE_FIELD_NUMBER: _ClassVar[int]
        SECOND_COORDINATE_FIELD_NUMBER: _ClassVar[int]
        EMPTY_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        first_coordinate: float
        second_coordinate: float
        empty: _common_pb2.Value
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., first_coordinate: _Optional[float] = ..., second_coordinate: _Optional[float] = ..., empty: _Optional[_Union[_common_pb2.Value, _Mapping]] = ...) -> None: ...
    NO_FIELD_NUMBER: _ClassVar[int]
    LOAD_TYPE_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    LOAD_CASE_FIELD_NUMBER: _ClassVar[int]
    COORDINATE_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    LOAD_DISTRIBUTION_FIELD_NUMBER: _ClassVar[int]
    LOAD_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    LOAD_DIRECTION_ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    FORM_FINDING_DEFINITION_TYPE_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_1_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_2_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_3_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_T_C_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_T_C_1_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_T_C_2_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_T_C_3_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_DELTA_T_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_DELTA_T_1_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_DELTA_T_2_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_DELTA_T_3_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_T_T_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_T_T_1_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_T_T_2_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_T_T_3_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_T_B_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_T_B_1_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_T_B_2_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_T_B_3_FIELD_NUMBER: _ClassVar[int]
    MASS_GLOBAL_FIELD_NUMBER: _ClassVar[int]
    MASS_X_FIELD_NUMBER: _ClassVar[int]
    MASS_Y_FIELD_NUMBER: _ClassVar[int]
    MASS_Z_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_A_IS_DEFINED_AS_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_A_ABSOLUTE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_A_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_B_IS_DEFINED_AS_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_B_ABSOLUTE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_B_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_C_IS_DEFINED_AS_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_C_ABSOLUTE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_C_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    COUNT_N_FIELD_NUMBER: _ClassVar[int]
    VARYING_LOAD_PARAMETERS_ARE_DEFINED_AS_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    VARYING_LOAD_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    VARYING_LOAD_PARAMETERS_SORTED_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_ACCELERATION_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_TYPE_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P1_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P1_X_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P1_Y_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P1_Z_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P2_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P2_X_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P2_Y_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_P2_Z_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_AXIS_FIELD_NUMBER: _ClassVar[int]
    AXIS_DEFINITION_AXIS_ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    FILLING_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    COATING_CONTOUR_THICKNESS_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_TO_LIST_OF_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FROM_MEMBER_END_FIELD_NUMBER: _ClassVar[int]
    LOAD_IS_OVER_TOTAL_LENGTH_FIELD_NUMBER: _ClassVar[int]
    HAS_FORCE_ECCENTRICITY_FIELD_NUMBER: _ClassVar[int]
    ECCENTRICITY_HORIZONTAL_ALIGNMENT_FIELD_NUMBER: _ClassVar[int]
    ECCENTRICITY_VERTICAL_ALIGNMENT_FIELD_NUMBER: _ClassVar[int]
    ECCENTRICITY_SECTION_MIDDLE_FIELD_NUMBER: _ClassVar[int]
    IS_ECCENTRICITY_AT_END_DIFFERENT_FROM_START_FIELD_NUMBER: _ClassVar[int]
    ECCENTRICITY_Y_AT_START_FIELD_NUMBER: _ClassVar[int]
    ECCENTRICITY_Z_AT_START_FIELD_NUMBER: _ClassVar[int]
    ECCENTRICITY_Y_AT_END_FIELD_NUMBER: _ClassVar[int]
    ECCENTRICITY_Z_AT_END_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_POINT_A_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_POINT_B_FIELD_NUMBER: _ClassVar[int]
    COATING_POLYGON_AREA_FIELD_NUMBER: _ClassVar[int]
    ROTATION_ABOUT_AXIS_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    FORM_FINDING_INTERNAL_FORCE_FIELD_NUMBER: _ClassVar[int]
    FORM_FINDING_GEOMETRY_DEFINITION_FIELD_NUMBER: _ClassVar[int]
    FORM_FINDING_FORCE_DEFINITION_FIELD_NUMBER: _ClassVar[int]
    FORM_FINDING_MAGNITUDE_IS_DEFINED_AS_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    FORM_FINDING_MAGNITUDE_ABSOLUTE_FIELD_NUMBER: _ClassVar[int]
    FORM_FINDING_MAGNITUDE_RELATIVE_FIELD_NUMBER: _ClassVar[int]
    INDIVIDUAL_MASS_COMPONENTS_FIELD_NUMBER: _ClassVar[int]
    IMPORT_SUPPORT_REACTION_FIELD_NUMBER: _ClassVar[int]
    IMPORT_SUPPORT_REACTION_MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    IMPORT_SUPPORT_REACTION_MODEL_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IMPORT_SUPPORT_REACTION_LENGTH_OF_LINE_FIELD_NUMBER: _ClassVar[int]
    IMPORT_SUPPORT_REACTION_LOAD_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    HAS_LOAD_GRAPHIC_POSITION_BELOW_FIELD_NUMBER: _ClassVar[int]
    COATING_POLYGON_POINTS_FIELD_NUMBER: _ClassVar[int]
    PRESTRESS_TENDON_LOAD_DEFINITION_TYPE_FIELD_NUMBER: _ClassVar[int]
    PRESTRESS_TENDON_LOAD_DEFINITION_FIELD_NUMBER: _ClassVar[int]
    PRESTRESS_TENDON_LOAD_RATIO_FIELD_NUMBER: _ClassVar[int]
    PRESTRESS_TENDON_LOAD_ABSOLUTE_VALUE_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    load_type: MemberLoad.LoadType
    members: _containers.RepeatedScalarFieldContainer[int]
    load_case: int
    coordinate_system: _common_pb2.CoordinateSystemRepresentation
    load_distribution: MemberLoad.LoadDistribution
    load_direction: MemberLoad.LoadDirection
    load_direction_orientation: MemberLoad.LoadDirectionOrientation
    form_finding_definition_type: MemberLoad.FormFindingDefinitionType
    magnitude: float
    magnitude_1: float
    magnitude_2: float
    magnitude_3: float
    magnitude_t_c: float
    magnitude_t_c_1: float
    magnitude_t_c_2: float
    magnitude_t_c_3: float
    magnitude_delta_t: float
    magnitude_delta_t_1: float
    magnitude_delta_t_2: float
    magnitude_delta_t_3: float
    magnitude_t_t: float
    magnitude_t_t_1: float
    magnitude_t_t_2: float
    magnitude_t_t_3: float
    magnitude_t_b: float
    magnitude_t_b_1: float
    magnitude_t_b_2: float
    magnitude_t_b_3: float
    mass_global: float
    mass_x: float
    mass_y: float
    mass_z: float
    distance_a_is_defined_as_relative: bool
    distance_a_absolute: float
    distance_a_relative: float
    distance_b_is_defined_as_relative: bool
    distance_b_absolute: float
    distance_b_relative: float
    distance_c_is_defined_as_relative: bool
    distance_c_absolute: float
    distance_c_relative: float
    count_n: int
    varying_load_parameters_are_defined_as_relative: bool
    varying_load_parameters: MemberLoad.VaryingLoadParametersTable
    varying_load_parameters_sorted: bool
    angular_velocity: float
    angular_acceleration: float
    axis_definition_type: MemberLoad.AxisDefinitionType
    axis_definition_p1: _common_pb2.Vector3d
    axis_definition_p1_x: float
    axis_definition_p1_y: float
    axis_definition_p1_z: float
    axis_definition_p2: _common_pb2.Vector3d
    axis_definition_p2_x: float
    axis_definition_p2_y: float
    axis_definition_p2_z: float
    axis_definition_axis: MemberLoad.AxisDefinitionAxis
    axis_definition_axis_orientation: MemberLoad.AxisDefinitionAxisOrientation
    filling_height: float
    coating_contour_thickness: float
    reference_to_list_of_members: bool
    distance_from_member_end: bool
    load_is_over_total_length: bool
    has_force_eccentricity: bool
    eccentricity_horizontal_alignment: MemberLoad.EccentricityHorizontalAlignment
    eccentricity_vertical_alignment: MemberLoad.EccentricityVerticalAlignment
    eccentricity_section_middle: MemberLoad.EccentricitySectionMiddle
    is_eccentricity_at_end_different_from_start: bool
    eccentricity_y_at_start: float
    eccentricity_z_at_start: float
    eccentricity_y_at_end: float
    eccentricity_z_at_end: float
    reference_point_a: float
    reference_point_b: float
    coating_polygon_area: float
    rotation_about_axis: float
    comment: str
    is_generated: bool
    generating_object_info: str
    form_finding_internal_force: MemberLoad.FormFindingInternalForce
    form_finding_geometry_definition: MemberLoad.FormFindingGeometryDefinition
    form_finding_force_definition: MemberLoad.FormFindingForceDefinition
    form_finding_magnitude_is_defined_as_relative: bool
    form_finding_magnitude_absolute: float
    form_finding_magnitude_relative: float
    individual_mass_components: bool
    import_support_reaction: bool
    import_support_reaction_model_name: str
    import_support_reaction_model_description: str
    import_support_reaction_length_of_line: float
    import_support_reaction_load_direction: MemberLoad.ImportSupportReactionLoadDirection
    has_load_graphic_position_below: bool
    coating_polygon_points: MemberLoad.CoatingPolygonPointsTable
    prestress_tendon_load_definition_type: MemberLoad.PrestressTendonLoadDefinitionType
    prestress_tendon_load_definition: MemberLoad.PrestressTendonLoadDefinition
    prestress_tendon_load_ratio: float
    prestress_tendon_load_absolute_value: float
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., load_type: _Optional[_Union[MemberLoad.LoadType, str]] = ..., members: _Optional[_Iterable[int]] = ..., load_case: _Optional[int] = ..., coordinate_system: _Optional[_Union[_common_pb2.CoordinateSystemRepresentation, _Mapping]] = ..., load_distribution: _Optional[_Union[MemberLoad.LoadDistribution, str]] = ..., load_direction: _Optional[_Union[MemberLoad.LoadDirection, str]] = ..., load_direction_orientation: _Optional[_Union[MemberLoad.LoadDirectionOrientation, str]] = ..., form_finding_definition_type: _Optional[_Union[MemberLoad.FormFindingDefinitionType, str]] = ..., magnitude: _Optional[float] = ..., magnitude_1: _Optional[float] = ..., magnitude_2: _Optional[float] = ..., magnitude_3: _Optional[float] = ..., magnitude_t_c: _Optional[float] = ..., magnitude_t_c_1: _Optional[float] = ..., magnitude_t_c_2: _Optional[float] = ..., magnitude_t_c_3: _Optional[float] = ..., magnitude_delta_t: _Optional[float] = ..., magnitude_delta_t_1: _Optional[float] = ..., magnitude_delta_t_2: _Optional[float] = ..., magnitude_delta_t_3: _Optional[float] = ..., magnitude_t_t: _Optional[float] = ..., magnitude_t_t_1: _Optional[float] = ..., magnitude_t_t_2: _Optional[float] = ..., magnitude_t_t_3: _Optional[float] = ..., magnitude_t_b: _Optional[float] = ..., magnitude_t_b_1: _Optional[float] = ..., magnitude_t_b_2: _Optional[float] = ..., magnitude_t_b_3: _Optional[float] = ..., mass_global: _Optional[float] = ..., mass_x: _Optional[float] = ..., mass_y: _Optional[float] = ..., mass_z: _Optional[float] = ..., distance_a_is_defined_as_relative: bool = ..., distance_a_absolute: _Optional[float] = ..., distance_a_relative: _Optional[float] = ..., distance_b_is_defined_as_relative: bool = ..., distance_b_absolute: _Optional[float] = ..., distance_b_relative: _Optional[float] = ..., distance_c_is_defined_as_relative: bool = ..., distance_c_absolute: _Optional[float] = ..., distance_c_relative: _Optional[float] = ..., count_n: _Optional[int] = ..., varying_load_parameters_are_defined_as_relative: bool = ..., varying_load_parameters: _Optional[_Union[MemberLoad.VaryingLoadParametersTable, _Mapping]] = ..., varying_load_parameters_sorted: bool = ..., angular_velocity: _Optional[float] = ..., angular_acceleration: _Optional[float] = ..., axis_definition_type: _Optional[_Union[MemberLoad.AxisDefinitionType, str]] = ..., axis_definition_p1: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., axis_definition_p1_x: _Optional[float] = ..., axis_definition_p1_y: _Optional[float] = ..., axis_definition_p1_z: _Optional[float] = ..., axis_definition_p2: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., axis_definition_p2_x: _Optional[float] = ..., axis_definition_p2_y: _Optional[float] = ..., axis_definition_p2_z: _Optional[float] = ..., axis_definition_axis: _Optional[_Union[MemberLoad.AxisDefinitionAxis, str]] = ..., axis_definition_axis_orientation: _Optional[_Union[MemberLoad.AxisDefinitionAxisOrientation, str]] = ..., filling_height: _Optional[float] = ..., coating_contour_thickness: _Optional[float] = ..., reference_to_list_of_members: bool = ..., distance_from_member_end: bool = ..., load_is_over_total_length: bool = ..., has_force_eccentricity: bool = ..., eccentricity_horizontal_alignment: _Optional[_Union[MemberLoad.EccentricityHorizontalAlignment, str]] = ..., eccentricity_vertical_alignment: _Optional[_Union[MemberLoad.EccentricityVerticalAlignment, str]] = ..., eccentricity_section_middle: _Optional[_Union[MemberLoad.EccentricitySectionMiddle, str]] = ..., is_eccentricity_at_end_different_from_start: bool = ..., eccentricity_y_at_start: _Optional[float] = ..., eccentricity_z_at_start: _Optional[float] = ..., eccentricity_y_at_end: _Optional[float] = ..., eccentricity_z_at_end: _Optional[float] = ..., reference_point_a: _Optional[float] = ..., reference_point_b: _Optional[float] = ..., coating_polygon_area: _Optional[float] = ..., rotation_about_axis: _Optional[float] = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., form_finding_internal_force: _Optional[_Union[MemberLoad.FormFindingInternalForce, str]] = ..., form_finding_geometry_definition: _Optional[_Union[MemberLoad.FormFindingGeometryDefinition, str]] = ..., form_finding_force_definition: _Optional[_Union[MemberLoad.FormFindingForceDefinition, str]] = ..., form_finding_magnitude_is_defined_as_relative: bool = ..., form_finding_magnitude_absolute: _Optional[float] = ..., form_finding_magnitude_relative: _Optional[float] = ..., individual_mass_components: bool = ..., import_support_reaction: bool = ..., import_support_reaction_model_name: _Optional[str] = ..., import_support_reaction_model_description: _Optional[str] = ..., import_support_reaction_length_of_line: _Optional[float] = ..., import_support_reaction_load_direction: _Optional[_Union[MemberLoad.ImportSupportReactionLoadDirection, str]] = ..., has_load_graphic_position_below: bool = ..., coating_polygon_points: _Optional[_Union[MemberLoad.CoatingPolygonPointsTable, _Mapping]] = ..., prestress_tendon_load_definition_type: _Optional[_Union[MemberLoad.PrestressTendonLoadDefinitionType, str]] = ..., prestress_tendon_load_definition: _Optional[_Union[MemberLoad.PrestressTendonLoadDefinition, str]] = ..., prestress_tendon_load_ratio: _Optional[float] = ..., prestress_tendon_load_absolute_value: _Optional[float] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
