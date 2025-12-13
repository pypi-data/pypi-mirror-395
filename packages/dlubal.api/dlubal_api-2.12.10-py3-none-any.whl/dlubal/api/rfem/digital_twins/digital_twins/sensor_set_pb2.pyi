from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SensorSet(_message.Message):
    __slots__ = ("no", "type", "user_defined_name_enabled", "name", "sensors", "type_of_statistical_evaluation", "sensor_value_definition", "statistics_results_table", "statistics_results", "is_generated", "generating_object_info", "comment", "id_for_export_import", "metadata_for_export_import")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TYPE_UNKNOWN: _ClassVar[SensorSet.Type]
        TYPE_STANDARD: _ClassVar[SensorSet.Type]
    TYPE_UNKNOWN: SensorSet.Type
    TYPE_STANDARD: SensorSet.Type
    class TypeOfStatisticalEvaluation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TYPE_OF_STATISTICAL_EVALUATION_SINGLE: _ClassVar[SensorSet.TypeOfStatisticalEvaluation]
        TYPE_OF_STATISTICAL_EVALUATION_FUNCTION: _ClassVar[SensorSet.TypeOfStatisticalEvaluation]
    TYPE_OF_STATISTICAL_EVALUATION_SINGLE: SensorSet.TypeOfStatisticalEvaluation
    TYPE_OF_STATISTICAL_EVALUATION_FUNCTION: SensorSet.TypeOfStatisticalEvaluation
    class StatisticsResultsTableTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SensorSet.StatisticsResultsTableTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SensorSet.StatisticsResultsTableTreeTableRow, _Mapping]]] = ...) -> None: ...
    class StatisticsResultsTableTreeTableRow(_message.Message):
        __slots__ = ("key", "description", "symbol", "value", "unit", "rows")
        KEY_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        SYMBOL_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        UNIT_FIELD_NUMBER: _ClassVar[int]
        ROWS_FIELD_NUMBER: _ClassVar[int]
        key: str
        description: str
        symbol: str
        value: str
        unit: str
        rows: _containers.RepeatedCompositeFieldContainer[SensorSet.StatisticsResultsTableTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., description: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[str] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SensorSet.StatisticsResultsTableTreeTableRow, _Mapping]]] = ...) -> None: ...
    NO_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SENSORS_FIELD_NUMBER: _ClassVar[int]
    TYPE_OF_STATISTICAL_EVALUATION_FIELD_NUMBER: _ClassVar[int]
    SENSOR_VALUE_DEFINITION_FIELD_NUMBER: _ClassVar[int]
    STATISTICS_RESULTS_TABLE_FIELD_NUMBER: _ClassVar[int]
    STATISTICS_RESULTS_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    type: SensorSet.Type
    user_defined_name_enabled: bool
    name: str
    sensors: _containers.RepeatedScalarFieldContainer[int]
    type_of_statistical_evaluation: SensorSet.TypeOfStatisticalEvaluation
    sensor_value_definition: int
    statistics_results_table: SensorSet.StatisticsResultsTableTreeTable
    statistics_results: str
    is_generated: bool
    generating_object_info: str
    comment: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., type: _Optional[_Union[SensorSet.Type, str]] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., sensors: _Optional[_Iterable[int]] = ..., type_of_statistical_evaluation: _Optional[_Union[SensorSet.TypeOfStatisticalEvaluation, str]] = ..., sensor_value_definition: _Optional[int] = ..., statistics_results_table: _Optional[_Union[SensorSet.StatisticsResultsTableTreeTable, _Mapping]] = ..., statistics_results: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., comment: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
