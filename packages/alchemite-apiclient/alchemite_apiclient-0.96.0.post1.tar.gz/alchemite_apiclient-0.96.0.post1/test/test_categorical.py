import csv
import os
from io import StringIO

from util import assert_dataset_response, assert_model_response

from alchemite_apiclient.extensions import await_trained


def test_categorical(
    set_insecure_transport, api_models, api_datasets, example_dir
):
    # Provide path to the dataset to train a model from
    categorical_dataset_path = os.path.join(example_dir, "categorical.csv")

    # Define names for the dataset and model
    dataset_name = "categorical"
    model_name = "categorical"
    categorical_columns = [
        {
            "name": "t",
            "values": [
                "red",
                "orange",
                "yellow",
                "green",
                "blue",
                "indigo",
                "violet",
            ],
        }
    ]

    # Upload a dataset with POST /datasets
    with open(categorical_dataset_path, "r", encoding="UTF-8") as file:
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
        "categorical_columns": categorical_columns,
    }
    dataset_id = api_datasets.datasets_post(dataset=dataset)

    # Get the metadata about this dataset
    dataset_response = api_datasets.datasets_id_get(dataset_id)

    assert_dataset_response(
        dataset_response,
        dataset_name,
        column_headers,
        row_count,
        categorical_columns,
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
        model_response,
        model_name,
        dataset_id,
        column_headers,
        categorical_columns=categorical_columns,
    )
