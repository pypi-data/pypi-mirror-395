from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CadLinePoint(_message.Message):
    __slots__ = ("no", "type", "coordinates", "coordinate_1", "coordinate_2", "coordinate_3", "parent_layer", "is_locked_by_parent_layer", "id_for_export_import", "metadata_for_export_import")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TYPE_UNKNOWN: _ClassVar[CadLinePoint.Type]
        TYPE_STANDARD: _ClassVar[CadLinePoint.Type]
    TYPE_UNKNOWN: CadLinePoint.Type
    TYPE_STANDARD: CadLinePoint.Type
    NO_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    COORDINATES_FIELD_NUMBER: _ClassVar[int]
    COORDINATE_1_FIELD_NUMBER: _ClassVar[int]
    COORDINATE_2_FIELD_NUMBER: _ClassVar[int]
    COORDINATE_3_FIELD_NUMBER: _ClassVar[int]
    PARENT_LAYER_FIELD_NUMBER: _ClassVar[int]
    IS_LOCKED_BY_PARENT_LAYER_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    type: CadLinePoint.Type
    coordinates: _common_pb2.Vector3d
    coordinate_1: float
    coordinate_2: float
    coordinate_3: float
    parent_layer: int
    is_locked_by_parent_layer: bool
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., type: _Optional[_Union[CadLinePoint.Type, str]] = ..., coordinates: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., coordinate_1: _Optional[float] = ..., coordinate_2: _Optional[float] = ..., coordinate_3: _Optional[float] = ..., parent_layer: _Optional[int] = ..., is_locked_by_parent_layer: bool = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
