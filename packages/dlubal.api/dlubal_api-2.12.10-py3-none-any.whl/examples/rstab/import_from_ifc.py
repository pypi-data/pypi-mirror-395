import os
from dlubal.api import rstab, common


# Connect to the RSTAB application
with rstab.Application() as rstab_app:

    rstab_app.create_model(name='import_from_ifc')

    # Step 1: Import IFC model from the file
    ifc_file_path = os.path.join(os.path.dirname(__file__), 'src', 'ifc_structure.ifc')

    rstab_app.import_from(
        filepath=ifc_file_path,
        import_attributes=common.import_export.IfcImportAttributes()
    )

    # Step 2: Edit IFC model (e.g., mirror it along the Z-axis)
    ifc_model: rstab.ifc_objects.IfcFileModelObject = rstab_app.get_object(
        rstab.ifc_objects.IfcFileModelObject(no=1)
    )
    ifc_model.mirror_axis_z=True
    rstab_app.update_object(ifc_model)


    # Step 3: Categorize IFC model objects for conversion
    ifc_object_list = rstab_app.get_object_list(
        objs=[
            rstab.ifc_objects.IfcModelObject()
        ]
    )

    members = []

    for ifc_object in ifc_object_list:
        ifc_type = ifc_object.ifc_type
        if ifc_type in ["IfcColumn", "IfcBeam"]:
            members.append(ifc_object)

    # Step 4: Convert IFC model objects to appropriate RSTAB model objects
    # Convert columns and beams to RSTAB straight members
    rstab_app.convert_objects(
        convert_into=common.ConvertObjectInto.CONVERT_IFC_OBJECT_INTO_STRAIGHT_MEMBER,
        objs=members
    )

