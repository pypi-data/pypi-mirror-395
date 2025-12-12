from util import assert_impute_response, assert_model_response

import alchemite_apiclient as client
from alchemite_apiclient.extensions import await_trained


def test_hyperopt(
    set_insecure_transport,
    api_datasets,
    api_models,
    adrenergic_dataset,
):
    dataset_id = adrenergic_dataset
    column_headers = api_datasets.datasets_id_get(dataset_id)["column_headers"]
    model_name = "adrenergic model"

    # Train the model with hyperparameter optimization
    model = client.Model(
        name=model_name,
        training_method="alchemite",
        training_dataset_id=dataset_id,
    )
    model_id = api_models.models_post(model=model)

    train_request = client.TrainRequest(
        hyperparameter_optimization="TPE",
        validation="5-fold",
        max_number_samples=5,
    )
    api_models.models_id_train_put(model_id, train_request=train_request)
    await_trained(lambda: api_models.models_id_get(model_id))

    model_response = api_models.models_id_get(model_id)
    assert_model_response(
        model_response,
        model_name,
        dataset_id,
        column_headers,
        hyperopt="TPE",
        validation="5-fold",
    )

    # Impute the training dataset and write the output to a file
    impute_request = client.ImputeRequest(
        dataset_id=dataset_id,
        return_row_headers=True,
        return_column_headers=True,
    )
    impute_response = api_models.models_id_impute_put(
        model_id, impute_request=impute_request
    )
    assert_impute_response(impute_response, column_headers, True)
