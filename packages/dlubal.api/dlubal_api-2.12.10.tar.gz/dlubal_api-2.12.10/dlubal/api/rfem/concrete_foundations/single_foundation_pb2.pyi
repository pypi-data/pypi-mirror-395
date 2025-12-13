from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SingleFoundation(_message.Message):
    __slots__ = ("no", "foundation_type", "user_defined_name_enabled", "name", "nodal_supports", "plate_material", "bucket_material", "design_properties_enabled", "geometry_config", "plate_reinforcement_config", "bucket_reinforcement_config", "rough_bucket_reinforcement_config", "block_reinforcement_config", "reinforcement_material", "reinforcement_type", "plate_reinforcement_automatically_enabled", "horizontal_stirrups_type", "bucket_block_reinforcement_automatically_enabled", "concrete_cover_user_defined_enabled", "concrete_cover_different_at_section_sides_enabled", "concrete_cover", "concrete_cover_surface_top", "concrete_cover_surface_bottom", "concrete_cover_surface_side", "concrete_cover_bucket_or_block", "concrete_cover_min", "concrete_cover_min_surface_top", "concrete_cover_min_surface_bottom", "concrete_cover_min_surface_side", "concrete_cover_min_bucket_or_block", "concrete_durability", "concrete_durability_surface_top", "concrete_durability_surface_bottom", "concrete_durability_surface_side", "concrete_durability_bucket", "soil_definition_type", "subsoil_condition_type", "soil_layer_bottom", "soil_layer_middle", "soil_layer_top", "soil_parameters", "to_design", "selected_nodes", "nodes_to_design", "nodes_removed_from_design", "not_valid_deactivated_nodes", "all_nodes_to_design", "concrete_design_configuration", "geotechnical_design_configuration", "borehole", "borehole_soil_layers", "is_generated", "generated_by", "comment", "id_for_export_import", "metadata_for_export_import")
    class FoundationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        FOUNDATION_TYPE_UNKNOWN: _ClassVar[SingleFoundation.FoundationType]
        FOUNDATION_TYPE_BLOCK_FOUNDATION_WITH_ROUGH_BUCKET_SIDES: _ClassVar[SingleFoundation.FoundationType]
        FOUNDATION_TYPE_BLOCK_FOUNDATION_WITH_SMOOTH_BUCKET_SIDES: _ClassVar[SingleFoundation.FoundationType]
        FOUNDATION_TYPE_BUCKET_FOUNDATION_WITH_ROUGH_BUCKET_SIDES: _ClassVar[SingleFoundation.FoundationType]
        FOUNDATION_TYPE_BUCKET_FOUNDATION_WITH_SMOOTH_BUCKET_SIDES: _ClassVar[SingleFoundation.FoundationType]
        FOUNDATION_TYPE_FOUNDATION_PLATE: _ClassVar[SingleFoundation.FoundationType]
        FOUNDATION_TYPE_FOUNDATION_PLATE_WITHOUT_REINFORCEMENT: _ClassVar[SingleFoundation.FoundationType]
        FOUNDATION_TYPE_STEPPED_FOUNDATION: _ClassVar[SingleFoundation.FoundationType]
        FOUNDATION_TYPE_STEPPED_FOUNDATION_WITHOUT_REINFORCEMENT: _ClassVar[SingleFoundation.FoundationType]
    FOUNDATION_TYPE_UNKNOWN: SingleFoundation.FoundationType
    FOUNDATION_TYPE_BLOCK_FOUNDATION_WITH_ROUGH_BUCKET_SIDES: SingleFoundation.FoundationType
    FOUNDATION_TYPE_BLOCK_FOUNDATION_WITH_SMOOTH_BUCKET_SIDES: SingleFoundation.FoundationType
    FOUNDATION_TYPE_BUCKET_FOUNDATION_WITH_ROUGH_BUCKET_SIDES: SingleFoundation.FoundationType
    FOUNDATION_TYPE_BUCKET_FOUNDATION_WITH_SMOOTH_BUCKET_SIDES: SingleFoundation.FoundationType
    FOUNDATION_TYPE_FOUNDATION_PLATE: SingleFoundation.FoundationType
    FOUNDATION_TYPE_FOUNDATION_PLATE_WITHOUT_REINFORCEMENT: SingleFoundation.FoundationType
    FOUNDATION_TYPE_STEPPED_FOUNDATION: SingleFoundation.FoundationType
    FOUNDATION_TYPE_STEPPED_FOUNDATION_WITHOUT_REINFORCEMENT: SingleFoundation.FoundationType
    class ReinforcementType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        REINFORCEMENT_TYPE_MESH_AND_REBARS: _ClassVar[SingleFoundation.ReinforcementType]
        REINFORCEMENT_TYPE_MESH: _ClassVar[SingleFoundation.ReinforcementType]
        REINFORCEMENT_TYPE_REBARS: _ClassVar[SingleFoundation.ReinforcementType]
    REINFORCEMENT_TYPE_MESH_AND_REBARS: SingleFoundation.ReinforcementType
    REINFORCEMENT_TYPE_MESH: SingleFoundation.ReinforcementType
    REINFORCEMENT_TYPE_REBARS: SingleFoundation.ReinforcementType
    class HorizontalStirrupsType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        HORIZONTAL_STIRRUPS_TYPE_ENCLOSING_COLUMN: _ClassVar[SingleFoundation.HorizontalStirrupsType]
        HORIZONTAL_STIRRUPS_TYPE_ENTIRELY_LOCATED_IN_BUCKET_WALL: _ClassVar[SingleFoundation.HorizontalStirrupsType]
    HORIZONTAL_STIRRUPS_TYPE_ENCLOSING_COLUMN: SingleFoundation.HorizontalStirrupsType
    HORIZONTAL_STIRRUPS_TYPE_ENTIRELY_LOCATED_IN_BUCKET_WALL: SingleFoundation.HorizontalStirrupsType
    class SoilDefinitionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SOIL_DEFINITION_TYPE_SINGLE_LAYERED: _ClassVar[SingleFoundation.SoilDefinitionType]
        SOIL_DEFINITION_TYPE_MULTILAYERED_BOREHOLE: _ClassVar[SingleFoundation.SoilDefinitionType]
        SOIL_DEFINITION_TYPE_MULTILAYERED_SOIL_MASSIF: _ClassVar[SingleFoundation.SoilDefinitionType]
    SOIL_DEFINITION_TYPE_SINGLE_LAYERED: SingleFoundation.SoilDefinitionType
    SOIL_DEFINITION_TYPE_MULTILAYERED_BOREHOLE: SingleFoundation.SoilDefinitionType
    SOIL_DEFINITION_TYPE_MULTILAYERED_SOIL_MASSIF: SingleFoundation.SoilDefinitionType
    class SubsoilConditionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUBSOIL_CONDITION_TYPE_DRAINED: _ClassVar[SingleFoundation.SubsoilConditionType]
        SUBSOIL_CONDITION_TYPE_UNDRAINED: _ClassVar[SingleFoundation.SubsoilConditionType]
    SUBSOIL_CONDITION_TYPE_DRAINED: SingleFoundation.SubsoilConditionType
    SUBSOIL_CONDITION_TYPE_UNDRAINED: SingleFoundation.SubsoilConditionType
    class GeometryConfigTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SingleFoundation.GeometryConfigTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SingleFoundation.GeometryConfigTreeTableRow, _Mapping]]] = ...) -> None: ...
    class GeometryConfigTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[SingleFoundation.GeometryConfigTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SingleFoundation.GeometryConfigTreeTableRow, _Mapping]]] = ...) -> None: ...
    class PlateReinforcementConfigTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SingleFoundation.PlateReinforcementConfigTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SingleFoundation.PlateReinforcementConfigTreeTableRow, _Mapping]]] = ...) -> None: ...
    class PlateReinforcementConfigTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[SingleFoundation.PlateReinforcementConfigTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SingleFoundation.PlateReinforcementConfigTreeTableRow, _Mapping]]] = ...) -> None: ...
    class BucketReinforcementConfigTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SingleFoundation.BucketReinforcementConfigTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SingleFoundation.BucketReinforcementConfigTreeTableRow, _Mapping]]] = ...) -> None: ...
    class BucketReinforcementConfigTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[SingleFoundation.BucketReinforcementConfigTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SingleFoundation.BucketReinforcementConfigTreeTableRow, _Mapping]]] = ...) -> None: ...
    class RoughBucketReinforcementConfigTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SingleFoundation.RoughBucketReinforcementConfigTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SingleFoundation.RoughBucketReinforcementConfigTreeTableRow, _Mapping]]] = ...) -> None: ...
    class RoughBucketReinforcementConfigTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[SingleFoundation.RoughBucketReinforcementConfigTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SingleFoundation.RoughBucketReinforcementConfigTreeTableRow, _Mapping]]] = ...) -> None: ...
    class BlockReinforcementConfigTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SingleFoundation.BlockReinforcementConfigTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SingleFoundation.BlockReinforcementConfigTreeTableRow, _Mapping]]] = ...) -> None: ...
    class BlockReinforcementConfigTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[SingleFoundation.BlockReinforcementConfigTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SingleFoundation.BlockReinforcementConfigTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SoilParametersTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SingleFoundation.SoilParametersTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SingleFoundation.SoilParametersTreeTableRow, _Mapping]]] = ...) -> None: ...
    class SoilParametersTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[SingleFoundation.SoilParametersTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[SingleFoundation.SoilParametersTreeTableRow, _Mapping]]] = ...) -> None: ...
    class BoreholeSoilLayersTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[SingleFoundation.BoreholeSoilLayersRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[SingleFoundation.BoreholeSoilLayersRow, _Mapping]]] = ...) -> None: ...
    class BoreholeSoilLayersRow(_message.Message):
        __slots__ = ("no", "description", "layer_no", "soil_material", "depth", "bottom_ordinate_below_gl", "bottom_ordinate_below_foundation")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        LAYER_NO_FIELD_NUMBER: _ClassVar[int]
        SOIL_MATERIAL_FIELD_NUMBER: _ClassVar[int]
        DEPTH_FIELD_NUMBER: _ClassVar[int]
        BOTTOM_ORDINATE_BELOW_GL_FIELD_NUMBER: _ClassVar[int]
        BOTTOM_ORDINATE_BELOW_FOUNDATION_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        layer_no: int
        soil_material: int
        depth: float
        bottom_ordinate_below_gl: float
        bottom_ordinate_below_foundation: float
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., layer_no: _Optional[int] = ..., soil_material: _Optional[int] = ..., depth: _Optional[float] = ..., bottom_ordinate_below_gl: _Optional[float] = ..., bottom_ordinate_below_foundation: _Optional[float] = ...) -> None: ...
    NO_FIELD_NUMBER: _ClassVar[int]
    FOUNDATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NODAL_SUPPORTS_FIELD_NUMBER: _ClassVar[int]
    PLATE_MATERIAL_FIELD_NUMBER: _ClassVar[int]
    BUCKET_MATERIAL_FIELD_NUMBER: _ClassVar[int]
    DESIGN_PROPERTIES_ENABLED_FIELD_NUMBER: _ClassVar[int]
    GEOMETRY_CONFIG_FIELD_NUMBER: _ClassVar[int]
    PLATE_REINFORCEMENT_CONFIG_FIELD_NUMBER: _ClassVar[int]
    BUCKET_REINFORCEMENT_CONFIG_FIELD_NUMBER: _ClassVar[int]
    ROUGH_BUCKET_REINFORCEMENT_CONFIG_FIELD_NUMBER: _ClassVar[int]
    BLOCK_REINFORCEMENT_CONFIG_FIELD_NUMBER: _ClassVar[int]
    REINFORCEMENT_MATERIAL_FIELD_NUMBER: _ClassVar[int]
    REINFORCEMENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    PLATE_REINFORCEMENT_AUTOMATICALLY_ENABLED_FIELD_NUMBER: _ClassVar[int]
    HORIZONTAL_STIRRUPS_TYPE_FIELD_NUMBER: _ClassVar[int]
    BUCKET_BLOCK_REINFORCEMENT_AUTOMATICALLY_ENABLED_FIELD_NUMBER: _ClassVar[int]
    CONCRETE_COVER_USER_DEFINED_ENABLED_FIELD_NUMBER: _ClassVar[int]
    CONCRETE_COVER_DIFFERENT_AT_SECTION_SIDES_ENABLED_FIELD_NUMBER: _ClassVar[int]
    CONCRETE_COVER_FIELD_NUMBER: _ClassVar[int]
    CONCRETE_COVER_SURFACE_TOP_FIELD_NUMBER: _ClassVar[int]
    CONCRETE_COVER_SURFACE_BOTTOM_FIELD_NUMBER: _ClassVar[int]
    CONCRETE_COVER_SURFACE_SIDE_FIELD_NUMBER: _ClassVar[int]
    CONCRETE_COVER_BUCKET_OR_BLOCK_FIELD_NUMBER: _ClassVar[int]
    CONCRETE_COVER_MIN_FIELD_NUMBER: _ClassVar[int]
    CONCRETE_COVER_MIN_SURFACE_TOP_FIELD_NUMBER: _ClassVar[int]
    CONCRETE_COVER_MIN_SURFACE_BOTTOM_FIELD_NUMBER: _ClassVar[int]
    CONCRETE_COVER_MIN_SURFACE_SIDE_FIELD_NUMBER: _ClassVar[int]
    CONCRETE_COVER_MIN_BUCKET_OR_BLOCK_FIELD_NUMBER: _ClassVar[int]
    CONCRETE_DURABILITY_FIELD_NUMBER: _ClassVar[int]
    CONCRETE_DURABILITY_SURFACE_TOP_FIELD_NUMBER: _ClassVar[int]
    CONCRETE_DURABILITY_SURFACE_BOTTOM_FIELD_NUMBER: _ClassVar[int]
    CONCRETE_DURABILITY_SURFACE_SIDE_FIELD_NUMBER: _ClassVar[int]
    CONCRETE_DURABILITY_BUCKET_FIELD_NUMBER: _ClassVar[int]
    SOIL_DEFINITION_TYPE_FIELD_NUMBER: _ClassVar[int]
    SUBSOIL_CONDITION_TYPE_FIELD_NUMBER: _ClassVar[int]
    SOIL_LAYER_BOTTOM_FIELD_NUMBER: _ClassVar[int]
    SOIL_LAYER_MIDDLE_FIELD_NUMBER: _ClassVar[int]
    SOIL_LAYER_TOP_FIELD_NUMBER: _ClassVar[int]
    SOIL_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    TO_DESIGN_FIELD_NUMBER: _ClassVar[int]
    SELECTED_NODES_FIELD_NUMBER: _ClassVar[int]
    NODES_TO_DESIGN_FIELD_NUMBER: _ClassVar[int]
    NODES_REMOVED_FROM_DESIGN_FIELD_NUMBER: _ClassVar[int]
    NOT_VALID_DEACTIVATED_NODES_FIELD_NUMBER: _ClassVar[int]
    ALL_NODES_TO_DESIGN_FIELD_NUMBER: _ClassVar[int]
    CONCRETE_DESIGN_CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    GEOTECHNICAL_DESIGN_CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    BOREHOLE_FIELD_NUMBER: _ClassVar[int]
    BOREHOLE_SOIL_LAYERS_FIELD_NUMBER: _ClassVar[int]
    IS_GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATED_BY_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    foundation_type: SingleFoundation.FoundationType
    user_defined_name_enabled: bool
    name: str
    nodal_supports: _containers.RepeatedScalarFieldContainer[int]
    plate_material: int
    bucket_material: int
    design_properties_enabled: bool
    geometry_config: SingleFoundation.GeometryConfigTreeTable
    plate_reinforcement_config: SingleFoundation.PlateReinforcementConfigTreeTable
    bucket_reinforcement_config: SingleFoundation.BucketReinforcementConfigTreeTable
    rough_bucket_reinforcement_config: SingleFoundation.RoughBucketReinforcementConfigTreeTable
    block_reinforcement_config: SingleFoundation.BlockReinforcementConfigTreeTable
    reinforcement_material: int
    reinforcement_type: SingleFoundation.ReinforcementType
    plate_reinforcement_automatically_enabled: bool
    horizontal_stirrups_type: SingleFoundation.HorizontalStirrupsType
    bucket_block_reinforcement_automatically_enabled: bool
    concrete_cover_user_defined_enabled: bool
    concrete_cover_different_at_section_sides_enabled: bool
    concrete_cover: float
    concrete_cover_surface_top: float
    concrete_cover_surface_bottom: float
    concrete_cover_surface_side: float
    concrete_cover_bucket_or_block: float
    concrete_cover_min: float
    concrete_cover_min_surface_top: float
    concrete_cover_min_surface_bottom: float
    concrete_cover_min_surface_side: float
    concrete_cover_min_bucket_or_block: float
    concrete_durability: int
    concrete_durability_surface_top: int
    concrete_durability_surface_bottom: int
    concrete_durability_surface_side: int
    concrete_durability_bucket: int
    soil_definition_type: SingleFoundation.SoilDefinitionType
    subsoil_condition_type: SingleFoundation.SubsoilConditionType
    soil_layer_bottom: int
    soil_layer_middle: int
    soil_layer_top: int
    soil_parameters: SingleFoundation.SoilParametersTreeTable
    to_design: bool
    selected_nodes: _containers.RepeatedScalarFieldContainer[int]
    nodes_to_design: _containers.RepeatedScalarFieldContainer[int]
    nodes_removed_from_design: _containers.RepeatedScalarFieldContainer[int]
    not_valid_deactivated_nodes: _containers.RepeatedScalarFieldContainer[int]
    all_nodes_to_design: bool
    concrete_design_configuration: int
    geotechnical_design_configuration: int
    borehole: int
    borehole_soil_layers: SingleFoundation.BoreholeSoilLayersTable
    is_generated: bool
    generated_by: str
    comment: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., foundation_type: _Optional[_Union[SingleFoundation.FoundationType, str]] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., nodal_supports: _Optional[_Iterable[int]] = ..., plate_material: _Optional[int] = ..., bucket_material: _Optional[int] = ..., design_properties_enabled: bool = ..., geometry_config: _Optional[_Union[SingleFoundation.GeometryConfigTreeTable, _Mapping]] = ..., plate_reinforcement_config: _Optional[_Union[SingleFoundation.PlateReinforcementConfigTreeTable, _Mapping]] = ..., bucket_reinforcement_config: _Optional[_Union[SingleFoundation.BucketReinforcementConfigTreeTable, _Mapping]] = ..., rough_bucket_reinforcement_config: _Optional[_Union[SingleFoundation.RoughBucketReinforcementConfigTreeTable, _Mapping]] = ..., block_reinforcement_config: _Optional[_Union[SingleFoundation.BlockReinforcementConfigTreeTable, _Mapping]] = ..., reinforcement_material: _Optional[int] = ..., reinforcement_type: _Optional[_Union[SingleFoundation.ReinforcementType, str]] = ..., plate_reinforcement_automatically_enabled: bool = ..., horizontal_stirrups_type: _Optional[_Union[SingleFoundation.HorizontalStirrupsType, str]] = ..., bucket_block_reinforcement_automatically_enabled: bool = ..., concrete_cover_user_defined_enabled: bool = ..., concrete_cover_different_at_section_sides_enabled: bool = ..., concrete_cover: _Optional[float] = ..., concrete_cover_surface_top: _Optional[float] = ..., concrete_cover_surface_bottom: _Optional[float] = ..., concrete_cover_surface_side: _Optional[float] = ..., concrete_cover_bucket_or_block: _Optional[float] = ..., concrete_cover_min: _Optional[float] = ..., concrete_cover_min_surface_top: _Optional[float] = ..., concrete_cover_min_surface_bottom: _Optional[float] = ..., concrete_cover_min_surface_side: _Optional[float] = ..., concrete_cover_min_bucket_or_block: _Optional[float] = ..., concrete_durability: _Optional[int] = ..., concrete_durability_surface_top: _Optional[int] = ..., concrete_durability_surface_bottom: _Optional[int] = ..., concrete_durability_surface_side: _Optional[int] = ..., concrete_durability_bucket: _Optional[int] = ..., soil_definition_type: _Optional[_Union[SingleFoundation.SoilDefinitionType, str]] = ..., subsoil_condition_type: _Optional[_Union[SingleFoundation.SubsoilConditionType, str]] = ..., soil_layer_bottom: _Optional[int] = ..., soil_layer_middle: _Optional[int] = ..., soil_layer_top: _Optional[int] = ..., soil_parameters: _Optional[_Union[SingleFoundation.SoilParametersTreeTable, _Mapping]] = ..., to_design: bool = ..., selected_nodes: _Optional[_Iterable[int]] = ..., nodes_to_design: _Optional[_Iterable[int]] = ..., nodes_removed_from_design: _Optional[_Iterable[int]] = ..., not_valid_deactivated_nodes: _Optional[_Iterable[int]] = ..., all_nodes_to_design: bool = ..., concrete_design_configuration: _Optional[int] = ..., geotechnical_design_configuration: _Optional[int] = ..., borehole: _Optional[int] = ..., borehole_soil_layers: _Optional[_Union[SingleFoundation.BoreholeSoilLayersTable, _Mapping]] = ..., is_generated: bool = ..., generated_by: _Optional[str] = ..., comment: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
