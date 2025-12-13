from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Subpanel(_message.Message):
    __slots__ = ("no", "elements", "comment", "is_generated", "generating_object_info", "subpanel_type", "restrained_at_start", "restrained_at_end", "delta_start", "delta_end", "width", "thickness", "ct_ratio", "id_for_export_import", "metadata_for_export_import")
    class SubpanelType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUBPANEL_TYPE_STRAIGHT: _ClassVar[Subpanel.SubpanelType]
        SUBPANEL_TYPE_ARC: _ClassVar[Subpanel.SubpanelType]
        SUBPANEL_TYPE_CIRCLE: _ClassVar[Subpanel.SubpanelType]
    SUBPANEL_TYPE_STRAIGHT: Subpanel.SubpanelType
    SUBPANEL_TYPE_ARC: Subpanel.SubpanelType
    SUBPANEL_TYPE_CIRCLE: Subpanel.SubpanelType
    NO_FIELD_NUMBER: _ClassVar[int]
    ELEMENTS_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    SUBPANEL_TYPE_FIELD_NUMBER: _ClassVar[int]
    RESTRAINED_AT_START_FIELD_NUMBER: _ClassVar[int]
    RESTRAINED_AT_END_FIELD_NUMBER: _ClassVar[int]
    DELTA_START_FIELD_NUMBER: _ClassVar[int]
    DELTA_END_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    THICKNESS_FIELD_NUMBER: _ClassVar[int]
    CT_RATIO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    elements: _containers.RepeatedScalarFieldContainer[int]
    comment: str
    is_generated: bool
    generating_object_info: str
    subpanel_type: Subpanel.SubpanelType
    restrained_at_start: bool
    restrained_at_end: bool
    delta_start: float
    delta_end: float
    width: float
    thickness: float
    ct_ratio: float
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., elements: _Optional[_Iterable[int]] = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., subpanel_type: _Optional[_Union[Subpanel.SubpanelType, str]] = ..., restrained_at_start: bool = ..., restrained_at_end: bool = ..., delta_start: _Optional[float] = ..., delta_end: _Optional[float] = ..., width: _Optional[float] = ..., thickness: _Optional[float] = ..., ct_ratio: _Optional[float] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
