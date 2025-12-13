from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TimberDesignSlsConfiguration(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "assigned_to_all_members", "assigned_to_members", "assigned_to_all_member_sets", "assigned_to_member_sets", "settings_ec5", "settings_awc", "settings_gb50005", "settings_sia", "settings_csa", "settings_sans10163", "settings_sp64", "settings_nbr7190", "settings_as1720", "settings_ntc", "surfaces_settings_ec5", "surfaces_settings_awc", "surfaces_settings_gb50005", "surfaces_settings_sia", "surfaces_settings_csa", "surfaces_settings_sans10163", "surfaces_settings_sp64", "surfaces_settings_nbr7190", "surfaces_settings_as1720", "surfaces_settings_ntc", "standard_parameters", "comment", "standard_parameters_tree", "id_for_export_import", "metadata_for_export_import")
    class SettingsEc5TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SettingsEc5TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SettingsEc5TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsEc5TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SettingsEc5TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SettingsEc5TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsAwcTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SettingsAwcTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SettingsAwcTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsAwcTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SettingsAwcTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SettingsAwcTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsGb50005TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SettingsGb50005TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SettingsGb50005TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsGb50005TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SettingsGb50005TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SettingsGb50005TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsSiaTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SettingsSiaTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SettingsSiaTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SettingsSiaTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SettingsSiaTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsCsaTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SettingsCsaTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SettingsCsaTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SettingsCsaTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SettingsCsaTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsSans10163TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SettingsSans10163TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SettingsSans10163TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsSans10163TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SettingsSans10163TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SettingsSans10163TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsSp64TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SettingsSp64TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SettingsSp64TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsSp64TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SettingsSp64TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SettingsSp64TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsNbr7190TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SettingsNbr7190TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SettingsNbr7190TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsNbr7190TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SettingsNbr7190TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SettingsNbr7190TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsAs1720TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SettingsAs1720TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SettingsAs1720TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsAs1720TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SettingsAs1720TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SettingsAs1720TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsNtcTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SettingsNtcTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SettingsNtcTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SettingsNtcTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SettingsNtcTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsEc5TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SurfacesSettingsEc5TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SurfacesSettingsEc5TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsEc5TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SurfacesSettingsEc5TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SurfacesSettingsEc5TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsAwcTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SurfacesSettingsAwcTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SurfacesSettingsAwcTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsAwcTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SurfacesSettingsAwcTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SurfacesSettingsAwcTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsGb50005TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SurfacesSettingsGb50005TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SurfacesSettingsGb50005TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsGb50005TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SurfacesSettingsGb50005TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SurfacesSettingsGb50005TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsSiaTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SurfacesSettingsSiaTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SurfacesSettingsSiaTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SurfacesSettingsSiaTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SurfacesSettingsSiaTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsCsaTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SurfacesSettingsCsaTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SurfacesSettingsCsaTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SurfacesSettingsCsaTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SurfacesSettingsCsaTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsSans10163TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SurfacesSettingsSans10163TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SurfacesSettingsSans10163TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsSans10163TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SurfacesSettingsSans10163TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SurfacesSettingsSans10163TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsSp64TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SurfacesSettingsSp64TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SurfacesSettingsSp64TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsSp64TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SurfacesSettingsSp64TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SurfacesSettingsSp64TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsNbr7190TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SurfacesSettingsNbr7190TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SurfacesSettingsNbr7190TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsNbr7190TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SurfacesSettingsNbr7190TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SurfacesSettingsNbr7190TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsAs1720TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SurfacesSettingsAs1720TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SurfacesSettingsAs1720TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsAs1720TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SurfacesSettingsAs1720TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SurfacesSettingsAs1720TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsNtcTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SurfacesSettingsNtcTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SurfacesSettingsNtcTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.SurfacesSettingsNtcTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.SurfacesSettingsNtcTreeTableRow, _Mapping]]] = ...) -> None: ...
    class StandardParametersTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.StandardParametersTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.StandardParametersTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.StandardParametersTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.StandardParametersTreeTableRow, _Mapping]]] = ...) -> None: ...
    class StandardParametersTreeTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.StandardParametersTreeTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.StandardParametersTreeTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignSlsConfiguration.StandardParametersTreeTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., description: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., note: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignSlsConfiguration.StandardParametersTreeTreeTableRow, _Mapping]]] = ...) -> None: ...
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_ALL_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_ALL_MEMBER_SETS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_MEMBER_SETS_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_EC5_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_AWC_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_GB50005_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_SIA_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_CSA_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_SANS10163_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_SP64_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_NBR7190_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_AS1720_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_NTC_FIELD_NUMBER: _ClassVar[int]
    SURFACES_SETTINGS_EC5_FIELD_NUMBER: _ClassVar[int]
    SURFACES_SETTINGS_AWC_FIELD_NUMBER: _ClassVar[int]
    SURFACES_SETTINGS_GB50005_FIELD_NUMBER: _ClassVar[int]
    SURFACES_SETTINGS_SIA_FIELD_NUMBER: _ClassVar[int]
    SURFACES_SETTINGS_CSA_FIELD_NUMBER: _ClassVar[int]
    SURFACES_SETTINGS_SANS10163_FIELD_NUMBER: _ClassVar[int]
    SURFACES_SETTINGS_SP64_FIELD_NUMBER: _ClassVar[int]
    SURFACES_SETTINGS_NBR7190_FIELD_NUMBER: _ClassVar[int]
    SURFACES_SETTINGS_AS1720_FIELD_NUMBER: _ClassVar[int]
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
    settings_ec5: TimberDesignSlsConfiguration.SettingsEc5TreeTable
    settings_awc: TimberDesignSlsConfiguration.SettingsAwcTreeTable
    settings_gb50005: TimberDesignSlsConfiguration.SettingsGb50005TreeTable
    settings_sia: TimberDesignSlsConfiguration.SettingsSiaTreeTable
    settings_csa: TimberDesignSlsConfiguration.SettingsCsaTreeTable
    settings_sans10163: TimberDesignSlsConfiguration.SettingsSans10163TreeTable
    settings_sp64: TimberDesignSlsConfiguration.SettingsSp64TreeTable
    settings_nbr7190: TimberDesignSlsConfiguration.SettingsNbr7190TreeTable
    settings_as1720: TimberDesignSlsConfiguration.SettingsAs1720TreeTable
    settings_ntc: TimberDesignSlsConfiguration.SettingsNtcTreeTable
    surfaces_settings_ec5: TimberDesignSlsConfiguration.SurfacesSettingsEc5TreeTable
    surfaces_settings_awc: TimberDesignSlsConfiguration.SurfacesSettingsAwcTreeTable
    surfaces_settings_gb50005: TimberDesignSlsConfiguration.SurfacesSettingsGb50005TreeTable
    surfaces_settings_sia: TimberDesignSlsConfiguration.SurfacesSettingsSiaTreeTable
    surfaces_settings_csa: TimberDesignSlsConfiguration.SurfacesSettingsCsaTreeTable
    surfaces_settings_sans10163: TimberDesignSlsConfiguration.SurfacesSettingsSans10163TreeTable
    surfaces_settings_sp64: TimberDesignSlsConfiguration.SurfacesSettingsSp64TreeTable
    surfaces_settings_nbr7190: TimberDesignSlsConfiguration.SurfacesSettingsNbr7190TreeTable
    surfaces_settings_as1720: TimberDesignSlsConfiguration.SurfacesSettingsAs1720TreeTable
    surfaces_settings_ntc: TimberDesignSlsConfiguration.SurfacesSettingsNtcTreeTable
    standard_parameters: TimberDesignSlsConfiguration.StandardParametersTreeTable
    comment: str
    standard_parameters_tree: TimberDesignSlsConfiguration.StandardParametersTreeTreeTable
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., assigned_to_all_members: bool = ..., assigned_to_members: _Optional[_Iterable[int]] = ..., assigned_to_all_member_sets: bool = ..., assigned_to_member_sets: _Optional[_Iterable[int]] = ..., settings_ec5: _Optional[_Union[TimberDesignSlsConfiguration.SettingsEc5TreeTable, _Mapping]] = ..., settings_awc: _Optional[_Union[TimberDesignSlsConfiguration.SettingsAwcTreeTable, _Mapping]] = ..., settings_gb50005: _Optional[_Union[TimberDesignSlsConfiguration.SettingsGb50005TreeTable, _Mapping]] = ..., settings_sia: _Optional[_Union[TimberDesignSlsConfiguration.SettingsSiaTreeTable, _Mapping]] = ..., settings_csa: _Optional[_Union[TimberDesignSlsConfiguration.SettingsCsaTreeTable, _Mapping]] = ..., settings_sans10163: _Optional[_Union[TimberDesignSlsConfiguration.SettingsSans10163TreeTable, _Mapping]] = ..., settings_sp64: _Optional[_Union[TimberDesignSlsConfiguration.SettingsSp64TreeTable, _Mapping]] = ..., settings_nbr7190: _Optional[_Union[TimberDesignSlsConfiguration.SettingsNbr7190TreeTable, _Mapping]] = ..., settings_as1720: _Optional[_Union[TimberDesignSlsConfiguration.SettingsAs1720TreeTable, _Mapping]] = ..., settings_ntc: _Optional[_Union[TimberDesignSlsConfiguration.SettingsNtcTreeTable, _Mapping]] = ..., surfaces_settings_ec5: _Optional[_Union[TimberDesignSlsConfiguration.SurfacesSettingsEc5TreeTable, _Mapping]] = ..., surfaces_settings_awc: _Optional[_Union[TimberDesignSlsConfiguration.SurfacesSettingsAwcTreeTable, _Mapping]] = ..., surfaces_settings_gb50005: _Optional[_Union[TimberDesignSlsConfiguration.SurfacesSettingsGb50005TreeTable, _Mapping]] = ..., surfaces_settings_sia: _Optional[_Union[TimberDesignSlsConfiguration.SurfacesSettingsSiaTreeTable, _Mapping]] = ..., surfaces_settings_csa: _Optional[_Union[TimberDesignSlsConfiguration.SurfacesSettingsCsaTreeTable, _Mapping]] = ..., surfaces_settings_sans10163: _Optional[_Union[TimberDesignSlsConfiguration.SurfacesSettingsSans10163TreeTable, _Mapping]] = ..., surfaces_settings_sp64: _Optional[_Union[TimberDesignSlsConfiguration.SurfacesSettingsSp64TreeTable, _Mapping]] = ..., surfaces_settings_nbr7190: _Optional[_Union[TimberDesignSlsConfiguration.SurfacesSettingsNbr7190TreeTable, _Mapping]] = ..., surfaces_settings_as1720: _Optional[_Union[TimberDesignSlsConfiguration.SurfacesSettingsAs1720TreeTable, _Mapping]] = ..., surfaces_settings_ntc: _Optional[_Union[TimberDesignSlsConfiguration.SurfacesSettingsNtcTreeTable, _Mapping]] = ..., standard_parameters: _Optional[_Union[TimberDesignSlsConfiguration.StandardParametersTreeTable, _Mapping]] = ..., comment: _Optional[str] = ..., standard_parameters_tree: _Optional[_Union[TimberDesignSlsConfiguration.StandardParametersTreeTreeTable, _Mapping]] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
