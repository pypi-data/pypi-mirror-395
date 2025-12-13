from dlubal.api import rfem

with rfem.Application() as rfem_app:

    mesh_settings: rfem.mesh.MeshSettings = rfem_app.get_mesh_settings()
    print(mesh_settings)


    mesh_stats_current = rfem_app.get_mesh_statistics()
    print(mesh_stats_current)


    mesh_settings.general_target_length_of_fe = 0.005
    rfem_app.set_mesh_settings(
        mesh_settings=mesh_settings
    )

    rfem_app.delete_mesh()

    rfem_app.generate_mesh(
        skip_warnings=True
    )

    mesh_stats_new = rfem_app.get_mesh_statistics()
    print(mesh_stats_new)