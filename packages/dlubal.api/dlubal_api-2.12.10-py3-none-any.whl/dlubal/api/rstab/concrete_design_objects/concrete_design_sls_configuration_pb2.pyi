from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ConcreteDesignSlsConfiguration(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "assigned_to_all_members", "assigned_to_members", "assigned_to_all_member_sets", "assigned_to_member_sets", "assigned_to_all_shear_walls", "assigned_to_shear_walls", "assigned_to_all_deep_beams", "assigned_to_deep_beams", "assigned_to_design_strips", "assigned_to_all_design_strips", "settings_main_ec2", "settings_main_is456", "settings_main_aci318", "settings_main_csaa233", "settings_main_sp63", "standard_parameters", "generating_object_info", "is_generated", "comment", "standard_parameters_tree", "id_for_export_import", "metadata_for_export_import")
    class SettingsMainEc2TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignSlsConfiguration.SettingsMainEc2TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[ConcreteDesignSlsConfiguration.SettingsMainEc2TreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignSlsConfiguration.SettingsMainEc2TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[ConcreteDesignSlsConfiguration.SettingsMainEc2TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsMainIs456TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignSlsConfiguration.SettingsMainIs456TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[ConcreteDesignSlsConfiguration.SettingsMainIs456TreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignSlsConfiguration.SettingsMainIs456TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[ConcreteDesignSlsConfiguration.SettingsMainIs456TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsMainAci318TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignSlsConfiguration.SettingsMainAci318TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[ConcreteDesignSlsConfiguration.SettingsMainAci318TreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignSlsConfiguration.SettingsMainAci318TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[ConcreteDesignSlsConfiguration.SettingsMainAci318TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsMainCsaa233TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignSlsConfiguration.SettingsMainCsaa233TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[ConcreteDesignSlsConfiguration.SettingsMainCsaa233TreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignSlsConfiguration.SettingsMainCsaa233TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[ConcreteDesignSlsConfiguration.SettingsMainCsaa233TreeTableRow, _Mapping]]] = ...) -> None: ...
    class SettingsMainSp63TreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignSlsConfiguration.SettingsMainSp63TreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[ConcreteDesignSlsConfiguration.SettingsMainSp63TreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignSlsConfiguration.SettingsMainSp63TreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[ConcreteDesignSlsConfiguration.SettingsMainSp63TreeTableRow, _Mapping]]] = ...) -> None: ...
    class StandardParametersTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignSlsConfiguration.StandardParametersTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[ConcreteDesignSlsConfiguration.StandardParametersTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignSlsConfiguration.StandardParametersTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[ConcreteDesignSlsConfiguration.StandardParametersTreeTableRow, _Mapping]]] = ...) -> None: ...
    class StandardParametersTreeTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignSlsConfiguration.StandardParametersTreeTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[ConcreteDesignSlsConfiguration.StandardParametersTreeTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[ConcreteDesignSlsConfiguration.StandardParametersTreeTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., description: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., note: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[ConcreteDesignSlsConfiguration.StandardParametersTreeTreeTableRow, _Mapping]]] = ...) -> None: ...
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
    settings_main_ec2: ConcreteDesignSlsConfiguration.SettingsMainEc2TreeTable
    settings_main_is456: ConcreteDesignSlsConfiguration.SettingsMainIs456TreeTable
    settings_main_aci318: ConcreteDesignSlsConfiguration.SettingsMainAci318TreeTable
    settings_main_csaa233: ConcreteDesignSlsConfiguration.SettingsMainCsaa233TreeTable
    settings_main_sp63: ConcreteDesignSlsConfiguration.SettingsMainSp63TreeTable
    standard_parameters: ConcreteDesignSlsConfiguration.StandardParametersTreeTable
    generating_object_info: str
    is_generated: bool
    comment: str
    standard_parameters_tree: ConcreteDesignSlsConfiguration.StandardParametersTreeTreeTable
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., assigned_to_all_members: bool = ..., assigned_to_members: _Optional[_Iterable[int]] = ..., assigned_to_all_member_sets: bool = ..., assigned_to_member_sets: _Optional[_Iterable[int]] = ..., assigned_to_all_shear_walls: bool = ..., assigned_to_shear_walls: _Optional[_Iterable[int]] = ..., assigned_to_all_deep_beams: bool = ..., assigned_to_deep_beams: _Optional[_Iterable[int]] = ..., assigned_to_design_strips: _Optional[_Iterable[int]] = ..., assigned_to_all_design_strips: bool = ..., settings_main_ec2: _Optional[_Union[ConcreteDesignSlsConfiguration.SettingsMainEc2TreeTable, _Mapping]] = ..., settings_main_is456: _Optional[_Union[ConcreteDesignSlsConfiguration.SettingsMainIs456TreeTable, _Mapping]] = ..., settings_main_aci318: _Optional[_Union[ConcreteDesignSlsConfiguration.SettingsMainAci318TreeTable, _Mapping]] = ..., settings_main_csaa233: _Optional[_Union[ConcreteDesignSlsConfiguration.SettingsMainCsaa233TreeTable, _Mapping]] = ..., settings_main_sp63: _Optional[_Union[ConcreteDesignSlsConfiguration.SettingsMainSp63TreeTable, _Mapping]] = ..., standard_parameters: _Optional[_Union[ConcreteDesignSlsConfiguration.StandardParametersTreeTable, _Mapping]] = ..., generating_object_info: _Optional[str] = ..., is_generated: bool = ..., comment: _Optional[str] = ..., standard_parameters_tree: _Optional[_Union[ConcreteDesignSlsConfiguration.StandardParametersTreeTreeTable, _Mapping]] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
