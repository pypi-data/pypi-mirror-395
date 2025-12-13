from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GlassDesignUlsConfiguration(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "assigned_to_all_surfaces", "assigned_to_surfaces", "assigned_to_all_solids", "assigned_to_solids", "assigned_to_all_solid_sets", "assigned_to_solid_sets", "surfaces_settings_astm", "surfaces_settings_din", "surfaces_settings_none", "solids_settings_astm", "solids_settings_din", "solids_settings_none", "standard_parameters", "comment", "standard_parameters_tree", "id_for_export_import", "metadata_for_export_import")
    class SurfacesSettingsAstmTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[GlassDesignUlsConfiguration.SurfacesSettingsAstmTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[GlassDesignUlsConfiguration.SurfacesSettingsAstmTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsAstmTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[GlassDesignUlsConfiguration.SurfacesSettingsAstmTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[GlassDesignUlsConfiguration.SurfacesSettingsAstmTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsDinTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[GlassDesignUlsConfiguration.SurfacesSettingsDinTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[GlassDesignUlsConfiguration.SurfacesSettingsDinTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsDinTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[GlassDesignUlsConfiguration.SurfacesSettingsDinTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[GlassDesignUlsConfiguration.SurfacesSettingsDinTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsNoneTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[GlassDesignUlsConfiguration.SurfacesSettingsNoneTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[GlassDesignUlsConfiguration.SurfacesSettingsNoneTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsNoneTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[GlassDesignUlsConfiguration.SurfacesSettingsNoneTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[GlassDesignUlsConfiguration.SurfacesSettingsNoneTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SolidsSettingsAstmTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[GlassDesignUlsConfiguration.SolidsSettingsAstmTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[GlassDesignUlsConfiguration.SolidsSettingsAstmTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SolidsSettingsAstmTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[GlassDesignUlsConfiguration.SolidsSettingsAstmTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[GlassDesignUlsConfiguration.SolidsSettingsAstmTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SolidsSettingsDinTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[GlassDesignUlsConfiguration.SolidsSettingsDinTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[GlassDesignUlsConfiguration.SolidsSettingsDinTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SolidsSettingsDinTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[GlassDesignUlsConfiguration.SolidsSettingsDinTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[GlassDesignUlsConfiguration.SolidsSettingsDinTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SolidsSettingsNoneTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[GlassDesignUlsConfiguration.SolidsSettingsNoneTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[GlassDesignUlsConfiguration.SolidsSettingsNoneTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SolidsSettingsNoneTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[GlassDesignUlsConfiguration.SolidsSettingsNoneTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[GlassDesignUlsConfiguration.SolidsSettingsNoneTreeTableRow, _Mapping]]] = ...) -> None: ...
    class StandardParametersTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[GlassDesignUlsConfiguration.StandardParametersTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[GlassDesignUlsConfiguration.StandardParametersTreeTableRow, _Mapping]]] = ...) -> None: ...
    class StandardParametersTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[GlassDesignUlsConfiguration.StandardParametersTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[GlassDesignUlsConfiguration.StandardParametersTreeTableRow, _Mapping]]] = ...) -> None: ...
    class StandardParametersTreeTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[GlassDesignUlsConfiguration.StandardParametersTreeTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[GlassDesignUlsConfiguration.StandardParametersTreeTreeTableRow, _Mapping]]] = ...) -> None: ...
    class StandardParametersTreeTreeTableRow(_message.Message):
        __slots__ = ("key", "description", "symbol", "value", "unit", "note", "rows")
        KEY_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        SYMBOL_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        UNIT_FIELD_NUMBER: _ClassVar[int]
        NOTE_FIELD_NUMBER: _ClassVar[int]
        ROWS_FIELD_NUMBER: _ClassVar[int]
        key: str
        description: str
        symbol: str
        value: _common_pb2.Value
        unit: str
        note: str
        rows: _containers.RepeatedCompositeFieldContainer[GlassDesignUlsConfiguration.StandardParametersTreeTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., description: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., note: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[GlassDesignUlsConfiguration.StandardParametersTreeTreeTableRow, _Mapping]]] = ...) -> None: ...
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_ALL_SURFACES_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_SURFACES_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_ALL_SOLIDS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_SOLIDS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_ALL_SOLID_SETS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_SOLID_SETS_FIELD_NUMBER: _ClassVar[int]
    SURFACES_SETTINGS_ASTM_FIELD_NUMBER: _ClassVar[int]
    SURFACES_SETTINGS_DIN_FIELD_NUMBER: _ClassVar[int]
    SURFACES_SETTINGS_NONE_FIELD_NUMBER: _ClassVar[int]
    SOLIDS_SETTINGS_ASTM_FIELD_NUMBER: _ClassVar[int]
    SOLIDS_SETTINGS_DIN_FIELD_NUMBER: _ClassVar[int]
    SOLIDS_SETTINGS_NONE_FIELD_NUMBER: _ClassVar[int]
    STANDARD_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    STANDARD_PARAMETERS_TREE_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    assigned_to_all_surfaces: bool
    assigned_to_surfaces: _containers.RepeatedScalarFieldContainer[int]
    assigned_to_all_solids: bool
    assigned_to_solids: _containers.RepeatedScalarFieldContainer[int]
    assigned_to_all_solid_sets: bool
    assigned_to_solid_sets: _containers.RepeatedScalarFieldContainer[int]
    surfaces_settings_astm: GlassDesignUlsConfiguration.SurfacesSettingsAstmTreeTable
    surfaces_settings_din: GlassDesignUlsConfiguration.SurfacesSettingsDinTreeTable
    surfaces_settings_none: GlassDesignUlsConfiguration.SurfacesSettingsNoneTreeTable
    solids_settings_astm: GlassDesignUlsConfiguration.SolidsSettingsAstmTreeTable
    solids_settings_din: GlassDesignUlsConfiguration.SolidsSettingsDinTreeTable
    solids_settings_none: GlassDesignUlsConfiguration.SolidsSettingsNoneTreeTable
    standard_parameters: GlassDesignUlsConfiguration.StandardParametersTreeTable
    comment: str
    standard_parameters_tree: GlassDesignUlsConfiguration.StandardParametersTreeTreeTable
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., assigned_to_all_surfaces: bool = ..., assigned_to_surfaces: _Optional[_Iterable[int]] = ..., assigned_to_all_solids: bool = ..., assigned_to_solids: _Optional[_Iterable[int]] = ..., assigned_to_all_solid_sets: bool = ..., assigned_to_solid_sets: _Optional[_Iterable[int]] = ..., surfaces_settings_astm: _Optional[_Union[GlassDesignUlsConfiguration.SurfacesSettingsAstmTreeTable, _Mapping]] = ..., surfaces_settings_din: _Optional[_Union[GlassDesignUlsConfiguration.SurfacesSettingsDinTreeTable, _Mapping]] = ..., surfaces_settings_none: _Optional[_Union[GlassDesignUlsConfiguration.SurfacesSettingsNoneTreeTable, _Mapping]] = ..., solids_settings_astm: _Optional[_Union[GlassDesignUlsConfiguration.SolidsSettingsAstmTreeTable, _Mapping]] = ..., solids_settings_din: _Optional[_Union[GlassDesignUlsConfiguration.SolidsSettingsDinTreeTable, _Mapping]] = ..., solids_settings_none: _Optional[_Union[GlassDesignUlsConfiguration.SolidsSettingsNoneTreeTable, _Mapping]] = ..., standard_parameters: _Optional[_Union[GlassDesignUlsConfiguration.StandardParametersTreeTable, _Mapping]] = ..., comment: _Optional[str] = ..., standard_parameters_tree: _Optional[_Union[GlassDesignUlsConfiguration.StandardParametersTreeTreeTable, _Mapping]] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
