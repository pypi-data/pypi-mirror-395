from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Layer(_message.Message):
    __slots__ = ("no", "name", "current", "locked", "color", "cad_line_type", "cad_line_thickness", "transparency", "comment", "id_for_export_import", "metadata_for_export_import")
    class CadLineType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CAD_LINE_TYPE_SOLID: _ClassVar[Layer.CadLineType]
        CAD_LINE_TYPE_DASHED: _ClassVar[Layer.CadLineType]
        CAD_LINE_TYPE_DOTTED: _ClassVar[Layer.CadLineType]
        CAD_LINE_TYPE_DOT_DASHED: _ClassVar[Layer.CadLineType]
        CAD_LINE_TYPE_LOOSELY_DASHED: _ClassVar[Layer.CadLineType]
    CAD_LINE_TYPE_SOLID: Layer.CadLineType
    CAD_LINE_TYPE_DASHED: Layer.CadLineType
    CAD_LINE_TYPE_DOTTED: Layer.CadLineType
    CAD_LINE_TYPE_DOT_DASHED: Layer.CadLineType
    CAD_LINE_TYPE_LOOSELY_DASHED: Layer.CadLineType
    NO_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CURRENT_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    CAD_LINE_TYPE_FIELD_NUMBER: _ClassVar[int]
    CAD_LINE_THICKNESS_FIELD_NUMBER: _ClassVar[int]
    TRANSPARENCY_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    name: str
    current: bool
    locked: bool
    color: str
    cad_line_type: Layer.CadLineType
    cad_line_thickness: int
    transparency: float
    comment: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., name: _Optional[str] = ..., current: bool = ..., locked: bool = ..., color: _Optional[str] = ..., cad_line_type: _Optional[_Union[Layer.CadLineType, str]] = ..., cad_line_thickness: _Optional[int] = ..., transparency: _Optional[float] = ..., comment: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
