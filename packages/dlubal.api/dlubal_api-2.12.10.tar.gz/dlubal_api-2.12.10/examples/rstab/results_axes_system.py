from dlubal.api import rstab, common

with rstab.Application() as rstab_app:

    # --- Support Forces ---
    # The direction of support forces can be defined in either the Local (default) or Global
    # Coordinate System (CS). This choice affects how the support reactions are
    # recalculated and aligned with the selected coordinate system for correct results.

    # Get results
    support_forces: common.Table = rstab_app.get_results(
        results_type=rstab.results.ResultsType.STATIC_ANALYSIS_NODES_SUPPORT_FORCES,
        support_coordinate_system=rstab.results.settings.CoordinateSystem.COORDINATE_SYSTEM_GLOBAL
    )
    print(f"\nSupport Forces:\n{support_forces.data}")

    # Get result table
    support_forces_table: common.Table = rstab_app.get_result_table(
        table=rstab.results.ResultTable.STATIC_ANALYSIS_NODES_SUPPORT_FORCES_TABLE,
        loading= rstab.ObjectId(
            no=1,
            object_type=rstab.OBJECT_TYPE_LOAD_CASE
        ),
        support_coordinate_system=rstab.results.settings.CoordinateSystem.COORDINATE_SYSTEM_GLOBAL
    )
    print(f"\nSupport Forces Table:\n{support_forces_table.data}")


    # --- Member Forces ---
    # Member forces can be defined in either the Member Local XYZ (default)
    # or the Principal Axes XUV coordinate system. This choice determines how
    # the forces are calculated and aligned according to the respective axes
    # system of the member's geometry.

    # Get results
    member_forces: common.Table = rstab_app.get_results(
        results_type=rstab.results.ResultsType.STATIC_ANALYSIS_MEMBERS_INTERNAL_FORCES,
        member_axes_system=rstab.results.settings.MEMBER_AXES_SYSTEM_PRINCIPAL_AXES_X_U_V,
    )
    print(f"\nMember Forces:\n{member_forces.data}")

    # Get result table
    member_forces_table: common.Table = rstab_app.get_result_table(
        table=rstab.results.ResultTable.STATIC_ANALYSIS_MEMBERS_INTERNAL_FORCES_TABLE,
        loading= rstab.ObjectId(
            no=1,
            object_type=rstab.OBJECT_TYPE_LOAD_CASE
        ),
        member_axes_system=rstab.results.settings.MEMBER_AXES_SYSTEM_PRINCIPAL_AXES_X_U_V,
    )
    print(f"\nMember Forces Table:\n{member_forces_table.data}")


