from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LoadModel(_message.Message):
    __slots__ = ("type", "no", "user_defined_name_enabled", "name", "load_components", "comment", "id_for_export_import", "metadata_for_export_import")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TYPE_UNKNOWN: _ClassVar[LoadModel.Type]
        TYPE_MEMBERS: _ClassVar[LoadModel.Type]
        TYPE_SURFACES: _ClassVar[LoadModel.Type]
    TYPE_UNKNOWN: LoadModel.Type
    TYPE_MEMBERS: LoadModel.Type
    TYPE_SURFACES: LoadModel.Type
    class LoadComponentsTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[LoadModel.LoadComponentsTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[LoadModel.LoadComponentsTreeTableRow, _Mapping]]] = ...) -> None: ...
    class LoadComponentsTreeTableRow(_message.Message):
        __slots__ = ("key", "name", "symbol", "value", "unit", "count_of_components", "load_definition", "position_x", "position_y", "position_A", "position_B", "load_magnitude_P", "load_magnitude_P2", "load_magnitude_M", "load_magnitude_M2", "eccentricity_y", "eccentricity_z", "width", "length", "diameter", "gauge", "number_of_loads", "load_type", "coordinate_system", "load_direction", "definition_type", "rows")
        class LoadDefinition(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            LOAD_DEFINITION_UNKNOWN: _ClassVar[LoadModel.LoadComponentsTreeTableRow.LoadDefinition]
        LOAD_DEFINITION_UNKNOWN: LoadModel.LoadComponentsTreeTableRow.LoadDefinition
        class LoadType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            LOAD_TYPE_UNKNOWN: _ClassVar[LoadModel.LoadComponentsTreeTableRow.LoadType]
        LOAD_TYPE_UNKNOWN: LoadModel.LoadComponentsTreeTableRow.LoadType
        class LoadDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            LOAD_DIRECTION_UNKNOWN: _ClassVar[LoadModel.LoadComponentsTreeTableRow.LoadDirection]
        LOAD_DIRECTION_UNKNOWN: LoadModel.LoadComponentsTreeTableRow.LoadDirection
        class DefinitionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            DEFINITION_TYPE_UNKNOWN: _ClassVar[LoadModel.LoadComponentsTreeTableRow.DefinitionType]
        DEFINITION_TYPE_UNKNOWN: LoadModel.LoadComponentsTreeTableRow.DefinitionType
        KEY_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        SYMBOL_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        UNIT_FIELD_NUMBER: _ClassVar[int]
        COUNT_OF_COMPONENTS_FIELD_NUMBER: _ClassVar[int]
        LOAD_DEFINITION_FIELD_NUMBER: _ClassVar[int]
        POSITION_X_FIELD_NUMBER: _ClassVar[int]
        POSITION_Y_FIELD_NUMBER: _ClassVar[int]
        POSITION_A_FIELD_NUMBER: _ClassVar[int]
        POSITION_B_FIELD_NUMBER: _ClassVar[int]
        LOAD_MAGNITUDE_P_FIELD_NUMBER: _ClassVar[int]
        LOAD_MAGNITUDE_P2_FIELD_NUMBER: _ClassVar[int]
        LOAD_MAGNITUDE_M_FIELD_NUMBER: _ClassVar[int]
        LOAD_MAGNITUDE_M2_FIELD_NUMBER: _ClassVar[int]
        ECCENTRICITY_Y_FIELD_NUMBER: _ClassVar[int]
        ECCENTRICITY_Z_FIELD_NUMBER: _ClassVar[int]
        WIDTH_FIELD_NUMBER: _ClassVar[int]
        LENGTH_FIELD_NUMBER: _ClassVar[int]
        DIAMETER_FIELD_NUMBER: _ClassVar[int]
        GAUGE_FIELD_NUMBER: _ClassVar[int]
        NUMBER_OF_LOADS_FIELD_NUMBER: _ClassVar[int]
        LOAD_TYPE_FIELD_NUMBER: _ClassVar[int]
        COORDINATE_SYSTEM_FIELD_NUMBER: _ClassVar[int]
        LOAD_DIRECTION_FIELD_NUMBER: _ClassVar[int]
        DEFINITION_TYPE_FIELD_NUMBER: _ClassVar[int]
        ROWS_FIELD_NUMBER: _ClassVar[int]
        key: str
        name: str
        symbol: str
        value: str
        unit: str
        count_of_components: int
        load_definition: LoadModel.LoadComponentsTreeTableRow.LoadDefinition
        position_x: float
        position_y: float
        position_A: float
        position_B: float
        load_magnitude_P: float
        load_magnitude_P2: float
        load_magnitude_M: float
        load_magnitude_M2: float
        eccentricity_y: float
        eccentricity_z: float
        width: float
        length: float
        diameter: float
        gauge: float
        number_of_loads: int
        load_type: LoadModel.LoadComponentsTreeTableRow.LoadType
        coordinate_system: int
        load_direction: LoadModel.LoadComponentsTreeTableRow.LoadDirection
        definition_type: LoadModel.LoadComponentsTreeTableRow.DefinitionType
        rows: _containers.RepeatedCompositeFieldContainer[LoadModel.LoadComponentsTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., name: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[str] = ..., unit: _Optional[str] = ..., count_of_components: _Optional[int] = ..., load_definition: _Optional[_Union[LoadModel.LoadComponentsTreeTableRow.LoadDefinition, str]] = ..., position_x: _Optional[float] = ..., position_y: _Optional[float] = ..., position_A: _Optional[float] = ..., position_B: _Optional[float] = ..., load_magnitude_P: _Optional[float] = ..., load_magnitude_P2: _Optional[float] = ..., load_magnitude_M: _Optional[float] = ..., load_magnitude_M2: _Optional[float] = ..., eccentricity_y: _Optional[float] = ..., eccentricity_z: _Optional[float] = ..., width: _Optional[float] = ..., length: _Optional[float] = ..., diameter: _Optional[float] = ..., gauge: _Optional[float] = ..., number_of_loads: _Optional[int] = ..., load_type: _Optional[_Union[LoadModel.LoadComponentsTreeTableRow.LoadType, str]] = ..., coordinate_system: _Optional[int] = ..., load_direction: _Optional[_Union[LoadModel.LoadComponentsTreeTableRow.LoadDirection, str]] = ..., definition_type: _Optional[_Union[LoadModel.LoadComponentsTreeTableRow.DefinitionType, str]] = ..., rows: _Optional[_Iterable[_Union[LoadModel.LoadComponentsTreeTableRow, _Mapping]]] = ...) -> None: ...
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    LOAD_COMPONENTS_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    type: LoadModel.Type
    no: int
    user_defined_name_enabled: bool
    name: str
    load_components: LoadModel.LoadComponentsTreeTable
    comment: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, type: _Optional[_Union[LoadModel.Type, str]] = ..., no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., load_components: _Optional[_Union[LoadModel.LoadComponentsTreeTable, _Mapping]] = ..., comment: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
