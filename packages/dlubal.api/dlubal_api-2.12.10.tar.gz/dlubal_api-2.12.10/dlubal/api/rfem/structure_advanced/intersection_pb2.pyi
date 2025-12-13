from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Intersection(_message.Message):
    __slots__ = ("no", "surface_a", "surface_b", "generated_nodes", "generated_lines", "comment", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    SURFACE_A_FIELD_NUMBER: _ClassVar[int]
    SURFACE_B_FIELD_NUMBER: _ClassVar[int]
    GENERATED_NODES_FIELD_NUMBER: _ClassVar[int]
    GENERATED_LINES_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    surface_a: int
    surface_b: int
    generated_nodes: _containers.RepeatedScalarFieldContainer[int]
    generated_lines: _containers.RepeatedScalarFieldContainer[int]
    comment: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., surface_a: _Optional[int] = ..., surface_b: _Optional[int] = ..., generated_nodes: _Optional[_Iterable[int]] = ..., generated_lines: _Optional[_Iterable[int]] = ..., comment: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
