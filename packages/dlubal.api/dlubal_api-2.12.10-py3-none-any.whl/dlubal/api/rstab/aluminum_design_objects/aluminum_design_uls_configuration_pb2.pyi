from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AluminumDesignUlsConfiguration(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "assigned_to_all_members", "assigned_to_members", "assigned_to_all_member_sets", "assigned_to_member_sets", "assigned_to_all_surfaces", "assigned_to_surfaces", "assigned_to_all_surface_sets", "assigned_to_surface_sets", "settings_ec9", "settings_adm", "settings_gb50429", "settings_csa", "surfaces_settings_ec9", "surfaces_settings_adm", "surfaces_settings_gb50429", "surfaces_settings_csa", "standard_parameters", "comment", "standard_parameters_tree", "id_for_export_import", "metadata_for_export_import")
    class SettingsEc9TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[AluminumDesignUlsConfiguration.SettingsEc9TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[AluminumDesignUlsConfiguration.SettingsEc9TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsEc9TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[AluminumDesignUlsConfiguration.SettingsEc9TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[AluminumDesignUlsConfiguration.SettingsEc9TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsAdmTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[AluminumDesignUlsConfiguration.SettingsAdmTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[AluminumDesignUlsConfiguration.SettingsAdmTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsAdmTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[AluminumDesignUlsConfiguration.SettingsAdmTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[AluminumDesignUlsConfiguration.SettingsAdmTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsGb50429TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[AluminumDesignUlsConfiguration.SettingsGb50429TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[AluminumDesignUlsConfiguration.SettingsGb50429TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsGb50429TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[AluminumDesignUlsConfiguration.SettingsGb50429TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[AluminumDesignUlsConfiguration.SettingsGb50429TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsCsaTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[AluminumDesignUlsConfiguration.SettingsCsaTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[AluminumDesignUlsConfiguration.SettingsCsaTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[AluminumDesignUlsConfiguration.SettingsCsaTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[AluminumDesignUlsConfiguration.SettingsCsaTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsEc9TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[AluminumDesignUlsConfiguration.SurfacesSettingsEc9TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[AluminumDesignUlsConfiguration.SurfacesSettingsEc9TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsEc9TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[AluminumDesignUlsConfiguration.SurfacesSettingsEc9TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[AluminumDesignUlsConfiguration.SurfacesSettingsEc9TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsAdmTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[AluminumDesignUlsConfiguration.SurfacesSettingsAdmTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[AluminumDesignUlsConfiguration.SurfacesSettingsAdmTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsAdmTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[AluminumDesignUlsConfiguration.SurfacesSettingsAdmTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[AluminumDesignUlsConfiguration.SurfacesSettingsAdmTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsGb50429TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[AluminumDesignUlsConfiguration.SurfacesSettingsGb50429TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[AluminumDesignUlsConfiguration.SurfacesSettingsGb50429TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsGb50429TreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[AluminumDesignUlsConfiguration.SurfacesSettingsGb50429TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[AluminumDesignUlsConfiguration.SurfacesSettingsGb50429TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SurfacesSettingsCsaTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[AluminumDesignUlsConfiguration.SurfacesSettingsCsaTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[AluminumDesignUlsConfiguration.SurfacesSettingsCsaTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[AluminumDesignUlsConfiguration.SurfacesSettingsCsaTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[AluminumDesignUlsConfiguration.SurfacesSettingsCsaTreeTableRow, _Mapping]]] = ...) -> None: ...
    class StandardParametersTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[AluminumDesignUlsConfiguration.StandardParametersTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[AluminumDesignUlsConfiguration.StandardParametersTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[AluminumDesignUlsConfiguration.StandardParametersTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[AluminumDesignUlsConfiguration.StandardParametersTreeTableRow, _Mapping]]] = ...) -> None: ...
    class StandardParametersTreeTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[AluminumDesignUlsConfiguration.StandardParametersTreeTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[AluminumDesignUlsConfiguration.StandardParametersTreeTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[AluminumDesignUlsConfiguration.StandardParametersTreeTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., description: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., note: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[AluminumDesignUlsConfiguration.StandardParametersTreeTreeTableRow, _Mapping]]] = ...) -> None: ...
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
    SETTINGS_EC9_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_ADM_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_GB50429_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_CSA_FIELD_NUMBER: _ClassVar[int]
    SURFACES_SETTINGS_EC9_FIELD_NUMBER: _ClassVar[int]
    SURFACES_SETTINGS_ADM_FIELD_NUMBER: _ClassVar[int]
    SURFACES_SETTINGS_GB50429_FIELD_NUMBER: _ClassVar[int]
    SURFACES_SETTINGS_CSA_FIELD_NUMBER: _ClassVar[int]
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
    settings_ec9: AluminumDesignUlsConfiguration.SettingsEc9TreeTable
    settings_adm: AluminumDesignUlsConfiguration.SettingsAdmTreeTable
    settings_gb50429: AluminumDesignUlsConfiguration.SettingsGb50429TreeTable
    settings_csa: AluminumDesignUlsConfiguration.SettingsCsaTreeTable
    surfaces_settings_ec9: AluminumDesignUlsConfiguration.SurfacesSettingsEc9TreeTable
    surfaces_settings_adm: AluminumDesignUlsConfiguration.SurfacesSettingsAdmTreeTable
    surfaces_settings_gb50429: AluminumDesignUlsConfiguration.SurfacesSettingsGb50429TreeTable
    surfaces_settings_csa: AluminumDesignUlsConfiguration.SurfacesSettingsCsaTreeTable
    standard_parameters: AluminumDesignUlsConfiguration.StandardParametersTreeTable
    comment: str
    standard_parameters_tree: AluminumDesignUlsConfiguration.StandardParametersTreeTreeTable
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., assigned_to_all_members: bool = ..., assigned_to_members: _Optional[_Iterable[int]] = ..., assigned_to_all_member_sets: bool = ..., assigned_to_member_sets: _Optional[_Iterable[int]] = ..., assigned_to_all_surfaces: bool = ..., assigned_to_surfaces: _Optional[_Iterable[int]] = ..., assigned_to_all_surface_sets: bool = ..., assigned_to_surface_sets: _Optional[_Iterable[int]] = ..., settings_ec9: _Optional[_Union[AluminumDesignUlsConfiguration.SettingsEc9TreeTable, _Mapping]] = ..., settings_adm: _Optional[_Union[AluminumDesignUlsConfiguration.SettingsAdmTreeTable, _Mapping]] = ..., settings_gb50429: _Optional[_Union[AluminumDesignUlsConfiguration.SettingsGb50429TreeTable, _Mapping]] = ..., settings_csa: _Optional[_Union[AluminumDesignUlsConfiguration.SettingsCsaTreeTable, _Mapping]] = ..., surfaces_settings_ec9: _Optional[_Union[AluminumDesignUlsConfiguration.SurfacesSettingsEc9TreeTable, _Mapping]] = ..., surfaces_settings_adm: _Optional[_Union[AluminumDesignUlsConfiguration.SurfacesSettingsAdmTreeTable, _Mapping]] = ..., surfaces_settings_gb50429: _Optional[_Union[AluminumDesignUlsConfiguration.SurfacesSettingsGb50429TreeTable, _Mapping]] = ..., surfaces_settings_csa: _Optional[_Union[AluminumDesignUlsConfiguration.SurfacesSettingsCsaTreeTable, _Mapping]] = ..., standard_parameters: _Optional[_Union[AluminumDesignUlsConfiguration.StandardParametersTreeTable, _Mapping]] = ..., comment: _Optional[str] = ..., standard_parameters_tree: _Optional[_Union[AluminumDesignUlsConfiguration.StandardParametersTreeTreeTable, _Mapping]] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
