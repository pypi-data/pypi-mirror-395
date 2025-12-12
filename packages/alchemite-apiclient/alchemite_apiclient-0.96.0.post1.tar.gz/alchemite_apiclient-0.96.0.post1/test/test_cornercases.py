import csv

import alchemite_apiclient as client
from alchemite_apiclient.extensions import await_trained, row_chunks


def test_utf8(data_dir, api_default, api_models, api_datasets):
    dataset_file = data_dir("unicode.csv")

    dataset_name = "steels"
    model_name = "steels"

    ############################################################################
    ### Upload the dataset in chunks
    ############################################################################
    # Call POST /datasets to create the dataset record but don't pass it the
    # 'data' argument.  We'll upload the data later.
    with open(dataset_file, "r", encoding="UTF-8") as file:
        reader = csv.reader(file, delimiter=",")
        column_headers = next(reader)[1:]
        for row_index, _ in enumerate(reader):
            pass
        row_count = row_index + 1

    # The number of rows to upload at once
    chunk_size = 500
    descriptor_columns = [0] * len(column_headers)

    dataset = client.Dataset(
        name=dataset_name,
        row_count=row_count,
        column_headers=column_headers,
        descriptor_columns=descriptor_columns,
        complete_columns=descriptor_columns,
    )

    dataset_id = api_datasets.datasets_post(dataset=dataset)
    print("Created dataset record:", dataset_id)
    print("--- dataset metadata before upload ---")
    print(api_datasets.datasets_id_get(dataset_id))

    # Upload the data in chunks of rows at a time
    for chunk_number, chunk in enumerate(row_chunks(dataset_file, chunk_size)):
        response = api_datasets.datasets_id_chunks_chunk_number_put(
            dataset_id, chunk_number, body=chunk
        )
        print("Uploaded chunk", chunk_number)

    # Show all the chunks
    response = api_datasets.datasets_id_chunks_get(dataset_id)
    print("Chunks:", response)

    # Say that we've finished uploading the dataset
    api_datasets.datasets_id_uploaded_post(dataset_id)
    print("Uploaded dataset")
    print("--- dataset metadata after upload ---")
    print(api_datasets.datasets_id_get(dataset_id))

    # Get the metadata about this dataset
    dataset_metadata = api_datasets.datasets_id_get(dataset_id)
    print("--- dataset metadata ---")
    print(dataset_metadata)