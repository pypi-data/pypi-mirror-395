from dlubal.api import rfem
import pandas, os

with rfem.Application() as rfem_app:

    # --- Pre-processing results by Filters ---

    # Add optional filters to limit the amount of data retrieved from the database.
    # Currently, filters can only be applied to 'object_no' and/or 'loading'!
    filters=[
        rfem.results.ResultsFilter(column_id='member_no', filter_expression='1,3,6'),
        rfem.results.ResultsFilter(column_id='loading', filter_expression='LC1, CO1'),
    ]

     # Retrieve filtered results as a Pandas DataFrame (.data)
    results: pandas.DataFrame  = rfem_app.get_results(
        results_type=rfem.results.ResultsType.STATIC_ANALYSIS_MEMBERS_INTERNAL_FORCES,
        filters=filters
    ).data
    print(f"\nResults Pre-processed (Filters):\n{results}")


    # --- Post-processing results by Pandas DataFrame  ---

    # Once the relevant data has been filtered, we can further process and analyze it using the Pandas DataFrame.
    # Pandas provides powerful tools to manipulate and analyze data in an efficient and flexible manner.

    # Retrieve the entire row that corresponds to this minimum 'n' value
    row_n_min = results.loc[results['n'].idxmin()]
    print(f"\nResults Post-processed (Pandas):\n{row_n_min}")

    # Find the minimum value of the 'n' column
    n_min = results['n'].min()
    print("n_min:", n_min)


    # # --- Export the results to a CSV file ---

    # Save the Pandas dataframe to a CSV file in the current working directory.
    file_path = os.path.abspath('./results.csv')
    results.to_csv(path_or_buf=file_path)
    print(f"\nResults Exported:\n{file_path}")

