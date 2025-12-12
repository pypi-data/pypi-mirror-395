import csv
import os
from io import StringIO

from util import (
    assert_dataset_response,
    assert_impute_response,
    assert_model_response,
)

from alchemite_apiclient.extensions import await_trained


def test_basic(set_insecure_transport, api_models, api_datasets, example_dir):
    # Provide path to the dataset to train a model from
    steels_dataset_path = os.path.join(example_dir, "steels.csv")
    impute_input_path = os.path.join(example_dir, "steels_impute.csv")

    # Define names for the dataset and model
    dataset_name = "steels"
    model_name = "steels"

    # Upload a dataset with POST /datasets
    with open(steels_dataset_path, "r", encoding="UTF-8") as file:
        data = file.read()
        reader = csv.reader(StringIO(data), delimiter=",")
        rows = [row for row in reader]
        row_count = len(rows) - 1
        column_headers = rows[0][1:]
    descriptor_columns = [0] * len(column_headers)

    dataset = {
        "name": dataset_name,
        "row_count": row_count,
        "column_headers": column_headers,
        "descriptor_columns": descriptor_columns,
        "data": data,
    }
    dataset_id = api_datasets.datasets_post(dataset=dataset)

    # Get the metadata about this dataset
    dataset_response = api_datasets.datasets_id_get(dataset_id)

    assert_dataset_response(
        dataset_response, dataset_name, column_headers, row_count
    )

    # Train a basic model without validaiton or hyperparameter optimization
    model = {
        "name": model_name,
        "training_method": "alchemite",
        "training_dataset_id": dataset_id,
    }
    model_id = api_models.models_post(model=model)

    # Start training the model using default hyperparameters and no validation
    api_models.models_id_train_put(model_id, train_request={})

    # Wait until the model has finished training
    await_trained(lambda: api_models.models_id_get(model_id))

    # Get the model metadata
    model_response = api_models.models_id_get(model_id)

    assert_model_response(
        model_response, model_name, dataset_id, column_headers
    )

    # Use the model to predict some missing values from a dataset
    with open(impute_input_path, "r", encoding="UTF-8") as file:
        impute_data = file.read()

    impute_request = {
        "return_probability_distribution": False,
        "return_column_headers": True,
        "data": impute_data,
    }
    impute_response = api_models.models_id_impute_put(
        model_id, impute_request=impute_request
    )

    assert_impute_response(impute_response, column_headers)
