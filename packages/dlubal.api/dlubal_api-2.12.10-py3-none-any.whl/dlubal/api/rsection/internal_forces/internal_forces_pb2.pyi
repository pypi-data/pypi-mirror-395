from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InternalForces(_message.Message):
    __slots__ = ("no", "load_case", "member_no", "location_x", "internal_forces_system", "axial_force_n", "shear_force_v_y", "shear_force_v_z", "torsional_moment_m_xp", "torsional_moment_m_xs", "sum_of_torsional_moments", "bending_moment_m_y", "bending_moment_m_z", "bimoment_m_omega", "shear_force_v_u", "shear_force_v_v", "bending_moment_m_u", "bending_moment_m_v", "comment", "id_for_export_import", "metadata_for_export_import")
    class InternalForcesSystem(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        INTERNAL_FORCES_SYSTEM_PRINCIPAL_AXES_U_V: _ClassVar[InternalForces.InternalForcesSystem]
        INTERNAL_FORCES_SYSTEM_AXES_Y_Z: _ClassVar[InternalForces.InternalForcesSystem]
    INTERNAL_FORCES_SYSTEM_PRINCIPAL_AXES_U_V: InternalForces.InternalForcesSystem
    INTERNAL_FORCES_SYSTEM_AXES_Y_Z: InternalForces.InternalForcesSystem
    NO_FIELD_NUMBER: _ClassVar[int]
    LOAD_CASE_FIELD_NUMBER: _ClassVar[int]
    MEMBER_NO_FIELD_NUMBER: _ClassVar[int]
    LOCATION_X_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_FORCES_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    AXIAL_FORCE_N_FIELD_NUMBER: _ClassVar[int]
    SHEAR_FORCE_V_Y_FIELD_NUMBER: _ClassVar[int]
    SHEAR_FORCE_V_Z_FIELD_NUMBER: _ClassVar[int]
    TORSIONAL_MOMENT_M_XP_FIELD_NUMBER: _ClassVar[int]
    TORSIONAL_MOMENT_M_XS_FIELD_NUMBER: _ClassVar[int]
    SUM_OF_TORSIONAL_MOMENTS_FIELD_NUMBER: _ClassVar[int]
    BENDING_MOMENT_M_Y_FIELD_NUMBER: _ClassVar[int]
    BENDING_MOMENT_M_Z_FIELD_NUMBER: _ClassVar[int]
    BIMOMENT_M_OMEGA_FIELD_NUMBER: _ClassVar[int]
    SHEAR_FORCE_V_U_FIELD_NUMBER: _ClassVar[int]
    SHEAR_FORCE_V_V_FIELD_NUMBER: _ClassVar[int]
    BENDING_MOMENT_M_U_FIELD_NUMBER: _ClassVar[int]
    BENDING_MOMENT_M_V_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    ID_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FOR_EXPORT_IMPORT_FIELD_NUMBER: _ClassVar[int]
    no: int
    load_case: int
    member_no: int
    location_x: float
    internal_forces_system: InternalForces.InternalForcesSystem
    axial_force_n: float
    shear_force_v_y: float
    shear_force_v_z: float
    torsional_moment_m_xp: float
    torsional_moment_m_xs: float
    sum_of_torsional_moments: float
    bending_moment_m_y: float
    bending_moment_m_z: float
    bimoment_m_omega: float
    shear_force_v_u: float
    shear_force_v_v: float
    bending_moment_m_u: float
    bending_moment_m_v: float
    comment: str
    id_for_export_import: str
    metadata_for_export_import: str
    def __init__(self, no: _Optional[int] = ..., load_case: _Optional[int] = ..., member_no: _Optional[int] = ..., location_x: _Optional[float] = ..., internal_forces_system: _Optional[_Union[InternalForces.InternalForcesSystem, str]] = ..., axial_force_n: _Optional[float] = ..., shear_force_v_y: _Optional[float] = ..., shear_force_v_z: _Optional[float] = ..., torsional_moment_m_xp: _Optional[float] = ..., torsional_moment_m_xs: _Optional[float] = ..., sum_of_torsional_moments: _Optional[float] = ..., bending_moment_m_y: _Optional[float] = ..., bending_moment_m_z: _Optional[float] = ..., bimoment_m_omega: _Optional[float] = ..., shear_force_v_u: _Optional[float] = ..., shear_force_v_v: _Optional[float] = ..., bending_moment_m_u: _Optional[float] = ..., bending_moment_m_v: _Optional[float] = ..., comment: _Optional[str] = ..., id_for_export_import: _Optional[str] = ..., metadata_for_export_import: _Optional[str] = ...) -> None: ...
