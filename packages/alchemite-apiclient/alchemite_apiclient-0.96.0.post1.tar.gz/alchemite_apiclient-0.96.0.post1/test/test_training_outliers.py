from util import assert_outliers_response


def test_training_outliers(
    set_insecure_transport,
    api_models,
    adrenergic_model_validated,
):
    model_id = adrenergic_model_validated

    # Get the training dataset outliers
    training_outliers_response = (
        api_models.models_id_training_dataset_outliers_put(
            model_id, _preload_content=False
        )
    )
    assert_outliers_response(
        training_outliers_response, additional_headers={"Row"}
    )
