from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Texture(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "file_path_albedo", "file_name_albedo", "file_path_metalness", "file_name_metalness", "file_path_roughness", "file_name_roughness", "file_path_normal_map", "file_name_normal_map", "comment", "is_generated", "generating_object_info", "id_for_export_import", "metadata_for_export_import")
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    FILE_PATH_ALBEDO_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_ALBEDO_FIELD_NUMBER: _ClassVar[int]
    FILE_PATH_METALNESS_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_METALNESS_FIELD_NUMBER: _ClassVar[int]
    FILE_PATH_ROUGHNESS_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_ROUGHNESS_FIELD_NUMBER: _ClassVar[int]
    FILE_PATH_NORMAL_MAP_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_NORMAL_MAP_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    file_path_albedo: str
    file_name_albedo: str
    file_path_metalness: str
    file_name_metalness: str
    file_path_roughness: str
    file_name_roughness: str
    file_path_normal_map: str
    file_name_normal_map: str
    comment: str
    is_generated: bool
    generating_object_info: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., file_path_albedo: _Optional[str] = ..., file_name_albedo: _Optional[str] = ..., file_path_metalness: _Optional[str] = ..., file_name_metalness: _Optional[str] = ..., file_path_roughness: _Optional[str] = ..., file_name_roughness: _Optional[str] = ..., file_path_normal_map: _Optional[str] = ..., file_name_normal_map: _Optional[str] = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
