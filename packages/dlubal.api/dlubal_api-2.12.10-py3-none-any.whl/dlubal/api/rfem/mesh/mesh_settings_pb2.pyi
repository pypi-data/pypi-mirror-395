from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MeshSettings(_message.Message):
    __slots__ = ("general_target_length_of_fe", "general_maximum_distance_between_node_and_line", "general_independent_mesh_preferred", "general_independent_mesh_connect_eliminated_node", "general_independent_mesh_connect_eliminated_node_to_group_of_elements_radius", "members_number_of_divisions_for_special_types", "members_activate_division_due_to_analysis_settings", "members_number_of_divisions_for_result_diagram", "members_number_of_divisions_for_min_max_values", "members_use_division_for_concrete_members", "members_number_of_divisions_for_concrete_members", "members_use_division_for_members_with_nodes", "surfaces_maximum_ratio_of_fe", "surfaces_maximum_out_of_plane_inclination", "surfaces_mesh_refinement", "surfaces_relationship", "surfaces_integrate_also_unutilized_objects", "surfaces_shape_of_finite_elements", "surfaces_same_squares", "surfaces_triangles_for_membranes", "surfaces_mapped_mesh_preferred", "solids_use_refinement_if_containing_close_nodes", "solids_maximum_number_of_elements", "solids_use_target_length_of_fe_for_type_soil", "solids_target_length_of_fe_for_type_soil", "surfaces_mesh_quality_config", "solids_mesh_quality_config", "wind_simulation_mesh_config")
    class SurfacesShapeOfFiniteElementsType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SURFACES_SHAPE_OF_FINITE_ELEMENTS_UNKNOWN: _ClassVar[MeshSettings.SurfacesShapeOfFiniteElementsType]
        SURFACES_SHAPE_OF_FINITE_ELEMENTS_FOR_SURFACES__QUADRANGLES_ONLY: _ClassVar[MeshSettings.SurfacesShapeOfFiniteElementsType]
        SURFACES_SHAPE_OF_FINITE_ELEMENTS_FOR_SURFACES__TRIANGLES_AND_QUADRANGLES: _ClassVar[MeshSettings.SurfacesShapeOfFiniteElementsType]
        SURFACES_SHAPE_OF_FINITE_ELEMENTS_FOR_SURFACES__TRIANGLES_ONLY: _ClassVar[MeshSettings.SurfacesShapeOfFiniteElementsType]
    SURFACES_SHAPE_OF_FINITE_ELEMENTS_UNKNOWN: MeshSettings.SurfacesShapeOfFiniteElementsType
    SURFACES_SHAPE_OF_FINITE_ELEMENTS_FOR_SURFACES__QUADRANGLES_ONLY: MeshSettings.SurfacesShapeOfFiniteElementsType
    SURFACES_SHAPE_OF_FINITE_ELEMENTS_FOR_SURFACES__TRIANGLES_AND_QUADRANGLES: MeshSettings.SurfacesShapeOfFiniteElementsType
    SURFACES_SHAPE_OF_FINITE_ELEMENTS_FOR_SURFACES__TRIANGLES_ONLY: MeshSettings.SurfacesShapeOfFiniteElementsType
    class SurfacesMeshQualityConfig(_message.Message):
        __slots__ = ("mesh_quality_color_indicator_ok_color", "mesh_quality_color_indicator_warning_color", "mesh_quality_color_indicator_failure_color", "quality_criteria_config_for_surfaces")
        class QualityCriteriaConfigForSurfaces(_message.Message):
            __slots__ = ("quality_criterion_check_aspect_ratio", "quality_criterion_check_aspect_ratio_warning", "quality_criterion_check_aspect_ratio_failure", "quality_criterion_parallel_deviations", "quality_criterion_parallel_deviations_warning", "quality_criterion_parallel_deviations_failure", "quality_criterion_corner_angles_of_triangle_elements", "quality_criterion_corner_angles_of_triangle_elements_warning", "quality_criterion_corner_angles_of_triangle_elements_failure", "quality_criterion_corner_angles_of_quadrangle_elements", "quality_criterion_corner_angles_of_quadrangle_elements_warning", "quality_criterion_corner_angles_of_quadrangle_elements_failure", "quality_criterion_warping_of_membrane_elements", "quality_criterion_warping_of_membrane_elements_warning", "quality_criterion_warping_of_membrane_elements_failure", "quality_criterion_warping_of_non_membrane_elements", "quality_criterion_warping_of_non_membrane_elements_warning", "quality_criterion_warping_of_non_membrane_elements_failure", "quality_criterion_jacobian_ratio", "quality_criterion_jacobian_ratio_warning", "quality_criterion_jacobian_ratio_failure")
            QUALITY_CRITERION_CHECK_ASPECT_RATIO_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_CHECK_ASPECT_RATIO_WARNING_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_CHECK_ASPECT_RATIO_FAILURE_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_PARALLEL_DEVIATIONS_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_PARALLEL_DEVIATIONS_WARNING_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_PARALLEL_DEVIATIONS_FAILURE_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_CORNER_ANGLES_OF_TRIANGLE_ELEMENTS_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_CORNER_ANGLES_OF_TRIANGLE_ELEMENTS_WARNING_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_CORNER_ANGLES_OF_TRIANGLE_ELEMENTS_FAILURE_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_CORNER_ANGLES_OF_QUADRANGLE_ELEMENTS_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_CORNER_ANGLES_OF_QUADRANGLE_ELEMENTS_WARNING_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_CORNER_ANGLES_OF_QUADRANGLE_ELEMENTS_FAILURE_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_WARPING_OF_MEMBRANE_ELEMENTS_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_WARPING_OF_MEMBRANE_ELEMENTS_WARNING_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_WARPING_OF_MEMBRANE_ELEMENTS_FAILURE_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_WARPING_OF_NON_MEMBRANE_ELEMENTS_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_WARPING_OF_NON_MEMBRANE_ELEMENTS_WARNING_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_WARPING_OF_NON_MEMBRANE_ELEMENTS_FAILURE_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_JACOBIAN_RATIO_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_JACOBIAN_RATIO_WARNING_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_JACOBIAN_RATIO_FAILURE_FIELD_NUMBER: _ClassVar[int]
            quality_criterion_check_aspect_ratio: bool
            quality_criterion_check_aspect_ratio_warning: float
            quality_criterion_check_aspect_ratio_failure: float
            quality_criterion_parallel_deviations: bool
            quality_criterion_parallel_deviations_warning: float
            quality_criterion_parallel_deviations_failure: float
            quality_criterion_corner_angles_of_triangle_elements: bool
            quality_criterion_corner_angles_of_triangle_elements_warning: float
            quality_criterion_corner_angles_of_triangle_elements_failure: float
            quality_criterion_corner_angles_of_quadrangle_elements: bool
            quality_criterion_corner_angles_of_quadrangle_elements_warning: float
            quality_criterion_corner_angles_of_quadrangle_elements_failure: float
            quality_criterion_warping_of_membrane_elements: bool
            quality_criterion_warping_of_membrane_elements_warning: float
            quality_criterion_warping_of_membrane_elements_failure: float
            quality_criterion_warping_of_non_membrane_elements: bool
            quality_criterion_warping_of_non_membrane_elements_warning: float
            quality_criterion_warping_of_non_membrane_elements_failure: float
            quality_criterion_jacobian_ratio: bool
            quality_criterion_jacobian_ratio_warning: float
            quality_criterion_jacobian_ratio_failure: float
            def __init__(self, quality_criterion_check_aspect_ratio: bool = ..., quality_criterion_check_aspect_ratio_warning: _Optional[float] = ..., quality_criterion_check_aspect_ratio_failure: _Optional[float] = ..., quality_criterion_parallel_deviations: bool = ..., quality_criterion_parallel_deviations_warning: _Optional[float] = ..., quality_criterion_parallel_deviations_failure: _Optional[float] = ..., quality_criterion_corner_angles_of_triangle_elements: bool = ..., quality_criterion_corner_angles_of_triangle_elements_warning: _Optional[float] = ..., quality_criterion_corner_angles_of_triangle_elements_failure: _Optional[float] = ..., quality_criterion_corner_angles_of_quadrangle_elements: bool = ..., quality_criterion_corner_angles_of_quadrangle_elements_warning: _Optional[float] = ..., quality_criterion_corner_angles_of_quadrangle_elements_failure: _Optional[float] = ..., quality_criterion_warping_of_membrane_elements: bool = ..., quality_criterion_warping_of_membrane_elements_warning: _Optional[float] = ..., quality_criterion_warping_of_membrane_elements_failure: _Optional[float] = ..., quality_criterion_warping_of_non_membrane_elements: bool = ..., quality_criterion_warping_of_non_membrane_elements_warning: _Optional[float] = ..., quality_criterion_warping_of_non_membrane_elements_failure: _Optional[float] = ..., quality_criterion_jacobian_ratio: bool = ..., quality_criterion_jacobian_ratio_warning: _Optional[float] = ..., quality_criterion_jacobian_ratio_failure: _Optional[float] = ...) -> None: ...
        MESH_QUALITY_COLOR_INDICATOR_OK_COLOR_FIELD_NUMBER: _ClassVar[int]
        MESH_QUALITY_COLOR_INDICATOR_WARNING_COLOR_FIELD_NUMBER: _ClassVar[int]
        MESH_QUALITY_COLOR_INDICATOR_FAILURE_COLOR_FIELD_NUMBER: _ClassVar[int]
        QUALITY_CRITERIA_CONFIG_FOR_SURFACES_FIELD_NUMBER: _ClassVar[int]
        mesh_quality_color_indicator_ok_color: _common_pb2.Color
        mesh_quality_color_indicator_warning_color: _common_pb2.Color
        mesh_quality_color_indicator_failure_color: _common_pb2.Color
        quality_criteria_config_for_surfaces: MeshSettings.SurfacesMeshQualityConfig.QualityCriteriaConfigForSurfaces
        def __init__(self, mesh_quality_color_indicator_ok_color: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., mesh_quality_color_indicator_warning_color: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., mesh_quality_color_indicator_failure_color: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., quality_criteria_config_for_surfaces: _Optional[_Union[MeshSettings.SurfacesMeshQualityConfig.QualityCriteriaConfigForSurfaces, _Mapping]] = ...) -> None: ...
    class SolidsMeshQualityConfig(_message.Message):
        __slots__ = ("mesh_quality_color_indicator_ok_color", "mesh_quality_color_indicator_warning_color", "mesh_quality_color_indicator_failure_color", "quality_criteria_config_for_solids")
        class QualityCriteriaConfigForSolids(_message.Message):
            __slots__ = ("quality_criterion_check_aspect_ratio", "quality_criterion_check_aspect_ratio_warning", "quality_criterion_check_aspect_ratio_failure", "quality_criterion_parallel_deviations", "quality_criterion_parallel_deviations_warning", "quality_criterion_parallel_deviations_failure", "quality_criterion_corner_angles_of_triangle_elements", "quality_criterion_corner_angles_of_triangle_elements_warning", "quality_criterion_corner_angles_of_triangle_elements_failure", "quality_criterion_corner_angles_of_quadrangle_elements", "quality_criterion_corner_angles_of_quadrangle_elements_warning", "quality_criterion_corner_angles_of_quadrangle_elements_failure", "quality_criterion_warping", "quality_criterion_warping_warning", "quality_criterion_warping_failure", "quality_criterion_jacobian_ratio", "quality_criterion_jacobian_ratio_warning", "quality_criterion_jacobian_ratio_failure")
            QUALITY_CRITERION_CHECK_ASPECT_RATIO_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_CHECK_ASPECT_RATIO_WARNING_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_CHECK_ASPECT_RATIO_FAILURE_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_PARALLEL_DEVIATIONS_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_PARALLEL_DEVIATIONS_WARNING_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_PARALLEL_DEVIATIONS_FAILURE_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_CORNER_ANGLES_OF_TRIANGLE_ELEMENTS_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_CORNER_ANGLES_OF_TRIANGLE_ELEMENTS_WARNING_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_CORNER_ANGLES_OF_TRIANGLE_ELEMENTS_FAILURE_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_CORNER_ANGLES_OF_QUADRANGLE_ELEMENTS_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_CORNER_ANGLES_OF_QUADRANGLE_ELEMENTS_WARNING_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_CORNER_ANGLES_OF_QUADRANGLE_ELEMENTS_FAILURE_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_WARPING_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_WARPING_WARNING_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_WARPING_FAILURE_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_JACOBIAN_RATIO_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_JACOBIAN_RATIO_WARNING_FIELD_NUMBER: _ClassVar[int]
            QUALITY_CRITERION_JACOBIAN_RATIO_FAILURE_FIELD_NUMBER: _ClassVar[int]
            quality_criterion_check_aspect_ratio: bool
            quality_criterion_check_aspect_ratio_warning: float
            quality_criterion_check_aspect_ratio_failure: float
            quality_criterion_parallel_deviations: bool
            quality_criterion_parallel_deviations_warning: float
            quality_criterion_parallel_deviations_failure: float
            quality_criterion_corner_angles_of_triangle_elements: bool
            quality_criterion_corner_angles_of_triangle_elements_warning: float
            quality_criterion_corner_angles_of_triangle_elements_failure: float
            quality_criterion_corner_angles_of_quadrangle_elements: bool
            quality_criterion_corner_angles_of_quadrangle_elements_warning: float
            quality_criterion_corner_angles_of_quadrangle_elements_failure: float
            quality_criterion_warping: bool
            quality_criterion_warping_warning: float
            quality_criterion_warping_failure: float
            quality_criterion_jacobian_ratio: bool
            quality_criterion_jacobian_ratio_warning: float
            quality_criterion_jacobian_ratio_failure: float
            def __init__(self, quality_criterion_check_aspect_ratio: bool = ..., quality_criterion_check_aspect_ratio_warning: _Optional[float] = ..., quality_criterion_check_aspect_ratio_failure: _Optional[float] = ..., quality_criterion_parallel_deviations: bool = ..., quality_criterion_parallel_deviations_warning: _Optional[float] = ..., quality_criterion_parallel_deviations_failure: _Optional[float] = ..., quality_criterion_corner_angles_of_triangle_elements: bool = ..., quality_criterion_corner_angles_of_triangle_elements_warning: _Optional[float] = ..., quality_criterion_corner_angles_of_triangle_elements_failure: _Optional[float] = ..., quality_criterion_corner_angles_of_quadrangle_elements: bool = ..., quality_criterion_corner_angles_of_quadrangle_elements_warning: _Optional[float] = ..., quality_criterion_corner_angles_of_quadrangle_elements_failure: _Optional[float] = ..., quality_criterion_warping: bool = ..., quality_criterion_warping_warning: _Optional[float] = ..., quality_criterion_warping_failure: _Optional[float] = ..., quality_criterion_jacobian_ratio: bool = ..., quality_criterion_jacobian_ratio_warning: _Optional[float] = ..., quality_criterion_jacobian_ratio_failure: _Optional[float] = ...) -> None: ...
        MESH_QUALITY_COLOR_INDICATOR_OK_COLOR_FIELD_NUMBER: _ClassVar[int]
        MESH_QUALITY_COLOR_INDICATOR_WARNING_COLOR_FIELD_NUMBER: _ClassVar[int]
        MESH_QUALITY_COLOR_INDICATOR_FAILURE_COLOR_FIELD_NUMBER: _ClassVar[int]
        QUALITY_CRITERIA_CONFIG_FOR_SOLIDS_FIELD_NUMBER: _ClassVar[int]
        mesh_quality_color_indicator_ok_color: _common_pb2.Color
        mesh_quality_color_indicator_warning_color: _common_pb2.Color
        mesh_quality_color_indicator_failure_color: _common_pb2.Color
        quality_criteria_config_for_solids: MeshSettings.SolidsMeshQualityConfig.QualityCriteriaConfigForSolids
        def __init__(self, mesh_quality_color_indicator_ok_color: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., mesh_quality_color_indicator_warning_color: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., mesh_quality_color_indicator_failure_color: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., quality_criteria_config_for_solids: _Optional[_Union[MeshSettings.SolidsMeshQualityConfig.QualityCriteriaConfigForSolids, _Mapping]] = ...) -> None: ...
    class WindSimulationMeshConfig(_message.Message):
        __slots__ = ("windsimulation_mesh_config_value_shrink_wrapping_main_structure", "windsimulation_mesh_config_value_shrink_wrapping_surrounding_objects", "windsimulation_mesh_config_value_shrink_wrapping_terrain", "windsimulation_mesh_config_value_member_detail_size", "windsimulation_mesh_config_value_use_only_external_surface_for_hollow_sections", "windsimulation_mesh_config_value_consider_surface_thickness_above_enabled", "windsimulation_mesh_config_value_consider_surface_thickness_above_value", "windsimulation_mesh_config_value_terrain_enabled", "windsimulation_mesh_config_value_keep_results_if_mesh_deleted", "windsimulation_mesh_config_value_run_rwind_silent")
        WINDSIMULATION_MESH_CONFIG_VALUE_SHRINK_WRAPPING_MAIN_STRUCTURE_FIELD_NUMBER: _ClassVar[int]
        WINDSIMULATION_MESH_CONFIG_VALUE_SHRINK_WRAPPING_SURROUNDING_OBJECTS_FIELD_NUMBER: _ClassVar[int]
        WINDSIMULATION_MESH_CONFIG_VALUE_SHRINK_WRAPPING_TERRAIN_FIELD_NUMBER: _ClassVar[int]
        WINDSIMULATION_MESH_CONFIG_VALUE_MEMBER_DETAIL_SIZE_FIELD_NUMBER: _ClassVar[int]
        WINDSIMULATION_MESH_CONFIG_VALUE_USE_ONLY_EXTERNAL_SURFACE_FOR_HOLLOW_SECTIONS_FIELD_NUMBER: _ClassVar[int]
        WINDSIMULATION_MESH_CONFIG_VALUE_CONSIDER_SURFACE_THICKNESS_ABOVE_ENABLED_FIELD_NUMBER: _ClassVar[int]
        WINDSIMULATION_MESH_CONFIG_VALUE_CONSIDER_SURFACE_THICKNESS_ABOVE_VALUE_FIELD_NUMBER: _ClassVar[int]
        WINDSIMULATION_MESH_CONFIG_VALUE_TERRAIN_ENABLED_FIELD_NUMBER: _ClassVar[int]
        WINDSIMULATION_MESH_CONFIG_VALUE_KEEP_RESULTS_IF_MESH_DELETED_FIELD_NUMBER: _ClassVar[int]
        WINDSIMULATION_MESH_CONFIG_VALUE_RUN_RWIND_SILENT_FIELD_NUMBER: _ClassVar[int]
        windsimulation_mesh_config_value_shrink_wrapping_main_structure: int
        windsimulation_mesh_config_value_shrink_wrapping_surrounding_objects: int
        windsimulation_mesh_config_value_shrink_wrapping_terrain: int
        windsimulation_mesh_config_value_member_detail_size: int
        windsimulation_mesh_config_value_use_only_external_surface_for_hollow_sections: bool
        windsimulation_mesh_config_value_consider_surface_thickness_above_enabled: bool
        windsimulation_mesh_config_value_consider_surface_thickness_above_value: float
        windsimulation_mesh_config_value_terrain_enabled: bool
        windsimulation_mesh_config_value_keep_results_if_mesh_deleted: bool
        windsimulation_mesh_config_value_run_rwind_silent: bool
        def __init__(self, windsimulation_mesh_config_value_shrink_wrapping_main_structure: _Optional[int] = ..., windsimulation_mesh_config_value_shrink_wrapping_surrounding_objects: _Optional[int] = ..., windsimulation_mesh_config_value_shrink_wrapping_terrain: _Optional[int] = ..., windsimulation_mesh_config_value_member_detail_size: _Optional[int] = ..., windsimulation_mesh_config_value_use_only_external_surface_for_hollow_sections: bool = ..., windsimulation_mesh_config_value_consider_surface_thickness_above_enabled: bool = ..., windsimulation_mesh_config_value_consider_surface_thickness_above_value: _Optional[float] = ..., windsimulation_mesh_config_value_terrain_enabled: bool = ..., windsimulation_mesh_config_value_keep_results_if_mesh_deleted: bool = ..., windsimulation_mesh_config_value_run_rwind_silent: bool = ...) -> None: ...
    GENERAL_TARGET_LENGTH_OF_FE_FIELD_NUMBER: _ClassVar[int]
    GENERAL_MAXIMUM_DISTANCE_BETWEEN_NODE_AND_LINE_FIELD_NUMBER: _ClassVar[int]
    GENERAL_INDEPENDENT_MESH_PREFERRED_FIELD_NUMBER: _ClassVar[int]
    GENERAL_INDEPENDENT_MESH_CONNECT_ELIMINATED_NODE_FIELD_NUMBER: _ClassVar[int]
    GENERAL_INDEPENDENT_MESH_CONNECT_ELIMINATED_NODE_TO_GROUP_OF_ELEMENTS_RADIUS_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_NUMBER_OF_DIVISIONS_FOR_SPECIAL_TYPES_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_ACTIVATE_DIVISION_DUE_TO_ANALYSIS_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_NUMBER_OF_DIVISIONS_FOR_RESULT_DIAGRAM_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_NUMBER_OF_DIVISIONS_FOR_MIN_MAX_VALUES_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_USE_DIVISION_FOR_CONCRETE_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_NUMBER_OF_DIVISIONS_FOR_CONCRETE_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_USE_DIVISION_FOR_MEMBERS_WITH_NODES_FIELD_NUMBER: _ClassVar[int]
    SURFACES_MAXIMUM_RATIO_OF_FE_FIELD_NUMBER: _ClassVar[int]
    SURFACES_MAXIMUM_OUT_OF_PLANE_INCLINATION_FIELD_NUMBER: _ClassVar[int]
    SURFACES_MESH_REFINEMENT_FIELD_NUMBER: _ClassVar[int]
    SURFACES_RELATIONSHIP_FIELD_NUMBER: _ClassVar[int]
    SURFACES_INTEGRATE_ALSO_UNUTILIZED_OBJECTS_FIELD_NUMBER: _ClassVar[int]
    SURFACES_SHAPE_OF_FINITE_ELEMENTS_FIELD_NUMBER: _ClassVar[int]
    SURFACES_SAME_SQUARES_FIELD_NUMBER: _ClassVar[int]
    SURFACES_TRIANGLES_FOR_MEMBRANES_FIELD_NUMBER: _ClassVar[int]
    SURFACES_MAPPED_MESH_PREFERRED_FIELD_NUMBER: _ClassVar[int]
    SOLIDS_USE_REFINEMENT_IF_CONTAINING_CLOSE_NODES_FIELD_NUMBER: _ClassVar[int]
    SOLIDS_MAXIMUM_NUMBER_OF_ELEMENTS_FIELD_NUMBER: _ClassVar[int]
    SOLIDS_USE_TARGET_LENGTH_OF_FE_FOR_TYPE_SOIL_FIELD_NUMBER: _ClassVar[int]
    SOLIDS_TARGET_LENGTH_OF_FE_FOR_TYPE_SOIL_FIELD_NUMBER: _ClassVar[int]
    SURFACES_MESH_QUALITY_CONFIG_FIELD_NUMBER: _ClassVar[int]
    SOLIDS_MESH_QUALITY_CONFIG_FIELD_NUMBER: _ClassVar[int]
    WIND_SIMULATION_MESH_CONFIG_FIELD_NUMBER: _ClassVar[int]
    general_target_length_of_fe: float
    general_maximum_distance_between_node_and_line: float
    general_independent_mesh_preferred: bool
    general_independent_mesh_connect_eliminated_node: int
    general_independent_mesh_connect_eliminated_node_to_group_of_elements_radius: float
    members_number_of_divisions_for_special_types: int
    members_activate_division_due_to_analysis_settings: bool
    members_number_of_divisions_for_result_diagram: int
    members_number_of_divisions_for_min_max_values: int
    members_use_division_for_concrete_members: bool
    members_number_of_divisions_for_concrete_members: int
    members_use_division_for_members_with_nodes: bool
    surfaces_maximum_ratio_of_fe: float
    surfaces_maximum_out_of_plane_inclination: float
    surfaces_mesh_refinement: bool
    surfaces_relationship: float
    surfaces_integrate_also_unutilized_objects: bool
    surfaces_shape_of_finite_elements: MeshSettings.SurfacesShapeOfFiniteElementsType
    surfaces_same_squares: bool
    surfaces_triangles_for_membranes: bool
    surfaces_mapped_mesh_preferred: bool
    solids_use_refinement_if_containing_close_nodes: bool
    solids_maximum_number_of_elements: int
    solids_use_target_length_of_fe_for_type_soil: bool
    solids_target_length_of_fe_for_type_soil: float
    surfaces_mesh_quality_config: MeshSettings.SurfacesMeshQualityConfig
    solids_mesh_quality_config: MeshSettings.SolidsMeshQualityConfig
    wind_simulation_mesh_config: MeshSettings.WindSimulationMeshConfig
    def __init__(self, general_target_length_of_fe: _Optional[float] = ..., general_maximum_distance_between_node_and_line: _Optional[float] = ..., general_independent_mesh_preferred: bool = ..., general_independent_mesh_connect_eliminated_node: _Optional[int] = ..., general_independent_mesh_connect_eliminated_node_to_group_of_elements_radius: _Optional[float] = ..., members_number_of_divisions_for_special_types: _Optional[int] = ..., members_activate_division_due_to_analysis_settings: bool = ..., members_number_of_divisions_for_result_diagram: _Optional[int] = ..., members_number_of_divisions_for_min_max_values: _Optional[int] = ..., members_use_division_for_concrete_members: bool = ..., members_number_of_divisions_for_concrete_members: _Optional[int] = ..., members_use_division_for_members_with_nodes: bool = ..., surfaces_maximum_ratio_of_fe: _Optional[float] = ..., surfaces_maximum_out_of_plane_inclination: _Optional[float] = ..., surfaces_mesh_refinement: bool = ..., surfaces_relationship: _Optional[float] = ..., surfaces_integrate_also_unutilized_objects: bool = ..., surfaces_shape_of_finite_elements: _Optional[_Union[MeshSettings.SurfacesShapeOfFiniteElementsType, str]] = ..., surfaces_same_squares: bool = ..., surfaces_triangles_for_membranes: bool = ..., surfaces_mapped_mesh_preferred: bool = ..., solids_use_refinement_if_containing_close_nodes: bool = ..., solids_maximum_number_of_elements: _Optional[int] = ..., solids_use_target_length_of_fe_for_type_soil: bool = ..., solids_target_length_of_fe_for_type_soil: _Optional[float] = ..., surfaces_mesh_quality_config: _Optional[_Union[MeshSettings.SurfacesMeshQualityConfig, _Mapping]] = ..., solids_mesh_quality_config: _Optional[_Union[MeshSettings.SolidsMeshQualityConfig, _Mapping]] = ..., wind_simulation_mesh_config: _Optional[_Union[MeshSettings.WindSimulationMeshConfig, _Mapping]] = ...) -> None: ...

class MeshStatistics(_message.Message):
    __slots__ = ("member_1D_finite_elements", "surface_2D_finite_elements", "solid_3D_finite_elements", "node_elements")
    MEMBER_1D_FINITE_ELEMENTS_FIELD_NUMBER: _ClassVar[int]
    SURFACE_2D_FINITE_ELEMENTS_FIELD_NUMBER: _ClassVar[int]
    SOLID_3D_FINITE_ELEMENTS_FIELD_NUMBER: _ClassVar[int]
    NODE_ELEMENTS_FIELD_NUMBER: _ClassVar[int]
    member_1D_finite_elements: int
    surface_2D_finite_elements: int
    solid_3D_finite_elements: int
    node_elements: int
    def __init__(self, member_1D_finite_elements: _Optional[int] = ..., surface_2D_finite_elements: _Optional[int] = ..., solid_3D_finite_elements: _Optional[int] = ..., node_elements: _Optional[int] = ...) -> None: ...
