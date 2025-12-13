from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BeamToBeamConnector(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "connector_type", "member_hinge", "comment", "thicknesses", "is_generated", "generating_object_info", "id_for_export_import", "metadata_for_export_import")
    class ConnectorType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CONNECTOR_TYPE_HINGED: _ClassVar[BeamToBeamConnector.ConnectorType]
        CONNECTOR_TYPE_USER_DEFINED: _ClassVar[BeamToBeamConnector.ConnectorType]
    CONNECTOR_TYPE_HINGED: BeamToBeamConnector.ConnectorType
    CONNECTOR_TYPE_USER_DEFINED: BeamToBeamConnector.ConnectorType
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONNECTOR_TYPE_FIELD_NUMBER: _ClassVar[int]
    MEMBER_HINGE_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    THICKNESSES_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    connector_type: BeamToBeamConnector.ConnectorType
    member_hinge: int
    comment: str
    thicknesses: _containers.RepeatedScalarFieldContainer[int]
    is_generated: bool
    generating_object_info: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., connector_type: _Optional[_Union[BeamToBeamConnector.ConnectorType, str]] = ..., member_hinge: _Optional[int] = ..., comment: _Optional[str] = ..., thicknesses: _Optional[_Iterable[int]] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
