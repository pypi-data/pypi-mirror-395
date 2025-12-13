from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NodalLink(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "assigned_nodes", "linking_to_nodes_allowed", "linking_to_members_allowed", "linking_to_surfaces_allowed", "include_related_objects", "nodes_excluded_from_search", "members_exclued_from_search", "surfaces_excluded_from_search", "search_method", "search_radius", "member_hinge_start", "member_hinge_end", "parameters", "comment", "is_generated", "generating_object_info", "id_for_export_import", "metadata_for_export_import")
    class SearchMethod(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SEARCH_METHOD_CLOSEST_OBJECTS: _ClassVar[NodalLink.SearchMethod]
    SEARCH_METHOD_CLOSEST_OBJECTS: NodalLink.SearchMethod
    class ParametersTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[NodalLink.ParametersTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[NodalLink.ParametersTreeTableRow, _Mapping]]] = ...) -> None: ...
    class ParametersTreeTableRow(_message.Message):
        __slots__ = ("key", "caption", "symbol", "value", "unit", "rows")
        KEY_FIELD_NUMBER: _ClassVar[int]
        CAPTION_FIELD_NUMBER: _ClassVar[int]
        SYMBOL_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        UNIT_FIELD_NUMBER: _ClassVar[int]
        ROWS_FIELD_NUMBER: _ClassVar[int]
        key: str
        caption: str
        symbol: str
        value: _common_pb2.Value
        unit: str
        rows: _containers.RepeatedCompositeFieldContainer[NodalLink.ParametersTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[NodalLink.ParametersTreeTableRow, _Mapping]]] = ...) -> None: ...
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_NODES_FIELD_NUMBER: _ClassVar[int]
    LINKING_TO_NODES_ALLOWED_FIELD_NUMBER: _ClassVar[int]
    LINKING_TO_MEMBERS_ALLOWED_FIELD_NUMBER: _ClassVar[int]
    LINKING_TO_SURFACES_ALLOWED_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_RELATED_OBJECTS_FIELD_NUMBER: _ClassVar[int]
    NODES_EXCLUDED_FROM_SEARCH_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_EXCLUED_FROM_SEARCH_FIELD_NUMBER: _ClassVar[int]
    SURFACES_EXCLUDED_FROM_SEARCH_FIELD_NUMBER: _ClassVar[int]
    SEARCH_METHOD_FIELD_NUMBER: _ClassVar[int]
    SEARCH_RADIUS_FIELD_NUMBER: _ClassVar[int]
    MEMBER_HINGE_START_FIELD_NUMBER: _ClassVar[int]
    MEMBER_HINGE_END_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    assigned_nodes: _containers.RepeatedScalarFieldContainer[int]
    linking_to_nodes_allowed: bool
    linking_to_members_allowed: bool
    linking_to_surfaces_allowed: bool
    include_related_objects: bool
    nodes_excluded_from_search: _containers.RepeatedScalarFieldContainer[int]
    members_exclued_from_search: _containers.RepeatedScalarFieldContainer[int]
    surfaces_excluded_from_search: _containers.RepeatedScalarFieldContainer[int]
    search_method: NodalLink.SearchMethod
    search_radius: float
    member_hinge_start: int
    member_hinge_end: int
    parameters: NodalLink.ParametersTreeTable
    comment: str
    is_generated: bool
    generating_object_info: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., assigned_nodes: _Optional[_Iterable[int]] = ..., linking_to_nodes_allowed: bool = ..., linking_to_members_allowed: bool = ..., linking_to_surfaces_allowed: bool = ..., include_related_objects: bool = ..., nodes_excluded_from_search: _Optional[_Iterable[int]] = ..., members_exclued_from_search: _Optional[_Iterable[int]] = ..., surfaces_excluded_from_search: _Optional[_Iterable[int]] = ..., search_method: _Optional[_Union[NodalLink.SearchMethod, str]] = ..., search_radius: _Optional[float] = ..., member_hinge_start: _Optional[int] = ..., member_hinge_end: _Optional[int] = ..., parameters: _Optional[_Union[NodalLink.ParametersTreeTable, _Mapping]] = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
