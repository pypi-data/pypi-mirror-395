from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SurfacesContact(_message.Message):
    __slots__ = ("no", "surfaces_group1", "surfaces_group2", "contact_type_between", "contact_member", "contact_surface", "surfaces_contact_type", "surfaces_release_type", "use_independent_mesh", "comment", "id_for_export_import", "metadata_for_export_import")
    class ContactTypeBetween(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CONTACT_TYPE_BETWEEN_SURFACE_AND_SURFACE: _ClassVar[SurfacesContact.ContactTypeBetween]
    CONTACT_TYPE_BETWEEN_SURFACE_AND_SURFACE: SurfacesContact.ContactTypeBetween
    NO_FIELD_NUMBER: _ClassVar[int]
    SURFACES_GROUP1_FIELD_NUMBER: _ClassVar[int]
    SURFACES_GROUP2_FIELD_NUMBER: _ClassVar[int]
    CONTACT_TYPE_BETWEEN_FIELD_NUMBER: _ClassVar[int]
    CONTACT_MEMBER_FIELD_NUMBER: _ClassVar[int]
    CONTACT_SURFACE_FIELD_NUMBER: _ClassVar[int]
    SURFACES_CONTACT_TYPE_FIELD_NUMBER: _ClassVar[int]
    SURFACES_RELEASE_TYPE_FIELD_NUMBER: _ClassVar[int]
    USE_INDEPENDENT_MESH_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    surfaces_group1: _containers.RepeatedScalarFieldContainer[int]
    surfaces_group2: _containers.RepeatedScalarFieldContainer[int]
    contact_type_between: SurfacesContact.ContactTypeBetween
    contact_member: int
    contact_surface: int
    surfaces_contact_type: int
    surfaces_release_type: int
    use_independent_mesh: bool
    comment: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., surfaces_group1: _Optional[_Iterable[int]] = ..., surfaces_group2: _Optional[_Iterable[int]] = ..., contact_type_between: _Optional[_Union[SurfacesContact.ContactTypeBetween, str]] = ..., contact_member: _Optional[int] = ..., contact_surface: _Optional[int] = ..., surfaces_contact_type: _Optional[int] = ..., surfaces_release_type: _Optional[int] = ..., use_independent_mesh: bool = ..., comment: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
