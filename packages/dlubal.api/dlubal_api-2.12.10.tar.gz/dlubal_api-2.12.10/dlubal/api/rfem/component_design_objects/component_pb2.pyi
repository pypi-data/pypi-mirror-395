from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Component(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "user_defined", "to_design", "component_series", "component_snap_point_number", "component_snap_point_offset_x", "component_snap_point_offset_z", "assigned_to_member_ends", "assigned_to_members", "assigned_to_member_x_location", "all_objects_to_design", "members_to_design", "component_on_member_end_section_point", "component_on_member_end_section_point_user_id", "component_on_member_end_section_point_y_offset", "component_on_member_end_section_point_z_offset", "component_on_member_end_longitudinal_alignment", "component_on_member_end_longitudinal_offset", "component_on_member_end_rotation_sequence", "component_on_member_end_rotation_angle_0", "component_on_member_end_rotation_angle_1", "component_on_member_end_rotation_angle_2", "component_on_member_rotation_type", "component_on_member_rotation_angle", "component_on_member_rotation_help_node", "component_on_member_rotation_plane_type", "component_on_member_longitudinal_alignment", "component_on_member_longitudinal_offset", "component_settings", "component_parameters", "comment", "id_for_export_import", "metadata_for_export_import")
    class ComponentOnMemberEndLongitudinalAlignment(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        COMPONENT_ON_MEMBER_END_LONGITUDINAL_ALIGNMENT_LEFT: _ClassVar[Component.ComponentOnMemberEndLongitudinalAlignment]
        COMPONENT_ON_MEMBER_END_LONGITUDINAL_ALIGNMENT_CENTER: _ClassVar[Component.ComponentOnMemberEndLongitudinalAlignment]
        COMPONENT_ON_MEMBER_END_LONGITUDINAL_ALIGNMENT_RIGHT: _ClassVar[Component.ComponentOnMemberEndLongitudinalAlignment]
    COMPONENT_ON_MEMBER_END_LONGITUDINAL_ALIGNMENT_LEFT: Component.ComponentOnMemberEndLongitudinalAlignment
    COMPONENT_ON_MEMBER_END_LONGITUDINAL_ALIGNMENT_CENTER: Component.ComponentOnMemberEndLongitudinalAlignment
    COMPONENT_ON_MEMBER_END_LONGITUDINAL_ALIGNMENT_RIGHT: Component.ComponentOnMemberEndLongitudinalAlignment
    class ComponentOnMemberEndRotationSequence(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        COMPONENT_ON_MEMBER_END_ROTATION_SEQUENCE_XYZ: _ClassVar[Component.ComponentOnMemberEndRotationSequence]
        COMPONENT_ON_MEMBER_END_ROTATION_SEQUENCE_XZY: _ClassVar[Component.ComponentOnMemberEndRotationSequence]
        COMPONENT_ON_MEMBER_END_ROTATION_SEQUENCE_YXZ: _ClassVar[Component.ComponentOnMemberEndRotationSequence]
        COMPONENT_ON_MEMBER_END_ROTATION_SEQUENCE_YZX: _ClassVar[Component.ComponentOnMemberEndRotationSequence]
        COMPONENT_ON_MEMBER_END_ROTATION_SEQUENCE_ZXY: _ClassVar[Component.ComponentOnMemberEndRotationSequence]
        COMPONENT_ON_MEMBER_END_ROTATION_SEQUENCE_ZYX: _ClassVar[Component.ComponentOnMemberEndRotationSequence]
    COMPONENT_ON_MEMBER_END_ROTATION_SEQUENCE_XYZ: Component.ComponentOnMemberEndRotationSequence
    COMPONENT_ON_MEMBER_END_ROTATION_SEQUENCE_XZY: Component.ComponentOnMemberEndRotationSequence
    COMPONENT_ON_MEMBER_END_ROTATION_SEQUENCE_YXZ: Component.ComponentOnMemberEndRotationSequence
    COMPONENT_ON_MEMBER_END_ROTATION_SEQUENCE_YZX: Component.ComponentOnMemberEndRotationSequence
    COMPONENT_ON_MEMBER_END_ROTATION_SEQUENCE_ZXY: Component.ComponentOnMemberEndRotationSequence
    COMPONENT_ON_MEMBER_END_ROTATION_SEQUENCE_ZYX: Component.ComponentOnMemberEndRotationSequence
    class ComponentOnMemberRotationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        COMPONENT_ON_MEMBER_ROTATION_TYPE_BY_ANGLE: _ClassVar[Component.ComponentOnMemberRotationType]
        COMPONENT_ON_MEMBER_ROTATION_TYPE_TO_NODE: _ClassVar[Component.ComponentOnMemberRotationType]
    COMPONENT_ON_MEMBER_ROTATION_TYPE_BY_ANGLE: Component.ComponentOnMemberRotationType
    COMPONENT_ON_MEMBER_ROTATION_TYPE_TO_NODE: Component.ComponentOnMemberRotationType
    class ComponentOnMemberRotationPlaneType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        COMPONENT_ON_MEMBER_ROTATION_PLANE_TYPE_ROTATION_PLANE_XY: _ClassVar[Component.ComponentOnMemberRotationPlaneType]
        COMPONENT_ON_MEMBER_ROTATION_PLANE_TYPE_ROTATION_PLANE_XZ: _ClassVar[Component.ComponentOnMemberRotationPlaneType]
    COMPONENT_ON_MEMBER_ROTATION_PLANE_TYPE_ROTATION_PLANE_XY: Component.ComponentOnMemberRotationPlaneType
    COMPONENT_ON_MEMBER_ROTATION_PLANE_TYPE_ROTATION_PLANE_XZ: Component.ComponentOnMemberRotationPlaneType
    class ComponentOnMemberLongitudinalAlignment(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        COMPONENT_ON_MEMBER_LONGITUDINAL_ALIGNMENT_LEFT: _ClassVar[Component.ComponentOnMemberLongitudinalAlignment]
        COMPONENT_ON_MEMBER_LONGITUDINAL_ALIGNMENT_CENTER: _ClassVar[Component.ComponentOnMemberLongitudinalAlignment]
        COMPONENT_ON_MEMBER_LONGITUDINAL_ALIGNMENT_RIGHT: _ClassVar[Component.ComponentOnMemberLongitudinalAlignment]
    COMPONENT_ON_MEMBER_LONGITUDINAL_ALIGNMENT_LEFT: Component.ComponentOnMemberLongitudinalAlignment
    COMPONENT_ON_MEMBER_LONGITUDINAL_ALIGNMENT_CENTER: Component.ComponentOnMemberLongitudinalAlignment
    COMPONENT_ON_MEMBER_LONGITUDINAL_ALIGNMENT_RIGHT: Component.ComponentOnMemberLongitudinalAlignment
    class ComponentSettingsTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[Component.ComponentSettingsTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[Component.ComponentSettingsTreeTableRow, _Mapping]]] = ...) -> None: ...
    class ComponentSettingsTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[Component.ComponentSettingsTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[Component.ComponentSettingsTreeTableRow, _Mapping]]] = ...) -> None: ...
    class ComponentParametersTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[Component.ComponentParametersTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[Component.ComponentParametersTreeTableRow, _Mapping]]] = ...) -> None: ...
    class ComponentParametersTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[Component.ComponentParametersTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[Component.ComponentParametersTreeTableRow, _Mapping]]] = ...) -> None: ...
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_FIELD_NUMBER: _ClassVar[int]
    TO_DESIGN_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_SERIES_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_SNAP_POINT_NUMBER_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_SNAP_POINT_OFFSET_X_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_SNAP_POINT_OFFSET_Z_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_MEMBER_ENDS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_MEMBER_X_LOCATION_FIELD_NUMBER: _ClassVar[int]
    ALL_OBJECTS_TO_DESIGN_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_TO_DESIGN_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_ON_MEMBER_END_SECTION_POINT_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_ON_MEMBER_END_SECTION_POINT_USER_ID_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_ON_MEMBER_END_SECTION_POINT_Y_OFFSET_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_ON_MEMBER_END_SECTION_POINT_Z_OFFSET_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_ON_MEMBER_END_LONGITUDINAL_ALIGNMENT_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_ON_MEMBER_END_LONGITUDINAL_OFFSET_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_ON_MEMBER_END_ROTATION_SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_ON_MEMBER_END_ROTATION_ANGLE_0_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_ON_MEMBER_END_ROTATION_ANGLE_1_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_ON_MEMBER_END_ROTATION_ANGLE_2_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_ON_MEMBER_ROTATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_ON_MEMBER_ROTATION_ANGLE_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_ON_MEMBER_ROTATION_HELP_NODE_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_ON_MEMBER_ROTATION_PLANE_TYPE_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_ON_MEMBER_LONGITUDINAL_ALIGNMENT_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_ON_MEMBER_LONGITUDINAL_OFFSET_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    user_defined: bool
    to_design: bool
    component_series: int
    component_snap_point_number: int
    component_snap_point_offset_x: float
    component_snap_point_offset_z: float
    assigned_to_member_ends: str
    assigned_to_members: str
    assigned_to_member_x_location: str
    all_objects_to_design: bool
    members_to_design: _containers.RepeatedScalarFieldContainer[int]
    component_on_member_end_section_point: int
    component_on_member_end_section_point_user_id: int
    component_on_member_end_section_point_y_offset: float
    component_on_member_end_section_point_z_offset: float
    component_on_member_end_longitudinal_alignment: Component.ComponentOnMemberEndLongitudinalAlignment
    component_on_member_end_longitudinal_offset: float
    component_on_member_end_rotation_sequence: Component.ComponentOnMemberEndRotationSequence
    component_on_member_end_rotation_angle_0: float
    component_on_member_end_rotation_angle_1: float
    component_on_member_end_rotation_angle_2: float
    component_on_member_rotation_type: Component.ComponentOnMemberRotationType
    component_on_member_rotation_angle: float
    component_on_member_rotation_help_node: int
    component_on_member_rotation_plane_type: Component.ComponentOnMemberRotationPlaneType
    component_on_member_longitudinal_alignment: Component.ComponentOnMemberLongitudinalAlignment
    component_on_member_longitudinal_offset: float
    component_settings: Component.ComponentSettingsTreeTable
    component_parameters: Component.ComponentParametersTreeTable
    comment: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., user_defined: bool = ..., to_design: bool = ..., component_series: _Optional[int] = ..., component_snap_point_number: _Optional[int] = ..., component_snap_point_offset_x: _Optional[float] = ..., component_snap_point_offset_z: _Optional[float] = ..., assigned_to_member_ends: _Optional[str] = ..., assigned_to_members: _Optional[str] = ..., assigned_to_member_x_location: _Optional[str] = ..., all_objects_to_design: bool = ..., members_to_design: _Optional[_Iterable[int]] = ..., component_on_member_end_section_point: _Optional[int] = ..., component_on_member_end_section_point_user_id: _Optional[int] = ..., component_on_member_end_section_point_y_offset: _Optional[float] = ..., component_on_member_end_section_point_z_offset: _Optional[float] = ..., component_on_member_end_longitudinal_alignment: _Optional[_Union[Component.ComponentOnMemberEndLongitudinalAlignment, str]] = ..., component_on_member_end_longitudinal_offset: _Optional[float] = ..., component_on_member_end_rotation_sequence: _Optional[_Union[Component.ComponentOnMemberEndRotationSequence, str]] = ..., component_on_member_end_rotation_angle_0: _Optional[float] = ..., component_on_member_end_rotation_angle_1: _Optional[float] = ..., component_on_member_end_rotation_angle_2: _Optional[float] = ..., component_on_member_rotation_type: _Optional[_Union[Component.ComponentOnMemberRotationType, str]] = ..., component_on_member_rotation_angle: _Optional[float] = ..., component_on_member_rotation_help_node: _Optional[int] = ..., component_on_member_rotation_plane_type: _Optional[_Union[Component.ComponentOnMemberRotationPlaneType, str]] = ..., component_on_member_longitudinal_alignment: _Optional[_Union[Component.ComponentOnMemberLongitudinalAlignment, str]] = ..., component_on_member_longitudinal_offset: _Optional[float] = ..., component_settings: _Optional[_Union[Component.ComponentSettingsTreeTable, _Mapping]] = ..., component_parameters: _Optional[_Union[Component.ComponentParametersTreeTable, _Mapping]] = ..., comment: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
