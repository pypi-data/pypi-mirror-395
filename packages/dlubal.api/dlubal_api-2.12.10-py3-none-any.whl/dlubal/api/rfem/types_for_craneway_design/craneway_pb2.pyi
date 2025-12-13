from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Craneway(_message.Message):
    __slots__ = ("no", "type", "designed_craneway_girders_number", "crane_type", "calculation_method", "craneway_girder_one", "craneway_girder_two", "ultimate_configuration", "serviceability_configuration", "to_design", "members_to_design", "consider_buffers", "start_buffer_position", "start_buffer_height", "end_buffer_position", "end_buffer_height", "assigned_crane_number", "assigned_crane_one", "assigned_crane_two", "assigned_crane_three", "crane_position_increment", "nodal_support_table", "id_for_export_import", "metadata_for_export_import")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        TYPE_UNKNOWN: _ClassVar[Craneway.Type]
    TYPE_UNKNOWN: Craneway.Type
    class DesignedCranewayGirdersNumber(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        DESIGNED_CRANEWAY_GIRDERS_NUMBER_ONE: _ClassVar[Craneway.DesignedCranewayGirdersNumber]
        DESIGNED_CRANEWAY_GIRDERS_NUMBER_TWO: _ClassVar[Craneway.DesignedCranewayGirdersNumber]
    DESIGNED_CRANEWAY_GIRDERS_NUMBER_ONE: Craneway.DesignedCranewayGirdersNumber
    DESIGNED_CRANEWAY_GIRDERS_NUMBER_TWO: Craneway.DesignedCranewayGirdersNumber
    class CraneType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CRANE_TYPE_BRIDGE: _ClassVar[Craneway.CraneType]
        CRANE_TYPE_SUSPENSION: _ClassVar[Craneway.CraneType]
    CRANE_TYPE_BRIDGE: Craneway.CraneType
    CRANE_TYPE_SUSPENSION: Craneway.CraneType
    class CalculationMethod(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CALCULATION_METHOD_PARTIAL_INTERACTION_ONE: _ClassVar[Craneway.CalculationMethod]
        CALCULATION_METHOD_FULL_INTERACTION: _ClassVar[Craneway.CalculationMethod]
        CALCULATION_METHOD_PARTIAL_INTERACTION_TWO: _ClassVar[Craneway.CalculationMethod]
    CALCULATION_METHOD_PARTIAL_INTERACTION_ONE: Craneway.CalculationMethod
    CALCULATION_METHOD_FULL_INTERACTION: Craneway.CalculationMethod
    CALCULATION_METHOD_PARTIAL_INTERACTION_TWO: Craneway.CalculationMethod
    class ConsiderBuffers(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CONSIDER_BUFFERS_NONE: _ClassVar[Craneway.ConsiderBuffers]
        CONSIDER_BUFFERS_BOTH: _ClassVar[Craneway.ConsiderBuffers]
        CONSIDER_BUFFERS_END: _ClassVar[Craneway.ConsiderBuffers]
        CONSIDER_BUFFERS_START: _ClassVar[Craneway.ConsiderBuffers]
    CONSIDER_BUFFERS_NONE: Craneway.ConsiderBuffers
    CONSIDER_BUFFERS_BOTH: Craneway.ConsiderBuffers
    CONSIDER_BUFFERS_END: Craneway.ConsiderBuffers
    CONSIDER_BUFFERS_START: Craneway.ConsiderBuffers
    class AssignedCraneNumber(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ASSIGNED_CRANE_NUMBER_ONE: _ClassVar[Craneway.AssignedCraneNumber]
        ASSIGNED_CRANE_NUMBER_THREE: _ClassVar[Craneway.AssignedCraneNumber]
        ASSIGNED_CRANE_NUMBER_TWO: _ClassVar[Craneway.AssignedCraneNumber]
    ASSIGNED_CRANE_NUMBER_ONE: Craneway.AssignedCraneNumber
    ASSIGNED_CRANE_NUMBER_THREE: Craneway.AssignedCraneNumber
    ASSIGNED_CRANE_NUMBER_TWO: Craneway.AssignedCraneNumber
    class NodalSupportTable(_message.Message):
        __slots__ = ("rows",)
        ROWS_FIELD_NUMBER: _ClassVar[int]
        rows: _containers.RepeatedCompositeFieldContainer[Craneway.NodalSupportTableRow]
        def __init__(self, rows: _Optional[_Iterable[_Union[Craneway.NodalSupportTableRow, _Mapping]]] = ...) -> None: ...
    class NodalSupportTableRow(_message.Message):
        __slots__ = ("no", "description", "assigned_nodes", "support")
        NO_FIELD_NUMBER: _ClassVar[int]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        ASSIGNED_NODES_FIELD_NUMBER: _ClassVar[int]
        SUPPORT_FIELD_NUMBER: _ClassVar[int]
        no: int
        description: str
        assigned_nodes: _containers.RepeatedScalarFieldContainer[int]
        support: int
        def __init__(self, no: _Optional[int] = ..., description: _Optional[str] = ..., assigned_nodes: _Optional[_Iterable[int]] = ..., support: _Optional[int] = ...) -> None: ...
    NO_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DESIGNED_CRANEWAY_GIRDERS_NUMBER_FIELD_NUMBER: _ClassVar[int]
    CRANE_TYPE_FIELD_NUMBER: _ClassVar[int]
    CALCULATION_METHOD_FIELD_NUMBER: _ClassVar[int]
    CRANEWAY_GIRDER_ONE_FIELD_NUMBER: _ClassVar[int]
    CRANEWAY_GIRDER_TWO_FIELD_NUMBER: _ClassVar[int]
    ULTIMATE_CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    SERVICEABILITY_CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    TO_DESIGN_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_TO_DESIGN_FIELD_NUMBER: _ClassVar[int]
    CONSIDER_BUFFERS_FIELD_NUMBER: _ClassVar[int]
    START_BUFFER_POSITION_FIELD_NUMBER: _ClassVar[int]
    START_BUFFER_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    END_BUFFER_POSITION_FIELD_NUMBER: _ClassVar[int]
    END_BUFFER_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_CRANE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_CRANE_ONE_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_CRANE_TWO_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_CRANE_THREE_FIELD_NUMBER: _ClassVar[int]
    CRANE_POSITION_INCREMENT_FIELD_NUMBER: _ClassVar[int]
    NODAL_SUPPORT_TABLE_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    type: Craneway.Type
    designed_craneway_girders_number: Craneway.DesignedCranewayGirdersNumber
    crane_type: Craneway.CraneType
    calculation_method: Craneway.CalculationMethod
    craneway_girder_one: _containers.RepeatedScalarFieldContainer[int]
    craneway_girder_two: _containers.RepeatedScalarFieldContainer[int]
    ultimate_configuration: int
    serviceability_configuration: int
    to_design: bool
    members_to_design: _containers.RepeatedScalarFieldContainer[int]
    consider_buffers: Craneway.ConsiderBuffers
    start_buffer_position: float
    start_buffer_height: float
    end_buffer_position: float
    end_buffer_height: float
    assigned_crane_number: Craneway.AssignedCraneNumber
    assigned_crane_one: int
    assigned_crane_two: int
    assigned_crane_three: int
    crane_position_increment: float
    nodal_support_table: Craneway.NodalSupportTable
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., type: _Optional[_Union[Craneway.Type, str]] = ..., designed_craneway_girders_number: _Optional[_Union[Craneway.DesignedCranewayGirdersNumber, str]] = ..., crane_type: _Optional[_Union[Craneway.CraneType, str]] = ..., calculation_method: _Optional[_Union[Craneway.CalculationMethod, str]] = ..., craneway_girder_one: _Optional[_Iterable[int]] = ..., craneway_girder_two: _Optional[_Iterable[int]] = ..., ultimate_configuration: _Optional[int] = ..., serviceability_configuration: _Optional[int] = ..., to_design: bool = ..., members_to_design: _Optional[_Iterable[int]] = ..., consider_buffers: _Optional[_Union[Craneway.ConsiderBuffers, str]] = ..., start_buffer_position: _Optional[float] = ..., start_buffer_height: _Optional[float] = ..., end_buffer_position: _Optional[float] = ..., end_buffer_height: _Optional[float] = ..., assigned_crane_number: _Optional[_Union[Craneway.AssignedCraneNumber, str]] = ..., assigned_crane_one: _Optional[int] = ..., assigned_crane_two: _Optional[int] = ..., assigned_crane_three: _Optional[int] = ..., crane_position_increment: _Optional[float] = ..., nodal_support_table: _Optional[_Union[Craneway.NodalSupportTable, _Mapping]] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
