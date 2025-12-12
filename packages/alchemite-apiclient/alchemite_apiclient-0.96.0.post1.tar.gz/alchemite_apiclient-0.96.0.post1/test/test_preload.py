import os


def test_preload(set_insecure_transport, api_models, adrenergic_model, example_dir):
    model_id = adrenergic_model
    impute_input_file = os.path.join(example_dir, "adrenergic_row.csv")

    # Load model into memory
    load_request = {
        # If a loaded model is idle for 'timeout' seconds then it will unload itself
        "timeout": 600
    }
    api_models.models_id_load_post(model_id, load_request=load_request)
    # This impute response will block until the model is loaded
    impute_request = {
        "return_probability_distribution": False,
        "return_column_headers": True,
        "data": open(impute_input_file).read(),
    }
    api_models.models_id_impute_put(model_id, impute_request=impute_request)

    model_loaded = api_models.models_id_get(model_id).loaded
    assert model_loaded
    api_models.models_id_impute_put(model_id, impute_request=impute_request)

    # Manually unload model and impute again
    api_models.models_id_unload_put(model_id)
    model_loaded = api_models.models_id_get(model_id).loaded
    assert not model_loaded
    api_models.models_id_impute_put(model_id, impute_request=impute_request)
