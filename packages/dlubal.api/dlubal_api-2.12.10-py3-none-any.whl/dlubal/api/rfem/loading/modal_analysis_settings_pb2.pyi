from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ModalAnalysisSettings(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "comment", "assigned_to", "number_of_modes_method", "number_of_modes", "effective_modal_mass_factor", "maxmimum_natural_frequency", "find_eigenvectors_beyond_frequency", "frequency", "mass_conversion_type", "activate_minimum_initial_prestress", "minimum_initial_strain", "acting_masses_in_direction_x_enabled", "acting_masses_in_direction_y_enabled", "acting_masses_in_direction_z_enabled", "acting_masses_about_axis_x_enabled", "acting_masses_about_axis_y_enabled", "acting_masses_about_axis_z_enabled", "neglect_masses", "solution_method", "mass_matrix_type", "neglect_masses_of_selected_objects_table", "id_for_export_import", "metadata_for_export_import")
    class NumberOfModesMethod(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        NUMBER_OF_MODES_METHOD_USER_DEFINED: _ClassVar[ModalAnalysisSettings.NumberOfModesMethod]
        NUMBER_OF_MODES_METHOD_EFFECTIVE_MASS_FACTORS: _ClassVar[ModalAnalysisSettings.NumberOfModesMethod]
        NUMBER_OF_MODES_METHOD_MAXIMUM_FREQUENCY: _ClassVar[ModalAnalysisSettings.NumberOfModesMethod]
    NUMBER_OF_MODES_METHOD_USER_DEFINED: ModalAnalysisSettings.NumberOfModesMethod
    NUMBER_OF_MODES_METHOD_EFFECTIVE_MASS_FACTORS: ModalAnalysisSettings.NumberOfModesMethod
    NUMBER_OF_MODES_METHOD_MAXIMUM_FREQUENCY: ModalAnalysisSettings.NumberOfModesMethod
    class MassConversionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        MASS_CONVERSION_TYPE_Z_COMPONENTS_OF_LOADS: _ClassVar[ModalAnalysisSettings.MassConversionType]
        MASS_CONVERSION_TYPE_FULL_LOADS_AS_MASS: _ClassVar[ModalAnalysisSettings.MassConversionType]
        MASS_CONVERSION_TYPE_Z_COMPONENTS_OF_LOADS_IN_DIRECTION_OF_GRAVITY: _ClassVar[ModalAnalysisSettings.MassConversionType]
    MASS_CONVERSION_TYPE_Z_COMPONENTS_OF_LOADS: ModalAnalysisSettings.MassConversionType
    MASS_CONVERSION_TYPE_FULL_LOADS_AS_MASS: ModalAnalysisSettings.MassConversionType
    MASS_CONVERSION_TYPE_Z_COMPONENTS_OF_LOADS_IN_DIRECTION_OF_GRAVITY: ModalAnalysisSettings.MassConversionType
    class NeglectMasses(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        NEGLECT_MASSES_IN_ALL_FIXED_SUPPORTS: _ClassVar[ModalAnalysisSettings.NeglectMasses]
        NEGLECT_MASSES_NO_NEGLECTION: _ClassVar[ModalAnalysisSettings.NeglectMasses]
        NEGLECT_MASSES_USER_DEFINED: _ClassVar[ModalAnalysisSettings.NeglectMasses]
    NEGLECT_MASSES_IN_ALL_FIXED_SUPPORTS: ModalAnalysisSettings.NeglectMasses
    NEGLECT_MASSES_NO_NEGLECTION: ModalAnalysisSettings.NeglectMasses
    NEGLECT_MASSES_USER_DEFINED: ModalAnalysisSettings.NeglectMasses
    class SolutionMethod(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SOLUTION_METHOD_LANCZOS: _ClassVar[ModalAnalysisSettings.SolutionMethod]
        SOLUTION_METHOD_ROOT_OF_CHARACTERISTIC_POLYNOMIAL: _ClassVar[ModalAnalysisSettings.SolutionMethod]
        SOLUTION_METHOD_SHIFTED_INVERSE_POWER_METHOD: _ClassVar[ModalAnalysisSettings.SolutionMethod]
        SOLUTION_METHOD_SUBSPACE_ITERATION: _ClassVar[ModalAnalysisSettings.SolutionMethod]
    SOLUTION_METHOD_LANCZOS: ModalAnalysisSettings.SolutionMethod
    SOLUTION_METHOD_ROOT_OF_CHARACTERISTIC_POLYNOMIAL: ModalAnalysisSettings.SolutionMethod
    SOLUTION_METHOD_SHIFTED_INVERSE_POWER_METHOD: ModalAnalysisSettings.SolutionMethod
    SOLUTION_METHOD_SUBSPACE_ITERATION: ModalAnalysisSettings.SolutionMethod
    class MassMatrixType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        MASS_MATRIX_TYPE_DIAGONAL: _ClassVar[ModalAnalysisSettings.MassMatrixType]
        MASS_MATRIX_TYPE_CONSISTENT: _ClassVar[ModalAnalysisSettings.MassMatrixType]
        MASS_MATRIX_TYPE_DIAGONAL_TRANSLATIONAL_AND_ROTATIONAL_DOFS: _ClassVar[ModalAnalysisSettings.MassMatrixType]
        MASS_MATRIX_TYPE_UNIT: _ClassVar[ModalAnalysisSettings.MassMatrixType]
    MASS_MATRIX_TYPE_DIAGONAL: ModalAnalysisSettings.MassMatrixType
    MASS_MATRIX_TYPE_CONSISTENT: ModalAnalysisSettings.MassMatrixType
    MASS_MATRIX_TYPE_DIAGONAL_TRANSLATIONAL_AND_ROTATIONAL_DOFS: ModalAnalysisSettings.MassMatrixType
    MASS_MATRIX_TYPE_UNIT: ModalAnalysisSettings.MassMatrixType
    class NeglectMassesOfSelectedObjectsTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[ModalAnalysisSettings.NeglectMassesOfSelectedObjectsTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[ModalAnalysisSettings.NeglectMassesOfSelectedObjectsTableRow, _Mapping]]] = ...) -> None: ...
    class NeglectMassesOfSelectedObjectsTableRow(_message.Message):
        __slots__ = ("no", "description", "object_type", "object_list", "neglect_mass_component_in_direction_x_enabled", "neglect_mass_component_in_direction_y_enabled", "neglect_mass_component_in_direction_z_enabled", "neglect_mass_component_about_axis_x_enabled", "neglect_mass_component_about_axis_y_enabled", "neglect_mass_component_about_axis_z_enabled", "comment")
        class ObjectType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            OBJECT_TYPE_UNKNOWN: _ClassVar[ModalAnalysisSettings.NeglectMassesOfSelectedObjectsTableRow.ObjectType]
            OBJECT_TYPE_LINE: _ClassVar[ModalAnalysisSettings.NeglectMassesOfSelectedObjectsTableRow.ObjectType]
            OBJECT_TYPE_LINE_WITH_SUPPORT: _ClassVar[ModalAnalysisSettings.NeglectMassesOfSelectedObjectsTableRow.ObjectType]
            OBJECT_TYPE_MEMBER: _ClassVar[ModalAnalysisSettings.NeglectMassesOfSelectedObjectsTableRow.ObjectType]
            OBJECT_TYPE_NODE: _ClassVar[ModalAnalysisSettings.NeglectMassesOfSelectedObjectsTableRow.ObjectType]
            OBJECT_TYPE_NODE_WITH_SUPPORT: _ClassVar[ModalAnalysisSettings.NeglectMassesOfSelectedObjectsTableRow.ObjectType]
            OBJECT_TYPE_SOLID: _ClassVar[ModalAnalysisSettings.NeglectMassesOfSelectedObjectsTableRow.ObjectType]
            OBJECT_TYPE_SURFACE: _ClassVar[ModalAnalysisSettings.NeglectMassesOfSelectedObjectsTableRow.ObjectType]
        OBJECT_TYPE_UNKNOWN: ModalAnalysisSettings.NeglectMassesOfSelectedObjectsTableRow.ObjectType
        OBJECT_TYPE_LINE: ModalAnalysisSettings.NeglectMassesOfSelectedObjectsTableRow.ObjectType
        OBJECT_TYPE_LINE_WITH_SUPPORT: ModalAnalysisSettings.NeglectMassesOfSelectedObjectsTableRow.ObjectType
        OBJECT_TYPE_MEMBER: ModalAnalysisSettings.NeglectMassesOfSelectedObjectsTableRow.ObjectType
        OBJECT_TYPE_NODE: ModalAnalysisSettings.NeglectMassesOfSelectedObjectsTableRow.ObjectType
        OBJECT_TYPE_NODE_WITH_SUPPORT: ModalAnalysisSettings.NeglectMassesOfSelectedObjectsTableRow.ObjectType
        OBJECT_TYPE_SOLID: ModalAnalysisSettings.NeglectMassesOfSelectedObjectsTableRow.ObjectType
        OBJECT_TYPE_SURFACE: ModalAnalysisSettings.NeglectMassesOfSelectedObjectsTableRow.ObjectType
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        OBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
        OBJECT_LIST_FIELD_NUMBER: _ClassVar[int]
        NEGLECT_MASS_COMPONENT_IN_DIRECTION_X_ENABLED_FIELD_NUMBER: _ClassVar[int]
        NEGLECT_MASS_COMPONENT_IN_DIRECTION_Y_ENABLED_FIELD_NUMBER: _ClassVar[int]
        NEGLECT_MASS_COMPONENT_IN_DIRECTION_Z_ENABLED_FIELD_NUMBER: _ClassVar[int]
        NEGLECT_MASS_COMPONENT_ABOUT_AXIS_X_ENABLED_FIELD_NUMBER: _ClassVar[int]
        NEGLECT_MASS_COMPONENT_ABOUT_AXIS_Y_ENABLED_FIELD_NUMBER: _ClassVar[int]
        NEGLECT_MASS_COMPONENT_ABOUT_AXIS_Z_ENABLED_FIELD_NUMBER: _ClassVar[int]
        COMMENT_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        object_type: ModalAnalysisSettings.NeglectMassesOfSelectedObjectsTableRow.ObjectType
        object_list: _containers.RepeatedScalarFieldContainer[int]
        neglect_mass_component_in_direction_x_enabled: bool
        neglect_mass_component_in_direction_y_enabled: bool
        neglect_mass_component_in_direction_z_enabled: bool
        neglect_mass_component_about_axis_x_enabled: bool
        neglect_mass_component_about_axis_y_enabled: bool
        neglect_mass_component_about_axis_z_enabled: bool
        comment: str
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., object_type: _Optional[_Union[ModalAnalysisSettings.NeglectMassesOfSelectedObjectsTableRow.ObjectType, str]] = ..., object_list: _Optional[_Iterable[int]] = ..., neglect_mass_component_in_direction_x_enabled: bool = ..., neglect_mass_component_in_direction_y_enabled: bool = ..., neglect_mass_component_in_direction_z_enabled: bool = ..., neglect_mass_component_about_axis_x_enabled: bool = ..., neglect_mass_component_about_axis_y_enabled: bool = ..., neglect_mass_component_about_axis_z_enabled: bool = ..., comment: _Optional[str] = ...) -> None: ...
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_MODES_METHOD_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_MODES_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_MODAL_MASS_FACTOR_FIELD_NUMBER: _ClassVar[int]
    MAXMIMUM_NATURAL_FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    FIND_EIGENVECTORS_BEYOND_FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    MASS_CONVERSION_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACTIVATE_MINIMUM_INITIAL_PRESTRESS_FIELD_NUMBER: _ClassVar[int]
    MINIMUM_INITIAL_STRAIN_FIELD_NUMBER: _ClassVar[int]
    ACTING_MASSES_IN_DIRECTION_X_ENABLED_FIELD_NUMBER: _ClassVar[int]
    ACTING_MASSES_IN_DIRECTION_Y_ENABLED_FIELD_NUMBER: _ClassVar[int]
    ACTING_MASSES_IN_DIRECTION_Z_ENABLED_FIELD_NUMBER: _ClassVar[int]
    ACTING_MASSES_ABOUT_AXIS_X_ENABLED_FIELD_NUMBER: _ClassVar[int]
    ACTING_MASSES_ABOUT_AXIS_Y_ENABLED_FIELD_NUMBER: _ClassVar[int]
    ACTING_MASSES_ABOUT_AXIS_Z_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NEGLECT_MASSES_FIELD_NUMBER: _ClassVar[int]
    SOLUTION_METHOD_FIELD_NUMBER: _ClassVar[int]
    MASS_MATRIX_TYPE_FIELD_NUMBER: _ClassVar[int]
    NEGLECT_MASSES_OF_SELECTED_OBJECTS_TABLE_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    comment: str
    assigned_to: str
    number_of_modes_method: ModalAnalysisSettings.NumberOfModesMethod
    number_of_modes: int
    effective_modal_mass_factor: float
    maxmimum_natural_frequency: float
    find_eigenvectors_beyond_frequency: bool
    frequency: float
    mass_conversion_type: ModalAnalysisSettings.MassConversionType
    activate_minimum_initial_prestress: bool
    minimum_initial_strain: float
    acting_masses_in_direction_x_enabled: bool
    acting_masses_in_direction_y_enabled: bool
    acting_masses_in_direction_z_enabled: bool
    acting_masses_about_axis_x_enabled: bool
    acting_masses_about_axis_y_enabled: bool
    acting_masses_about_axis_z_enabled: bool
    neglect_masses: ModalAnalysisSettings.NeglectMasses
    solution_method: ModalAnalysisSettings.SolutionMethod
    mass_matrix_type: ModalAnalysisSettings.MassMatrixType
    neglect_masses_of_selected_objects_table: ModalAnalysisSettings.NeglectMassesOfSelectedObjectsTable
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., comment: _Optional[str] = ..., assigned_to: _Optional[str] = ..., number_of_modes_method: _Optional[_Union[ModalAnalysisSettings.NumberOfModesMethod, str]] = ..., number_of_modes: _Optional[int] = ..., effective_modal_mass_factor: _Optional[float] = ..., maxmimum_natural_frequency: _Optional[float] = ..., find_eigenvectors_beyond_frequency: bool = ..., frequency: _Optional[float] = ..., mass_conversion_type: _Optional[_Union[ModalAnalysisSettings.MassConversionType, str]] = ..., activate_minimum_initial_prestress: bool = ..., minimum_initial_strain: _Optional[float] = ..., acting_masses_in_direction_x_enabled: bool = ..., acting_masses_in_direction_y_enabled: bool = ..., acting_masses_in_direction_z_enabled: bool = ..., acting_masses_about_axis_x_enabled: bool = ..., acting_masses_about_axis_y_enabled: bool = ..., acting_masses_about_axis_z_enabled: bool = ..., neglect_masses: _Optional[_Union[ModalAnalysisSettings.NeglectMasses, str]] = ..., solution_method: _Optional[_Union[ModalAnalysisSettings.SolutionMethod, str]] = ..., mass_matrix_type: _Optional[_Union[ModalAnalysisSettings.MassMatrixType, str]] = ..., neglect_masses_of_selected_objects_table: _Optional[_Union[ModalAnalysisSettings.NeglectMassesOfSelectedObjectsTable, _Mapping]] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
