from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class DesignAddons(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DESIGN_ADDON_UNKNOWN: _ClassVar[DesignAddons]
    ALUMINUM_DESIGN: _ClassVar[DesignAddons]
    CONCRETE_DESIGN: _ClassVar[DesignAddons]
    CONCRETE_FOUNDATIONS: _ClassVar[DesignAddons]
    STEEL_DESIGN: _ClassVar[DesignAddons]
    STRESS_ANALYSIS: _ClassVar[DesignAddons]
    TIMBER_DESIGN: _ClassVar[DesignAddons]
DESIGN_ADDON_UNKNOWN: DesignAddons
ALUMINUM_DESIGN: DesignAddons
CONCRETE_DESIGN: DesignAddons
CONCRETE_FOUNDATIONS: DesignAddons
STEEL_DESIGN: DesignAddons
STRESS_ANALYSIS: DesignAddons
TIMBER_DESIGN: DesignAddons
