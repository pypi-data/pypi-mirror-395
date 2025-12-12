import os

from util import (
    assert_custom_validation_splits_response,
    assert_impute_response,
    assert_model_response,
)

import alchemite_apiclient as client
from alchemite_apiclient.extensions import await_trained


def test_custom_validation_splits(
    set_insecure_transport,
    api_datasets,
    api_models,
    example_dir,
    steels_dataset,
):
    dataset_id = steels_dataset
    column_headers = api_datasets.datasets_id_get(dataset_id)["column_headers"]
    model_name = "steels"
    impute_input_path = os.path.join(example_dir, "steels_impute.csv")

    # Train the model with hyperparameter optimization
    model = client.Model(
        name=model_name,
        training_method="alchemite",
        training_dataset_id=dataset_id,
    )
    model_id = api_models.models_post(model=model)

    # Train the optimial model for this dataset
    train_request = {
        "hyperparameterOptimization": "TPE",
        "validation": "custom",
        "validationSplits": [
            {
                "name": "Carbon Splits 1",
                "trainRowIDs": [
                    "Carbon steel 1",
                    "Carbon steel 2",
                    "Carbon steel 3",
                ],
                "testRowIDs": [
                    "Carbon steel 4",
                    "Carbon steel 5",
                    "Carbon steel 6",
                ],
            },
            {
                "name": "Carbon Splits 2",
                "trainRowIDs": [
                    "Carbon steel 4",
                    "Carbon steel 5",
                    "Carbon steel 6",
                ],
                "testRowIDs": [
                    "Carbon steel 1",
                    "Carbon steel 2",
                    "Carbon steel 3",
                ],
            },
            {
                "name": "Low Alloy Steel Splits 1",
                "trainRowIDs": [
                    "Low alloy steel 1",
                    "Low alloy steel 2",
                    "Low alloy steel 3",
                ],
                "testRowIDs": [
                    "Low alloy steel 4",
                    "Low alloy steel 5",
                    "Low alloy steel 6",
                ],
            },
            {
                "name": "Low Alloy Steel Splits 2",
                "trainRowIDs": [
                    "Low alloy steel 4",
                    "Low alloy steel 5",
                    "Low alloy steel 6",
                ],
                "testRowIDs": [
                    "Low alloy steel 1",
                    "Low alloy steel 2",
                    "Low alloy steel 3",
                ],
            },
        ],
    }

    api_models.models_id_train_put(model_id, train_request=train_request)
    await_trained(lambda: api_models.models_id_get(model_id))

    # Get the model metadata
    model_response = api_models.models_id_get(model_id)
    assert_model_response(
        model_response,
        model_name,
        dataset_id,
        column_headers,
        hyperopt="TPE",
        validation="custom",
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

    # Fetch the custom validation splits for the model
    custom_validation_splits_response = (
        api_models.models_id_validation_splits_get(model_id)
    )
    assert_custom_validation_splits_response(custom_validation_splits_response)
