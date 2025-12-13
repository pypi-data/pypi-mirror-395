from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TimberDesignUlsConfiguration(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "assigned_to_all_members", "assigned_to_members", "assigned_to_all_member_sets", "assigned_to_member_sets", "assigned_to_all_deep_beams", "assigned_to_deep_beams", "assigned_to_all_shear_walls", "assigned_to_shear_walls", "assigned_to_all_lines", "assigned_to_lines", "assigned_to_all_line_sets", "assigned_to_line_sets", "settings_ec5", "settings_awc", "settings_gb50005", "settings_sia", "settings_csa", "settings_sans10163", "settings_sp64", "settings_nbr7190", "settings_as1720", "settings_ntc", "surfaces_settings_ec5", "surfaces_settings_awc", "surfaces_settings_gb50005", "surfaces_settings_sia", "surfaces_settings_csa", "surfaces_settings_sans10163", "surfaces_settings_sp64", "surfaces_settings_nbr7190", "surfaces_settings_as1720", "surfaces_settings_ntc", "lines_settings_ec5", "lines_settings_awc", "lines_settings_gb50005", "lines_settings_sia", "lines_settings_csa", "lines_settings_sans10163", "lines_settings_sp64", "lines_settings_nbr7190", "lines_settings_as1720", "lines_settings_ntc", "standard_parameters", "comment", "standard_parameters_tree", "id_for_export_import", "metadata_for_export_import")
    class SettingsEc5TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SettingsEc5TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SettingsEc5TreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SettingsEc5TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SettingsEc5TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsAwcTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SettingsAwcTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SettingsAwcTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SettingsAwcTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SettingsAwcTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsGb50005TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SettingsGb50005TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SettingsGb50005TreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SettingsGb50005TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SettingsGb50005TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsSiaTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SettingsSiaTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SettingsSiaTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SettingsSiaTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SettingsSiaTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsCsaTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SettingsCsaTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SettingsCsaTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SettingsCsaTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SettingsCsaTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsSans10163TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SettingsSans10163TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SettingsSans10163TreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SettingsSans10163TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SettingsSans10163TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsSp64TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SettingsSp64TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SettingsSp64TreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SettingsSp64TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SettingsSp64TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsNbr7190TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SettingsNbr7190TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SettingsNbr7190TreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SettingsNbr7190TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SettingsNbr7190TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsAs1720TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SettingsAs1720TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SettingsAs1720TreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SettingsAs1720TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SettingsAs1720TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsNtcTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SettingsNtcTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SettingsNtcTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SettingsNtcTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SettingsNtcTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsEc5TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SurfacesSettingsEc5TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SurfacesSettingsEc5TreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SurfacesSettingsEc5TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SurfacesSettingsEc5TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsAwcTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SurfacesSettingsAwcTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SurfacesSettingsAwcTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SurfacesSettingsAwcTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SurfacesSettingsAwcTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsGb50005TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SurfacesSettingsGb50005TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SurfacesSettingsGb50005TreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SurfacesSettingsGb50005TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SurfacesSettingsGb50005TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsSiaTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SurfacesSettingsSiaTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SurfacesSettingsSiaTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SurfacesSettingsSiaTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SurfacesSettingsSiaTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsCsaTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SurfacesSettingsCsaTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SurfacesSettingsCsaTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SurfacesSettingsCsaTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SurfacesSettingsCsaTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsSans10163TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SurfacesSettingsSans10163TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SurfacesSettingsSans10163TreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SurfacesSettingsSans10163TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SurfacesSettingsSans10163TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsSp64TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SurfacesSettingsSp64TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SurfacesSettingsSp64TreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SurfacesSettingsSp64TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SurfacesSettingsSp64TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsNbr7190TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SurfacesSettingsNbr7190TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SurfacesSettingsNbr7190TreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SurfacesSettingsNbr7190TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SurfacesSettingsNbr7190TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsAs1720TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SurfacesSettingsAs1720TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SurfacesSettingsAs1720TreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SurfacesSettingsAs1720TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SurfacesSettingsAs1720TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsNtcTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SurfacesSettingsNtcTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SurfacesSettingsNtcTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.SurfacesSettingsNtcTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.SurfacesSettingsNtcTreeTableRow, _Mapping]]] = ...) -> None: ...
    class LinesSettingsEc5TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.LinesSettingsEc5TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.LinesSettingsEc5TreeTableRow, _Mapping]]] = ...) -> None: ...
    class LinesSettingsEc5TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.LinesSettingsEc5TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.LinesSettingsEc5TreeTableRow, _Mapping]]] = ...) -> None: ...
    class LinesSettingsAwcTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.LinesSettingsAwcTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.LinesSettingsAwcTreeTableRow, _Mapping]]] = ...) -> None: ...
    class LinesSettingsAwcTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.LinesSettingsAwcTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.LinesSettingsAwcTreeTableRow, _Mapping]]] = ...) -> None: ...
    class LinesSettingsGb50005TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.LinesSettingsGb50005TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.LinesSettingsGb50005TreeTableRow, _Mapping]]] = ...) -> None: ...
    class LinesSettingsGb50005TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.LinesSettingsGb50005TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.LinesSettingsGb50005TreeTableRow, _Mapping]]] = ...) -> None: ...
    class LinesSettingsSiaTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.LinesSettingsSiaTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.LinesSettingsSiaTreeTableRow, _Mapping]]] = ...) -> None: ...
    class LinesSettingsSiaTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.LinesSettingsSiaTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.LinesSettingsSiaTreeTableRow, _Mapping]]] = ...) -> None: ...
    class LinesSettingsCsaTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.LinesSettingsCsaTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.LinesSettingsCsaTreeTableRow, _Mapping]]] = ...) -> None: ...
    class LinesSettingsCsaTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.LinesSettingsCsaTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.LinesSettingsCsaTreeTableRow, _Mapping]]] = ...) -> None: ...
    class LinesSettingsSans10163TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.LinesSettingsSans10163TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.LinesSettingsSans10163TreeTableRow, _Mapping]]] = ...) -> None: ...
    class LinesSettingsSans10163TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.LinesSettingsSans10163TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.LinesSettingsSans10163TreeTableRow, _Mapping]]] = ...) -> None: ...
    class LinesSettingsSp64TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.LinesSettingsSp64TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.LinesSettingsSp64TreeTableRow, _Mapping]]] = ...) -> None: ...
    class LinesSettingsSp64TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.LinesSettingsSp64TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.LinesSettingsSp64TreeTableRow, _Mapping]]] = ...) -> None: ...
    class LinesSettingsNbr7190TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.LinesSettingsNbr7190TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.LinesSettingsNbr7190TreeTableRow, _Mapping]]] = ...) -> None: ...
    class LinesSettingsNbr7190TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.LinesSettingsNbr7190TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.LinesSettingsNbr7190TreeTableRow, _Mapping]]] = ...) -> None: ...
    class LinesSettingsAs1720TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.LinesSettingsAs1720TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.LinesSettingsAs1720TreeTableRow, _Mapping]]] = ...) -> None: ...
    class LinesSettingsAs1720TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.LinesSettingsAs1720TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.LinesSettingsAs1720TreeTableRow, _Mapping]]] = ...) -> None: ...
    class LinesSettingsNtcTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.LinesSettingsNtcTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.LinesSettingsNtcTreeTableRow, _Mapping]]] = ...) -> None: ...
    class LinesSettingsNtcTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.LinesSettingsNtcTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.LinesSettingsNtcTreeTableRow, _Mapping]]] = ...) -> None: ...
    class StandardParametersTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.StandardParametersTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.StandardParametersTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.StandardParametersTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.StandardParametersTreeTableRow, _Mapping]]] = ...) -> None: ...
    class StandardParametersTreeTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.StandardParametersTreeTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.StandardParametersTreeTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[TimberDesignUlsConfiguration.StandardParametersTreeTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., description: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., note: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[TimberDesignUlsConfiguration.StandardParametersTreeTreeTableRow, _Mapping]]] = ...) -> None: ...
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_ALL_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_ALL_MEMBER_SETS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_MEMBER_SETS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_ALL_DEEP_BEAMS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_DEEP_BEAMS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_ALL_SHEAR_WALLS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_SHEAR_WALLS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_ALL_LINES_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_LINES_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_ALL_LINE_SETS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_LINE_SETS_FIELD_NUMBER: _ClassVar[int]
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
    LINES_SETTINGS_EC5_FIELD_NUMBER: _ClassVar[int]
    LINES_SETTINGS_AWC_FIELD_NUMBER: _ClassVar[int]
    LINES_SETTINGS_GB50005_FIELD_NUMBER: _ClassVar[int]
    LINES_SETTINGS_SIA_FIELD_NUMBER: _ClassVar[int]
    LINES_SETTINGS_CSA_FIELD_NUMBER: _ClassVar[int]
    LINES_SETTINGS_SANS10163_FIELD_NUMBER: _ClassVar[int]
    LINES_SETTINGS_SP64_FIELD_NUMBER: _ClassVar[int]
    LINES_SETTINGS_NBR7190_FIELD_NUMBER: _ClassVar[int]
    LINES_SETTINGS_AS1720_FIELD_NUMBER: _ClassVar[int]
    LINES_SETTINGS_NTC_FIELD_NUMBER: _ClassVar[int]
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
    assigned_to_all_deep_beams: bool
    assigned_to_deep_beams: _containers.RepeatedScalarFieldContainer[int]
    assigned_to_all_shear_walls: bool
    assigned_to_shear_walls: _containers.RepeatedScalarFieldContainer[int]
    assigned_to_all_lines: bool
    assigned_to_lines: _containers.RepeatedScalarFieldContainer[int]
    assigned_to_all_line_sets: bool
    assigned_to_line_sets: _containers.RepeatedScalarFieldContainer[int]
    settings_ec5: TimberDesignUlsConfiguration.SettingsEc5TreeTable
    settings_awc: TimberDesignUlsConfiguration.SettingsAwcTreeTable
    settings_gb50005: TimberDesignUlsConfiguration.SettingsGb50005TreeTable
    settings_sia: TimberDesignUlsConfiguration.SettingsSiaTreeTable
    settings_csa: TimberDesignUlsConfiguration.SettingsCsaTreeTable
    settings_sans10163: TimberDesignUlsConfiguration.SettingsSans10163TreeTable
    settings_sp64: TimberDesignUlsConfiguration.SettingsSp64TreeTable
    settings_nbr7190: TimberDesignUlsConfiguration.SettingsNbr7190TreeTable
    settings_as1720: TimberDesignUlsConfiguration.SettingsAs1720TreeTable
    settings_ntc: TimberDesignUlsConfiguration.SettingsNtcTreeTable
    surfaces_settings_ec5: TimberDesignUlsConfiguration.SurfacesSettingsEc5TreeTable
    surfaces_settings_awc: TimberDesignUlsConfiguration.SurfacesSettingsAwcTreeTable
    surfaces_settings_gb50005: TimberDesignUlsConfiguration.SurfacesSettingsGb50005TreeTable
    surfaces_settings_sia: TimberDesignUlsConfiguration.SurfacesSettingsSiaTreeTable
    surfaces_settings_csa: TimberDesignUlsConfiguration.SurfacesSettingsCsaTreeTable
    surfaces_settings_sans10163: TimberDesignUlsConfiguration.SurfacesSettingsSans10163TreeTable
    surfaces_settings_sp64: TimberDesignUlsConfiguration.SurfacesSettingsSp64TreeTable
    surfaces_settings_nbr7190: TimberDesignUlsConfiguration.SurfacesSettingsNbr7190TreeTable
    surfaces_settings_as1720: TimberDesignUlsConfiguration.SurfacesSettingsAs1720TreeTable
    surfaces_settings_ntc: TimberDesignUlsConfiguration.SurfacesSettingsNtcTreeTable
    lines_settings_ec5: TimberDesignUlsConfiguration.LinesSettingsEc5TreeTable
    lines_settings_awc: TimberDesignUlsConfiguration.LinesSettingsAwcTreeTable
    lines_settings_gb50005: TimberDesignUlsConfiguration.LinesSettingsGb50005TreeTable
    lines_settings_sia: TimberDesignUlsConfiguration.LinesSettingsSiaTreeTable
    lines_settings_csa: TimberDesignUlsConfiguration.LinesSettingsCsaTreeTable
    lines_settings_sans10163: TimberDesignUlsConfiguration.LinesSettingsSans10163TreeTable
    lines_settings_sp64: TimberDesignUlsConfiguration.LinesSettingsSp64TreeTable
    lines_settings_nbr7190: TimberDesignUlsConfiguration.LinesSettingsNbr7190TreeTable
    lines_settings_as1720: TimberDesignUlsConfiguration.LinesSettingsAs1720TreeTable
    lines_settings_ntc: TimberDesignUlsConfiguration.LinesSettingsNtcTreeTable
    standard_parameters: TimberDesignUlsConfiguration.StandardParametersTreeTable
    comment: str
    standard_parameters_tree: TimberDesignUlsConfiguration.StandardParametersTreeTreeTable
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., assigned_to_all_members: bool = ..., assigned_to_members: _Optional[_Iterable[int]] = ..., assigned_to_all_member_sets: bool = ..., assigned_to_member_sets: _Optional[_Iterable[int]] = ..., assigned_to_all_deep_beams: bool = ..., assigned_to_deep_beams: _Optional[_Iterable[int]] = ..., assigned_to_all_shear_walls: bool = ..., assigned_to_shear_walls: _Optional[_Iterable[int]] = ..., assigned_to_all_lines: bool = ..., assigned_to_lines: _Optional[_Iterable[int]] = ..., assigned_to_all_line_sets: bool = ..., assigned_to_line_sets: _Optional[_Iterable[int]] = ..., settings_ec5: _Optional[_Union[TimberDesignUlsConfiguration.SettingsEc5TreeTable, _Mapping]] = ..., settings_awc: _Optional[_Union[TimberDesignUlsConfiguration.SettingsAwcTreeTable, _Mapping]] = ..., settings_gb50005: _Optional[_Union[TimberDesignUlsConfiguration.SettingsGb50005TreeTable, _Mapping]] = ..., settings_sia: _Optional[_Union[TimberDesignUlsConfiguration.SettingsSiaTreeTable, _Mapping]] = ..., settings_csa: _Optional[_Union[TimberDesignUlsConfiguration.SettingsCsaTreeTable, _Mapping]] = ..., settings_sans10163: _Optional[_Union[TimberDesignUlsConfiguration.SettingsSans10163TreeTable, _Mapping]] = ..., settings_sp64: _Optional[_Union[TimberDesignUlsConfiguration.SettingsSp64TreeTable, _Mapping]] = ..., settings_nbr7190: _Optional[_Union[TimberDesignUlsConfiguration.SettingsNbr7190TreeTable, _Mapping]] = ..., settings_as1720: _Optional[_Union[TimberDesignUlsConfiguration.SettingsAs1720TreeTable, _Mapping]] = ..., settings_ntc: _Optional[_Union[TimberDesignUlsConfiguration.SettingsNtcTreeTable, _Mapping]] = ..., surfaces_settings_ec5: _Optional[_Union[TimberDesignUlsConfiguration.SurfacesSettingsEc5TreeTable, _Mapping]] = ..., surfaces_settings_awc: _Optional[_Union[TimberDesignUlsConfiguration.SurfacesSettingsAwcTreeTable, _Mapping]] = ..., surfaces_settings_gb50005: _Optional[_Union[TimberDesignUlsConfiguration.SurfacesSettingsGb50005TreeTable, _Mapping]] = ..., surfaces_settings_sia: _Optional[_Union[TimberDesignUlsConfiguration.SurfacesSettingsSiaTreeTable, _Mapping]] = ..., surfaces_settings_csa: _Optional[_Union[TimberDesignUlsConfiguration.SurfacesSettingsCsaTreeTable, _Mapping]] = ..., surfaces_settings_sans10163: _Optional[_Union[TimberDesignUlsConfiguration.SurfacesSettingsSans10163TreeTable, _Mapping]] = ..., surfaces_settings_sp64: _Optional[_Union[TimberDesignUlsConfiguration.SurfacesSettingsSp64TreeTable, _Mapping]] = ..., surfaces_settings_nbr7190: _Optional[_Union[TimberDesignUlsConfiguration.SurfacesSettingsNbr7190TreeTable, _Mapping]] = ..., surfaces_settings_as1720: _Optional[_Union[TimberDesignUlsConfiguration.SurfacesSettingsAs1720TreeTable, _Mapping]] = ..., surfaces_settings_ntc: _Optional[_Union[TimberDesignUlsConfiguration.SurfacesSettingsNtcTreeTable, _Mapping]] = ..., lines_settings_ec5: _Optional[_Union[TimberDesignUlsConfiguration.LinesSettingsEc5TreeTable, _Mapping]] = ..., lines_settings_awc: _Optional[_Union[TimberDesignUlsConfiguration.LinesSettingsAwcTreeTable, _Mapping]] = ..., lines_settings_gb50005: _Optional[_Union[TimberDesignUlsConfiguration.LinesSettingsGb50005TreeTable, _Mapping]] = ..., lines_settings_sia: _Optional[_Union[TimberDesignUlsConfiguration.LinesSettingsSiaTreeTable, _Mapping]] = ..., lines_settings_csa: _Optional[_Union[TimberDesignUlsConfiguration.LinesSettingsCsaTreeTable, _Mapping]] = ..., lines_settings_sans10163: _Optional[_Union[TimberDesignUlsConfiguration.LinesSettingsSans10163TreeTable, _Mapping]] = ..., lines_settings_sp64: _Optional[_Union[TimberDesignUlsConfiguration.LinesSettingsSp64TreeTable, _Mapping]] = ..., lines_settings_nbr7190: _Optional[_Union[TimberDesignUlsConfiguration.LinesSettingsNbr7190TreeTable, _Mapping]] = ..., lines_settings_as1720: _Optional[_Union[TimberDesignUlsConfiguration.LinesSettingsAs1720TreeTable, _Mapping]] = ..., lines_settings_ntc: _Optional[_Union[TimberDesignUlsConfiguration.LinesSettingsNtcTreeTable, _Mapping]] = ..., standard_parameters: _Optional[_Union[TimberDesignUlsConfiguration.StandardParametersTreeTable, _Mapping]] = ..., comment: _Optional[str] = ..., standard_parameters_tree: _Optional[_Union[TimberDesignUlsConfiguration.StandardParametersTreeTreeTable, _Mapping]] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
