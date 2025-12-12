from util import assert_importance_response


def test_importance(
    set_insecure_transport,
    api_datasets,
    api_models,
    steels_model_descriptors,
):
    model_id = steels_model_descriptors
    model_response = api_models.models_id_get(model_id)
    column_headers = model_response["training_column_headers"]
    dataset_id = model_response["training_dataset_id"]
    dataset_descriptors = api_datasets.datasets_id_get(dataset_id)[
        "descriptor_columns"
    ]
    descriptor_column_headers = [
        col
        for i, col in enumerate(column_headers)
        if dataset_descriptors[i] == 1
    ]

    importance_request = {"useOnlyDescriptors": True}
    importance_response = api_models.models_id_importance_put(
        model_id, importance_request=importance_request, _preload_content=False
    )

    assert_importance_response(
        importance_response, column_headers, descriptor_column_headers
    )
