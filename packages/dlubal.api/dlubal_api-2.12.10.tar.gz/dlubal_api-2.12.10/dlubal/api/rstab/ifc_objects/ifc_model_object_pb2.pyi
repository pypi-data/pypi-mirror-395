from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IfcModelObject(_message.Message):
    __slots__ = ("no", "type", "ifc_file", "ifc_type", "id_for_export_import", "metadata_for_export_import")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TYPE_UNKNOWN: _ClassVar[IfcModelObject.Type]
        TYPE_IFC2X3: _ClassVar[IfcModelObject.Type]
        TYPE_IFC4: _ClassVar[IfcModelObject.Type]
        TYPE_IFC4X3: _ClassVar[IfcModelObject.Type]
    TYPE_UNKNOWN: IfcModelObject.Type
    TYPE_IFC2X3: IfcModelObject.Type
    TYPE_IFC4: IfcModelObject.Type
    TYPE_IFC4X3: IfcModelObject.Type
    NO_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    IFC_FILE_FIELD_NUMBER: _ClassVar[int]
    IFC_TYPE_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    type: IfcModelObject.Type
    ifc_file: int
    ifc_type: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., type: _Optional[_Union[IfcModelObject.Type, str]] = ..., ifc_file: _Optional[int] = ..., ifc_type: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
