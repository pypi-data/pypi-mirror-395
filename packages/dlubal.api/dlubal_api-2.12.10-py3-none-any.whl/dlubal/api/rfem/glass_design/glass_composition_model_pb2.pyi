from dlubal.api.common import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GlassCompositionModel(_message.Message):
    __slots__ = ("no", "user_defined_name_enabled", "name", "surfaces", "to_design", "display_stiffness_matrix_for_uncoupled_and_coupled", "calculation_type", "modeling_type", "shear_coupling_between_layers", "stiffness_matrix_elements_uncoupled", "uncoupled_D11", "uncoupled_D12", "uncoupled_D13", "uncoupled_D22", "uncoupled_D23", "uncoupled_D33", "uncoupled_D44", "uncoupled_D45", "uncoupled_D55", "uncoupled_D66", "uncoupled_D67", "uncoupled_D68", "uncoupled_D77", "uncoupled_D78", "uncoupled_D88", "uncoupled_D16", "uncoupled_D17", "uncoupled_D18", "uncoupled_D27", "uncoupled_D28", "uncoupled_D38", "stiffness_matrix_info_uncoupled", "stiffness_matrix_elements_coupled", "coupled_D11", "coupled_D12", "coupled_D13", "coupled_D22", "coupled_D23", "coupled_D33", "coupled_D44", "coupled_D45", "coupled_D55", "coupled_D66", "coupled_D67", "coupled_D68", "coupled_D77", "coupled_D78", "coupled_D88", "coupled_D16", "coupled_D17", "coupled_D18", "coupled_D27", "coupled_D28", "coupled_D38", "stiffness_matrix_info_coupled", "layers_surface_thickness", "layers_reference_table", "layers_total_thickness", "layers_total_weight", "line_supports_table", "nodal_supports_table", "surface_thickness_with_material", "surface_stiffness_type", "surface_geometry_type", "surface_area", "surface_volume", "surface_mass", "surface_total_area", "surface_total_volume", "surface_total_mass", "climatic_loads_summer_parameters", "climatic_loads_winter_parameters", "climatic_loads_summer_parameters_enabled", "climatic_loads_winter_parameters_enabled", "insulating_glass_unit_enabled", "spacer_activated", "spacer_thickness", "supports_for_side_surfaces_of_gas_deactivated", "number_of_finite_element_layers", "comment", "id_for_export_import", "metadata_for_export_import")
    class CalculationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CALCULATION_TYPE_1_PHASE_FULL_MODEL: _ClassVar[GlassCompositionModel.CalculationType]
    CALCULATION_TYPE_1_PHASE_FULL_MODEL: GlassCompositionModel.CalculationType
    class ModelingType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        MODELING_TYPE_SURFACE_MODEL: _ClassVar[GlassCompositionModel.ModelingType]
    MODELING_TYPE_SURFACE_MODEL: GlassCompositionModel.ModelingType
    class ShearCouplingBetweenLayers(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SHEAR_COUPLING_BETWEEN_LAYERS_COUPLED: _ClassVar[GlassCompositionModel.ShearCouplingBetweenLayers]
        SHEAR_COUPLING_BETWEEN_LAYERS_UNCOUPLED: _ClassVar[GlassCompositionModel.ShearCouplingBetweenLayers]
    SHEAR_COUPLING_BETWEEN_LAYERS_COUPLED: GlassCompositionModel.ShearCouplingBetweenLayers
    SHEAR_COUPLING_BETWEEN_LAYERS_UNCOUPLED: GlassCompositionModel.ShearCouplingBetweenLayers
    class SurfaceStiffnessType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SURFACE_STIFFNESS_TYPE_STANDARD: _ClassVar[GlassCompositionModel.SurfaceStiffnessType]
        SURFACE_STIFFNESS_TYPE_DISCONTINUITY: _ClassVar[GlassCompositionModel.SurfaceStiffnessType]
        SURFACE_STIFFNESS_TYPE_FLOOR: _ClassVar[GlassCompositionModel.SurfaceStiffnessType]
        SURFACE_STIFFNESS_TYPE_FLOOR_DIAPHRAGM: _ClassVar[GlassCompositionModel.SurfaceStiffnessType]
        SURFACE_STIFFNESS_TYPE_FLOOR_FLEXIBLE_DIAPHRAGM: _ClassVar[GlassCompositionModel.SurfaceStiffnessType]
        SURFACE_STIFFNESS_TYPE_FLOOR_SEMIRIGID: _ClassVar[GlassCompositionModel.SurfaceStiffnessType]
        SURFACE_STIFFNESS_TYPE_GROUNDWATER: _ClassVar[GlassCompositionModel.SurfaceStiffnessType]
        SURFACE_STIFFNESS_TYPE_LOAD_TRANSFER: _ClassVar[GlassCompositionModel.SurfaceStiffnessType]
        SURFACE_STIFFNESS_TYPE_MEMBRANE: _ClassVar[GlassCompositionModel.SurfaceStiffnessType]
        SURFACE_STIFFNESS_TYPE_RIGID: _ClassVar[GlassCompositionModel.SurfaceStiffnessType]
        SURFACE_STIFFNESS_TYPE_WITHOUT_MEMBRANE_TENSION: _ClassVar[GlassCompositionModel.SurfaceStiffnessType]
        SURFACE_STIFFNESS_TYPE_WITHOUT_THICKNESS: _ClassVar[GlassCompositionModel.SurfaceStiffnessType]
    SURFACE_STIFFNESS_TYPE_STANDARD: GlassCompositionModel.SurfaceStiffnessType
    SURFACE_STIFFNESS_TYPE_DISCONTINUITY: GlassCompositionModel.SurfaceStiffnessType
    SURFACE_STIFFNESS_TYPE_FLOOR: GlassCompositionModel.SurfaceStiffnessType
    SURFACE_STIFFNESS_TYPE_FLOOR_DIAPHRAGM: GlassCompositionModel.SurfaceStiffnessType
    SURFACE_STIFFNESS_TYPE_FLOOR_FLEXIBLE_DIAPHRAGM: GlassCompositionModel.SurfaceStiffnessType
    SURFACE_STIFFNESS_TYPE_FLOOR_SEMIRIGID: GlassCompositionModel.SurfaceStiffnessType
    SURFACE_STIFFNESS_TYPE_GROUNDWATER: GlassCompositionModel.SurfaceStiffnessType
    SURFACE_STIFFNESS_TYPE_LOAD_TRANSFER: GlassCompositionModel.SurfaceStiffnessType
    SURFACE_STIFFNESS_TYPE_MEMBRANE: GlassCompositionModel.SurfaceStiffnessType
    SURFACE_STIFFNESS_TYPE_RIGID: GlassCompositionModel.SurfaceStiffnessType
    SURFACE_STIFFNESS_TYPE_WITHOUT_MEMBRANE_TENSION: GlassCompositionModel.SurfaceStiffnessType
    SURFACE_STIFFNESS_TYPE_WITHOUT_THICKNESS: GlassCompositionModel.SurfaceStiffnessType
    class SurfaceGeometryType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SURFACE_GEOMETRY_TYPE_UNKNOWN: _ClassVar[GlassCompositionModel.SurfaceGeometryType]
        SURFACE_GEOMETRY_TYPE_MINIMUM_CURVATURE_SPLINE: _ClassVar[GlassCompositionModel.SurfaceGeometryType]
        SURFACE_GEOMETRY_TYPE_NURBS: _ClassVar[GlassCompositionModel.SurfaceGeometryType]
        SURFACE_GEOMETRY_TYPE_PIPE: _ClassVar[GlassCompositionModel.SurfaceGeometryType]
        SURFACE_GEOMETRY_TYPE_PLANE: _ClassVar[GlassCompositionModel.SurfaceGeometryType]
        SURFACE_GEOMETRY_TYPE_QUADRANGLE: _ClassVar[GlassCompositionModel.SurfaceGeometryType]
        SURFACE_GEOMETRY_TYPE_ROTATED: _ClassVar[GlassCompositionModel.SurfaceGeometryType]
        SURFACE_GEOMETRY_TYPE_TRIMMED: _ClassVar[GlassCompositionModel.SurfaceGeometryType]
    SURFACE_GEOMETRY_TYPE_UNKNOWN: GlassCompositionModel.SurfaceGeometryType
    SURFACE_GEOMETRY_TYPE_MINIMUM_CURVATURE_SPLINE: GlassCompositionModel.SurfaceGeometryType
    SURFACE_GEOMETRY_TYPE_NURBS: GlassCompositionModel.SurfaceGeometryType
    SURFACE_GEOMETRY_TYPE_PIPE: GlassCompositionModel.SurfaceGeometryType
    SURFACE_GEOMETRY_TYPE_PLANE: GlassCompositionModel.SurfaceGeometryType
    SURFACE_GEOMETRY_TYPE_QUADRANGLE: GlassCompositionModel.SurfaceGeometryType
    SURFACE_GEOMETRY_TYPE_ROTATED: GlassCompositionModel.SurfaceGeometryType
    SURFACE_GEOMETRY_TYPE_TRIMMED: GlassCompositionModel.SurfaceGeometryType
    class StiffnessMatrixElementsUncoupledTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[GlassCompositionModel.StiffnessMatrixElementsUncoupledTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[GlassCompositionModel.StiffnessMatrixElementsUncoupledTreeTableRow, _Mapping]]] = ...) -> None: ...
    class StiffnessMatrixElementsUncoupledTreeTableRow(_message.Message):
        __slots__ = ("key", "caption", "value", "unit", "rows")
        KEY_FIELD_NUMBER: _ClassVar[int]
        CAPTION_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        UNIT_FIELD_NUMBER: _ClassVar[int]
        ROWS_FIELD_NUMBER: _ClassVar[int]
        key: str
        caption: str
        value: float
        unit: str
        rows: _containers.RepeatedCompositeFieldContainer[GlassCompositionModel.StiffnessMatrixElementsUncoupledTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., value: _Optional[float] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[GlassCompositionModel.StiffnessMatrixElementsUncoupledTreeTableRow, _Mapping]]] = ...) -> None: ...
    class StiffnessMatrixInfoUncoupledTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[GlassCompositionModel.StiffnessMatrixInfoUncoupledTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[GlassCompositionModel.StiffnessMatrixInfoUncoupledTreeTableRow, _Mapping]]] = ...) -> None: ...
    class StiffnessMatrixInfoUncoupledTreeTableRow(_message.Message):
        __slots__ = ("key", "description", "value", "unit", "rows")
        KEY_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        UNIT_FIELD_NUMBER: _ClassVar[int]
        ROWS_FIELD_NUMBER: _ClassVar[int]
        key: str
        description: str
        value: float
        unit: str
        rows: _containers.RepeatedCompositeFieldContainer[GlassCompositionModel.StiffnessMatrixInfoUncoupledTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., description: _Optional[str] = ..., value: _Optional[float] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[GlassCompositionModel.StiffnessMatrixInfoUncoupledTreeTableRow, _Mapping]]] = ...) -> None: ...
    class StiffnessMatrixElementsCoupledTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[GlassCompositionModel.StiffnessMatrixElementsCoupledTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[GlassCompositionModel.StiffnessMatrixElementsCoupledTreeTableRow, _Mapping]]] = ...) -> None: ...
    class StiffnessMatrixElementsCoupledTreeTableRow(_message.Message):
        __slots__ = ("key", "caption", "value", "unit", "rows")
        KEY_FIELD_NUMBER: _ClassVar[int]
        CAPTION_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        UNIT_FIELD_NUMBER: _ClassVar[int]
        ROWS_FIELD_NUMBER: _ClassVar[int]
        key: str
        caption: str
        value: float
        unit: str
        rows: _containers.RepeatedCompositeFieldContainer[GlassCompositionModel.StiffnessMatrixElementsCoupledTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., value: _Optional[float] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[GlassCompositionModel.StiffnessMatrixElementsCoupledTreeTableRow, _Mapping]]] = ...) -> None: ...
    class StiffnessMatrixInfoCoupledTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[GlassCompositionModel.StiffnessMatrixInfoCoupledTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[GlassCompositionModel.StiffnessMatrixInfoCoupledTreeTableRow, _Mapping]]] = ...) -> None: ...
    class StiffnessMatrixInfoCoupledTreeTableRow(_message.Message):
        __slots__ = ("key", "description", "value", "unit", "rows")
        KEY_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        UNIT_FIELD_NUMBER: _ClassVar[int]
        ROWS_FIELD_NUMBER: _ClassVar[int]
        key: str
        description: str
        value: float
        unit: str
        rows: _containers.RepeatedCompositeFieldContainer[GlassCompositionModel.StiffnessMatrixInfoCoupledTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., description: _Optional[str] = ..., value: _Optional[float] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[GlassCompositionModel.StiffnessMatrixInfoCoupledTreeTableRow, _Mapping]]] = ...) -> None: ...
    class LayersReferenceTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[GlassCompositionModel.LayersReferenceTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[GlassCompositionModel.LayersReferenceTableRow, _Mapping]]] = ...) -> None: ...
    class LayersReferenceTableRow(_message.Message):
        __slots__ = ("no", "description", "layer_no", "layer_type", "thickness_type_or_id", "material", "thickness", "angle", "integration_points", "connection_with_other_topological_elements", "edge_finishing", "comment", "specific_weight", "weight")
        class LayerType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            LAYER_TYPE_E_LAYER_TYPE_LAYER: _ClassVar[GlassCompositionModel.LayersReferenceTableRow.LayerType]
            LAYER_TYPE_E_LAYER_TYPE_CONTACT: _ClassVar[GlassCompositionModel.LayersReferenceTableRow.LayerType]
            LAYER_TYPE_E_LAYER_TYPE_GAS: _ClassVar[GlassCompositionModel.LayersReferenceTableRow.LayerType]
        LAYER_TYPE_E_LAYER_TYPE_LAYER: GlassCompositionModel.LayersReferenceTableRow.LayerType
        LAYER_TYPE_E_LAYER_TYPE_CONTACT: GlassCompositionModel.LayersReferenceTableRow.LayerType
        LAYER_TYPE_E_LAYER_TYPE_GAS: GlassCompositionModel.LayersReferenceTableRow.LayerType
        class EdgeFinishing(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            EDGE_FINISHING_CLEAN_CUT_EDGES: _ClassVar[GlassCompositionModel.LayersReferenceTableRow.EdgeFinishing]
            EDGE_FINISHING_NONE: _ClassVar[GlassCompositionModel.LayersReferenceTableRow.EdgeFinishing]
            EDGE_FINISHING_POLISHED_EDGES: _ClassVar[GlassCompositionModel.LayersReferenceTableRow.EdgeFinishing]
            EDGE_FINISHING_SEAMED_EDGES: _ClassVar[GlassCompositionModel.LayersReferenceTableRow.EdgeFinishing]
        EDGE_FINISHING_CLEAN_CUT_EDGES: GlassCompositionModel.LayersReferenceTableRow.EdgeFinishing
        EDGE_FINISHING_NONE: GlassCompositionModel.LayersReferenceTableRow.EdgeFinishing
        EDGE_FINISHING_POLISHED_EDGES: GlassCompositionModel.LayersReferenceTableRow.EdgeFinishing
        EDGE_FINISHING_SEAMED_EDGES: GlassCompositionModel.LayersReferenceTableRow.EdgeFinishing
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        LAYER_NO_FIELD_NUMBER: _ClassVar[int]
        LAYER_TYPE_FIELD_NUMBER: _ClassVar[int]
        THICKNESS_TYPE_OR_ID_FIELD_NUMBER: _ClassVar[int]
        MATERIAL_FIELD_NUMBER: _ClassVar[int]
        THICKNESS_FIELD_NUMBER: _ClassVar[int]
        ANGLE_FIELD_NUMBER: _ClassVar[int]
        INTEGRATION_POINTS_FIELD_NUMBER: _ClassVar[int]
        CONNECTION_WITH_OTHER_TOPOLOGICAL_ELEMENTS_FIELD_NUMBER: _ClassVar[int]
        EDGE_FINISHING_FIELD_NUMBER: _ClassVar[int]
        COMMENT_FIELD_NUMBER: _ClassVar[int]
        SPECIFIC_WEIGHT_FIELD_NUMBER: _ClassVar[int]
        WEIGHT_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        layer_no: int
        layer_type: GlassCompositionModel.LayersReferenceTableRow.LayerType
        thickness_type_or_id: str
        material: int
        thickness: float
        angle: float
        integration_points: int
        connection_with_other_topological_elements: bool
        edge_finishing: GlassCompositionModel.LayersReferenceTableRow.EdgeFinishing
        comment: str
        specific_weight: float
        weight: float
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., layer_no: _Optional[int] = ..., layer_type: _Optional[_Union[GlassCompositionModel.LayersReferenceTableRow.LayerType, str]] = ..., thickness_type_or_id: _Optional[str] = ..., material: _Optional[int] = ..., thickness: _Optional[float] = ..., angle: _Optional[float] = ..., integration_points: _Optional[int] = ..., connection_with_other_topological_elements: bool = ..., edge_finishing: _Optional[_Union[GlassCompositionModel.LayersReferenceTableRow.EdgeFinishing, str]] = ..., comment: _Optional[str] = ..., specific_weight: _Optional[float] = ..., weight: _Optional[float] = ...) -> None: ...
    class LineSupportsTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[GlassCompositionModel.LineSupportsTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[GlassCompositionModel.LineSupportsTableRow, _Mapping]]] = ...) -> None: ...
    class LineSupportsTableRow(_message.Message):
        __slots__ = ("no", "description", "object_pack", "layer_no", "support_location", "support")
        class SupportLocation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            SUPPORT_LOCATION_TOP: _ClassVar[GlassCompositionModel.LineSupportsTableRow.SupportLocation]
            SUPPORT_LOCATION_BOTTOM: _ClassVar[GlassCompositionModel.LineSupportsTableRow.SupportLocation]
            SUPPORT_LOCATION_MIDDLE: _ClassVar[GlassCompositionModel.LineSupportsTableRow.SupportLocation]
        SUPPORT_LOCATION_TOP: GlassCompositionModel.LineSupportsTableRow.SupportLocation
        SUPPORT_LOCATION_BOTTOM: GlassCompositionModel.LineSupportsTableRow.SupportLocation
        SUPPORT_LOCATION_MIDDLE: GlassCompositionModel.LineSupportsTableRow.SupportLocation
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        OBJECT_PACK_FIELD_NUMBER: _ClassVar[int]
        LAYER_NO_FIELD_NUMBER: _ClassVar[int]
        SUPPORT_LOCATION_FIELD_NUMBER: _ClassVar[int]
        SUPPORT_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        object_pack: str
        layer_no: str
        support_location: GlassCompositionModel.LineSupportsTableRow.SupportLocation
        support: int
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., object_pack: _Optional[str] = ..., layer_no: _Optional[str] = ..., support_location: _Optional[_Union[GlassCompositionModel.LineSupportsTableRow.SupportLocation, str]] = ..., support: _Optional[int] = ...) -> None: ...
    class NodalSupportsTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[GlassCompositionModel.NodalSupportsTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[GlassCompositionModel.NodalSupportsTableRow, _Mapping]]] = ...) -> None: ...
    class NodalSupportsTableRow(_message.Message):
        __slots__ = ("no", "description", "object_pack", "layer_no", "support_location", "support")
        class SupportLocation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            SUPPORT_LOCATION_TOP: _ClassVar[GlassCompositionModel.NodalSupportsTableRow.SupportLocation]
            SUPPORT_LOCATION_BOTTOM: _ClassVar[GlassCompositionModel.NodalSupportsTableRow.SupportLocation]
            SUPPORT_LOCATION_MIDDLE: _ClassVar[GlassCompositionModel.NodalSupportsTableRow.SupportLocation]
        SUPPORT_LOCATION_TOP: GlassCompositionModel.NodalSupportsTableRow.SupportLocation
        SUPPORT_LOCATION_BOTTOM: GlassCompositionModel.NodalSupportsTableRow.SupportLocation
        SUPPORT_LOCATION_MIDDLE: GlassCompositionModel.NodalSupportsTableRow.SupportLocation
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        OBJECT_PACK_FIELD_NUMBER: _ClassVar[int]
        LAYER_NO_FIELD_NUMBER: _ClassVar[int]
        SUPPORT_LOCATION_FIELD_NUMBER: _ClassVar[int]
        SUPPORT_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        object_pack: str
        layer_no: str
        support_location: GlassCompositionModel.NodalSupportsTableRow.SupportLocation
        support: int
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., object_pack: _Optional[str] = ..., layer_no: _Optional[str] = ..., support_location: _Optional[_Union[GlassCompositionModel.NodalSupportsTableRow.SupportLocation, str]] = ..., support: _Optional[int] = ...) -> None: ...
    class ClimaticLoadsSummerParametersTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[GlassCompositionModel.ClimaticLoadsSummerParametersTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[GlassCompositionModel.ClimaticLoadsSummerParametersTreeTableRow, _Mapping]]] = ...) -> None: ...
    class ClimaticLoadsSummerParametersTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[GlassCompositionModel.ClimaticLoadsSummerParametersTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[GlassCompositionModel.ClimaticLoadsSummerParametersTreeTableRow, _Mapping]]] = ...) -> None: ...
    class ClimaticLoadsWinterParametersTreeTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[GlassCompositionModel.ClimaticLoadsWinterParametersTreeTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[GlassCompositionModel.ClimaticLoadsWinterParametersTreeTableRow, _Mapping]]] = ...) -> None: ...
    class ClimaticLoadsWinterParametersTreeTableRow(_message.Message):
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
        rows: _containers.RepeatedCompositeFieldContainer[GlassCompositionModel.ClimaticLoadsWinterParametersTreeTableRow]
        def __init__(self, key: _Optional[str] = ..., caption: _Optional[str] = ..., symbol: _Optional[str] = ..., value: _Optional[_Union[_common_pb2.Value, _Mapping]] = ..., unit: _Optional[str] = ..., rows: _Optional[_Iterable[_Union[GlassCompositionModel.ClimaticLoadsWinterParametersTreeTableRow, _Mapping]]] = ...) -> None: ...
    NO_FIELD_NUMBER: _ClassVar[int]
    USER_DEFINED_NAME_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SURFACES_FIELD_NUMBER: _ClassVar[int]
    TO_DESIGN_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_STIFFNESS_MATRIX_FOR_UNCOUPLED_AND_COUPLED_FIELD_NUMBER: _ClassVar[int]
    CALCULATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    MODELING_TYPE_FIELD_NUMBER: _ClassVar[int]
    SHEAR_COUPLING_BETWEEN_LAYERS_FIELD_NUMBER: _ClassVar[int]
    STIFFNESS_MATRIX_ELEMENTS_UNCOUPLED_FIELD_NUMBER: _ClassVar[int]
    UNCOUPLED_D11_FIELD_NUMBER: _ClassVar[int]
    UNCOUPLED_D12_FIELD_NUMBER: _ClassVar[int]
    UNCOUPLED_D13_FIELD_NUMBER: _ClassVar[int]
    UNCOUPLED_D22_FIELD_NUMBER: _ClassVar[int]
    UNCOUPLED_D23_FIELD_NUMBER: _ClassVar[int]
    UNCOUPLED_D33_FIELD_NUMBER: _ClassVar[int]
    UNCOUPLED_D44_FIELD_NUMBER: _ClassVar[int]
    UNCOUPLED_D45_FIELD_NUMBER: _ClassVar[int]
    UNCOUPLED_D55_FIELD_NUMBER: _ClassVar[int]
    UNCOUPLED_D66_FIELD_NUMBER: _ClassVar[int]
    UNCOUPLED_D67_FIELD_NUMBER: _ClassVar[int]
    UNCOUPLED_D68_FIELD_NUMBER: _ClassVar[int]
    UNCOUPLED_D77_FIELD_NUMBER: _ClassVar[int]
    UNCOUPLED_D78_FIELD_NUMBER: _ClassVar[int]
    UNCOUPLED_D88_FIELD_NUMBER: _ClassVar[int]
    UNCOUPLED_D16_FIELD_NUMBER: _ClassVar[int]
    UNCOUPLED_D17_FIELD_NUMBER: _ClassVar[int]
    UNCOUPLED_D18_FIELD_NUMBER: _ClassVar[int]
    UNCOUPLED_D27_FIELD_NUMBER: _ClassVar[int]
    UNCOUPLED_D28_FIELD_NUMBER: _ClassVar[int]
    UNCOUPLED_D38_FIELD_NUMBER: _ClassVar[int]
    STIFFNESS_MATRIX_INFO_UNCOUPLED_FIELD_NUMBER: _ClassVar[int]
    STIFFNESS_MATRIX_ELEMENTS_COUPLED_FIELD_NUMBER: _ClassVar[int]
    COUPLED_D11_FIELD_NUMBER: _ClassVar[int]
    COUPLED_D12_FIELD_NUMBER: _ClassVar[int]
    COUPLED_D13_FIELD_NUMBER: _ClassVar[int]
    COUPLED_D22_FIELD_NUMBER: _ClassVar[int]
    COUPLED_D23_FIELD_NUMBER: _ClassVar[int]
    COUPLED_D33_FIELD_NUMBER: _ClassVar[int]
    COUPLED_D44_FIELD_NUMBER: _ClassVar[int]
    COUPLED_D45_FIELD_NUMBER: _ClassVar[int]
    COUPLED_D55_FIELD_NUMBER: _ClassVar[int]
    COUPLED_D66_FIELD_NUMBER: _ClassVar[int]
    COUPLED_D67_FIELD_NUMBER: _ClassVar[int]
    COUPLED_D68_FIELD_NUMBER: _ClassVar[int]
    COUPLED_D77_FIELD_NUMBER: _ClassVar[int]
    COUPLED_D78_FIELD_NUMBER: _ClassVar[int]
    COUPLED_D88_FIELD_NUMBER: _ClassVar[int]
    COUPLED_D16_FIELD_NUMBER: _ClassVar[int]
    COUPLED_D17_FIELD_NUMBER: _ClassVar[int]
    COUPLED_D18_FIELD_NUMBER: _ClassVar[int]
    COUPLED_D27_FIELD_NUMBER: _ClassVar[int]
    COUPLED_D28_FIELD_NUMBER: _ClassVar[int]
    COUPLED_D38_FIELD_NUMBER: _ClassVar[int]
    STIFFNESS_MATRIX_INFO_COUPLED_FIELD_NUMBER: _ClassVar[int]
    LAYERS_SURFACE_THICKNESS_FIELD_NUMBER: _ClassVar[int]
    LAYERS_REFERENCE_TABLE_FIELD_NUMBER: _ClassVar[int]
    LAYERS_TOTAL_THICKNESS_FIELD_NUMBER: _ClassVar[int]
    LAYERS_TOTAL_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    LINE_SUPPORTS_TABLE_FIELD_NUMBER: _ClassVar[int]
    NODAL_SUPPORTS_TABLE_FIELD_NUMBER: _ClassVar[int]
    SURFACE_THICKNESS_WITH_MATERIAL_FIELD_NUMBER: _ClassVar[int]
    SURFACE_STIFFNESS_TYPE_FIELD_NUMBER: _ClassVar[int]
    SURFACE_GEOMETRY_TYPE_FIELD_NUMBER: _ClassVar[int]
    SURFACE_AREA_FIELD_NUMBER: _ClassVar[int]
    SURFACE_VOLUME_FIELD_NUMBER: _ClassVar[int]
    SURFACE_MASS_FIELD_NUMBER: _ClassVar[int]
    SURFACE_TOTAL_AREA_FIELD_NUMBER: _ClassVar[int]
    SURFACE_TOTAL_VOLUME_FIELD_NUMBER: _ClassVar[int]
    SURFACE_TOTAL_MASS_FIELD_NUMBER: _ClassVar[int]
    CLIMATIC_LOADS_SUMMER_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    CLIMATIC_LOADS_WINTER_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    CLIMATIC_LOADS_SUMMER_PARAMETERS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    CLIMATIC_LOADS_WINTER_PARAMETERS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    INSULATING_GLASS_UNIT_ENABLED_FIELD_NUMBER: _ClassVar[int]
    SPACER_ACTIVATED_FIELD_NUMBER: _ClassVar[int]
    SPACER_THICKNESS_FIELD_NUMBER: _ClassVar[int]
    SUPPORTS_FOR_SIDE_SURFACES_OF_GAS_DEACTIVATED_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_FINITE_ELEMENT_LAYERS_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    user_defined_name_enabled: bool
    name: str
    surfaces: _containers.RepeatedScalarFieldContainer[int]
    to_design: bool
    display_stiffness_matrix_for_uncoupled_and_coupled: bool
    calculation_type: GlassCompositionModel.CalculationType
    modeling_type: GlassCompositionModel.ModelingType
    shear_coupling_between_layers: GlassCompositionModel.ShearCouplingBetweenLayers
    stiffness_matrix_elements_uncoupled: GlassCompositionModel.StiffnessMatrixElementsUncoupledTreeTable
    uncoupled_D11: float
    uncoupled_D12: float
    uncoupled_D13: float
    uncoupled_D22: float
    uncoupled_D23: float
    uncoupled_D33: float
    uncoupled_D44: float
    uncoupled_D45: float
    uncoupled_D55: float
    uncoupled_D66: float
    uncoupled_D67: float
    uncoupled_D68: float
    uncoupled_D77: float
    uncoupled_D78: float
    uncoupled_D88: float
    uncoupled_D16: float
    uncoupled_D17: float
    uncoupled_D18: float
    uncoupled_D27: float
    uncoupled_D28: float
    uncoupled_D38: float
    stiffness_matrix_info_uncoupled: GlassCompositionModel.StiffnessMatrixInfoUncoupledTreeTable
    stiffness_matrix_elements_coupled: GlassCompositionModel.StiffnessMatrixElementsCoupledTreeTable
    coupled_D11: float
    coupled_D12: float
    coupled_D13: float
    coupled_D22: float
    coupled_D23: float
    coupled_D33: float
    coupled_D44: float
    coupled_D45: float
    coupled_D55: float
    coupled_D66: float
    coupled_D67: float
    coupled_D68: float
    coupled_D77: float
    coupled_D78: float
    coupled_D88: float
    coupled_D16: float
    coupled_D17: float
    coupled_D18: float
    coupled_D27: float
    coupled_D28: float
    coupled_D38: float
    stiffness_matrix_info_coupled: GlassCompositionModel.StiffnessMatrixInfoCoupledTreeTable
    layers_surface_thickness: int
    layers_reference_table: GlassCompositionModel.LayersReferenceTable
    layers_total_thickness: float
    layers_total_weight: float
    line_supports_table: GlassCompositionModel.LineSupportsTable
    nodal_supports_table: GlassCompositionModel.NodalSupportsTable
    surface_thickness_with_material: int
    surface_stiffness_type: GlassCompositionModel.SurfaceStiffnessType
    surface_geometry_type: GlassCompositionModel.SurfaceGeometryType
    surface_area: float
    surface_volume: float
    surface_mass: float
    surface_total_area: float
    surface_total_volume: float
    surface_total_mass: float
    climatic_loads_summer_parameters: GlassCompositionModel.ClimaticLoadsSummerParametersTreeTable
    climatic_loads_winter_parameters: GlassCompositionModel.ClimaticLoadsWinterParametersTreeTable
    climatic_loads_summer_parameters_enabled: bool
    climatic_loads_winter_parameters_enabled: bool
    insulating_glass_unit_enabled: bool
    spacer_activated: bool
    spacer_thickness: int
    supports_for_side_surfaces_of_gas_deactivated: bool
    number_of_finite_element_layers: int
    comment: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., user_defined_name_enabled: bool = ..., name: _Optional[str] = ..., surfaces: _Optional[_Iterable[int]] = ..., to_design: bool = ..., display_stiffness_matrix_for_uncoupled_and_coupled: bool = ..., calculation_type: _Optional[_Union[GlassCompositionModel.CalculationType, str]] = ..., modeling_type: _Optional[_Union[GlassCompositionModel.ModelingType, str]] = ..., shear_coupling_between_layers: _Optional[_Union[GlassCompositionModel.ShearCouplingBetweenLayers, str]] = ..., stiffness_matrix_elements_uncoupled: _Optional[_Union[GlassCompositionModel.StiffnessMatrixElementsUncoupledTreeTable, _Mapping]] = ..., uncoupled_D11: _Optional[float] = ..., uncoupled_D12: _Optional[float] = ..., uncoupled_D13: _Optional[float] = ..., uncoupled_D22: _Optional[float] = ..., uncoupled_D23: _Optional[float] = ..., uncoupled_D33: _Optional[float] = ..., uncoupled_D44: _Optional[float] = ..., uncoupled_D45: _Optional[float] = ..., uncoupled_D55: _Optional[float] = ..., uncoupled_D66: _Optional[float] = ..., uncoupled_D67: _Optional[float] = ..., uncoupled_D68: _Optional[float] = ..., uncoupled_D77: _Optional[float] = ..., uncoupled_D78: _Optional[float] = ..., uncoupled_D88: _Optional[float] = ..., uncoupled_D16: _Optional[float] = ..., uncoupled_D17: _Optional[float] = ..., uncoupled_D18: _Optional[float] = ..., uncoupled_D27: _Optional[float] = ..., uncoupled_D28: _Optional[float] = ..., uncoupled_D38: _Optional[float] = ..., stiffness_matrix_info_uncoupled: _Optional[_Union[GlassCompositionModel.StiffnessMatrixInfoUncoupledTreeTable, _Mapping]] = ..., stiffness_matrix_elements_coupled: _Optional[_Union[GlassCompositionModel.StiffnessMatrixElementsCoupledTreeTable, _Mapping]] = ..., coupled_D11: _Optional[float] = ..., coupled_D12: _Optional[float] = ..., coupled_D13: _Optional[float] = ..., coupled_D22: _Optional[float] = ..., coupled_D23: _Optional[float] = ..., coupled_D33: _Optional[float] = ..., coupled_D44: _Optional[float] = ..., coupled_D45: _Optional[float] = ..., coupled_D55: _Optional[float] = ..., coupled_D66: _Optional[float] = ..., coupled_D67: _Optional[float] = ..., coupled_D68: _Optional[float] = ..., coupled_D77: _Optional[float] = ..., coupled_D78: _Optional[float] = ..., coupled_D88: _Optional[float] = ..., coupled_D16: _Optional[float] = ..., coupled_D17: _Optional[float] = ..., coupled_D18: _Optional[float] = ..., coupled_D27: _Optional[float] = ..., coupled_D28: _Optional[float] = ..., coupled_D38: _Optional[float] = ..., stiffness_matrix_info_coupled: _Optional[_Union[GlassCompositionModel.StiffnessMatrixInfoCoupledTreeTable, _Mapping]] = ..., layers_surface_thickness: _Optional[int] = ..., layers_reference_table: _Optional[_Union[GlassCompositionModel.LayersReferenceTable, _Mapping]] = ..., layers_total_thickness: _Optional[float] = ..., layers_total_weight: _Optional[float] = ..., line_supports_table: _Optional[_Union[GlassCompositionModel.LineSupportsTable, _Mapping]] = ..., nodal_supports_table: _Optional[_Union[GlassCompositionModel.NodalSupportsTable, _Mapping]] = ..., surface_thickness_with_material: _Optional[int] = ..., surface_stiffness_type: _Optional[_Union[GlassCompositionModel.SurfaceStiffnessType, str]] = ..., surface_geometry_type: _Optional[_Union[GlassCompositionModel.SurfaceGeometryType, str]] = ..., surface_area: _Optional[float] = ..., surface_volume: _Optional[float] = ..., surface_mass: _Optional[float] = ..., surface_total_area: _Optional[float] = ..., surface_total_volume: _Optional[float] = ..., surface_total_mass: _Optional[float] = ..., climatic_loads_summer_parameters: _Optional[_Union[GlassCompositionModel.ClimaticLoadsSummerParametersTreeTable, _Mapping]] = ..., climatic_loads_winter_parameters: _Optional[_Union[GlassCompositionModel.ClimaticLoadsWinterParametersTreeTable, _Mapping]] = ..., climatic_loads_summer_parameters_enabled: bool = ..., climatic_loads_winter_parameters_enabled: bool = ..., insulating_glass_unit_enabled: bool = ..., spacer_activated: bool = ..., spacer_thickness: _Optional[int] = ..., supports_for_side_surfaces_of_gas_deactivated: bool = ..., number_of_finite_element_layers: _Optional[int] = ..., comment: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
