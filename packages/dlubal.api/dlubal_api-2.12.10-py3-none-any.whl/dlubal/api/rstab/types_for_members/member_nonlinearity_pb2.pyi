from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MemberNonlinearity(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "assigned_to", "type", "slippage", "tension_force", "compression_force", "comment", "is_generated", "generating_object_info", "id_for_export_import", "metadata_for_export_import")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TYPE_FAILURE_IF_TENSION: _ClassVar[MemberNonlinearity.Type]
        TYPE_FAILURE: _ClassVar[MemberNonlinearity.Type]
        TYPE_FAILURE_IF_COMPRESSION: _ClassVar[MemberNonlinearity.Type]
        TYPE_FAILURE_IF_COMPRESSION_WITH_SLIPPAGE: _ClassVar[MemberNonlinearity.Type]
        TYPE_FAILURE_IF_TENSION_WITH_SLIPPAGE: _ClassVar[MemberNonlinearity.Type]
        TYPE_FAILURE_UNDER_COMPRESSION: _ClassVar[MemberNonlinearity.Type]
        TYPE_FAILURE_UNDER_TENSION: _ClassVar[MemberNonlinearity.Type]
        TYPE_SLIPPAGE: _ClassVar[MemberNonlinearity.Type]
        TYPE_YIELDING: _ClassVar[MemberNonlinearity.Type]
        TYPE_YIELDING_UNDER_COMPRESSION: _ClassVar[MemberNonlinearity.Type]
        TYPE_YIELDING_UNDER_TENSION: _ClassVar[MemberNonlinearity.Type]
    TYPE_FAILURE_IF_TENSION: MemberNonlinearity.Type
    TYPE_FAILURE: MemberNonlinearity.Type
    TYPE_FAILURE_IF_COMPRESSION: MemberNonlinearity.Type
    TYPE_FAILURE_IF_COMPRESSION_WITH_SLIPPAGE: MemberNonlinearity.Type
    TYPE_FAILURE_IF_TENSION_WITH_SLIPPAGE: MemberNonlinearity.Type
    TYPE_FAILURE_UNDER_COMPRESSION: MemberNonlinearity.Type
    TYPE_FAILURE_UNDER_TENSION: MemberNonlinearity.Type
    TYPE_SLIPPAGE: MemberNonlinearity.Type
    TYPE_YIELDING: MemberNonlinearity.Type
    TYPE_YIELDING_UNDER_COMPRESSION: MemberNonlinearity.Type
    TYPE_YIELDING_UNDER_TENSION: MemberNonlinearity.Type
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SLIPPAGE_FIELD_NUMBER: _ClassVar[int]
    TENSION_FORCE_FIELD_NUMBER: _ClassVar[int]
    COMPRESSION_FORCE_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    assigned_to: _containers.RepeatedScalarFieldContainer[int]
    type: MemberNonlinearity.Type
    slippage: float
    tension_force: float
    compression_force: float
    comment: str
    is_generated: bool
    generating_object_info: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., assigned_to: _Optional[_Iterable[int]] = ..., type: _Optional[_Union[MemberNonlinearity.Type, str]] = ..., slippage: _Optional[float] = ..., tension_force: _Optional[float] = ..., compression_force: _Optional[float] = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
