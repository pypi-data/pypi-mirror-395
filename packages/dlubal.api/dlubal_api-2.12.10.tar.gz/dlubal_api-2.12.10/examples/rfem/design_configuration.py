from dlubal.api import rfem, common
import google.protobuf.json_format as pbjson

# Connect to the RFEM application
with rfem.Application() as rfem_app:

    # --- Steel Design | ULS Configuration ---

    # Retrieve Design ULS Configuration TreeTable
    steel_uls_config: rfem.steel_design_objects.SteelDesignUlsConfiguration = rfem_app.get_object(
        obj=rfem.steel_design_objects.SteelDesignUlsConfiguration(no=1)
    )
    settings_ec3_uls = steel_uls_config.settings_ec3
    print(f"\nSETTINGS_EC3_ULS:\n{settings_ec3_uls}")

    # Retrieve a specific value from the configuration
    # Path to the specific value
    elastic_design_path=[
        "options",
        "options_elastic_design_root",
        "options_elastic_design"
    ]
    # Get specific value
    elastic_design_val = common.get_tree_value(
        tree=settings_ec3_uls,
        path=elastic_design_path
    )
    print(f"\nElastic Design: {elastic_design_val}")

    # Modify the value
    # Create empty TreeTable and set only the values that we want to change
    settings_ec3_uls_updated = rfem.steel_design_objects.SteelDesignUlsConfiguration.SettingsEc3TreeTable()
    common.set_tree_value(
        tree=settings_ec3_uls_updated,
        path=elastic_design_path,
        value=True
    )

    # Apply the updated configuration to the model
    rfem_app.update_object(
        obj=rfem.steel_design_objects.SteelDesignUlsConfiguration(
            no=1,
            settings_ec3=settings_ec3_uls_updated
        )
    )


    # --- Steel Design | SLS Configuration ---

    # Retrieve Design SLS Configuration TreeTable
    steel_sls_config: rfem.steel_design_objects.SteelDesignSlsConfiguration = rfem_app.get_object(
        obj=rfem.steel_design_objects.SteelDesignSlsConfiguration(no=1)
    )
    settings_ec3_sls = steel_sls_config.settings_ec3
    print(f"\nSETTINGS_EC3_SLS:\n{settings_ec3_sls}")

    # Retrieve a specific value from the configuration
    # Path to the specific value
    beam_rel_deflection_limit_path=[
        "serviceability_limits",
        "sl_check_limit_characteristic",
        "sl_check_deformation_z_or_resulting_axis_characteristic",
        "l_", # Beam | Relative limit
    ]
    # Get specific value
    beam_rel_deflection_limit_val = common.get_tree_value(
        tree=settings_ec3_sls,
        path=beam_rel_deflection_limit_path
    )
    print(f"\nBeam | Relative deflection limit: L/{beam_rel_deflection_limit_val}")

    # Modify the value
    # Create empty TreeTable and set only the values that we want to change
    settings_ec3_sls_updated =rfem.steel_design_objects.SteelDesignSlsConfiguration.SettingsEc3TreeTable()
    common.set_tree_value(
        tree=settings_ec3_sls_updated,
        path=beam_rel_deflection_limit_path,
        value=250
    )

    # Apply the updated configuration to the model
    rfem_app.update_object(
        obj=rfem.steel_design_objects.SteelDesignSlsConfiguration(
            no=1,
            settings_ec3=settings_ec3_sls_updated
        )
    )
