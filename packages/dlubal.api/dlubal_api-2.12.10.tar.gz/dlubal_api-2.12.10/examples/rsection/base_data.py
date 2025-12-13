from dlubal.api import rsection

with rsection.Application() as rsection_app:

    # Step 1: Retrieve the Base data (active model)
    base_data: rsection.BaseData  = rsection_app.get_base_data()
    print(f"BASE DATA:\n{base_data}")

    # Step 2: Modify the values in Base data object
    # Main model data
    base_data.main.model_description = "cold_formed"
    base_data.main.comment = "thin_walled"
    base_data.main.analysis_method = rsection.BaseData.Main.ANALYSIS_METHOD_THIN_WALLED
    # Add-ons activation
    base_data.addons.has_effective_section_properties_active = True
    # Standards assignment
    base_data.standards.effective_section_standard = rsection.BaseData.Standards.EFFECTIVE_SECTION_STANDARD_EN_1993_1_3_COLD_FORMED

    # Step 3: Apply the updated Base data to the model
    rsection_app.set_base_data(base_data=base_data)