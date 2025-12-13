from dlubal.api.common import common_pb2 as _common_pb2
from dlubal.api.rfem import object_id_pb2 as _object_id_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NodalReleaseType(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "nodal_releases", "coordinate_system", "axial_release_n", "axial_release_vy", "axial_release_vz", "moment_release_mt", "moment_release_my", "moment_release_mz", "axial_release_n_nonlinearity", "axial_release_vy_nonlinearity", "axial_release_vz_nonlinearity", "moment_release_mt_nonlinearity", "moment_release_my_nonlinearity", "moment_release_mz_nonlinearity", "partial_activity_along_x_negative_type", "partial_activity_along_x_positive_type", "partial_activity_along_y_negative_type", "partial_activity_along_y_positive_type", "partial_activity_along_z_negative_type", "partial_activity_along_z_positive_type", "partial_activity_around_x_negative_type", "partial_activity_around_x_positive_type", "partial_activity_around_y_negative_type", "partial_activity_around_y_positive_type", "partial_activity_around_z_negative_type", "partial_activity_around_z_positive_type", "partial_activity_along_x_negative_displacement", "partial_activity_along_x_positive_displacement", "partial_activity_along_y_negative_displacement", "partial_activity_along_y_positive_displacement", "partial_activity_along_z_negative_displacement", "partial_activity_along_z_positive_displacement", "partial_activity_around_x_negative_rotation", "partial_activity_around_x_positive_rotation", "partial_activity_around_y_negative_rotation", "partial_activity_around_y_positive_rotation", "partial_activity_around_z_negative_rotation", "partial_activity_around_z_positive_rotation", "partial_activity_along_x_negative_force", "partial_activity_along_x_positive_force", "partial_activity_along_y_negative_force", "partial_activity_along_y_positive_force", "partial_activity_along_z_negative_force", "partial_activity_along_z_positive_force", "partial_activity_around_x_negative_moment", "partial_activity_around_x_positive_moment", "partial_activity_around_y_negative_moment", "partial_activity_around_y_positive_moment", "partial_activity_around_z_negative_moment", "partial_activity_around_z_positive_moment", "partial_activity_along_x_negative_slippage", "partial_activity_along_x_positive_slippage", "partial_activity_along_y_negative_slippage", "partial_activity_along_y_positive_slippage", "partial_activity_along_z_negative_slippage", "partial_activity_along_z_positive_slippage", "partial_activity_around_x_negative_slippage", "partial_activity_around_x_positive_slippage", "partial_activity_around_y_negative_slippage", "partial_activity_around_y_positive_slippage", "partial_activity_around_z_negative_slippage", "partial_activity_around_z_positive_slippage", "diagram_along_x_symmetric", "diagram_along_y_symmetric", "diagram_along_z_symmetric", "diagram_around_x_symmetric", "diagram_around_y_symmetric", "diagram_around_z_symmetric", "diagram_along_x_is_sorted", "diagram_along_y_is_sorted", "diagram_along_z_is_sorted", "diagram_around_x_is_sorted", "diagram_around_y_is_sorted", "diagram_around_z_is_sorted", "diagram_along_x_start", "diagram_along_y_start", "diagram_along_z_start", "diagram_around_x_start", "diagram_around_y_start", "diagram_around_z_start", "diagram_along_x_end", "diagram_along_y_end", "diagram_along_z_end", "diagram_around_x_end", "diagram_around_y_end", "diagram_around_z_end", "diagram_along_x_table", "diagram_along_y_table", "diagram_along_z_table", "diagram_around_x_table", "diagram_around_y_table", "diagram_around_z_table", "diagram_along_x_ac_yield_minus", "diagram_along_y_ac_yield_minus", "diagram_along_z_ac_yield_minus", "diagram_around_x_ac_yield_minus", "diagram_around_y_ac_yield_minus", "diagram_around_z_ac_yield_minus", "diagram_along_x_ac_yield_plus", "diagram_along_y_ac_yield_plus", "diagram_along_z_ac_yield_plus", "diagram_around_x_ac_yield_plus", "diagram_around_y_ac_yield_plus", "diagram_around_z_ac_yield_plus", "diagram_along_x_acceptance_criteria_active", "diagram_along_y_acceptance_criteria_active", "diagram_along_z_acceptance_criteria_active", "diagram_around_x_acceptance_criteria_active", "diagram_around_y_acceptance_criteria_active", "diagram_around_z_acceptance_criteria_active", "diagram_along_x_minus_color_one", "diagram_along_y_minus_color_one", "diagram_along_z_minus_color_one", "diagram_around_x_minus_color_one", "diagram_around_y_minus_color_one", "diagram_around_z_minus_color_one", "diagram_along_x_minus_color_two", "diagram_along_y_minus_color_two", "diagram_along_z_minus_color_two", "diagram_around_x_minus_color_two", "diagram_around_y_minus_color_two", "diagram_around_z_minus_color_two", "diagram_along_x_plus_color_one", "diagram_along_y_plus_color_one", "diagram_along_z_plus_color_one", "diagram_around_x_plus_color_one", "diagram_around_y_plus_color_one", "diagram_around_z_plus_color_one", "diagram_along_x_plus_color_two", "diagram_along_y_plus_color_two", "diagram_along_z_plus_color_two", "diagram_around_x_plus_color_two", "diagram_around_y_plus_color_two", "diagram_around_z_plus_color_two", "diagram_along_x_color_table", "diagram_along_y_color_table", "diagram_along_z_color_table", "diagram_around_x_color_table", "diagram_around_y_color_table", "diagram_around_z_color_table", "plastic_diagram_along_x_table", "plastic_diagram_along_y_table", "plastic_diagram_along_z_table", "plastic_diagram_around_y_table", "plastic_diagram_around_z_table", "plastic_diagram_along_x_symmetric", "plastic_diagram_along_y_symmetric", "plastic_diagram_along_z_symmetric", "plastic_diagram_around_y_symmetric", "plastic_diagram_around_z_symmetric", "plastic_diagram_around_y_force_interaction", "plastic_diagram_around_z_force_interaction", "plastic_diagram_along_x_user_defined", "plastic_diagram_along_y_user_defined", "plastic_diagram_along_z_user_defined", "plastic_diagram_around_y_user_defined", "plastic_diagram_around_z_user_defined", "plastic_diagram_along_x_is_user_defined_member_length", "plastic_diagram_along_y_is_user_defined_member_length", "plastic_diagram_along_z_is_user_defined_member_length", "plastic_diagram_around_y_is_user_defined_member_length", "plastic_diagram_around_z_is_user_defined_member_length", "plastic_diagram_along_x_user_defined_member_length", "plastic_diagram_along_y_user_defined_member_length", "plastic_diagram_along_z_user_defined_member_length", "plastic_diagram_around_y_user_defined_member_length", "plastic_diagram_around_z_user_defined_member_length", "plastic_diagram_along_x_attached_members_min_max_length", "plastic_diagram_along_y_attached_members_min_max_length", "plastic_diagram_along_z_attached_members_min_max_length", "plastic_diagram_around_y_attached_members_min_max_length", "plastic_diagram_around_z_attached_members_min_max_length", "plastic_diagram_along_x_io_negative", "plastic_diagram_along_y_io_negative", "plastic_diagram_along_z_io_negative", "plastic_diagram_around_y_io_negative", "plastic_diagram_around_z_io_negative", "plastic_diagram_along_x_io_positive", "plastic_diagram_along_y_io_positive", "plastic_diagram_along_z_io_positive", "plastic_diagram_around_y_io_positive", "plastic_diagram_around_z_io_positive", "plastic_diagram_along_x_ls_negative", "plastic_diagram_along_y_ls_negative", "plastic_diagram_along_z_ls_negative", "plastic_diagram_around_y_ls_negative", "plastic_diagram_around_z_ls_negative", "plastic_diagram_along_x_ls_positive", "plastic_diagram_along_y_ls_positive", "plastic_diagram_along_z_ls_positive", "plastic_diagram_around_y_ls_positive", "plastic_diagram_around_z_ls_positive", "plastic_diagram_along_x_cp_negative", "plastic_diagram_along_y_cp_negative", "plastic_diagram_along_z_cp_negative", "plastic_diagram_around_y_cp_negative", "plastic_diagram_around_z_cp_negative", "plastic_diagram_along_x_cp_positive", "plastic_diagram_along_y_cp_positive", "plastic_diagram_along_z_cp_positive", "plastic_diagram_around_y_cp_positive", "plastic_diagram_around_z_cp_positive", "plastic_diagram_along_x_minus_color_one", "plastic_diagram_along_y_minus_color_one", "plastic_diagram_along_z_minus_color_one", "plastic_diagram_around_y_minus_color_one", "plastic_diagram_around_z_minus_color_one", "plastic_diagram_along_x_minus_color_two", "plastic_diagram_along_y_minus_color_two", "plastic_diagram_along_z_minus_color_two", "plastic_diagram_around_y_minus_color_two", "plastic_diagram_around_z_minus_color_two", "plastic_diagram_along_x_minus_color_three", "plastic_diagram_along_y_minus_color_three", "plastic_diagram_along_z_minus_color_three", "plastic_diagram_around_y_minus_color_three", "plastic_diagram_around_z_minus_color_three", "plastic_diagram_along_x_minus_color_four", "plastic_diagram_along_y_minus_color_four", "plastic_diagram_along_z_minus_color_four", "plastic_diagram_around_y_minus_color_four", "plastic_diagram_around_z_minus_color_four", "plastic_diagram_along_x_plus_color_one", "plastic_diagram_along_y_plus_color_one", "plastic_diagram_along_z_plus_color_one", "plastic_diagram_around_y_plus_color_one", "plastic_diagram_around_z_plus_color_one", "plastic_diagram_along_x_plus_color_two", "plastic_diagram_along_y_plus_color_two", "plastic_diagram_along_z_plus_color_two", "plastic_diagram_around_y_plus_color_two", "plastic_diagram_around_z_plus_color_two", "plastic_diagram_along_x_plus_color_three", "plastic_diagram_along_y_plus_color_three", "plastic_diagram_along_z_plus_color_three", "plastic_diagram_around_y_plus_color_three", "plastic_diagram_around_z_plus_color_three", "plastic_diagram_along_x_plus_color_four", "plastic_diagram_along_y_plus_color_four", "plastic_diagram_along_z_plus_color_four", "plastic_diagram_around_y_plus_color_four", "plastic_diagram_around_z_plus_color_four", "plastic_diagram_along_x_component_type", "plastic_diagram_along_y_component_type", "plastic_diagram_along_z_component_type", "plastic_diagram_around_y_component_type", "plastic_diagram_around_z_component_type", "plastic_diagram_along_x_color_table", "plastic_diagram_along_y_color_table", "plastic_diagram_along_z_color_table", "plastic_diagram_around_y_color_table", "plastic_diagram_around_z_color_table", "friction_coefficient_x", "friction_coefficient_xy", "friction_coefficient_xz", "friction_coefficient_y", "friction_coefficient_yx", "friction_coefficient_yz", "friction_coefficient_z", "friction_coefficient_zx", "friction_coefficient_zy", "friction_direction_independent_x", "friction_direction_independent_y", "friction_direction_independent_z", "comment", "is_generated", "generating_object_info", "generated_by_pile", "local_axis_system_object_type", "local_axis_system_reference_object", "id_for_export_import", "metadata_for_export_import")
    class AxialReleaseNNonlinearity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        AXIAL_RELEASE_N_NONLINEARITY_NONE: _ClassVar[NodalReleaseType.AxialReleaseNNonlinearity]
        AXIAL_RELEASE_N_NONLINEARITY_DIAGRAM: _ClassVar[NodalReleaseType.AxialReleaseNNonlinearity]
        AXIAL_RELEASE_N_NONLINEARITY_FAILURE_ALL_IF_NEGATIVE: _ClassVar[NodalReleaseType.AxialReleaseNNonlinearity]
        AXIAL_RELEASE_N_NONLINEARITY_FAILURE_ALL_IF_POSITIVE: _ClassVar[NodalReleaseType.AxialReleaseNNonlinearity]
        AXIAL_RELEASE_N_NONLINEARITY_FAILURE_IF_NEGATIVE: _ClassVar[NodalReleaseType.AxialReleaseNNonlinearity]
        AXIAL_RELEASE_N_NONLINEARITY_FAILURE_IF_POSITIVE: _ClassVar[NodalReleaseType.AxialReleaseNNonlinearity]
        AXIAL_RELEASE_N_NONLINEARITY_FORCE_MOMENT_DIAGRAM: _ClassVar[NodalReleaseType.AxialReleaseNNonlinearity]
        AXIAL_RELEASE_N_NONLINEARITY_FRICTION_DIRECTION_1: _ClassVar[NodalReleaseType.AxialReleaseNNonlinearity]
        AXIAL_RELEASE_N_NONLINEARITY_FRICTION_DIRECTION_1_2: _ClassVar[NodalReleaseType.AxialReleaseNNonlinearity]
        AXIAL_RELEASE_N_NONLINEARITY_FRICTION_DIRECTION_1_PLUS_2: _ClassVar[NodalReleaseType.AxialReleaseNNonlinearity]
        AXIAL_RELEASE_N_NONLINEARITY_FRICTION_DIRECTION_2: _ClassVar[NodalReleaseType.AxialReleaseNNonlinearity]
        AXIAL_RELEASE_N_NONLINEARITY_PARTIAL_ACTIVITY: _ClassVar[NodalReleaseType.AxialReleaseNNonlinearity]
        AXIAL_RELEASE_N_NONLINEARITY_STIFFNESS_DIAGRAM: _ClassVar[NodalReleaseType.AxialReleaseNNonlinearity]
    AXIAL_RELEASE_N_NONLINEARITY_NONE: NodalReleaseType.AxialReleaseNNonlinearity
    AXIAL_RELEASE_N_NONLINEARITY_DIAGRAM: NodalReleaseType.AxialReleaseNNonlinearity
    AXIAL_RELEASE_N_NONLINEARITY_FAILURE_ALL_IF_NEGATIVE: NodalReleaseType.AxialReleaseNNonlinearity
    AXIAL_RELEASE_N_NONLINEARITY_FAILURE_ALL_IF_POSITIVE: NodalReleaseType.AxialReleaseNNonlinearity
    AXIAL_RELEASE_N_NONLINEARITY_FAILURE_IF_NEGATIVE: NodalReleaseType.AxialReleaseNNonlinearity
    AXIAL_RELEASE_N_NONLINEARITY_FAILURE_IF_POSITIVE: NodalReleaseType.AxialReleaseNNonlinearity
    AXIAL_RELEASE_N_NONLINEARITY_FORCE_MOMENT_DIAGRAM: NodalReleaseType.AxialReleaseNNonlinearity
    AXIAL_RELEASE_N_NONLINEARITY_FRICTION_DIRECTION_1: NodalReleaseType.AxialReleaseNNonlinearity
    AXIAL_RELEASE_N_NONLINEARITY_FRICTION_DIRECTION_1_2: NodalReleaseType.AxialReleaseNNonlinearity
    AXIAL_RELEASE_N_NONLINEARITY_FRICTION_DIRECTION_1_PLUS_2: NodalReleaseType.AxialReleaseNNonlinearity
    AXIAL_RELEASE_N_NONLINEARITY_FRICTION_DIRECTION_2: NodalReleaseType.AxialReleaseNNonlinearity
    AXIAL_RELEASE_N_NONLINEARITY_PARTIAL_ACTIVITY: NodalReleaseType.AxialReleaseNNonlinearity
    AXIAL_RELEASE_N_NONLINEARITY_STIFFNESS_DIAGRAM: NodalReleaseType.AxialReleaseNNonlinearity
    class AxialReleaseVyNonlinearity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        AXIAL_RELEASE_VY_NONLINEARITY_NONE: _ClassVar[NodalReleaseType.AxialReleaseVyNonlinearity]
        AXIAL_RELEASE_VY_NONLINEARITY_DIAGRAM: _ClassVar[NodalReleaseType.AxialReleaseVyNonlinearity]
        AXIAL_RELEASE_VY_NONLINEARITY_FAILURE_ALL_IF_NEGATIVE: _ClassVar[NodalReleaseType.AxialReleaseVyNonlinearity]
        AXIAL_RELEASE_VY_NONLINEARITY_FAILURE_ALL_IF_POSITIVE: _ClassVar[NodalReleaseType.AxialReleaseVyNonlinearity]
        AXIAL_RELEASE_VY_NONLINEARITY_FAILURE_IF_NEGATIVE: _ClassVar[NodalReleaseType.AxialReleaseVyNonlinearity]
        AXIAL_RELEASE_VY_NONLINEARITY_FAILURE_IF_POSITIVE: _ClassVar[NodalReleaseType.AxialReleaseVyNonlinearity]
        AXIAL_RELEASE_VY_NONLINEARITY_FORCE_MOMENT_DIAGRAM: _ClassVar[NodalReleaseType.AxialReleaseVyNonlinearity]
        AXIAL_RELEASE_VY_NONLINEARITY_FRICTION_DIRECTION_1: _ClassVar[NodalReleaseType.AxialReleaseVyNonlinearity]
        AXIAL_RELEASE_VY_NONLINEARITY_FRICTION_DIRECTION_1_2: _ClassVar[NodalReleaseType.AxialReleaseVyNonlinearity]
        AXIAL_RELEASE_VY_NONLINEARITY_FRICTION_DIRECTION_1_PLUS_2: _ClassVar[NodalReleaseType.AxialReleaseVyNonlinearity]
        AXIAL_RELEASE_VY_NONLINEARITY_FRICTION_DIRECTION_2: _ClassVar[NodalReleaseType.AxialReleaseVyNonlinearity]
        AXIAL_RELEASE_VY_NONLINEARITY_PARTIAL_ACTIVITY: _ClassVar[NodalReleaseType.AxialReleaseVyNonlinearity]
        AXIAL_RELEASE_VY_NONLINEARITY_STIFFNESS_DIAGRAM: _ClassVar[NodalReleaseType.AxialReleaseVyNonlinearity]
    AXIAL_RELEASE_VY_NONLINEARITY_NONE: NodalReleaseType.AxialReleaseVyNonlinearity
    AXIAL_RELEASE_VY_NONLINEARITY_DIAGRAM: NodalReleaseType.AxialReleaseVyNonlinearity
    AXIAL_RELEASE_VY_NONLINEARITY_FAILURE_ALL_IF_NEGATIVE: NodalReleaseType.AxialReleaseVyNonlinearity
    AXIAL_RELEASE_VY_NONLINEARITY_FAILURE_ALL_IF_POSITIVE: NodalReleaseType.AxialReleaseVyNonlinearity
    AXIAL_RELEASE_VY_NONLINEARITY_FAILURE_IF_NEGATIVE: NodalReleaseType.AxialReleaseVyNonlinearity
    AXIAL_RELEASE_VY_NONLINEARITY_FAILURE_IF_POSITIVE: NodalReleaseType.AxialReleaseVyNonlinearity
    AXIAL_RELEASE_VY_NONLINEARITY_FORCE_MOMENT_DIAGRAM: NodalReleaseType.AxialReleaseVyNonlinearity
    AXIAL_RELEASE_VY_NONLINEARITY_FRICTION_DIRECTION_1: NodalReleaseType.AxialReleaseVyNonlinearity
    AXIAL_RELEASE_VY_NONLINEARITY_FRICTION_DIRECTION_1_2: NodalReleaseType.AxialReleaseVyNonlinearity
    AXIAL_RELEASE_VY_NONLINEARITY_FRICTION_DIRECTION_1_PLUS_2: NodalReleaseType.AxialReleaseVyNonlinearity
    AXIAL_RELEASE_VY_NONLINEARITY_FRICTION_DIRECTION_2: NodalReleaseType.AxialReleaseVyNonlinearity
    AXIAL_RELEASE_VY_NONLINEARITY_PARTIAL_ACTIVITY: NodalReleaseType.AxialReleaseVyNonlinearity
    AXIAL_RELEASE_VY_NONLINEARITY_STIFFNESS_DIAGRAM: NodalReleaseType.AxialReleaseVyNonlinearity
    class AxialReleaseVzNonlinearity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        AXIAL_RELEASE_VZ_NONLINEARITY_NONE: _ClassVar[NodalReleaseType.AxialReleaseVzNonlinearity]
        AXIAL_RELEASE_VZ_NONLINEARITY_DIAGRAM: _ClassVar[NodalReleaseType.AxialReleaseVzNonlinearity]
        AXIAL_RELEASE_VZ_NONLINEARITY_FAILURE_ALL_IF_NEGATIVE: _ClassVar[NodalReleaseType.AxialReleaseVzNonlinearity]
        AXIAL_RELEASE_VZ_NONLINEARITY_FAILURE_ALL_IF_POSITIVE: _ClassVar[NodalReleaseType.AxialReleaseVzNonlinearity]
        AXIAL_RELEASE_VZ_NONLINEARITY_FAILURE_IF_NEGATIVE: _ClassVar[NodalReleaseType.AxialReleaseVzNonlinearity]
        AXIAL_RELEASE_VZ_NONLINEARITY_FAILURE_IF_POSITIVE: _ClassVar[NodalReleaseType.AxialReleaseVzNonlinearity]
        AXIAL_RELEASE_VZ_NONLINEARITY_FORCE_MOMENT_DIAGRAM: _ClassVar[NodalReleaseType.AxialReleaseVzNonlinearity]
        AXIAL_RELEASE_VZ_NONLINEARITY_FRICTION_DIRECTION_1: _ClassVar[NodalReleaseType.AxialReleaseVzNonlinearity]
        AXIAL_RELEASE_VZ_NONLINEARITY_FRICTION_DIRECTION_1_2: _ClassVar[NodalReleaseType.AxialReleaseVzNonlinearity]
        AXIAL_RELEASE_VZ_NONLINEARITY_FRICTION_DIRECTION_1_PLUS_2: _ClassVar[NodalReleaseType.AxialReleaseVzNonlinearity]
        AXIAL_RELEASE_VZ_NONLINEARITY_FRICTION_DIRECTION_2: _ClassVar[NodalReleaseType.AxialReleaseVzNonlinearity]
        AXIAL_RELEASE_VZ_NONLINEARITY_PARTIAL_ACTIVITY: _ClassVar[NodalReleaseType.AxialReleaseVzNonlinearity]
        AXIAL_RELEASE_VZ_NONLINEARITY_STIFFNESS_DIAGRAM: _ClassVar[NodalReleaseType.AxialReleaseVzNonlinearity]
    AXIAL_RELEASE_VZ_NONLINEARITY_NONE: NodalReleaseType.AxialReleaseVzNonlinearity
    AXIAL_RELEASE_VZ_NONLINEARITY_DIAGRAM: NodalReleaseType.AxialReleaseVzNonlinearity
    AXIAL_RELEASE_VZ_NONLINEARITY_FAILURE_ALL_IF_NEGATIVE: NodalReleaseType.AxialReleaseVzNonlinearity
    AXIAL_RELEASE_VZ_NONLINEARITY_FAILURE_ALL_IF_POSITIVE: NodalReleaseType.AxialReleaseVzNonlinearity
    AXIAL_RELEASE_VZ_NONLINEARITY_FAILURE_IF_NEGATIVE: NodalReleaseType.AxialReleaseVzNonlinearity
    AXIAL_RELEASE_VZ_NONLINEARITY_FAILURE_IF_POSITIVE: NodalReleaseType.AxialReleaseVzNonlinearity
    AXIAL_RELEASE_VZ_NONLINEARITY_FORCE_MOMENT_DIAGRAM: NodalReleaseType.AxialReleaseVzNonlinearity
    AXIAL_RELEASE_VZ_NONLINEARITY_FRICTION_DIRECTION_1: NodalReleaseType.AxialReleaseVzNonlinearity
    AXIAL_RELEASE_VZ_NONLINEARITY_FRICTION_DIRECTION_1_2: NodalReleaseType.AxialReleaseVzNonlinearity
    AXIAL_RELEASE_VZ_NONLINEARITY_FRICTION_DIRECTION_1_PLUS_2: NodalReleaseType.AxialReleaseVzNonlinearity
    AXIAL_RELEASE_VZ_NONLINEARITY_FRICTION_DIRECTION_2: NodalReleaseType.AxialReleaseVzNonlinearity
    AXIAL_RELEASE_VZ_NONLINEARITY_PARTIAL_ACTIVITY: NodalReleaseType.AxialReleaseVzNonlinearity
    AXIAL_RELEASE_VZ_NONLINEARITY_STIFFNESS_DIAGRAM: NodalReleaseType.AxialReleaseVzNonlinearity
    class MomentReleaseMtNonlinearity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        MOMENT_RELEASE_MT_NONLINEARITY_NONE: _ClassVar[NodalReleaseType.MomentReleaseMtNonlinearity]
        MOMENT_RELEASE_MT_NONLINEARITY_DIAGRAM: _ClassVar[NodalReleaseType.MomentReleaseMtNonlinearity]
        MOMENT_RELEASE_MT_NONLINEARITY_FAILURE_ALL_IF_NEGATIVE: _ClassVar[NodalReleaseType.MomentReleaseMtNonlinearity]
        MOMENT_RELEASE_MT_NONLINEARITY_FAILURE_ALL_IF_POSITIVE: _ClassVar[NodalReleaseType.MomentReleaseMtNonlinearity]
        MOMENT_RELEASE_MT_NONLINEARITY_FAILURE_IF_NEGATIVE: _ClassVar[NodalReleaseType.MomentReleaseMtNonlinearity]
        MOMENT_RELEASE_MT_NONLINEARITY_FAILURE_IF_POSITIVE: _ClassVar[NodalReleaseType.MomentReleaseMtNonlinearity]
        MOMENT_RELEASE_MT_NONLINEARITY_FORCE_MOMENT_DIAGRAM: _ClassVar[NodalReleaseType.MomentReleaseMtNonlinearity]
        MOMENT_RELEASE_MT_NONLINEARITY_FRICTION_DIRECTION_1: _ClassVar[NodalReleaseType.MomentReleaseMtNonlinearity]
        MOMENT_RELEASE_MT_NONLINEARITY_FRICTION_DIRECTION_1_2: _ClassVar[NodalReleaseType.MomentReleaseMtNonlinearity]
        MOMENT_RELEASE_MT_NONLINEARITY_FRICTION_DIRECTION_1_PLUS_2: _ClassVar[NodalReleaseType.MomentReleaseMtNonlinearity]
        MOMENT_RELEASE_MT_NONLINEARITY_FRICTION_DIRECTION_2: _ClassVar[NodalReleaseType.MomentReleaseMtNonlinearity]
        MOMENT_RELEASE_MT_NONLINEARITY_PARTIAL_ACTIVITY: _ClassVar[NodalReleaseType.MomentReleaseMtNonlinearity]
        MOMENT_RELEASE_MT_NONLINEARITY_STIFFNESS_DIAGRAM: _ClassVar[NodalReleaseType.MomentReleaseMtNonlinearity]
    MOMENT_RELEASE_MT_NONLINEARITY_NONE: NodalReleaseType.MomentReleaseMtNonlinearity
    MOMENT_RELEASE_MT_NONLINEARITY_DIAGRAM: NodalReleaseType.MomentReleaseMtNonlinearity
    MOMENT_RELEASE_MT_NONLINEARITY_FAILURE_ALL_IF_NEGATIVE: NodalReleaseType.MomentReleaseMtNonlinearity
    MOMENT_RELEASE_MT_NONLINEARITY_FAILURE_ALL_IF_POSITIVE: NodalReleaseType.MomentReleaseMtNonlinearity
    MOMENT_RELEASE_MT_NONLINEARITY_FAILURE_IF_NEGATIVE: NodalReleaseType.MomentReleaseMtNonlinearity
    MOMENT_RELEASE_MT_NONLINEARITY_FAILURE_IF_POSITIVE: NodalReleaseType.MomentReleaseMtNonlinearity
    MOMENT_RELEASE_MT_NONLINEARITY_FORCE_MOMENT_DIAGRAM: NodalReleaseType.MomentReleaseMtNonlinearity
    MOMENT_RELEASE_MT_NONLINEARITY_FRICTION_DIRECTION_1: NodalReleaseType.MomentReleaseMtNonlinearity
    MOMENT_RELEASE_MT_NONLINEARITY_FRICTION_DIRECTION_1_2: NodalReleaseType.MomentReleaseMtNonlinearity
    MOMENT_RELEASE_MT_NONLINEARITY_FRICTION_DIRECTION_1_PLUS_2: NodalReleaseType.MomentReleaseMtNonlinearity
    MOMENT_RELEASE_MT_NONLINEARITY_FRICTION_DIRECTION_2: NodalReleaseType.MomentReleaseMtNonlinearity
    MOMENT_RELEASE_MT_NONLINEARITY_PARTIAL_ACTIVITY: NodalReleaseType.MomentReleaseMtNonlinearity
    MOMENT_RELEASE_MT_NONLINEARITY_STIFFNESS_DIAGRAM: NodalReleaseType.MomentReleaseMtNonlinearity
    class MomentReleaseMyNonlinearity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        MOMENT_RELEASE_MY_NONLINEARITY_NONE: _ClassVar[NodalReleaseType.MomentReleaseMyNonlinearity]
        MOMENT_RELEASE_MY_NONLINEARITY_DIAGRAM: _ClassVar[NodalReleaseType.MomentReleaseMyNonlinearity]
        MOMENT_RELEASE_MY_NONLINEARITY_FAILURE_ALL_IF_NEGATIVE: _ClassVar[NodalReleaseType.MomentReleaseMyNonlinearity]
        MOMENT_RELEASE_MY_NONLINEARITY_FAILURE_ALL_IF_POSITIVE: _ClassVar[NodalReleaseType.MomentReleaseMyNonlinearity]
        MOMENT_RELEASE_MY_NONLINEARITY_FAILURE_IF_NEGATIVE: _ClassVar[NodalReleaseType.MomentReleaseMyNonlinearity]
        MOMENT_RELEASE_MY_NONLINEARITY_FAILURE_IF_POSITIVE: _ClassVar[NodalReleaseType.MomentReleaseMyNonlinearity]
        MOMENT_RELEASE_MY_NONLINEARITY_FORCE_MOMENT_DIAGRAM: _ClassVar[NodalReleaseType.MomentReleaseMyNonlinearity]
        MOMENT_RELEASE_MY_NONLINEARITY_FRICTION_DIRECTION_1: _ClassVar[NodalReleaseType.MomentReleaseMyNonlinearity]
        MOMENT_RELEASE_MY_NONLINEARITY_FRICTION_DIRECTION_1_2: _ClassVar[NodalReleaseType.MomentReleaseMyNonlinearity]
        MOMENT_RELEASE_MY_NONLINEARITY_FRICTION_DIRECTION_1_PLUS_2: _ClassVar[NodalReleaseType.MomentReleaseMyNonlinearity]
        MOMENT_RELEASE_MY_NONLINEARITY_FRICTION_DIRECTION_2: _ClassVar[NodalReleaseType.MomentReleaseMyNonlinearity]
        MOMENT_RELEASE_MY_NONLINEARITY_PARTIAL_ACTIVITY: _ClassVar[NodalReleaseType.MomentReleaseMyNonlinearity]
        MOMENT_RELEASE_MY_NONLINEARITY_STIFFNESS_DIAGRAM: _ClassVar[NodalReleaseType.MomentReleaseMyNonlinearity]
    MOMENT_RELEASE_MY_NONLINEARITY_NONE: NodalReleaseType.MomentReleaseMyNonlinearity
    MOMENT_RELEASE_MY_NONLINEARITY_DIAGRAM: NodalReleaseType.MomentReleaseMyNonlinearity
    MOMENT_RELEASE_MY_NONLINEARITY_FAILURE_ALL_IF_NEGATIVE: NodalReleaseType.MomentReleaseMyNonlinearity
    MOMENT_RELEASE_MY_NONLINEARITY_FAILURE_ALL_IF_POSITIVE: NodalReleaseType.MomentReleaseMyNonlinearity
    MOMENT_RELEASE_MY_NONLINEARITY_FAILURE_IF_NEGATIVE: NodalReleaseType.MomentReleaseMyNonlinearity
    MOMENT_RELEASE_MY_NONLINEARITY_FAILURE_IF_POSITIVE: NodalReleaseType.MomentReleaseMyNonlinearity
    MOMENT_RELEASE_MY_NONLINEARITY_FORCE_MOMENT_DIAGRAM: NodalReleaseType.MomentReleaseMyNonlinearity
    MOMENT_RELEASE_MY_NONLINEARITY_FRICTION_DIRECTION_1: NodalReleaseType.MomentReleaseMyNonlinearity
    MOMENT_RELEASE_MY_NONLINEARITY_FRICTION_DIRECTION_1_2: NodalReleaseType.MomentReleaseMyNonlinearity
    MOMENT_RELEASE_MY_NONLINEARITY_FRICTION_DIRECTION_1_PLUS_2: NodalReleaseType.MomentReleaseMyNonlinearity
    MOMENT_RELEASE_MY_NONLINEARITY_FRICTION_DIRECTION_2: NodalReleaseType.MomentReleaseMyNonlinearity
    MOMENT_RELEASE_MY_NONLINEARITY_PARTIAL_ACTIVITY: NodalReleaseType.MomentReleaseMyNonlinearity
    MOMENT_RELEASE_MY_NONLINEARITY_STIFFNESS_DIAGRAM: NodalReleaseType.MomentReleaseMyNonlinearity
    class MomentReleaseMzNonlinearity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        MOMENT_RELEASE_MZ_NONLINEARITY_NONE: _ClassVar[NodalReleaseType.MomentReleaseMzNonlinearity]
        MOMENT_RELEASE_MZ_NONLINEARITY_DIAGRAM: _ClassVar[NodalReleaseType.MomentReleaseMzNonlinearity]
        MOMENT_RELEASE_MZ_NONLINEARITY_FAILURE_ALL_IF_NEGATIVE: _ClassVar[NodalReleaseType.MomentReleaseMzNonlinearity]
        MOMENT_RELEASE_MZ_NONLINEARITY_FAILURE_ALL_IF_POSITIVE: _ClassVar[NodalReleaseType.MomentReleaseMzNonlinearity]
        MOMENT_RELEASE_MZ_NONLINEARITY_FAILURE_IF_NEGATIVE: _ClassVar[NodalReleaseType.MomentReleaseMzNonlinearity]
        MOMENT_RELEASE_MZ_NONLINEARITY_FAILURE_IF_POSITIVE: _ClassVar[NodalReleaseType.MomentReleaseMzNonlinearity]
        MOMENT_RELEASE_MZ_NONLINEARITY_FORCE_MOMENT_DIAGRAM: _ClassVar[NodalReleaseType.MomentReleaseMzNonlinearity]
        MOMENT_RELEASE_MZ_NONLINEARITY_FRICTION_DIRECTION_1: _ClassVar[NodalReleaseType.MomentReleaseMzNonlinearity]
        MOMENT_RELEASE_MZ_NONLINEARITY_FRICTION_DIRECTION_1_2: _ClassVar[NodalReleaseType.MomentReleaseMzNonlinearity]
        MOMENT_RELEASE_MZ_NONLINEARITY_FRICTION_DIRECTION_1_PLUS_2: _ClassVar[NodalReleaseType.MomentReleaseMzNonlinearity]
        MOMENT_RELEASE_MZ_NONLINEARITY_FRICTION_DIRECTION_2: _ClassVar[NodalReleaseType.MomentReleaseMzNonlinearity]
        MOMENT_RELEASE_MZ_NONLINEARITY_PARTIAL_ACTIVITY: _ClassVar[NodalReleaseType.MomentReleaseMzNonlinearity]
        MOMENT_RELEASE_MZ_NONLINEARITY_STIFFNESS_DIAGRAM: _ClassVar[NodalReleaseType.MomentReleaseMzNonlinearity]
    MOMENT_RELEASE_MZ_NONLINEARITY_NONE: NodalReleaseType.MomentReleaseMzNonlinearity
    MOMENT_RELEASE_MZ_NONLINEARITY_DIAGRAM: NodalReleaseType.MomentReleaseMzNonlinearity
    MOMENT_RELEASE_MZ_NONLINEARITY_FAILURE_ALL_IF_NEGATIVE: NodalReleaseType.MomentReleaseMzNonlinearity
    MOMENT_RELEASE_MZ_NONLINEARITY_FAILURE_ALL_IF_POSITIVE: NodalReleaseType.MomentReleaseMzNonlinearity
    MOMENT_RELEASE_MZ_NONLINEARITY_FAILURE_IF_NEGATIVE: NodalReleaseType.MomentReleaseMzNonlinearity
    MOMENT_RELEASE_MZ_NONLINEARITY_FAILURE_IF_POSITIVE: NodalReleaseType.MomentReleaseMzNonlinearity
    MOMENT_RELEASE_MZ_NONLINEARITY_FORCE_MOMENT_DIAGRAM: NodalReleaseType.MomentReleaseMzNonlinearity
    MOMENT_RELEASE_MZ_NONLINEARITY_FRICTION_DIRECTION_1: NodalReleaseType.MomentReleaseMzNonlinearity
    MOMENT_RELEASE_MZ_NONLINEARITY_FRICTION_DIRECTION_1_2: NodalReleaseType.MomentReleaseMzNonlinearity
    MOMENT_RELEASE_MZ_NONLINEARITY_FRICTION_DIRECTION_1_PLUS_2: NodalReleaseType.MomentReleaseMzNonlinearity
    MOMENT_RELEASE_MZ_NONLINEARITY_FRICTION_DIRECTION_2: NodalReleaseType.MomentReleaseMzNonlinearity
    MOMENT_RELEASE_MZ_NONLINEARITY_PARTIAL_ACTIVITY: NodalReleaseType.MomentReleaseMzNonlinearity
    MOMENT_RELEASE_MZ_NONLINEARITY_STIFFNESS_DIAGRAM: NodalReleaseType.MomentReleaseMzNonlinearity
    class PartialActivityAlongXNegativeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PARTIAL_ACTIVITY_ALONG_X_NEGATIVE_TYPE_COMPLETE: _ClassVar[NodalReleaseType.PartialActivityAlongXNegativeType]
        PARTIAL_ACTIVITY_ALONG_X_NEGATIVE_TYPE_FAILURE: _ClassVar[NodalReleaseType.PartialActivityAlongXNegativeType]
        PARTIAL_ACTIVITY_ALONG_X_NEGATIVE_TYPE_FAILURE_FROM_FORCE_OR_MOMENT: _ClassVar[NodalReleaseType.PartialActivityAlongXNegativeType]
        PARTIAL_ACTIVITY_ALONG_X_NEGATIVE_TYPE_FIXED: _ClassVar[NodalReleaseType.PartialActivityAlongXNegativeType]
        PARTIAL_ACTIVITY_ALONG_X_NEGATIVE_TYPE_YIELDING_FROM_FORCE_OR_MOMENT: _ClassVar[NodalReleaseType.PartialActivityAlongXNegativeType]
    PARTIAL_ACTIVITY_ALONG_X_NEGATIVE_TYPE_COMPLETE: NodalReleaseType.PartialActivityAlongXNegativeType
    PARTIAL_ACTIVITY_ALONG_X_NEGATIVE_TYPE_FAILURE: NodalReleaseType.PartialActivityAlongXNegativeType
    PARTIAL_ACTIVITY_ALONG_X_NEGATIVE_TYPE_FAILURE_FROM_FORCE_OR_MOMENT: NodalReleaseType.PartialActivityAlongXNegativeType
    PARTIAL_ACTIVITY_ALONG_X_NEGATIVE_TYPE_FIXED: NodalReleaseType.PartialActivityAlongXNegativeType
    PARTIAL_ACTIVITY_ALONG_X_NEGATIVE_TYPE_YIELDING_FROM_FORCE_OR_MOMENT: NodalReleaseType.PartialActivityAlongXNegativeType
    class PartialActivityAlongXPositiveType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PARTIAL_ACTIVITY_ALONG_X_POSITIVE_TYPE_COMPLETE: _ClassVar[NodalReleaseType.PartialActivityAlongXPositiveType]
        PARTIAL_ACTIVITY_ALONG_X_POSITIVE_TYPE_FAILURE: _ClassVar[NodalReleaseType.PartialActivityAlongXPositiveType]
        PARTIAL_ACTIVITY_ALONG_X_POSITIVE_TYPE_FAILURE_FROM_FORCE_OR_MOMENT: _ClassVar[NodalReleaseType.PartialActivityAlongXPositiveType]
        PARTIAL_ACTIVITY_ALONG_X_POSITIVE_TYPE_FIXED: _ClassVar[NodalReleaseType.PartialActivityAlongXPositiveType]
        PARTIAL_ACTIVITY_ALONG_X_POSITIVE_TYPE_YIELDING_FROM_FORCE_OR_MOMENT: _ClassVar[NodalReleaseType.PartialActivityAlongXPositiveType]
    PARTIAL_ACTIVITY_ALONG_X_POSITIVE_TYPE_COMPLETE: NodalReleaseType.PartialActivityAlongXPositiveType
    PARTIAL_ACTIVITY_ALONG_X_POSITIVE_TYPE_FAILURE: NodalReleaseType.PartialActivityAlongXPositiveType
    PARTIAL_ACTIVITY_ALONG_X_POSITIVE_TYPE_FAILURE_FROM_FORCE_OR_MOMENT: NodalReleaseType.PartialActivityAlongXPositiveType
    PARTIAL_ACTIVITY_ALONG_X_POSITIVE_TYPE_FIXED: NodalReleaseType.PartialActivityAlongXPositiveType
    PARTIAL_ACTIVITY_ALONG_X_POSITIVE_TYPE_YIELDING_FROM_FORCE_OR_MOMENT: NodalReleaseType.PartialActivityAlongXPositiveType
    class PartialActivityAlongYNegativeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PARTIAL_ACTIVITY_ALONG_Y_NEGATIVE_TYPE_COMPLETE: _ClassVar[NodalReleaseType.PartialActivityAlongYNegativeType]
        PARTIAL_ACTIVITY_ALONG_Y_NEGATIVE_TYPE_FAILURE: _ClassVar[NodalReleaseType.PartialActivityAlongYNegativeType]
        PARTIAL_ACTIVITY_ALONG_Y_NEGATIVE_TYPE_FAILURE_FROM_FORCE_OR_MOMENT: _ClassVar[NodalReleaseType.PartialActivityAlongYNegativeType]
        PARTIAL_ACTIVITY_ALONG_Y_NEGATIVE_TYPE_FIXED: _ClassVar[NodalReleaseType.PartialActivityAlongYNegativeType]
        PARTIAL_ACTIVITY_ALONG_Y_NEGATIVE_TYPE_YIELDING_FROM_FORCE_OR_MOMENT: _ClassVar[NodalReleaseType.PartialActivityAlongYNegativeType]
    PARTIAL_ACTIVITY_ALONG_Y_NEGATIVE_TYPE_COMPLETE: NodalReleaseType.PartialActivityAlongYNegativeType
    PARTIAL_ACTIVITY_ALONG_Y_NEGATIVE_TYPE_FAILURE: NodalReleaseType.PartialActivityAlongYNegativeType
    PARTIAL_ACTIVITY_ALONG_Y_NEGATIVE_TYPE_FAILURE_FROM_FORCE_OR_MOMENT: NodalReleaseType.PartialActivityAlongYNegativeType
    PARTIAL_ACTIVITY_ALONG_Y_NEGATIVE_TYPE_FIXED: NodalReleaseType.PartialActivityAlongYNegativeType
    PARTIAL_ACTIVITY_ALONG_Y_NEGATIVE_TYPE_YIELDING_FROM_FORCE_OR_MOMENT: NodalReleaseType.PartialActivityAlongYNegativeType
    class PartialActivityAlongYPositiveType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PARTIAL_ACTIVITY_ALONG_Y_POSITIVE_TYPE_COMPLETE: _ClassVar[NodalReleaseType.PartialActivityAlongYPositiveType]
        PARTIAL_ACTIVITY_ALONG_Y_POSITIVE_TYPE_FAILURE: _ClassVar[NodalReleaseType.PartialActivityAlongYPositiveType]
        PARTIAL_ACTIVITY_ALONG_Y_POSITIVE_TYPE_FAILURE_FROM_FORCE_OR_MOMENT: _ClassVar[NodalReleaseType.PartialActivityAlongYPositiveType]
        PARTIAL_ACTIVITY_ALONG_Y_POSITIVE_TYPE_FIXED: _ClassVar[NodalReleaseType.PartialActivityAlongYPositiveType]
        PARTIAL_ACTIVITY_ALONG_Y_POSITIVE_TYPE_YIELDING_FROM_FORCE_OR_MOMENT: _ClassVar[NodalReleaseType.PartialActivityAlongYPositiveType]
    PARTIAL_ACTIVITY_ALONG_Y_POSITIVE_TYPE_COMPLETE: NodalReleaseType.PartialActivityAlongYPositiveType
    PARTIAL_ACTIVITY_ALONG_Y_POSITIVE_TYPE_FAILURE: NodalReleaseType.PartialActivityAlongYPositiveType
    PARTIAL_ACTIVITY_ALONG_Y_POSITIVE_TYPE_FAILURE_FROM_FORCE_OR_MOMENT: NodalReleaseType.PartialActivityAlongYPositiveType
    PARTIAL_ACTIVITY_ALONG_Y_POSITIVE_TYPE_FIXED: NodalReleaseType.PartialActivityAlongYPositiveType
    PARTIAL_ACTIVITY_ALONG_Y_POSITIVE_TYPE_YIELDING_FROM_FORCE_OR_MOMENT: NodalReleaseType.PartialActivityAlongYPositiveType
    class PartialActivityAlongZNegativeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PARTIAL_ACTIVITY_ALONG_Z_NEGATIVE_TYPE_COMPLETE: _ClassVar[NodalReleaseType.PartialActivityAlongZNegativeType]
        PARTIAL_ACTIVITY_ALONG_Z_NEGATIVE_TYPE_FAILURE: _ClassVar[NodalReleaseType.PartialActivityAlongZNegativeType]
        PARTIAL_ACTIVITY_ALONG_Z_NEGATIVE_TYPE_FAILURE_FROM_FORCE_OR_MOMENT: _ClassVar[NodalReleaseType.PartialActivityAlongZNegativeType]
        PARTIAL_ACTIVITY_ALONG_Z_NEGATIVE_TYPE_FIXED: _ClassVar[NodalReleaseType.PartialActivityAlongZNegativeType]
        PARTIAL_ACTIVITY_ALONG_Z_NEGATIVE_TYPE_YIELDING_FROM_FORCE_OR_MOMENT: _ClassVar[NodalReleaseType.PartialActivityAlongZNegativeType]
    PARTIAL_ACTIVITY_ALONG_Z_NEGATIVE_TYPE_COMPLETE: NodalReleaseType.PartialActivityAlongZNegativeType
    PARTIAL_ACTIVITY_ALONG_Z_NEGATIVE_TYPE_FAILURE: NodalReleaseType.PartialActivityAlongZNegativeType
    PARTIAL_ACTIVITY_ALONG_Z_NEGATIVE_TYPE_FAILURE_FROM_FORCE_OR_MOMENT: NodalReleaseType.PartialActivityAlongZNegativeType
    PARTIAL_ACTIVITY_ALONG_Z_NEGATIVE_TYPE_FIXED: NodalReleaseType.PartialActivityAlongZNegativeType
    PARTIAL_ACTIVITY_ALONG_Z_NEGATIVE_TYPE_YIELDING_FROM_FORCE_OR_MOMENT: NodalReleaseType.PartialActivityAlongZNegativeType
    class PartialActivityAlongZPositiveType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PARTIAL_ACTIVITY_ALONG_Z_POSITIVE_TYPE_COMPLETE: _ClassVar[NodalReleaseType.PartialActivityAlongZPositiveType]
        PARTIAL_ACTIVITY_ALONG_Z_POSITIVE_TYPE_FAILURE: _ClassVar[NodalReleaseType.PartialActivityAlongZPositiveType]
        PARTIAL_ACTIVITY_ALONG_Z_POSITIVE_TYPE_FAILURE_FROM_FORCE_OR_MOMENT: _ClassVar[NodalReleaseType.PartialActivityAlongZPositiveType]
        PARTIAL_ACTIVITY_ALONG_Z_POSITIVE_TYPE_FIXED: _ClassVar[NodalReleaseType.PartialActivityAlongZPositiveType]
        PARTIAL_ACTIVITY_ALONG_Z_POSITIVE_TYPE_YIELDING_FROM_FORCE_OR_MOMENT: _ClassVar[NodalReleaseType.PartialActivityAlongZPositiveType]
    PARTIAL_ACTIVITY_ALONG_Z_POSITIVE_TYPE_COMPLETE: NodalReleaseType.PartialActivityAlongZPositiveType
    PARTIAL_ACTIVITY_ALONG_Z_POSITIVE_TYPE_FAILURE: NodalReleaseType.PartialActivityAlongZPositiveType
    PARTIAL_ACTIVITY_ALONG_Z_POSITIVE_TYPE_FAILURE_FROM_FORCE_OR_MOMENT: NodalReleaseType.PartialActivityAlongZPositiveType
    PARTIAL_ACTIVITY_ALONG_Z_POSITIVE_TYPE_FIXED: NodalReleaseType.PartialActivityAlongZPositiveType
    PARTIAL_ACTIVITY_ALONG_Z_POSITIVE_TYPE_YIELDING_FROM_FORCE_OR_MOMENT: NodalReleaseType.PartialActivityAlongZPositiveType
    class PartialActivityAroundXNegativeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PARTIAL_ACTIVITY_AROUND_X_NEGATIVE_TYPE_COMPLETE: _ClassVar[NodalReleaseType.PartialActivityAroundXNegativeType]
        PARTIAL_ACTIVITY_AROUND_X_NEGATIVE_TYPE_FAILURE: _ClassVar[NodalReleaseType.PartialActivityAroundXNegativeType]
        PARTIAL_ACTIVITY_AROUND_X_NEGATIVE_TYPE_FAILURE_FROM_FORCE_OR_MOMENT: _ClassVar[NodalReleaseType.PartialActivityAroundXNegativeType]
        PARTIAL_ACTIVITY_AROUND_X_NEGATIVE_TYPE_FIXED: _ClassVar[NodalReleaseType.PartialActivityAroundXNegativeType]
        PARTIAL_ACTIVITY_AROUND_X_NEGATIVE_TYPE_YIELDING_FROM_FORCE_OR_MOMENT: _ClassVar[NodalReleaseType.PartialActivityAroundXNegativeType]
    PARTIAL_ACTIVITY_AROUND_X_NEGATIVE_TYPE_COMPLETE: NodalReleaseType.PartialActivityAroundXNegativeType
    PARTIAL_ACTIVITY_AROUND_X_NEGATIVE_TYPE_FAILURE: NodalReleaseType.PartialActivityAroundXNegativeType
    PARTIAL_ACTIVITY_AROUND_X_NEGATIVE_TYPE_FAILURE_FROM_FORCE_OR_MOMENT: NodalReleaseType.PartialActivityAroundXNegativeType
    PARTIAL_ACTIVITY_AROUND_X_NEGATIVE_TYPE_FIXED: NodalReleaseType.PartialActivityAroundXNegativeType
    PARTIAL_ACTIVITY_AROUND_X_NEGATIVE_TYPE_YIELDING_FROM_FORCE_OR_MOMENT: NodalReleaseType.PartialActivityAroundXNegativeType
    class PartialActivityAroundXPositiveType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PARTIAL_ACTIVITY_AROUND_X_POSITIVE_TYPE_COMPLETE: _ClassVar[NodalReleaseType.PartialActivityAroundXPositiveType]
        PARTIAL_ACTIVITY_AROUND_X_POSITIVE_TYPE_FAILURE: _ClassVar[NodalReleaseType.PartialActivityAroundXPositiveType]
        PARTIAL_ACTIVITY_AROUND_X_POSITIVE_TYPE_FAILURE_FROM_FORCE_OR_MOMENT: _ClassVar[NodalReleaseType.PartialActivityAroundXPositiveType]
        PARTIAL_ACTIVITY_AROUND_X_POSITIVE_TYPE_FIXED: _ClassVar[NodalReleaseType.PartialActivityAroundXPositiveType]
        PARTIAL_ACTIVITY_AROUND_X_POSITIVE_TYPE_YIELDING_FROM_FORCE_OR_MOMENT: _ClassVar[NodalReleaseType.PartialActivityAroundXPositiveType]
    PARTIAL_ACTIVITY_AROUND_X_POSITIVE_TYPE_COMPLETE: NodalReleaseType.PartialActivityAroundXPositiveType
    PARTIAL_ACTIVITY_AROUND_X_POSITIVE_TYPE_FAILURE: NodalReleaseType.PartialActivityAroundXPositiveType
    PARTIAL_ACTIVITY_AROUND_X_POSITIVE_TYPE_FAILURE_FROM_FORCE_OR_MOMENT: NodalReleaseType.PartialActivityAroundXPositiveType
    PARTIAL_ACTIVITY_AROUND_X_POSITIVE_TYPE_FIXED: NodalReleaseType.PartialActivityAroundXPositiveType
    PARTIAL_ACTIVITY_AROUND_X_POSITIVE_TYPE_YIELDING_FROM_FORCE_OR_MOMENT: NodalReleaseType.PartialActivityAroundXPositiveType
    class PartialActivityAroundYNegativeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PARTIAL_ACTIVITY_AROUND_Y_NEGATIVE_TYPE_COMPLETE: _ClassVar[NodalReleaseType.PartialActivityAroundYNegativeType]
        PARTIAL_ACTIVITY_AROUND_Y_NEGATIVE_TYPE_FAILURE: _ClassVar[NodalReleaseType.PartialActivityAroundYNegativeType]
        PARTIAL_ACTIVITY_AROUND_Y_NEGATIVE_TYPE_FAILURE_FROM_FORCE_OR_MOMENT: _ClassVar[NodalReleaseType.PartialActivityAroundYNegativeType]
        PARTIAL_ACTIVITY_AROUND_Y_NEGATIVE_TYPE_FIXED: _ClassVar[NodalReleaseType.PartialActivityAroundYNegativeType]
        PARTIAL_ACTIVITY_AROUND_Y_NEGATIVE_TYPE_YIELDING_FROM_FORCE_OR_MOMENT: _ClassVar[NodalReleaseType.PartialActivityAroundYNegativeType]
    PARTIAL_ACTIVITY_AROUND_Y_NEGATIVE_TYPE_COMPLETE: NodalReleaseType.PartialActivityAroundYNegativeType
    PARTIAL_ACTIVITY_AROUND_Y_NEGATIVE_TYPE_FAILURE: NodalReleaseType.PartialActivityAroundYNegativeType
    PARTIAL_ACTIVITY_AROUND_Y_NEGATIVE_TYPE_FAILURE_FROM_FORCE_OR_MOMENT: NodalReleaseType.PartialActivityAroundYNegativeType
    PARTIAL_ACTIVITY_AROUND_Y_NEGATIVE_TYPE_FIXED: NodalReleaseType.PartialActivityAroundYNegativeType
    PARTIAL_ACTIVITY_AROUND_Y_NEGATIVE_TYPE_YIELDING_FROM_FORCE_OR_MOMENT: NodalReleaseType.PartialActivityAroundYNegativeType
    class PartialActivityAroundYPositiveType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PARTIAL_ACTIVITY_AROUND_Y_POSITIVE_TYPE_COMPLETE: _ClassVar[NodalReleaseType.PartialActivityAroundYPositiveType]
        PARTIAL_ACTIVITY_AROUND_Y_POSITIVE_TYPE_FAILURE: _ClassVar[NodalReleaseType.PartialActivityAroundYPositiveType]
        PARTIAL_ACTIVITY_AROUND_Y_POSITIVE_TYPE_FAILURE_FROM_FORCE_OR_MOMENT: _ClassVar[NodalReleaseType.PartialActivityAroundYPositiveType]
        PARTIAL_ACTIVITY_AROUND_Y_POSITIVE_TYPE_FIXED: _ClassVar[NodalReleaseType.PartialActivityAroundYPositiveType]
        PARTIAL_ACTIVITY_AROUND_Y_POSITIVE_TYPE_YIELDING_FROM_FORCE_OR_MOMENT: _ClassVar[NodalReleaseType.PartialActivityAroundYPositiveType]
    PARTIAL_ACTIVITY_AROUND_Y_POSITIVE_TYPE_COMPLETE: NodalReleaseType.PartialActivityAroundYPositiveType
    PARTIAL_ACTIVITY_AROUND_Y_POSITIVE_TYPE_FAILURE: NodalReleaseType.PartialActivityAroundYPositiveType
    PARTIAL_ACTIVITY_AROUND_Y_POSITIVE_TYPE_FAILURE_FROM_FORCE_OR_MOMENT: NodalReleaseType.PartialActivityAroundYPositiveType
    PARTIAL_ACTIVITY_AROUND_Y_POSITIVE_TYPE_FIXED: NodalReleaseType.PartialActivityAroundYPositiveType
    PARTIAL_ACTIVITY_AROUND_Y_POSITIVE_TYPE_YIELDING_FROM_FORCE_OR_MOMENT: NodalReleaseType.PartialActivityAroundYPositiveType
    class PartialActivityAroundZNegativeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PARTIAL_ACTIVITY_AROUND_Z_NEGATIVE_TYPE_COMPLETE: _ClassVar[NodalReleaseType.PartialActivityAroundZNegativeType]
        PARTIAL_ACTIVITY_AROUND_Z_NEGATIVE_TYPE_FAILURE: _ClassVar[NodalReleaseType.PartialActivityAroundZNegativeType]
        PARTIAL_ACTIVITY_AROUND_Z_NEGATIVE_TYPE_FAILURE_FROM_FORCE_OR_MOMENT: _ClassVar[NodalReleaseType.PartialActivityAroundZNegativeType]
        PARTIAL_ACTIVITY_AROUND_Z_NEGATIVE_TYPE_FIXED: _ClassVar[NodalReleaseType.PartialActivityAroundZNegativeType]
        PARTIAL_ACTIVITY_AROUND_Z_NEGATIVE_TYPE_YIELDING_FROM_FORCE_OR_MOMENT: _ClassVar[NodalReleaseType.PartialActivityAroundZNegativeType]
    PARTIAL_ACTIVITY_AROUND_Z_NEGATIVE_TYPE_COMPLETE: NodalReleaseType.PartialActivityAroundZNegativeType
    PARTIAL_ACTIVITY_AROUND_Z_NEGATIVE_TYPE_FAILURE: NodalReleaseType.PartialActivityAroundZNegativeType
    PARTIAL_ACTIVITY_AROUND_Z_NEGATIVE_TYPE_FAILURE_FROM_FORCE_OR_MOMENT: NodalReleaseType.PartialActivityAroundZNegativeType
    PARTIAL_ACTIVITY_AROUND_Z_NEGATIVE_TYPE_FIXED: NodalReleaseType.PartialActivityAroundZNegativeType
    PARTIAL_ACTIVITY_AROUND_Z_NEGATIVE_TYPE_YIELDING_FROM_FORCE_OR_MOMENT: NodalReleaseType.PartialActivityAroundZNegativeType
    class PartialActivityAroundZPositiveType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PARTIAL_ACTIVITY_AROUND_Z_POSITIVE_TYPE_COMPLETE: _ClassVar[NodalReleaseType.PartialActivityAroundZPositiveType]
        PARTIAL_ACTIVITY_AROUND_Z_POSITIVE_TYPE_FAILURE: _ClassVar[NodalReleaseType.PartialActivityAroundZPositiveType]
        PARTIAL_ACTIVITY_AROUND_Z_POSITIVE_TYPE_FAILURE_FROM_FORCE_OR_MOMENT: _ClassVar[NodalReleaseType.PartialActivityAroundZPositiveType]
        PARTIAL_ACTIVITY_AROUND_Z_POSITIVE_TYPE_FIXED: _ClassVar[NodalReleaseType.PartialActivityAroundZPositiveType]
        PARTIAL_ACTIVITY_AROUND_Z_POSITIVE_TYPE_YIELDING_FROM_FORCE_OR_MOMENT: _ClassVar[NodalReleaseType.PartialActivityAroundZPositiveType]
    PARTIAL_ACTIVITY_AROUND_Z_POSITIVE_TYPE_COMPLETE: NodalReleaseType.PartialActivityAroundZPositiveType
    PARTIAL_ACTIVITY_AROUND_Z_POSITIVE_TYPE_FAILURE: NodalReleaseType.PartialActivityAroundZPositiveType
    PARTIAL_ACTIVITY_AROUND_Z_POSITIVE_TYPE_FAILURE_FROM_FORCE_OR_MOMENT: NodalReleaseType.PartialActivityAroundZPositiveType
    PARTIAL_ACTIVITY_AROUND_Z_POSITIVE_TYPE_FIXED: NodalReleaseType.PartialActivityAroundZPositiveType
    PARTIAL_ACTIVITY_AROUND_Z_POSITIVE_TYPE_YIELDING_FROM_FORCE_OR_MOMENT: NodalReleaseType.PartialActivityAroundZPositiveType
    class DiagramAlongXStart(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DIAGRAM_ALONG_X_START_FAILURE: _ClassVar[NodalReleaseType.DiagramAlongXStart]
        DIAGRAM_ALONG_X_START_CONTINUOUS: _ClassVar[NodalReleaseType.DiagramAlongXStart]
        DIAGRAM_ALONG_X_START_STOP: _ClassVar[NodalReleaseType.DiagramAlongXStart]
        DIAGRAM_ALONG_X_START_YIELDING: _ClassVar[NodalReleaseType.DiagramAlongXStart]
    DIAGRAM_ALONG_X_START_FAILURE: NodalReleaseType.DiagramAlongXStart
    DIAGRAM_ALONG_X_START_CONTINUOUS: NodalReleaseType.DiagramAlongXStart
    DIAGRAM_ALONG_X_START_STOP: NodalReleaseType.DiagramAlongXStart
    DIAGRAM_ALONG_X_START_YIELDING: NodalReleaseType.DiagramAlongXStart
    class DiagramAlongYStart(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DIAGRAM_ALONG_Y_START_FAILURE: _ClassVar[NodalReleaseType.DiagramAlongYStart]
        DIAGRAM_ALONG_Y_START_CONTINUOUS: _ClassVar[NodalReleaseType.DiagramAlongYStart]
        DIAGRAM_ALONG_Y_START_STOP: _ClassVar[NodalReleaseType.DiagramAlongYStart]
        DIAGRAM_ALONG_Y_START_YIELDING: _ClassVar[NodalReleaseType.DiagramAlongYStart]
    DIAGRAM_ALONG_Y_START_FAILURE: NodalReleaseType.DiagramAlongYStart
    DIAGRAM_ALONG_Y_START_CONTINUOUS: NodalReleaseType.DiagramAlongYStart
    DIAGRAM_ALONG_Y_START_STOP: NodalReleaseType.DiagramAlongYStart
    DIAGRAM_ALONG_Y_START_YIELDING: NodalReleaseType.DiagramAlongYStart
    class DiagramAlongZStart(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DIAGRAM_ALONG_Z_START_FAILURE: _ClassVar[NodalReleaseType.DiagramAlongZStart]
        DIAGRAM_ALONG_Z_START_CONTINUOUS: _ClassVar[NodalReleaseType.DiagramAlongZStart]
        DIAGRAM_ALONG_Z_START_STOP: _ClassVar[NodalReleaseType.DiagramAlongZStart]
        DIAGRAM_ALONG_Z_START_YIELDING: _ClassVar[NodalReleaseType.DiagramAlongZStart]
    DIAGRAM_ALONG_Z_START_FAILURE: NodalReleaseType.DiagramAlongZStart
    DIAGRAM_ALONG_Z_START_CONTINUOUS: NodalReleaseType.DiagramAlongZStart
    DIAGRAM_ALONG_Z_START_STOP: NodalReleaseType.DiagramAlongZStart
    DIAGRAM_ALONG_Z_START_YIELDING: NodalReleaseType.DiagramAlongZStart
    class DiagramAroundXStart(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DIAGRAM_AROUND_X_START_FAILURE: _ClassVar[NodalReleaseType.DiagramAroundXStart]
        DIAGRAM_AROUND_X_START_CONTINUOUS: _ClassVar[NodalReleaseType.DiagramAroundXStart]
        DIAGRAM_AROUND_X_START_STOP: _ClassVar[NodalReleaseType.DiagramAroundXStart]
        DIAGRAM_AROUND_X_START_YIELDING: _ClassVar[NodalReleaseType.DiagramAroundXStart]
    DIAGRAM_AROUND_X_START_FAILURE: NodalReleaseType.DiagramAroundXStart
    DIAGRAM_AROUND_X_START_CONTINUOUS: NodalReleaseType.DiagramAroundXStart
    DIAGRAM_AROUND_X_START_STOP: NodalReleaseType.DiagramAroundXStart
    DIAGRAM_AROUND_X_START_YIELDING: NodalReleaseType.DiagramAroundXStart
    class DiagramAroundYStart(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DIAGRAM_AROUND_Y_START_FAILURE: _ClassVar[NodalReleaseType.DiagramAroundYStart]
        DIAGRAM_AROUND_Y_START_CONTINUOUS: _ClassVar[NodalReleaseType.DiagramAroundYStart]
        DIAGRAM_AROUND_Y_START_STOP: _ClassVar[NodalReleaseType.DiagramAroundYStart]
        DIAGRAM_AROUND_Y_START_YIELDING: _ClassVar[NodalReleaseType.DiagramAroundYStart]
    DIAGRAM_AROUND_Y_START_FAILURE: NodalReleaseType.DiagramAroundYStart
    DIAGRAM_AROUND_Y_START_CONTINUOUS: NodalReleaseType.DiagramAroundYStart
    DIAGRAM_AROUND_Y_START_STOP: NodalReleaseType.DiagramAroundYStart
    DIAGRAM_AROUND_Y_START_YIELDING: NodalReleaseType.DiagramAroundYStart
    class DiagramAroundZStart(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DIAGRAM_AROUND_Z_START_FAILURE: _ClassVar[NodalReleaseType.DiagramAroundZStart]
        DIAGRAM_AROUND_Z_START_CONTINUOUS: _ClassVar[NodalReleaseType.DiagramAroundZStart]
        DIAGRAM_AROUND_Z_START_STOP: _ClassVar[NodalReleaseType.DiagramAroundZStart]
        DIAGRAM_AROUND_Z_START_YIELDING: _ClassVar[NodalReleaseType.DiagramAroundZStart]
    DIAGRAM_AROUND_Z_START_FAILURE: NodalReleaseType.DiagramAroundZStart
    DIAGRAM_AROUND_Z_START_CONTINUOUS: NodalReleaseType.DiagramAroundZStart
    DIAGRAM_AROUND_Z_START_STOP: NodalReleaseType.DiagramAroundZStart
    DIAGRAM_AROUND_Z_START_YIELDING: NodalReleaseType.DiagramAroundZStart
    class DiagramAlongXEnd(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DIAGRAM_ALONG_X_END_FAILURE: _ClassVar[NodalReleaseType.DiagramAlongXEnd]
        DIAGRAM_ALONG_X_END_CONTINUOUS: _ClassVar[NodalReleaseType.DiagramAlongXEnd]
        DIAGRAM_ALONG_X_END_STOP: _ClassVar[NodalReleaseType.DiagramAlongXEnd]
        DIAGRAM_ALONG_X_END_YIELDING: _ClassVar[NodalReleaseType.DiagramAlongXEnd]
    DIAGRAM_ALONG_X_END_FAILURE: NodalReleaseType.DiagramAlongXEnd
    DIAGRAM_ALONG_X_END_CONTINUOUS: NodalReleaseType.DiagramAlongXEnd
    DIAGRAM_ALONG_X_END_STOP: NodalReleaseType.DiagramAlongXEnd
    DIAGRAM_ALONG_X_END_YIELDING: NodalReleaseType.DiagramAlongXEnd
    class DiagramAlongYEnd(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DIAGRAM_ALONG_Y_END_FAILURE: _ClassVar[NodalReleaseType.DiagramAlongYEnd]
        DIAGRAM_ALONG_Y_END_CONTINUOUS: _ClassVar[NodalReleaseType.DiagramAlongYEnd]
        DIAGRAM_ALONG_Y_END_STOP: _ClassVar[NodalReleaseType.DiagramAlongYEnd]
        DIAGRAM_ALONG_Y_END_YIELDING: _ClassVar[NodalReleaseType.DiagramAlongYEnd]
    DIAGRAM_ALONG_Y_END_FAILURE: NodalReleaseType.DiagramAlongYEnd
    DIAGRAM_ALONG_Y_END_CONTINUOUS: NodalReleaseType.DiagramAlongYEnd
    DIAGRAM_ALONG_Y_END_STOP: NodalReleaseType.DiagramAlongYEnd
    DIAGRAM_ALONG_Y_END_YIELDING: NodalReleaseType.DiagramAlongYEnd
    class DiagramAlongZEnd(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DIAGRAM_ALONG_Z_END_FAILURE: _ClassVar[NodalReleaseType.DiagramAlongZEnd]
        DIAGRAM_ALONG_Z_END_CONTINUOUS: _ClassVar[NodalReleaseType.DiagramAlongZEnd]
        DIAGRAM_ALONG_Z_END_STOP: _ClassVar[NodalReleaseType.DiagramAlongZEnd]
        DIAGRAM_ALONG_Z_END_YIELDING: _ClassVar[NodalReleaseType.DiagramAlongZEnd]
    DIAGRAM_ALONG_Z_END_FAILURE: NodalReleaseType.DiagramAlongZEnd
    DIAGRAM_ALONG_Z_END_CONTINUOUS: NodalReleaseType.DiagramAlongZEnd
    DIAGRAM_ALONG_Z_END_STOP: NodalReleaseType.DiagramAlongZEnd
    DIAGRAM_ALONG_Z_END_YIELDING: NodalReleaseType.DiagramAlongZEnd
    class DiagramAroundXEnd(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DIAGRAM_AROUND_X_END_FAILURE: _ClassVar[NodalReleaseType.DiagramAroundXEnd]
        DIAGRAM_AROUND_X_END_CONTINUOUS: _ClassVar[NodalReleaseType.DiagramAroundXEnd]
        DIAGRAM_AROUND_X_END_STOP: _ClassVar[NodalReleaseType.DiagramAroundXEnd]
        DIAGRAM_AROUND_X_END_YIELDING: _ClassVar[NodalReleaseType.DiagramAroundXEnd]
    DIAGRAM_AROUND_X_END_FAILURE: NodalReleaseType.DiagramAroundXEnd
    DIAGRAM_AROUND_X_END_CONTINUOUS: NodalReleaseType.DiagramAroundXEnd
    DIAGRAM_AROUND_X_END_STOP: NodalReleaseType.DiagramAroundXEnd
    DIAGRAM_AROUND_X_END_YIELDING: NodalReleaseType.DiagramAroundXEnd
    class DiagramAroundYEnd(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DIAGRAM_AROUND_Y_END_FAILURE: _ClassVar[NodalReleaseType.DiagramAroundYEnd]
        DIAGRAM_AROUND_Y_END_CONTINUOUS: _ClassVar[NodalReleaseType.DiagramAroundYEnd]
        DIAGRAM_AROUND_Y_END_STOP: _ClassVar[NodalReleaseType.DiagramAroundYEnd]
        DIAGRAM_AROUND_Y_END_YIELDING: _ClassVar[NodalReleaseType.DiagramAroundYEnd]
    DIAGRAM_AROUND_Y_END_FAILURE: NodalReleaseType.DiagramAroundYEnd
    DIAGRAM_AROUND_Y_END_CONTINUOUS: NodalReleaseType.DiagramAroundYEnd
    DIAGRAM_AROUND_Y_END_STOP: NodalReleaseType.DiagramAroundYEnd
    DIAGRAM_AROUND_Y_END_YIELDING: NodalReleaseType.DiagramAroundYEnd
    class DiagramAroundZEnd(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DIAGRAM_AROUND_Z_END_FAILURE: _ClassVar[NodalReleaseType.DiagramAroundZEnd]
        DIAGRAM_AROUND_Z_END_CONTINUOUS: _ClassVar[NodalReleaseType.DiagramAroundZEnd]
        DIAGRAM_AROUND_Z_END_STOP: _ClassVar[NodalReleaseType.DiagramAroundZEnd]
        DIAGRAM_AROUND_Z_END_YIELDING: _ClassVar[NodalReleaseType.DiagramAroundZEnd]
    DIAGRAM_AROUND_Z_END_FAILURE: NodalReleaseType.DiagramAroundZEnd
    DIAGRAM_AROUND_Z_END_CONTINUOUS: NodalReleaseType.DiagramAroundZEnd
    DIAGRAM_AROUND_Z_END_STOP: NodalReleaseType.DiagramAroundZEnd
    DIAGRAM_AROUND_Z_END_YIELDING: NodalReleaseType.DiagramAroundZEnd
    class PlasticDiagramAlongXComponentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PLASTIC_DIAGRAM_ALONG_X_COMPONENT_TYPE_PRIMARY: _ClassVar[NodalReleaseType.PlasticDiagramAlongXComponentType]
        PLASTIC_DIAGRAM_ALONG_X_COMPONENT_TYPE_SECONDARY: _ClassVar[NodalReleaseType.PlasticDiagramAlongXComponentType]
    PLASTIC_DIAGRAM_ALONG_X_COMPONENT_TYPE_PRIMARY: NodalReleaseType.PlasticDiagramAlongXComponentType
    PLASTIC_DIAGRAM_ALONG_X_COMPONENT_TYPE_SECONDARY: NodalReleaseType.PlasticDiagramAlongXComponentType
    class PlasticDiagramAlongYComponentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PLASTIC_DIAGRAM_ALONG_Y_COMPONENT_TYPE_PRIMARY: _ClassVar[NodalReleaseType.PlasticDiagramAlongYComponentType]
        PLASTIC_DIAGRAM_ALONG_Y_COMPONENT_TYPE_SECONDARY: _ClassVar[NodalReleaseType.PlasticDiagramAlongYComponentType]
    PLASTIC_DIAGRAM_ALONG_Y_COMPONENT_TYPE_PRIMARY: NodalReleaseType.PlasticDiagramAlongYComponentType
    PLASTIC_DIAGRAM_ALONG_Y_COMPONENT_TYPE_SECONDARY: NodalReleaseType.PlasticDiagramAlongYComponentType
    class PlasticDiagramAlongZComponentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PLASTIC_DIAGRAM_ALONG_Z_COMPONENT_TYPE_PRIMARY: _ClassVar[NodalReleaseType.PlasticDiagramAlongZComponentType]
        PLASTIC_DIAGRAM_ALONG_Z_COMPONENT_TYPE_SECONDARY: _ClassVar[NodalReleaseType.PlasticDiagramAlongZComponentType]
    PLASTIC_DIAGRAM_ALONG_Z_COMPONENT_TYPE_PRIMARY: NodalReleaseType.PlasticDiagramAlongZComponentType
    PLASTIC_DIAGRAM_ALONG_Z_COMPONENT_TYPE_SECONDARY: NodalReleaseType.PlasticDiagramAlongZComponentType
    class PlasticDiagramAroundYComponentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PLASTIC_DIAGRAM_AROUND_Y_COMPONENT_TYPE_PRIMARY: _ClassVar[NodalReleaseType.PlasticDiagramAroundYComponentType]
        PLASTIC_DIAGRAM_AROUND_Y_COMPONENT_TYPE_SECONDARY: _ClassVar[NodalReleaseType.PlasticDiagramAroundYComponentType]
    PLASTIC_DIAGRAM_AROUND_Y_COMPONENT_TYPE_PRIMARY: NodalReleaseType.PlasticDiagramAroundYComponentType
    PLASTIC_DIAGRAM_AROUND_Y_COMPONENT_TYPE_SECONDARY: NodalReleaseType.PlasticDiagramAroundYComponentType
    class PlasticDiagramAroundZComponentType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PLASTIC_DIAGRAM_AROUND_Z_COMPONENT_TYPE_PRIMARY: _ClassVar[NodalReleaseType.PlasticDiagramAroundZComponentType]
        PLASTIC_DIAGRAM_AROUND_Z_COMPONENT_TYPE_SECONDARY: _ClassVar[NodalReleaseType.PlasticDiagramAroundZComponentType]
    PLASTIC_DIAGRAM_AROUND_Z_COMPONENT_TYPE_PRIMARY: NodalReleaseType.PlasticDiagramAroundZComponentType
    PLASTIC_DIAGRAM_AROUND_Z_COMPONENT_TYPE_SECONDARY: NodalReleaseType.PlasticDiagramAroundZComponentType
    class LocalAxisSystemObjectType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LOCAL_AXIS_SYSTEM_OBJECT_TYPE_MEMBER: _ClassVar[NodalReleaseType.LocalAxisSystemObjectType]
        LOCAL_AXIS_SYSTEM_OBJECT_TYPE_LINE: _ClassVar[NodalReleaseType.LocalAxisSystemObjectType]
    LOCAL_AXIS_SYSTEM_OBJECT_TYPE_MEMBER: NodalReleaseType.LocalAxisSystemObjectType
    LOCAL_AXIS_SYSTEM_OBJECT_TYPE_LINE: NodalReleaseType.LocalAxisSystemObjectType
    class DiagramAlongXTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[NodalReleaseType.DiagramAlongXTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[NodalReleaseType.DiagramAlongXTableRow, _Mapping]]] = ...) -> None: ...
    class DiagramAlongXTableRow(_message.Message):
        __slots__ = ("no", "description", "displacement", "force", "spring", "note")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        DISPLACEMENT_FIELD_NUMBER: _ClassVar[int]
        FORCE_FIELD_NUMBER: _ClassVar[int]
        SPRING_FIELD_NUMBER: _ClassVar[int]
        NOTE_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        displacement: float
        force: float
        spring: float
        note: str
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., displacement: _Optional[float] = ..., force: _Optional[float] = ..., spring: _Optional[float] = ..., note: _Optional[str] = ...) -> None: ...
    class DiagramAlongYTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[NodalReleaseType.DiagramAlongYTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[NodalReleaseType.DiagramAlongYTableRow, _Mapping]]] = ...) -> None: ...
    class DiagramAlongYTableRow(_message.Message):
        __slots__ = ("no", "description", "displacement", "force", "spring", "note")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        DISPLACEMENT_FIELD_NUMBER: _ClassVar[int]
        FORCE_FIELD_NUMBER: _ClassVar[int]
        SPRING_FIELD_NUMBER: _ClassVar[int]
        NOTE_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        displacement: float
        force: float
        spring: float
        note: str
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., displacement: _Optional[float] = ..., force: _Optional[float] = ..., spring: _Optional[float] = ..., note: _Optional[str] = ...) -> None: ...
    class DiagramAlongZTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[NodalReleaseType.DiagramAlongZTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[NodalReleaseType.DiagramAlongZTableRow, _Mapping]]] = ...) -> None: ...
    class DiagramAlongZTableRow(_message.Message):
        __slots__ = ("no", "description", "displacement", "force", "spring", "note")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        DISPLACEMENT_FIELD_NUMBER: _ClassVar[int]
        FORCE_FIELD_NUMBER: _ClassVar[int]
        SPRING_FIELD_NUMBER: _ClassVar[int]
        NOTE_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        displacement: float
        force: float
        spring: float
        note: str
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., displacement: _Optional[float] = ..., force: _Optional[float] = ..., spring: _Optional[float] = ..., note: _Optional[str] = ...) -> None: ...
    class DiagramAroundXTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[NodalReleaseType.DiagramAroundXTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[NodalReleaseType.DiagramAroundXTableRow, _Mapping]]] = ...) -> None: ...
    class DiagramAroundXTableRow(_message.Message):
        __slots__ = ("no", "description", "rotation", "moment", "spring", "note")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        ROTATION_FIELD_NUMBER: _ClassVar[int]
        MOMENT_FIELD_NUMBER: _ClassVar[int]
        SPRING_FIELD_NUMBER: _ClassVar[int]
        NOTE_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        rotation: float
        moment: float
        spring: float
        note: str
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., rotation: _Optional[float] = ..., moment: _Optional[float] = ..., spring: _Optional[float] = ..., note: _Optional[str] = ...) -> None: ...
    class DiagramAroundYTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[NodalReleaseType.DiagramAroundYTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[NodalReleaseType.DiagramAroundYTableRow, _Mapping]]] = ...) -> None: ...
    class DiagramAroundYTableRow(_message.Message):
        __slots__ = ("no", "description", "rotation", "moment", "spring", "note")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        ROTATION_FIELD_NUMBER: _ClassVar[int]
        MOMENT_FIELD_NUMBER: _ClassVar[int]
        SPRING_FIELD_NUMBER: _ClassVar[int]
        NOTE_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        rotation: float
        moment: float
        spring: float
        note: str
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., rotation: _Optional[float] = ..., moment: _Optional[float] = ..., spring: _Optional[float] = ..., note: _Optional[str] = ...) -> None: ...
    class DiagramAroundZTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[NodalReleaseType.DiagramAroundZTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[NodalReleaseType.DiagramAroundZTableRow, _Mapping]]] = ...) -> None: ...
    class DiagramAroundZTableRow(_message.Message):
        __slots__ = ("no", "description", "rotation", "moment", "spring", "note")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        ROTATION_FIELD_NUMBER: _ClassVar[int]
        MOMENT_FIELD_NUMBER: _ClassVar[int]
        SPRING_FIELD_NUMBER: _ClassVar[int]
        NOTE_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        rotation: float
        moment: float
        spring: float
        note: str
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., rotation: _Optional[float] = ..., moment: _Optional[float] = ..., spring: _Optional[float] = ..., note: _Optional[str] = ...) -> None: ...
    class DiagramAlongXColorTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[NodalReleaseType.DiagramAlongXColorTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[NodalReleaseType.DiagramAlongXColorTableRow, _Mapping]]] = ...) -> None: ...
    class DiagramAlongXColorTableRow(_message.Message):
        __slots__ = ("no", "description", "color")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        COLOR_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        color: _common_pb2.Color
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., color: _Optional[_Union[_common_pb2.Color, _Mapping]] = ...) -> None: ...
    class DiagramAlongYColorTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[NodalReleaseType.DiagramAlongYColorTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[NodalReleaseType.DiagramAlongYColorTableRow, _Mapping]]] = ...) -> None: ...
    class DiagramAlongYColorTableRow(_message.Message):
        __slots__ = ("no", "description", "color")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        COLOR_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        color: _common_pb2.Color
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., color: _Optional[_Union[_common_pb2.Color, _Mapping]] = ...) -> None: ...
    class DiagramAlongZColorTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[NodalReleaseType.DiagramAlongZColorTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[NodalReleaseType.DiagramAlongZColorTableRow, _Mapping]]] = ...) -> None: ...
    class DiagramAlongZColorTableRow(_message.Message):
        __slots__ = ("no", "description", "color")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        COLOR_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        color: _common_pb2.Color
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., color: _Optional[_Union[_common_pb2.Color, _Mapping]] = ...) -> None: ...
    class DiagramAroundXColorTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[NodalReleaseType.DiagramAroundXColorTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[NodalReleaseType.DiagramAroundXColorTableRow, _Mapping]]] = ...) -> None: ...
    class DiagramAroundXColorTableRow(_message.Message):
        __slots__ = ("no", "description", "color")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        COLOR_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        color: _common_pb2.Color
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., color: _Optional[_Union[_common_pb2.Color, _Mapping]] = ...) -> None: ...
    class DiagramAroundYColorTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[NodalReleaseType.DiagramAroundYColorTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[NodalReleaseType.DiagramAroundYColorTableRow, _Mapping]]] = ...) -> None: ...
    class DiagramAroundYColorTableRow(_message.Message):
        __slots__ = ("no", "description", "color")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        COLOR_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        color: _common_pb2.Color
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., color: _Optional[_Union[_common_pb2.Color, _Mapping]] = ...) -> None: ...
    class DiagramAroundZColorTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[NodalReleaseType.DiagramAroundZColorTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[NodalReleaseType.DiagramAroundZColorTableRow, _Mapping]]] = ...) -> None: ...
    class DiagramAroundZColorTableRow(_message.Message):
        __slots__ = ("no", "description", "color")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        COLOR_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        color: _common_pb2.Color
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., color: _Optional[_Union[_common_pb2.Color, _Mapping]] = ...) -> None: ...
    class PlasticDiagramAlongXTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[NodalReleaseType.PlasticDiagramAlongXTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[NodalReleaseType.PlasticDiagramAlongXTableRow, _Mapping]]] = ...) -> None: ...
    class PlasticDiagramAlongXTableRow(_message.Message):
        __slots__ = ("no", "description", "force_ratio", "deflection_ratio")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        FORCE_RATIO_FIELD_NUMBER: _ClassVar[int]
        DEFLECTION_RATIO_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        force_ratio: float
        deflection_ratio: float
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., force_ratio: _Optional[float] = ..., deflection_ratio: _Optional[float] = ...) -> None: ...
    class PlasticDiagramAlongYTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[NodalReleaseType.PlasticDiagramAlongYTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[NodalReleaseType.PlasticDiagramAlongYTableRow, _Mapping]]] = ...) -> None: ...
    class PlasticDiagramAlongYTableRow(_message.Message):
        __slots__ = ("no", "description", "force_ratio", "deflection_ratio")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        FORCE_RATIO_FIELD_NUMBER: _ClassVar[int]
        DEFLECTION_RATIO_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        force_ratio: float
        deflection_ratio: float
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., force_ratio: _Optional[float] = ..., deflection_ratio: _Optional[float] = ...) -> None: ...
    class PlasticDiagramAlongZTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[NodalReleaseType.PlasticDiagramAlongZTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[NodalReleaseType.PlasticDiagramAlongZTableRow, _Mapping]]] = ...) -> None: ...
    class PlasticDiagramAlongZTableRow(_message.Message):
        __slots__ = ("no", "description", "force_ratio", "deflection_ratio")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        FORCE_RATIO_FIELD_NUMBER: _ClassVar[int]
        DEFLECTION_RATIO_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        force_ratio: float
        deflection_ratio: float
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., force_ratio: _Optional[float] = ..., deflection_ratio: _Optional[float] = ...) -> None: ...
    class PlasticDiagramAroundYTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[NodalReleaseType.PlasticDiagramAroundYTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[NodalReleaseType.PlasticDiagramAroundYTableRow, _Mapping]]] = ...) -> None: ...
    class PlasticDiagramAroundYTableRow(_message.Message):
        __slots__ = ("no", "description", "force_ratio", "deflection_ratio")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        FORCE_RATIO_FIELD_NUMBER: _ClassVar[int]
        DEFLECTION_RATIO_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        force_ratio: float
        deflection_ratio: float
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., force_ratio: _Optional[float] = ..., deflection_ratio: _Optional[float] = ...) -> None: ...
    class PlasticDiagramAroundZTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[NodalReleaseType.PlasticDiagramAroundZTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[NodalReleaseType.PlasticDiagramAroundZTableRow, _Mapping]]] = ...) -> None: ...
    class PlasticDiagramAroundZTableRow(_message.Message):
        __slots__ = ("no", "description", "force_ratio", "deflection_ratio")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        FORCE_RATIO_FIELD_NUMBER: _ClassVar[int]
        DEFLECTION_RATIO_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        force_ratio: float
        deflection_ratio: float
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., force_ratio: _Optional[float] = ..., deflection_ratio: _Optional[float] = ...) -> None: ...
    class PlasticDiagramAlongXColorTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[NodalReleaseType.PlasticDiagramAlongXColorTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[NodalReleaseType.PlasticDiagramAlongXColorTableRow, _Mapping]]] = ...) -> None: ...
    class PlasticDiagramAlongXColorTableRow(_message.Message):
        __slots__ = ("no", "description", "color")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        COLOR_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        color: _common_pb2.Color
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., color: _Optional[_Union[_common_pb2.Color, _Mapping]] = ...) -> None: ...
    class PlasticDiagramAlongYColorTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[NodalReleaseType.PlasticDiagramAlongYColorTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[NodalReleaseType.PlasticDiagramAlongYColorTableRow, _Mapping]]] = ...) -> None: ...
    class PlasticDiagramAlongYColorTableRow(_message.Message):
        __slots__ = ("no", "description", "color")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        COLOR_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        color: _common_pb2.Color
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., color: _Optional[_Union[_common_pb2.Color, _Mapping]] = ...) -> None: ...
    class PlasticDiagramAlongZColorTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[NodalReleaseType.PlasticDiagramAlongZColorTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[NodalReleaseType.PlasticDiagramAlongZColorTableRow, _Mapping]]] = ...) -> None: ...
    class PlasticDiagramAlongZColorTableRow(_message.Message):
        __slots__ = ("no", "description", "color")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        COLOR_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        color: _common_pb2.Color
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., color: _Optional[_Union[_common_pb2.Color, _Mapping]] = ...) -> None: ...
    class PlasticDiagramAroundYColorTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[NodalReleaseType.PlasticDiagramAroundYColorTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[NodalReleaseType.PlasticDiagramAroundYColorTableRow, _Mapping]]] = ...) -> None: ...
    class PlasticDiagramAroundYColorTableRow(_message.Message):
        __slots__ = ("no", "description", "color")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        COLOR_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        color: _common_pb2.Color
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., color: _Optional[_Union[_common_pb2.Color, _Mapping]] = ...) -> None: ...
    class PlasticDiagramAroundZColorTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[NodalReleaseType.PlasticDiagramAroundZColorTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[NodalReleaseType.PlasticDiagramAroundZColorTableRow, _Mapping]]] = ...) -> None: ...
    class PlasticDiagramAroundZColorTableRow(_message.Message):
        __slots__ = ("no", "description", "color")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        COLOR_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        color: _common_pb2.Color
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., color: _Optional[_Union[_common_pb2.Color, _Mapping]] = ...) -> None: ...
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NODAL_RELEASES_FIELD_NUMBER: _ClassVar[int]
    COORDINATE_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    AXIAL_RELEASE_N_FIELD_NUMBER: _ClassVar[int]
    AXIAL_RELEASE_VY_FIELD_NUMBER: _ClassVar[int]
    AXIAL_RELEASE_VZ_FIELD_NUMBER: _ClassVar[int]
    MOMENT_RELEASE_MT_FIELD_NUMBER: _ClassVar[int]
    MOMENT_RELEASE_MY_FIELD_NUMBER: _ClassVar[int]
    MOMENT_RELEASE_MZ_FIELD_NUMBER: _ClassVar[int]
    AXIAL_RELEASE_N_NONLINEARITY_FIELD_NUMBER: _ClassVar[int]
    AXIAL_RELEASE_VY_NONLINEARITY_FIELD_NUMBER: _ClassVar[int]
    AXIAL_RELEASE_VZ_NONLINEARITY_FIELD_NUMBER: _ClassVar[int]
    MOMENT_RELEASE_MT_NONLINEARITY_FIELD_NUMBER: _ClassVar[int]
    MOMENT_RELEASE_MY_NONLINEARITY_FIELD_NUMBER: _ClassVar[int]
    MOMENT_RELEASE_MZ_NONLINEARITY_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_ALONG_X_NEGATIVE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_ALONG_X_POSITIVE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_ALONG_Y_NEGATIVE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_ALONG_Y_POSITIVE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_ALONG_Z_NEGATIVE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_ALONG_Z_POSITIVE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_AROUND_X_NEGATIVE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_AROUND_X_POSITIVE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_AROUND_Y_NEGATIVE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_AROUND_Y_POSITIVE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_AROUND_Z_NEGATIVE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_AROUND_Z_POSITIVE_TYPE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_ALONG_X_NEGATIVE_DISPLACEMENT_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_ALONG_X_POSITIVE_DISPLACEMENT_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_ALONG_Y_NEGATIVE_DISPLACEMENT_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_ALONG_Y_POSITIVE_DISPLACEMENT_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_ALONG_Z_NEGATIVE_DISPLACEMENT_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_ALONG_Z_POSITIVE_DISPLACEMENT_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_AROUND_X_NEGATIVE_ROTATION_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_AROUND_X_POSITIVE_ROTATION_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_AROUND_Y_NEGATIVE_ROTATION_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_AROUND_Y_POSITIVE_ROTATION_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_AROUND_Z_NEGATIVE_ROTATION_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_AROUND_Z_POSITIVE_ROTATION_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_ALONG_X_NEGATIVE_FORCE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_ALONG_X_POSITIVE_FORCE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_ALONG_Y_NEGATIVE_FORCE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_ALONG_Y_POSITIVE_FORCE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_ALONG_Z_NEGATIVE_FORCE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_ALONG_Z_POSITIVE_FORCE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_AROUND_X_NEGATIVE_MOMENT_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_AROUND_X_POSITIVE_MOMENT_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_AROUND_Y_NEGATIVE_MOMENT_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_AROUND_Y_POSITIVE_MOMENT_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_AROUND_Z_NEGATIVE_MOMENT_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_AROUND_Z_POSITIVE_MOMENT_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_ALONG_X_NEGATIVE_SLIPPAGE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_ALONG_X_POSITIVE_SLIPPAGE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_ALONG_Y_NEGATIVE_SLIPPAGE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_ALONG_Y_POSITIVE_SLIPPAGE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_ALONG_Z_NEGATIVE_SLIPPAGE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_ALONG_Z_POSITIVE_SLIPPAGE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_AROUND_X_NEGATIVE_SLIPPAGE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_AROUND_X_POSITIVE_SLIPPAGE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_AROUND_Y_NEGATIVE_SLIPPAGE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_AROUND_Y_POSITIVE_SLIPPAGE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_AROUND_Z_NEGATIVE_SLIPPAGE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_ACTIVITY_AROUND_Z_POSITIVE_SLIPPAGE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_X_SYMMETRIC_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Y_SYMMETRIC_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Z_SYMMETRIC_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_X_SYMMETRIC_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_Y_SYMMETRIC_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_Z_SYMMETRIC_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_X_IS_SORTED_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Y_IS_SORTED_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Z_IS_SORTED_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_X_IS_SORTED_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_Y_IS_SORTED_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_Z_IS_SORTED_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_X_START_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Y_START_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Z_START_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_X_START_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_Y_START_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_Z_START_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_X_END_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Y_END_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Z_END_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_X_END_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_Y_END_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_Z_END_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_X_TABLE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Y_TABLE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Z_TABLE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_X_TABLE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_Y_TABLE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_Z_TABLE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_X_AC_YIELD_MINUS_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Y_AC_YIELD_MINUS_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Z_AC_YIELD_MINUS_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_X_AC_YIELD_MINUS_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_Y_AC_YIELD_MINUS_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_Z_AC_YIELD_MINUS_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_X_AC_YIELD_PLUS_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Y_AC_YIELD_PLUS_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Z_AC_YIELD_PLUS_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_X_AC_YIELD_PLUS_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_Y_AC_YIELD_PLUS_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_Z_AC_YIELD_PLUS_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_X_ACCEPTANCE_CRITERIA_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Y_ACCEPTANCE_CRITERIA_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Z_ACCEPTANCE_CRITERIA_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_X_ACCEPTANCE_CRITERIA_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_Y_ACCEPTANCE_CRITERIA_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_Z_ACCEPTANCE_CRITERIA_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_X_MINUS_COLOR_ONE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Y_MINUS_COLOR_ONE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Z_MINUS_COLOR_ONE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_X_MINUS_COLOR_ONE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_Y_MINUS_COLOR_ONE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_Z_MINUS_COLOR_ONE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_X_MINUS_COLOR_TWO_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Y_MINUS_COLOR_TWO_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Z_MINUS_COLOR_TWO_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_X_MINUS_COLOR_TWO_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_Y_MINUS_COLOR_TWO_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_Z_MINUS_COLOR_TWO_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_X_PLUS_COLOR_ONE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Y_PLUS_COLOR_ONE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Z_PLUS_COLOR_ONE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_X_PLUS_COLOR_ONE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_Y_PLUS_COLOR_ONE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_Z_PLUS_COLOR_ONE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_X_PLUS_COLOR_TWO_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Y_PLUS_COLOR_TWO_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Z_PLUS_COLOR_TWO_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_X_PLUS_COLOR_TWO_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_Y_PLUS_COLOR_TWO_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_Z_PLUS_COLOR_TWO_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_X_COLOR_TABLE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Y_COLOR_TABLE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_ALONG_Z_COLOR_TABLE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_X_COLOR_TABLE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_Y_COLOR_TABLE_FIELD_NUMBER: _ClassVar[int]
    DIAGRAM_AROUND_Z_COLOR_TABLE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_X_TABLE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Y_TABLE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Z_TABLE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Y_TABLE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Z_TABLE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_X_SYMMETRIC_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Y_SYMMETRIC_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Z_SYMMETRIC_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Y_SYMMETRIC_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Z_SYMMETRIC_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Y_FORCE_INTERACTION_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Z_FORCE_INTERACTION_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_X_USER_DEFINED_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Y_USER_DEFINED_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Z_USER_DEFINED_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Y_USER_DEFINED_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Z_USER_DEFINED_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_X_IS_USER_DEFINED_MEMBER_LENGTH_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Y_IS_USER_DEFINED_MEMBER_LENGTH_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Z_IS_USER_DEFINED_MEMBER_LENGTH_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Y_IS_USER_DEFINED_MEMBER_LENGTH_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Z_IS_USER_DEFINED_MEMBER_LENGTH_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_X_USER_DEFINED_MEMBER_LENGTH_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Y_USER_DEFINED_MEMBER_LENGTH_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Z_USER_DEFINED_MEMBER_LENGTH_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Y_USER_DEFINED_MEMBER_LENGTH_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Z_USER_DEFINED_MEMBER_LENGTH_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_X_ATTACHED_MEMBERS_MIN_MAX_LENGTH_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Y_ATTACHED_MEMBERS_MIN_MAX_LENGTH_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Z_ATTACHED_MEMBERS_MIN_MAX_LENGTH_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Y_ATTACHED_MEMBERS_MIN_MAX_LENGTH_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Z_ATTACHED_MEMBERS_MIN_MAX_LENGTH_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_X_IO_NEGATIVE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Y_IO_NEGATIVE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Z_IO_NEGATIVE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Y_IO_NEGATIVE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Z_IO_NEGATIVE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_X_IO_POSITIVE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Y_IO_POSITIVE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Z_IO_POSITIVE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Y_IO_POSITIVE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Z_IO_POSITIVE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_X_LS_NEGATIVE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Y_LS_NEGATIVE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Z_LS_NEGATIVE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Y_LS_NEGATIVE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Z_LS_NEGATIVE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_X_LS_POSITIVE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Y_LS_POSITIVE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Z_LS_POSITIVE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Y_LS_POSITIVE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Z_LS_POSITIVE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_X_CP_NEGATIVE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Y_CP_NEGATIVE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Z_CP_NEGATIVE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Y_CP_NEGATIVE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Z_CP_NEGATIVE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_X_CP_POSITIVE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Y_CP_POSITIVE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Z_CP_POSITIVE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Y_CP_POSITIVE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Z_CP_POSITIVE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_X_MINUS_COLOR_ONE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Y_MINUS_COLOR_ONE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Z_MINUS_COLOR_ONE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Y_MINUS_COLOR_ONE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Z_MINUS_COLOR_ONE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_X_MINUS_COLOR_TWO_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Y_MINUS_COLOR_TWO_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Z_MINUS_COLOR_TWO_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Y_MINUS_COLOR_TWO_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Z_MINUS_COLOR_TWO_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_X_MINUS_COLOR_THREE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Y_MINUS_COLOR_THREE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Z_MINUS_COLOR_THREE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Y_MINUS_COLOR_THREE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Z_MINUS_COLOR_THREE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_X_MINUS_COLOR_FOUR_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Y_MINUS_COLOR_FOUR_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Z_MINUS_COLOR_FOUR_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Y_MINUS_COLOR_FOUR_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Z_MINUS_COLOR_FOUR_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_X_PLUS_COLOR_ONE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Y_PLUS_COLOR_ONE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Z_PLUS_COLOR_ONE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Y_PLUS_COLOR_ONE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Z_PLUS_COLOR_ONE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_X_PLUS_COLOR_TWO_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Y_PLUS_COLOR_TWO_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Z_PLUS_COLOR_TWO_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Y_PLUS_COLOR_TWO_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Z_PLUS_COLOR_TWO_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_X_PLUS_COLOR_THREE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Y_PLUS_COLOR_THREE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Z_PLUS_COLOR_THREE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Y_PLUS_COLOR_THREE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Z_PLUS_COLOR_THREE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_X_PLUS_COLOR_FOUR_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Y_PLUS_COLOR_FOUR_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Z_PLUS_COLOR_FOUR_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Y_PLUS_COLOR_FOUR_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Z_PLUS_COLOR_FOUR_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_X_COMPONENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Y_COMPONENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Z_COMPONENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Y_COMPONENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Z_COMPONENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_X_COLOR_TABLE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Y_COLOR_TABLE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_ALONG_Z_COLOR_TABLE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Y_COLOR_TABLE_FIELD_NUMBER: _ClassVar[int]
    PLASTIC_DIAGRAM_AROUND_Z_COLOR_TABLE_FIELD_NUMBER: _ClassVar[int]
    FRICTION_COEFFICIENT_X_FIELD_NUMBER: _ClassVar[int]
    FRICTION_COEFFICIENT_XY_FIELD_NUMBER: _ClassVar[int]
    FRICTION_COEFFICIENT_XZ_FIELD_NUMBER: _ClassVar[int]
    FRICTION_COEFFICIENT_Y_FIELD_NUMBER: _ClassVar[int]
    FRICTION_COEFFICIENT_YX_FIELD_NUMBER: _ClassVar[int]
    FRICTION_COEFFICIENT_YZ_FIELD_NUMBER: _ClassVar[int]
    FRICTION_COEFFICIENT_Z_FIELD_NUMBER: _ClassVar[int]
    FRICTION_COEFFICIENT_ZX_FIELD_NUMBER: _ClassVar[int]
    FRICTION_COEFFICIENT_ZY_FIELD_NUMBER: _ClassVar[int]
    FRICTION_DIRECTION_INDEPENDENT_X_FIELD_NUMBER: _ClassVar[int]
    FRICTION_DIRECTION_INDEPENDENT_Y_FIELD_NUMBER: _ClassVar[int]
    FRICTION_DIRECTION_INDEPENDENT_Z_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    GENERATED_BY_PILE_FIELD_NUMBER: _ClassVar[int]
    LOCAL_AXIS_SYSTEM_OBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    LOCAL_AXIS_SYSTEM_REFERENCE_OBJECT_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    nodal_releases: _containers.RepeatedScalarFieldContainer[int]
    coordinate_system: _common_pb2.CoordinateSystemRepresentation
    axial_release_n: float
    axial_release_vy: float
    axial_release_vz: float
    moment_release_mt: float
    moment_release_my: float
    moment_release_mz: float
    axial_release_n_nonlinearity: NodalReleaseType.AxialReleaseNNonlinearity
    axial_release_vy_nonlinearity: NodalReleaseType.AxialReleaseVyNonlinearity
    axial_release_vz_nonlinearity: NodalReleaseType.AxialReleaseVzNonlinearity
    moment_release_mt_nonlinearity: NodalReleaseType.MomentReleaseMtNonlinearity
    moment_release_my_nonlinearity: NodalReleaseType.MomentReleaseMyNonlinearity
    moment_release_mz_nonlinearity: NodalReleaseType.MomentReleaseMzNonlinearity
    partial_activity_along_x_negative_type: NodalReleaseType.PartialActivityAlongXNegativeType
    partial_activity_along_x_positive_type: NodalReleaseType.PartialActivityAlongXPositiveType
    partial_activity_along_y_negative_type: NodalReleaseType.PartialActivityAlongYNegativeType
    partial_activity_along_y_positive_type: NodalReleaseType.PartialActivityAlongYPositiveType
    partial_activity_along_z_negative_type: NodalReleaseType.PartialActivityAlongZNegativeType
    partial_activity_along_z_positive_type: NodalReleaseType.PartialActivityAlongZPositiveType
    partial_activity_around_x_negative_type: NodalReleaseType.PartialActivityAroundXNegativeType
    partial_activity_around_x_positive_type: NodalReleaseType.PartialActivityAroundXPositiveType
    partial_activity_around_y_negative_type: NodalReleaseType.PartialActivityAroundYNegativeType
    partial_activity_around_y_positive_type: NodalReleaseType.PartialActivityAroundYPositiveType
    partial_activity_around_z_negative_type: NodalReleaseType.PartialActivityAroundZNegativeType
    partial_activity_around_z_positive_type: NodalReleaseType.PartialActivityAroundZPositiveType
    partial_activity_along_x_negative_displacement: float
    partial_activity_along_x_positive_displacement: float
    partial_activity_along_y_negative_displacement: float
    partial_activity_along_y_positive_displacement: float
    partial_activity_along_z_negative_displacement: float
    partial_activity_along_z_positive_displacement: float
    partial_activity_around_x_negative_rotation: float
    partial_activity_around_x_positive_rotation: float
    partial_activity_around_y_negative_rotation: float
    partial_activity_around_y_positive_rotation: float
    partial_activity_around_z_negative_rotation: float
    partial_activity_around_z_positive_rotation: float
    partial_activity_along_x_negative_force: float
    partial_activity_along_x_positive_force: float
    partial_activity_along_y_negative_force: float
    partial_activity_along_y_positive_force: float
    partial_activity_along_z_negative_force: float
    partial_activity_along_z_positive_force: float
    partial_activity_around_x_negative_moment: float
    partial_activity_around_x_positive_moment: float
    partial_activity_around_y_negative_moment: float
    partial_activity_around_y_positive_moment: float
    partial_activity_around_z_negative_moment: float
    partial_activity_around_z_positive_moment: float
    partial_activity_along_x_negative_slippage: float
    partial_activity_along_x_positive_slippage: float
    partial_activity_along_y_negative_slippage: float
    partial_activity_along_y_positive_slippage: float
    partial_activity_along_z_negative_slippage: float
    partial_activity_along_z_positive_slippage: float
    partial_activity_around_x_negative_slippage: float
    partial_activity_around_x_positive_slippage: float
    partial_activity_around_y_negative_slippage: float
    partial_activity_around_y_positive_slippage: float
    partial_activity_around_z_negative_slippage: float
    partial_activity_around_z_positive_slippage: float
    diagram_along_x_symmetric: bool
    diagram_along_y_symmetric: bool
    diagram_along_z_symmetric: bool
    diagram_around_x_symmetric: bool
    diagram_around_y_symmetric: bool
    diagram_around_z_symmetric: bool
    diagram_along_x_is_sorted: bool
    diagram_along_y_is_sorted: bool
    diagram_along_z_is_sorted: bool
    diagram_around_x_is_sorted: bool
    diagram_around_y_is_sorted: bool
    diagram_around_z_is_sorted: bool
    diagram_along_x_start: NodalReleaseType.DiagramAlongXStart
    diagram_along_y_start: NodalReleaseType.DiagramAlongYStart
    diagram_along_z_start: NodalReleaseType.DiagramAlongZStart
    diagram_around_x_start: NodalReleaseType.DiagramAroundXStart
    diagram_around_y_start: NodalReleaseType.DiagramAroundYStart
    diagram_around_z_start: NodalReleaseType.DiagramAroundZStart
    diagram_along_x_end: NodalReleaseType.DiagramAlongXEnd
    diagram_along_y_end: NodalReleaseType.DiagramAlongYEnd
    diagram_along_z_end: NodalReleaseType.DiagramAlongZEnd
    diagram_around_x_end: NodalReleaseType.DiagramAroundXEnd
    diagram_around_y_end: NodalReleaseType.DiagramAroundYEnd
    diagram_around_z_end: NodalReleaseType.DiagramAroundZEnd
    diagram_along_x_table: NodalReleaseType.DiagramAlongXTable
    diagram_along_y_table: NodalReleaseType.DiagramAlongYTable
    diagram_along_z_table: NodalReleaseType.DiagramAlongZTable
    diagram_around_x_table: NodalReleaseType.DiagramAroundXTable
    diagram_around_y_table: NodalReleaseType.DiagramAroundYTable
    diagram_around_z_table: NodalReleaseType.DiagramAroundZTable
    diagram_along_x_ac_yield_minus: float
    diagram_along_y_ac_yield_minus: float
    diagram_along_z_ac_yield_minus: float
    diagram_around_x_ac_yield_minus: float
    diagram_around_y_ac_yield_minus: float
    diagram_around_z_ac_yield_minus: float
    diagram_along_x_ac_yield_plus: float
    diagram_along_y_ac_yield_plus: float
    diagram_along_z_ac_yield_plus: float
    diagram_around_x_ac_yield_plus: float
    diagram_around_y_ac_yield_plus: float
    diagram_around_z_ac_yield_plus: float
    diagram_along_x_acceptance_criteria_active: bool
    diagram_along_y_acceptance_criteria_active: bool
    diagram_along_z_acceptance_criteria_active: bool
    diagram_around_x_acceptance_criteria_active: bool
    diagram_around_y_acceptance_criteria_active: bool
    diagram_around_z_acceptance_criteria_active: bool
    diagram_along_x_minus_color_one: _common_pb2.Color
    diagram_along_y_minus_color_one: _common_pb2.Color
    diagram_along_z_minus_color_one: _common_pb2.Color
    diagram_around_x_minus_color_one: _common_pb2.Color
    diagram_around_y_minus_color_one: _common_pb2.Color
    diagram_around_z_minus_color_one: _common_pb2.Color
    diagram_along_x_minus_color_two: _common_pb2.Color
    diagram_along_y_minus_color_two: _common_pb2.Color
    diagram_along_z_minus_color_two: _common_pb2.Color
    diagram_around_x_minus_color_two: _common_pb2.Color
    diagram_around_y_minus_color_two: _common_pb2.Color
    diagram_around_z_minus_color_two: _common_pb2.Color
    diagram_along_x_plus_color_one: _common_pb2.Color
    diagram_along_y_plus_color_one: _common_pb2.Color
    diagram_along_z_plus_color_one: _common_pb2.Color
    diagram_around_x_plus_color_one: _common_pb2.Color
    diagram_around_y_plus_color_one: _common_pb2.Color
    diagram_around_z_plus_color_one: _common_pb2.Color
    diagram_along_x_plus_color_two: _common_pb2.Color
    diagram_along_y_plus_color_two: _common_pb2.Color
    diagram_along_z_plus_color_two: _common_pb2.Color
    diagram_around_x_plus_color_two: _common_pb2.Color
    diagram_around_y_plus_color_two: _common_pb2.Color
    diagram_around_z_plus_color_two: _common_pb2.Color
    diagram_along_x_color_table: NodalReleaseType.DiagramAlongXColorTable
    diagram_along_y_color_table: NodalReleaseType.DiagramAlongYColorTable
    diagram_along_z_color_table: NodalReleaseType.DiagramAlongZColorTable
    diagram_around_x_color_table: NodalReleaseType.DiagramAroundXColorTable
    diagram_around_y_color_table: NodalReleaseType.DiagramAroundYColorTable
    diagram_around_z_color_table: NodalReleaseType.DiagramAroundZColorTable
    plastic_diagram_along_x_table: NodalReleaseType.PlasticDiagramAlongXTable
    plastic_diagram_along_y_table: NodalReleaseType.PlasticDiagramAlongYTable
    plastic_diagram_along_z_table: NodalReleaseType.PlasticDiagramAlongZTable
    plastic_diagram_around_y_table: NodalReleaseType.PlasticDiagramAroundYTable
    plastic_diagram_around_z_table: NodalReleaseType.PlasticDiagramAroundZTable
    plastic_diagram_along_x_symmetric: bool
    plastic_diagram_along_y_symmetric: bool
    plastic_diagram_along_z_symmetric: bool
    plastic_diagram_around_y_symmetric: bool
    plastic_diagram_around_z_symmetric: bool
    plastic_diagram_around_y_force_interaction: bool
    plastic_diagram_around_z_force_interaction: bool
    plastic_diagram_along_x_user_defined: bool
    plastic_diagram_along_y_user_defined: bool
    plastic_diagram_along_z_user_defined: bool
    plastic_diagram_around_y_user_defined: bool
    plastic_diagram_around_z_user_defined: bool
    plastic_diagram_along_x_is_user_defined_member_length: bool
    plastic_diagram_along_y_is_user_defined_member_length: bool
    plastic_diagram_along_z_is_user_defined_member_length: bool
    plastic_diagram_around_y_is_user_defined_member_length: bool
    plastic_diagram_around_z_is_user_defined_member_length: bool
    plastic_diagram_along_x_user_defined_member_length: float
    plastic_diagram_along_y_user_defined_member_length: float
    plastic_diagram_along_z_user_defined_member_length: float
    plastic_diagram_around_y_user_defined_member_length: float
    plastic_diagram_around_z_user_defined_member_length: float
    plastic_diagram_along_x_attached_members_min_max_length: str
    plastic_diagram_along_y_attached_members_min_max_length: str
    plastic_diagram_along_z_attached_members_min_max_length: str
    plastic_diagram_around_y_attached_members_min_max_length: str
    plastic_diagram_around_z_attached_members_min_max_length: str
    plastic_diagram_along_x_io_negative: float
    plastic_diagram_along_y_io_negative: float
    plastic_diagram_along_z_io_negative: float
    plastic_diagram_around_y_io_negative: float
    plastic_diagram_around_z_io_negative: float
    plastic_diagram_along_x_io_positive: float
    plastic_diagram_along_y_io_positive: float
    plastic_diagram_along_z_io_positive: float
    plastic_diagram_around_y_io_positive: float
    plastic_diagram_around_z_io_positive: float
    plastic_diagram_along_x_ls_negative: float
    plastic_diagram_along_y_ls_negative: float
    plastic_diagram_along_z_ls_negative: float
    plastic_diagram_around_y_ls_negative: float
    plastic_diagram_around_z_ls_negative: float
    plastic_diagram_along_x_ls_positive: float
    plastic_diagram_along_y_ls_positive: float
    plastic_diagram_along_z_ls_positive: float
    plastic_diagram_around_y_ls_positive: float
    plastic_diagram_around_z_ls_positive: float
    plastic_diagram_along_x_cp_negative: float
    plastic_diagram_along_y_cp_negative: float
    plastic_diagram_along_z_cp_negative: float
    plastic_diagram_around_y_cp_negative: float
    plastic_diagram_around_z_cp_negative: float
    plastic_diagram_along_x_cp_positive: float
    plastic_diagram_along_y_cp_positive: float
    plastic_diagram_along_z_cp_positive: float
    plastic_diagram_around_y_cp_positive: float
    plastic_diagram_around_z_cp_positive: float
    plastic_diagram_along_x_minus_color_one: _common_pb2.Color
    plastic_diagram_along_y_minus_color_one: _common_pb2.Color
    plastic_diagram_along_z_minus_color_one: _common_pb2.Color
    plastic_diagram_around_y_minus_color_one: _common_pb2.Color
    plastic_diagram_around_z_minus_color_one: _common_pb2.Color
    plastic_diagram_along_x_minus_color_two: _common_pb2.Color
    plastic_diagram_along_y_minus_color_two: _common_pb2.Color
    plastic_diagram_along_z_minus_color_two: _common_pb2.Color
    plastic_diagram_around_y_minus_color_two: _common_pb2.Color
    plastic_diagram_around_z_minus_color_two: _common_pb2.Color
    plastic_diagram_along_x_minus_color_three: _common_pb2.Color
    plastic_diagram_along_y_minus_color_three: _common_pb2.Color
    plastic_diagram_along_z_minus_color_three: _common_pb2.Color
    plastic_diagram_around_y_minus_color_three: _common_pb2.Color
    plastic_diagram_around_z_minus_color_three: _common_pb2.Color
    plastic_diagram_along_x_minus_color_four: _common_pb2.Color
    plastic_diagram_along_y_minus_color_four: _common_pb2.Color
    plastic_diagram_along_z_minus_color_four: _common_pb2.Color
    plastic_diagram_around_y_minus_color_four: _common_pb2.Color
    plastic_diagram_around_z_minus_color_four: _common_pb2.Color
    plastic_diagram_along_x_plus_color_one: _common_pb2.Color
    plastic_diagram_along_y_plus_color_one: _common_pb2.Color
    plastic_diagram_along_z_plus_color_one: _common_pb2.Color
    plastic_diagram_around_y_plus_color_one: _common_pb2.Color
    plastic_diagram_around_z_plus_color_one: _common_pb2.Color
    plastic_diagram_along_x_plus_color_two: _common_pb2.Color
    plastic_diagram_along_y_plus_color_two: _common_pb2.Color
    plastic_diagram_along_z_plus_color_two: _common_pb2.Color
    plastic_diagram_around_y_plus_color_two: _common_pb2.Color
    plastic_diagram_around_z_plus_color_two: _common_pb2.Color
    plastic_diagram_along_x_plus_color_three: _common_pb2.Color
    plastic_diagram_along_y_plus_color_three: _common_pb2.Color
    plastic_diagram_along_z_plus_color_three: _common_pb2.Color
    plastic_diagram_around_y_plus_color_three: _common_pb2.Color
    plastic_diagram_around_z_plus_color_three: _common_pb2.Color
    plastic_diagram_along_x_plus_color_four: _common_pb2.Color
    plastic_diagram_along_y_plus_color_four: _common_pb2.Color
    plastic_diagram_along_z_plus_color_four: _common_pb2.Color
    plastic_diagram_around_y_plus_color_four: _common_pb2.Color
    plastic_diagram_around_z_plus_color_four: _common_pb2.Color
    plastic_diagram_along_x_component_type: NodalReleaseType.PlasticDiagramAlongXComponentType
    plastic_diagram_along_y_component_type: NodalReleaseType.PlasticDiagramAlongYComponentType
    plastic_diagram_along_z_component_type: NodalReleaseType.PlasticDiagramAlongZComponentType
    plastic_diagram_around_y_component_type: NodalReleaseType.PlasticDiagramAroundYComponentType
    plastic_diagram_around_z_component_type: NodalReleaseType.PlasticDiagramAroundZComponentType
    plastic_diagram_along_x_color_table: NodalReleaseType.PlasticDiagramAlongXColorTable
    plastic_diagram_along_y_color_table: NodalReleaseType.PlasticDiagramAlongYColorTable
    plastic_diagram_along_z_color_table: NodalReleaseType.PlasticDiagramAlongZColorTable
    plastic_diagram_around_y_color_table: NodalReleaseType.PlasticDiagramAroundYColorTable
    plastic_diagram_around_z_color_table: NodalReleaseType.PlasticDiagramAroundZColorTable
    friction_coefficient_x: float
    friction_coefficient_xy: float
    friction_coefficient_xz: float
    friction_coefficient_y: float
    friction_coefficient_yx: float
    friction_coefficient_yz: float
    friction_coefficient_z: float
    friction_coefficient_zx: float
    friction_coefficient_zy: float
    friction_direction_independent_x: bool
    friction_direction_independent_y: bool
    friction_direction_independent_z: bool
    comment: str
    is_generated: bool
    generating_object_info: str
    generated_by_pile: bool
    local_axis_system_object_type: NodalReleaseType.LocalAxisSystemObjectType
    local_axis_system_reference_object: _object_id_pb2.ObjectId
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., nodal_releases: _Optional[_Iterable[int]] = ..., coordinate_system: _Optional[_Union[_common_pb2.CoordinateSystemRepresentation, _Mapping]] = ..., axial_release_n: _Optional[float] = ..., axial_release_vy: _Optional[float] = ..., axial_release_vz: _Optional[float] = ..., moment_release_mt: _Optional[float] = ..., moment_release_my: _Optional[float] = ..., moment_release_mz: _Optional[float] = ..., axial_release_n_nonlinearity: _Optional[_Union[NodalReleaseType.AxialReleaseNNonlinearity, str]] = ..., axial_release_vy_nonlinearity: _Optional[_Union[NodalReleaseType.AxialReleaseVyNonlinearity, str]] = ..., axial_release_vz_nonlinearity: _Optional[_Union[NodalReleaseType.AxialReleaseVzNonlinearity, str]] = ..., moment_release_mt_nonlinearity: _Optional[_Union[NodalReleaseType.MomentReleaseMtNonlinearity, str]] = ..., moment_release_my_nonlinearity: _Optional[_Union[NodalReleaseType.MomentReleaseMyNonlinearity, str]] = ..., moment_release_mz_nonlinearity: _Optional[_Union[NodalReleaseType.MomentReleaseMzNonlinearity, str]] = ..., partial_activity_along_x_negative_type: _Optional[_Union[NodalReleaseType.PartialActivityAlongXNegativeType, str]] = ..., partial_activity_along_x_positive_type: _Optional[_Union[NodalReleaseType.PartialActivityAlongXPositiveType, str]] = ..., partial_activity_along_y_negative_type: _Optional[_Union[NodalReleaseType.PartialActivityAlongYNegativeType, str]] = ..., partial_activity_along_y_positive_type: _Optional[_Union[NodalReleaseType.PartialActivityAlongYPositiveType, str]] = ..., partial_activity_along_z_negative_type: _Optional[_Union[NodalReleaseType.PartialActivityAlongZNegativeType, str]] = ..., partial_activity_along_z_positive_type: _Optional[_Union[NodalReleaseType.PartialActivityAlongZPositiveType, str]] = ..., partial_activity_around_x_negative_type: _Optional[_Union[NodalReleaseType.PartialActivityAroundXNegativeType, str]] = ..., partial_activity_around_x_positive_type: _Optional[_Union[NodalReleaseType.PartialActivityAroundXPositiveType, str]] = ..., partial_activity_around_y_negative_type: _Optional[_Union[NodalReleaseType.PartialActivityAroundYNegativeType, str]] = ..., partial_activity_around_y_positive_type: _Optional[_Union[NodalReleaseType.PartialActivityAroundYPositiveType, str]] = ..., partial_activity_around_z_negative_type: _Optional[_Union[NodalReleaseType.PartialActivityAroundZNegativeType, str]] = ..., partial_activity_around_z_positive_type: _Optional[_Union[NodalReleaseType.PartialActivityAroundZPositiveType, str]] = ..., partial_activity_along_x_negative_displacement: _Optional[float] = ..., partial_activity_along_x_positive_displacement: _Optional[float] = ..., partial_activity_along_y_negative_displacement: _Optional[float] = ..., partial_activity_along_y_positive_displacement: _Optional[float] = ..., partial_activity_along_z_negative_displacement: _Optional[float] = ..., partial_activity_along_z_positive_displacement: _Optional[float] = ..., partial_activity_around_x_negative_rotation: _Optional[float] = ..., partial_activity_around_x_positive_rotation: _Optional[float] = ..., partial_activity_around_y_negative_rotation: _Optional[float] = ..., partial_activity_around_y_positive_rotation: _Optional[float] = ..., partial_activity_around_z_negative_rotation: _Optional[float] = ..., partial_activity_around_z_positive_rotation: _Optional[float] = ..., partial_activity_along_x_negative_force: _Optional[float] = ..., partial_activity_along_x_positive_force: _Optional[float] = ..., partial_activity_along_y_negative_force: _Optional[float] = ..., partial_activity_along_y_positive_force: _Optional[float] = ..., partial_activity_along_z_negative_force: _Optional[float] = ..., partial_activity_along_z_positive_force: _Optional[float] = ..., partial_activity_around_x_negative_moment: _Optional[float] = ..., partial_activity_around_x_positive_moment: _Optional[float] = ..., partial_activity_around_y_negative_moment: _Optional[float] = ..., partial_activity_around_y_positive_moment: _Optional[float] = ..., partial_activity_around_z_negative_moment: _Optional[float] = ..., partial_activity_around_z_positive_moment: _Optional[float] = ..., partial_activity_along_x_negative_slippage: _Optional[float] = ..., partial_activity_along_x_positive_slippage: _Optional[float] = ..., partial_activity_along_y_negative_slippage: _Optional[float] = ..., partial_activity_along_y_positive_slippage: _Optional[float] = ..., partial_activity_along_z_negative_slippage: _Optional[float] = ..., partial_activity_along_z_positive_slippage: _Optional[float] = ..., partial_activity_around_x_negative_slippage: _Optional[float] = ..., partial_activity_around_x_positive_slippage: _Optional[float] = ..., partial_activity_around_y_negative_slippage: _Optional[float] = ..., partial_activity_around_y_positive_slippage: _Optional[float] = ..., partial_activity_around_z_negative_slippage: _Optional[float] = ..., partial_activity_around_z_positive_slippage: _Optional[float] = ..., diagram_along_x_symmetric: bool = ..., diagram_along_y_symmetric: bool = ..., diagram_along_z_symmetric: bool = ..., diagram_around_x_symmetric: bool = ..., diagram_around_y_symmetric: bool = ..., diagram_around_z_symmetric: bool = ..., diagram_along_x_is_sorted: bool = ..., diagram_along_y_is_sorted: bool = ..., diagram_along_z_is_sorted: bool = ..., diagram_around_x_is_sorted: bool = ..., diagram_around_y_is_sorted: bool = ..., diagram_around_z_is_sorted: bool = ..., diagram_along_x_start: _Optional[_Union[NodalReleaseType.DiagramAlongXStart, str]] = ..., diagram_along_y_start: _Optional[_Union[NodalReleaseType.DiagramAlongYStart, str]] = ..., diagram_along_z_start: _Optional[_Union[NodalReleaseType.DiagramAlongZStart, str]] = ..., diagram_around_x_start: _Optional[_Union[NodalReleaseType.DiagramAroundXStart, str]] = ..., diagram_around_y_start: _Optional[_Union[NodalReleaseType.DiagramAroundYStart, str]] = ..., diagram_around_z_start: _Optional[_Union[NodalReleaseType.DiagramAroundZStart, str]] = ..., diagram_along_x_end: _Optional[_Union[NodalReleaseType.DiagramAlongXEnd, str]] = ..., diagram_along_y_end: _Optional[_Union[NodalReleaseType.DiagramAlongYEnd, str]] = ..., diagram_along_z_end: _Optional[_Union[NodalReleaseType.DiagramAlongZEnd, str]] = ..., diagram_around_x_end: _Optional[_Union[NodalReleaseType.DiagramAroundXEnd, str]] = ..., diagram_around_y_end: _Optional[_Union[NodalReleaseType.DiagramAroundYEnd, str]] = ..., diagram_around_z_end: _Optional[_Union[NodalReleaseType.DiagramAroundZEnd, str]] = ..., diagram_along_x_table: _Optional[_Union[NodalReleaseType.DiagramAlongXTable, _Mapping]] = ..., diagram_along_y_table: _Optional[_Union[NodalReleaseType.DiagramAlongYTable, _Mapping]] = ..., diagram_along_z_table: _Optional[_Union[NodalReleaseType.DiagramAlongZTable, _Mapping]] = ..., diagram_around_x_table: _Optional[_Union[NodalReleaseType.DiagramAroundXTable, _Mapping]] = ..., diagram_around_y_table: _Optional[_Union[NodalReleaseType.DiagramAroundYTable, _Mapping]] = ..., diagram_around_z_table: _Optional[_Union[NodalReleaseType.DiagramAroundZTable, _Mapping]] = ..., diagram_along_x_ac_yield_minus: _Optional[float] = ..., diagram_along_y_ac_yield_minus: _Optional[float] = ..., diagram_along_z_ac_yield_minus: _Optional[float] = ..., diagram_around_x_ac_yield_minus: _Optional[float] = ..., diagram_around_y_ac_yield_minus: _Optional[float] = ..., diagram_around_z_ac_yield_minus: _Optional[float] = ..., diagram_along_x_ac_yield_plus: _Optional[float] = ..., diagram_along_y_ac_yield_plus: _Optional[float] = ..., diagram_along_z_ac_yield_plus: _Optional[float] = ..., diagram_around_x_ac_yield_plus: _Optional[float] = ..., diagram_around_y_ac_yield_plus: _Optional[float] = ..., diagram_around_z_ac_yield_plus: _Optional[float] = ..., diagram_along_x_acceptance_criteria_active: bool = ..., diagram_along_y_acceptance_criteria_active: bool = ..., diagram_along_z_acceptance_criteria_active: bool = ..., diagram_around_x_acceptance_criteria_active: bool = ..., diagram_around_y_acceptance_criteria_active: bool = ..., diagram_around_z_acceptance_criteria_active: bool = ..., diagram_along_x_minus_color_one: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., diagram_along_y_minus_color_one: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., diagram_along_z_minus_color_one: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., diagram_around_x_minus_color_one: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., diagram_around_y_minus_color_one: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., diagram_around_z_minus_color_one: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., diagram_along_x_minus_color_two: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., diagram_along_y_minus_color_two: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., diagram_along_z_minus_color_two: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., diagram_around_x_minus_color_two: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., diagram_around_y_minus_color_two: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., diagram_around_z_minus_color_two: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., diagram_along_x_plus_color_one: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., diagram_along_y_plus_color_one: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., diagram_along_z_plus_color_one: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., diagram_around_x_plus_color_one: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., diagram_around_y_plus_color_one: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., diagram_around_z_plus_color_one: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., diagram_along_x_plus_color_two: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., diagram_along_y_plus_color_two: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., diagram_along_z_plus_color_two: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., diagram_around_x_plus_color_two: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., diagram_around_y_plus_color_two: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., diagram_around_z_plus_color_two: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., diagram_along_x_color_table: _Optional[_Union[NodalReleaseType.DiagramAlongXColorTable, _Mapping]] = ..., diagram_along_y_color_table: _Optional[_Union[NodalReleaseType.DiagramAlongYColorTable, _Mapping]] = ..., diagram_along_z_color_table: _Optional[_Union[NodalReleaseType.DiagramAlongZColorTable, _Mapping]] = ..., diagram_around_x_color_table: _Optional[_Union[NodalReleaseType.DiagramAroundXColorTable, _Mapping]] = ..., diagram_around_y_color_table: _Optional[_Union[NodalReleaseType.DiagramAroundYColorTable, _Mapping]] = ..., diagram_around_z_color_table: _Optional[_Union[NodalReleaseType.DiagramAroundZColorTable, _Mapping]] = ..., plastic_diagram_along_x_table: _Optional[_Union[NodalReleaseType.PlasticDiagramAlongXTable, _Mapping]] = ..., plastic_diagram_along_y_table: _Optional[_Union[NodalReleaseType.PlasticDiagramAlongYTable, _Mapping]] = ..., plastic_diagram_along_z_table: _Optional[_Union[NodalReleaseType.PlasticDiagramAlongZTable, _Mapping]] = ..., plastic_diagram_around_y_table: _Optional[_Union[NodalReleaseType.PlasticDiagramAroundYTable, _Mapping]] = ..., plastic_diagram_around_z_table: _Optional[_Union[NodalReleaseType.PlasticDiagramAroundZTable, _Mapping]] = ..., plastic_diagram_along_x_symmetric: bool = ..., plastic_diagram_along_y_symmetric: bool = ..., plastic_diagram_along_z_symmetric: bool = ..., plastic_diagram_around_y_symmetric: bool = ..., plastic_diagram_around_z_symmetric: bool = ..., plastic_diagram_around_y_force_interaction: bool = ..., plastic_diagram_around_z_force_interaction: bool = ..., plastic_diagram_along_x_user_defined: bool = ..., plastic_diagram_along_y_user_defined: bool = ..., plastic_diagram_along_z_user_defined: bool = ..., plastic_diagram_around_y_user_defined: bool = ..., plastic_diagram_around_z_user_defined: bool = ..., plastic_diagram_along_x_is_user_defined_member_length: bool = ..., plastic_diagram_along_y_is_user_defined_member_length: bool = ..., plastic_diagram_along_z_is_user_defined_member_length: bool = ..., plastic_diagram_around_y_is_user_defined_member_length: bool = ..., plastic_diagram_around_z_is_user_defined_member_length: bool = ..., plastic_diagram_along_x_user_defined_member_length: _Optional[float] = ..., plastic_diagram_along_y_user_defined_member_length: _Optional[float] = ..., plastic_diagram_along_z_user_defined_member_length: _Optional[float] = ..., plastic_diagram_around_y_user_defined_member_length: _Optional[float] = ..., plastic_diagram_around_z_user_defined_member_length: _Optional[float] = ..., plastic_diagram_along_x_attached_members_min_max_length: _Optional[str] = ..., plastic_diagram_along_y_attached_members_min_max_length: _Optional[str] = ..., plastic_diagram_along_z_attached_members_min_max_length: _Optional[str] = ..., plastic_diagram_around_y_attached_members_min_max_length: _Optional[str] = ..., plastic_diagram_around_z_attached_members_min_max_length: _Optional[str] = ..., plastic_diagram_along_x_io_negative: _Optional[float] = ..., plastic_diagram_along_y_io_negative: _Optional[float] = ..., plastic_diagram_along_z_io_negative: _Optional[float] = ..., plastic_diagram_around_y_io_negative: _Optional[float] = ..., plastic_diagram_around_z_io_negative: _Optional[float] = ..., plastic_diagram_along_x_io_positive: _Optional[float] = ..., plastic_diagram_along_y_io_positive: _Optional[float] = ..., plastic_diagram_along_z_io_positive: _Optional[float] = ..., plastic_diagram_around_y_io_positive: _Optional[float] = ..., plastic_diagram_around_z_io_positive: _Optional[float] = ..., plastic_diagram_along_x_ls_negative: _Optional[float] = ..., plastic_diagram_along_y_ls_negative: _Optional[float] = ..., plastic_diagram_along_z_ls_negative: _Optional[float] = ..., plastic_diagram_around_y_ls_negative: _Optional[float] = ..., plastic_diagram_around_z_ls_negative: _Optional[float] = ..., plastic_diagram_along_x_ls_positive: _Optional[float] = ..., plastic_diagram_along_y_ls_positive: _Optional[float] = ..., plastic_diagram_along_z_ls_positive: _Optional[float] = ..., plastic_diagram_around_y_ls_positive: _Optional[float] = ..., plastic_diagram_around_z_ls_positive: _Optional[float] = ..., plastic_diagram_along_x_cp_negative: _Optional[float] = ..., plastic_diagram_along_y_cp_negative: _Optional[float] = ..., plastic_diagram_along_z_cp_negative: _Optional[float] = ..., plastic_diagram_around_y_cp_negative: _Optional[float] = ..., plastic_diagram_around_z_cp_negative: _Optional[float] = ..., plastic_diagram_along_x_cp_positive: _Optional[float] = ..., plastic_diagram_along_y_cp_positive: _Optional[float] = ..., plastic_diagram_along_z_cp_positive: _Optional[float] = ..., plastic_diagram_around_y_cp_positive: _Optional[float] = ..., plastic_diagram_around_z_cp_positive: _Optional[float] = ..., plastic_diagram_along_x_minus_color_one: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_along_y_minus_color_one: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_along_z_minus_color_one: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_around_y_minus_color_one: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_around_z_minus_color_one: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_along_x_minus_color_two: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_along_y_minus_color_two: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_along_z_minus_color_two: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_around_y_minus_color_two: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_around_z_minus_color_two: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_along_x_minus_color_three: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_along_y_minus_color_three: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_along_z_minus_color_three: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_around_y_minus_color_three: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_around_z_minus_color_three: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_along_x_minus_color_four: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_along_y_minus_color_four: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_along_z_minus_color_four: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_around_y_minus_color_four: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_around_z_minus_color_four: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_along_x_plus_color_one: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_along_y_plus_color_one: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_along_z_plus_color_one: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_around_y_plus_color_one: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_around_z_plus_color_one: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_along_x_plus_color_two: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_along_y_plus_color_two: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_along_z_plus_color_two: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_around_y_plus_color_two: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_around_z_plus_color_two: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_along_x_plus_color_three: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_along_y_plus_color_three: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_along_z_plus_color_three: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_around_y_plus_color_three: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_around_z_plus_color_three: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_along_x_plus_color_four: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_along_y_plus_color_four: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_along_z_plus_color_four: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_around_y_plus_color_four: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_around_z_plus_color_four: _Optional[_Union[_common_pb2.Color, _Mapping]] = ..., plastic_diagram_along_x_component_type: _Optional[_Union[NodalReleaseType.PlasticDiagramAlongXComponentType, str]] = ..., plastic_diagram_along_y_component_type: _Optional[_Union[NodalReleaseType.PlasticDiagramAlongYComponentType, str]] = ..., plastic_diagram_along_z_component_type: _Optional[_Union[NodalReleaseType.PlasticDiagramAlongZComponentType, str]] = ..., plastic_diagram_around_y_component_type: _Optional[_Union[NodalReleaseType.PlasticDiagramAroundYComponentType, str]] = ..., plastic_diagram_around_z_component_type: _Optional[_Union[NodalReleaseType.PlasticDiagramAroundZComponentType, str]] = ..., plastic_diagram_along_x_color_table: _Optional[_Union[NodalReleaseType.PlasticDiagramAlongXColorTable, _Mapping]] = ..., plastic_diagram_along_y_color_table: _Optional[_Union[NodalReleaseType.PlasticDiagramAlongYColorTable, _Mapping]] = ..., plastic_diagram_along_z_color_table: _Optional[_Union[NodalReleaseType.PlasticDiagramAlongZColorTable, _Mapping]] = ..., plastic_diagram_around_y_color_table: _Optional[_Union[NodalReleaseType.PlasticDiagramAroundYColorTable, _Mapping]] = ..., plastic_diagram_around_z_color_table: _Optional[_Union[NodalReleaseType.PlasticDiagramAroundZColorTable, _Mapping]] = ..., friction_coefficient_x: _Optional[float] = ..., friction_coefficient_xy: _Optional[float] = ..., friction_coefficient_xz: _Optional[float] = ..., friction_coefficient_y: _Optional[float] = ..., friction_coefficient_yx: _Optional[float] = ..., friction_coefficient_yz: _Optional[float] = ..., friction_coefficient_z: _Optional[float] = ..., friction_coefficient_zx: _Optional[float] = ..., friction_coefficient_zy: _Optional[float] = ..., friction_direction_independent_x: bool = ..., friction_direction_independent_y: bool = ..., friction_direction_independent_z: bool = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., generated_by_pile: bool = ..., local_axis_system_object_type: _Optional[_Union[NodalReleaseType.LocalAxisSystemObjectType, str]] = ..., local_axis_system_reference_object: _Optional[_Union[_object_id_pb2.ObjectId, _Mapping]] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
