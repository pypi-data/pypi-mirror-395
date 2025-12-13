from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SensorValueDefinition(_message.Message):
    __slots__ = ("no", "type", "user_defined_name_enabled", "name", "value_type_x", "value_x", "symbol_x", "variable_name_x", "unit_x", "decimal_places_x", "value_type_y", "value_y", "symbol_y", "variable_name_y", "unit_y", "decimal_places_y", "warning_limit", "alarm_limit", "unit_for_limits", "decimal_places_for_limits", "determination_of_sensor_status_based_on", "is_generated", "generating_object_info", "comment", "id_for_export_import", "metadata_for_export_import")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TYPE_UNKNOWN: _ClassVar[SensorValueDefinition.Type]
        TYPE_USER_DEFINED_FUNCTION: _ClassVar[SensorValueDefinition.Type]
        TYPE_USER_DEFINED_SINGLE: _ClassVar[SensorValueDefinition.Type]
    TYPE_UNKNOWN: SensorValueDefinition.Type
    TYPE_USER_DEFINED_FUNCTION: SensorValueDefinition.Type
    TYPE_USER_DEFINED_SINGLE: SensorValueDefinition.Type
    class ValueTypeX(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        VALUE_TYPE_X_DOUBLE: _ClassVar[SensorValueDefinition.ValueTypeX]
        VALUE_TYPE_X_DATE: _ClassVar[SensorValueDefinition.ValueTypeX]
        VALUE_TYPE_X_DATETIME: _ClassVar[SensorValueDefinition.ValueTypeX]
        VALUE_TYPE_X_STRING: _ClassVar[SensorValueDefinition.ValueTypeX]
    VALUE_TYPE_X_DOUBLE: SensorValueDefinition.ValueTypeX
    VALUE_TYPE_X_DATE: SensorValueDefinition.ValueTypeX
    VALUE_TYPE_X_DATETIME: SensorValueDefinition.ValueTypeX
    VALUE_TYPE_X_STRING: SensorValueDefinition.ValueTypeX
    class ValueTypeY(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        VALUE_TYPE_Y_DOUBLE: _ClassVar[SensorValueDefinition.ValueTypeY]
        VALUE_TYPE_Y_DATE: _ClassVar[SensorValueDefinition.ValueTypeY]
        VALUE_TYPE_Y_DATETIME: _ClassVar[SensorValueDefinition.ValueTypeY]
        VALUE_TYPE_Y_STRING: _ClassVar[SensorValueDefinition.ValueTypeY]
    VALUE_TYPE_Y_DOUBLE: SensorValueDefinition.ValueTypeY
    VALUE_TYPE_Y_DATE: SensorValueDefinition.ValueTypeY
    VALUE_TYPE_Y_DATETIME: SensorValueDefinition.ValueTypeY
    VALUE_TYPE_Y_STRING: SensorValueDefinition.ValueTypeY
    class DeterminationOfSensorStatusBasedOn(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DETERMINATION_OF_SENSOR_STATUS_BASED_ON_MOST_CRITICAL_VALUE: _ClassVar[SensorValueDefinition.DeterminationOfSensorStatusBasedOn]
        DETERMINATION_OF_SENSOR_STATUS_BASED_ON_COMPARISON: _ClassVar[SensorValueDefinition.DeterminationOfSensorStatusBasedOn]
        DETERMINATION_OF_SENSOR_STATUS_BASED_ON_LATEST_VALUE: _ClassVar[SensorValueDefinition.DeterminationOfSensorStatusBasedOn]
    DETERMINATION_OF_SENSOR_STATUS_BASED_ON_MOST_CRITICAL_VALUE: SensorValueDefinition.DeterminationOfSensorStatusBasedOn
    DETERMINATION_OF_SENSOR_STATUS_BASED_ON_COMPARISON: SensorValueDefinition.DeterminationOfSensorStatusBasedOn
    DETERMINATION_OF_SENSOR_STATUS_BASED_ON_LATEST_VALUE: SensorValueDefinition.DeterminationOfSensorStatusBasedOn
    NO_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_TYPE_X_FIELD_NUMBER: _ClassVar[int]
    VALUE_X_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_X_FIELD_NUMBER: _ClassVar[int]
    VARIABLE_NAME_X_FIELD_NUMBER: _ClassVar[int]
    UNIT_X_FIELD_NUMBER: _ClassVar[int]
    DECIMAL_PLACES_X_FIELD_NUMBER: _ClassVar[int]
    VALUE_TYPE_Y_FIELD_NUMBER: _ClassVar[int]
    VALUE_Y_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_Y_FIELD_NUMBER: _ClassVar[int]
    VARIABLE_NAME_Y_FIELD_NUMBER: _ClassVar[int]
    UNIT_Y_FIELD_NUMBER: _ClassVar[int]
    DECIMAL_PLACES_Y_FIELD_NUMBER: _ClassVar[int]
    WARNING_LIMIT_FIELD_NUMBER: _ClassVar[int]
    ALARM_LIMIT_FIELD_NUMBER: _ClassVar[int]
    UNIT_FOR_LIMITS_FIELD_NUMBER: _ClassVar[int]
    DECIMAL_PLACES_FOR_LIMITS_FIELD_NUMBER: _ClassVar[int]
    DETERMINATION_OF_SENSOR_STATUS_BASED_ON_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    type: SensorValueDefinition.Type
    user_defined_name_enabled: bool
    name: str
    value_type_x: SensorValueDefinition.ValueTypeX
    value_x: str
    symbol_x: str
    variable_name_x: str
    unit_x: str
    decimal_places_x: int
    value_type_y: SensorValueDefinition.ValueTypeY
    value_y: str
    symbol_y: str
    variable_name_y: str
    unit_y: str
    decimal_places_y: int
    warning_limit: str
    alarm_limit: str
    unit_for_limits: str
    decimal_places_for_limits: int
    determination_of_sensor_status_based_on: SensorValueDefinition.DeterminationOfSensorStatusBasedOn
    is_generated: bool
    generating_object_info: str
    comment: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., type: _Optional[_Union[SensorValueDefinition.Type, str]] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., value_type_x: _Optional[_Union[SensorValueDefinition.ValueTypeX, str]] = ..., value_x: _Optional[str] = ..., symbol_x: _Optional[str] = ..., variable_name_x: _Optional[str] = ..., unit_x: _Optional[str] = ..., decimal_places_x: _Optional[int] = ..., value_type_y: _Optional[_Union[SensorValueDefinition.ValueTypeY, str]] = ..., value_y: _Optional[str] = ..., symbol_y: _Optional[str] = ..., variable_name_y: _Optional[str] = ..., unit_y: _Optional[str] = ..., decimal_places_y: _Optional[int] = ..., warning_limit: _Optional[str] = ..., alarm_limit: _Optional[str] = ..., unit_for_limits: _Optional[str] = ..., decimal_places_for_limits: _Optional[int] = ..., determination_of_sensor_status_based_on: _Optional[_Union[SensorValueDefinition.DeterminationOfSensorStatusBasedOn, str]] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., comment: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
