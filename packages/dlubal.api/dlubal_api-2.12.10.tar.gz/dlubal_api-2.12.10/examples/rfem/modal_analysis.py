from dlubal.api import rfem, common
from math import inf


def initialize_model():

    # Create new empty model
    rfem_app.close_all_models(save_changes=False)
    rfem_app.create_model(name="Modal Analysis")

    # Set global model settings:
    base_data: rfem.BaseData = rfem_app.get_base_data()

    # Activate add-ons
    base_data.addons.modal_analysis_active = True
    # Set standard
    base_data.standards.dynamic_analysis_standard = rfem.BaseData.Standards.DYNAMIC_ANALYSIS_NATIONAL_ANNEX_AND_EDITION_EN_1998_1_DIN_2023_11_STANDARD
    # Adjust general settings
    base_data.general_settings.gravitational_acceleration = 9.81

    # Activate combination wizard
    base_data.combinations_settings.combination_wizard_active = True

    rfem_app.set_base_data(base_data=base_data)
    rfem_app.delete_all_objects()


def create_structure():

    structure = [

            # Material
            rfem.structure_core.Material(
                no=1,
                name="S235 | EN 1993-1-1:2005-05",
            ),

            # Section
            rfem.structure_core.Section(
                no=1,
                name="IPE 550 | DIN 1025-5:1994-03 | Ferona",
                material=1,
            ),

            # Nodes
            rfem.structure_core.Node(
                no=1,
                coordinate_2=-2,
            ),
            rfem.structure_core.Node(
                no=2,
                coordinate_2=-2,
                coordinate_3=-4,
            ),

            # Line
            rfem.structure_core.Line(
                no=1,
                definition_nodes=[1, 2],
            ),

            # Member
            rfem.structure_core.Member(
                no=1,
                line=1,
                section_start=1,
            ),

            # Support
            rfem.types_for_nodes.NodalSupport(
                no=1,
                user_defined_name_enabled=True,
                name="Fixed",
                nodes=[1],
                spring=common.Vector3d(x=inf, y=inf, z=inf),
                rotational_restraint=common.Vector3d(x=inf, y=inf, z=inf),
            )
    ]

    rfem_app.create_object_list(structure)


def create_loading():

    loading = [
        # Load Case | LC1
        rfem.loading.LoadCase(
            no=1,
            name="Static | Self-weight",
            static_analysis_settings=1,
        ),
        # Nodal Loads | LC1
        rfem.loads.NodalLoad(   # Force
            no=1,
            nodes=[2],
            force_magnitude=1000,
            load_direction=rfem.loads.NodalLoad.LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W_TRUE_LENGTH,
            load_case=1,
        ),
        rfem.loads.NodalLoad(   # Mass
            no=2,
            load_type=rfem.loads.NodalLoad.LOAD_TYPE_MASS,
            nodes=[2],
            individual_mass_components=True,
            mass=common.Vector3d(x=100, y=100, z=100),
            mass_moment_of_inertia=common.Vector3d(x=100, y=100, z=100),
            load_case=1,
        ),

        # Static Analysis Settings
        rfem.loading.StaticAnalysisSettings(
            no=1,
            analysis_type=rfem.loading.StaticAnalysisSettings.ANALYSIS_TYPE_SECOND_ORDER_P_DELTA,
            mass_conversion_enabled=True,
        ),

        # --- Combinatoric for Seismic Mass ---

        # Combination Wizard
        rfem.loading.CombinationWizard(
            no=1,
            static_analysis_settings=1,
            consider_imperfection_case=True,
        ),

        # Design Situations
        rfem.loading.DesignSituation(
            no=1,
            name="Seismic/Mass Combination - psi-E,i",
            design_situation_type=rfem.loading.DesignSituation.DESIGN_SITUATION_TYPE_SEISMIC_MASS,
            combination_wizard=1,
        ),
    ]

    rfem_app.create_object_list(loading)


def define_modal_analysis_cases():

    modal_analysis = [

        # Modal Analysis Settings
        rfem.loading.ModalAnalysisSettings(
            no=1,
            name='User-defined | Mode=2',
            user_defined_name_enabled=True,
            acting_masses_about_axis_x_enabled=False,
            acting_masses_about_axis_y_enabled=False,
            acting_masses_about_axis_z_enabled=False,
            acting_masses_in_direction_z_enabled=False,
            activate_minimum_initial_prestress=True,
            solution_method=rfem.loading.ModalAnalysisSettings.SOLUTION_METHOD_ROOT_OF_CHARACTERISTIC_POLYNOMIAL,
            number_of_modes=2,
        ),
        rfem.loading.ModalAnalysisSettings(
            no=2,
            name='Automated | Mass=95%',
            user_defined_name_enabled=True,
            acting_masses_about_axis_x_enabled=False,
            acting_masses_about_axis_y_enabled=False,
            acting_masses_about_axis_z_enabled=False,
            acting_masses_in_direction_z_enabled=False,
            activate_minimum_initial_prestress=True,
            solution_method=rfem.loading.ModalAnalysisSettings.SOLUTION_METHOD_ROOT_OF_CHARACTERISTIC_POLYNOMIAL,
            number_of_modes_method=rfem.loading.ModalAnalysisSettings.NUMBER_OF_MODES_METHOD_EFFECTIVE_MASS_FACTORS,
            effective_modal_mass_factor=0.95
        ),

        # Modal Load Cases
        rfem.loading.LoadCase(
            no=2,
            analysis_type=rfem.loading.LoadCase.ANALYSIS_TYPE_MODAL_ANALYSIS,
            name="Modal | Self-mass",
            modal_analysis_settings=1,
        ),
        rfem.loading.LoadCase(
            no=3,
            analysis_type=rfem.loading.LoadCase.ANALYSIS_TYPE_MODAL_ANALYSIS,
            name="Modal | Mass=95%",
            modal_analysis_settings=2,
        ),
    ]

    rfem_app.create_object_list(modal_analysis)


def import_masses_to_cases():

    rfem_app.generate_combinations()

    object_list = rfem_app.get_object_list(
        objs=[
            rfem.loading.LoadCase()
        ]
    )

    for obj in object_list:

        lc: rfem.loading.LoadCase = obj

        if lc.analysis_type is rfem.loading.LoadCase.ANALYSIS_TYPE_MODAL_ANALYSIS:

            lc.import_masses_from.no = 1
            lc.import_masses_from.object_type = rfem.ObjectType.OBJECT_TYPE_LOAD_COMBINATION

    rfem_app.update_object_list(object_list)


def get_effective_modal_masses():

    rfem_app.calculate_all(skip_warnings=True)

    results = rfem_app.get_results(
        results_type=rfem.results.ResultsType.MODAL_ANALYSIS_EFFECTIVE_MODAL_MASSES
    )
    print(f"\nEffective Modal Masses:\n{results.data}")





with rfem.Application() as rfem_app:

    # Modal Analysis Procedure

    initialize_model()              # Activate add-on, ...

    create_structure()              # Column IPE 550 (fixed)
    create_loading()                # Force + Mass

    define_modal_analysis_cases()   # Self-mass (Mode=2) | Mass=95% (Mode=auto)
    import_masses_to_cases()        # Import masses from generated combination

    get_effective_modal_masses()    # Calculation + reading results









