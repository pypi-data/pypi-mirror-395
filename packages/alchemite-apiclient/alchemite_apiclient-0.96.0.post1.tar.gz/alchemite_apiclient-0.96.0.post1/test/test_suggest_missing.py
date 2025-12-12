def test_suggest_missing(
    set_insecure_transport,
    api_models,
    steels_model,
):
    model_id = steels_model
    dataset_id = api_models.models_id_get(model_id)["training_dataset_id"]

    # Make a suggest missing request
    suggest_missing_response = api_models.models_id_suggest_missing_put(
        model_id, {"datasetID": dataset_id}
    )
    for result in suggest_missing_response:
        assert "column_header" in result
        assert "row_header" in result
