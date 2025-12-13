from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DesignSupport(_message.Message):
    __slots__ = ("no", "type", "user_defined_name_enabled", "name", "assigned_to_members", "assigned_to_member_sets", "assigned_to_nodes", "assigned_to_objects", "support_width_z", "support_depth_z", "support_width_y", "support_depth_y", "support_depth_by_section_width_of_member_z_enabled", "support_depth_by_section_width_of_member_y_enabled", "design_support_orientation_z", "design_support_orientation_y", "direct_support_z_enabled", "direct_support_y_enabled", "activate_in_z", "activate_in_y", "consider_in_deflection_design_z", "consider_in_deflection_design_y", "concrete_monolithic_connection_z_enabled", "inner_support_z_enabled", "inner_support_y_enabled", "concrete_ratio_of_moment_redistribution_z", "timber_reinforcement_elements_z_enabled", "timber_reinforcement_elements_y_enabled", "timber_reinforcement_elements_type_z", "timber_reinforcement_elements_type_y", "timber_reinforcement_parameters_specification_type_z", "timber_reinforcement_parameters_specification_type_y", "timber_screw_z", "timber_screw_y", "timber_withdrawal_strength_of_one_screw_z", "timber_withdrawal_strength_of_one_screw_y", "timber_buckling_strength_of_one_screw_z", "timber_buckling_strength_of_one_screw_y", "timber_load_distribution_z", "timber_load_distribution_y", "timber_screw_length_z", "timber_screw_length_y", "timber_thread_length_z", "timber_thread_length_y", "timber_number_of_screws_in_grain_direction_z", "timber_number_of_screws_in_grain_direction_y", "timber_number_of_screws_perpendicular_to_grain_direction_z", "timber_number_of_screws_perpendicular_to_grain_direction_y", "timber_spacing_of_screws_in_grain_direction_z", "timber_spacing_of_screws_in_grain_direction_y", "timber_spacing_of_rows_perpendicular_to_grain_directionz", "timber_spacing_of_rows_perpendicular_to_grain_directiony", "timber_check_critical_bearing_z_enabled", "timber_check_critical_bearing_y_enabled", "timber_calculation_method_z", "timber_calculation_method_y", "timber_compression_design_value_z", "timber_compression_design_value_y", "timber_allow_higher_deformation_z_enabled", "timber_allow_higher_deformation_y_enabled", "timber_factor_of_compression_z", "timber_factor_of_compression_y", "limit_of_high_bending_stresses_z", "limit_of_high_bending_stresses_y", "consider_in_fire_design_z", "consider_in_fire_design_y", "timber_shear_force_reduction_z", "timber_shear_force_reduction_y", "end_support_z_enabled", "overhang_length_z", "fastened_to_support_z_enabled", "comment", "is_generated", "generating_object_info", "id_for_export_import", "metadata_for_export_import")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TYPE_UNKNOWN: _ClassVar[DesignSupport.Type]
        TYPE_ALUMINUM: _ClassVar[DesignSupport.Type]
        TYPE_CONCRETE: _ClassVar[DesignSupport.Type]
        TYPE_GENERAL: _ClassVar[DesignSupport.Type]
        TYPE_STEEL: _ClassVar[DesignSupport.Type]
        TYPE_TIMBER: _ClassVar[DesignSupport.Type]
    TYPE_UNKNOWN: DesignSupport.Type
    TYPE_ALUMINUM: DesignSupport.Type
    TYPE_CONCRETE: DesignSupport.Type
    TYPE_GENERAL: DesignSupport.Type
    TYPE_STEEL: DesignSupport.Type
    TYPE_TIMBER: DesignSupport.Type
    class DesignSupportOrientationZ(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DESIGN_SUPPORT_ORIENTATION_Z_POSITIVE: _ClassVar[DesignSupport.DesignSupportOrientationZ]
        DESIGN_SUPPORT_ORIENTATION_Z_BOTH: _ClassVar[DesignSupport.DesignSupportOrientationZ]
        DESIGN_SUPPORT_ORIENTATION_Z_NEGATIVE: _ClassVar[DesignSupport.DesignSupportOrientationZ]
    DESIGN_SUPPORT_ORIENTATION_Z_POSITIVE: DesignSupport.DesignSupportOrientationZ
    DESIGN_SUPPORT_ORIENTATION_Z_BOTH: DesignSupport.DesignSupportOrientationZ
    DESIGN_SUPPORT_ORIENTATION_Z_NEGATIVE: DesignSupport.DesignSupportOrientationZ
    class DesignSupportOrientationY(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DESIGN_SUPPORT_ORIENTATION_Y_POSITIVE: _ClassVar[DesignSupport.DesignSupportOrientationY]
        DESIGN_SUPPORT_ORIENTATION_Y_BOTH: _ClassVar[DesignSupport.DesignSupportOrientationY]
        DESIGN_SUPPORT_ORIENTATION_Y_NEGATIVE: _ClassVar[DesignSupport.DesignSupportOrientationY]
    DESIGN_SUPPORT_ORIENTATION_Y_POSITIVE: DesignSupport.DesignSupportOrientationY
    DESIGN_SUPPORT_ORIENTATION_Y_BOTH: DesignSupport.DesignSupportOrientationY
    DESIGN_SUPPORT_ORIENTATION_Y_NEGATIVE: DesignSupport.DesignSupportOrientationY
    class TimberReinforcementElementsTypeZ(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TIMBER_REINFORCEMENT_ELEMENTS_TYPE_Z_SCREWS: _ClassVar[DesignSupport.TimberReinforcementElementsTypeZ]
    TIMBER_REINFORCEMENT_ELEMENTS_TYPE_Z_SCREWS: DesignSupport.TimberReinforcementElementsTypeZ
    class TimberReinforcementElementsTypeY(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TIMBER_REINFORCEMENT_ELEMENTS_TYPE_Y_SCREWS: _ClassVar[DesignSupport.TimberReinforcementElementsTypeY]
    TIMBER_REINFORCEMENT_ELEMENTS_TYPE_Y_SCREWS: DesignSupport.TimberReinforcementElementsTypeY
    class TimberReinforcementParametersSpecificationTypeZ(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TIMBER_REINFORCEMENT_PARAMETERS_SPECIFICATION_TYPE_Z_USER_DEFINED_STRENGTHS: _ClassVar[DesignSupport.TimberReinforcementParametersSpecificationTypeZ]
        TIMBER_REINFORCEMENT_PARAMETERS_SPECIFICATION_TYPE_Z_ACC_TO_REINFORCEMENT_ELEMENT: _ClassVar[DesignSupport.TimberReinforcementParametersSpecificationTypeZ]
    TIMBER_REINFORCEMENT_PARAMETERS_SPECIFICATION_TYPE_Z_USER_DEFINED_STRENGTHS: DesignSupport.TimberReinforcementParametersSpecificationTypeZ
    TIMBER_REINFORCEMENT_PARAMETERS_SPECIFICATION_TYPE_Z_ACC_TO_REINFORCEMENT_ELEMENT: DesignSupport.TimberReinforcementParametersSpecificationTypeZ
    class TimberReinforcementParametersSpecificationTypeY(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TIMBER_REINFORCEMENT_PARAMETERS_SPECIFICATION_TYPE_Y_USER_DEFINED_STRENGTHS: _ClassVar[DesignSupport.TimberReinforcementParametersSpecificationTypeY]
        TIMBER_REINFORCEMENT_PARAMETERS_SPECIFICATION_TYPE_Y_ACC_TO_REINFORCEMENT_ELEMENT: _ClassVar[DesignSupport.TimberReinforcementParametersSpecificationTypeY]
    TIMBER_REINFORCEMENT_PARAMETERS_SPECIFICATION_TYPE_Y_USER_DEFINED_STRENGTHS: DesignSupport.TimberReinforcementParametersSpecificationTypeY
    TIMBER_REINFORCEMENT_PARAMETERS_SPECIFICATION_TYPE_Y_ACC_TO_REINFORCEMENT_ELEMENT: DesignSupport.TimberReinforcementParametersSpecificationTypeY
    class TimberLoadDistributionZ(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TIMBER_LOAD_DISTRIBUTION_Z_LINEAR_45_DEGREES: _ClassVar[DesignSupport.TimberLoadDistributionZ]
        TIMBER_LOAD_DISTRIBUTION_Z_NONLINEAR: _ClassVar[DesignSupport.TimberLoadDistributionZ]
    TIMBER_LOAD_DISTRIBUTION_Z_LINEAR_45_DEGREES: DesignSupport.TimberLoadDistributionZ
    TIMBER_LOAD_DISTRIBUTION_Z_NONLINEAR: DesignSupport.TimberLoadDistributionZ
    class TimberLoadDistributionY(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TIMBER_LOAD_DISTRIBUTION_Y_LINEAR_45_DEGREES: _ClassVar[DesignSupport.TimberLoadDistributionY]
        TIMBER_LOAD_DISTRIBUTION_Y_NONLINEAR: _ClassVar[DesignSupport.TimberLoadDistributionY]
    TIMBER_LOAD_DISTRIBUTION_Y_LINEAR_45_DEGREES: DesignSupport.TimberLoadDistributionY
    TIMBER_LOAD_DISTRIBUTION_Y_NONLINEAR: DesignSupport.TimberLoadDistributionY
    class TimberCalculationMethodZ(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TIMBER_CALCULATION_METHOD_Z_ACC_TO_4_2_2_2: _ClassVar[DesignSupport.TimberCalculationMethodZ]
        TIMBER_CALCULATION_METHOD_Z_ACC_TO_ANNEX_C: _ClassVar[DesignSupport.TimberCalculationMethodZ]
    TIMBER_CALCULATION_METHOD_Z_ACC_TO_4_2_2_2: DesignSupport.TimberCalculationMethodZ
    TIMBER_CALCULATION_METHOD_Z_ACC_TO_ANNEX_C: DesignSupport.TimberCalculationMethodZ
    class TimberCalculationMethodY(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TIMBER_CALCULATION_METHOD_Y_ACC_TO_4_2_2_2: _ClassVar[DesignSupport.TimberCalculationMethodY]
        TIMBER_CALCULATION_METHOD_Y_ACC_TO_ANNEX_C: _ClassVar[DesignSupport.TimberCalculationMethodY]
    TIMBER_CALCULATION_METHOD_Y_ACC_TO_4_2_2_2: DesignSupport.TimberCalculationMethodY
    TIMBER_CALCULATION_METHOD_Y_ACC_TO_ANNEX_C: DesignSupport.TimberCalculationMethodY
    class TimberCompressionDesignValueZ(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TIMBER_COMPRESSION_DESIGN_VALUE_Z_0_0_4: _ClassVar[DesignSupport.TimberCompressionDesignValueZ]
        TIMBER_COMPRESSION_DESIGN_VALUE_Z_0_0_2: _ClassVar[DesignSupport.TimberCompressionDesignValueZ]
    TIMBER_COMPRESSION_DESIGN_VALUE_Z_0_0_4: DesignSupport.TimberCompressionDesignValueZ
    TIMBER_COMPRESSION_DESIGN_VALUE_Z_0_0_2: DesignSupport.TimberCompressionDesignValueZ
    class TimberCompressionDesignValueY(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TIMBER_COMPRESSION_DESIGN_VALUE_Y_0_0_4: _ClassVar[DesignSupport.TimberCompressionDesignValueY]
        TIMBER_COMPRESSION_DESIGN_VALUE_Y_0_0_2: _ClassVar[DesignSupport.TimberCompressionDesignValueY]
    TIMBER_COMPRESSION_DESIGN_VALUE_Y_0_0_4: DesignSupport.TimberCompressionDesignValueY
    TIMBER_COMPRESSION_DESIGN_VALUE_Y_0_0_2: DesignSupport.TimberCompressionDesignValueY
    NO_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_MEMBER_SETS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_NODES_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_OBJECTS_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_WIDTH_Z_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_DEPTH_Z_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_WIDTH_Y_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_DEPTH_Y_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_DEPTH_BY_SECTION_WIDTH_OF_MEMBER_Z_ENABLED_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_DEPTH_BY_SECTION_WIDTH_OF_MEMBER_Y_ENABLED_FIELD_NUMBER: _ClassVar[int]
    DESIGN_SUPPORT_ORIENTATION_Z_FIELD_NUMBER: _ClassVar[int]
    DESIGN_SUPPORT_ORIENTATION_Y_FIELD_NUMBER: _ClassVar[int]
    DIRECT_SUPPORT_Z_ENABLED_FIELD_NUMBER: _ClassVar[int]
    DIRECT_SUPPORT_Y_ENABLED_FIELD_NUMBER: _ClassVar[int]
    ACTIVATE_IN_Z_FIELD_NUMBER: _ClassVar[int]
    ACTIVATE_IN_Y_FIELD_NUMBER: _ClassVar[int]
    CONSIDER_IN_DEFLECTION_DESIGN_Z_FIELD_NUMBER: _ClassVar[int]
    CONSIDER_IN_DEFLECTION_DESIGN_Y_FIELD_NUMBER: _ClassVar[int]
    CONCRETE_MONOLITHIC_CONNECTION_Z_ENABLED_FIELD_NUMBER: _ClassVar[int]
    INNER_SUPPORT_Z_ENABLED_FIELD_NUMBER: _ClassVar[int]
    INNER_SUPPORT_Y_ENABLED_FIELD_NUMBER: _ClassVar[int]
    CONCRETE_RATIO_OF_MOMENT_REDISTRIBUTION_Z_FIELD_NUMBER: _ClassVar[int]
    TIMBER_REINFORCEMENT_ELEMENTS_Z_ENABLED_FIELD_NUMBER: _ClassVar[int]
    TIMBER_REINFORCEMENT_ELEMENTS_Y_ENABLED_FIELD_NUMBER: _ClassVar[int]
    TIMBER_REINFORCEMENT_ELEMENTS_TYPE_Z_FIELD_NUMBER: _ClassVar[int]
    TIMBER_REINFORCEMENT_ELEMENTS_TYPE_Y_FIELD_NUMBER: _ClassVar[int]
    TIMBER_REINFORCEMENT_PARAMETERS_SPECIFICATION_TYPE_Z_FIELD_NUMBER: _ClassVar[int]
    TIMBER_REINFORCEMENT_PARAMETERS_SPECIFICATION_TYPE_Y_FIELD_NUMBER: _ClassVar[int]
    TIMBER_SCREW_Z_FIELD_NUMBER: _ClassVar[int]
    TIMBER_SCREW_Y_FIELD_NUMBER: _ClassVar[int]
    TIMBER_WITHDRAWAL_STRENGTH_OF_ONE_SCREW_Z_FIELD_NUMBER: _ClassVar[int]
    TIMBER_WITHDRAWAL_STRENGTH_OF_ONE_SCREW_Y_FIELD_NUMBER: _ClassVar[int]
    TIMBER_BUCKLING_STRENGTH_OF_ONE_SCREW_Z_FIELD_NUMBER: _ClassVar[int]
    TIMBER_BUCKLING_STRENGTH_OF_ONE_SCREW_Y_FIELD_NUMBER: _ClassVar[int]
    TIMBER_LOAD_DISTRIBUTION_Z_FIELD_NUMBER: _ClassVar[int]
    TIMBER_LOAD_DISTRIBUTION_Y_FIELD_NUMBER: _ClassVar[int]
    TIMBER_SCREW_LENGTH_Z_FIELD_NUMBER: _ClassVar[int]
    TIMBER_SCREW_LENGTH_Y_FIELD_NUMBER: _ClassVar[int]
    TIMBER_THREAD_LENGTH_Z_FIELD_NUMBER: _ClassVar[int]
    TIMBER_THREAD_LENGTH_Y_FIELD_NUMBER: _ClassVar[int]
    TIMBER_NUMBER_OF_SCREWS_IN_GRAIN_DIRECTION_Z_FIELD_NUMBER: _ClassVar[int]
    TIMBER_NUMBER_OF_SCREWS_IN_GRAIN_DIRECTION_Y_FIELD_NUMBER: _ClassVar[int]
    TIMBER_NUMBER_OF_SCREWS_PERPENDICULAR_TO_GRAIN_DIRECTION_Z_FIELD_NUMBER: _ClassVar[int]
    TIMBER_NUMBER_OF_SCREWS_PERPENDICULAR_TO_GRAIN_DIRECTION_Y_FIELD_NUMBER: _ClassVar[int]
    TIMBER_SPACING_OF_SCREWS_IN_GRAIN_DIRECTION_Z_FIELD_NUMBER: _ClassVar[int]
    TIMBER_SPACING_OF_SCREWS_IN_GRAIN_DIRECTION_Y_FIELD_NUMBER: _ClassVar[int]
    TIMBER_SPACING_OF_ROWS_PERPENDICULAR_TO_GRAIN_DIRECTIONZ_FIELD_NUMBER: _ClassVar[int]
    TIMBER_SPACING_OF_ROWS_PERPENDICULAR_TO_GRAIN_DIRECTIONY_FIELD_NUMBER: _ClassVar[int]
    TIMBER_CHECK_CRITICAL_BEARING_Z_ENABLED_FIELD_NUMBER: _ClassVar[int]
    TIMBER_CHECK_CRITICAL_BEARING_Y_ENABLED_FIELD_NUMBER: _ClassVar[int]
    TIMBER_CALCULATION_METHOD_Z_FIELD_NUMBER: _ClassVar[int]
    TIMBER_CALCULATION_METHOD_Y_FIELD_NUMBER: _ClassVar[int]
    TIMBER_COMPRESSION_DESIGN_VALUE_Z_FIELD_NUMBER: _ClassVar[int]
    TIMBER_COMPRESSION_DESIGN_VALUE_Y_FIELD_NUMBER: _ClassVar[int]
    TIMBER_ALLOW_HIGHER_DEFORMATION_Z_ENABLED_FIELD_NUMBER: _ClassVar[int]
    TIMBER_ALLOW_HIGHER_DEFORMATION_Y_ENABLED_FIELD_NUMBER: _ClassVar[int]
    TIMBER_FACTOR_OF_COMPRESSION_Z_FIELD_NUMBER: _ClassVar[int]
    TIMBER_FACTOR_OF_COMPRESSION_Y_FIELD_NUMBER: _ClassVar[int]
    LIMIT_OF_HIGH_BENDING_STRESSES_Z_FIELD_NUMBER: _ClassVar[int]
    LIMIT_OF_HIGH_BENDING_STRESSES_Y_FIELD_NUMBER: _ClassVar[int]
    CONSIDER_IN_FIRE_DESIGN_Z_FIELD_NUMBER: _ClassVar[int]
    CONSIDER_IN_FIRE_DESIGN_Y_FIELD_NUMBER: _ClassVar[int]
    TIMBER_SHEAR_FORCE_REDUCTION_Z_FIELD_NUMBER: _ClassVar[int]
    TIMBER_SHEAR_FORCE_REDUCTION_Y_FIELD_NUMBER: _ClassVar[int]
    END_SUPPORT_Z_ENABLED_FIELD_NUMBER: _ClassVar[int]
    OVERHANG_LENGTH_Z_FIELD_NUMBER: _ClassVar[int]
    FASTENED_TO_SUPPORT_Z_ENABLED_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    type: DesignSupport.Type
    user_defined_name_enabled: bool
    name: str
    assigned_to_members: _containers.RepeatedScalarFieldContainer[int]
    assigned_to_member_sets: _containers.RepeatedScalarFieldContainer[int]
    assigned_to_nodes: _containers.RepeatedScalarFieldContainer[int]
    assigned_to_objects: str
    support_width_z: float
    support_depth_z: float
    support_width_y: float
    support_depth_y: float
    support_depth_by_section_width_of_member_z_enabled: bool
    support_depth_by_section_width_of_member_y_enabled: bool
    design_support_orientation_z: DesignSupport.DesignSupportOrientationZ
    design_support_orientation_y: DesignSupport.DesignSupportOrientationY
    direct_support_z_enabled: bool
    direct_support_y_enabled: bool
    activate_in_z: bool
    activate_in_y: bool
    consider_in_deflection_design_z: bool
    consider_in_deflection_design_y: bool
    concrete_monolithic_connection_z_enabled: bool
    inner_support_z_enabled: bool
    inner_support_y_enabled: bool
    concrete_ratio_of_moment_redistribution_z: float
    timber_reinforcement_elements_z_enabled: bool
    timber_reinforcement_elements_y_enabled: bool
    timber_reinforcement_elements_type_z: DesignSupport.TimberReinforcementElementsTypeZ
    timber_reinforcement_elements_type_y: DesignSupport.TimberReinforcementElementsTypeY
    timber_reinforcement_parameters_specification_type_z: DesignSupport.TimberReinforcementParametersSpecificationTypeZ
    timber_reinforcement_parameters_specification_type_y: DesignSupport.TimberReinforcementParametersSpecificationTypeY
    timber_screw_z: int
    timber_screw_y: int
    timber_withdrawal_strength_of_one_screw_z: float
    timber_withdrawal_strength_of_one_screw_y: float
    timber_buckling_strength_of_one_screw_z: float
    timber_buckling_strength_of_one_screw_y: float
    timber_load_distribution_z: DesignSupport.TimberLoadDistributionZ
    timber_load_distribution_y: DesignSupport.TimberLoadDistributionY
    timber_screw_length_z: float
    timber_screw_length_y: float
    timber_thread_length_z: float
    timber_thread_length_y: float
    timber_number_of_screws_in_grain_direction_z: int
    timber_number_of_screws_in_grain_direction_y: int
    timber_number_of_screws_perpendicular_to_grain_direction_z: int
    timber_number_of_screws_perpendicular_to_grain_direction_y: int
    timber_spacing_of_screws_in_grain_direction_z: float
    timber_spacing_of_screws_in_grain_direction_y: float
    timber_spacing_of_rows_perpendicular_to_grain_directionz: float
    timber_spacing_of_rows_perpendicular_to_grain_directiony: float
    timber_check_critical_bearing_z_enabled: bool
    timber_check_critical_bearing_y_enabled: bool
    timber_calculation_method_z: DesignSupport.TimberCalculationMethodZ
    timber_calculation_method_y: DesignSupport.TimberCalculationMethodY
    timber_compression_design_value_z: DesignSupport.TimberCompressionDesignValueZ
    timber_compression_design_value_y: DesignSupport.TimberCompressionDesignValueY
    timber_allow_higher_deformation_z_enabled: bool
    timber_allow_higher_deformation_y_enabled: bool
    timber_factor_of_compression_z: float
    timber_factor_of_compression_y: float
    limit_of_high_bending_stresses_z: float
    limit_of_high_bending_stresses_y: float
    consider_in_fire_design_z: bool
    consider_in_fire_design_y: bool
    timber_shear_force_reduction_z: bool
    timber_shear_force_reduction_y: bool
    end_support_z_enabled: bool
    overhang_length_z: float
    fastened_to_support_z_enabled: bool
    comment: str
    is_generated: bool
    generating_object_info: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., type: _Optional[_Union[DesignSupport.Type, str]] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., assigned_to_members: _Optional[_Iterable[int]] = ..., assigned_to_member_sets: _Optional[_Iterable[int]] = ..., assigned_to_nodes: _Optional[_Iterable[int]] = ..., assigned_to_objects: _Optional[str] = ..., support_width_z: _Optional[float] = ..., support_depth_z: _Optional[float] = ..., support_width_y: _Optional[float] = ..., support_depth_y: _Optional[float] = ..., support_depth_by_section_width_of_member_z_enabled: bool = ..., support_depth_by_section_width_of_member_y_enabled: bool = ..., design_support_orientation_z: _Optional[_Union[DesignSupport.DesignSupportOrientationZ, str]] = ..., design_support_orientation_y: _Optional[_Union[DesignSupport.DesignSupportOrientationY, str]] = ..., direct_support_z_enabled: bool = ..., direct_support_y_enabled: bool = ..., activate_in_z: bool = ..., activate_in_y: bool = ..., consider_in_deflection_design_z: bool = ..., consider_in_deflection_design_y: bool = ..., concrete_monolithic_connection_z_enabled: bool = ..., inner_support_z_enabled: bool = ..., inner_support_y_enabled: bool = ..., concrete_ratio_of_moment_redistribution_z: _Optional[float] = ..., timber_reinforcement_elements_z_enabled: bool = ..., timber_reinforcement_elements_y_enabled: bool = ..., timber_reinforcement_elements_type_z: _Optional[_Union[DesignSupport.TimberReinforcementElementsTypeZ, str]] = ..., timber_reinforcement_elements_type_y: _Optional[_Union[DesignSupport.TimberReinforcementElementsTypeY, str]] = ..., timber_reinforcement_parameters_specification_type_z: _Optional[_Union[DesignSupport.TimberReinforcementParametersSpecificationTypeZ, str]] = ..., timber_reinforcement_parameters_specification_type_y: _Optional[_Union[DesignSupport.TimberReinforcementParametersSpecificationTypeY, str]] = ..., timber_screw_z: _Optional[int] = ..., timber_screw_y: _Optional[int] = ..., timber_withdrawal_strength_of_one_screw_z: _Optional[float] = ..., timber_withdrawal_strength_of_one_screw_y: _Optional[float] = ..., timber_buckling_strength_of_one_screw_z: _Optional[float] = ..., timber_buckling_strength_of_one_screw_y: _Optional[float] = ..., timber_load_distribution_z: _Optional[_Union[DesignSupport.TimberLoadDistributionZ, str]] = ..., timber_load_distribution_y: _Optional[_Union[DesignSupport.TimberLoadDistributionY, str]] = ..., timber_screw_length_z: _Optional[float] = ..., timber_screw_length_y: _Optional[float] = ..., timber_thread_length_z: _Optional[float] = ..., timber_thread_length_y: _Optional[float] = ..., timber_number_of_screws_in_grain_direction_z: _Optional[int] = ..., timber_number_of_screws_in_grain_direction_y: _Optional[int] = ..., timber_number_of_screws_perpendicular_to_grain_direction_z: _Optional[int] = ..., timber_number_of_screws_perpendicular_to_grain_direction_y: _Optional[int] = ..., timber_spacing_of_screws_in_grain_direction_z: _Optional[float] = ..., timber_spacing_of_screws_in_grain_direction_y: _Optional[float] = ..., timber_spacing_of_rows_perpendicular_to_grain_directionz: _Optional[float] = ..., timber_spacing_of_rows_perpendicular_to_grain_directiony: _Optional[float] = ..., timber_check_critical_bearing_z_enabled: bool = ..., timber_check_critical_bearing_y_enabled: bool = ..., timber_calculation_method_z: _Optional[_Union[DesignSupport.TimberCalculationMethodZ, str]] = ..., timber_calculation_method_y: _Optional[_Union[DesignSupport.TimberCalculationMethodY, str]] = ..., timber_compression_design_value_z: _Optional[_Union[DesignSupport.TimberCompressionDesignValueZ, str]] = ..., timber_compression_design_value_y: _Optional[_Union[DesignSupport.TimberCompressionDesignValueY, str]] = ..., timber_allow_higher_deformation_z_enabled: bool = ..., timber_allow_higher_deformation_y_enabled: bool = ..., timber_factor_of_compression_z: _Optional[float] = ..., timber_factor_of_compression_y: _Optional[float] = ..., limit_of_high_bending_stresses_z: _Optional[float] = ..., limit_of_high_bending_stresses_y: _Optional[float] = ..., consider_in_fire_design_z: bool = ..., consider_in_fire_design_y: bool = ..., timber_shear_force_reduction_z: bool = ..., timber_shear_force_reduction_y: bool = ..., end_support_z_enabled: bool = ..., overhang_length_z: _Optional[float] = ..., fastened_to_support_z_enabled: bool = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
