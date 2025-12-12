import json
import os

from util import assert_dimensionality_reduction_response

from alchemite_apiclient.extensions import await_job


def test_dimensionality_reduction(
    set_insecure_transport,
    api_models,
    api_datasets,
    steels_model,
    example_dir,
):
    model_id = steels_model
    dataset_id = api_models.models_id_get(model_id)["training_dataset_id"]

    optimize_args_path = os.path.join(example_dir, "optimize_args_steel.json")
    with open(optimize_args_path, encoding="UTF-8") as f:
        optimize_args = json.load(f)

    suggest_args_path = os.path.join(
        example_dir, "suggest_additional_args_steel.json"
    )
    with open(suggest_args_path, encoding="UTF-8") as f:
        suggest_additional_args = json.load(f)

    # Make an suggest additional request
    suggest_additional_job_id = api_models.models_id_suggest_additional_post(
        model_id, **suggest_additional_args
    )
    await_job(
        lambda: api_models.models_id_suggest_additional_job_id_get(
            model_id, job_id=suggest_additional_job_id
        )
    )

    # Make an optimize request
    optimize_job_id = api_models.models_id_optimize_post(
        model_id, **optimize_args
    )

    await_job(
        lambda: api_models.models_id_optimize_job_id_get(
            model_id, job_id=optimize_job_id
        )
    )

    # Reduce the dataset down to a visualisable amount of dimensions
    reduction_data_types = ["dataset", "optimize", "suggest-additional"]
    expected_results = [12, 1, 5]

    for reduction_data_type, expected_result in zip(
        reduction_data_types, expected_results
    ):
        # Build dimensionality reduction request
        dimensionality_reduction_request = {
            "reductionData": {
                "modelID": model_id,
                "reductionDataType": reduction_data_type,
                "columnType": "all columns",
            },
            "reductionMethod": {
                "method": "UMAP",
                "dimensions": 2,
                "numNeighbours": 5,
                "minimumDistance": 0.5,
            },
        }
        dimensionality_reduction_response = api_datasets.datasets_id_dimensionality_reduction_put(
            dataset_id,
            dimensionality_reduction_request=dimensionality_reduction_request,
        )
        assert_dimensionality_reduction_response(
            dimensionality_reduction_response,
            reduction_data_type,
            expected_result,
        )
