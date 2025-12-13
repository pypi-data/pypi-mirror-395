from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DynamicAnalysis(_message.Message):
    __slots__ = ("MODAL", "SPECTRAL", "TIME_HISTORY", "PUSHOVER", "HARMONIC_RESPONSE", "id_for_export_import", "metadata_for_export_import")
    MODAL_FIELD_NUMBER: _ClassVar[int]
    SPECTRAL_FIELD_NUMBER: _ClassVar[int]
    TIME_HISTORY_FIELD_NUMBER: _ClassVar[int]
    PUSHOVER_FIELD_NUMBER: _ClassVar[int]
    HARMONIC_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    MODAL: bool
    SPECTRAL: bool
    TIME_HISTORY: bool
    PUSHOVER: bool
    HARMONIC_RESPONSE: bool
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, MODAL: bool = ..., SPECTRAL: bool = ..., TIME_HISTORY: bool = ..., PUSHOVER: bool = ..., HARMONIC_RESPONSE: bool = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
