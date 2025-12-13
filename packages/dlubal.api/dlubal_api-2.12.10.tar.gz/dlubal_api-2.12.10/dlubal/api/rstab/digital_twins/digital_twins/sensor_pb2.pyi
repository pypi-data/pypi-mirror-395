from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Sensor(_message.Message):
    __slots__ = ("no", "type", "user_defined_name_enabled", "name", "sensor_point", "sensor_point_x", "sensor_point_y", "sensor_point_z", "point", "point_x", "point_y", "point_z", "node", "measurements", "values", "status", "is_generated", "generating_object_info", "comment", "id_for_export_import", "metadata_for_export_import")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TYPE_UNKNOWN: _ClassVar[Sensor.Type]
        TYPE_LINE: _ClassVar[Sensor.Type]
        TYPE_MEMBER: _ClassVar[Sensor.Type]
        TYPE_NODE: _ClassVar[Sensor.Type]
        TYPE_POINT: _ClassVar[Sensor.Type]
        TYPE_SOLID: _ClassVar[Sensor.Type]
        TYPE_SURFACE: _ClassVar[Sensor.Type]
    TYPE_UNKNOWN: Sensor.Type
    TYPE_LINE: Sensor.Type
    TYPE_MEMBER: Sensor.Type
    TYPE_NODE: Sensor.Type
    TYPE_POINT: Sensor.Type
    TYPE_SOLID: Sensor.Type
    TYPE_SURFACE: Sensor.Type
    class MeasurementsTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[Sensor.MeasurementsRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[Sensor.MeasurementsRow, _Mapping]]] = ...) -> None: ...
    class MeasurementsRow(_message.Message):
        __slots__ = ("no", "description", "value_definition", "value", "unit", "status", "comment", "values", "reference", "deviations", "relative_values", "statuses")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        VALUE_DEFINITION_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        UNIT_FIELD_NUMBER: _ClassVar[int]
        STATUS_FIELD_NUMBER: _ClassVar[int]
        COMMENT_FIELD_NUMBER: _ClassVar[int]
        VALUES_FIELD_NUMBER: _ClassVar[int]
        REFERENCE_FIELD_NUMBER: _ClassVar[int]
        DEVIATIONS_FIELD_NUMBER: _ClassVar[int]
        RELATIVE_VALUES_FIELD_NUMBER: _ClassVar[int]
        STATUSES_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        value_definition: int
        value: str
        unit: str
        status: str
        comment: str
        values: str
        reference: str
        deviations: str
        relative_values: str
        statuses: str
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., value_definition: _Optional[int] = ..., value: _Optional[str] = ..., unit: _Optional[str] = ..., status: _Optional[str] = ..., comment: _Optional[str] = ..., values: _Optional[str] = ..., reference: _Optional[str] = ..., deviations: _Optional[str] = ..., relative_values: _Optional[str] = ..., statuses: _Optional[str] = ...) -> None: ...
    class ValuesTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[Sensor.ValuesRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[Sensor.ValuesRow, _Mapping]]] = ...) -> None: ...
    class ValuesRow(_message.Message):
        __slots__ = ("no", "description", "reference", "value_x", "value_y", "relative_value", "deviation", "status")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        REFERENCE_FIELD_NUMBER: _ClassVar[int]
        VALUE_X_FIELD_NUMBER: _ClassVar[int]
        VALUE_Y_FIELD_NUMBER: _ClassVar[int]
        RELATIVE_VALUE_FIELD_NUMBER: _ClassVar[int]
        DEVIATION_FIELD_NUMBER: _ClassVar[int]
        STATUS_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        reference: bool
        value_x: str
        value_y: str
        relative_value: str
        deviation: str
        status: str
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., reference: bool = ..., value_x: _Optional[str] = ..., value_y: _Optional[str] = ..., relative_value: _Optional[str] = ..., deviation: _Optional[str] = ..., status: _Optional[str] = ...) -> None: ...
    NO_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SENSOR_POINT_FIELD_NUMBER: _ClassVar[int]
    SENSOR_POINT_X_FIELD_NUMBER: _ClassVar[int]
    SENSOR_POINT_Y_FIELD_NUMBER: _ClassVar[int]
    SENSOR_POINT_Z_FIELD_NUMBER: _ClassVar[int]
    POINT_FIELD_NUMBER: _ClassVar[int]
    POINT_X_FIELD_NUMBER: _ClassVar[int]
    POINT_Y_FIELD_NUMBER: _ClassVar[int]
    POINT_Z_FIELD_NUMBER: _ClassVar[int]
    NODE_FIELD_NUMBER: _ClassVar[int]
    MEASUREMENTS_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    type: Sensor.Type
    user_defined_name_enabled: bool
    name: str
    sensor_point: _common_pb2.Vector3d
    sensor_point_x: float
    sensor_point_y: float
    sensor_point_z: float
    point: _common_pb2.Vector3d
    point_x: float
    point_y: float
    point_z: float
    node: int
    measurements: Sensor.MeasurementsTable
    values: Sensor.ValuesTable
    status: str
    is_generated: bool
    generating_object_info: str
    comment: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., type: _Optional[_Union[Sensor.Type, str]] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., sensor_point: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., sensor_point_x: _Optional[float] = ..., sensor_point_y: _Optional[float] = ..., sensor_point_z: _Optional[float] = ..., point: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., point_x: _Optional[float] = ..., point_y: _Optional[float] = ..., point_z: _Optional[float] = ..., node: _Optional[int] = ..., measurements: _Optional[_Union[Sensor.MeasurementsTable, _Mapping]] = ..., values: _Optional[_Union[Sensor.ValuesTable, _Mapping]] = ..., status: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., comment: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
