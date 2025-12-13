from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PileResistance(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "members", "skin_resistance_type", "shear_strength_start", "shear_strength_end", "shear_stiffness_start", "shear_stiffness_end", "skin_resistance_parameters", "use_relative_distances", "axial_strength", "axial_stiffness", "interface_strength_reduction", "comment", "is_generated", "generating_object_info", "id_for_export_import", "metadata_for_export_import")
    class SkinResistanceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SKIN_RESISTANCE_TYPE_TRAPEZOIDAL: _ClassVar[PileResistance.SkinResistanceType]
        SKIN_RESISTANCE_TYPE_VARYING: _ClassVar[PileResistance.SkinResistanceType]
    SKIN_RESISTANCE_TYPE_TRAPEZOIDAL: PileResistance.SkinResistanceType
    SKIN_RESISTANCE_TYPE_VARYING: PileResistance.SkinResistanceType
    class SkinResistanceParametersTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[PileResistance.SkinResistanceParametersRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[PileResistance.SkinResistanceParametersRow, _Mapping]]] = ...) -> None: ...
    class SkinResistanceParametersRow(_message.Message):
        __slots__ = ("no", "description", "relative_distance", "absolute_distance", "shear_strength", "shear_stiffness")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        RELATIVE_DISTANCE_FIELD_NUMBER: _ClassVar[int]
        ABSOLUTE_DISTANCE_FIELD_NUMBER: _ClassVar[int]
        SHEAR_STRENGTH_FIELD_NUMBER: _ClassVar[int]
        SHEAR_STIFFNESS_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        relative_distance: float
        absolute_distance: float
        shear_strength: float
        shear_stiffness: float
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., relative_distance: _Optional[float] = ..., absolute_distance: _Optional[float] = ..., shear_strength: _Optional[float] = ..., shear_stiffness: _Optional[float] = ...) -> None: ...
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    SKIN_RESISTANCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SHEAR_STRENGTH_START_FIELD_NUMBER: _ClassVar[int]
    SHEAR_STRENGTH_END_FIELD_NUMBER: _ClassVar[int]
    SHEAR_STIFFNESS_START_FIELD_NUMBER: _ClassVar[int]
    SHEAR_STIFFNESS_END_FIELD_NUMBER: _ClassVar[int]
    SKIN_RESISTANCE_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    USE_RELATIVE_DISTANCES_FIELD_NUMBER: _ClassVar[int]
    AXIAL_STRENGTH_FIELD_NUMBER: _ClassVar[int]
    AXIAL_STIFFNESS_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_STRENGTH_REDUCTION_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    members: _containers.RepeatedScalarFieldContainer[int]
    skin_resistance_type: PileResistance.SkinResistanceType
    shear_strength_start: float
    shear_strength_end: float
    shear_stiffness_start: float
    shear_stiffness_end: float
    skin_resistance_parameters: PileResistance.SkinResistanceParametersTable
    use_relative_distances: bool
    axial_strength: float
    axial_stiffness: float
    interface_strength_reduction: float
    comment: str
    is_generated: bool
    generating_object_info: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., members: _Optional[_Iterable[int]] = ..., skin_resistance_type: _Optional[_Union[PileResistance.SkinResistanceType, str]] = ..., shear_strength_start: _Optional[float] = ..., shear_strength_end: _Optional[float] = ..., shear_stiffness_start: _Optional[float] = ..., shear_stiffness_end: _Optional[float] = ..., skin_resistance_parameters: _Optional[_Union[PileResistance.SkinResistanceParametersTable, _Mapping]] = ..., use_relative_distances: bool = ..., axial_strength: _Optional[float] = ..., axial_stiffness: _Optional[float] = ..., interface_strength_reduction: _Optional[float] = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
