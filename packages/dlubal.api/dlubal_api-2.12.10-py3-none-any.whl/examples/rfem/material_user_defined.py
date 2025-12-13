from dlubal.api import rfem
from dlubal.api import common

# Connect to the RFEM application
with rfem.Application() as rfem_app:

    # Retrieve a specific material (ID = 2) from the active model
    material:rfem.structure_core.Material = rfem_app.get_object(
        rfem.structure_core.Material(no=2)  # Concrete material
    )

    # --- Update Material Properties ---

    # Print material values for all temperatures (=rows)
    for material_values in material.material_values.rows:
        print(material_values)

    # Define paths for material properties to be updated
    fck_path = ['strengths', 'f_ck']
    ecm_path = ['moduli', 'e_cm']

    # Create an empty MaterialValuesTreeTable and set the desired material property values
    material_values_tree = rfem.structure_core.Material.MaterialValuesRow.MaterialValuesTreeTable()
    common.set_tree_value(material_values_tree, fck_path, 28000000.0)
    common.set_tree_value(material_values_tree, ecm_path, 25000000000.0)

   # Copy the updated material values to the first temperature row of the material's values table.
    material.material_values.rows[0].material_values_tree.CopyFrom(material_values_tree)

    # --- Update Standard Parameters ---

    # Print material values for all temperature rows
    standard_params = material.standard_parameters
    print(standard_params)

    # Define paths for material properties to be updated
    gamma_c_path = ['2_basis_of_design', '2_4_2_4_partial_factors_for_materials', 'gamma_c']

    # Create an empty MaterialValuesTreeTable and set the desired material property values
    standard_params_tree = rfem.structure_core.Material.StandardParametersTreeTable()
    common.set_tree_value(standard_params_tree, gamma_c_path, 1.35)


    # --- Apply modified Material back to the model ---
    rfem_app.update_object(
        obj=rfem.structure_core.Material(
            no=2,
            user_defined=True,
            material_values=material.material_values, # material values
            standard_parameters=standard_params_tree  # standard parameters
        )
    )