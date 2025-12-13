from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ComponentSerie(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "user_defined", "name", "comment", "image_filename", "parameter_structure_filename", "parameter_data_filename", "visualization_filename", "script_after_calculation_filename", "script_after_savefilename", "category_object_assignment", "category_function", "category_standard_edition", "category_material", "category_manufacturer", "id_for_export_import", "metadata_for_export_import")
    class CategoryObjectAssignment(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CATEGORY_OBJECT_ASSIGNMENT_MEMBER_START_END: _ClassVar[ComponentSerie.CategoryObjectAssignment]
        CATEGORY_OBJECT_ASSIGNMENT_INVALID: _ClassVar[ComponentSerie.CategoryObjectAssignment]
        CATEGORY_OBJECT_ASSIGNMENT_MEMBER: _ClassVar[ComponentSerie.CategoryObjectAssignment]
        CATEGORY_OBJECT_ASSIGNMENT_MEMBER_X_LOCATION: _ClassVar[ComponentSerie.CategoryObjectAssignment]
    CATEGORY_OBJECT_ASSIGNMENT_MEMBER_START_END: ComponentSerie.CategoryObjectAssignment
    CATEGORY_OBJECT_ASSIGNMENT_INVALID: ComponentSerie.CategoryObjectAssignment
    CATEGORY_OBJECT_ASSIGNMENT_MEMBER: ComponentSerie.CategoryObjectAssignment
    CATEGORY_OBJECT_ASSIGNMENT_MEMBER_X_LOCATION: ComponentSerie.CategoryObjectAssignment
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FILENAME_FIELD_NUMBER: _ClassVar[int]
    PARAMETER_STRUCTURE_FILENAME_FIELD_NUMBER: _ClassVar[int]
    PARAMETER_DATA_FILENAME_FIELD_NUMBER: _ClassVar[int]
    VISUALIZATION_FILENAME_FIELD_NUMBER: _ClassVar[int]
    SCRIPT_AFTER_CALCULATION_FILENAME_FIELD_NUMBER: _ClassVar[int]
    SCRIPT_AFTER_SAVEFILENAME_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_OBJECT_ASSIGNMENT_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FUNCTION_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_STANDARD_EDITION_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_MATERIAL_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_MANUFACTURER_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    user_defined: bool
    name: str
    comment: str
    image_filename: str
    parameter_structure_filename: str
    parameter_data_filename: str
    visualization_filename: str
    script_after_calculation_filename: str
    script_after_savefilename: str
    category_object_assignment: ComponentSerie.CategoryObjectAssignment
    category_function: str
    category_standard_edition: str
    category_material: str
    category_manufacturer: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., user_defined: bool = ..., name: _Optional[str] = ..., comment: _Optional[str] = ..., image_filename: _Optional[str] = ..., parameter_structure_filename: _Optional[str] = ..., parameter_data_filename: _Optional[str] = ..., visualization_filename: _Optional[str] = ..., script_after_calculation_filename: _Optional[str] = ..., script_after_savefilename: _Optional[str] = ..., category_object_assignment: _Optional[_Union[ComponentSerie.CategoryObjectAssignment, str]] = ..., category_function: _Optional[str] = ..., category_standard_edition: _Optional[str] = ..., category_material: _Optional[str] = ..., category_manufacturer: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
