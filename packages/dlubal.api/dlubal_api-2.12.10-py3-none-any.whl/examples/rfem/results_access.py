from dlubal.api import rfem, common

with rfem.Application() as rfem_app:

    # --- get_results ---
    # Retrieves complete, unprocessed results from the RFEM database.
    # These results are returned wrapped in a DataFrame (.data).
    results:common.Table = rfem_app.get_results(
        results_type=rfem.results.ResultsType.STATIC_ANALYSIS_MEMBERS_INTERNAL_FORCES
    )
    print(f"\nResults:\n{results.data}")



    # --- get_result_table ---
    # Retrieves a pre-processed result table wrapped in a DataFrame (.data),
    # containing only the most relevant values as displayed in the RFEM desktop application.
    result_table:common.Table = rfem_app.get_result_table(
        table = rfem.results.ResultTable.STATIC_ANALYSIS_MEMBERS_INTERNAL_FORCES_TABLE,
        loading= rfem.ObjectId(
            no=1,
            object_type=rfem.OBJECT_TYPE_LOAD_COMBINATION
        )
    )
    print(f"\nResult Table:\n{result_table.data}")

    # --- has_results ---
    # Checks if results exist for a specified loading condition.
    # This is useful to confirm results availability before retrieving them,
    # preventing errors or unnecessary data requests.
    has_results = rfem_app.has_results(
        loading = rfem.ObjectId
        (
            no = 1,
            object_type = rfem.OBJECT_TYPE_LOAD_COMBINATION,
        )
    )
    print(f"\nResults Available: {has_results.value}")