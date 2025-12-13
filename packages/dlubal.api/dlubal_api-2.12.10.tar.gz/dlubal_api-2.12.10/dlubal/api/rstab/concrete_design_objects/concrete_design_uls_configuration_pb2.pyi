from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ConcreteDesignUlsConfiguration(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "assigned_to_all_members", "assigned_to_members", "assigned_to_all_member_sets", "assigned_to_member_sets", "assigned_to_all_shear_walls", "assigned_to_shear_walls", "assigned_to_all_deep_beams", "assigned_to_deep_beams", "assigned_to_design_strips", "assigned_to_all_design_strips", "settings_main_ec2", "settings_main_is456", "settings_main_aci318", "settings_main_csaa233", "settings_main_sp63", "settings_member_ec2", "settings_member_IS456", "settings_member_aci318", "settings_member_csaa233", "settings_member_sp63", "settings_surface_ec2", "settings_surface_is456", "settings_surface_aci318", "settings_surface_csaa233", "settings_surface_sp63", "settings_node_ec2", "settings_node_IS456", "settings_node_aci318", "settings_node_csaa233", "settings_node_sp63", "standard_parameters", "generating_object_info", "is_generated", "comment", "standard_parameters_tree", "id_for_export_import", "metadata_for_export_import")
    class SettingsMainEc2TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsMainEc2TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsMainEc2TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsMainEc2TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsMainEc2TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsMainEc2TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsMainIs456TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsMainIs456TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsMainIs456TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsMainIs456TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsMainIs456TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsMainIs456TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsMainAci318TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsMainAci318TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsMainAci318TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsMainAci318TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsMainAci318TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsMainAci318TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsMainCsaa233TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsMainCsaa233TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsMainCsaa233TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsMainCsaa233TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsMainCsaa233TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsMainCsaa233TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsMainSp63TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsMainSp63TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsMainSp63TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsMainSp63TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsMainSp63TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsMainSp63TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsMemberEc2TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsMemberEc2TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsMemberEc2TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsMemberEc2TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsMemberEc2TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsMemberEc2TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsMemberIs456TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsMemberIs456TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsMemberIs456TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsMemberIs456TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsMemberIs456TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsMemberIs456TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsMemberAci318TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsMemberAci318TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsMemberAci318TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsMemberAci318TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsMemberAci318TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsMemberAci318TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsMemberCsaa233TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsMemberCsaa233TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsMemberCsaa233TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsMemberCsaa233TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsMemberCsaa233TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsMemberCsaa233TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsMemberSp63TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsMemberSp63TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsMemberSp63TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsMemberSp63TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsMemberSp63TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsMemberSp63TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsSurfaceEc2TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsSurfaceEc2TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsSurfaceEc2TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsSurfaceEc2TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsSurfaceEc2TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsSurfaceEc2TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsSurfaceIs456TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsSurfaceIs456TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsSurfaceIs456TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsSurfaceIs456TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsSurfaceIs456TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsSurfaceIs456TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsSurfaceAci318TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsSurfaceAci318TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsSurfaceAci318TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsSurfaceAci318TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsSurfaceAci318TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsSurfaceAci318TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsSurfaceCsaa233TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsSurfaceCsaa233TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsSurfaceCsaa233TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsSurfaceCsaa233TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsSurfaceCsaa233TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsSurfaceCsaa233TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsSurfaceSp63TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsSurfaceSp63TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsSurfaceSp63TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsSurfaceSp63TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsSurfaceSp63TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsSurfaceSp63TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsNodeEc2TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsNodeEc2TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsNodeEc2TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsNodeEc2TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsNodeEc2TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsNodeEc2TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsNodeIs456TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsNodeIs456TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsNodeIs456TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsNodeIs456TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsNodeIs456TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsNodeIs456TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsNodeAci318TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsNodeAci318TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsNodeAci318TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsNodeAci318TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsNodeAci318TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsNodeAci318TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsNodeCsaa233TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsNodeCsaa233TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsNodeCsaa233TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsNodeCsaa233TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsNodeCsaa233TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsNodeCsaa233TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsNodeSp63TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsNodeSp63TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsNodeSp63TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsNodeSp63TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.SettingsNodeSp63TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.SettingsNodeSp63TreeTableRow, _Mapping]]] = ...) -> None: ...
    class StandardParametersTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.StandardParametersTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.StandardParametersTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.StandardParametersTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.StandardParametersTreeTableRow, _Mapping]]] = ...) -> None: ...
    class StandardParametersTreeTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.StandardParametersTreeTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.StandardParametersTreeTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignUlsConfiguration.StandardParametersTreeTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., description: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., note: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[ConcreteDesignUlsConfiguration.StandardParametersTreeTreeTableRow, _Mapping]]] = ...) -> None: ...
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_ALL_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_ALL_MEMBER_SETS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_MEMBER_SETS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_ALL_SHEAR_WALLS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_SHEAR_WALLS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_ALL_DEEP_BEAMS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_DEEP_BEAMS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_DESIGN_STRIPS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_ALL_DESIGN_STRIPS_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_MAIN_EC2_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_MAIN_IS456_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_MAIN_ACI318_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_MAIN_CSAA233_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_MAIN_SP63_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_MEMBER_EC2_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_MEMBER_IS456_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_MEMBER_ACI318_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_MEMBER_CSAA233_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_MEMBER_SP63_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_SURFACE_EC2_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_SURFACE_IS456_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_SURFACE_ACI318_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_SURFACE_CSAA233_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_SURFACE_SP63_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_NODE_EC2_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_NODE_IS456_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_NODE_ACI318_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_NODE_CSAA233_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_NODE_SP63_FIELD_NUMBER: _ClassVar[int]
    STANDARD_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
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
    assigned_to_all_shear_walls: bool
    assigned_to_shear_walls: _containers.RepeatedScalarFieldContainer[int]
    assigned_to_all_deep_beams: bool
    assigned_to_deep_beams: _containers.RepeatedScalarFieldContainer[int]
    assigned_to_design_strips: _containers.RepeatedScalarFieldContainer[int]
    assigned_to_all_design_strips: bool
    settings_main_ec2: ConcreteDesignUlsConfiguration.SettingsMainEc2TreeTable
    settings_main_is456: ConcreteDesignUlsConfiguration.SettingsMainIs456TreeTable
    settings_main_aci318: ConcreteDesignUlsConfiguration.SettingsMainAci318TreeTable
    settings_main_csaa233: ConcreteDesignUlsConfiguration.SettingsMainCsaa233TreeTable
    settings_main_sp63: ConcreteDesignUlsConfiguration.SettingsMainSp63TreeTable
    settings_member_ec2: ConcreteDesignUlsConfiguration.SettingsMemberEc2TreeTable
    settings_member_IS456: ConcreteDesignUlsConfiguration.SettingsMemberIs456TreeTable
    settings_member_aci318: ConcreteDesignUlsConfiguration.SettingsMemberAci318TreeTable
    settings_member_csaa233: ConcreteDesignUlsConfiguration.SettingsMemberCsaa233TreeTable
    settings_member_sp63: ConcreteDesignUlsConfiguration.SettingsMemberSp63TreeTable
    settings_surface_ec2: ConcreteDesignUlsConfiguration.SettingsSurfaceEc2TreeTable
    settings_surface_is456: ConcreteDesignUlsConfiguration.SettingsSurfaceIs456TreeTable
    settings_surface_aci318: ConcreteDesignUlsConfiguration.SettingsSurfaceAci318TreeTable
    settings_surface_csaa233: ConcreteDesignUlsConfiguration.SettingsSurfaceCsaa233TreeTable
    settings_surface_sp63: ConcreteDesignUlsConfiguration.SettingsSurfaceSp63TreeTable
    settings_node_ec2: ConcreteDesignUlsConfiguration.SettingsNodeEc2TreeTable
    settings_node_IS456: ConcreteDesignUlsConfiguration.SettingsNodeIs456TreeTable
    settings_node_aci318: ConcreteDesignUlsConfiguration.SettingsNodeAci318TreeTable
    settings_node_csaa233: ConcreteDesignUlsConfiguration.SettingsNodeCsaa233TreeTable
    settings_node_sp63: ConcreteDesignUlsConfiguration.SettingsNodeSp63TreeTable
    standard_parameters: ConcreteDesignUlsConfiguration.StandardParametersTreeTable
    generating_object_info: str
    is_generated: bool
    comment: str
    standard_parameters_tree: ConcreteDesignUlsConfiguration.StandardParametersTreeTreeTable
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., assigned_to_all_members: bool = ..., assigned_to_members: _Optional[_Iterable[int]] = ..., assigned_to_all_member_sets: bool = ..., assigned_to_member_sets: _Optional[_Iterable[int]] = ..., assigned_to_all_shear_walls: bool = ..., assigned_to_shear_walls: _Optional[_Iterable[int]] = ..., assigned_to_all_deep_beams: bool = ..., assigned_to_deep_beams: _Optional[_Iterable[int]] = ..., assigned_to_design_strips: _Optional[_Iterable[int]] = ..., assigned_to_all_design_strips: bool = ..., settings_main_ec2: _Optional[_Union[ConcreteDesignUlsConfiguration.SettingsMainEc2TreeTable, _Mapping]] = ..., settings_main_is456: _Optional[_Union[ConcreteDesignUlsConfiguration.SettingsMainIs456TreeTable, _Mapping]] = ..., settings_main_aci318: _Optional[_Union[ConcreteDesignUlsConfiguration.SettingsMainAci318TreeTable, _Mapping]] = ..., settings_main_csaa233: _Optional[_Union[ConcreteDesignUlsConfiguration.SettingsMainCsaa233TreeTable, _Mapping]] = ..., settings_main_sp63: _Optional[_Union[ConcreteDesignUlsConfiguration.SettingsMainSp63TreeTable, _Mapping]] = ..., settings_member_ec2: _Optional[_Union[ConcreteDesignUlsConfiguration.SettingsMemberEc2TreeTable, _Mapping]] = ..., settings_member_IS456: _Optional[_Union[ConcreteDesignUlsConfiguration.SettingsMemberIs456TreeTable, _Mapping]] = ..., settings_member_aci318: _Optional[_Union[ConcreteDesignUlsConfiguration.SettingsMemberAci318TreeTable, _Mapping]] = ..., settings_member_csaa233: _Optional[_Union[ConcreteDesignUlsConfiguration.SettingsMemberCsaa233TreeTable, _Mapping]] = ..., settings_member_sp63: _Optional[_Union[ConcreteDesignUlsConfiguration.SettingsMemberSp63TreeTable, _Mapping]] = ..., settings_surface_ec2: _Optional[_Union[ConcreteDesignUlsConfiguration.SettingsSurfaceEc2TreeTable, _Mapping]] = ..., settings_surface_is456: _Optional[_Union[ConcreteDesignUlsConfiguration.SettingsSurfaceIs456TreeTable, _Mapping]] = ..., settings_surface_aci318: _Optional[_Union[ConcreteDesignUlsConfiguration.SettingsSurfaceAci318TreeTable, _Mapping]] = ..., settings_surface_csaa233: _Optional[_Union[ConcreteDesignUlsConfiguration.SettingsSurfaceCsaa233TreeTable, _Mapping]] = ..., settings_surface_sp63: _Optional[_Union[ConcreteDesignUlsConfiguration.SettingsSurfaceSp63TreeTable, _Mapping]] = ..., settings_node_ec2: _Optional[_Union[ConcreteDesignUlsConfiguration.SettingsNodeEc2TreeTable, _Mapping]] = ..., settings_node_IS456: _Optional[_Union[ConcreteDesignUlsConfiguration.SettingsNodeIs456TreeTable, _Mapping]] = ..., settings_node_aci318: _Optional[_Union[ConcreteDesignUlsConfiguration.SettingsNodeAci318TreeTable, _Mapping]] = ..., settings_node_csaa233: _Optional[_Union[ConcreteDesignUlsConfiguration.SettingsNodeCsaa233TreeTable, _Mapping]] = ..., settings_node_sp63: _Optional[_Union[ConcreteDesignUlsConfiguration.SettingsNodeSp63TreeTable, _Mapping]] = ..., standard_parameters: _Optional[_Union[ConcreteDesignUlsConfiguration.StandardParametersTreeTable, _Mapping]] = ..., generating_object_info: _Optional[str] = ..., is_generated: bool = ..., comment: _Optional[str] = ..., standard_parameters_tree: _Optional[_Union[ConcreteDesignUlsConfiguration.StandardParametersTreeTreeTable, _Mapping]] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
