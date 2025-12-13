from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CuttingLineSetting(_message.Message):
    __slots__ = ("no", "type", "name", "cutting_pattern_allowance", "comment", "id_for_export_import", "metadata_for_export_import")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TYPE_UNKNOWN: _ClassVar[CuttingLineSetting.Type]
        TYPE_STANDARD: _ClassVar[CuttingLineSetting.Type]
    TYPE_UNKNOWN: CuttingLineSetting.Type
    TYPE_STANDARD: CuttingLineSetting.Type
    NO_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CUTTING_PATTERN_ALLOWANCE_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    type: CuttingLineSetting.Type
    name: str
    cutting_pattern_allowance: float
    comment: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., type: _Optional[_Union[CuttingLineSetting.Type, str]] = ..., name: _Optional[str] = ..., cutting_pattern_allowance: _Optional[float] = ..., comment: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
