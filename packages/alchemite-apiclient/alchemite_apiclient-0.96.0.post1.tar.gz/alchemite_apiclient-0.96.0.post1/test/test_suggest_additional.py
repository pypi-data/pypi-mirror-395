import json
import os

from alchemite_apiclient.extensions import await_job


def test_suggest_additional(
    set_insecure_transport, api_models, steels_model, example_dir
):
    model_id = steels_model
    suggest_args = os.path.join(
        example_dir, "suggest_additional_args_steel.json"
    )

    # Get suggest additional input arguments
    with open(suggest_args, encoding="UTF-8") as f:
        suggest_additional_args = json.load(f)

    # Send suggest_additional request
    suggest_additional_job_id = api_models.models_id_suggest_additional_post(
        model_id, **suggest_additional_args
    )

    # Wait until the suggest_additional job has finished
    def get_suggest_additional_job_metadata():
        return api_models.models_id_suggest_additional_job_id_get(
            model_id, job_id=suggest_additional_job_id
        )

    suggest_additional_response = await_job(get_suggest_additional_job_metadata)
    assert "status" in suggest_additional_response
    assert suggest_additional_response["status"] == "done"
