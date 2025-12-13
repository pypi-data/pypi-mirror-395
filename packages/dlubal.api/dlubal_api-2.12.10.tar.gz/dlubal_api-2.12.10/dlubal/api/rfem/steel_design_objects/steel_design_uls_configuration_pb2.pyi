from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SteelDesignUlsConfiguration(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "assigned_to_all_members", "assigned_to_members", "assigned_to_all_member_sets", "assigned_to_member_sets", "assigned_to_all_surfaces", "assigned_to_surfaces", "assigned_to_all_surface_sets", "assigned_to_surface_sets", "assigned_to_all_deep_beams", "assigned_to_deep_beams", "assigned_to_all_shear_walls", "assigned_to_shear_walls", "settings_ec3", "settings_aisc", "settings_bs5", "settings_gb50017", "settings_sia", "settings_csa", "settings_sans", "settings_sp16", "settings_is", "settings_nbr", "settings_as4100", "settings_ntc", "surfaces_settings_ec3", "surfaces_settings_aisc", "surfaces_settings_bs5", "surfaces_settings_gb50017", "surfaces_settings_sia", "surfaces_settings_csa", "surfaces_settings_sans", "surfaces_settings_sp16", "surfaces_settings_is", "surfaces_settings_nbr", "surfaces_settings_as4100", "surfaces_settings_ntc", "standard_parameters", "comment", "standard_parameters_tree", "id_for_export_import", "metadata_for_export_import")
    class SettingsEc3TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SettingsEc3TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SettingsEc3TreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SettingsEc3TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SettingsEc3TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsAiscTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SettingsAiscTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SettingsAiscTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SettingsAiscTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SettingsAiscTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsBs5TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SettingsBs5TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SettingsBs5TreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SettingsBs5TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SettingsBs5TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsGb50017TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SettingsGb50017TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SettingsGb50017TreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SettingsGb50017TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SettingsGb50017TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsSiaTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SettingsSiaTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SettingsSiaTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SettingsSiaTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SettingsSiaTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsCsaTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SettingsCsaTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SettingsCsaTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SettingsCsaTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SettingsCsaTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsSansTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SettingsSansTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SettingsSansTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SettingsSansTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SettingsSansTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsSp16TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SettingsSp16TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SettingsSp16TreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SettingsSp16TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SettingsSp16TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsIsTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SettingsIsTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SettingsIsTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SettingsIsTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SettingsIsTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsNbrTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SettingsNbrTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SettingsNbrTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SettingsNbrTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SettingsNbrTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsAs4100TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SettingsAs4100TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SettingsAs4100TreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SettingsAs4100TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SettingsAs4100TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsNtcTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SettingsNtcTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SettingsNtcTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SettingsNtcTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SettingsNtcTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsEc3TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SurfacesSettingsEc3TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SurfacesSettingsEc3TreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SurfacesSettingsEc3TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SurfacesSettingsEc3TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsAiscTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SurfacesSettingsAiscTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SurfacesSettingsAiscTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SurfacesSettingsAiscTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SurfacesSettingsAiscTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsBs5TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SurfacesSettingsBs5TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SurfacesSettingsBs5TreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SurfacesSettingsBs5TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SurfacesSettingsBs5TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsGb50017TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SurfacesSettingsGb50017TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SurfacesSettingsGb50017TreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SurfacesSettingsGb50017TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SurfacesSettingsGb50017TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsSiaTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SurfacesSettingsSiaTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SurfacesSettingsSiaTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SurfacesSettingsSiaTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SurfacesSettingsSiaTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsCsaTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SurfacesSettingsCsaTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SurfacesSettingsCsaTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SurfacesSettingsCsaTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SurfacesSettingsCsaTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsSansTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SurfacesSettingsSansTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SurfacesSettingsSansTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SurfacesSettingsSansTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SurfacesSettingsSansTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsSp16TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SurfacesSettingsSp16TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SurfacesSettingsSp16TreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SurfacesSettingsSp16TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SurfacesSettingsSp16TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsIsTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SurfacesSettingsIsTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SurfacesSettingsIsTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SurfacesSettingsIsTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SurfacesSettingsIsTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsNbrTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SurfacesSettingsNbrTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SurfacesSettingsNbrTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SurfacesSettingsNbrTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SurfacesSettingsNbrTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsAs4100TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SurfacesSettingsAs4100TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SurfacesSettingsAs4100TreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SurfacesSettingsAs4100TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SurfacesSettingsAs4100TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsNtcTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SurfacesSettingsNtcTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SurfacesSettingsNtcTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.SurfacesSettingsNtcTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.SurfacesSettingsNtcTreeTableRow, _Mapping]]] = ...) -> None: ...
    class StandardParametersTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.StandardParametersTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.StandardParametersTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.StandardParametersTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.StandardParametersTreeTableRow, _Mapping]]] = ...) -> None: ...
    class StandardParametersTreeTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.StandardParametersTreeTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.StandardParametersTreeTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[SteelDesignUlsConfiguration.StandardParametersTreeTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., description: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., note: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SteelDesignUlsConfiguration.StandardParametersTreeTreeTableRow, _Mapping]]] = ...) -> None: ...
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
    ASSIGNED_TO_ALL_DEEP_BEAMS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_DEEP_BEAMS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_ALL_SHEAR_WALLS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_SHEAR_WALLS_FIELD_NUMBER: _ClassVar[int]
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
    assigned_to_all_deep_beams: bool
    assigned_to_deep_beams: _containers.RepeatedScalarFieldContainer[int]
    assigned_to_all_shear_walls: bool
    assigned_to_shear_walls: _containers.RepeatedScalarFieldContainer[int]
    settings_ec3: SteelDesignUlsConfiguration.SettingsEc3TreeTable
    settings_aisc: SteelDesignUlsConfiguration.SettingsAiscTreeTable
    settings_bs5: SteelDesignUlsConfiguration.SettingsBs5TreeTable
    settings_gb50017: SteelDesignUlsConfiguration.SettingsGb50017TreeTable
    settings_sia: SteelDesignUlsConfiguration.SettingsSiaTreeTable
    settings_csa: SteelDesignUlsConfiguration.SettingsCsaTreeTable
    settings_sans: SteelDesignUlsConfiguration.SettingsSansTreeTable
    settings_sp16: SteelDesignUlsConfiguration.SettingsSp16TreeTable
    settings_is: SteelDesignUlsConfiguration.SettingsIsTreeTable
    settings_nbr: SteelDesignUlsConfiguration.SettingsNbrTreeTable
    settings_as4100: SteelDesignUlsConfiguration.SettingsAs4100TreeTable
    settings_ntc: SteelDesignUlsConfiguration.SettingsNtcTreeTable
    surfaces_settings_ec3: SteelDesignUlsConfiguration.SurfacesSettingsEc3TreeTable
    surfaces_settings_aisc: SteelDesignUlsConfiguration.SurfacesSettingsAiscTreeTable
    surfaces_settings_bs5: SteelDesignUlsConfiguration.SurfacesSettingsBs5TreeTable
    surfaces_settings_gb50017: SteelDesignUlsConfiguration.SurfacesSettingsGb50017TreeTable
    surfaces_settings_sia: SteelDesignUlsConfiguration.SurfacesSettingsSiaTreeTable
    surfaces_settings_csa: SteelDesignUlsConfiguration.SurfacesSettingsCsaTreeTable
    surfaces_settings_sans: SteelDesignUlsConfiguration.SurfacesSettingsSansTreeTable
    surfaces_settings_sp16: SteelDesignUlsConfiguration.SurfacesSettingsSp16TreeTable
    surfaces_settings_is: SteelDesignUlsConfiguration.SurfacesSettingsIsTreeTable
    surfaces_settings_nbr: SteelDesignUlsConfiguration.SurfacesSettingsNbrTreeTable
    surfaces_settings_as4100: SteelDesignUlsConfiguration.SurfacesSettingsAs4100TreeTable
    surfaces_settings_ntc: SteelDesignUlsConfiguration.SurfacesSettingsNtcTreeTable
    standard_parameters: SteelDesignUlsConfiguration.StandardParametersTreeTable
    comment: str
    standard_parameters_tree: SteelDesignUlsConfiguration.StandardParametersTreeTreeTable
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., assigned_to_all_members: bool = ..., assigned_to_members: _Optional[_Iterable[int]] = ..., assigned_to_all_member_sets: bool = ..., assigned_to_member_sets: _Optional[_Iterable[int]] = ..., assigned_to_all_surfaces: bool = ..., assigned_to_surfaces: _Optional[_Iterable[int]] = ..., assigned_to_all_surface_sets: bool = ..., assigned_to_surface_sets: _Optional[_Iterable[int]] = ..., assigned_to_all_deep_beams: bool = ..., assigned_to_deep_beams: _Optional[_Iterable[int]] = ..., assigned_to_all_shear_walls: bool = ..., assigned_to_shear_walls: _Optional[_Iterable[int]] = ..., settings_ec3: _Optional[_Union[SteelDesignUlsConfiguration.SettingsEc3TreeTable, _Mapping]] = ..., settings_aisc: _Optional[_Union[SteelDesignUlsConfiguration.SettingsAiscTreeTable, _Mapping]] = ..., settings_bs5: _Optional[_Union[SteelDesignUlsConfiguration.SettingsBs5TreeTable, _Mapping]] = ..., settings_gb50017: _Optional[_Union[SteelDesignUlsConfiguration.SettingsGb50017TreeTable, _Mapping]] = ..., settings_sia: _Optional[_Union[SteelDesignUlsConfiguration.SettingsSiaTreeTable, _Mapping]] = ..., settings_csa: _Optional[_Union[SteelDesignUlsConfiguration.SettingsCsaTreeTable, _Mapping]] = ..., settings_sans: _Optional[_Union[SteelDesignUlsConfiguration.SettingsSansTreeTable, _Mapping]] = ..., settings_sp16: _Optional[_Union[SteelDesignUlsConfiguration.SettingsSp16TreeTable, _Mapping]] = ..., settings_is: _Optional[_Union[SteelDesignUlsConfiguration.SettingsIsTreeTable, _Mapping]] = ..., settings_nbr: _Optional[_Union[SteelDesignUlsConfiguration.SettingsNbrTreeTable, _Mapping]] = ..., settings_as4100: _Optional[_Union[SteelDesignUlsConfiguration.SettingsAs4100TreeTable, _Mapping]] = ..., settings_ntc: _Optional[_Union[SteelDesignUlsConfiguration.SettingsNtcTreeTable, _Mapping]] = ..., surfaces_settings_ec3: _Optional[_Union[SteelDesignUlsConfiguration.SurfacesSettingsEc3TreeTable, _Mapping]] = ..., surfaces_settings_aisc: _Optional[_Union[SteelDesignUlsConfiguration.SurfacesSettingsAiscTreeTable, _Mapping]] = ..., surfaces_settings_bs5: _Optional[_Union[SteelDesignUlsConfiguration.SurfacesSettingsBs5TreeTable, _Mapping]] = ..., surfaces_settings_gb50017: _Optional[_Union[SteelDesignUlsConfiguration.SurfacesSettingsGb50017TreeTable, _Mapping]] = ..., surfaces_settings_sia: _Optional[_Union[SteelDesignUlsConfiguration.SurfacesSettingsSiaTreeTable, _Mapping]] = ..., surfaces_settings_csa: _Optional[_Union[SteelDesignUlsConfiguration.SurfacesSettingsCsaTreeTable, _Mapping]] = ..., surfaces_settings_sans: _Optional[_Union[SteelDesignUlsConfiguration.SurfacesSettingsSansTreeTable, _Mapping]] = ..., surfaces_settings_sp16: _Optional[_Union[SteelDesignUlsConfiguration.SurfacesSettingsSp16TreeTable, _Mapping]] = ..., surfaces_settings_is: _Optional[_Union[SteelDesignUlsConfiguration.SurfacesSettingsIsTreeTable, _Mapping]] = ..., surfaces_settings_nbr: _Optional[_Union[SteelDesignUlsConfiguration.SurfacesSettingsNbrTreeTable, _Mapping]] = ..., surfaces_settings_as4100: _Optional[_Union[SteelDesignUlsConfiguration.SurfacesSettingsAs4100TreeTable, _Mapping]] = ..., surfaces_settings_ntc: _Optional[_Union[SteelDesignUlsConfiguration.SurfacesSettingsNtcTreeTable, _Mapping]] = ..., standard_parameters: _Optional[_Union[SteelDesignUlsConfiguration.StandardParametersTreeTable, _Mapping]] = ..., comment: _Optional[str] = ..., standard_parameters_tree: _Optional[_Union[SteelDesignUlsConfiguration.StandardParametersTreeTreeTable, _Mapping]] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
