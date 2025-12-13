from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ImportSupportReactions(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "is_generated", "generating_object_info", "connected_model_uid", "objects_connection_type", "import_from_supported_nodes_no", "import_from_all_supported_nodes", "import_from_supported_lines_no", "import_from_all_supported_lines", "import_to_nodes_no", "import_to_lines_no", "import_to_surfaces_no", "import_to_all_surfaces", "create_member_loads_instead_of_line_loads", "loading_connection_type", "connected_loading", "load_distribution", "comment", "id_for_export_import", "metadata_for_export_import")
    class ObjectsConnectionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        OBJECTS_CONNECTION_TYPE_MANUALLY: _ClassVar[ImportSupportReactions.ObjectsConnectionType]
    OBJECTS_CONNECTION_TYPE_MANUALLY: ImportSupportReactions.ObjectsConnectionType
    class LoadingConnectionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LOADING_CONNECTION_TYPE_MANUALLY: _ClassVar[ImportSupportReactions.LoadingConnectionType]
        LOADING_CONNECTION_TYPE_AUTOMATICALLY: _ClassVar[ImportSupportReactions.LoadingConnectionType]
    LOADING_CONNECTION_TYPE_MANUALLY: ImportSupportReactions.LoadingConnectionType
    LOADING_CONNECTION_TYPE_AUTOMATICALLY: ImportSupportReactions.LoadingConnectionType
    class LoadDistribution(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LOAD_DISTRIBUTION_UNKNOWN: _ClassVar[ImportSupportReactions.LoadDistribution]
        LOAD_DISTRIBUTION_UNIFORM_TOTAL: _ClassVar[ImportSupportReactions.LoadDistribution]
        LOAD_DISTRIBUTION_VARYING: _ClassVar[ImportSupportReactions.LoadDistribution]
    LOAD_DISTRIBUTION_UNKNOWN: ImportSupportReactions.LoadDistribution
    LOAD_DISTRIBUTION_UNIFORM_TOTAL: ImportSupportReactions.LoadDistribution
    LOAD_DISTRIBUTION_VARYING: ImportSupportReactions.LoadDistribution
    class ConnectedLoadingTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[ImportSupportReactions.ConnectedLoadingRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[ImportSupportReactions.ConnectedLoadingRow, _Mapping]]] = ...) -> None: ...
    class ConnectedLoadingRow(_message.Message):
        __slots__ = ("no", "description", "from_loading", "to_loading")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        FROM_LOADING_FIELD_NUMBER: _ClassVar[int]
        TO_LOADING_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        from_loading: int
        to_loading: int
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., from_loading: _Optional[int] = ..., to_loading: _Optional[int] = ...) -> None: ...
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    CONNECTED_MODEL_UID_FIELD_NUMBER: _ClassVar[int]
    OBJECTS_CONNECTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    IMPORT_FROM_SUPPORTED_NODES_NO_FIELD_NUMBER: _ClassVar[int]
    IMPORT_FROM_ALL_SUPPORTED_NODES_FIELD_NUMBER: _ClassVar[int]
    IMPORT_FROM_SUPPORTED_LINES_NO_FIELD_NUMBER: _ClassVar[int]
    IMPORT_FROM_ALL_SUPPORTED_LINES_FIELD_NUMBER: _ClassVar[int]
    IMPORT_TO_NODES_NO_FIELD_NUMBER: _ClassVar[int]
    IMPORT_TO_LINES_NO_FIELD_NUMBER: _ClassVar[int]
    IMPORT_TO_SURFACES_NO_FIELD_NUMBER: _ClassVar[int]
    IMPORT_TO_ALL_SURFACES_FIELD_NUMBER: _ClassVar[int]
    CREATE_MEMBER_LOADS_INSTEAD_OF_LINE_LOADS_FIELD_NUMBER: _ClassVar[int]
    LOADING_CONNECTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    CONNECTED_LOADING_FIELD_NUMBER: _ClassVar[int]
    LOAD_DISTRIBUTION_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    is_generated: bool
    generating_object_info: str
    connected_model_uid: str
    objects_connection_type: ImportSupportReactions.ObjectsConnectionType
    import_from_supported_nodes_no: str
    import_from_all_supported_nodes: bool
    import_from_supported_lines_no: str
    import_from_all_supported_lines: bool
    import_to_nodes_no: _containers.RepeatedScalarFieldContainer[int]
    import_to_lines_no: _containers.RepeatedScalarFieldContainer[int]
    import_to_surfaces_no: _containers.RepeatedScalarFieldContainer[int]
    import_to_all_surfaces: bool
    create_member_loads_instead_of_line_loads: bool
    loading_connection_type: ImportSupportReactions.LoadingConnectionType
    connected_loading: ImportSupportReactions.ConnectedLoadingTable
    load_distribution: ImportSupportReactions.LoadDistribution
    comment: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., connected_model_uid: _Optional[str] = ..., objects_connection_type: _Optional[_Union[ImportSupportReactions.ObjectsConnectionType, str]] = ..., import_from_supported_nodes_no: _Optional[str] = ..., import_from_all_supported_nodes: bool = ..., import_from_supported_lines_no: _Optional[str] = ..., import_from_all_supported_lines: bool = ..., import_to_nodes_no: _Optional[_Iterable[int]] = ..., import_to_lines_no: _Optional[_Iterable[int]] = ..., import_to_surfaces_no: _Optional[_Iterable[int]] = ..., import_to_all_surfaces: bool = ..., create_member_loads_instead_of_line_loads: bool = ..., loading_connection_type: _Optional[_Union[ImportSupportReactions.LoadingConnectionType, str]] = ..., connected_loading: _Optional[_Union[ImportSupportReactions.ConnectedLoadingTable, _Mapping]] = ..., load_distribution: _Optional[_Union[ImportSupportReactions.LoadDistribution, str]] = ..., comment: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
