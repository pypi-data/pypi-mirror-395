import time

import pandas as pd


def test_query(
    set_insecure_transport,
    api_default,
    api_datasets,
    adrenergic_dataset,
):
    dataset_id = adrenergic_dataset
    limit = 20

    # Wait for dataset to exit processing and enter uploaded
    i = 0
    dataset_response = api_datasets.datasets_id_get(dataset_id)
    while dataset_response["status"] != "uploaded":
        time.sleep(1)
        dataset_response = api_datasets.datasets_id_get(dataset_id)
        i += 1
        if i > 60:
            assert False

    # Query dataset
    query_result = api_default.query_v1_put(
        query_request={
            "type": "dataset",
            "id": dataset_id,
            "filters": {
                # Get rows from the dataset where the column LM has no value
                "LM": None,
                # AND where the column D is equal to 0
                "D": 0,
                # AND where the column A is <= 3
                "A": {"max": 3},
                # AND where the column B is > 300
                "B": {"min": 300, "inclusiveMin": False},
            },
            # Only return a subset of the columns in the dataset. An "exclude"
            # option is also available if we wanted to return all column in the
            # dataset except certain ones
            "columnSelection": {
                "include": ["A", "B", "C", "D", "E", "F", "LM"]
            },
            # sort by column E in descending order, then A in ascending
            "sort": [
                {"name": "E", "direction": "desc"},
                {"name": "A", "direction": "asc"},
            ],
        },
        # Get only the results 10-30 from the above query (so skip the first 10
        # and limit the number of results returned to 20)
        offset=10,
        limit=limit,
    )

    # query_result is a dictionary
    assert len(query_result["result"]) == limit

    # Can convert query_result to a pandas DataFrame if needed
    query_df = pd.DataFrame(
        [
            {e["name"]: e["value"] for e in row.data}
            for row in query_result.result
        ],
        index=[row.row_id for row in query_result.result],
    )
    assert isinstance(query_df, pd.DataFrame)
