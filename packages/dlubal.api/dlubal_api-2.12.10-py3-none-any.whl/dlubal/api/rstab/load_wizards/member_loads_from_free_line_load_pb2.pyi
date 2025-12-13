from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MemberLoadsFromFreeLineLoad(_message.Message):
    __slots__ = ("no", "generated_on", "user_defined_name_enabled", "name", "load_case", "lock_for_new_members", "consider_member_eccentricity", "consider_section_distribution", "tolerance_type_for_member_on_plane", "relative_tolerance_for_member_on_plane", "absolute_tolerance_for_member_on_plane", "tolerance_type_for_node_on_line", "relative_tolerance_for_node_on_line", "absolute_tolerance_for_node_on_line", "excluded_members", "excluded_parallel_members", "convert_to_single_members", "comment", "is_generated", "generating_object_info", "load_distribution", "load_direction", "coordinate_system", "magnitude_uniform", "magnitude_first", "magnitude_second", "node_1", "node_2", "node_3", "id_for_export_import", "metadata_for_export_import")
    class ToleranceTypeForMemberOnPlane(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TOLERANCE_TYPE_FOR_MEMBER_ON_PLANE_ABSOLUTE: _ClassVar[MemberLoadsFromFreeLineLoad.ToleranceTypeForMemberOnPlane]
        TOLERANCE_TYPE_FOR_MEMBER_ON_PLANE_RELATIVE: _ClassVar[MemberLoadsFromFreeLineLoad.ToleranceTypeForMemberOnPlane]
    TOLERANCE_TYPE_FOR_MEMBER_ON_PLANE_ABSOLUTE: MemberLoadsFromFreeLineLoad.ToleranceTypeForMemberOnPlane
    TOLERANCE_TYPE_FOR_MEMBER_ON_PLANE_RELATIVE: MemberLoadsFromFreeLineLoad.ToleranceTypeForMemberOnPlane
    class ToleranceTypeForNodeOnLine(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TOLERANCE_TYPE_FOR_NODE_ON_LINE_ABSOLUTE: _ClassVar[MemberLoadsFromFreeLineLoad.ToleranceTypeForNodeOnLine]
        TOLERANCE_TYPE_FOR_NODE_ON_LINE_RELATIVE: _ClassVar[MemberLoadsFromFreeLineLoad.ToleranceTypeForNodeOnLine]
    TOLERANCE_TYPE_FOR_NODE_ON_LINE_ABSOLUTE: MemberLoadsFromFreeLineLoad.ToleranceTypeForNodeOnLine
    TOLERANCE_TYPE_FOR_NODE_ON_LINE_RELATIVE: MemberLoadsFromFreeLineLoad.ToleranceTypeForNodeOnLine
    class LoadDistribution(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LOAD_DISTRIBUTION_UNIFORM: _ClassVar[MemberLoadsFromFreeLineLoad.LoadDistribution]
        LOAD_DISTRIBUTION_LINEAR: _ClassVar[MemberLoadsFromFreeLineLoad.LoadDistribution]
    LOAD_DISTRIBUTION_UNIFORM: MemberLoadsFromFreeLineLoad.LoadDistribution
    LOAD_DISTRIBUTION_LINEAR: MemberLoadsFromFreeLineLoad.LoadDistribution
    class LoadDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LOAD_DIRECTION_UNKNOWN: _ClassVar[MemberLoadsFromFreeLineLoad.LoadDirection]
        LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_PROJECTED_LENGTH: _ClassVar[MemberLoadsFromFreeLineLoad.LoadDirection]
        LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_TRUE_LENGTH: _ClassVar[MemberLoadsFromFreeLineLoad.LoadDirection]
        LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_PROJECTED_LENGTH: _ClassVar[MemberLoadsFromFreeLineLoad.LoadDirection]
        LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_TRUE_LENGTH: _ClassVar[MemberLoadsFromFreeLineLoad.LoadDirection]
        LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_PROJECTED_LENGTH: _ClassVar[MemberLoadsFromFreeLineLoad.LoadDirection]
        LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_TRUE_LENGTH: _ClassVar[MemberLoadsFromFreeLineLoad.LoadDirection]
        LOAD_DIRECTION_LOCAL_Z: _ClassVar[MemberLoadsFromFreeLineLoad.LoadDirection]
    LOAD_DIRECTION_UNKNOWN: MemberLoadsFromFreeLineLoad.LoadDirection
    LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_PROJECTED_LENGTH: MemberLoadsFromFreeLineLoad.LoadDirection
    LOAD_DIRECTION_GLOBAL_X_OR_USER_DEFINED_U_TRUE_LENGTH: MemberLoadsFromFreeLineLoad.LoadDirection
    LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_PROJECTED_LENGTH: MemberLoadsFromFreeLineLoad.LoadDirection
    LOAD_DIRECTION_GLOBAL_Y_OR_USER_DEFINED_V_TRUE_LENGTH: MemberLoadsFromFreeLineLoad.LoadDirection
    LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_PROJECTED_LENGTH: MemberLoadsFromFreeLineLoad.LoadDirection
    LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_TRUE_LENGTH: MemberLoadsFromFreeLineLoad.LoadDirection
    LOAD_DIRECTION_LOCAL_Z: MemberLoadsFromFreeLineLoad.LoadDirection
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
    LOAD_DISTRIBUTION_FIELD_NUMBER: _ClassVar[int]
    LOAD_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    COORDINATE_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_UNIFORM_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_FIRST_FIELD_NUMBER: _ClassVar[int]
    MAGNITUDE_SECOND_FIELD_NUMBER: _ClassVar[int]
    NODE_1_FIELD_NUMBER: _ClassVar[int]
    NODE_2_FIELD_NUMBER: _ClassVar[int]
    NODE_3_FIELD_NUMBER: _ClassVar[int]
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
    tolerance_type_for_member_on_plane: MemberLoadsFromFreeLineLoad.ToleranceTypeForMemberOnPlane
    relative_tolerance_for_member_on_plane: float
    absolute_tolerance_for_member_on_plane: float
    tolerance_type_for_node_on_line: MemberLoadsFromFreeLineLoad.ToleranceTypeForNodeOnLine
    relative_tolerance_for_node_on_line: float
    absolute_tolerance_for_node_on_line: float
    excluded_members: _containers.RepeatedScalarFieldContainer[int]
    excluded_parallel_members: _containers.RepeatedScalarFieldContainer[int]
    convert_to_single_members: bool
    comment: str
    is_generated: bool
    generating_object_info: str
    load_distribution: MemberLoadsFromFreeLineLoad.LoadDistribution
    load_direction: MemberLoadsFromFreeLineLoad.LoadDirection
    coordinate_system: _common_pb2.CoordinateSystemRepresentation
    magnitude_uniform: float
    magnitude_first: float
    magnitude_second: float
    node_1: int
    node_2: int
    node_3: int
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., generated_on: _Optional[_Iterable[int]] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., load_case: _Optional[int] = ..., lock_for_new_members: bool = ..., consider_member_eccentricity: bool = ..., consider_section_distribution: bool = ..., tolerance_type_for_member_on_plane: _Optional[_Union[MemberLoadsFromFreeLineLoad.ToleranceTypeForMemberOnPlane, str]] = ..., relative_tolerance_for_member_on_plane: _Optional[float] = ..., absolute_tolerance_for_member_on_plane: _Optional[float] = ..., tolerance_type_for_node_on_line: _Optional[_Union[MemberLoadsFromFreeLineLoad.ToleranceTypeForNodeOnLine, str]] = ..., relative_tolerance_for_node_on_line: _Optional[float] = ..., absolute_tolerance_for_node_on_line: _Optional[float] = ..., excluded_members: _Optional[_Iterable[int]] = ..., excluded_parallel_members: _Optional[_Iterable[int]] = ..., convert_to_single_members: bool = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., load_distribution: _Optional[_Union[MemberLoadsFromFreeLineLoad.LoadDistribution, str]] = ..., load_direction: _Optional[_Union[MemberLoadsFromFreeLineLoad.LoadDirection, str]] = ..., coordinate_system: _Optional[_Union[_common_pb2.CoordinateSystemRepresentation, _Mapping]] = ..., magnitude_uniform: _Optional[float] = ..., magnitude_first: _Optional[float] = ..., magnitude_second: _Optional[float] = ..., node_1: _Optional[int] = ..., node_2: _Optional[int] = ..., node_3: _Optional[int] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
