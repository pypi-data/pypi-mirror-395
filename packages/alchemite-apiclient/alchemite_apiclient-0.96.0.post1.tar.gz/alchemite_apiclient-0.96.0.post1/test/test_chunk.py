import csv
import os

from util import assert_chunk_response, assert_dataset_response

from alchemite_apiclient.extensions import row_chunks


def test_chunk(set_insecure_transport, api_datasets, example_dir):
    # Provide path to the dataset to train a model from
    adrenergic_dataset_path = os.path.join(example_dir, "adrenergic.csv")
    chunk_size = 500

    # First 320 columns in this dataset are descriptor (input only) columns and are
    # complete columns in the training dataset as well as any future datasets we ask
    # the model to predict from.  The last 5 are normal columns
    descriptor_columns = [1] * 320 + [0] * 5
    complete_columns = descriptor_columns
    dataset_name = "chunked adrenergic"

    with open(adrenergic_dataset_path, "r", encoding="UTF-8") as file:
        reader = csv.reader(file, delimiter=",")
        column_headers = next(reader)[1:]
        for row_index, _ in enumerate(reader):
            pass
        row_count = row_index + 1

    dataset = {
        "name": dataset_name,
        "row_count": row_count,
        "column_headers": column_headers,
        "descriptor_columns": descriptor_columns,
        "complete_columns": complete_columns,
    }

    dataset_id = api_datasets.datasets_post(dataset=dataset)

    # Upload the data in chunks of rows at a time
    for chunk_number, chunk in enumerate(
        row_chunks(adrenergic_dataset_path, chunk_size)
    ):
        api_datasets.datasets_id_chunks_chunk_number_put(
            dataset_id, chunk_number, body=chunk
        )

    # Show all the chunks
    chunk_response = api_datasets.datasets_id_chunks_get(dataset_id)
    assert_chunk_response(chunk_response, len(column_headers), chunk_size)

    # Say that we've finished uploading the dataset
    api_datasets.datasets_id_uploaded_post(dataset_id)
    dataset_response = api_datasets.datasets_id_get(dataset_id)
    assert_dataset_response(
        dataset_response, dataset_name, column_headers, row_count
    )
