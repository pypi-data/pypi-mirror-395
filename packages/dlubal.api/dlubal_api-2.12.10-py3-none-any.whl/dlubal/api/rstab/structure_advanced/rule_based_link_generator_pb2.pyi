from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RuleBasedLinkGenerator(_message.Message):
    __slots__ = ("no", "type", "name", "user_defined_name_enabled", "comment", "is_active", "rules", "parameters", "is_generated", "generating_object_info", "id_for_export_import", "metadata_for_export_import")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TYPE_UNKNOWN: _ClassVar[RuleBasedLinkGenerator.Type]
        TYPE_STANDARD: _ClassVar[RuleBasedLinkGenerator.Type]
    TYPE_UNKNOWN: RuleBasedLinkGenerator.Type
    TYPE_STANDARD: RuleBasedLinkGenerator.Type
    class RulesTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[RuleBasedLinkGenerator.RulesRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[RuleBasedLinkGenerator.RulesRow, _Mapping]]] = ...) -> None: ...
    class RulesRow(_message.Message):
        __slots__ = ("no", "description", "is_active", "rule_type", "priority", "comment")
        class RuleType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            RULE_TYPE_COLUMN_SLAB: _ClassVar[RuleBasedLinkGenerator.RulesRow.RuleType]
            RULE_TYPE_BEAM_MEMBER: _ClassVar[RuleBasedLinkGenerator.RulesRow.RuleType]
            RULE_TYPE_BEAM_NODE: _ClassVar[RuleBasedLinkGenerator.RulesRow.RuleType]
            RULE_TYPE_BEAM_SLAB: _ClassVar[RuleBasedLinkGenerator.RulesRow.RuleType]
            RULE_TYPE_BEAM_WALL: _ClassVar[RuleBasedLinkGenerator.RulesRow.RuleType]
            RULE_TYPE_COLUMN_MEMBER: _ClassVar[RuleBasedLinkGenerator.RulesRow.RuleType]
            RULE_TYPE_COLUMN_NODE: _ClassVar[RuleBasedLinkGenerator.RulesRow.RuleType]
            RULE_TYPE_DIAGONAL_MEMBER: _ClassVar[RuleBasedLinkGenerator.RulesRow.RuleType]
            RULE_TYPE_DIAGONAL_NODE: _ClassVar[RuleBasedLinkGenerator.RulesRow.RuleType]
            RULE_TYPE_DIAGONAL_SLAB: _ClassVar[RuleBasedLinkGenerator.RulesRow.RuleType]
            RULE_TYPE_WALL_SLAB: _ClassVar[RuleBasedLinkGenerator.RulesRow.RuleType]
            RULE_TYPE_WALL_WALL: _ClassVar[RuleBasedLinkGenerator.RulesRow.RuleType]
        RULE_TYPE_COLUMN_SLAB: RuleBasedLinkGenerator.RulesRow.RuleType
        RULE_TYPE_BEAM_MEMBER: RuleBasedLinkGenerator.RulesRow.RuleType
        RULE_TYPE_BEAM_NODE: RuleBasedLinkGenerator.RulesRow.RuleType
        RULE_TYPE_BEAM_SLAB: RuleBasedLinkGenerator.RulesRow.RuleType
        RULE_TYPE_BEAM_WALL: RuleBasedLinkGenerator.RulesRow.RuleType
        RULE_TYPE_COLUMN_MEMBER: RuleBasedLinkGenerator.RulesRow.RuleType
        RULE_TYPE_COLUMN_NODE: RuleBasedLinkGenerator.RulesRow.RuleType
        RULE_TYPE_DIAGONAL_MEMBER: RuleBasedLinkGenerator.RulesRow.RuleType
        RULE_TYPE_DIAGONAL_NODE: RuleBasedLinkGenerator.RulesRow.RuleType
        RULE_TYPE_DIAGONAL_SLAB: RuleBasedLinkGenerator.RulesRow.RuleType
        RULE_TYPE_WALL_SLAB: RuleBasedLinkGenerator.RulesRow.RuleType
        RULE_TYPE_WALL_WALL: RuleBasedLinkGenerator.RulesRow.RuleType
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
        RULE_TYPE_FIELD_NUMBER: _ClassVar[int]
        PRIORITY_FIELD_NUMBER: _ClassVar[int]
        COMMENT_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        is_active: bool
        rule_type: RuleBasedLinkGenerator.RulesRow.RuleType
        priority: int
        comment: str
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., is_active: bool = ..., rule_type: _Optional[_Union[RuleBasedLinkGenerator.RulesRow.RuleType, str]] = ..., priority: _Optional[int] = ..., comment: _Optional[str] = ...) -> None: ...
    class ParametersTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[RuleBasedLinkGenerator.ParametersTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[RuleBasedLinkGenerator.ParametersTreeTableRow, _Mapping]]] = ...) -> None: ...
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
        rows: _containers.RepeatedCompositeFieldContainer[RuleBasedLinkGenerator.ParametersTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[RuleBasedLinkGenerator.ParametersTreeTableRow, _Mapping]]] = ...) -> None: ...
    NO_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    RULES_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    type: RuleBasedLinkGenerator.Type
    name: str
    user_defined_name_enabled: bool
    comment: str
    is_active: bool
    rules: RuleBasedLinkGenerator.RulesTable
    parameters: RuleBasedLinkGenerator.ParametersTreeTable
    is_generated: bool
    generating_object_info: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., type: _Optional[_Union[RuleBasedLinkGenerator.Type, str]] = ..., name: _Optional[str] = ..., user_defined_name_enabled: bool = ..., comment: _Optional[str] = ..., is_active: bool = ..., rules: _Optional[_Union[RuleBasedLinkGenerator.RulesTable, _Mapping]] = ..., parameters: _Optional[_Union[RuleBasedLinkGenerator.ParametersTreeTable, _Mapping]] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
