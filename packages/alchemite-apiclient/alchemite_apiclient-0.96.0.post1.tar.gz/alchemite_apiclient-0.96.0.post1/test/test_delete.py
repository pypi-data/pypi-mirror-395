import csv
import os
from io import StringIO


def test_delete(set_insecure_transport, api_datasets, api_models, example_dir):
    # Provide path to the dataset to train a model from
    steels_dataset_path = os.path.join(example_dir, "steels.csv")

    # Upload a dataset with POST /datasets
    with open(steels_dataset_path, "r", encoding="UTF-8") as file:
        data = file.read()
        reader = csv.reader(StringIO(data), delimiter=",")
        rows = [row for row in reader]
        row_count = len(rows) - 1
        column_headers = rows[0][1:]
    descriptor_columns = [0] * len(column_headers)

    dataset = {
        "name": "test_dataset",
        "row_count": row_count,
        "column_headers": column_headers,
        "descriptor_columns": descriptor_columns,
        "data": data,
    }
    dataset_id_to_delete = api_datasets.datasets_post(dataset=dataset)

    # Train a basic model without validaiton or hyperparameter optimization
    model = {
        "name": "test_model",
        "training_method": "alchemite",
        "training_dataset_id": dataset_id_to_delete,
    }
    model_id_to_delete = api_models.models_post(model=model)

    for model in api_models.models_get():
        if model.id == model_id_to_delete:
            api_models.models_id_delete(model.id)

    # Datasets can also be deleted in a similar way
    for dataset in api_datasets.datasets_get():
        if dataset.id == dataset_id_to_delete:
            api_datasets.datasets_id_delete(dataset.id)
