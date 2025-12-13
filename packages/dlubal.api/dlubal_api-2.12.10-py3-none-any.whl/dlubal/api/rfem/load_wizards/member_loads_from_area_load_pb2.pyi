from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MemberLoadsFromAreaLoad(_message.Message):
    __slots__ = ("no", "generated_on", "user_defined_name_enabled", "name", "load_case", "lock_for_new_members", "consider_member_eccentricity", "consider_section_distribution", "tolerance_type_for_member_on_plane", "relative_tolerance_for_member_on_plane", "absolute_tolerance_for_member_on_plane", "tolerance_type_for_node_on_line", "relative_tolerance_for_node_on_line", "absolute_tolerance_for_node_on_line", "excluded_members", "excluded_parallel_members", "convert_to_single_members", "comment", "is_generated", "generating_object_info", "corner_nodes", "area_of_application", "smooth_punctual_load_enabled", "id_for_export_import", "metadata_for_export_import")
    class ToleranceTypeForMemberOnPlane(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TOLERANCE_TYPE_FOR_MEMBER_ON_PLANE_ABSOLUTE: _ClassVar[MemberLoadsFromAreaLoad.ToleranceTypeForMemberOnPlane]
        TOLERANCE_TYPE_FOR_MEMBER_ON_PLANE_RELATIVE: _ClassVar[MemberLoadsFromAreaLoad.ToleranceTypeForMemberOnPlane]
    TOLERANCE_TYPE_FOR_MEMBER_ON_PLANE_ABSOLUTE: MemberLoadsFromAreaLoad.ToleranceTypeForMemberOnPlane
    TOLERANCE_TYPE_FOR_MEMBER_ON_PLANE_RELATIVE: MemberLoadsFromAreaLoad.ToleranceTypeForMemberOnPlane
    class ToleranceTypeForNodeOnLine(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TOLERANCE_TYPE_FOR_NODE_ON_LINE_ABSOLUTE: _ClassVar[MemberLoadsFromAreaLoad.ToleranceTypeForNodeOnLine]
        TOLERANCE_TYPE_FOR_NODE_ON_LINE_RELATIVE: _ClassVar[MemberLoadsFromAreaLoad.ToleranceTypeForNodeOnLine]
    TOLERANCE_TYPE_FOR_NODE_ON_LINE_ABSOLUTE: MemberLoadsFromAreaLoad.ToleranceTypeForNodeOnLine
    TOLERANCE_TYPE_FOR_NODE_ON_LINE_RELATIVE: MemberLoadsFromAreaLoad.ToleranceTypeForNodeOnLine
    class AreaOfApplication(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        AREA_OF_APPLICATION_FULLY_CLOSED: _ClassVar[MemberLoadsFromAreaLoad.AreaOfApplication]
        AREA_OF_APPLICATION_EMPTY: _ClassVar[MemberLoadsFromAreaLoad.AreaOfApplication]
    AREA_OF_APPLICATION_FULLY_CLOSED: MemberLoadsFromAreaLoad.AreaOfApplication
    AREA_OF_APPLICATION_EMPTY: MemberLoadsFromAreaLoad.AreaOfApplication
    class CornerNodesTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[MemberLoadsFromAreaLoad.CornerNodesRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[MemberLoadsFromAreaLoad.CornerNodesRow, _Mapping]]] = ...) -> None: ...
    class CornerNodesRow(_message.Message):
        __slots__ = ("no", "description", "row")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        ROW_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        row: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., row: _Optional[_Iterable[int]] = ...) -> None: ...
    NO_FIELD_NUMBER: _ClassVar[int]
    GENERATED_ON_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    LOAD_CASE_FIELD_NUMBER: _ClassVar[int]
    LOCK_FOR_NEW_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    CONSIDER_MEMBER_ECCENTRICITY_FIELD_NUMBER: _ClassVar[int]
    CONSIDER_SECTION_DISTRIBUTION_FIELD_NUMBER: _ClassVar[int]
    TOLERANCE_TYPE_FOR_MEMBER_ON_PLANE_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_TOLERANCE_FOR_MEMBER_ON_PLANE_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_TOLERANCE_FOR_MEMBER_ON_PLANE_FIELD_NUMBER: _ClassVar[int]
    TOLERANCE_TYPE_FOR_NODE_ON_LINE_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_TOLERANCE_FOR_NODE_ON_LINE_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_TOLERANCE_FOR_NODE_ON_LINE_FIELD_NUMBER: _ClassVar[int]
    EXCLUDED_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    EXCLUDED_PARALLEL_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    CONVERT_TO_SINGLE_MEMBERS_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    CORNER_NODES_FIELD_NUMBER: _ClassVar[int]
    AREA_OF_APPLICATION_FIELD_NUMBER: _ClassVar[int]
    SMOOTH_PUNCTUAL_LOAD_ENABLED_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    generated_on: _containers.RepeatedScalarFieldContainer[int]
    user_defined_name_enabled: bool
    name: str
    load_case: int
    lock_for_new_members: bool
    consider_member_eccentricity: bool
    consider_section_distribution: bool
    tolerance_type_for_member_on_plane: MemberLoadsFromAreaLoad.ToleranceTypeForMemberOnPlane
    relative_tolerance_for_member_on_plane: float
    absolute_tolerance_for_member_on_plane: float
    tolerance_type_for_node_on_line: MemberLoadsFromAreaLoad.ToleranceTypeForNodeOnLine
    relative_tolerance_for_node_on_line: float
    absolute_tolerance_for_node_on_line: float
    excluded_members: _containers.RepeatedScalarFieldContainer[int]
    excluded_parallel_members: _containers.RepeatedScalarFieldContainer[int]
    convert_to_single_members: bool
    comment: str
    is_generated: bool
    generating_object_info: str
    corner_nodes: MemberLoadsFromAreaLoad.CornerNodesTable
    area_of_application: MemberLoadsFromAreaLoad.AreaOfApplication
    smooth_punctual_load_enabled: bool
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., generated_on: _Optional[_Iterable[int]] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., load_case: _Optional[int] = ..., lock_for_new_members: bool = ..., consider_member_eccentricity: bool = ..., consider_section_distribution: bool = ..., tolerance_type_for_member_on_plane: _Optional[_Union[MemberLoadsFromAreaLoad.ToleranceTypeForMemberOnPlane, str]] = ..., relative_tolerance_for_member_on_plane: _Optional[float] = ..., absolute_tolerance_for_member_on_plane: _Optional[float] = ..., tolerance_type_for_node_on_line: _Optional[_Union[MemberLoadsFromAreaLoad.ToleranceTypeForNodeOnLine, str]] = ..., relative_tolerance_for_node_on_line: _Optional[float] = ..., absolute_tolerance_for_node_on_line: _Optional[float] = ..., excluded_members: _Optional[_Iterable[int]] = ..., excluded_parallel_members: _Optional[_Iterable[int]] = ..., convert_to_single_members: bool = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., corner_nodes: _Optional[_Union[MemberLoadsFromAreaLoad.CornerNodesTable, _Mapping]] = ..., area_of_application: _Optional[_Union[MemberLoadsFromAreaLoad.AreaOfApplication, str]] = ..., smooth_punctual_load_enabled: bool = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
