from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LineLink(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "assigned_lines", "linking_to_lines_allowed", "linking_to_surfaces_allowed", "lines_excluded_from_search", "surfaces_excluded_from_search", "search_method", "search_radius", "line_hinge", "parameters", "comment", "is_generated", "generating_object_info", "id_for_export_import", "metadata_for_export_import")
    class SearchMethod(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SEARCH_METHOD_CLOSEST_OBJECTS: _ClassVar[LineLink.SearchMethod]
    SEARCH_METHOD_CLOSEST_OBJECTS: LineLink.SearchMethod
    class ParametersTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[LineLink.ParametersTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[LineLink.ParametersTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[LineLink.ParametersTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[LineLink.ParametersTreeTableRow, _Mapping]]] = ...) -> None: ...
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_LINES_FIELD_NUMBER: _ClassVar[int]
    LINKING_TO_LINES_ALLOWED_FIELD_NUMBER: _ClassVar[int]
    LINKING_TO_SURFACES_ALLOWED_FIELD_NUMBER: _ClassVar[int]
    LINES_EXCLUDED_FROM_SEARCH_FIELD_NUMBER: _ClassVar[int]
    SURFACES_EXCLUDED_FROM_SEARCH_FIELD_NUMBER: _ClassVar[int]
    SEARCH_METHOD_FIELD_NUMBER: _ClassVar[int]
    SEARCH_RADIUS_FIELD_NUMBER: _ClassVar[int]
    LINE_HINGE_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    assigned_lines: _containers.RepeatedScalarFieldContainer[int]
    linking_to_lines_allowed: bool
    linking_to_surfaces_allowed: bool
    lines_excluded_from_search: _containers.RepeatedScalarFieldContainer[int]
    surfaces_excluded_from_search: _containers.RepeatedScalarFieldContainer[int]
    search_method: LineLink.SearchMethod
    search_radius: float
    line_hinge: int
    parameters: LineLink.ParametersTreeTable
    comment: str
    is_generated: bool
    generating_object_info: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., assigned_lines: _Optional[_Iterable[int]] = ..., linking_to_lines_allowed: bool = ..., linking_to_surfaces_allowed: bool = ..., lines_excluded_from_search: _Optional[_Iterable[int]] = ..., surfaces_excluded_from_search: _Optional[_Iterable[int]] = ..., search_method: _Optional[_Union[LineLink.SearchMethod, str]] = ..., search_radius: _Optional[float] = ..., line_hinge: _Optional[int] = ..., parameters: _Optional[_Union[LineLink.ParametersTreeTable, _Mapping]] = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
