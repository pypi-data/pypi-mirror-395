from util import assert_outliers_response


def test_outliers(set_insecure_transport, api_models, adrenergic_model):
    model_id = adrenergic_model
    dataset_id = api_models.models_id_get(model_id)["training_dataset_id"]

    outliers_request = {"dataset_id": dataset_id}

    outliers_response = api_models.models_id_outliers_put(
        model_id, outliers_request=outliers_request, _preload_content=False
    )
    assert_outliers_response(outliers_response)
