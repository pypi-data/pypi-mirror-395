from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Weld(_message.Message):
    __slots__ = ("no", "first_element", "second_element", "weld_position", "throat_thickness", "welding_properties", "number_of_heat_paths", "temperature_of_material_between_welding_cycles", "comment", "parent_layer", "is_locked_by_parent_layer", "generating_object_info", "is_generated", "id_for_export_import", "metadata_for_export_import")
    class WeldPosition(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        WELD_POSITION_AT_START_OF_FIRST_ELEMENT: _ClassVar[Weld.WeldPosition]
        WELD_POSITION_AT_END_OF_FIRST_ELEMENT: _ClassVar[Weld.WeldPosition]
    WELD_POSITION_AT_START_OF_FIRST_ELEMENT: Weld.WeldPosition
    WELD_POSITION_AT_END_OF_FIRST_ELEMENT: Weld.WeldPosition
    NO_FIELD_NUMBER: _ClassVar[int]
    FIRST_ELEMENT_FIELD_NUMBER: _ClassVar[int]
    SECOND_ELEMENT_FIELD_NUMBER: _ClassVar[int]
    WELD_POSITION_FIELD_NUMBER: _ClassVar[int]
    THROAT_THICKNESS_FIELD_NUMBER: _ClassVar[int]
    WELDING_PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_HEAT_PATHS_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_OF_MATERIAL_BETWEEN_WELDING_CYCLES_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    PARENT_LAYER_FIELD_NUMBER: _ClassVar[int]
    IS_LOCKED_BY_PARENT_LAYER_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    first_element: int
    second_element: int
    weld_position: Weld.WeldPosition
    throat_thickness: float
    welding_properties: bool
    number_of_heat_paths: int
    temperature_of_material_between_welding_cycles: float
    comment: str
    parent_layer: int
    is_locked_by_parent_layer: bool
    generating_object_info: str
    is_generated: bool
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., first_element: _Optional[int] = ..., second_element: _Optional[int] = ..., weld_position: _Optional[_Union[Weld.WeldPosition, str]] = ..., throat_thickness: _Optional[float] = ..., welding_properties: bool = ..., number_of_heat_paths: _Optional[int] = ..., temperature_of_material_between_welding_cycles: _Optional[float] = ..., comment: _Optional[str] = ..., parent_layer: _Optional[int] = ..., is_locked_by_parent_layer: bool = ..., generating_object_info: _Optional[str] = ..., is_generated: bool = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
