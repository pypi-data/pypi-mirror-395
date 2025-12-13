from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NodalRelease(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "nodes", "nodal_release_type", "release_location", "released_members", "generated_released_objects", "deactivated", "define_release_type_for_each_object", "define_release_type_table", "is_generated", "generating_object_info", "comment", "id_for_export_import", "metadata_for_export_import")
    class ReleaseLocation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        RELEASE_LOCATION_ORIGIN: _ClassVar[NodalRelease.ReleaseLocation]
        RELEASE_LOCATION_RELEASED: _ClassVar[NodalRelease.ReleaseLocation]
    RELEASE_LOCATION_ORIGIN: NodalRelease.ReleaseLocation
    RELEASE_LOCATION_RELEASED: NodalRelease.ReleaseLocation
    class DefineReleaseTypeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[NodalRelease.DefineReleaseTypeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[NodalRelease.DefineReleaseTypeTableRow, _Mapping]]] = ...) -> None: ...
    class DefineReleaseTypeTableRow(_message.Message):
        __slots__ = ("no", "description", "object_no", "object_release_type")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        OBJECT_NO_FIELD_NUMBER: _ClassVar[int]
        OBJECT_RELEASE_TYPE_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        object_no: int
        object_release_type: int
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., object_no: _Optional[int] = ..., object_release_type: _Optional[int] = ...) -> None: ...
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NODES_FIELD_NUMBER: _ClassVar[int]
    NODAL_RELEASE_TYPE_FIELD_NUMBER: _ClassVar[int]
    RELEASE_LOCATION_FIELD_NUMBER: _ClassVar[int]
    RELEASED_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    GENERATED_RELEASED_OBJECTS_FIELD_NUMBER: _ClassVar[int]
    DEACTIVATED_FIELD_NUMBER: _ClassVar[int]
    DEFINE_RELEASE_TYPE_FOR_EACH_OBJECT_FIELD_NUMBER: _ClassVar[int]
    DEFINE_RELEASE_TYPE_TABLE_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    nodes: _containers.RepeatedScalarFieldContainer[int]
    nodal_release_type: int
    release_location: NodalRelease.ReleaseLocation
    released_members: _containers.RepeatedScalarFieldContainer[int]
    generated_released_objects: _containers.RepeatedScalarFieldContainer[int]
    deactivated: bool
    define_release_type_for_each_object: bool
    define_release_type_table: NodalRelease.DefineReleaseTypeTable
    is_generated: bool
    generating_object_info: str
    comment: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., nodes: _Optional[_Iterable[int]] = ..., nodal_release_type: _Optional[int] = ..., release_location: _Optional[_Union[NodalRelease.ReleaseLocation, str]] = ..., released_members: _Optional[_Iterable[int]] = ..., generated_released_objects: _Optional[_Iterable[int]] = ..., deactivated: bool = ..., define_release_type_for_each_object: bool = ..., define_release_type_table: _Optional[_Union[NodalRelease.DefineReleaseTypeTable, _Mapping]] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., comment: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
