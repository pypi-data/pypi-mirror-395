from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DesignStripWizard(_message.Message):
    __slots__ = ("no", "type", "user_defined_name_enabled", "name", "surfaces", "building_grid", "grid_plane", "enable_primary_reinforcement_direction", "primary_reinforcement_direction", "enable_secondary_reinforcement_direction", "secondary_reinforcement_direction", "enable_column_strip_type", "enable_middle_strip_type", "enable_edge_strip_type", "enable_user_defined_strip_width", "user_defined_strip_width", "adjust_internal_moment", "primary_parameters", "secondary_parameters", "analytical_length", "analytical_area", "analytical_mass", "analytical_volume", "analytical_center_of_gravity", "analytical_center_of_gravity_x", "analytical_center_of_gravity_y", "analytical_center_of_gravity_z", "length", "area", "mass", "volume", "center_of_gravity", "center_of_gravity_x", "center_of_gravity_y", "center_of_gravity_z", "comment", "is_generated", "generating_object_info", "id_for_export_import", "metadata_for_export_import")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TYPE_UNKNOWN: _ClassVar[DesignStripWizard.Type]
        TYPE_STANDARD: _ClassVar[DesignStripWizard.Type]
    TYPE_UNKNOWN: DesignStripWizard.Type
    TYPE_STANDARD: DesignStripWizard.Type
    class GridPlane(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        GRID_PLANE_XY: _ClassVar[DesignStripWizard.GridPlane]
        GRID_PLANE_XZ: _ClassVar[DesignStripWizard.GridPlane]
        GRID_PLANE_YZ: _ClassVar[DesignStripWizard.GridPlane]
    GRID_PLANE_XY: DesignStripWizard.GridPlane
    GRID_PLANE_XZ: DesignStripWizard.GridPlane
    GRID_PLANE_YZ: DesignStripWizard.GridPlane
    class PrimaryReinforcementDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PRIMARY_REINFORCEMENT_DIRECTION_X: _ClassVar[DesignStripWizard.PrimaryReinforcementDirection]
        PRIMARY_REINFORCEMENT_DIRECTION_Y: _ClassVar[DesignStripWizard.PrimaryReinforcementDirection]
        PRIMARY_REINFORCEMENT_DIRECTION_Z: _ClassVar[DesignStripWizard.PrimaryReinforcementDirection]
    PRIMARY_REINFORCEMENT_DIRECTION_X: DesignStripWizard.PrimaryReinforcementDirection
    PRIMARY_REINFORCEMENT_DIRECTION_Y: DesignStripWizard.PrimaryReinforcementDirection
    PRIMARY_REINFORCEMENT_DIRECTION_Z: DesignStripWizard.PrimaryReinforcementDirection
    class SecondaryReinforcementDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SECONDARY_REINFORCEMENT_DIRECTION_X: _ClassVar[DesignStripWizard.SecondaryReinforcementDirection]
        SECONDARY_REINFORCEMENT_DIRECTION_Y: _ClassVar[DesignStripWizard.SecondaryReinforcementDirection]
        SECONDARY_REINFORCEMENT_DIRECTION_Z: _ClassVar[DesignStripWizard.SecondaryReinforcementDirection]
    SECONDARY_REINFORCEMENT_DIRECTION_X: DesignStripWizard.SecondaryReinforcementDirection
    SECONDARY_REINFORCEMENT_DIRECTION_Y: DesignStripWizard.SecondaryReinforcementDirection
    SECONDARY_REINFORCEMENT_DIRECTION_Z: DesignStripWizard.SecondaryReinforcementDirection
    class PrimaryParametersTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[DesignStripWizard.PrimaryParametersRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[DesignStripWizard.PrimaryParametersRow, _Mapping]]] = ...) -> None: ...
    class PrimaryParametersRow(_message.Message):
        __slots__ = ("no", "description", "label", "position", "isEnabled")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        LABEL_FIELD_NUMBER: _ClassVar[int]
        POSITION_FIELD_NUMBER: _ClassVar[int]
        ISENABLED_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        label: str
        position: float
        isEnabled: bool
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., label: _Optional[str] = ..., position: _Optional[float] = ..., isEnabled: bool = ...) -> None: ...
    class SecondaryParametersTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[DesignStripWizard.SecondaryParametersRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[DesignStripWizard.SecondaryParametersRow, _Mapping]]] = ...) -> None: ...
    class SecondaryParametersRow(_message.Message):
        __slots__ = ("no", "description", "label", "position", "isEnabled")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        LABEL_FIELD_NUMBER: _ClassVar[int]
        POSITION_FIELD_NUMBER: _ClassVar[int]
        ISENABLED_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        label: str
        position: float
        isEnabled: bool
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., label: _Optional[str] = ..., position: _Optional[float] = ..., isEnabled: bool = ...) -> None: ...
    NO_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SURFACES_FIELD_NUMBER: _ClassVar[int]
    BUILDING_GRID_FIELD_NUMBER: _ClassVar[int]
    GRID_PLANE_FIELD_NUMBER: _ClassVar[int]
    ENABLE_PRIMARY_REINFORCEMENT_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    PRIMARY_REINFORCEMENT_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    ENABLE_SECONDARY_REINFORCEMENT_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    SECONDARY_REINFORCEMENT_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    ENABLE_COLUMN_STRIP_TYPE_FIELD_NUMBER: _ClassVar[int]
    ENABLE_MIDDLE_STRIP_TYPE_FIELD_NUMBER: _ClassVar[int]
    ENABLE_EDGE_STRIP_TYPE_FIELD_NUMBER: _ClassVar[int]
    ENABLE_USER_DEFINED_STRIP_WIDTH_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_STRIP_WIDTH_FIELD_NUMBER: _ClassVar[int]
    ADJUST_INTERNAL_MOMENT_FIELD_NUMBER: _ClassVar[int]
    PRIMARY_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    SECONDARY_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    ANALYTICAL_LENGTH_FIELD_NUMBER: _ClassVar[int]
    ANALYTICAL_AREA_FIELD_NUMBER: _ClassVar[int]
    ANALYTICAL_MASS_FIELD_NUMBER: _ClassVar[int]
    ANALYTICAL_VOLUME_FIELD_NUMBER: _ClassVar[int]
    ANALYTICAL_CENTER_OF_GRAVITY_FIELD_NUMBER: _ClassVar[int]
    ANALYTICAL_CENTER_OF_GRAVITY_X_FIELD_NUMBER: _ClassVar[int]
    ANALYTICAL_CENTER_OF_GRAVITY_Y_FIELD_NUMBER: _ClassVar[int]
    ANALYTICAL_CENTER_OF_GRAVITY_Z_FIELD_NUMBER: _ClassVar[int]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    AREA_FIELD_NUMBER: _ClassVar[int]
    MASS_FIELD_NUMBER: _ClassVar[int]
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    CENTER_OF_GRAVITY_FIELD_NUMBER: _ClassVar[int]
    CENTER_OF_GRAVITY_X_FIELD_NUMBER: _ClassVar[int]
    CENTER_OF_GRAVITY_Y_FIELD_NUMBER: _ClassVar[int]
    CENTER_OF_GRAVITY_Z_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATING_OBJECT_INFO_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    type: DesignStripWizard.Type
    user_defined_name_enabled: bool
    name: str
    surfaces: _containers.RepeatedScalarFieldContainer[int]
    building_grid: int
    grid_plane: DesignStripWizard.GridPlane
    enable_primary_reinforcement_direction: bool
    primary_reinforcement_direction: DesignStripWizard.PrimaryReinforcementDirection
    enable_secondary_reinforcement_direction: bool
    secondary_reinforcement_direction: DesignStripWizard.SecondaryReinforcementDirection
    enable_column_strip_type: bool
    enable_middle_strip_type: bool
    enable_edge_strip_type: bool
    enable_user_defined_strip_width: bool
    user_defined_strip_width: float
    adjust_internal_moment: bool
    primary_parameters: DesignStripWizard.PrimaryParametersTable
    secondary_parameters: DesignStripWizard.SecondaryParametersTable
    analytical_length: float
    analytical_area: float
    analytical_mass: float
    analytical_volume: float
    analytical_center_of_gravity: _common_pb2.Vector3d
    analytical_center_of_gravity_x: float
    analytical_center_of_gravity_y: float
    analytical_center_of_gravity_z: float
    length: float
    area: float
    mass: float
    volume: float
    center_of_gravity: _common_pb2.Vector3d
    center_of_gravity_x: float
    center_of_gravity_y: float
    center_of_gravity_z: float
    comment: str
    is_generated: bool
    generating_object_info: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., type: _Optional[_Union[DesignStripWizard.Type, str]] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., surfaces: _Optional[_Iterable[int]] = ..., building_grid: _Optional[int] = ..., grid_plane: _Optional[_Union[DesignStripWizard.GridPlane, str]] = ..., enable_primary_reinforcement_direction: bool = ..., primary_reinforcement_direction: _Optional[_Union[DesignStripWizard.PrimaryReinforcementDirection, str]] = ..., enable_secondary_reinforcement_direction: bool = ..., secondary_reinforcement_direction: _Optional[_Union[DesignStripWizard.SecondaryReinforcementDirection, str]] = ..., enable_column_strip_type: bool = ..., enable_middle_strip_type: bool = ..., enable_edge_strip_type: bool = ..., enable_user_defined_strip_width: bool = ..., user_defined_strip_width: _Optional[float] = ..., adjust_internal_moment: bool = ..., primary_parameters: _Optional[_Union[DesignStripWizard.PrimaryParametersTable, _Mapping]] = ..., secondary_parameters: _Optional[_Union[DesignStripWizard.SecondaryParametersTable, _Mapping]] = ..., analytical_length: _Optional[float] = ..., analytical_area: _Optional[float] = ..., analytical_mass: _Optional[float] = ..., analytical_volume: _Optional[float] = ..., analytical_center_of_gravity: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., analytical_center_of_gravity_x: _Optional[float] = ..., analytical_center_of_gravity_y: _Optional[float] = ..., analytical_center_of_gravity_z: _Optional[float] = ..., length: _Optional[float] = ..., area: _Optional[float] = ..., mass: _Optional[float] = ..., volume: _Optional[float] = ..., center_of_gravity: _Optional[_Union[_common_pb2.Vector3d, _Mapping]] = ..., center_of_gravity_x: _Optional[float] = ..., center_of_gravity_y: _Optional[float] = ..., center_of_gravity_z: _Optional[float] = ..., comment: _Optional[str] = ..., is_generated: bool = ..., generating_object_info: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
