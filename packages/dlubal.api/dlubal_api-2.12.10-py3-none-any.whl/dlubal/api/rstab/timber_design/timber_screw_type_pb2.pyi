from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TimberScrewType(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "screw_type", "outer_diameter", "core_diameter", "screw_length", "thread_length", "elastic_modulus", "yield_strength", "characteristic_tensile_strength", "characteristic_withdrawal_strength", "reference_density", "minimum_screw_spacing_1", "minimum_screw_spacing_2", "minimum_screw_edge_distance_1", "minimum_screw_edge_distance_2", "comment", "is_generated", "generating_object_info", "id_for_export_import", "metadata_for_export_import")
    class ScrewType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SCREW_TYPE_FULLY_THREADED: _ClassVar[TimberScrewType.ScrewType]
    SCREW_TYPE_FULLY_THREADED: TimberScrewType.ScrewType
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SCREW_TYPE_FIELD_NUMBER: _ClassVar[int]
    OUTER_DIAMETER_FIELD_NUMBER: _ClassVar[int]
    CORE_DIAMETER_FIELD_NUMBER: _ClassVar[int]
    SCREW_LENGTH_FIELD_NUMBER: _ClassVar[int]
    THREAD_LENGTH_FIELD_NUMBER: _ClassVar[int]
    ELASTIC_MODULUS_FIELD_NUMBER: _ClassVar[int]
    YIELD_STRENGTH_FIELD_NUMBER: _ClassVar[int]
    CHARACTERISTIC_TENSILE_STRENGTH_FIELD_NUMBER: _ClassVar[int]
    CHARACTERISTIC_WITHDRAWAL_STRENGTH_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_DENSITY_FIELD_NUMBER: _ClassVar[int]
    MINIMUM_SCREW_SPACING_1_FIELD_NUMBER: _ClassVar[int]
    MINIMUM_SCREW_SPACING_2_FIELD_NUMBER: _ClassVar[int]
    MINIMUM_SCREW_EDGE_DISTANCE_1_FIELD_NUMBER: _ClassVar[int]
    MINIMUM_SCREW_EDGE_DISTANCE_2_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    screw_type: TimberScrewType.ScrewType
    outer_diameter: float
    core_diameter: float
    screw_length: float
    thread_length: float
    elastic_modulus: float
    yield_strength: float
    characteristic_tensile_strength: float
    characteristic_withdrawal_strength: float
    reference_density: float
    minimum_screw_spacing_1: float
    minimum_screw_spacing_2: float
    minimum_screw_edge_distance_1: float
    minimum_screw_edge_distance_2: float
    comment: str
    is_generated: bool
    generating_object_info: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., screw_type: _Optional[_Union[TimberScrewType.ScrewType, str]] = ..., outer_diameter: _Optional[float] = ..., core_diameter: _Optional[float] = ..., screw_length: _Optional[float] = ..., thread_length: _Optional[float] = ..., elastic_modulus: _Optional[float] = ..., yield_strength: _Optional[float] = ..., characteristic_tensile_strength: _Optional[float] = ..., characteristic_withdrawal_strength: _Optional[float] = ..., reference_density: _Optional[float] = ..., minimum_screw_spacing_1: _Optional[float] = ..., minimum_screw_spacing_2: _Optional[float] = ..., minimum_screw_edge_distance_1: _Optional[float] = ..., minimum_screw_edge_distance_2: _Optional[float] = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
