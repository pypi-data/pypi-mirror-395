import os
from dlubal.api import rfem, common


# Connect to the RFEM application
with rfem.Application() as rfem_app:

    rfem_app.create_model(name='import_from_ifc')

    # Step 1: Import IFC model from the file
    ifc_file_path = os.path.join(os.path.dirname(__file__), 'src', 'ifc_structure.ifc')

    rfem_app.import_from(
        filepath=ifc_file_path,
        import_attributes=common.import_export.IfcImportAttributes()
    )

    # Step 2: Edit IFC model (e.g., mirror it along the Z-axis)
    ifc_model: rfem.ifc_objects.IfcFileModelObject = rfem_app.get_object(
        rfem.ifc_objects.IfcFileModelObject(no=1)
    )
    ifc_model.mirror_axis_z=True
    rfem_app.update_object(ifc_model)


    # Step 3: Categorize IFC model objects for conversion
    ifc_object_list = rfem_app.get_object_list(
        objs=[
            rfem.ifc_objects.IfcModelObject()
        ]
    )

    members, surfaces, solids = [], [], []

    for ifc_object in ifc_object_list:
        ifc_type = ifc_object.ifc_type
        if ifc_type in ["IfcColumn", "IfcBeam"]:
            members.append(ifc_object)
        elif ifc_type in ["IfcWallStandardCase", "IfcSlab",]:
            surfaces.append(ifc_object)
        elif ifc_type in ["IfcFooting"]:
            solids.append(ifc_object)

    # Step 4: Convert IFC model objects to appropriate RFEM model objects
    # Convert columns and beams to RFEM straight members
    rfem_app.convert_objects(
        convert_into=common.ConvertObjectInto.CONVERT_IFC_OBJECT_INTO_STRAIGHT_MEMBER,
        objs=members
    )
    # Convert walls and slabs to RFEM surfaces
    rfem_app.convert_objects(
        convert_into=common.ConvertObjectInto.CONVERT_IFC_OBJECT_INTO_SURFACE,
        objs=surfaces
    )
    # Convert footings to RFEM solids
    rfem_app.convert_objects(
        convert_into=common.ConvertObjectInto.CONVERT_IFC_OBJECT_INTO_SOLID,
        objs=solids
    )

