from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SheathingToBeamConnector(_message.Message):
    __slots__ = ("no", "type", "user_defined_name_enabled", "name", "connector_type", "stiffness_calculation", "nail_type", "diameter", "length", "dimension_a", "dimension_b", "parameter_d", "parameter_l", "spacing", "stiffness_longitudinal_only", "dry_lumber", "structural_one_grade_sheathing", "line_hinge", "comment", "thicknesses", "is_generated", "generating_object_info", "id_for_export_import", "metadata_for_export_import")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TYPE_UNKNOWN: _ClassVar[SheathingToBeamConnector.Type]
        TYPE_STANDARD: _ClassVar[SheathingToBeamConnector.Type]
    TYPE_UNKNOWN: SheathingToBeamConnector.Type
    TYPE_STANDARD: SheathingToBeamConnector.Type
    class ConnectorType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CONNECTOR_TYPE_NAIL: _ClassVar[SheathingToBeamConnector.ConnectorType]
        CONNECTOR_TYPE_STAPLE: _ClassVar[SheathingToBeamConnector.ConnectorType]
        CONNECTOR_TYPE_USER_DEFINED: _ClassVar[SheathingToBeamConnector.ConnectorType]
    CONNECTOR_TYPE_NAIL: SheathingToBeamConnector.ConnectorType
    CONNECTOR_TYPE_STAPLE: SheathingToBeamConnector.ConnectorType
    CONNECTOR_TYPE_USER_DEFINED: SheathingToBeamConnector.ConnectorType
    class StiffnessCalculation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        STIFFNESS_CALCULATION_EN_1995: _ClassVar[SheathingToBeamConnector.StiffnessCalculation]
        STIFFNESS_CALCULATION_CSA_O86: _ClassVar[SheathingToBeamConnector.StiffnessCalculation]
        STIFFNESS_CALCULATION_NDS: _ClassVar[SheathingToBeamConnector.StiffnessCalculation]
        STIFFNESS_CALCULATION_SIA_265: _ClassVar[SheathingToBeamConnector.StiffnessCalculation]
        STIFFNESS_CALCULATION_USER_DEFINED: _ClassVar[SheathingToBeamConnector.StiffnessCalculation]
    STIFFNESS_CALCULATION_EN_1995: SheathingToBeamConnector.StiffnessCalculation
    STIFFNESS_CALCULATION_CSA_O86: SheathingToBeamConnector.StiffnessCalculation
    STIFFNESS_CALCULATION_NDS: SheathingToBeamConnector.StiffnessCalculation
    STIFFNESS_CALCULATION_SIA_265: SheathingToBeamConnector.StiffnessCalculation
    STIFFNESS_CALCULATION_USER_DEFINED: SheathingToBeamConnector.StiffnessCalculation
    class NailType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        NAIL_TYPE_USER_DEFINED: _ClassVar[SheathingToBeamConnector.NailType]
        NAIL_TYPE_10D_COMMON: _ClassVar[SheathingToBeamConnector.NailType]
        NAIL_TYPE_6D_COMMON: _ClassVar[SheathingToBeamConnector.NailType]
        NAIL_TYPE_8D_COMMON: _ClassVar[SheathingToBeamConnector.NailType]
    NAIL_TYPE_USER_DEFINED: SheathingToBeamConnector.NailType
    NAIL_TYPE_10D_COMMON: SheathingToBeamConnector.NailType
    NAIL_TYPE_6D_COMMON: SheathingToBeamConnector.NailType
    NAIL_TYPE_8D_COMMON: SheathingToBeamConnector.NailType
    NO_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONNECTOR_TYPE_FIELD_NUMBER: _ClassVar[int]
    STIFFNESS_CALCULATION_FIELD_NUMBER: _ClassVar[int]
    NAIL_TYPE_FIELD_NUMBER: _ClassVar[int]
    DIAMETER_FIELD_NUMBER: _ClassVar[int]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    DIMENSION_A_FIELD_NUMBER: _ClassVar[int]
    DIMENSION_B_FIELD_NUMBER: _ClassVar[int]
    PARAMETER_D_FIELD_NUMBER: _ClassVar[int]
    PARAMETER_L_FIELD_NUMBER: _ClassVar[int]
    SPACING_FIELD_NUMBER: _ClassVar[int]
    STIFFNESS_LONGITUDINAL_ONLY_FIELD_NUMBER: _ClassVar[int]
    DRY_LUMBER_FIELD_NUMBER: _ClassVar[int]
    STRUCTURAL_ONE_GRADE_SHEATHING_FIELD_NUMBER: _ClassVar[int]
    LINE_HINGE_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    THICKNESSES_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    type: SheathingToBeamConnector.Type
    user_defined_name_enabled: bool
    name: str
    connector_type: SheathingToBeamConnector.ConnectorType
    stiffness_calculation: SheathingToBeamConnector.StiffnessCalculation
    nail_type: SheathingToBeamConnector.NailType
    diameter: float
    length: float
    dimension_a: float
    dimension_b: float
    parameter_d: float
    parameter_l: float
    spacing: float
    stiffness_longitudinal_only: bool
    dry_lumber: bool
    structural_one_grade_sheathing: bool
    line_hinge: int
    comment: str
    thicknesses: _containers.RepeatedScalarFieldContainer[int]
    is_generated: bool
    generating_object_info: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., type: _Optional[_Union[SheathingToBeamConnector.Type, str]] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., connector_type: _Optional[_Union[SheathingToBeamConnector.ConnectorType, str]] = ..., stiffness_calculation: _Optional[_Union[SheathingToBeamConnector.StiffnessCalculation, str]] = ..., nail_type: _Optional[_Union[SheathingToBeamConnector.NailType, str]] = ..., diameter: _Optional[float] = ..., length: _Optional[float] = ..., dimension_a: _Optional[float] = ..., dimension_b: _Optional[float] = ..., parameter_d: _Optional[float] = ..., parameter_l: _Optional[float] = ..., spacing: _Optional[float] = ..., stiffness_longitudinal_only: bool = ..., dry_lumber: bool = ..., structural_one_grade_sheathing: bool = ..., line_hinge: _Optional[int] = ..., comment: _Optional[str] = ..., thicknesses: _Optional[_Iterable[int]] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
