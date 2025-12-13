from dlubal.api import rfem

with rfem.Application() as rfem_app:

    # Step 1: Retrieve the Base data (active model)
    base_data: rfem.BaseData  = rfem_app.get_base_data()
    print(f"BASE DATA:\n{base_data}")

    # Step 2: Modify the values in Base data object
    # Main model data
    base_data.main.model_description = "model_type_2D"
    base_data.main.comment = "test version"
    base_data.main.model_type = rfem.BaseData.Main.MODEL_TYPE_2D_XZ_PLANE_STRESS
    base_data.main.surfaces_active = False
    # Add-ons activation
    base_data.addons.steel_design_active = True
    base_data.addons.load_wizards_active = True
    base_data.addons.combination_wizard_and_classification_active = True
    # Standards assignment
    base_data.standards.load_wizard_standard_group = rfem.BaseData.Standards.LOAD_WIZARD_STANDARD_GROUP_EN_1991_STANDARD_GROUP
    base_data.standards.load_wizard_standard = rfem.BaseData.Standards.LOAD_WIZARD_NATIONAL_ANNEX_AND_EDITION_EN_1991_DIN_2019_04_STANDARD
    base_data.standards.combination_wizard_standard = rfem.BaseData.Standards.COMBINATION_WIZARD_NATIONAL_ANNEX_AND_EDITION_EN_1990_DIN_2012_08_STANDARD
    base_data.standards.steel_design_standard = rfem.BaseData.Standards.STEEL_DESIGN_NATIONAL_ANNEX_AND_EDITION_EN_1993_DIN_2020_11_STANDARD

    # Step 3: Apply the updated Base data to the model
    rfem_app.set_base_data(base_data=base_data)
