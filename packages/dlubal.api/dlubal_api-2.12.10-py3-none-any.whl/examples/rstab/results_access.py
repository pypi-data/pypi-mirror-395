from dlubal.api import rstab, common

with rstab.Application() as rstab_app:

    # --- get_results ---
    # Retrieves complete, unprocessed results from the RSTAB database.
    # These results are returned wrapped in a DataFrame (.Data).
    results:common.Table = rstab_app.get_results(
        results_type=rstab.results.ResultsType.STATIC_ANALYSIS_MEMBERS_INTERNAL_FORCES
    )
    print(f"\nResults:\n{results.data}")



    #--- get_result_table ---
    # Retrieves a pre-processed result table wrapped in a DataFrame (.Data),
    # containing only the most relevant values as displayed in the RSTAB desktop application.
    result_table:common.Table = rstab_app.get_result_table(
        table = rstab.results.ResultTable.STATIC_ANALYSIS_MEMBERS_INTERNAL_FORCES_TABLE,
        loading= rstab.ObjectId(
            no=1,
            object_type=rstab.OBJECT_TYPE_LOAD_COMBINATION
        )
    )
    print(f"\nResult Table:\n{result_table.data}")

    # --- has_results ---
    # Checks if results exist for a specified loading condition.
    # This is useful to confirm results availability before retrieving them,
    # preventing errors or unnecessary data requests.
    has_results = rstab_app.has_results(
        loading = rstab.ObjectId
        (
            no = 1,
            object_type = rstab.OBJECT_TYPE_LOAD_COMBINATION,
        )
    )
    print(f"\nResults Available: {has_results.value}")