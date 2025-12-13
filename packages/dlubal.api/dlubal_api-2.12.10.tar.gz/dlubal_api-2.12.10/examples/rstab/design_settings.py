from dlubal.api import rstab, common

# Connect to the rstab application
with rstab.Application() as rstab_app:

    # Step 1: Retrieve the global settings tree table for Steel Design (active model)
    design_settings: rstab.GlobalSettingsTreeTable = rstab_app.get_design_settings(
        addon=rstab.DesignAddons.STEEL_DESIGN
    )
    print(f"DESIGN SETTINGS:\n{design_settings}")

    # Step 2: Retrieve a specific value
    # Path to access the member slenderness setting
    member_slendernesses_path = [
        'member_slendernesses',
        'member_slendernesses_tension_ec3'
    ]
    # Fetch the value of the specific setting
    member_slendernesses_val = common.get_tree_value(
        tree=design_settings,
        path=member_slendernesses_path
    )
    print(f"\nMember slendernesses: {member_slendernesses_val}")

    # Step 3: Modify the value and save the updated design settings
    # Set a new value
    common.set_tree_value(
        tree=design_settings,
        path=member_slendernesses_path,
        value=250,
    )
    # Apply the updated design settings to the model
    rstab_app.set_design_settings(
        addon=rstab.DesignAddons.STEEL_DESIGN,
        global_settings_tree_table=design_settings
    )

