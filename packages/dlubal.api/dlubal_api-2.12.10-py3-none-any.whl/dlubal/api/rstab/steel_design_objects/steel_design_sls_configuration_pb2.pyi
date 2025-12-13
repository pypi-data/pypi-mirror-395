from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SteelDesignSlsConfiguration(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "assigned_to_all_members", "assigned_to_members", "assigned_to_all_member_sets", "assigned_to_member_sets", "assigned_to_all_surfaces", "assigned_to_surfaces", "assigned_to_all_surface_sets", "assigned_to_surface_sets", "settings_ec3", "settings_aisc", "settings_bs5", "settings_gb50017", "settings_sia", "settings_csa", "settings_sans", "settings_sp16", "settings_is", "settings_nbr", "settings_as4100", "settings_ntc", "surfaces_settings_ec3", "surfaces_settings_aisc", "surfaces_settings_bs5", "surfaces_settings_gb50017", "surfaces_settings_sia", "surfaces_settings_csa", "surfaces_settings_sans", "surfaces_settings_sp16", "surfaces_settings_is", "surfaces_settings_nbr", "surfaces_settings_as4100", "surfaces_settings_ntc", "standard_parameters", "comment", "standard_parameters_tree", "id_for_export_import", "metadata_for_export_import")
    class SettingsEc3TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SettingsEc3TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SettingsEc3TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsEc3TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SettingsEc3TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SettingsEc3TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsAiscTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SettingsAiscTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SettingsAiscTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsAiscTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SettingsAiscTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SettingsAiscTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsBs5TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SettingsBs5TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SettingsBs5TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsBs5TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SettingsBs5TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SettingsBs5TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsGb50017TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SettingsGb50017TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SettingsGb50017TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsGb50017TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SettingsGb50017TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SettingsGb50017TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsSiaTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SettingsSiaTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SettingsSiaTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsSiaTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SettingsSiaTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SettingsSiaTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsCsaTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SettingsCsaTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SettingsCsaTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsCsaTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SettingsCsaTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SettingsCsaTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsSansTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SettingsSansTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SettingsSansTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsSansTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SettingsSansTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SettingsSansTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsSp16TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SettingsSp16TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SettingsSp16TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsSp16TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SettingsSp16TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SettingsSp16TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsIsTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SettingsIsTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SettingsIsTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsIsTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SettingsIsTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SettingsIsTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsNbrTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SettingsNbrTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SettingsNbrTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsNbrTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SettingsNbrTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SettingsNbrTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsAs4100TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SettingsAs4100TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SettingsAs4100TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsAs4100TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SettingsAs4100TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SettingsAs4100TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsNtcTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SettingsNtcTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SettingsNtcTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsNtcTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SettingsNtcTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SettingsNtcTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsEc3TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SurfacesSettingsEc3TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SurfacesSettingsEc3TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsEc3TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SurfacesSettingsEc3TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SurfacesSettingsEc3TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsAiscTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SurfacesSettingsAiscTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SurfacesSettingsAiscTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsAiscTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SurfacesSettingsAiscTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SurfacesSettingsAiscTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsBs5TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SurfacesSettingsBs5TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SurfacesSettingsBs5TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsBs5TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SurfacesSettingsBs5TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SurfacesSettingsBs5TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsGb50017TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SurfacesSettingsGb50017TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SurfacesSettingsGb50017TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsGb50017TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SurfacesSettingsGb50017TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SurfacesSettingsGb50017TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsSiaTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SurfacesSettingsSiaTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SurfacesSettingsSiaTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsSiaTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SurfacesSettingsSiaTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SurfacesSettingsSiaTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsCsaTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SurfacesSettingsCsaTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SurfacesSettingsCsaTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsCsaTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SurfacesSettingsCsaTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SurfacesSettingsCsaTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsSansTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SurfacesSettingsSansTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SurfacesSettingsSansTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsSansTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SurfacesSettingsSansTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SurfacesSettingsSansTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsSp16TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SurfacesSettingsSp16TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SurfacesSettingsSp16TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsSp16TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SurfacesSettingsSp16TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SurfacesSettingsSp16TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsIsTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SurfacesSettingsIsTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SurfacesSettingsIsTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsIsTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SurfacesSettingsIsTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SurfacesSettingsIsTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsNbrTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SurfacesSettingsNbrTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SurfacesSettingsNbrTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsNbrTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SurfacesSettingsNbrTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SurfacesSettingsNbrTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsAs4100TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SurfacesSettingsAs4100TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SurfacesSettingsAs4100TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsAs4100TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SurfacesSettingsAs4100TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SurfacesSettingsAs4100TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsNtcTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SurfacesSettingsNtcTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SurfacesSettingsNtcTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsNtcTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.SurfacesSettingsNtcTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.SurfacesSettingsNtcTreeTableRow, _Mapping]]] = ...) -> None: ...
    class StandardParametersTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.StandardParametersTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.StandardParametersTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.StandardParametersTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.StandardParametersTreeTableRow, _Mapping]]] = ...) -> None: ...
    class StandardParametersTreeTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.StandardParametersTreeTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.StandardParametersTreeTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignSlsConfiguration.StandardParametersTreeTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., description: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., note: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignSlsConfiguration.StandardParametersTreeTreeTableRow, _Mapping]]] = ...) -> None: ...
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_ALL_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_ALL_MEMBER_SETS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_MEMBER_SETS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_ALL_SURFACES_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_SURFACES_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_ALL_SURFACE_SETS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_SURFACE_SETS_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_EC3_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_AISC_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_BS5_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_GB50017_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_SIA_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_CSA_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_SANS_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_SP16_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_IS_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_NBR_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_AS4100_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_NTC_FIELD_NUMBER: _ClassVar[int]
    SURFACES_SETTINGS_EC3_FIELD_NUMBER: _ClassVar[int]
    SURFACES_SETTINGS_AISC_FIELD_NUMBER: _ClassVar[int]
    SURFACES_SETTINGS_BS5_FIELD_NUMBER: _ClassVar[int]
    SURFACES_SETTINGS_GB50017_FIELD_NUMBER: _ClassVar[int]
    SURFACES_SETTINGS_SIA_FIELD_NUMBER: _ClassVar[int]
    SURFACES_SETTINGS_CSA_FIELD_NUMBER: _ClassVar[int]
    SURFACES_SETTINGS_SANS_FIELD_NUMBER: _ClassVar[int]
    SURFACES_SETTINGS_SP16_FIELD_NUMBER: _ClassVar[int]
    SURFACES_SETTINGS_IS_FIELD_NUMBER: _ClassVar[int]
    SURFACES_SETTINGS_NBR_FIELD_NUMBER: _ClassVar[int]
    SURFACES_SETTINGS_AS4100_FIELD_NUMBER: _ClassVar[int]
    SURFACES_SETTINGS_NTC_FIELD_NUMBER: _ClassVar[int]
    STANDARD_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    STANDARD_PARAMETERS_TREE_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    assigned_to_all_members: bool
    assigned_to_members: _containers.RepeatedScalarFieldContainer[int]
    assigned_to_all_member_sets: bool
    assigned_to_member_sets: _containers.RepeatedScalarFieldContainer[int]
    assigned_to_all_surfaces: bool
    assigned_to_surfaces: _containers.RepeatedScalarFieldContainer[int]
    assigned_to_all_surface_sets: bool
    assigned_to_surface_sets: _containers.RepeatedScalarFieldContainer[int]
    settings_ec3: SteelDesignSlsConfiguration.SettingsEc3TreeTable
    settings_aisc: SteelDesignSlsConfiguration.SettingsAiscTreeTable
    settings_bs5: SteelDesignSlsConfiguration.SettingsBs5TreeTable
    settings_gb50017: SteelDesignSlsConfiguration.SettingsGb50017TreeTable
    settings_sia: SteelDesignSlsConfiguration.SettingsSiaTreeTable
    settings_csa: SteelDesignSlsConfiguration.SettingsCsaTreeTable
    settings_sans: SteelDesignSlsConfiguration.SettingsSansTreeTable
    settings_sp16: SteelDesignSlsConfiguration.SettingsSp16TreeTable
    settings_is: SteelDesignSlsConfiguration.SettingsIsTreeTable
    settings_nbr: SteelDesignSlsConfiguration.SettingsNbrTreeTable
    settings_as4100: SteelDesignSlsConfiguration.SettingsAs4100TreeTable
    settings_ntc: SteelDesignSlsConfiguration.SettingsNtcTreeTable
    surfaces_settings_ec3: SteelDesignSlsConfiguration.SurfacesSettingsEc3TreeTable
    surfaces_settings_aisc: SteelDesignSlsConfiguration.SurfacesSettingsAiscTreeTable
    surfaces_settings_bs5: SteelDesignSlsConfiguration.SurfacesSettingsBs5TreeTable
    surfaces_settings_gb50017: SteelDesignSlsConfiguration.SurfacesSettingsGb50017TreeTable
    surfaces_settings_sia: SteelDesignSlsConfiguration.SurfacesSettingsSiaTreeTable
    surfaces_settings_csa: SteelDesignSlsConfiguration.SurfacesSettingsCsaTreeTable
    surfaces_settings_sans: SteelDesignSlsConfiguration.SurfacesSettingsSansTreeTable
    surfaces_settings_sp16: SteelDesignSlsConfiguration.SurfacesSettingsSp16TreeTable
    surfaces_settings_is: SteelDesignSlsConfiguration.SurfacesSettingsIsTreeTable
    surfaces_settings_nbr: SteelDesignSlsConfiguration.SurfacesSettingsNbrTreeTable
    surfaces_settings_as4100: SteelDesignSlsConfiguration.SurfacesSettingsAs4100TreeTable
    surfaces_settings_ntc: SteelDesignSlsConfiguration.SurfacesSettingsNtcTreeTable
    standard_parameters: SteelDesignSlsConfiguration.StandardParametersTreeTable
    comment: str
    standard_parameters_tree: SteelDesignSlsConfiguration.StandardParametersTreeTreeTable
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., assigned_to_all_members: bool = ..., assigned_to_members: _Optional[_Iterable[int]] = ..., assigned_to_all_member_sets: bool = ..., assigned_to_member_sets: _Optional[_Iterable[int]] = ..., assigned_to_all_surfaces: bool = ..., assigned_to_surfaces: _Optional[_Iterable[int]] = ..., assigned_to_all_surface_sets: bool = ..., assigned_to_surface_sets: _Optional[_Iterable[int]] = ..., settings_ec3: _Optional[_Union[SteelDesignSlsConfiguration.SettingsEc3TreeTable, _Mapping]] = ..., settings_aisc: _Optional[_Union[SteelDesignSlsConfiguration.SettingsAiscTreeTable, _Mapping]] = ..., settings_bs5: _Optional[_Union[SteelDesignSlsConfiguration.SettingsBs5TreeTable, _Mapping]] = ..., settings_gb50017: _Optional[_Union[SteelDesignSlsConfiguration.SettingsGb50017TreeTable, _Mapping]] = ..., settings_sia: _Optional[_Union[SteelDesignSlsConfiguration.SettingsSiaTreeTable, _Mapping]] = ..., settings_csa: _Optional[_Union[SteelDesignSlsConfiguration.SettingsCsaTreeTable, _Mapping]] = ..., settings_sans: _Optional[_Union[SteelDesignSlsConfiguration.SettingsSansTreeTable, _Mapping]] = ..., settings_sp16: _Optional[_Union[SteelDesignSlsConfiguration.SettingsSp16TreeTable, _Mapping]] = ..., settings_is: _Optional[_Union[SteelDesignSlsConfiguration.SettingsIsTreeTable, _Mapping]] = ..., settings_nbr: _Optional[_Union[SteelDesignSlsConfiguration.SettingsNbrTreeTable, _Mapping]] = ..., settings_as4100: _Optional[_Union[SteelDesignSlsConfiguration.SettingsAs4100TreeTable, _Mapping]] = ..., settings_ntc: _Optional[_Union[SteelDesignSlsConfiguration.SettingsNtcTreeTable, _Mapping]] = ..., surfaces_settings_ec3: _Optional[_Union[SteelDesignSlsConfiguration.SurfacesSettingsEc3TreeTable, _Mapping]] = ..., surfaces_settings_aisc: _Optional[_Union[SteelDesignSlsConfiguration.SurfacesSettingsAiscTreeTable, _Mapping]] = ..., surfaces_settings_bs5: _Optional[_Union[SteelDesignSlsConfiguration.SurfacesSettingsBs5TreeTable, _Mapping]] = ..., surfaces_settings_gb50017: _Optional[_Union[SteelDesignSlsConfiguration.SurfacesSettingsGb50017TreeTable, _Mapping]] = ..., surfaces_settings_sia: _Optional[_Union[SteelDesignSlsConfiguration.SurfacesSettingsSiaTreeTable, _Mapping]] = ..., surfaces_settings_csa: _Optional[_Union[SteelDesignSlsConfiguration.SurfacesSettingsCsaTreeTable, _Mapping]] = ..., surfaces_settings_sans: _Optional[_Union[SteelDesignSlsConfiguration.SurfacesSettingsSansTreeTable, _Mapping]] = ..., surfaces_settings_sp16: _Optional[_Union[SteelDesignSlsConfiguration.SurfacesSettingsSp16TreeTable, _Mapping]] = ..., surfaces_settings_is: _Optional[_Union[SteelDesignSlsConfiguration.SurfacesSettingsIsTreeTable, _Mapping]] = ..., surfaces_settings_nbr: _Optional[_Union[SteelDesignSlsConfiguration.SurfacesSettingsNbrTreeTable, _Mapping]] = ..., surfaces_settings_as4100: _Optional[_Union[SteelDesignSlsConfiguration.SurfacesSettingsAs4100TreeTable, _Mapping]] = ..., surfaces_settings_ntc: _Optional[_Union[SteelDesignSlsConfiguration.SurfacesSettingsNtcTreeTable, _Mapping]] = ..., standard_parameters: _Optional[_Union[SteelDesignSlsConfiguration.StandardParametersTreeTable, _Mapping]] = ..., comment: _Optional[str] = ..., standard_parameters_tree: _Optional[_Union[SteelDesignSlsConfiguration.StandardParametersTreeTreeTable, _Mapping]] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
