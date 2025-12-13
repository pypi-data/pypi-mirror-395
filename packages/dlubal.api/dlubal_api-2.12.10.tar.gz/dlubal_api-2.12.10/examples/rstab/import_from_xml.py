import os
from dlubal.api import rstab, common

# Connect to the RSTAB application
with rstab.Application() as rstab_app:

    # Reset RSTAB by closing models, creating a new one, and clearing all objects
    rstab_app.close_all_models(save_changes=False)
    rstab_app.create_model(name='xml_structure')
    rstab_app.delete_all_objects()

    # Step 1: Import IFC model from the file
    xml_path = os.path.join(os.path.dirname(__file__), 'src', 'xml_structure.xml')

    rstab_app.import_from(
        filepath=xml_path,
        import_attributes=common.import_export.XmlImportAttributes()
    )

    # Step 2: Get object ID list
    object_id_list = rstab_app.get_object_id_list()

    # Iterate through object IDs and print their types and IDs
    for obj in object_id_list.object_id:

        object_id = obj.no
        object_type = obj.object_type

        print(f"{rstab.ObjectType.Name(object_type)}: {object_id}")