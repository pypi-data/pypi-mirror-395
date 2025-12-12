import json
import os

from alchemite_apiclient.extensions import await_job


def test_suggest_historic(
    set_insecure_transport, api_models, steels_model, example_dir
):
    model_id = steels_model
    dataset_id = api_models.models_id_get(model_id)["training_dataset_id"]
    suggest_args = os.path.join(example_dir, "suggest_historic_args_steel.json")

    # Get suggest historic input arguments
    with open(suggest_args, encoding="UTF-8") as f:
        suggest_historic_args = json.load(f)

    suggest_historic_args["suggest_historic_request"]["datasetID"] = dataset_id

    # Send suggest_historic request
    suggest_historic_job_id = api_models.models_id_suggest_historic_post(
        model_id, **suggest_historic_args
    )

    # Wait until the suggest_historic job has finished
    def get_suggest_historic_job_metadata():
        return api_models.models_id_suggest_historic_job_id_get(
            model_id, job_id=suggest_historic_job_id
        )

    suggest_historic_response = await_job(get_suggest_historic_job_metadata)
    assert "status" in suggest_historic_response
    assert suggest_historic_response["status"] == "done"
