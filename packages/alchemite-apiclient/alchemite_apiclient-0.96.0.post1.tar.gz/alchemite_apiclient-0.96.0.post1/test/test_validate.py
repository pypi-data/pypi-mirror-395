import os


def test_validate(
    set_insecure_transport, api_models, adrenergic_model_validated, example_dir
):
    model_id = adrenergic_model_validated
    col_count = len(
        api_models.models_id_get(model_id)["training_column_headers"]
    )

    holdout_dataset_file = os.path.join(example_dir, "adrenergic_holdout.csv")

    # Use the model to re-predict values in a holdout set
    with open(holdout_dataset_file, encoding="UTF-8") as f:
        holdout_data = f.read()

    analyse_validate_response = api_models.models_id_analyse_validate_put(
        model_id,
        analyse_validate_request={
            "data": holdout_data,
            "return_predictions": True,
        },
    )
    assert "predictions" in analyse_validate_response
    assert len(analyse_validate_response["column_analytics"]) == col_count
